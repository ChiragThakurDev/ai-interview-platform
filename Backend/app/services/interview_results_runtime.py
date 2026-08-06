from sqlalchemy.orm import Session

from app.repositories.interview_repository import (
    InterviewRepository,
)

from app.repositories.interview_report_repository import (
    InterviewReportRepository,
)


class InterviewResultsRuntime:
    """
    Builds the complete interview results payload.

    Returns

    {
        interview,
        average_score,
        total_questions,
        questions,
        report
    }
    """

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.interview_repository = InterviewRepository(
            db
        )

        self.report_repository = InterviewReportRepository(
            db
        )

    def get_results(
        self,
        interview_id: int,
    ) -> dict:

        interview = (
            self.interview_repository
            .get_with_results(
                interview_id
            )
        )

        if interview is None:
            return {}

        questions = []

        scores = []

        for question in interview.questions:

            answer = question.answer

            score = 0
            feedback = ""
            candidate_answer = ""

            if answer:

                score = answer.score or 0
                feedback = answer.feedback or ""
                candidate_answer = answer.answer or ""

            scores.append(score)

            questions.append(
                {
                    "id": question.id,
                    "question": question.question,
                    "category": question.category,
                    "difficulty": question.difficulty,
                    "answer": candidate_answer,
                    "score": score,
                    "feedback": feedback,
                }
            )

        average_score = (
            round(
                sum(scores) / len(scores),
                2,
            )
            if scores
            else 0
        )

        report = (
            self.report_repository
            .get_by_interview_id(
                interview_id
            )
        )

        report_data = None

        if report:

            report_data = {
                "overall_score": report.overall_score,
                "technical_level": report.technical_level,
                "communication": report.communication,
                "strengths": report.strengths,
                "weaknesses": report.weaknesses,
                "recommendation": report.recommendation,
                "summary": report.summary,
                "created_at": report.created_at,
            }

        return {

            "interview": {

                "id": interview.id,

                "role": interview.role,

                "difficulty": interview.difficulty,

                "status": interview.status,

                "created_at": interview.created_at,

            },

            "average_score": average_score,

            "total_questions": len(questions),

            "questions": questions,

            "report": report_data,

        }
