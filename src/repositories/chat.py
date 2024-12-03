from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import defer, load_only, selectinload

from src.domain.models import User
from src.domain.models.chat_message import ChatMessage
from src.domain.schemas.chat import ChatMessageGet, RecentChatMessagesFiltersGet
from src.domain.schemas.user import UserBase
from src.repositories.base import BaseRepository


class ChatRepository(BaseRepository[ChatMessage]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, ChatMessage)

    async def get_recent_chat_messages(self, filters: RecentChatMessagesFiltersGet):
        stmt = (
            select(ChatMessage)
            .options(
                defer(ChatMessage.user_id),
                defer(ChatMessage.updated_at),
                selectinload(ChatMessage.user).options(
                    load_only(User.id, User.username)
                ),
            )
            .order_by(ChatMessage.created_at.desc())
        )
        stmt = stmt.offset((filters.offset - 1) * filters.limit).limit(filters.limit)
        results = await self._session.execute(stmt)
        chat_messages = results.scalars().all()
        return chat_messages

    @staticmethod
    def to_schema(chat_message: ChatMessage, username: str) -> ChatMessageGet:
        return ChatMessageGet(
            id=chat_message.id,
            user=UserBase(id=chat_message.user_id, username=username),
            message=chat_message.message,
            created_at=chat_message.created_at.isoformat(),
        )
