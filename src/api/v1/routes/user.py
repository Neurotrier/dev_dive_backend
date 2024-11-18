from typing import Annotated, Optional, Union
from uuid import UUID

from fastapi import APIRouter, Depends, Form, HTTPException, Path, UploadFile, status

from src.db.session import DBSession
from src.domain.schemas.user import UserPoliciesUpdate, UserUpdate
from src.services.auth import AuthService
from src.services.user import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
)
async def get_user(
    db: DBSession,
    user_id: Annotated[UUID, Path()],
):
    _service = UserService(session=db)
    response = await _service.get_user_personal_data(user_id=user_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found"
        )
    else:
        return response


@router.patch(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
)
async def update_user(
    db: DBSession,
    user_id: Annotated[UUID, Path()],
    is_owner: Annotated[bool, Depends(AuthService.is_owner)],
    _: Annotated[bool, Depends(AuthService.access_jwt_required)],
    image: Optional[UploadFile] = None,
    username: Annotated[Union[str, None], Form()] = None,
    info: Annotated[Union[str, None], Form()] = None,
):
    if not is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    _service = UserService(session=db)

    data = UserUpdate(username=username, info=info)

    response = await _service.update_user(user_id=user_id, data=data, image=image)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    else:
        return response


@router.patch("/{user_id}/policies/", status_code=status.HTTP_200_OK)
async def update_user_policies(
    db: DBSession,
    user_id: Annotated[UUID, Path()],
    is_moderator: Annotated[bool, Depends(AuthService.is_moderator)],
    _: Annotated[bool, Depends(AuthService.access_jwt_required)],
    data: UserPoliciesUpdate,
):
    if not is_moderator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    _service = UserService(session=db)

    response = await _service.update_user_policies(user_id=user_id, data=data)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    else:
        return response


@router.delete(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    db: DBSession,
    user_id: Annotated[UUID, Path()],
    is_owner: Annotated[bool, Depends(AuthService.is_owner)],
    is_moderator: Annotated[bool, Depends(AuthService.is_moderator)],
    _: Annotated[bool, Depends(AuthService.access_jwt_required)],
):
    if not is_owner and not is_moderator:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    _service = UserService(session=db)

    response = await _service.delete_user(user_id=user_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    else:
        return response
