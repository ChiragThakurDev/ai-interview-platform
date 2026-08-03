from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.interview import Interview

from app.repositories.interview_repository import InterviewRepository

from app.services.interview_question_service import (
    InterviewQuestionService,
)

from app.services.interview_answer_service import (
    InterviewAnswerService,
)

from app.services.ai_service import AIService

from app.services.interview_runtime_service import (
    InterviewRuntimeService,
)

from app.schemas.interview_result import (
    InterviewResultResponse,
    InterviewInfoResponse,
    QuestionResultResponse,
)


class InterviewService:

    def __init__(
        self,
        db: Session,
    ):

        self.db = db

        self.repository = InterviewRepository(
            db
        )

        self.question_service = InterviewQuestionService(
            db
        )

        self.answer_service = InterviewAnswerService(
            db
        )

        self.ai_service = AIService()

        self.runtime_service = InterviewRuntimeService(
            ai_service=self.ai_service,
            answer_service=self.answer_service,
        )


    # =====================================================
    # Create Interview
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

        return self.repository.create(
            interview
        )


    # =====================================================
    # Get Interview
    # =====================================================

    def get_interview(
        self,
        interview_id: int,
    ):

        return self.repository.get_by_id(
            interview_id
        )


    # =====================================================
    # User Interviews
    # =====================================================

    def get_user_interviews(
        self,
        user_id: int,
    ):

        return self.repository.get_by_user(
            user_id
        )


    # =====================================================
    # Current Question
    # =====================================================

    def get_current_question(
        self,
        interview: Interview,
    ):

        if interview.status != "in_progress":

            raise HTTPException(
                status_code=400,
                detail="Interview is not active.",
            )


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


        question = questions[index]


        return {
            "interview_id": interview.id,
            "question_id": question.id,
            "current_question": interview.current_question,
            "total_questions": len(questions),
            "question": question.question,
            "category": question.category,
            "difficulty": question.difficulty,
        }


    # =====================================================
    # Start Interview
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

            return self.get_current_question(
                interview
            )


        interview.status = "in_progress"

        interview.started_at = datetime.now(
            timezone.utc
        )

        interview.current_question = 1


        self.repository.update(
            interview
        )


        runtime = self.runtime_service.start_runtime(
            interview.id
        )


        questions = self.question_service.get_questions(
            interview.id
        )


        if not questions:

            raise HTTPException(
                status_code=404,
                detail="No questions found.",
            )


        runtime.progress.total_questions = len(
            questions
        )


        return {
            "interview_id": interview.id,
            "status": interview.status,
            "current_question":1,
            "question":questions[0].question,
        }


    # =====================================================
    # Submit Answer
    # =====================================================

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


        index = interview.current_question - 1


        if index >= len(questions):

            raise HTTPException(
                status_code=400,
                detail="Interview completed.",
            )


        question = questions[index]


        ai_result = self.ai_service.evaluate_answer(
            question=question.question,
            answer=answer,
        )


        existing_answer = self.answer_service.get_answer(
            question.id
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
                interview_id=interview.id,
                question_id=question.id,
                answer=answer,
                score=ai_result.score,
                feedback=ai_result.feedback,
            )


        if interview.current_question >= len(questions):

            result = self.finish_interview(
                interview
            )


            return {
                "interview_completed":True,
                "score":result["score"],
                "feedback":ai_result.feedback,
                "message":result["message"],
            }


        interview.current_question += 1


        self.repository.update(
            interview
        )


        next_question = questions[
            interview.current_question - 1
        ]


        return {

            "interview_completed":False,

            "current_question":
                interview.current_question,

            "next_question":
                next_question.question,

            "score":
                ai_result.score,

            "feedback":
                ai_result.feedback,

            "message":
                "Answer submitted successfully."
        }



    # =====================================================
    # Finish Interview
    # =====================================================

    def finish_interview(
        self,
        interview: Interview,
    ):


        questions = self.question_service.get_questions(
            interview.id
        )


        total = 0
        count = 0


        for question in questions:

            answer = self.answer_service.get_answer(
                question.id
            )


            if answer:

                total += answer.score
                count += 1


        score = (
            total // count
            if count
            else 0
        )


        interview.score = score

        interview.status = "completed"


        interview.completed_at = datetime.now(
            timezone.utc
        )


        if interview.started_at:

            interview.duration = int(
                (
                    interview.completed_at -
                    interview.started_at
                ).total_seconds()
            )


        self.repository.update(
            interview
        )


        return {

            "interview_id":
                interview.id,

            "status":
                interview.status,

            "score":
                score,

            "duration":
                interview.duration,

            "message":
                "Interview completed successfully."
        }



    # =====================================================
    # Interview Results
    # =====================================================

    def get_interview_results(
        self,
        interview_id:int,
    ):

        interview = self.repository.get_with_results(
            interview_id
        )


        if not interview:

            raise HTTPException(
                status_code=404,
                detail="Interview not found."
            )


        total_score = 0
        answered = 0

        results = []


        for question in interview.questions:


            answer = self.answer_service.get_answer(
                question.id
            )


            if answer:

                total_score += answer.score
                answered += 1



            results.append(

                QuestionResultResponse(

                    id=question.id,

                    question=question.question,

                    category=question.category,

                    difficulty=question.difficulty,

                    answer=
                    answer.answer
                    if answer
                    else None,

                    score=
                    answer.score
                    if answer
                    else None,

                    feedback=
                    answer.feedback
                    if answer
                    else None,
                )
            )



        average_score = (

            total_score / answered

            if answered

            else 0
        )


        return InterviewResultResponse(

            interview=
            InterviewInfoResponse.model_validate(
                interview
            ),


            average_score=average_score,


            total_questions=
            len(interview.questions),


            questions=results,


            report=None
        )
