from typing import Annotated, Union
from uuid import UUID

from pydantic import AfterValidator, BaseModel

from src.core.role import Role
from src.domain.schemas._validators import check_role
from src.domain.schemas.answer import AnswerGet
from src.domain.schemas.question import QuestionGet
from src.domain.schemas.tag import TagWithQuestionsCountGet


class UserGet(BaseModel):
    id: UUID
    username: str
    info: str | None
    email: str
    reputation: int


class UserPersonalDataGet(BaseModel):
    user: UserGet
    questions: list[QuestionGet]
    answers: list[AnswerGet]
    tags: list[TagWithQuestionsCountGet]
    presigned_url: str | None


class UserUpdate(BaseModel):
    user_id: UUID
    username: str | None = None
    info: str | None = None


class UserPoliciesUpdate(BaseModel):
    is_banned: bool | None = None
    role: Annotated[Union[Role, None], AfterValidator(check_role)]
