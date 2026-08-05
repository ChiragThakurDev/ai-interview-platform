from sqlalchemy.orm import Session

from app.models.interview_transcript import InterviewTranscript


class TranscriptRepository:


    def create(
        self,
        db: Session,
        interview_id: int,
        question_id: int,
        speaker: str,
        transcript: str,
        confidence: float | None = None,
        language: str | None = None,
        start_time: float | None = None,
        end_time: float | None = None,
    ):

        record = InterviewTranscript(
            interview_id=interview_id,
            question_id=question_id,
            speaker=speaker,
            transcript=transcript,
            confidence=confidence,
            language=language,
            start_time=start_time,
            end_time=end_time,
        )


        try:

            db.add(record)

            db.commit()

            db.refresh(record)

        except Exception:

            db.rollback()

            raise


        return record



    def get_by_id(
        self,
        db: Session,
        transcript_id: int,
    ):

        return (
            db.query(InterviewTranscript)
            .filter(
                InterviewTranscript.id == transcript_id
            )
            .first()
        )



    def get_by_interview(
        self,
        db: Session,
        interview_id: int,
    ):

        return (
            db.query(InterviewTranscript)
            .filter(
                InterviewTranscript.interview_id == interview_id
            )
            .order_by(
                InterviewTranscript.created_at.asc()
            )
            .all()
        )



    def get_by_question(
        self,
        db: Session,
        question_id: int,
    ):

        return (
            db.query(InterviewTranscript)
            .filter(
                InterviewTranscript.question_id == question_id
            )
            .order_by(
                InterviewTranscript.start_time.asc()
            )
            .all()
        )



    def update(
        self,
        db: Session,
        transcript_id: int,
        **kwargs,
    ):

        record = self.get_by_id(
            db,
            transcript_id,
        )


        if not record:
            return None


        for key,value in kwargs.items():

            if hasattr(record,key):

                setattr(
                    record,
                    key,
                    value
                )


        try:

            db.commit()

            db.refresh(record)

        except Exception:

            db.rollback()

            raise


        return record



    def delete(
        self,
        db: Session,
        transcript_id:int,
    ):

        record = self.get_by_id(
            db,
            transcript_id,
        )


        if not record:

            return False


        try:

            db.delete(record)

            db.commit()


        except Exception:

            db.rollback()

            raise


        return True



    def list(
        self,
        db: Session,
        interview_id:int|None=None,
        speaker:str|None=None,
        language:str|None=None,
    ):

        query = db.query(
            InterviewTranscript
        )


        if interview_id is not None:

            query=query.filter(
                InterviewTranscript.interview_id == interview_id
            )


        if speaker is not None:

            query=query.filter(
                InterviewTranscript.speaker == speaker
            )


        if language is not None:

            query=query.filter(
                InterviewTranscript.language == language
            )


        return (
            query
            .order_by(
                InterviewTranscript.created_at.asc()
            )
            .all()
        )
