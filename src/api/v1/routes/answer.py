from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, status, HTTPException, Path

from src.db.session import DBSession
from src.domain.schemas.answer import AnswerCreate, AnswerUpdate
from src.services.answer import AnswerService

router = APIRouter(prefix="/answers", tags=["answers"])


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
)
async def create_answer(db: DBSession, data: AnswerCreate):
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

    response = await _service.get_answer(answer_id=answer_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="answer not found"
        )
    else:
        return response


@router.patch(
    "/{answer_id}/",
    status_code=status.HTTP_200_OK,
)
async def update_answer(
    db: DBSession, answer_id: Annotated[UUID, Path()], data: AnswerUpdate
):
    _service = AnswerService(session=db)

    response = await _service.update_answer(answer_id=answer_id, data=data)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="answer not found"
        )
    else:
        return response
