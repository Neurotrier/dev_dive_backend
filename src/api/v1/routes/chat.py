import json
from typing import Annotated
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    WebSocket,
    WebSocketDisconnect,
    status,
)

from src.db.session import DBSession
from src.domain.schemas.chat import RecentChatMessagesFiltersGet
from src.managers.websocket_manager import websocket_manager
from src.services.auth import AuthService
from src.services.chat import ChatService
from src.services.user import UserService

router = APIRouter(tags=["chat"], prefix="/chat")


@router.websocket("/{user_id}/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: UUID,
    db: DBSession,
):
    _service_chat = ChatService(session=db)
    _service_user = UserService(session=db)

    await websocket_manager.connect(websocket)
    try:
        while True:
            user = await _service_user.get_user(user_id)
            data = await websocket.receive_text()
            if not data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Empty message"
                )
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )
            chat_message = await _service_chat.create_chat_message(
                message=json.loads(data)["data"], user_id=user.id
            )
            message = {
                "data": json.loads(data)["data"],
                "user_id": str(user.id),
                "username": user.username,
                "created_at": chat_message.created_at.isoformat(),
            }
            await websocket_manager.broadcast(
                current_connection=websocket, message=message
            )
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
    except HTTPException as e:
        raise e


@router.get("/")
async def get_recent_chat_messages(
    db: DBSession,
    _: Annotated[bool, Depends(AuthService.access_jwt_required)],
    limit: int = Query(50),
    offset: int = Query(1),
):
    _service = ChatService(session=db)
    filters = RecentChatMessagesFiltersGet(limit=limit, offset=offset)
    response = await _service.get_recent_chat_messages(filters=filters)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat messages not found"
        )
    else:
        return response
