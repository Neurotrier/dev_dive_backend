from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from src.db.session import DBSession
from src.domain.schemas.tag import TagCreate, TagUpdate
from src.services.auth import AuthService
from src.services.tag import TagService

router = APIRouter(
    prefix="/tags",
    tags=["tags"],
    dependencies=[Depends(AuthService.access_jwt_required)],
)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
)
async def create_tag(db: DBSession, data: TagCreate):
    _service = TagService(session=db)

    response = await _service.create_tag(data=data)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create tag",
        )
    else:
        return response


@router.get(
    "/{tag_id}/",
    status_code=status.HTTP_200_OK,
)
async def get_tag(db: DBSession, tag_id: Annotated[UUID, Path()]):
    _service = TagService(session=db)

    response = await _service.get_tag(tag_id=tag_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tag not found")
    else:
        return response


@router.patch(
    "/{tag_id}/",
    status_code=status.HTTP_200_OK,
)
async def update_tag(db: DBSession, tag_id: Annotated[UUID, Path()], data: TagUpdate):
    _service = TagService(session=db)

    response = await _service.update_tag(tag_id=tag_id, data=data)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tag not found")
    else:
        return response


@router.delete(
    "/{tag_id}/",
    status_code=status.HTTP_200_OK,
)
async def delete_tag(db: DBSession, tag_id: Annotated[UUID, Path()]):
    _service = TagService(session=db)

    response = await _service.delete_tag(tag_id=tag_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="tag not found")
    else:
        return response
