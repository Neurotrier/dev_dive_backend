from fastapi import WebSocket


class WebsocketManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        pass

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_text(str(message))


websocket_manager = WebsocketManager()
