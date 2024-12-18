import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.models.base import Base

if TYPE_CHECKING:
    from .question import Question
    from .user import User


class Answer(Base):
    content: Mapped[str] = mapped_column(String(1000))

    question_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("question.id", ondelete="CASCADE")
    )
    question: Mapped["Question"] = relationship("Question", back_populates="answers")

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
    user: Mapped["User"] = relationship("User", back_populates="answers")
