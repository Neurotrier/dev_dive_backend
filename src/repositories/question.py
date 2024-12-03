from uuid import UUID

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer, load_only, selectinload

from src.domain.models import Answer, Downvote, QuestionTag, Tag, Upvote, User
from src.domain.models.question import Question
from src.domain.schemas.question import QuestionGet, QuestionsWithFiltersGet
from src.repositories.base import BaseRepository


class QuestionRepository(BaseRepository[Question]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Question)

    async def create_question_tags(self, tags: list, question_id: UUID) -> list | None:
        stmt = select(Tag.id, Tag.name).where(Tag.id.in_(tags))
        res = await self._session.execute(stmt)
        tags = [dict(row) for row in res.mappings().all()]
        if not tags:
            return None

        question_tags = []
        for tag in tags:
            question_tags.append(QuestionTag(question_id=question_id, tag_id=tag["id"]))
        self._session.add_all(question_tags)

        return tags

    async def get_question_with_tags_and_answers(
        self, question_id: UUID
    ) -> dict | None:
        # load a question with tags and answers
        latest_answer_subquery = (
            select(func.max(Answer.updated_at))
            .where(Answer.question_id == Question.id)
            .correlate(Question)
            .scalar_subquery()
        )

        stmt = (
            select(Question)
            .options(
                selectinload(Question.tags).options(load_only(Tag.id, Tag.name)),
                defer(Question.user_id),
                selectinload(Question.user).options(load_only(User.id, User.username)),
                selectinload(Question.answers).options(
                    defer(Answer.user_id),
                    selectinload(Answer.user).options(
                        load_only(User.id, User.username)
                    ),
                ),
            )
            .where(Question.id == question_id)
            .order_by(latest_answer_subquery.desc())
        )

        res = await self._session.execute(stmt)
        question = res.scalar_one_or_none()
        if question:

            stmt = select(func.count(Upvote.user_id)).where(
                Upvote.source_id == question_id
            )
            res = await self._session.execute(stmt)
            upvotes = res.scalar_one_or_none()

            stmt = select(func.count(Downvote.user_id)).where(
                Downvote.source_id == question_id
            )
            res = await self._session.execute(stmt)
            downvotes = res.scalar_one_or_none()

            question.upvotes = upvotes
            question.downvotes = downvotes

            for answer in question.answers:
                stmt = select(func.count(Upvote.user_id)).where(
                    Upvote.source_id == answer.id
                )
                res = await self._session.execute(stmt)
                upvotes = res.scalar_one_or_none()

                stmt = select(func.count(Downvote.user_id)).where(
                    Downvote.source_id == answer.id
                )
                res = await self._session.execute(stmt)
                downvotes = res.scalar_one_or_none()

                answer.upvotes = upvotes
                answer.downvotes = downvotes

        return question

    async def get_questions(self, filters: QuestionsWithFiltersGet) -> dict:
        stmt = (
            select(Question)
            .distinct()
            .options(
                defer(Question.user_id),
                selectinload(Question.tags).options(load_only(Tag.id, Tag.name)),
                selectinload(Question.user).options(load_only(User.id, User.username)),
            )
        )

        if filters.user_id:
            stmt = stmt.where(Question.user_id == filters.user_id)

        if filters.tags:
            stmt = stmt.join(Question.tags).where(Tag.name.in_(filters.tags))

        if filters.content:
            stmt = (
                stmt.add_columns(
                    func.similarity(Question.content, text(":search_term")).label("sim")
                )
                .where(text("content % :search_term"))
                .params(search_term=filters.content)
                .order_by(
                    func.similarity(Question.content, text(":search_term"))
                    .params(search_term=filters.content)
                    .desc()
                )
            )

            total_query = (
                select(func.count(Question.id))
                .where(text("content % :search_term"))
                .params(search_term=filters.content)
            )

        else:
            total_query = select(func.count(Question.id))

        if filters.user_id:
            total_query = total_query.where(Question.user_id == filters.user_id)

        if filters.tags:
            total_query = total_query.join(Question.tags).where(
                Tag.name.in_(filters.tags)
            )

        total = await self._session.scalar(total_query)
        stmt = (
            stmt.order_by(Question.updated_at.desc())
            .offset((filters.offset - 1) * filters.limit)
            .limit(filters.limit)
        )

        results = await self._session.execute(stmt)
        questions = results.scalars().all()

        return {"total": total, "questions": questions}

    async def delete_question(self, question_id: UUID) -> UUID | None:
        record = await self.get_by_pk(id=question_id)
        if record is not None:
            await self._session.delete(record)
            await self._session.commit()

            return record.id

        return None

    @staticmethod
    def to_schema(question: Question) -> QuestionGet:
        return QuestionGet(
            id=question.id,
            content=question.content,
            user_id=question.user_id,
            created_at=question.created_at.isoformat(),
        )
