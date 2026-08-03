from datetime import datetime, UTC

from sqlalchemy.orm import Session

from app.models.prompt import Prompt


class PromptRepository:
    """
    Repository for managing AI prompts.

    Responsibilities:
    - Fetch active prompts
    - Manage versions
    - Activate/deactivate versions
    - Create/update/delete prompts
    """


    def __init__(
        self,
        db: Session
    ):
        self.db = db



    # =====================================================
    # Get Active Prompt
    # =====================================================

    def get_active(
        self,
        name: str
    ):
        """
        Get active prompt version.
        """

        return (
            self.db.query(Prompt)
            .filter(
                Prompt.name == name,
                Prompt.is_active.is_(True)
            )
            .first()
        )



    # =====================================================
    # Get Specific Version
    # =====================================================

    def get_version(
        self,
        name: str,
        version: str
    ):
        """
        Get prompt by version.
        """

        return (
            self.db.query(Prompt)
            .filter(
                Prompt.name == name,
                Prompt.version == version
            )
            .first()
        )



    # =====================================================
    # Get All Versions
    # =====================================================

    def get_all_versions(
        self,
        name: str
    ):
        """
        Return all versions of prompt.
        """

        return (
            self.db.query(Prompt)
            .filter(
                Prompt.name == name
            )
            .order_by(
                Prompt.created_at.desc()
            )
            .all()
        )



    # =====================================================
    # Create Prompt
    # =====================================================

    def create(
        self,
        prompt: Prompt
    ):
        """
        Create new prompt version.
        """

        self.db.add(prompt)

        self.db.commit()

        self.db.refresh(prompt)

        return prompt



    # =====================================================
    # Update Prompt
    # =====================================================

    def update(
        self,
        prompt: Prompt,
        data: dict
    ):
        """
        Update prompt fields.
        """

        for key, value in data.items():

            if hasattr(prompt, key):

                setattr(
                    prompt,
                    key,
                    value
                )


        prompt.updated_at = datetime.now(UTC)


        self.db.commit()

        self.db.refresh(prompt)


        return prompt



    # =====================================================
    # Disable All Versions
    # =====================================================

    def deactivate_versions(
        self,
        name: str
    ):
        """
        Disable all active versions.
        """

        (
            self.db.query(Prompt)
            .filter(
                Prompt.name == name
            )
            .update(
                {
                    "is_active": False
                }
            )
        )


        self.db.commit()



    # =====================================================
    # Activate Version
    # =====================================================

    def activate_version(
        self,
        name: str,
        version: str
    ):
        """
        Activate selected prompt version.

        Example:

        v1 -> inactive
        v2 -> active
        """

        self.deactivate_versions(
            name
        )


        prompt = self.get_version(
            name,
            version
        )


        if prompt is None:
            return None


        prompt.is_active = True

        prompt.updated_at = datetime.now(UTC)


        self.db.commit()

        self.db.refresh(prompt)


        return prompt



    # =====================================================
    # Delete Prompt
    # =====================================================

    def delete(
        self,
        prompt: Prompt
    ):
        """
        Delete prompt version.
        """

        self.db.delete(
            prompt
        )

        self.db.commit()



    # =====================================================
    # Get Prompt Configuration
    # =====================================================

    def get_config(
        self,
        name: str
    ):
        """
        Return active prompt AI configuration.

        Used by LLM factory.

        Returns:

        {
            model,
            temperature,
            provider
        }

        """

        prompt = self.get_active(
            name
        )


        if not prompt:
            return None



        return {
            "provider": prompt.provider,
            "model": prompt.model,
            "temperature": prompt.temperature,
            "template": prompt.template,
        }
