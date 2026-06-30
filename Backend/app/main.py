from fastapi import FastAPI
from sqlalchemy import text
from app.api.user import router as user_router
from app.core.config import settings
from app.db.session import engine

from app.models.user import User
from app.db.base import Base

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.include_router(user_router)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name}"
    }


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
