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


class AnswerUpdate(BaseModel):
    content: str | None = None
