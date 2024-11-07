from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, relationship

from src.domain.models._vote import Vote

if TYPE_CHECKING:
    from .user import User


class Downvote(Vote):
    user: Mapped["User"] = relationship("User", back_populates="downvotes")

    __table_args__ = (
        UniqueConstraint("user_id", "source_id", name="uq_user_source_downvote"),
    )
