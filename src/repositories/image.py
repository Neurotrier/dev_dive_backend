from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.image import Image
from src.repositories.base import BaseRepository


class ImageRepository(BaseRepository[Image]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Image)
