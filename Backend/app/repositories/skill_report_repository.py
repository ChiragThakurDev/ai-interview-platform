from sqlalchemy.orm import Session

from app.models.skill_report import SkillReport



class SkillReportRepository:


    def __init__(
        self,
        db: Session,
    ):
        self.db = db



    def create(
        self,
        report: SkillReport,
    ):

        self.db.add(report)

        self.db.commit()

        self.db.refresh(report)

        return report



    def get_by_user_id(
        self,
        user_id: int,
    ):

        return (
            self.db.query(
                SkillReport
            )
            .filter(
                SkillReport.user_id == user_id
            )
            .first()
        )



    def delete(
        self,
        report: SkillReport,
    ):

        self.db.delete(report)

        self.db.commit()
