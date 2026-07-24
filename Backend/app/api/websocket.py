from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.services.coding_interview_service import CodingInterviewService
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

    db: Session = SessionLocal()

    service = CodingInterviewService(db)

    try:

        while True:

            data = await websocket.receive_json()

            if data["type"] == "submit_code":

                result = service.submit_code(
                    question_id=data["question_id"],
                    language=data["language"],
                    code=data["code"],
                )

                await manager.send_message(
                    interview_id,
                    {
                        "type": "submission_result",
                        **result,
                    },
                )

            else:

                await manager.send_message(
                    interview_id,
                    {
                        "type": "error",
                        "message": "Unknown message type",
                    },
                )

    except WebSocketDisconnect:

        manager.disconnect(interview_id)

    finally:

        db.close()
