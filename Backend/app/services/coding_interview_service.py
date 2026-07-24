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




    # =====================================================
    # GET INTERVIEW PROGRESS
    # =====================================================

    def get_progress(
            self,
            interview_id: int,
            ):

        interview = self.get_interview(
                interview_id
                )

        questions = interview.questions

        total_questions = len(
                questions
                )

        answered_questions = 0

        total_score = 0

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

        remaining_questions = (
                total_questions - answered_questions
                )

        current_score = (
                total_score // answered_questions
                if answered_questions > 0
                else 0
                )

        progress_percentage = (
                (answered_questions * 100) // total_questions
                if total_questions > 0
                else 0
                )

        return {
                "interview_id": interview.id,
                "status": interview.status,
                "total_questions": total_questions,
                "answered_questions": answered_questions,
                "remaining_questions": remaining_questions,
                "current_score": current_score,
                "progress_percentage": progress_percentage,
                }

        # =====================================================
# GET INTERVIEW HISTORY
# =====================================================

    def get_history(
            self,
            user_id: int,
            ):

        interviews = self.repository.get_user_interviews(
                user_id
                )

        return {
                "history": interviews
                }

# =====================================================
# DASHBOARD
# =====================================================

    def get_dashboard(
            self,
            user_id: int,
            ):

        interviews = self.repository.get_user_interviews(
                user_id
                )

        total_interviews = len(interviews)

        completed_interviews = sum(
                1
                for interview in interviews
                if interview.status == "completed"
                )

        pending_interviews = total_interviews - completed_interviews

        completed_scores = [
                interview.score
                for interview in interviews
                if interview.score is not None
                ]

        average_score = (
                sum(completed_scores) // len(completed_scores)
                if completed_scores
                else 0
                )

        best_score = max(completed_scores) if completed_scores else 0

        total_questions = 0
        total_submissions = 0
        passed_submissions = 0

        for interview in interviews:

            total_questions += len(interview.questions)

            for question in interview.questions:

               total_submissions += len(question.submissions)

               passed_submissions += sum(
                     1
                     for submission in question.submissions
                     if submission.passed
                     )

        success_rate = (
                (passed_submissions * 100) // total_submissions
                if total_submissions
                else 0
                )

        latest = interviews[0] if interviews else None

        return {
                "total_interviews": total_interviews,
                "completed_interviews": completed_interviews,
                "pending_interviews": pending_interviews,
                "average_score": average_score,
                "best_score": best_score,
                "total_questions": total_questions,
                "total_submissions": total_submissions,
                "passed_submissions": passed_submissions,
                "success_rate": success_rate,
                "latest_interview": latest,
                }


        # =====================================================
    # GENERATE CODING INTERVIEW REPORT
    # =====================================================

    def generate_report(
            self,
            interview_id: int,
            ):

        interview = self.get_interview(
                interview_id
                )

        if not interview.questions:

            raise HTTPException(
                    status_code=400,
                    detail="Interview has no questions.",
                    )

        results = ""

        for question in interview.questions:

            submission = (
                    self.db.query(CodingSubmission)
                    .filter(
                        CodingSubmission.question_id == question.id
                        )
                    .order_by(
                        CodingSubmission.submitted_at.desc()
                        )
                    .first()
                    )

            if not submission:
                continue

            results += f"""
Question:
    {question.title}

Description:
    {question.description}

Submitted Code:
    {submission.code}

Score:
    {submission.score}

Feedback:
    {submission.feedback}

--------------------------------------
"""

        if not results.strip():

            raise HTTPException(
                    status_code=400,
                    detail="No submissions found.",
                    )

        report = self.ai_service.generate_coding_report(
                results
                )

        return report

    def get_leaderboard(self):

        rows = self.repository.get_leaderboard()

        return {
                "leaderboard": [
                    {
                        "user_id": row.user_id,
                        "user_name": row.user_name,
                        "total_interviews": row.total_interviews,
                        "best_score": row.best_score or 0,
                        "average_score": round(
                            float(row.average_score or 0),
                            2,
                            ),
                        }
                    for row in rows
                    ]
                }



