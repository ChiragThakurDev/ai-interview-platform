from sqlalchemy.orm import Session

from app.models.interview_session import InterviewSession


class InterviewSessionRepository:

    def __init__(self, db: Session):
        self.db = db


    # ==========================================
    # Create Session
    # ==========================================

    def create(
        self,
        session: InterviewSession,
    ):

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session


    # ==========================================
    # Get Session By Interview
    # ==========================================

    def get_by_interview_id(
        self,
        interview_id: int,
    ):

        return (
            self.db.query(InterviewSession)
            .filter(
                InterviewSession.interview_id == interview_id
            )
            .first()
        )


    # ==========================================
    # Update Session
    # ==========================================

    def update(
        self,
        session: InterviewSession,
    ):

        self.db.commit()
        self.db.refresh(session)

        return session


    # ==========================================
    # Increment Answer Progress
    # ==========================================

    def increment_answered(
        self,
        session: InterviewSession,
    ):

        session.answered_questions += 1
        session.current_question += 1

        self.db.commit()
        self.db.refresh(session)

        return session


    # ==========================================
    # Complete Session
    # ==========================================

    def complete(
        self,
        session: InterviewSession,
    ):

        from datetime import datetime, timezone

        session.status = "completed"
        session.completed_at = datetime.now(timezone.utc)

        self.db.commit()
        self.db.refresh(session)

        return session


    # ==========================================
    # Delete Session
    # ==========================================

    def delete(
        self,
        session: InterviewSession,
    ):

        self.db.delete(session)
        self.db.commit()
