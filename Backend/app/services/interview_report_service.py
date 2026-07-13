from sqlalchemy.orm import Session

from app.models.interview_report import InterviewReport

from app.repositories.interview_report_repository import (
    InterviewReportRepository,
)


class InterviewReportService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = InterviewReportRepository(db)


    def create_report(
        self,
        interview_id: int,
        report_data: dict,
    ):

        report = InterviewReport(
            interview_id=interview_id,
            overall_score=report_data["overall_score"],
            technical_level=report_data["technical_level"],
            communication=report_data["communication"],
            strengths=report_data["strengths"],
            weaknesses=report_data["weaknesses"],
            recommendation=report_data["recommendation"],
            summary=report_data["summary"],
        )

        return self.repository.create(report)


    def get_report(
        self,
        interview_id: int,
    ):

        return self.repository.get_by_interview_id(
            interview_id
        )
