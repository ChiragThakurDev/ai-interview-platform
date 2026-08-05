from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TranscriptCreate(BaseModel):

    interview_id: int

    question_id: int

    speaker: str = "candidate"

    transcript: str

    confidence: Optional[float] = None

    language: Optional[str] = None

    start_time: float

    end_time: float


class TranscriptResponse(BaseModel):

    id: int

    interview_id: int

    question_id: int

    speaker: str

    transcript: str

    confidence: Optional[float]

    language: Optional[str]

    start_time: float

    end_time: float

    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class TranscriptListResponse(BaseModel):

    transcripts: list[TranscriptResponse]
