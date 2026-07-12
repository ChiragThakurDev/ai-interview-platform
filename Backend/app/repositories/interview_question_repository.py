from sqlalchemy.orm import Session

from app.models.interview_question import InterviewQuestion


class InterviewQuestionRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_many(self, questions: list[InterviewQuestion]):
        self.db.add_all(questions)
        self.db.commit()

    def get_by_interview(self, interview_id: int):
        return (
            self.db.query(InterviewQuestion)
            .filter(
                InterviewQuestion.interview_id == interview_id
            )
            .all()
        )

    def delete_all(self, interview_id: int):
        (
            self.db.query(InterviewQuestion)
            .filter(
                InterviewQuestion.interview_id == interview_id
            )
            .delete()
        )

        self.db.commit()
