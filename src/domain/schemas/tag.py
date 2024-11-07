from uuid import UUID

from pydantic import BaseModel

from src.domain.schemas.question import QuestionGet


class TagCreate(BaseModel):
    name: str
    description: str | None


class TagID(BaseModel):
    id: UUID


class TagGet(TagID):
    name: str
    description: str


class TagWithQuestionsGet(TagGet):
    questions: list[QuestionGet]


class TagWithQuestionsCountGet(BaseModel):
    id: UUID
    name: str
    questions_count: int


class TagUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
