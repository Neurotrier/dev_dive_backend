from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.role import Role

from .base import Base


class User(Base):
    username: Mapped[str] = mapped_column(String(30), nullable=False)
    info: Mapped[str] = mapped_column(String(200), nullable=True)
    password: Mapped[bytes]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    role: Mapped[Role] = mapped_column(default=Role.USER)
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    reputation: Mapped[int] = mapped_column(Integer, default=0)
    image_url: Mapped[str] = mapped_column(String(200), nullable=True)
