from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from src.db.session import DBSession
from src.domain.schemas.question import QuestionCreate, QuestionUpdate
from src.services.auth import AuthService
from src.services.question import QuestionService

router = APIRouter(
    prefix="/questions",
    tags=["questions"],
    dependencies=[Depends(AuthService.access_jwt_required)],
)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
)
async def create_question(db: DBSession, data: QuestionCreate):
    _service = QuestionService(session=db)

    response = await _service.create_question(data=data)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create question",
        )
    else:
        return response


@router.get(
    "/{question_id}/",
    status_code=status.HTTP_200_OK,
)
async def get_question(db: DBSession, question_id: Annotated[UUID, Path()]):
    _service = QuestionService(session=db)

    response = await _service.get_question(question_id=question_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    else:
        return response


@router.patch(
    "/{question_id}/",
    status_code=status.HTTP_200_OK,
)
async def update_question(
    db: DBSession, question_id: Annotated[UUID, Path()], data: QuestionUpdate
):
    _service = QuestionService(session=db)

    response = await _service.update_question(question_id=question_id, data=data)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    else:
        return response


@router.delete(
    "/{question_id}/",
    status_code=status.HTTP_200_OK,
)
async def delete_question(db: DBSession, question_id: Annotated[UUID, Path()]):
    _service = QuestionService(session=db)

    response = await _service.delete_question(question_id=question_id)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    else:
        return response
