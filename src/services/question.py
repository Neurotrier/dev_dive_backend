from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import Question
from src.domain.schemas.question import (
    QuestionCreate,
    QuestionGet,
    QuestionsWithFiltersGet,
    QuestionUpdate,
    QuestionWithTagsGet,
)
from src.repositories.question import QuestionRepository


class QuestionService:
    def __init__(self, session: AsyncSession):
        self.repository = QuestionRepository(session)

    async def create_question(
        self, data: QuestionCreate
    ) -> Optional[QuestionWithTagsGet]:
        input_data = Question(**data.model_dump(exclude={"tags"}))
        question = await self.repository.add(record=input_data)
        tags = await self.repository.create_question_tags(
            tags=data.tags, question_id=question.id
        )
        if tags is None:
            return None

        await self.repository.commit()
        return QuestionWithTagsGet(
            id=question.id,
            user_id=question.user_id,
            content=question.content,
            tags=tags,
        )

    async def get_question_with_tags_and_answers(
        self, question_id: UUID
    ) -> Optional[dict]:
        return await self.repository.get_question_with_tags_and_answers(
            question_id=question_id
        )

    async def get_question(self, question_id: UUID) -> Optional[QuestionGet]:
        question = await self.repository.get_by_pk(id=question_id)
        if question:
            return QuestionRepository.to_schema(question)
        return None

    async def get_questions(self, filters: QuestionsWithFiltersGet) -> dict:
        questions = await self.repository.get_questions(filters=filters)
        return questions

    async def update_question(
        self, question_id: UUID, data: QuestionUpdate
    ) -> QuestionGet:
        await self.repository.update(
            data=data.model_dump(),
            id=question_id,
        )
        await self.repository.commit()
        return await self.repository.get_by_pk(id=question_id)

    async def delete_question(self, question_id: UUID) -> Optional[UUID]:
        question_id = await self.repository.delete_question(question_id=question_id)
        await self.repository.commit()
        return question_id
