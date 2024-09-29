from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import Answer
from src.domain.schemas.answer import AnswerCreate, AnswerGet, AnswerUpdate
from src.repositories.answer import AnswerRepository


class AnswerService:
    def __init__(self, session: AsyncSession):
        self.repository = AnswerRepository(session)

    async def create_answer(self, data: AnswerCreate) -> Answer:
        input_data = Answer(**data.dict())
        answer = await self.repository.add(record=input_data)
        await self.repository.commit()
        return answer

    async def get_answer(self, answer_id: UUID) -> AnswerGet:
        return await self.repository.get_by_pk(id=answer_id)

    async def update_answer(self, answer_id: UUID, data: AnswerUpdate) -> Answer:
        answer = await self.repository.update(
            data.dict(),
            id=answer_id,
        )
        await self.repository.commit()
        return answer

    async def delete_answer(self, answer_id: UUID):
        answer_id = await self.repository.delete_answer(answer_id=answer_id)
        await self.repository.commit()
        return answer_id
