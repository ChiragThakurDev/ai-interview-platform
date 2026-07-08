from fastapi import APIRouter
from sqlalchemy import text

from app.db.session import engine
from app.db.redis import redis_client


router = APIRouter()


@router.get("/health")
def health_check():

    database_status = "unknown"
    redis_status = "unknown"


    # PostgreSQL check
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        database_status = "connected"

    except Exception as e:
        print("Database error:", e)
        database_status = "failed"



    # Redis check
    try:
        redis_client.ping()
        redis_status = "connected"

    except Exception as e:
        print("Redis error:", e)
        redis_status = "failed"



    return {
        "status": "ok",
        "database": database_status,
        "redis": redis_status
    }
