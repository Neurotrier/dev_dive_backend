from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from src.db.session import DBSession
from src.domain.schemas.answer import AnswerCreate, AnswerUpdate
from src.services.answer import AnswerService
from src.services.auth import AuthService

router = APIRouter(
    prefix="/answers",
    tags=["answers"],
)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
)
async def create_answer(
    db: DBSession,
    data: AnswerCreate,
    token: Annotated[str, Depends(AuthService.access_jwt_required)],
):
    is_owner = await AuthService.is_owner(data=data, token=token)
    if not is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )

    _service = AnswerService(session=db)
    response = await _service.create_answer(data=data)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create answer",
        )
    else:
        return response


@router.get(
    "/{answer_id}/",
    status_code=status.HTTP_200_OK,
)
async def get_answer(db: DBSession, answer_id: Annotated[UUID, Path()]):
    _service = AnswerService(session=db)
    response = await _service.get_answer_with_user(answer_id=answer_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found"
        )
    else:
        return response


@router.patch(
    "/{answer_id}/",
    status_code=status.HTTP_200_OK,
)
async def update_answer(
    db: DBSession,
    answer_id: Annotated[UUID, Path()],
    data: AnswerUpdate,
    is_answer_owner: Annotated[bool, Depends(AuthService.is_answer_owner)],
    _: Annotated[str, Depends(AuthService.access_jwt_required)],
):
    if not is_answer_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )

    _service = AnswerService(session=db)
    response = await _service.update_answer(answer_id=answer_id, data=data)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found"
        )
    else:
        return response


@router.delete(
    "/{answer_id}/",
    status_code=status.HTTP_200_OK,
)
async def delete_answer(
    db: DBSession,
    answer_id: Annotated[UUID, Path()],
    is_answer_owner: Annotated[bool, Depends(AuthService.is_answer_owner)],
    _: Annotated[str, Depends(AuthService.access_jwt_required)],
):
    if not is_answer_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )

    _service = AnswerService(session=db)
    response = await _service.delete_answer(answer_id=answer_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found"
        )
    else:
        return response
