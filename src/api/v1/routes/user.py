from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from src.db.session import DBSession
from src.domain.schemas.user import UserUpdate
from src.services.auth import AuthService
from src.services.user import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(AuthService.access_jwt_required)],
)


@router.get(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
)
async def get_user(
    db: DBSession,
    user_id: Annotated[UUID, Path()],
):
    _service = UserService(session=db)
    response = await _service.get_user(user_id=user_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    else:
        return response


@router.patch(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
)
async def update_user(db: DBSession, user_id: Annotated[UUID, Path()], data: UserUpdate):
    _service = UserService(session=db)

    response = await _service.update_user(user_id=user_id, data=data)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    else:
        return response
