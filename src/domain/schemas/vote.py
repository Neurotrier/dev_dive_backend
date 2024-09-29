from uuid import UUID

from pydantic import BaseModel


class VoteCreate(BaseModel):
    source_id: UUID
    user_id: UUID


class VoteGet(BaseModel):
    id: UUID
    source_id: UUID
    user_id: UUID


class UpvoteCreate(VoteCreate):
    pass


class DownvoteCreate(VoteCreate):
    pass


class UpvoteGet(VoteGet):
    pass


class DownvoteGet(VoteGet):
    pass
