import uuid

from sqlalchemy import ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.models import Base


class Image(Base):
    __tablename__ = "image"

    image: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE")
    )
