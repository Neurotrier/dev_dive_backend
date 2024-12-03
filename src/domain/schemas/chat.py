from uuid import UUID

from pydantic import BaseModel, Field

from src.domain.schemas.user import UserBase


class RecentChatMessagesFiltersGet(BaseModel):
    limit: int = Field(default=50, gt=0, le=150)
    offset: int = Field(default=1, gt=0)


class ChatMessageGet(BaseModel):
    id: UUID
    user: UserBase
    message: str
    created_at: str
