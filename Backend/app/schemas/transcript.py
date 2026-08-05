from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ==========================================
# Create Transcript
# ==========================================

class TranscriptCreate(BaseModel):

    interview_id: int

    question_id: int

    speaker: str

    transcript: str

    confidence: Optional[float] = None

    language: Optional[str] = None

    start_time: Optional[float] = None

    end_time: Optional[float] = None


# ==========================================
# Update Transcript
# ==========================================

class TranscriptUpdate(BaseModel):

    speaker: Optional[str] = None

    transcript: Optional[str] = None

    confidence: Optional[float] = None

    language: Optional[str] = None

    start_time: Optional[float] = None

    end_time: Optional[float] = None


# ==========================================
# Transcript Response
# ==========================================

class TranscriptResponse(BaseModel):

    id: int

    interview_id: int

    question_id: int

    speaker: str

    transcript: str

    confidence: Optional[float]

    language: Optional[str]

    start_time: Optional[float]

    end_time: Optional[float]

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# ==========================================
# Export Transcript Response
# ==========================================

class TranscriptExportResponse(BaseModel):

    interview_id: int

    transcript: str
