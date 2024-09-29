from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.downvote import Downvote
from src.repositories.base import BaseRepository


class DownvoteRepository(BaseRepository[Downvote]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Downvote)
