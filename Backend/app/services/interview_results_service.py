from sqlalchemy.orm import Session

from app.models.interview import Interview

from app.services.interview_report_service import (
    InterviewReportService,
)

from app.services.interview_question_service import (
    InterviewQuestionService,
)

from app.repositories.interview_answer_repository import (
    InterviewAnswerRepository,
)


class InterviewResultsService:

    def __init__(self, db: Session):

        self.db = db

        self.question_service = InterviewQuestionService(db)

        self.answer_repository = InterviewAnswerRepository(db)

        self.report_service = InterviewReportService(db)

    def get_results(
        self,
        interview_id: int,
    ):

        interview = (
            self.db.query(Interview)
            .filter(
                Interview.id == interview_id
            )
            .first()
        )

        if not interview:
            return None

        questions = self.question_service.get_questions(
            interview_id
        )

        answers = self.answer_repository.get_by_interview(
            interview_id
        )

        report = self.report_service.get_report(
            interview_id
        )

        answer_map = {
            answer.question_id: answer
            for answer in answers
        }

        total_score = 0

        question_results = []

        for question in questions:

            answer = answer_map.get(question.id)

            score = answer.score if answer else 0

            total_score += score

            question_results.append(
                {
                    "id": question.id,
                    "question": question.question,
                    "category": question.category,
                    "difficulty": question.difficulty,
                    "answer": (
                        answer.answer
                        if answer
                        else ""
                    ),
                    "score": score,
                    "feedback": (
                        answer.feedback
                        if answer
                        else ""
                    ),
                }
            )

        average_score = (
            round(
                total_score / len(question_results),
                2,
            )
            if question_results
            else 0
        )

        return {
            "interview": {
                "id": interview.id,
                "role": interview.role,
                "difficulty": interview.difficulty,
                "status": interview.status,
                "created_at": interview.created_at,
            },
            "average_score": average_score,
            "total_questions": len(question_results),
            "questions": question_results,
            "report": (
                {
                    "overall_score": report.overall_score,
                    "technical_level": report.technical_level,
                    "communication": report.communication,
                    "strengths": report.strengths,
                    "weaknesses": report.weaknesses,
                    "recommendation": report.recommendation,
                    "summary": report.summary,
                }
                if report
                else None
            ),
        }
