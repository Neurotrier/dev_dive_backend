from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logger import logger
from src.domain.models import Tag
from src.domain.schemas.tag import TagCreate, TagsWithFiltersGet, TagUpdate
from src.repositories.tag import TagRepository


class TagService:
    def __init__(self, session: AsyncSession):
        self.repository = TagRepository(session)

    async def create_tag(self, data: TagCreate):
        try:
            input_data = Tag(**data.model_dump())
            tag = await self.repository.add(record=input_data)
            await self.repository.commit()
            return tag
        except IntegrityError:
            return None
        except Exception as e:
            logger.error(str(e))

    async def get_tag(self, tag_id: UUID):
        tag = await self.repository.get_tag_with_questions(tag_id=tag_id)
        return tag

    async def get_tags(self, filters: TagsWithFiltersGet):
        questions = await self.repository.get_tags(filters=filters)
        return questions

    async def update_tag(self, tag_id: UUID, data: TagUpdate):
        try:
            tag = await self.repository.update(
                data=data.model_dump(),
                id=tag_id,
            )
            await self.repository.commit()
            return tag
        except IntegrityError:
            return None
        except Exception as e:
            logger.error(str(e))

    async def delete_tag(self, tag_id: UUID):
        tag_id = await self.repository.delete_tag(tag_id=tag_id)
        await self.repository.commit()
        return tag_id
