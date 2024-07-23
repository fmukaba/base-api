from core.database import get_db
from fastapi import APIRouter, WebSocket, Depends
from messaging.crud import create_message
from messaging.schemas import Message
from messaging.websocket_connection_manager import WebSocketConnectionManager
from sqlalchemy.orm import Session
from starlette.websockets import WebSocketDisconnect

router = APIRouter(
    prefix="/ws",
    tags=["ws"],
    responses={404: {"description": "Not found"}},
)

websocket_manager = WebSocketConnectionManager()


@router.post("/create-message")
def router_test(data: Message, db: Session = Depends(get_db)):
    try:
        message = create_message(db, data)
        return message
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
