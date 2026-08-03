from sqlalchemy.orm import Session

from app.models.prompt_execution import PromptExecution


class PromptExecutionRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # =====================================================
    # Create Log
    # =====================================================

    def create(
        self,
        execution: PromptExecution,
    ):
        """
        Save prompt execution.
        """

        self.db.add(execution)

        self.db.commit()

        self.db.refresh(execution)

        return execution

    # =====================================================
    # List Logs
    # =====================================================

    def get_all(
        self,
        limit: int = 100,
    ):
        return (
            self.db.query(PromptExecution)
            .order_by(
                PromptExecution.created_at.desc()
            )
            .limit(limit)
            .all()
        )

    # =====================================================
    # Filter by Prompt
    # =====================================================

    def get_by_prompt(
        self,
        prompt_name: str,
        limit: int = 100,
    ):
        return (
            self.db.query(PromptExecution)
            .filter(
                PromptExecution.prompt_name == prompt_name
            )
            .order_by(
                PromptExecution.created_at.desc()
            )
            .limit(limit)
            .all()
        )

    # =====================================================
    # Latest Execution
    # =====================================================

    def latest(
        self,
    ):
        return (
            self.db.query(PromptExecution)
            .order_by(
                PromptExecution.created_at.desc()
            )
            .first()
        )
