from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_admin
from app.schemas.prompt import (
    PromptCreate,
    PromptResponse,
)
from app.services.prompt_service import PromptService


router = APIRouter(
    prefix="/admin/prompts",
    tags=["Admin Prompts"],
)


# =====================================================
# Create Prompt Version
# =====================================================

@router.post(
    "",
    response_model=PromptResponse,
)
def create_prompt(
    data: PromptCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    service = PromptService(db)

    return service.create_prompt(
        name=data.name,
        version=data.version,
        template=data.template,
        provider=data.provider,
        model=data.model,
        temperature=data.temperature,
        is_active=data.is_active,
    )


# =====================================================
# Get Prompt History
# =====================================================

@router.get(
    "/{name}",
    response_model=list[PromptResponse],
)
def get_prompt_history(
    name: str,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    service = PromptService(db)

    return service.get_prompt_history(name)


# =====================================================
# Activate Prompt Version
# =====================================================

@router.put(
    "/{name}/{version}/activate",
)
def activate_prompt(
    name: str,
    version: str,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    service = PromptService(db)

    prompt = service.activate_prompt_version(
        name=name,
        version=version,
    )

    if prompt is None:
        raise HTTPException(
            status_code=404,
            detail="Prompt version not found",
        )

    return {
        "message": "Prompt activated successfully",
        "name": prompt.name,
        "version": prompt.version,
    }


# =====================================================
# Delete Prompt Version
# =====================================================

@router.delete(
    "/{name}/{version}",
)
def delete_prompt(
    name: str,
    version: str,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    service = PromptService(db)

    result = service.delete_prompt(
        name=name,
        version=version,
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Prompt not found",
        )

    return {
        "message": "Prompt deleted successfully",
    }
