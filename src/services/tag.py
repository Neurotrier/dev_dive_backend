from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import Tag
from src.domain.schemas.tag import TagCreate, TagUpdate
from src.repositories.tag import TagRepository


class TagService:
    def __init__(self, session: AsyncSession):
        self.repository = TagRepository(session)

    async def create_tag(self, data: TagCreate):
        input_data = Tag(**data.dict())
        tag = await self.repository.add(record=input_data)
        await self.repository.commit()
        return tag

    async def get_tag(self, tag_id: UUID):
        tag = await self.repository.get_tag_with_questions(tag_id=tag_id)
        return tag

    async def update_tag(self, tag_id: UUID, data: TagUpdate):
        tag = await self.repository.update(
            data.dict(),
            id=tag_id,
        )
        await self.repository.commit()
        return tag

    async def delete_tag(self, tag_id: UUID):
        tag_id = await self.repository.delete_tag(tag_id=tag_id)
        await self.repository.commit()
        return tag_id
