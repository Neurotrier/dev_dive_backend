from uuid import UUID

from pydantic import BaseModel


class VoteCreate(BaseModel):
    source_id: UUID
    user_id: UUID


class UpvoteCreate(VoteCreate):
    pass


class DownvoteCreate(VoteCreate):
    pass
