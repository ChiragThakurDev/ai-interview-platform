from sqlalchemy.orm import Session

from app.repositories.prompt_repository import PromptRepository
from app.services.prompt_service import PromptService
from app.ai.prompt_loader import PromptLoader


def get_prompt_repository(
    db: Session
):
    return PromptRepository(
        db
    )


def get_prompt_service(
    db: Session
):
    repository = PromptRepository(
        db
    )

    return PromptService(
        repository
    )


def get_prompt_loader(
    db: Session
):
    repository = PromptRepository(
        db
    )

    service = PromptService(
        repository
    )

    return PromptLoader(
        service
    )
