from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from src.db.session import DBSession
from src.domain.schemas.tag import TagCreate, TagsWithFiltersGet, TagUpdate
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
            status_code=status.HTTP_400_BAD_REQUEST,
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    else:
        return response


@router.get("/", status_code=status.HTTP_200_OK)
async def get_tags(
    db: DBSession,
    limit: Optional[int] = Query(50, gt=0),
    offset: Optional[int] = Query(1, gt=0),
):
    _service = TagService(session=db)
    filters = TagsWithFiltersGet(
        limit=limit,
        offset=offset,
    )
    response = await _service.get_tags(filters=filters)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tags not found"
        )
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not update tag"
        )
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    else:
        return response
