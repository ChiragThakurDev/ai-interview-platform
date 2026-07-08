from fastapi import APIRouter
from sqlalchemy import text

from app.db.session import engine
from app.core.redis import redis_client


router = APIRouter()


@router.get("/health")
async def health_check():

    database_status = "unknown"
    redis_status = "unknown"

    # Check PostgreSQL
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        database_status = "connected"

    except Exception:
        database_status = "failed"


    # Check Redis
    try:
        await redis_client.ping()
        redis_status = "connected"

    except Exception:
        redis_status = "failed"


    return {
        "status": "ok",
        "database": database_status,
        "redis": redis_status
    }
