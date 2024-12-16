from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.role import Role

from .base import Base

if TYPE_CHECKING:
    from .answer import Answer
    from .chat_message import ChatMessage
    from .downvote import Downvote
    from .image import Image
    from .question import Question
    from .upvote import Upvote


class User(Base):
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    info: Mapped[str] = mapped_column(String(200), nullable=True)
    password: Mapped[bytes]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    role: Mapped[Role] = mapped_column(default=Role.USER)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    reputation: Mapped[int] = mapped_column(Integer, default=0)

    questions: Mapped["Question"] = relationship(
        "Question", back_populates="user", cascade="all, delete-orphan"
    )
    answers: Mapped["Answer"] = relationship(
        "Answer", back_populates="user", cascade="all, delete-orphan"
    )
    upvotes: Mapped["Upvote"] = relationship(
        "Upvote", back_populates="user", cascade="all, delete-orphan"
    )
    downvotes: Mapped["Downvote"] = relationship(
        "Downvote", back_populates="user", cascade="all, delete-orphan"
    )
    chat_messages: Mapped["ChatMessage"] = relationship(
        "ChatMessage", back_populates="user"
    )
    image: Mapped["Image"] = relationship("Image")
