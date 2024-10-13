from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.models.base import Base


class Tag(Base):
    name: Mapped[str] = mapped_column(String(20), unique=True)
    description: Mapped[str] = mapped_column(String(200))

    questions = relationship(
        "Question", secondary="question_tag", back_populates="tags"
    )
