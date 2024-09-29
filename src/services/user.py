from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import User
from src.domain.schemas.auth import AuthSignup
from src.domain.schemas.user import UserGet, UserUpdate
from src.repositories.user import UserRepository


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def get_user(self, user_id: UUID):
        user = await self.repository.get_user(user_id=user_id)
        return user

    async def update_user(self, user_id: UUID, data: UserUpdate):
        user = await self.repository.update(
            data.dict(),
            id=user_id,
        )
        await self.repository.commit()
        return user
