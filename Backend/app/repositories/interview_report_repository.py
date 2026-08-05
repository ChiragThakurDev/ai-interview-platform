from sqlalchemy.orm import Session

from app.models.interview_report import InterviewReport


class InterviewReportRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        report: InterviewReport,
    ) -> InterviewReport:

        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)

        return report

    def get_by_interview_id(
        self,
        interview_id: int,
    ) -> InterviewReport | None:

        return (
            self.db.query(InterviewReport)
            .filter(
                InterviewReport.interview_id == interview_id
            )
            .first()
        )

    def update(
        self,
        report: InterviewReport,
        data: dict,
    ) -> InterviewReport:

        report.overall_score = data["overall_score"]
        report.technical_level = data["technical_level"]
        report.communication = data["communication"]
        report.strengths = data["strengths"]
        report.weaknesses = data["weaknesses"]
        report.recommendation = data["recommendation"]
        report.summary = data["summary"]

        self.db.commit()
        self.db.refresh(report)

        return report

    def create_or_update(
        self,
        interview_id: int,
        data: dict,
    ) -> InterviewReport:

        report = self.get_by_interview_id(
            interview_id
        )

        if report:
            return self.update(
                report,
                data,
            )

        report = InterviewReport(
            interview_id=interview_id,
            overall_score=data["overall_score"],
            technical_level=data["technical_level"],
            communication=data["communication"],
            strengths=data["strengths"],
            weaknesses=data["weaknesses"],
            recommendation=data["recommendation"],
            summary=data["summary"],
        )

        return self.create(report)

    def delete(
        self,
        report: InterviewReport,
    ) -> None:

        self.db.delete(report)
        self.db.commit()
