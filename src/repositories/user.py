from uuid import UUID

from sqlalchemy import delete, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from src.domain.models import Answer, ChatMessage, Question, QuestionTag, Tag
from src.domain.models.user import User
from src.domain.schemas.user import UserGet
from src.managers import minio_manager
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get_user_personal_data(self, user_id: UUID) -> dict | None:
        user = await self.get_by_pk(id=user_id)
        if not user:
            return None

        stmt = (
            select(Question)
            .filter(Question.user_id == user_id)
            .order_by(Question.updated_at.desc())
            .limit(3)
        )
        res = await self._session.execute(stmt)
        last_three_questions = res.scalars().all()

        stmt = (
            select(Answer)
            .filter(Answer.user_id == user_id)
            .order_by(Answer.updated_at.desc())
            .limit(3)
        )
        res = await self._session.execute(stmt)
        last_three_answers = res.scalars().all()

        question_alias = aliased(Question)
        question_tag_alias = aliased(QuestionTag)
        tag_alias = aliased(Tag)
        stmt = (
            select(
                tag_alias.id,
                tag_alias.name,
                func.count(question_alias.id).label("question_count"),
            )
            .select_from(question_alias)
            .join(
                question_tag_alias, question_alias.id == question_tag_alias.question_id
            )
            .join(tag_alias, question_tag_alias.tag_id == tag_alias.id)
            .where(question_alias.user_id == user_id)
            .group_by(tag_alias.id, tag_alias.name)
            .order_by(desc("question_count"))
            .limit(3)
        )
        res = await self._session.execute(stmt)
        best_three_tags = res.fetchall()

        if user.image_url:
            object_name = "/".join(user.image_url.split("/")[1:])
            presigned_url = minio_manager.generate_presigned_url(
                object_name=object_name
            )
        else:
            presigned_url = None

        stmt = select(func.count(Question.id)).where(Question.user_id == user_id)
        res = await self._session.execute(stmt)
        total_questions = res.scalar_one_or_none()

        stmt = select(func.count(Answer.id)).where(Answer.user_id == user_id)
        res = await self._session.execute(stmt)
        total_answers = res.scalar_one_or_none()

        return {
            "user": user,
            "total_questions": total_questions,
            "total_answers": total_answers,
            "questions": last_three_questions,
            "answers": last_three_answers,
            "tags": best_three_tags,
            "presigned_url": presigned_url,
        }

    async def delete_user(self, user_id: UUID) -> UUID | None:
        record = await self.get_by_pk(id=user_id)
        if record is not None:

            stmt = select(ChatMessage.id).filter(ChatMessage.user_id == user_id)
            res = await self._session.execute(stmt)
            chat_messages_id = res.scalars().all()

            stmt = delete(ChatMessage).filter(ChatMessage.id.in_(chat_messages_id))
            await self._session.execute(stmt)

            await self._session.delete(record)
            await self._session.commit()

            return user_id
        return None

    @staticmethod
    def to_schema(user: User):
        return UserGet(
            id=user.id,
            username=user.username,
            email=user.email,
            info=user.info,
            reputation=user.reputation,
            role=user.role,
            created_at=user.created_at.isoformat(),
        )
