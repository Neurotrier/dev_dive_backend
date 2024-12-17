from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, HTTPException, Path, Response, status

from src.db.session import DBSession
from src.services.image import ImageService

router = APIRouter(
    prefix="/images",
    tags=["images"],
)


@router.get(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
)
async def get_image_by_user_id(
    db: DBSession,
    user_id: Annotated[UUID, Path()],
):
    _service = ImageService(session=db)

    response = await _service.get_image_by_user_id(user_id=user_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )
    else:
        return Response(content=response.image, media_type="image/jpeg")
