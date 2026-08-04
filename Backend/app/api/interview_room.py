from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user

from app.services.interview_room_service import (
    interview_room_service,
)


router = APIRouter(
    prefix="/interview",
    tags=["Interview Room"]
)



@router.post("/{interview_id}/room/create")
def create_interview_room(
    interview_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):

    try:

        room = (
            interview_room_service
            .create_room(
                db,
                interview_id
            )
        )


        return {

            "success": True,

            "room": {
                "id": room.id,
                "room_name": room.room_name,
                "livekit_url": room.livekit_url,
                "status": room.status,
            }

        }


    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )




@router.post("/{interview_id}/room/start")
def start_room(
    interview_id:int,
    db:Session = Depends(get_db),
    user = Depends(get_current_user),
):


    room = (
        interview_room_service
        .start_room(
            db,
            interview_id
        )
    )


    return {

        "success":True,

        "status":room.status,

        "started_at":room.started_at,

    }





@router.post("/{interview_id}/room/end")
def end_room(
    interview_id:int,
    db:Session = Depends(get_db),
    user = Depends(get_current_user),
):


    room = (
        interview_room_service
        .end_room(
            db,
            interview_id
        )
    )


    return {

        "success":True,

        "status":room.status,

        "duration_seconds":
            room.duration_seconds,

    }




@router.get("/{interview_id}/room")
def get_room(
    interview_id:int,
    db:Session = Depends(get_db),
    user = Depends(get_current_user),
):


    room = (
        interview_room_service
        .get_room(
            db,
            interview_id
        )
    )


    if not room:

        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )


    return {

        "success":True,

        "room": {

            "id":room.id,

            "room_name":
                room.room_name,

            "livekit_url":
                room.livekit_url,

            "status":
                room.status,

        }

    }
