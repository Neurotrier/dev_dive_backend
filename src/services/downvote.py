from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.downvote import Downvote
from src.domain.schemas.vote import DownvoteCreate
from src.repositories.downvote import DownvoteRepository


class DownvoteService:
    def __init__(self, session: AsyncSession):
        self.repository = DownvoteRepository(session)

    async def create_downvote(self, data: DownvoteCreate):
        input_data = Downvote(**data.dict())
        downvote = await self.repository.add(record=input_data)
        await self.repository.commit()
        return downvote

    async def get_downvote(self, vote_id: UUID):
        downvote = await self.repository.get_by_pk(pk=vote_id)
        return downvote

    async def delete_downvote(self, vote_id: UUID):
        downvote_id = await self.repository.delete(id=vote_id)
        await self.repository.commit()
        return downvote_id
