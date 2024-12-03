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
        for connection in self.active_connections:
            await connection.send_text(str(chat_message))


websocket_manager = WebsocketManager()
