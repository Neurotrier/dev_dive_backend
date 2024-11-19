from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator, BaseModel

from src.domain.schemas._validators import check_email, check_password, check_username


class AuthSignup(BaseModel):
    username: Annotated[str, AfterValidator(check_username)]
    password: Annotated[str, AfterValidator(check_password)]
    email: Annotated[str, AfterValidator(check_email)]


class AuthSignin(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user_id: UUID
