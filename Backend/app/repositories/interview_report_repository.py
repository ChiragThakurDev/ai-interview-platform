from sqlalchemy.orm import Session

from app.models.interview_report import InterviewReport


class InterviewReportRepository:

    def __init__(self, db: Session):
        self.db = db


    def create(
        self,
        report: InterviewReport,
    ):
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)

        return report


    def get_by_interview_id(
        self,
        interview_id: int,
    ):
        return (
            self.db.query(InterviewReport)
            .filter(
                InterviewReport.interview_id == interview_id
            )
            .first()
        )


    def delete(
        self,
        report: InterviewReport,
    ):
        self.db.delete(report)
        self.db.commit()
