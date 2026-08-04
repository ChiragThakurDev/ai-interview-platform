# app/api/livekit.py

from fastapi import (
    APIRouter,
    Depends,
)

from app.core.config import settings

from app.dependencies.auth import (
    get_current_user,
)

from app.models.user import User

from app.services.livekit_service import (
    LiveKitService,
)


router = APIRouter(
    prefix="/livekit",
    tags=["LiveKit"],
)


livekit_service = LiveKitService()


# =====================================================
# Generate LiveKit Token
# =====================================================

@router.post(
    "/token/{interview_id}"
)
def generate_livekit_token(
    interview_id: int,
    current_user: User = Depends(
        get_current_user
    ),
):

    room_name = (
        f"interview-room-{interview_id}"
    )


    token = livekit_service.create_token(
        room_name=room_name,
        participant_identity=str(
            current_user.id
        ),
        participant_name=current_user.name,
    )


    return {
        "success": True,
        "room": room_name,
        "token": token,
        "url": settings.livekit_url,
        "participant": {
            "id": current_user.id,
            "name": current_user.name,
        },
    }
