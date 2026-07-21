from sqlalchemy.orm import Session

from app.repositories.api_log_repository import (
    APILogRepository,
)


class APILogService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = APILogRepository(db)

    def create_log(
        self,
        user_id: int | None,
        method: str,
        endpoint: str,
        status_code: int,
        response_time: int,
        ip_address: str,
    ):

        return self.repository.create(
            user_id=user_id,
            method=method,
            endpoint=endpoint,
            status_code=status_code,
            response_time=response_time,
            ip_address=ip_address,
        )

    def get_logs(self):

        return self.repository.get_all()

    def get_user_logs(
        self,
        user_id: int,
    ):

        return self.repository.get_by_user(
            user_id
        )
