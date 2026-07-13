from sqlalchemy.orm import Session

from app.models.interview_answer import InterviewAnswer


class InterviewAnswerRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, interview_answer: InterviewAnswer):
        self.db.add(interview_answer)
        self.db.commit()
        self.db.refresh(interview_answer)
        return interview_answer

    def get_by_question(self, question_id: int):
        return (
            self.db.query(InterviewAnswer)
            .filter(
                InterviewAnswer.question_id == question_id
            )
            .first()
        )

    def update(
        self,
        interview_answer: InterviewAnswer,
        answer: str,
        score: int,
        feedback: str,
    ):
        interview_answer.answer = answer
        interview_answer.score = score
        interview_answer.feedback = feedback

        self.db.commit()
        self.db.refresh(interview_answer)

        return interview_answer

    def delete(self, interview_answer: InterviewAnswer):
        self.db.delete(interview_answer)
        self.db.commit()
