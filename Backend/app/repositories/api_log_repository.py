from sqlalchemy.orm import Session

from app.models.api_log import APILog


class APILogRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        **kwargs,
    ):

        log = APILog(
            **kwargs,
        )

        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)

        return log

    def get_all(
        self,
    ):

        return (
            self.db.query(
                APILog
            )
            .order_by(
                APILog.created_at.desc()
            )
            .all()
        )

    def get_by_user(
        self,
        user_id: int,
    ):

        return (
            self.db.query(
                APILog
            )
            .filter(
                APILog.user_id == user_id
            )
            .order_by(
                APILog.created_at.desc()
            )
            .all()
        )
