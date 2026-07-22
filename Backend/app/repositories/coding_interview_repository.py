from sqlalchemy.orm import Session

from app.models.coding_interview import CodingInterview
from app.models.coding_question import CodingQuestion
from app.models.coding_submission import CodingSubmission



class CodingInterviewRepository:


    def __init__(
        self,
        db: Session
    ):
        self.db = db



    def create(
        self,
        interview
    ):

        self.db.add(interview)
        self.db.commit()
        self.db.refresh(interview)

        return interview



    def get_by_id(
        self,
        interview_id:int
    ):

        return (
            self.db.query(CodingInterview)
            .filter(
                CodingInterview.id == interview_id
            )
            .first()
        )



    def get_questions(
        self,
        interview_id:int
    ):

        return (
            self.db.query(CodingQuestion)
            .filter(
                CodingQuestion.coding_interview_id
                ==
                interview_id
            )
            .all()
        )



    def create_question(
        self,
        question
    ):

        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)

        return question



    def create_submission(
        self,
        submission
    ):

        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)

        return submission
