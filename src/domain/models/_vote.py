import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from src.domain.models.base import Base

if TYPE_CHECKING:
    from .user import User


class Vote(Base):
    __abstract__ = True

    @declared_attr
    def source_id(cls) -> Mapped[uuid.UUID]:
        return mapped_column(nullable=False)

    @declared_attr
    def user_id(cls) -> Mapped[uuid.UUID]:
        return mapped_column(ForeignKey("user.id", ondelete="CASCADE"))

    @declared_attr
    def user(cls) -> Mapped["User"]:
        return relationship("User")
