from sqlalchemy.orm import Session

from app.models.skill_report import SkillReport

from app.repositories.skill_report_repository import (
    SkillReportRepository,
)



class SkillReportService:


    def __init__(
        self,
        db: Session,
    ):

        self.repository = SkillReportRepository(db)



    def create_report(
        self,
        user_id: int,
        report_data: dict,
    ):

        report = SkillReport(

            user_id=user_id,

            strong_skills=
                report_data["strong_skills"],

            weak_skills=
                report_data["weak_skills"],

            recommended_topics=
                report_data["recommended_topics"],

            summary=
                report_data["summary"],
        )


        return self.repository.create(
            report
        )



    def get_report(
        self,
        user_id: int,
    ):

        return (
            self.repository.get_by_user_id(
                user_id
            )
        )
