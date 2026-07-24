from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from app.websocket.connection_manager import manager

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/coding-interview/{interview_id}")
async def coding_interview_socket(
    websocket: WebSocket,
    interview_id: int,
):
    await manager.connect(
        interview_id,
        websocket,
    )

    try:
        while True:
            data = await websocket.receive_json()

            await manager.send_message(
                interview_id,
                {
                    "type": "echo",
                    "data": data,
                },
            )

    except WebSocketDisconnect:
        manager.disconnect(interview_id)
