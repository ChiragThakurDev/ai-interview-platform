from sqlalchemy.orm import Session

from app.models.prompt import Prompt


class PromptRepository:

    def __init__(
        self,
        db: Session
    ):
        self.db = db


    def get_active(
        self,
        name: str
    ):
        """
        Get currently active prompt version.
        """

        return (
            self.db.query(Prompt)
            .filter(
                Prompt.name == name,
                Prompt.is_active.is_(True)
            )
            .first()
        )


    def get_version(
        self,
        name: str,
        version: str
    ):
        """
        Get a specific prompt version.
        """

        return (
            self.db.query(Prompt)
            .filter(
                Prompt.name == name,
                Prompt.version == version
            )
            .first()
        )


    def get_all_versions(
        self,
        name: str
    ):
        """
        Get all versions of a prompt.
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


    def deactivate_versions(
        self,
        name: str
    ):
        """
        Disable all previous versions
        before activating a new one.
        """

        (
            self.db.query(Prompt)
            .filter(
                Prompt.name == name
            )
            .update(
                {
                    Prompt.is_active: False
                }
            )
        )

        self.db.commit()


    def activate_version(
        self,
        name: str,
        version: str
    ):
        """
        Activate selected prompt version.
        """

        # Disable old versions
        self.deactivate_versions(name)


        # Activate selected version
        prompt = self.get_version(
            name,
            version
        )

        if prompt:
            prompt.is_active = True

            self.db.commit()

            self.db.refresh(prompt)


        return prompt


    def delete(
        self,
        prompt: Prompt
    ):
        """
        Delete prompt version.
        """

        self.db.delete(prompt)

        self.db.commit()
