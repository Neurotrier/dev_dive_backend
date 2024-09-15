import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr

from src.models.base import Base

if TYPE_CHECKING:
    from .user import User


class Vote(Base):
    __abstract__ = True

    @declared_attr
    def source_id(cls) -> Mapped[uuid.UUID]:
        return mapped_column(nullable=False)

    @declared_attr
    def user_id(cls) -> Mapped[uuid.UUID]:
        return mapped_column(ForeignKey("user.id"))

    @declared_attr
    def user(cls) -> Mapped["User"]:
        return relationship("User")


