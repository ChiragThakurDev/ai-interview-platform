from sqlalchemy.orm import Session

from app.models.interview_report import InterviewReport


class InterviewReportService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # ======================================
    # Get Existing Report
    # ======================================

    def get_report(
        self,
        interview_id: int,
    ):

        return (
            self.db
            .query(InterviewReport)
            .filter(
                InterviewReport.interview_id == interview_id
            )
            .first()
        )

    # ======================================
    # Create OR Update Report
    # ======================================

    def create_report(
        self,
        *,
        interview_id: int,
        report_data: dict,
    ):

        report = self.get_report(
            interview_id
        )

        if report is None:

            report = InterviewReport(
                interview_id=interview_id,
            )

            self.db.add(report)

        report.overall_score = report_data.get(
            "overall_score",
            0,
        )

        report.technical_level = report_data.get(
            "technical_level",
            "",
        )

        report.communication = report_data.get(
            "communication",
            "",
        )

        report.strengths = report_data.get(
            "strengths",
            [],
        )

        report.weaknesses = report_data.get(
            "weaknesses",
            [],
        )

        report.recommendation = report_data.get(
            "recommendation",
            "",
        )

        report.summary = report_data.get(
            "summary",
            "",
        )

        self.db.commit()

        self.db.refresh(report)

        return report

    # ======================================
    # Update Report
    # ======================================

    def update_report(
        self,
        *,
        interview_id: int,
        report_data: dict,
    ):

        report = self.get_report(
            interview_id
        )

        if report is None:
            return self.create_report(
                interview_id=interview_id,
                report_data=report_data,
            )

        report.overall_score = report_data.get(
            "overall_score",
            report.overall_score,
        )

        report.technical_level = report_data.get(
            "technical_level",
            report.technical_level,
        )

        report.communication = report_data.get(
            "communication",
            report.communication,
        )

        report.strengths = report_data.get(
            "strengths",
            report.strengths,
        )

        report.weaknesses = report_data.get(
            "weaknesses",
            report.weaknesses,
        )

        report.recommendation = report_data.get(
            "recommendation",
            report.recommendation,
        )

        report.summary = report_data.get(
            "summary",
            report.summary,
        )

        self.db.commit()

        self.db.refresh(report)

        return report

    # ======================================
    # Delete Report
    # ======================================

    def delete_report(
        self,
        interview_id: int,
    ):

        report = self.get_report(
            interview_id
        )

        if report:

            self.db.delete(report)

            self.db.commit()

        return report
