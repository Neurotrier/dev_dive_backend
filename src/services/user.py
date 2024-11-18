from typing import Optional
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logger import logger
from src.domain.schemas.tag import TagWithQuestionsCountGet
from src.domain.schemas.user import (
    UserGet,
    UserPersonalDataGet,
    UserPoliciesUpdate,
    UserUpdate,
)
from src.managers import minio_manager
from src.repositories.answer import AnswerRepository
from src.repositories.question import QuestionRepository
from src.repositories.user import UserRepository


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def get_user_personal_data(
        self, user_id: UUID
    ) -> Optional[UserPersonalDataGet]:
        res = await self.repository.get_user_personal_data(user_id=user_id)
        if res:
            return UserPersonalDataGet(
                user=self.repository.to_schema(res["user"]),
                questions=[
                    QuestionRepository.to_schema(question)
                    for question in res["questions"]
                ],
                answers=[
                    AnswerRepository.to_schema(answer) for answer in res["answers"]
                ],
                tags=[
                    TagWithQuestionsCountGet(
                        id=tag[0], name=tag[1], questions_count=tag[2]
                    )
                    for tag in res["tags"]
                ],
                presigned_url=res["presigned_url"],
            )
        else:
            return None

    async def get_user(self, user_id: UUID) -> Optional[UserGet]:
        user = await self.repository.get_by_pk(id=user_id)
        if user:
            return self.repository.to_schema(user)
        return None

    async def update_user(
        self, user_id: UUID, data: UserUpdate, image: Optional[UploadFile] = None
    ) -> UserGet:
        try:
            image_url = None
            if image:
                object_name = f"{user_id}/{image.filename}"
                image_url = await minio_manager.upload_image(
                    object_name=object_name, file=image
                )

            user = await self.repository.update(
                {**data.model_dump(), "image_url": image_url},
                id=user_id,
            )

            await self.repository.commit()
            return self.repository.to_schema(user)

        except Exception as e:
            logger.error(str(e))
            await self.repository.rollback()

    async def update_user_policies(
        self, user_id: UUID, data: UserPoliciesUpdate
    ) -> UserGet:
        user = await self.repository.update(
            data=data.model_dump(),
            id=user_id,
        )
        await self.repository.commit()
        return self.repository.to_schema(user)

    async def update_user_reputation(self, user_id: UUID, reputation: int) -> UserGet:
        user = await self.repository.get_by_pk(id=user_id)

        user = await self.repository.update(
            id=user_id, data={"reputation": user.reputation + reputation}
        )
        await self.repository.commit()
        return self.repository.to_schema(user)

    async def delete_user(self, user_id: UUID) -> Optional[UUID]:
        user_id = await self.repository.delete_user(user_id=user_id)
        await self.repository.commit()
        return user_id
