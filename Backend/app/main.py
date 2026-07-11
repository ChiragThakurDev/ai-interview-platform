from fastapi import FastAPI
from sqlalchemy import text
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.api.user import router as user_router
from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.core.config import settings
from app.core.exception_handler import (
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler,
)


from app.middleware.logging_middleware import LoggingMiddleware

from app.db.session import engine
from app.api.api_key import router as api_key_router
from app.core.logger import logger

from app.api.resume import router as resume_router

from app.api.ai import router as ai_router

logger.info("Starting AI Interview Platform...")

# -------------------------
# CREATE APP FIRST
# -------------------------
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.add_middleware(LoggingMiddleware)
# -------------------------
# EXCEPTION HANDLERS
# -------------------------
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler,)

# -------------------------
# ROUTES
# -------------------------
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(api_key_router)
app.include_router(health_router)
app.include_router(resume_router)
app.include_router(ai_router)
# -------------------------
# ROOT
# -------------------------
@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name}"
    }


# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "Database Connected Successfully"
        }

    except Exception as e:
        return {
            "status": "Database Connection Failed",
            "error": str(e)

            }        
