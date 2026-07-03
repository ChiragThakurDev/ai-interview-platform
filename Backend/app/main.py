from fastapi import FastAPI
from sqlalchemy import text
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from app.api.user import router as user_router
from app.api.auth import router as auth_router

from app.core.config import settings
from app.core.exception_handler import (
    http_exception_handler,
    validation_exception_handler,
)

from app.db.session import engine


# -------------------------
# CREATE APP FIRST
# -------------------------
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

# -------------------------
# EXCEPTION HANDLERS
# -------------------------
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# -------------------------
# ROUTES
# -------------------------
app.include_router(user_router)
app.include_router(auth_router)


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
