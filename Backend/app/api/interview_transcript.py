from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.speech import SpeechResponse

from app.services.whisper_service import WhisperService
from app.services.interview_transcript_service import (
    InterviewTranscriptService,
)

router = APIRouter(
    prefix="/interview",
    tags=["Interview Transcript"],
)

whisper_service = WhisperService()


@router.post(
    "/{interview_id}/question/{question_id}/transcribe",
    response_model=SpeechResponse,
)
def transcribe_interview_audio(
    interview_id: int,
    question_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    whisper_result = whisper_service.transcribe(
        file,
    )

    transcript_service = InterviewTranscriptService(
        db,
    )

    transcript_service.save_segments(
        interview_id=interview_id,
        question_id=question_id,
        whisper_result=whisper_result,
        speaker="candidate",
    )

    return SpeechResponse(
        success=True,
        language=whisper_result["language"],
        transcript=whisper_result["transcript"],
        segments=whisper_result["segments"],
    )
