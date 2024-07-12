from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websocket.connection_manager import ConnectionManager
from app.websocket.schemas import Message

router = APIRouter(
    prefix="/ws",
    tags=["ws"],
    responses={
        101: {"description": "Switching Protocols"},
        404: {"description": "Not found"}
    }
)

manager = ConnectionManager()


@router.websocket("/messages/{client_id}/{group_id}")
async def send_message(client_id: int, group_id: int, websocket: WebSocket):
    await manager.connect_to_group(group_id, websocket)
    try:
        while True:
            data: Message = await websocket.receive_json()
            await manager.broadcast_message_to_group_json(group_id, data.message)
    except WebSocketDisconnect:
        manager.disconnect_from_group(group_id, websocket)
        await manager.broadcast_message_to_group_text(group_id, f"Client {client_id} left the chat {group_id}")
