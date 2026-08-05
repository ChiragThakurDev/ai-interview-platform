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
    # Create Report
    # ======================================

    def create_report(
        self,
        *,
        interview_id: int,
        report_data: dict,
    ):


        report = InterviewReport(

            interview_id=interview_id,


            overall_score=
                report_data.get(
                    "overall_score",
                    0
                ),


            technical_level=
                report_data.get(
                    "technical_level",
                    ""
                ),


            communication=
                report_data.get(
                    "communication",
                    ""
                ),


            strengths=
                report_data.get(
                    "strengths",
                    []
                ),


            weaknesses=
                report_data.get(
                    "weaknesses",
                    []
                ),


            recommendation=
                report_data.get(
                    "recommendation",
                    ""
                ),


            summary=
                report_data.get(
                    "summary",
                    ""
                ),

        )


        self.db.add(report)

        self.db.commit()

        self.db.refresh(report)


        return report



    # ======================================
    # Delete Report
    # ======================================

    def delete_report(
        self,
        interview_id:int,
    ):

        report = self.get_report(
            interview_id
        )


        if report:

            self.db.delete(report)

            self.db.commit()


        return report
