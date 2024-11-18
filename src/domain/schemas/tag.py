from uuid import UUID

from pydantic import BaseModel, Field


class TagCreate(BaseModel):
    name: str
    description: str | None


class TagID(BaseModel):
    id: UUID


class TagsWithFiltersGet(BaseModel):
    limit: int = Field(default=50, gt=0, le=150)
    offset: int = Field(default=1, gt=0)


class TagWithQuestionsCountGet(BaseModel):
    id: UUID
    name: str
    questions_count: int


class TagUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
