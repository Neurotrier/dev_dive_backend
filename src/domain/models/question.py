import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.models import Base

if TYPE_CHECKING:
    from .user import User


class Question(Base):
    tags = relationship("Tag", secondary="question_tag", back_populates="questions")
    content: Mapped[str] = mapped_column(String(1000))

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User")
