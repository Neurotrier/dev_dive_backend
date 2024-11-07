import bcrypt
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.domain.models.user import User
from src.managers import RedisManager
from src.repositories.base import BaseRepository


class AuthRepository(BaseRepository[User]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def create_user(self, user: User) -> User | None:
        user.password = self.__hash_password(password=user.password)
        self._session.add(user)
        await self._session.commit()
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        try:
            stmt = select(User).where(User.email == email)
            res = await self._session.execute(stmt)
            user = res.scalar_one_or_none()
            return user
        except Exception:
            return None

    def check_is_valid(self, payload: dict, redis_manager: RedisManager) -> bool:
        jti = payload["jti"]
        if redis_manager.redisClient.hget(name=redis_manager.cache_name, key=jti):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This refresh token is not valid anymore!",
            )
        redis_manager.redisClient.hset(
            name=redis_manager.cache_name,
            key=jti,
            value="1",
        )

        return True

    def __hash_password(
        self,
        password: str,
    ) -> bytes:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)
