from fastapi import WebSocket
from pydantic import Json


class WebSocketConnectionManager:

    def __init__(self):
        # { group_id -> { client_id -> websocket } }
        self.group_to_active_connections: dict[int, dict[int: WebSocket]] = {}

    def group_exists(self, group_id: int):
        return group_id in self.group_to_active_connections

    def client_exists(self, client_id: int, group_id: int):
        if self.group_exists(group_id):
            return client_id in self.group_to_active_connections[group_id]
        return False

    async def connect(self, client_id: int, group_id: int, websocket: WebSocket):
        await websocket.accept()
        self.group_to_active_connections[group_id].update({client_id: websocket})

    def disconnect(self, client_id: int, group_id: int):
        self.group_to_active_connections.get(group_id).pop(client_id)

    async def broadcast(self, group_id: int, message: Json):
        active_connections = self.group_to_active_connections.get(group_id)
        for connection in active_connections:
            await active_connections[connection].send_json(message)
