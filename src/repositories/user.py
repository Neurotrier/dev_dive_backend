from collections import Counter
from uuid import UUID

import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models import Answer, Question
from src.domain.models.user import User
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get_user(self, user_id: UUID) -> dict | None:
        user = await self.get_by_pk(id=user_id)
        if not user:
            return None

        stmt = (
            select(Question)
            .filter(Question.user_id == user_id)
            .order_by(Question.created_at.desc())
            .limit(3)
        )
        res = await self._session.execute(stmt)
        last_three_questions = res.scalars().all()

        stmt = (
            select(Answer)
            .filter(Answer.user_id == user_id)
            .order_by(Answer.created_at.desc())
            .limit(3)
        )
        res = await self._session.execute(stmt)
        last_three_answers = res.scalars().all()

        return {
            "user": user,
            "questions": last_three_questions,
            "answers": last_three_answers,
        }
