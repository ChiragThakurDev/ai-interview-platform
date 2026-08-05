from sqlalchemy.orm import Session

from app.models.interview_transcript import InterviewTranscript
from app.schemas.interview_transcript import TranscriptCreate


class InterviewTranscriptRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # ==========================================
    # Create Single Transcript
    # ==========================================

    def create(
        self,
        transcript: TranscriptCreate,
    ) -> InterviewTranscript:

        db_transcript = InterviewTranscript(
            interview_id=transcript.interview_id,
            question_id=transcript.question_id,
            speaker=transcript.speaker,
            transcript=transcript.transcript,
            confidence=transcript.confidence,
            language=transcript.language,
            start_time=transcript.start_time,
            end_time=transcript.end_time,
        )

        self.db.add(
            db_transcript,
        )

        self.db.commit()

        self.db.refresh(
            db_transcript,
        )

        return db_transcript

    # ==========================================
    # Bulk Create
    # ==========================================

    def bulk_create(
        self,
        transcripts: list[TranscriptCreate],
    ) -> list[InterviewTranscript]:

        objects = [
            InterviewTranscript(
                interview_id=t.interview_id,
                question_id=t.question_id,
                speaker=t.speaker,
                transcript=t.transcript,
                confidence=t.confidence,
                language=t.language,
                start_time=t.start_time,
                end_time=t.end_time,
            )
            for t in transcripts
        ]

        self.db.bulk_save_objects(
            objects,
        )

        self.db.commit()

        return objects

    # ==========================================
    # Get By Interview
    # ==========================================

    def get_by_interview(
        self,
        interview_id: int,
    ) -> list[InterviewTranscript]:

        return (
            self.db.query(
                InterviewTranscript,
            )
            .filter(
                InterviewTranscript.interview_id == interview_id,
            )
            .order_by(
                InterviewTranscript.start_time.asc(),
            )
            .all()
        )

    # ==========================================
    # Get By Question
    # ==========================================

    def get_by_question(
        self,
        question_id: int,
    ) -> list[InterviewTranscript]:

        return (
            self.db.query(
                InterviewTranscript,
            )
            .filter(
                InterviewTranscript.question_id == question_id,
            )
            .order_by(
                InterviewTranscript.start_time.asc(),
            )
            .all()
        )

    # ==========================================
    # Delete By Interview
    # ==========================================

    def delete_by_interview(
        self,
        interview_id: int,
    ) -> int:

        deleted = (
            self.db.query(
                InterviewTranscript,
            )
            .filter(
                InterviewTranscript.interview_id == interview_id,
            )
            .delete()
        )

        self.db.commit()

        return deleted
