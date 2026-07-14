from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.interview import Interview
from app.repositories.interview_repository import (
    InterviewRepository,
)
from app.schemas.interview_result import (
    InterviewResultResponse,
    InterviewInfoResponse,
    QuestionResultResponse,
)


class InterviewService:

    def __init__(self, db: Session):
        self.repository = InterviewRepository(db)

    def create_interview(
        self,
        user_id: int,
        resume_id: int,
        role: str,
        difficulty: str,
    ):
        interview = Interview(
            user_id=user_id,
            resume_id=resume_id,
            title=f"{role} Interview",
            role=role,
            difficulty=difficulty,
            status="pending",
        )

        return self.repository.create(interview)

    def get_interview(
        self,
        interview_id: int,
    ):
        return self.repository.get_by_id(interview_id)

    def get_user_interviews(
        self,
        user_id: int,
    ):
        return self.repository.get_by_user(user_id)

    def get_interview_results(
        self,
        interview_id: int,
    ):
        interview = self.repository.get_with_results(
            interview_id
        )

        if not interview:
            return None

        total_score = 0
        answered_questions = 0

        question_results = []

        for question in interview.questions:

            answer = question.answer

            if answer:
                total_score += answer.score
                answered_questions += 1

            question_results.append(
                QuestionResultResponse(
                    id=question.id,
                    question=question.question,
                    category=question.category,
                    difficulty=question.difficulty,
                    answer=answer.answer if answer else None,
                    score=answer.score if answer else None,
                    feedback=answer.feedback if answer else None,
                )
            )

        average_score = (
            total_score / answered_questions
            if answered_questions > 0
            else 0
        )

        return InterviewResultResponse(
            interview=InterviewInfoResponse.model_validate(
                interview
            ),
            average_score=average_score,
            total_questions=len(interview.questions),
            questions=question_results,
        )

    def start_interview(
        self,
        interview_id: int,
    ):
        interview = self.repository.get_by_id(
            interview_id
        )

        if not interview:
            return None

        interview.status = "in_progress"
        interview.started_at = datetime.now(
            timezone.utc
        )

        return self.repository.update(interview)

    def complete_interview(
        self,
        interview_id: int,
    ):
        interview = self.repository.get_by_id(
            interview_id
        )

        if not interview:
            return None

        interview.status = "completed"
        interview.completed_at = datetime.now(
            timezone.utc
        )

        if interview.started_at:
            interview.duration = int(
                (
                    interview.completed_at
                    - interview.started_at
                ).total_seconds()
            )

        return self.repository.update(interview)

    def cancel_interview(
        self,
        interview_id: int,
    ):
        interview = self.repository.get_by_id(
            interview_id
        )

        if not interview:
            return None

        interview.status = "cancelled"

        return self.repository.update(interview)

    def delete_interview(
        self,
        interview: Interview,
    ):
        self.repository.delete(interview)
