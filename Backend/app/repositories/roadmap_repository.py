from sqlalchemy.orm import Session

from app.models.roadmap import Roadmap


class RoadmapRepository:

    def __init__(self, db: Session):
        self.db = db

    # -------------------------
    # Create
    # -------------------------
    def create(self, roadmap: Roadmap):
        self.db.add(roadmap)
        self.db.commit()
        self.db.refresh(roadmap)
        return roadmap

    # -------------------------
    # Get by ID
    # -------------------------
    def get_by_id(self, roadmap_id: int):
        return (
            self.db.query(Roadmap)
            .filter(Roadmap.id == roadmap_id)
            .first()
        )

    # -------------------------
    # Get by User
    # -------------------------
    def get_by_user(self, user_id: int):
        return (
            self.db.query(Roadmap)
            .filter(Roadmap.user_id == user_id)
            .order_by(Roadmap.created_at.desc())
            .all()
        )

    # -------------------------
    # Get by Skill Report
    # -------------------------
    def get_by_skill_report(self, skill_report_id: int):
        return (
            self.db.query(Roadmap)
            .filter(
                Roadmap.skill_report_id == skill_report_id
            )
            .first()
        )

    # -------------------------
    # Update
    # -------------------------
    def update(self, roadmap: Roadmap):
        self.db.commit()
        self.db.refresh(roadmap)
        return roadmap

    # -------------------------
    # Delete
    # -------------------------
    def delete(self, roadmap: Roadmap):
        self.db.delete(roadmap)
        self.db.commit()
