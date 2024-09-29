from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer, load_only, selectinload

from src.domain.models import Answer, Downvote, QuestionTag, Tag, Upvote, User
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
        # load a question with tags and answers
        stmt = (
            select(Question)
            .options(
                selectinload(Question.tags).options(load_only(Tag.id, Tag.name)),
                defer(Question.user_id),
                selectinload(Question.user).options(load_only(User.username)),
                selectinload(Question.answers)
                .options(load_only(Answer.id, Answer.content))
                .options(selectinload(Answer.user).options(load_only(User.id, User.username))),
            )
            .where(Question.id == question_id)
        )

        res = await self._session.execute(stmt)
        question = res.scalar_one_or_none()
        if question:
            stmt = select(Upvote.user_id).where(Upvote.source_id == question_id)
            res = await self._session.execute(stmt)
            upvotes = [row[0] for row in res.fetchall()]

            stmt = select(Downvote.user_id).where(Upvote.source_id == question_id)
            res = await self._session.execute(stmt)
            downvotes = [row[0] for row in res.fetchall()]

            question.upvotes = upvotes
            question.downvotes = downvotes

            for answer in question.answers:
                stmt = select(Upvote.user_id).where(Upvote.source_id == answer.id)
                res = await self._session.execute(stmt)
                upvotes = [row[0] for row in res.fetchall()]

                stmt = select(Downvote.user_id).where(Downvote.source_id == answer.id)
                res = await self._session.execute(stmt)
                downvotes = [row[0] for row in res.fetchall()]

                answer.upvotes = upvotes
                answer.downvotes = downvotes

        return question

    async def delete_question(self, question_id: UUID) -> UUID | None:
        record = await self.get_by_pk(id=question_id)
        if record is not None:
            stmt = delete(Answer).filter(Answer.question_id == question_id)
            await self._session.execute(stmt)

            stmt = delete(QuestionTag).filter(QuestionTag.question_id == question_id)
            await self._session.execute(stmt)

            stmt = delete(Upvote).filter(Upvote.source_id == question_id)
            await self._session.execute(stmt)

            stmt = delete(Downvote).filter(Downvote.source_id == question_id)
            await self._session.execute(stmt)

            stmt = delete(self._model).filter_by(id=record.id)
            await self._session.execute(stmt)
            return record.id

        return None
