from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, load_only, defer

from src.domain.models import QuestionTag, Tag, User
from src.domain.models.question import Question
from src.repositories.base import BaseRepository


class QuestionRepository(BaseRepository[Question]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Question)

    async def create_question_tags(self, tags: list, question_id: UUID) -> list:
        question_tags = []
        for tag_id in tags:
            question_tags.append(QuestionTag(question_id=question_id, tag_id=tag_id))
        self._session.add_all(question_tags)

        stmt = select(Tag.id, Tag.name).where(Tag.id.in_(tags))
        res = await self._session.execute(stmt)
        return [dict(row) for row in res.mappings().all()]

    async def get_question(self, question_id: UUID) -> Question | None:
        stmt = (
            select(Question)
            .options(
                selectinload(Question.tags).options(load_only(Tag.id, Tag.name)),
                defer(Question.user_id),
            )
            .options(selectinload(Question.user).options(load_only(User.username)))
            .where(Question.id == question_id)
        )
        res = await self._session.execute(stmt)
        question = res.scalar_one_or_none()
        return question
