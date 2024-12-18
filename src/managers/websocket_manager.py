from fastapi import WebSocket


class WebsocketManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, chat_message: dict):
        chat_message["id"] = str(chat_message["id"])
        chat_message["user"]["id"] = str(chat_message["user"]["id"])
        for connection in self.active_connections:
            await connection.send_text(str(chat_message))


websocket_manager = WebsocketManager()
