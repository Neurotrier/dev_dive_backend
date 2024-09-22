from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.schemas.auth import AuthSignup
from src.domain.schemas.user import UserGet, UserUpdate
from src.domain.models import User
from src.repositories.user import UserRepository


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)

    async def create_user(self, data: AuthSignup):
        input_data = User(**data.dict())
        user = await self.repository.create_user(input_data)
        await self.repository.commit()
        return user

    async def get_user(self, user_id: UUID):
        user = await self.repository.get_by_pk(id=user_id)
        return UserGet(
            id=user.id,
            username=user.username,
            email=user.email,
            info=user.info,
            reputation=user.reputation,
        )

    async def update_user(self, user_id: UUID, data: UserUpdate):
        user = await self.repository.update(
            data.dict(),
            id=user_id,
        )
        await self.repository.commit()
        return user
