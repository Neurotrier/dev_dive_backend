from typing import Optional
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logger import logger
from src.domain.schemas.user import UserUpdate
from src.managers import minio_manager
from src.repositories.user import UserRepository


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def get_user(self, user_id: UUID):
        user = await self.repository.get_user(user_id=user_id)
        return user

    async def update_user(
        self, user_id: UUID, data: UserUpdate, image: Optional[UploadFile] = None
    ):
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
            return user

        except Exception as e:
            logger.error(str(e))
            await self.repository.rollback()
