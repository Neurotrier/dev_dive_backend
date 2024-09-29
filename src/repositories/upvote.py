from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.upvote import Upvote
from src.repositories.base import BaseRepository


class UpvoteRepository(BaseRepository[Upvote]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Upvote)
