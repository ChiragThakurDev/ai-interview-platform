from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.interview import Interview

from app.repositories.interview_repository import (
    InterviewRepository,
)

from app.services.interview_question_service import (
    InterviewQuestionService,
)

from app.services.interview_answer_service import (
    InterviewAnswerService,
)

from app.services.ai_service import AIService

from app.schemas.interview_result import (
    InterviewResultResponse,
    InterviewInfoResponse,
    QuestionResultResponse,
)


class InterviewService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = InterviewRepository(db)
        self.question_service = InterviewQuestionService(db)
        self.answer_service = InterviewAnswerService(db)
        self.ai_service = AIService()

    # =====================================================
    # Existing Methods
    # =====================================================

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

    # =====================================================
    # Interview Session
    # =====================================================

    def start_interview(
        self,
        interview: Interview,
    ):

        if interview.status == "completed":
            raise HTTPException(
                status_code=400,
                detail="Interview already completed.",
            )

        if interview.status == "in_progress":

            questions = self.question_service.get_questions(
                interview.id
            )

            question = questions[
                interview.current_question - 1
            ]

            return {
                "interview_id": interview.id,
                "status": interview.status,
                "current_question": interview.current_question,
                "question": question.question,
            }

        interview.status = "in_progress"
        interview.started_at = datetime.utcnow()
        interview.current_question = 1

        self.repository.update(interview)

        questions = self.question_service.get_questions(
            interview.id
        )

        if not questions:
            raise HTTPException(
                status_code=404,
                detail="No questions found.",
            )

        return {
            "interview_id": interview.id,
            "status": interview.status,
            "current_question": 1,
            "question": questions[0].question,
        }

    def get_current_question(
        self,
        interview: Interview,
    ):

        questions = self.question_service.get_questions(
            interview.id
        )

        if not questions:
            raise HTTPException(
                status_code=404,
                detail="No questions found.",
            )

        index = interview.current_question - 1

        if index >= len(questions):
            raise HTTPException(
                status_code=400,
                detail="Interview completed.",
            )

        return {
            "interview_id": interview.id,
            "current_question": interview.current_question,
            "total_questions": len(questions),
            "question": questions[index].question,
        }

    def submit_answer(
        self,
        interview: Interview,
        answer: str,
    ):

        questions = self.question_service.get_questions(
            interview.id
        )

        if not questions:
            raise HTTPException(
                status_code=404,
                detail="No questions found.",
            )

        question_index = interview.current_question - 1

        if question_index >= len(questions):
            raise HTTPException(
                status_code=400,
                detail="Interview already completed.",
            )

        current_question = questions[question_index]

        ai_result = self.ai_service.evaluate_answer(
            question=current_question.question,
            answer=answer,
        )

        existing_answer = self.answer_service.get_answer(
            current_question.id
        )

        if existing_answer:

            self.answer_service.update_answer(
                interview_answer=existing_answer,
                answer=answer,
                score=ai_result.score,
                feedback=ai_result.feedback,
            )

        else:

            self.answer_service.create_answer(
                question_id=current_question.id,
                answer=answer,
                score=ai_result.score,
                feedback=ai_result.feedback,
            )

        if interview.current_question >= len(questions):
            return self.finish_interview(interview)

        interview.current_question += 1

        self.repository.update(interview)

        next_question = questions[
            interview.current_question - 1
        ]

        return {
            "interview_completed": False,
            "current_question": interview.current_question,
            "next_question": next_question.question,
            "score": ai_result.score,
            "feedback": ai_result.feedback,
            "message": "Answer submitted successfully.",
        }

    def finish_interview(
        self,
        interview: Interview,
    ):

        questions = self.question_service.get_questions(
            interview.id
        )

        total_score = 0
        answered = 0

        for question in questions:

            answer = self.answer_service.get_answer(
                question.id
            )

            if answer:
                total_score += answer.score
                answered += 1

        average_score = (
            total_score // answered
            if answered
            else 0
        )

        interview.score = average_score
        interview.status = "completed"
        interview.completed_at = datetime.utcnow()

        if interview.started_at:
            interview.duration = int(
                (
                    interview.completed_at
                    - interview.started_at
                ).total_seconds()
            )

        self.repository.update(interview)

        return {
            "interview_id": interview.id,
            "status": interview.status,
            "score": interview.score,
            "duration": interview.duration,
            "message": "Interview completed successfully.",
        }

    # =====================================================
    # Existing Result Methods
    # =====================================================

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

    def delete_interview(
        self,
        interview: Interview,
    ):
        self.repository.delete(interview)
