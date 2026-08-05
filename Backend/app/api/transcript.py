from typing import List

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user

from app.models.user import User

from app.schemas.transcript import (
    TranscriptCreate,
    TranscriptUpdate,
    TranscriptResponse,
)

from app.services.transcript_service import TranscriptService


router = APIRouter(
    prefix="/transcripts",
    tags=["Interview Transcripts"],
)


# ==========================================
# Create Transcript
# ==========================================

@router.post(
    "",
    response_model=TranscriptResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transcript(
    transcript: TranscriptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TranscriptService(db)

    return service.create(
        transcript,
        current_user.id,
    )


# ==========================================
# Get Transcript
# ==========================================

@router.get(
    "/{transcript_id}",
    response_model=TranscriptResponse,
)
def get_transcript(
    transcript_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TranscriptService(db)

    transcript = service.get_by_id(
        transcript_id,
        current_user.id,
    )

    if transcript is None:
        raise HTTPException(
            status_code=404,
            detail="Transcript not found",
        )

    return transcript


# ==========================================
# Update Transcript
# ==========================================

@router.put(
    "/{transcript_id}",
    response_model=TranscriptResponse,
)
def update_transcript(
    transcript_id: int,
    transcript: TranscriptUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TranscriptService(db)

    updated = service.update(
        transcript_id,
        transcript,
        current_user.id,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Transcript not found",
        )

    return updated


# ==========================================
# Delete Transcript
# ==========================================

@router.delete(
    "/{transcript_id}",
)
def delete_transcript(
    transcript_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TranscriptService(db)

    deleted = service.delete(
        transcript_id,
        current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Transcript not found",
        )

    return {
        "success": True,
        "message": "Transcript deleted successfully",
    }


# ==========================================
# Get Interview Transcripts
# ==========================================

@router.get(
    "/interview/{interview_id}",
    response_model=List[TranscriptResponse],
)
def get_interview_transcripts(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TranscriptService(db)

    return service.get_by_interview(
        interview_id,
        current_user.id,
    )


# ==========================================
# Export Interview Transcript
# ==========================================

@router.get(
    "/interview/{interview_id}/export",
)
def export_transcript(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TranscriptService(db)

    transcript = service.export(
        interview_id,
        current_user.id,
    )

    return {
        "success": True,
        "interview_id": interview_id,
        "transcript": transcript,
    }
