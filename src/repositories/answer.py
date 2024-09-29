from uuid import UUID

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import Downvote, Upvote
from src.domain.models.answer import Answer
from src.repositories.base import BaseRepository


class AnswerRepository(BaseRepository[Answer]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Answer)

    async def delete_answer(self, answer_id: UUID) -> UUID | None:
        record = await self.get_by_pk(id=answer_id)
        if record is not None:
            stmt = delete(Upvote).filter(Upvote.source_id == answer_id)
            await self._session.execute(stmt)

            stmt = delete(Downvote).filter(Downvote.source_id == answer_id)
            await self._session.execute(stmt)

            stmt = delete(self._model).filter_by(id=record.id)
            await self._session.execute(stmt)
            return record.id

        return None
