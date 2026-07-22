from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.coding_interview import CodingInterview
from app.models.coding_question import CodingQuestion
from app.models.coding_submission import CodingSubmission

from app.repositories.coding_interview_repository import (
        CodingInterviewRepository,
        )

from app.services.ai_service import AIService



class CodingInterviewService:


    def __init__(
            self,
            db: Session
            ):

        self.db = db

        self.repository = CodingInterviewRepository(
                db
                )

        self.ai_service = AIService()



    # =====================================================
    # CREATE CODING INTERVIEW
    # =====================================================

    def create_interview(
            self,
            user_id: int,
            role: str,
            company: str | None,
            language: str,
            difficulty: str,
            number_of_questions: int,
            ):


        interview = CodingInterview(

                user_id=user_id,

                role=role,

                company=company,

                language=language,

                difficulty=difficulty,

                status="pending",

                )


        interview = self.repository.create(
                interview
                )


        ai_response = self.ai_service.generate_coding_questions(

                role=role,

                company=company,

                language=language,

                difficulty=difficulty,

                number_of_questions=number_of_questions,

                )

        print("AI RESPONSE:", ai_response)

        for item in ai_response["questions"]:


            question = CodingQuestion(

                    coding_interview_id=interview.id,

                    title=item["title"],

                    description=item["description"],

                    starter_code=item.get(
                        "starter_code"
                        ),

                    solution=item.get(
                        "solution"
                        ),

                    difficulty=item["difficulty"],

                    )


            self.repository.create_question(
                    question
                    )


        interview.status = "in_progress"

        interview.started_at = datetime.now(
                timezone.utc
                )


        self.db.commit()

        self.db.refresh(
                interview
                )


        return interview




    # =====================================================
    # GET INTERVIEW
    # =====================================================


    def get_interview(
            self,
            interview_id:int
            ):


        interview = self.repository.get_by_id(
                interview_id
                )


        if not interview:

            raise HTTPException(
                    status_code=404,
                    detail="Coding interview not found",
                    )


        return interview




    # =====================================================
    # GET QUESTIONS
    # =====================================================


    def get_questions(
            self,
            interview_id:int
            ):


        return self.repository.get_questions(
                interview_id
                )




    # =====================================================
    # SUBMIT CODE
    # =====================================================


    def submit_code(
            self,
            question_id:int,
            language:str,
            code:str,
            ):


        question = (
                self.db.query(CodingQuestion)
                .filter(
                    CodingQuestion.id == question_id
                    )
                .first()
                )


        if not question:

            raise HTTPException(
                    status_code=404,
                    detail="Question not found",
                    )



        result = self.ai_service.evaluate_code(

                question=question.description,

                language=language,

                code=code,

                )



        submission = CodingSubmission(

                question_id=question_id,

                language=language,

                code=code,

                output=result.get(
                    "output"
                    ),

                passed=result.get(
                    "passed",
                    False
                    ),

                score=result.get(
                    "score",
                    0
                    ),

                feedback=result.get(
                    "feedback"
                    ),

                )


        self.repository.create_submission(
                submission
                )


        return result




    # =====================================================
    # COMPLETE INTERVIEW
    # =====================================================

    def finish_interview(
            self,
            interview_id: int,
            ):

        interview = self.get_interview(
                interview_id
                )


        questions = interview.questions


        if not questions:

            raise HTTPException(
                    status_code=400,
                    detail="No questions found",
                    )


        total_score = 0
        answered_questions = 0


        for question in questions:

            latest_submission = (
                    self.db.query(CodingSubmission)
                    .filter(
                        CodingSubmission.question_id == question.id
                        )
                    .order_by(
                        CodingSubmission.submitted_at.desc()
                        )
                    .first()
                    )


            if latest_submission:

                answered_questions += 1

                total_score += (
                        latest_submission.score or 0
                        )



        if answered_questions < len(questions):

            raise HTTPException(
                    status_code=400,
                    detail="Please answer all questions before completing interview",
                    )



        final_score = (
                total_score // len(questions)
                )


        interview.score = final_score

        interview.status = "completed"

        interview.completed_at = datetime.now(
                timezone.utc
                )


        self.db.commit()

        self.db.refresh(
                interview
                )


        return {
                "interview_id":interview.id,
                "status":interview.status,
                "score":interview.score,
                "completed_at":interview.completed_at,
                }
