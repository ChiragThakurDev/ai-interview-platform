import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.db.session import SessionLocal
from app.services.api_log_service import APILogService
from app.utils.jwt import verify_access_token


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next,
    ):

        start_time = time.time()

        response = await call_next(request)

        response_time = int(
            (time.time() - start_time) * 1000
        )

        user_id = None

        authorization = request.headers.get(
            "Authorization"
        )

        if authorization and authorization.startswith(
            "Bearer "
        ):

            token = authorization.split(" ")[1]

            payload = verify_access_token(token)

            if payload:
                user_id = payload.get("user_id")

        db = SessionLocal()

        try:

            service = APILogService(db)

            service.create_log(
                user_id=user_id,
                method=request.method,
                endpoint=request.url.path,
                status_code=response.status_code,
                response_time=response_time,
                ip_address=request.client.host
                if request.client
                else "",
            )

        finally:
            db.close()

        return response
