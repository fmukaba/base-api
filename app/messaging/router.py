from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.messaging.schemas import Message
from app.messaging.websocket_connection_manager import WebSocketConnectionManager

router = APIRouter(
    prefix="/ws",
    tags=["ws"],
    responses={
        101: {"description": "Switching Protocols"},
        404: {"description": "Not found"}
    }
)

manager = WebSocketConnectionManager()


@router.websocket("/messages/{client_id}/{group_id}")
async def send_message(client_id: int, group_id: int, websocket: WebSocket):
    await manager.connect_to_group(group_id, websocket)
    try:
        while True:
            data: Message = await websocket.receive_json()
            await manager.broadcast_message_to_group_json(group_id, data.message)
    except WebSocketDisconnect:
        manager.disconnect_from_group(group_id, websocket)
        print(f"Client {client_id} has left the group {group_id}.")
