from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, BaseModel, Field

from src.domain.schemas._validators import check_tags


class QuestionCreate(BaseModel):
    user_id: UUID
    content: str
    tags: Annotated[list[UUID], AfterValidator(check_tags)]


class QuestionGet(BaseModel):
    id: UUID
    user_id: UUID
    content: str


class QuestionsWithFiltersGet(BaseModel):
    limit: int = Field(default=50, gt=0, le=150)
    offset: int = Field(default=1, gt=0)
    tags: list[str] | None = None
    content: str | None = None


class QuestionWithTagsGet(QuestionGet):
    tags: list


class QuestionUpdate(BaseModel):
    content: str | None = None
