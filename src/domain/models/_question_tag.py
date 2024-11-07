import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.models.base import Base


class QuestionTag(Base):
    __tablename__ = "question_tag"
    question_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("question.id", ondelete="CASCADE")
    )
    tag_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("tag.id", ondelete="CASCADE"))
