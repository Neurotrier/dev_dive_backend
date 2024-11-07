import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class ChatMessage(Base):
    __tablename__ = "chat_message"
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
    message: Mapped[str] = mapped_column(String(300), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="chat_messages")
