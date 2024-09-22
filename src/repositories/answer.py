from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.answer import Answer
from src.repositories.base import BaseRepository


class AnswerRepository(BaseRepository[Answer]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Answer)
