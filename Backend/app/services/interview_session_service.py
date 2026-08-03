from sqlalchemy.orm import Session

from app.models.interview_session import InterviewSession

from app.repositories.interview_session_repository import (
    InterviewSessionRepository,
)


class InterviewSessionService:


    def __init__(
        self,
        db: Session,
    ):
        self.repository = InterviewSessionRepository(db)


    def create_session(
        self,
        interview_id: int,
        total_questions: int,
    ):

        session = InterviewSession(
            interview_id=interview_id,
            total_questions=total_questions,
        )

        return self.repository.create(session)



    def get_session(
        self,
        interview_id: int,
    ):

        return self.repository.get_by_interview_id(
            interview_id
        )



    def update_session(
        self,
        session: InterviewSession,
    ):

        return self.repository.update(session)



    def answer_question(
        self,
        session: InterviewSession,
    ):

        return self.repository.increment_answered(
            session
        )



    def finish_session(
        self,
        session: InterviewSession,
    ):

        return self.repository.complete(
            session
        )
