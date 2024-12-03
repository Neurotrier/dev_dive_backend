from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import Answer
from src.domain.schemas.answer import (
    AnswerCreate,
    AnswerGet,
    AnswerUpdate,
    AnswerWithUserGet,
)
from src.repositories.answer import AnswerRepository


class AnswerService:
    def __init__(self, session: AsyncSession):
        self.repository = AnswerRepository(session)

    async def create_answer(self, data: AnswerCreate) -> AnswerGet:
        input_data = Answer(**data.model_dump())
        answer = await self.repository.add(record=input_data)
        await self.repository.commit()
        return AnswerRepository.to_schema(answer)

    async def get_answer_with_user(
        self, answer_id: UUID
    ) -> Optional[AnswerWithUserGet]:
        answer = await self.repository.get_answer_with_user(answer_id=answer_id)
        if answer:
            user = {"user_id": answer.user.id, "username": answer.user.username}
            return AnswerWithUserGet(
                id=answer.id,
                content=answer.content,
                question_id=answer.question_id,
                created_at=answer.created_at.isoformat(),
                user=user,
            )
        return None

    async def get_answer(self, answer_id: UUID) -> Optional[AnswerGet]:
        answer = await self.repository.get_by_pk(id=answer_id)
        if answer:
            return AnswerRepository.to_schema(answer)
        return None

    async def update_answer(self, answer_id: UUID, data: AnswerUpdate) -> AnswerGet:
        answer = await self.repository.update(
            data=data.model_dump(),
            id=answer_id,
        )
        await self.repository.commit()
        return AnswerRepository.to_schema(answer)

    async def delete_answer(self, answer_id: UUID) -> Optional[UUID]:
        answer_id = await self.repository.delete_answer(answer_id=answer_id)
        await self.repository.commit()
        return answer_id
