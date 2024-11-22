from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from src.db.session import DBSession
from src.domain.schemas.vote import DownvoteCreate, UpvoteCreate
from src.services.auth import AuthService
from src.services.downvote import DownvoteService
from src.services.upvote import UpvoteService

router = APIRouter(
    prefix="/votes",
    tags=["votes"],
)


@router.post(
    "/upvote/",
    status_code=status.HTTP_200_OK,
)
async def create_upvote(
    db: DBSession,
    data: UpvoteCreate,
    token: Annotated[str, Depends(AuthService.access_jwt_required)],
):
    is_owner = await AuthService.is_owner(data=data, token=token)
    if not is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )

    _service = UpvoteService(session=db)
    response = await _service.create_upvote(data=data, session=db)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create upvote",
        )
    else:
        return response


@router.post(
    "/downvote/",
    status_code=status.HTTP_200_OK,
)
async def create_downvote(
    db: DBSession,
    data: DownvoteCreate,
    token: Annotated[str, Depends(AuthService.access_jwt_required)],
):
    is_owner = await AuthService.is_owner(data=data, token=token)
    if not is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )

    _service = DownvoteService(session=db)
    response = await _service.create_downvote(data=data, session=db)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create downvote",
        )
    else:
        return response


@router.get(
    "/upvote/{upvote_id}/",
    status_code=status.HTTP_200_OK,
)
async def get_upvote(db: DBSession, upvote_id: Annotated[UUID, Path()]):
    _service = UpvoteService(session=db)

    response = await _service.get_upvote(upvote_id=upvote_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Upvote not found"
        )
    else:
        return response


@router.get(
    "/downvote/{downvote_id}/",
    status_code=status.HTTP_200_OK,
)
async def get_downvote(db: DBSession, downvote_id: Annotated[UUID, Path()]):
    _service = DownvoteService(session=db)

    response = await _service.get_downvote(downvote_id=downvote_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Downvote not found"
        )
    else:
        return response


@router.delete(
    "/upvote/{upvote_id}/",
    status_code=status.HTTP_200_OK,
)
async def delete_upvote(
    db: DBSession,
    upvote_id: Annotated[UUID, Path()],
    is_upvote_owner: Annotated[bool, Depends(AuthService.is_upvote_owner)],
    _: Annotated[str, Depends(AuthService.access_jwt_required)],
):
    if not is_upvote_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )

    _service = UpvoteService(session=db)
    response = await _service.delete_upvote(upvote_id=upvote_id, session=db)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Upvote not found"
        )
    else:
        return response


@router.delete(
    "/downvote/{downvote_id}/",
    status_code=status.HTTP_200_OK,
)
async def delete_downvote(
    db: DBSession,
    downvote_id: Annotated[UUID, Path()],
    is_downvote_owner: Annotated[bool, Depends(AuthService.is_downvote_owner)],
    _: Annotated[str, Depends(AuthService.access_jwt_required)],
):
    if not is_downvote_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    _service = DownvoteService(session=db)

    response = await _service.delete_downvote(downvote_id=downvote_id, session=db)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Downvote not found"
        )
    else:
        return response
