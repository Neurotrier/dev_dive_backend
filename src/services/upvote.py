from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import Upvote
from src.domain.schemas.vote import UpvoteCreate
from src.repositories.upvote import UpvoteRepository


class UpvoteService:
    def __init__(self, session: AsyncSession):
        self.repository = UpvoteRepository(session)

    async def create_upvote(self, data: UpvoteCreate):
        input_data = Upvote(**data.dict())
        upvote = await self.repository.add(record=input_data)
        await self.repository.commit()
        return upvote

    async def get_upvote(self, vote_id: UUID):
        upvote = await self.repository.get_by_pk(id=vote_id)
        return upvote

    async def delete_upvote(self, vote_id: UUID):
        upvote_id = await self.repository.delete(id=vote_id)
        await self.repository.commit()
        return upvote_id
