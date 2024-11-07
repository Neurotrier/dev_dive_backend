from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.logger import logger
from src.domain.models.chat_message import ChatMessage
from src.domain.schemas.chat import RecentChatMessagesFiltersGet
from src.repositories.chat import ChatRepository


class ChatService:
    def __init__(self, session: AsyncSession):
        self.repository = ChatRepository(session)

    async def create_chat_message(self, message: str, user_id: UUID):
        try:
            input_data = ChatMessage(message=message, user_id=user_id)
            chat_message = await self.repository.add(record=input_data)
            await self.repository.commit()
            return chat_message
        except Exception as e:
            logger.error(str(e))
            return None

    async def get_recent_chat_messages(self, filters: RecentChatMessagesFiltersGet):
        chat_messages = await self.repository.get_recent_chat_messages(filters=filters)
        return chat_messages
