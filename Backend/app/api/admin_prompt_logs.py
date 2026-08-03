from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_admin

from app.repositories.prompt_analytics_repository import (
    PromptAnalyticsRepository,
)

from app.services.prompt_analytics_service import (
    PromptAnalyticsService,
)

router = APIRouter(
    prefix="/admin/prompt-logs",
    tags=["Admin Prompt Analytics"],
)


def get_service(
    db: Session,
) -> PromptAnalyticsService:

    repository = PromptAnalyticsRepository(
        db
    )

    return PromptAnalyticsService(
        repository
    )


# =====================================================
# Overall Statistics
# =====================================================

@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):

    service = get_service(db)

    return service.get_stats()


# =====================================================
# Prompt Usage
# =====================================================

@router.get("/usage")
def get_prompt_usage(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):

    service = get_service(db)

    return service.get_prompt_usage()


# =====================================================
# Model Usage
# =====================================================

@router.get("/models")
def get_model_usage(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):

    service = get_service(db)

    return service.get_model_usage()


# =====================================================
# Average Latency
# =====================================================

@router.get("/latency")
def get_average_latency(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):

    service = get_service(db)

    return service.get_average_latency()


# =====================================================
# Failed Executions
# =====================================================

@router.get("/errors")
def get_failed_executions(
    limit: int = 100,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):

    service = get_service(db)

    return service.get_failed_executions(
        limit
    )


# =====================================================
# Daily Usage
# =====================================================

@router.get("/daily")
def get_daily_usage(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):

    service = get_service(db)

    return service.get_daily_usage()
