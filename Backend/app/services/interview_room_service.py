from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.interview_room import InterviewRoom
from app.models.interview import Interview
from app.core.config import settings
from app.services.livekit_service import LiveKitService


class InterviewRoomService:

    def __init__(self):
        self.livekit_service = LiveKitService()


    def create_room(
        self,
        db: Session,
        interview_id: int,
    ):

        interview = (
            db.query(Interview)
            .filter(
                Interview.id == interview_id
            )
            .first()
        )


        if not interview:
            raise Exception(
                "Interview not found"
            )


        existing_room = (
            db.query(InterviewRoom)
            .filter(
                InterviewRoom.interview_id == interview_id
            )
            .first()
        )


        if existing_room:
            return existing_room



        room_name = (
            self.livekit_service
            .create_room_name(
                interview_id
            )
        )


        room = InterviewRoom(
            interview_id=interview_id,
            room_name=room_name,
            livekit_url=settings.livekit_url,
            status="waiting",
        )


        db.add(room)
        db.commit()
        db.refresh(room)


        return room



    def start_room(
        self,
        db: Session,
        interview_id: int,
    ):

        room = (
            db.query(InterviewRoom)
            .filter(
                InterviewRoom.interview_id == interview_id
            )
            .first()
        )


        if not room:
            raise Exception(
                "Room not found"
            )


        room.status = "active"

        room.started_at = (
            datetime.now(timezone.utc)
        )


        db.commit()
        db.refresh(room)

        return room



    def end_room(
        self,
        db: Session,
        interview_id: int,
    ):

        room = (
            db.query(InterviewRoom)
            .filter(
                InterviewRoom.interview_id == interview_id
            )
            .first()
        )


        if not room:
            raise Exception(
                "Room not found"
            )


        room.status = "completed"

        room.ended_at = (
            datetime.now(timezone.utc)
        )


        if room.started_at:

            duration = (
                room.ended_at
                -
                room.started_at
            )

            room.duration_seconds = int(
                duration.total_seconds()
            )


        db.commit()
        db.refresh(room)

        return room



    def get_room(
        self,
        db: Session,
        interview_id: int,
    ):

        return (
            db.query(InterviewRoom)
            .filter(
                InterviewRoom.interview_id == interview_id
            )
            .first()
        )


interview_room_service = InterviewRoomService()
