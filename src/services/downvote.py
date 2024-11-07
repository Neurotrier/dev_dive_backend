from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.domain.models.downvote import Downvote
from src.domain.schemas.vote import DownvoteCreate
from src.repositories.downvote import DownvoteRepository
from src.repositories.upvote import UpvoteRepository
from src.services.answer import AnswerService
from src.services.question import QuestionService
from src.services.user import UserService


class DownvoteService:
    def __init__(self, session: AsyncSession):
        self.repository = DownvoteRepository(session)

    async def create_downvote(self, data: DownvoteCreate, session: AsyncSession):
        try:
            upvote_repository = UpvoteRepository(session=session)
            upvote = await upvote_repository.get_by_filter(**data.model_dump())
            if upvote:
                return None

            input_data = Downvote(**data.model_dump())
            downvote = await self.repository.add(record=input_data)

            question_service = QuestionService(session=session)
            question = await question_service.get_question(
                question_id=downvote.source_id
            )

            answer_service = AnswerService(session=session)
            answer = await answer_service.get_answer(answer_id=downvote.source_id)

            source = question or answer
            if source is None:
                await self.repository.rollback()
                return None

            user_service = UserService(session=session)
            await user_service.update_user_reputation(
                user_id=source.user_id, reputation=settings.DOWNVOTE_VALUE
            )

            await self.repository.commit()
            return downvote
        except Exception:
            return None

    async def get_downvote(self, downvote_id: UUID):
        downvote = await self.repository.get_by_pk(id=downvote_id)
        return downvote

    async def delete_downvote(self, downvote_id: UUID, session: AsyncSession):
        downvote = await self.get_downvote(downvote_id)
        question_service = QuestionService(session=session)
        question = await question_service.get_question(question_id=downvote.source_id)

        answer_service = AnswerService(session=session)
        answer = await answer_service.get_answer(answer_id=downvote.source_id)

        source = question or answer
        if source is None:
            await self.repository.rollback()
            return None

        user_service = UserService(session=session)
        await user_service.update_user_reputation(
            user_id=source.user_id, reputation=-settings.DOWNVOTE_VALUE
        )
        downvote_id = await self.repository.delete(id=downvote_id)
        await self.repository.commit()
        return downvote_id
