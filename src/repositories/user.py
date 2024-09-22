import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.user import User
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def create_user(self, user: User) -> User | None:
        user.password = self.__hash_password(password=user.password)
        self._session.add(user)
        await self._session.commit()
        return user

    def __hash_password(
        self,
        password: str,
    ) -> bytes:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)
