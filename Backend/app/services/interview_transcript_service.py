from sqlalchemy.orm import Session

from app.repositories.interview_transcript_repository import (
    InterviewTranscriptRepository,
)
from app.schemas.interview_transcript import (
    TranscriptCreate,
)


class InterviewTranscriptService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = InterviewTranscriptRepository(
            db,
        )

    # ==========================================
    # Save Single Transcript
    # ==========================================

    def save(
        self,
        transcript: TranscriptCreate,
    ):

        return self.repository.create(
            transcript,
        )

    # ==========================================
    # Save Whisper Segments
    # ==========================================

    def save_segments(
        self,
        interview_id: int,
        question_id: int,
        whisper_result: dict,
        speaker: str = "candidate",
    ):

        transcripts = []

        language = whisper_result.get(
            "language",
        )

        for segment in whisper_result["segments"]:

            transcripts.append(
                TranscriptCreate(
                    interview_id=interview_id,
                    question_id=question_id,
                    speaker=speaker,
                    transcript=segment["text"],
                    confidence=None,
                    language=language,
                    start_time=segment["start"],
                    end_time=segment["end"],
                )
            )

        return self.repository.bulk_create(
            transcripts,
        )

    # ==========================================
    # Get Complete Transcript
    # ==========================================

    def get_interview_transcript(
        self,
        interview_id: int,
    ):

        return self.repository.get_by_interview(
            interview_id,
        )

    # ==========================================
    # Merge Transcript
    # ==========================================

    def get_full_text(
        self,
        interview_id: int,
    ):

        transcripts = self.repository.get_by_interview(
            interview_id,
        )

        return " ".join(
            item.transcript
            for item in transcripts
        )

    # ==========================================
    # Speaking Duration
    # ==========================================

    def get_speaking_duration(
        self,
        interview_id: int,
    ):

        transcripts = self.repository.get_by_interview(
            interview_id,
        )

        duration = 0.0

        for item in transcripts:

            duration += (
                item.end_time -
                item.start_time
            )

        return round(
            duration,
            2,
        )
