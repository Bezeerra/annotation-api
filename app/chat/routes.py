import uuid
from typing import Annotated

from fastapi import WebSocket, APIRouter, Depends
from orjson import orjson
from starlette.websockets import WebSocketDisconnect

from app.chat.schema import MessageChat
from app.context import RequestContext, get_context, get_context_websocket, WebSocketContext
# from app.kafka_service import send_message
# from app.es_service import get_history
from app.utils import create_response, ensure_uuid

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)

    async def send_personal_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            for websocket in self.active_connections[user_id]:
                await websocket.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/{user_id}")
async def websocket_chat(
    websocket: WebSocket,
    user_id: str,
    context: Annotated[WebSocketContext, Depends(get_context_websocket)],
):
    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data_obj = orjson.loads(data)
            data_obj["message_id"] = str(uuid.uuid4())
            message = MessageChat.from_dict(data_obj)
            if message.text != "start":
                await send_message(context.settings, "live_chat", message.to_string)
            await manager.send_personal_message(message.text, message.receiver)
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
        print(f"WebSocket disconnected for user {user_id}")


@router.get("/history/{sender}/{receiver}")
async def get_history_chat(
    sender: str, receiver: str, context: Annotated[RequestContext, Depends(get_context)]
):
    history = await get_history(context.settings, sender, receiver)
    return await create_response(
        content={"history": history}, status_code=200
    )
