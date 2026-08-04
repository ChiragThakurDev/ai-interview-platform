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
# Generate LiveKit Token  (interview-bound)
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


# =====================================================
# Generate LiveKit Token  (standalone room — no DB)
# POST /livekit/room-token/{room_code}
#
# room_code is a short alphanumeric string chosen by
# the host (e.g. "abc-1234").  No interview record
# is required — we just mint a JWT for that room.
# =====================================================

# =====================================================
# Generate LiveKit Token  (standalone room — no DB)
# POST /livekit/room-token/{room_code}
#
# Room-code prefix encodes type + capacity:
#   s-xxxxxx  →  single room, max 2 participants
#   g-xxxxxx  →  group  room, max 10 participants
# =====================================================

import secrets
from livekit import api as lk_api

@router.post(
    "/room-token/{room_code}"
)
async def generate_room_token(
    room_code: str,
    current_user: User = Depends(get_current_user),
):
    # Sanitise input
    safe_code = "".join(
        c for c in room_code.lower()
        if c.isalnum() or c == "-"
    )[:64]

    # Derive capacity from type segment of the code.
    # Prefixes: pub-s- / pub-g- / s- / g-
    # Strip leading "pub-" if present, then check s-/g-
    type_segment = safe_code[4:] if safe_code.startswith("pub-") else safe_code
    is_group   = type_segment.startswith("g-")
    max_people = 10 if is_group else 2
    room_name  = f"room-{safe_code}"

    # ── Count current participants via LiveKit server API ──────────────────
    try:
        lk = lk_api.LiveKitAPI(
            url    = settings.livekit_url,
            api_key    = settings.livekit_api_key,
            api_secret = settings.livekit_api_secret,
        )
        room_list = await lk.room.list_rooms(
            lk_api.ListRoomsRequest(names=[room_name])
        )
        await lk.aclose()

        rooms = room_list.rooms if room_list else []
        current_count = rooms[0].num_participants if rooms else 0

        if current_count >= max_people:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=403,
                detail=f"ROOM_FULL:{max_people}",
            )
    except Exception as exc:
        # If the room doesn't exist yet (first joiner) that's fine — proceed.
        # Re-raise only genuine 403s.
        err_str = str(exc)
        if "ROOM_FULL" in err_str:
            raise
        # Any other error (network, room not created yet) → let them in

    # Unique identity per session to prevent LiveKit duplicate-identity errors
    identity_suffix      = secrets.token_hex(4)
    participant_identity = f"{current_user.id}-{identity_suffix}"

    token = livekit_service.create_token(
        room_name=room_name,
        participant_identity=participant_identity,
        participant_name=current_user.name,
    )

    return {
        "success":    True,
        "room_code":  safe_code,
        "room":       room_name,
        "token":      token,
        "url":        settings.livekit_url,
        "participant": {
            "id":   current_user.id,
            "name": current_user.name,
        },
    }
