import uuid
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.config import settings
from src.core.logger import logger
from src.core.role import Role
from src.db.session import DBSession
from src.domain.models import User
from src.domain.schemas.auth import AuthSignin, AuthSignup
from src.domain.schemas.user import UserGet
from src.managers import RedisManager
from src.repositories.answer import AnswerRepository
from src.repositories.auth import AuthRepository
from src.repositories.question import QuestionRepository
from src.repositories.user import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/signin/")


class AuthService:
    def __init__(self, session: AsyncSession):
        self.repository = AuthRepository(session)

    async def signup(self, data: AuthSignup) -> Optional[UserGet]:
        user = await self.repository.get_user_by_email(email=data.email)
        if user:
            return None
        input_data = User(**data.model_dump())
        user = await self.repository.create_user(input_data)
        await self.repository.commit()
        return UserRepository.to_schema(user)

    async def signin(self, data: OAuth2PasswordRequestForm) -> Optional[AuthSignin]:
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
            return AuthSignin(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type=settings.token_type,
                user_id=user.id,
            )
        return None

    async def refresh_token(
        self, refresh_token: str, redis_manager: RedisManager
    ) -> AuthSignin:
        try:
            payload = AuthService.decode_jwt(token=refresh_token)
            if payload.get("status") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Refresh jwt token is required",
                )

            is_valid = self.repository.check_is_valid(
                payload=payload, redis_manager=redis_manager
            )
            if is_valid:
                access_token = self.__encode_jwt(
                    payload=payload, expire_minutes=settings.access_token_ttl_min
                )
                refresh_token = self.__encode_jwt(
                    payload=payload,
                    expire_minutes=settings.refresh_token_ttl_min,
                    is_access=False,
                )
                return AuthSignin(
                    access_token=access_token,
                    refresh_token=refresh_token,
                    token_type=settings.token_type,
                    user_id=payload["user_id"],
                )
        except (
            jwt.ExpiredSignatureError,
            jwt.InvalidTokenError,
            jwt.DecodeError,
            jwt.InvalidTokenError,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid jwt token"
            )
        except Exception as e:
            logger.error(str(e))

    @classmethod
    def access_jwt_required(cls, token: str = Depends(oauth2_scheme)) -> bool:
        try:
            payload = cls.decode_jwt(token=token)
            if payload.get("status") != "access":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access jwt token is required",
                )
            return True
        except (
            jwt.ExpiredSignatureError,
            jwt.InvalidTokenError,
            jwt.DecodeError,
            jwt.InvalidTokenError,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid jwt token"
            )
        except Exception as e:
            logger.error("Error in access_jwt_required")
            logger.error(str(e))

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
    def decode_jwt(
        self,
        token: str,
        secret_key: str = settings.authjwt_secret_key,
        algorithm: str = settings.algorithm,
    ) -> dict:
        decoded = jwt.decode(
            token,
            key=secret_key,
            algorithms=[algorithm],
        )
        return decoded

    @classmethod
    async def is_owner(
        cls, request: Request, token: str = Depends(oauth2_scheme)
    ) -> bool:
        try:
            res = await request.json()
            user_id = res.get("user_id", None)
            if user_id is None:
                return False
            payload = cls.decode_jwt(token=token)
            if str(user_id) != payload["user_id"]:
                return False
            return True
        except (
            jwt.ExpiredSignatureError,
            jwt.InvalidTokenError,
            jwt.DecodeError,
            jwt.InvalidTokenError,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
            )
        except Exception as e:
            logger.error(str(e))

    @classmethod
    async def is_moderator(cls, token: str = Depends(oauth2_scheme)) -> bool:
        try:
            payload = cls.decode_jwt(token=token)
            if payload["role"] not in (Role.MODERATOR, Role.ADMIN):
                return False
            return True
        except (
            jwt.ExpiredSignatureError,
            jwt.InvalidTokenError,
            jwt.DecodeError,
            jwt.InvalidTokenError,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
            )
        except Exception as e:
            logger.error(str(e))

    @classmethod
    async def is_admin(cls, token: str = Depends(oauth2_scheme)) -> bool:
        try:
            payload = cls.decode_jwt(token=token)
            if payload["role"] != Role.ADMIN:
                return False
            return True
        except (
            jwt.ExpiredSignatureError,
            jwt.InvalidTokenError,
            jwt.DecodeError,
            jwt.InvalidTokenError,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
            )
        except Exception as e:
            logger.error(str(e))

    @classmethod
    async def is_question_owner(
        cls, question_id: uuid.UUID, db: DBSession, token: str = Depends(oauth2_scheme)
    ) -> bool:
        try:
            payload = cls.decode_jwt(token=token)
            question_repository = QuestionRepository(session=db)
            question = await question_repository.get_by_pk(id=question_id)
            if question is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
                )
            if str(question.user_id) != payload["user_id"]:
                return False
            return True
        except (
            jwt.ExpiredSignatureError,
            jwt.InvalidTokenError,
            jwt.DecodeError,
            jwt.InvalidTokenError,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(str(e))

    @classmethod
    async def is_answer_owner(
        cls, answer_id: uuid.UUID, db: DBSession, token: str = Depends(oauth2_scheme)
    ) -> bool:
        try:
            payload = cls.decode_jwt(token=token)
            answer_repository = AnswerRepository(session=db)
            answer = await answer_repository.get_by_pk(id=answer_id)
            if answer is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found"
                )
            if str(answer.user_id) != payload["user_id"]:
                return False
            return True
        except (
            jwt.ExpiredSignatureError,
            jwt.InvalidTokenError,
            jwt.DecodeError,
            jwt.InvalidTokenError,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(str(e))
