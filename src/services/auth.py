import uuid
from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from managers.redis_manager import RedisManager
from src.core.config import settings
from src.domain.models import User
from src.domain.schemas.auth import AuthSignup, TokenInfo
from src.repositories.auth import AuthRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin/")


class AuthService:
    def __init__(self, session: AsyncSession):
        self.repository = AuthRepository(session)

    async def signup(self, data: AuthSignup):
        user = await self.repository.get_user_by_email(email=data.email)
        if user:
            return None
        input_data = User(**data.dict())
        user = await self.repository.create_user(input_data)
        await self.repository.commit()
        return user

    async def signin(self, data: OAuth2PasswordRequestForm):
        user = await self.repository.get_user_by_email(email=data.username)
        if user:
            payload = self.__make_jwt_payload(user=user)
            access_token = self.__encode_jwt(
                payload=payload, expire_minutes=settings.access_token_ttl_min
            )
            refresh_token = self.__encode_jwt(
                payload=payload,
                expire_minutes=settings.refresh_token_ttl_min,
                is_access=False,
            )
            return TokenInfo(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type=settings.token_type,
            )
        return None

    async def refresh_token(self, refresh_token: str, redis_manager: RedisManager):
        payload = AuthService.__decode_jwt(token=refresh_token)
        if payload.get("status") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Refresh jwt token is required",
            )

        is_valid = self.repository.check_is_valid(payload=payload, redis_manager=redis_manager)
        if is_valid:
            access_token = self.__encode_jwt(
                payload=payload, expire_minutes=settings.access_token_ttl_min
            )
            refresh_token = self.__encode_jwt(
                payload=payload,
                expire_minutes=settings.refresh_token_ttl_min,
                is_access=False,
            )
            return TokenInfo(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type=settings.token_type,
            )

    @classmethod
    def access_jwt_required(cls, token: str = Depends(oauth2_scheme)):
        try:
            payload = cls.__decode_jwt(token=token)
            if payload.get("status") != "access":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access jwt token is required",
                )
        except (
            jwt.ExpiredSignatureError,
            jwt.InvalidTokenError,
            jwt.DecodeError,
            jwt.InvalidTokenError,
        ):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid jwt token")
        except Exception as e:
            raise e

    def __make_jwt_payload(self, user: User) -> dict:
        payload = {
            "user_id": str(user.id),
            "email": user.email,
            "role": str(user.role),
        }
        return payload

    def __encode_jwt(
        self,
        payload: dict,
        expire_minutes: int,
        private_key: str = settings.authjwt_secret_key,
        algorithm: str = settings.algorithm,
        is_access: bool = True,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.utcnow()
        if is_access:
            status = "access"
        else:
            status = "refresh"
        expire = now + timedelta(minutes=expire_minutes)
        jti = str(uuid.uuid4())
        to_encode.update(exp=expire, iat=now, jti=jti, status=status)

        encoded = jwt.encode(
            to_encode,
            key=private_key,
            algorithm=algorithm,
        )
        return encoded

    def __validate_password(
        self,
        password: str | bytes,
        hashed_password: bytes,
    ) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )

    @classmethod
    def __decode_jwt(
        self,
        token: str | bytes,
        secret_key: str = settings.authjwt_secret_key,
        algorithm: str = settings.algorithm,
    ) -> dict:
        decoded = jwt.decode(
            token,
            key=secret_key,
            algorithms=[algorithm],
        )
        return decoded
