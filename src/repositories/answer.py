from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer, load_only, selectinload

from src.domain.models import User
from src.domain.models.answer import Answer
from src.domain.schemas.answer import AnswerGet
from src.repositories.base import BaseRepository


class AnswerRepository(BaseRepository[Answer]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Answer)

    async def get_answer_with_user(self, answer_id: UUID) -> Answer | None:
        stmt = (
            select(Answer)
            .options(
                defer(Answer.user_id),
                selectinload(Answer.user).options(load_only(User.username)),
            )
            .where(Answer.id == answer_id)
        )

        res = await self._session.execute(stmt)
        answer = res.scalar_one_or_none()
        return answer

    async def delete_answer(self, answer_id: UUID) -> UUID | None:
        record = await self.get_by_pk(id=answer_id)
        if record is not None:
            await self._session.delete(record)
            await self._session.commit()

            return record.id

        return None

    @staticmethod
    def to_schema(answer: Answer) -> AnswerGet:
        return AnswerGet(
            id=answer.id,
            content=answer.content,
            user_id=answer.user_id,
            question_id=answer.question_id,
            created_at=answer.created_at.isoformat(),
        )
