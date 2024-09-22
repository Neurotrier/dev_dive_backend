from uuid import UUID
from pydantic import BaseModel


class QuestionCreate(BaseModel):
    user_id: UUID
    content: str
    tags: list[UUID]


class QuestionGet(BaseModel):
    id: UUID
    user_id: UUID
    content: str


class QuestionWithTagsGet(QuestionGet):
    tags: list


class QuestionUpdate(BaseModel):
    content: str | None = None
