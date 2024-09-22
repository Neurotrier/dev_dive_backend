from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, load_only, defer

from src.domain.models import Question, User
from src.domain.models.tag import Tag
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
