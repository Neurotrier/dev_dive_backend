from uuid import UUID

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer, load_only, selectinload

from src.domain.models import Question, QuestionTag, User
from src.domain.models.tag import Tag
from src.domain.schemas.tag import TagsWithFiltersGet
from src.repositories.base import BaseRepository


class TagRepository(BaseRepository[Tag]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Tag)

    async def get_tag_with_questions(self, tag_id: UUID) -> Tag:
        stmt = (
            select(Tag)
            .options(
                selectinload(Tag.questions)
                .options(
                    load_only(Question.id, Question.content, Question.created_at),
                    defer(Question.user_id),
                )
                .selectinload(Question.user)
                .options(load_only(User.id, User.username))
            )
            .where(Tag.id == tag_id)
        )

        res = await self._session.execute(stmt)
        tag = res.scalar_one_or_none()
        return tag

    async def get_tags(self, filters: TagsWithFiltersGet) -> dict:
        stmt = select(Tag)
        total_query = select(func.count(Tag.id))

        total = await self._session.scalar(total_query)

        stmt = stmt.offset((filters.offset - 1) * filters.limit).limit(filters.limit)

        results = await self._session.execute(stmt)
        tags = results.scalars().all()

        return {"total": total, "tags": tags}

    async def delete_tag(self, tag_id: UUID) -> UUID | None:
        record = await self.get_by_pk(id=tag_id)
        if record is not None:
            stmt = select(QuestionTag.question_id).filter(QuestionTag.tag_id == tag_id)
            res = await self._session.execute(stmt)
            questions_id = res.scalars().all()

            await self._session.delete(record)

            stmt = delete(Question).filter(Question.id.in_(questions_id))
            await self._session.execute(stmt)
            await self._session.commit()

            return record.id

        return None
