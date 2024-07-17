from fastapi import WebSocket


class WebSocketConnectionManager:

    def __init__(self):
        self.group_to_active_connections: dict[int, list[WebSocket]] = {}

    async def connect_to_group(self, group_id: int, websocket: WebSocket):
        await websocket.accept()
        self.group_to_active_connections.get(group_id).append(websocket)

    def disconnect_from_group(self, group_id: int, websocket: WebSocket):
        self.group_to_active_connections.get(group_id).remove(websocket)

    async def broadcast_message_to_group_text(self, group_id: int, message: str):
        active_connections = self.group_to_active_connections.get(group_id)
        for connection in active_connections:
            await connection.send_text(message)

    async def broadcast_message_to_group_json(self, group_id: int, message: str):
        active_connections = self.group_to_active_connections.get(group_id)
        for connection in active_connections:
            await connection.send_text(message)
