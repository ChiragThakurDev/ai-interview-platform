from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.prompt import Prompt
from app.repositories.prompt_repository import PromptRepository


class AdminPromptService:

    def __init__(
        self,
        db: Session
    ):
        self.repository = PromptRepository(db)


    # ==========================================
    # Create Prompt Version
    # ==========================================

    def create_prompt(
        self,
        data
    ):

        existing = self.repository.get_version(
            data.name,
            data.version
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Prompt version already exists"
            )


        prompt = Prompt(
            name=data.name,
            version=data.version,
            template=data.template,
            provider=data.provider,
            model=data.model,
            temperature=data.temperature,
            is_active=data.is_active,
        )


        if data.is_active:
            self.repository.deactivate_versions(
                data.name
            )


        return self.repository.create(
            prompt
        )


    # ==========================================
    # Get Prompt History
    # ==========================================

    def get_history(
        self,
        name: str
    ):

        return self.repository.get_all_versions(
            name
        )


    # ==========================================
    # Activate Prompt Version
    # ==========================================

    def activate(
        self,
        name: str,
        version: str
    ):

        prompt = self.repository.activate_version(
            name,
            version
        )


        if not prompt:
            raise HTTPException(
                status_code=404,
                detail="Prompt version not found"
            )


        return prompt



    # ==========================================
    # Delete Prompt Version
    # ==========================================

    def delete(
        self,
        name: str,
        version: str
    ):

        prompt = self.repository.get_version(
            name,
            version
        )


        if not prompt:
            raise HTTPException(
                status_code=404,
                detail="Prompt version not found"
            )


        return self.repository.delete(
            prompt
        )
