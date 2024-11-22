from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from src.db.session import DBSession
from src.domain.schemas.question import (
    QuestionCreate,
    QuestionsWithFiltersGet,
    QuestionUpdate,
)
from src.services.auth import AuthService
from src.services.question import QuestionService

router = APIRouter(
    prefix="/questions",
    tags=["questions"],
)


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
)
async def create_question(
    db: DBSession,
    data: QuestionCreate,
    token: Annotated[str, Depends(AuthService.access_jwt_required)],
):
    is_owner = await AuthService.is_owner(data=data, token=token)
    if not is_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )

    _service = QuestionService(session=db)
    response = await _service.create_question(data=data)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create question",
        )
    else:
        return response


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def get_questions(
    db: DBSession,
    limit: Optional[int] = Query(50, gt=0),
    offset: Optional[int] = Query(1, gt=0),
    tags: list[Optional[str]] = Query(None),
    content: Optional[str] = Query(None),
):
    _service = QuestionService(session=db)
    filters = QuestionsWithFiltersGet(
        limit=limit, offset=offset, tags=tags, content=content
    )
    response = await _service.get_questions(filters=filters)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Questions not found"
        )
    else:
        return response


@router.get(
    "/{question_id}/",
    status_code=status.HTTP_200_OK,
)
async def get_question(db: DBSession, question_id: Annotated[UUID, Path()]):
    _service = QuestionService(session=db)
    response = await _service.get_question_with_tags_and_answers(
        question_id=question_id
    )
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )
    else:
        return response


@router.patch(
    "/{question_id}/",
    status_code=status.HTTP_200_OK,
)
async def update_question(
    db: DBSession,
    question_id: Annotated[UUID, Path()],
    data: QuestionUpdate,
    is_question_owner: Annotated[bool, Depends(AuthService.is_question_owner)],
    _: Annotated[str, Depends(AuthService.access_jwt_required)],
):
    if not is_question_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )

    _service = QuestionService(session=db)
    response = await _service.update_question(question_id=question_id, data=data)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )
    else:
        return response


@router.delete(
    "/{question_id}/",
    status_code=status.HTTP_200_OK,
)
async def delete_question(
    db: DBSession,
    question_id: Annotated[UUID, Path()],
    is_question_owner: Annotated[bool, Depends(AuthService.is_question_owner)],
    _: Annotated[str, Depends(AuthService.access_jwt_required)],
):
    if not is_question_owner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )

    _service = QuestionService(session=db)
    response = await _service.delete_question(question_id=question_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )
    else:
        return response
