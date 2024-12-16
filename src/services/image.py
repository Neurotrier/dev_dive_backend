from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import Image
from src.domain.schemas.image import ImageCreate
from src.repositories.image import ImageRepository


class ImageService:
    def __init__(self, session: AsyncSession):
        self.repository = ImageRepository(session)

    async def create_image(self, data: ImageCreate):
        input_data = Image(**data.model_dump())
        image = await self.repository.add(record=input_data)
        await self.repository.commit()
        return image

    async def get_image_by_user_id(self, user_id: UUID):
        images = await self.repository.get_by_filter(user_id=user_id)
        if not images:
            return None
        sorted_images = sorted(images, key=lambda img: img.created_at, reverse=True)
        return sorted_images[0]
