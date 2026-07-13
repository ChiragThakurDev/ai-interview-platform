from sqlalchemy.orm import Session

from app.models.interview_question import InterviewQuestion
from app.repositories.interview_question_repository import (
    InterviewQuestionRepository,
)


class InterviewQuestionService:

    def __init__(self, db: Session):
        self.repository = InterviewQuestionRepository(db)

    def create_questions(
        self,
        interview_id: int,
        questions: list[str],
        difficulty:str,
    ):
        question_objects = [
            InterviewQuestion(
                interview_id=interview_id,
                question=question,
                category="General",
                difficulty=difficulty.capitalize(),
            )
            for question in questions
        ]

        self.repository.create_many(question_objects)

        return question_objects

    def get_questions(self, interview_id: int):
        return self.repository.get_by_interview(interview_id)

    def delete_questions(self, interview_id: int):
        self.repository.delete_all(interview_id)
