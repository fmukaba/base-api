import json

from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.orm import Session
from starlette.websockets import WebSocketDisconnect

from app.core.database import get_db
from app.messaging.crud import create_message
from app.messaging.models import Message
from app.messaging.websocket_connection_manager import WebSocketConnectionManager

router = APIRouter(
    prefix="/ws",
    tags=["ws"],
    responses={
        101: {"description": "Switching Protocols"},
        404: {"description": "Not found"}
    }
)

websocket_manager = WebSocketConnectionManager()


@router.post("/router/test")
def router_test(data: Message, db: Session = Depends(get_db)):
    try:
        new_message: Message = create_message(db, data)
        print(json.dumps(new_message))
    except Exception:
        raise


@router.post("/message/ws/")
async def message_websocket(client_id: int, group_id: int, websocket: WebSocket):
    try:
        await websocket_manager.connect(client_id, group_id, websocket)  # update or create
        while True:
            message: Message = await websocket.receive_json()
            await websocket_manager.broadcast(group_id, message)
            # await create_message(db, message)
    except WebSocketDisconnect:
        if websocket_manager.client_exists(client_id, group_id):
            websocket_manager.disconnect(client_id, group_id)
