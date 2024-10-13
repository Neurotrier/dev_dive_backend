from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import Question
from src.domain.schemas.question import (
    QuestionCreate,
    QuestionsGetWithFilters,
    QuestionUpdate,
    QuestionWithTagsGet,
)
from src.repositories.question import QuestionRepository


class QuestionService:
    def __init__(self, session: AsyncSession):
        self.repository = QuestionRepository(session)

    async def create_question(self, data: QuestionCreate) -> QuestionWithTagsGet:
        input_data = Question(**data.dict(exclude={"tags"}))
        question = await self.repository.add(record=input_data)
        tags = await self.repository.create_question_tags(
            tags=data.tags, question_id=question.id
        )
        await self.repository.commit()
        return QuestionWithTagsGet(
            id=question.id,
            user_id=question.user_id,
            content=question.content,
            tags=tags,
        )

    async def get_question(self, question_id: UUID) -> Question:
        return await self.repository.get_question(question_id=question_id)

    async def get_questions(self, filters: QuestionsGetWithFilters):
        pages, items = await self.repository.get_questions(filters=filters)
        return items

    async def update_question(
        self, question_id: UUID, data: QuestionUpdate
    ) -> Question:
        await self.repository.update(
            data.dict(),
            id=question_id,
        )
        await self.repository.commit()
        return await self.repository.get_question(question_id=question_id)

    async def delete_question(self, question_id: UUID):
        question_id = await self.repository.delete_question(question_id=question_id)
        await self.repository.commit()
        return question_id
