import uuid

from pydantic import BaseModel


class ImageCreate(BaseModel):
    user_id: uuid.UUID
    image: bytes
