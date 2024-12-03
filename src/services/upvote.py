from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.domain.models import Upvote
from src.domain.schemas.vote import UpvoteCreate
from src.repositories.downvote import DownvoteRepository
from src.repositories.upvote import UpvoteRepository
from src.services.answer import AnswerService
from src.services.question import QuestionService
from src.services.user import UserService


class UpvoteService:
    def __init__(self, session: AsyncSession):
        self.repository = UpvoteRepository(session)

    async def create_upvote(self, data: UpvoteCreate, session: AsyncSession):
        fix_reputation = 0
        try:
            downvote_repository = DownvoteRepository(session=session)
            downvote = await downvote_repository.get_by_filter(**data.model_dump())
            if downvote:
                await downvote_repository.delete(id=downvote[0].id)
                await downvote_repository.commit()
                fix_reputation = -settings.DOWNVOTE_VALUE

            input_data = Upvote(**data.model_dump())
            upvote = await self.repository.add(record=input_data)

            question_service = QuestionService(session=session)
            question = await question_service.get_question(question_id=upvote.source_id)

            answer_service = AnswerService(session=session)
            answer = await answer_service.get_answer(answer_id=upvote.source_id)

            source = question or answer
            if source is None:
                await self.repository.rollback()
                return None

            user_service = UserService(session=session)
            await user_service.update_user_reputation(
                user_id=source.user_id,
                reputation=settings.UPVOTE_VALUE + fix_reputation,
            )

            await self.repository.commit()
            return upvote
        except Exception:
            return None

    async def get_upvote(self, upvote_id: UUID):
        upvote = await self.repository.get_by_pk(id=upvote_id)
        return upvote

    async def get_upvote_by_user_and_source(self, user_id: UUID, source_id: UUID):
        upvotes = await self.repository.get_by_filter(
            user_id=user_id, source_id=source_id
        )
        if not upvotes:
            return None
        return upvotes[0]

    async def delete_upvote(self, upvote_id: UUID, session: AsyncSession):
        upvote = await self.get_upvote(upvote_id)
        question_service = QuestionService(session=session)
        question = await question_service.get_question(question_id=upvote.source_id)

        answer_service = AnswerService(session=session)
        answer = await answer_service.get_answer(answer_id=upvote.source_id)

        source = question or answer
        if source is None:
            await self.repository.rollback()
            return None

        user_service = UserService(session=session)
        await user_service.update_user_reputation(
            user_id=source.user_id, reputation=-settings.UPVOTE_VALUE
        )

        upvote_id = await self.repository.delete(id=upvote_id)

        await self.repository.commit()
        return upvote_id
