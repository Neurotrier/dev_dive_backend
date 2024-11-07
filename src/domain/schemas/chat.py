from pydantic import BaseModel, Field


class RecentChatMessagesFiltersGet(BaseModel):
    limit: int = Field(default=50, gt=0, le=150)
    offset: int = Field(default=1, gt=0)
