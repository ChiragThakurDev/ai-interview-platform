from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from app.schemas.speech import SpeechResponse
from app.services.whisper_service import WhisperService


router = APIRouter(
    prefix="/speech",
    tags=["Speech"],
)

service = WhisperService()


@router.post(
    "/transcribe",
    response_model=SpeechResponse,
)
def transcribe_audio(
    file: UploadFile = File(...),
):

    allowed_extensions = {
        ".wav",
        ".mp3",
        ".m4a",
        ".ogg",
        ".webm",
    }

    extension = ""

    if file.filename:
        extension = "." + file.filename.split(".")[-1].lower()

    if extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format.",
        )

    result = service.transcribe(file)

    return SpeechResponse(
        success=True,
        language=result["language"],
        transcript=result["transcript"],
        segments=result["segments"],
    )
