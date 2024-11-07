from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import JSONResponse

from src.core.logger import logger
from src.db.session import DBSession
from src.domain.schemas.auth import AuthSignup
from src.managers import RedisManager
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup/", status_code=status.HTTP_201_CREATED)
async def signup(
    data: AuthSignup,
    db: DBSession,
):
    _service = AuthService(session=db)
    try:
        response = await _service.signup(data=data)
        if response:
            return response
        else:
            print(logger.name)
            logger.error("User with this email already exists")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "User with this email already exists"},
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/signin/", status_code=status.HTTP_200_OK)
async def signin(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DBSession,
):
    _service = AuthService(session=db)
    try:
        response = await _service.signin(data=data)
        if response:
            return response
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": "User does not exist"},
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/refresh-token/", status_code=status.HTTP_200_OK)
async def refresh_token(
    db: DBSession,
    refresh: str = Header("refresh-token"),
):
    _service = AuthService(session=db)
    try:
        token = refresh[7:].strip()
        response = await _service.refresh_token(
            refresh_token=token, redis_manager=RedisManager()
        )
        return response
    except Exception as e:
        raise e
