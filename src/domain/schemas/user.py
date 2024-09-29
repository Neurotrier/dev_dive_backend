import uuid

from pydantic import BaseModel


class UserGet(BaseModel):
    id: uuid.UUID
    username: str | None
    info: str | None
    email: str
    reputation: int


class UserUpdate(BaseModel):
    username: str | None = None
    info: str | None = None
