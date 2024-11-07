from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer, load_only, selectinload

from src.domain.models import User
from src.domain.models.chat_message import ChatMessage
from src.domain.schemas.chat import RecentChatMessagesFiltersGet
from src.repositories.base import BaseRepository


class ChatRepository(BaseRepository[ChatMessage]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ChatMessage)

    async def get_recent_chat_messages(self, filters: RecentChatMessagesFiltersGet):
        stmt = select(ChatMessage).options(
            defer(ChatMessage.user_id),
            selectinload(ChatMessage.user).options(load_only(User.id, User.username)),
        )
        stmt = stmt.offset((filters.offset - 1) * filters.limit).limit(filters.limit)
        results = await self._session.execute(stmt)
        chat_messages = results.scalars().all()
        return chat_messages
