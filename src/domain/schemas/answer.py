from uuid import UUID

from pydantic import BaseModel


class AnswerCreate(BaseModel):
    user_id: UUID
    question_id: UUID
    content: str


class AnswerGet(BaseModel):
    id: UUID
    user_id: UUID
    question_id: UUID
    content: str
    created_at: str


class AnswerWithUserGet(BaseModel):
    id: UUID
    question_id: UUID
    content: str
    created_at: str
    user: dict


class AnswerUpdate(BaseModel):
    content: str | None = None
