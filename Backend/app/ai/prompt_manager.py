"""
Prompt Manager.

Single entry point for all prompt generation.

Priority:

1. Active prompt from PostgreSQL
2. Fallback prompt from app.ai.prompts

Responsibilities:

- Validate prompt type
- Load prompt template
- Support database-backed prompts
- Render variables dynamically
"""

import logging

from sqlalchemy.orm import Session

from app.ai.templates.renderer import PromptRenderer
from app.ai.templates.registry import (
    PROMPT_TEMPLATE_REGISTRY,
)
from app.ai.prompts import (
    RESUME_ANALYSIS_PROMPT,
    INTERVIEW_GENERATION_PROMPT,
    ANSWER_EVALUATION_PROMPT,
    INTERVIEW_REPORT_PROMPT,
    SKILL_ANALYSIS_PROMPT,
    ROADMAP_PROMPT,
    CHAT_SYSTEM_PROMPT,
    CODING_INTERVIEW_GENERATION_PROMPT,
    CODING_EVALUATION_PROMPT,
    CODING_INTERVIEW_REPORT_PROMPT,
)

from app.services.prompt_service import PromptService
from app.ai.prompt_loader import PromptLoader

logger = logging.getLogger(__name__)


class PromptManager:
    """
    Central prompt management system.

    Priority:

    Database
        ↓
    Fallback Templates
        ↓
    Prompt Renderer
    """

    # --------------------------------------------------
    # Fallback Templates
    # --------------------------------------------------

    TEMPLATES = {

        "resume_analysis":
            RESUME_ANALYSIS_PROMPT,

        "interview_generation":
            INTERVIEW_GENERATION_PROMPT,

        "answer_evaluation":
            ANSWER_EVALUATION_PROMPT,

        "interview_report":
            INTERVIEW_REPORT_PROMPT,

        "skill_analysis":
            SKILL_ANALYSIS_PROMPT,

        "roadmap":
            ROADMAP_PROMPT,

        "chat":
            CHAT_SYSTEM_PROMPT,

        "chat_system":
            CHAT_SYSTEM_PROMPT,

        "coding_interview_generation":
            CODING_INTERVIEW_GENERATION_PROMPT,

        "coding_evaluation":
            CODING_EVALUATION_PROMPT,

        "coding_interview_report":
            CODING_INTERVIEW_REPORT_PROMPT,
    }

    @staticmethod
    def build(
        prompt_type: str,
        db: Session | None = None,
        **kwargs,
    ) -> str:
        """
        Build final prompt.

        Flow:

        Prompt Type
              │
              ▼
        PostgreSQL
              │
      Exists? │
        Yes   │   No
         ▼    │    ▼
     DB Prompt │ Fallback Template
          \    │    /
           ▼   ▼   ▼
          PromptRenderer
                │
                ▼
          Final Prompt
        """

        # ------------------------------------------
        # Validate prompt type
        # ------------------------------------------

        if prompt_type not in PROMPT_TEMPLATE_REGISTRY:
            raise ValueError(
                f"Unknown prompt type: {prompt_type}"
            )

        template = None
        db_prompt_loaded = False

        # ------------------------------------------
        # Try loading active prompt from DB
        # ------------------------------------------

        if db is not None:

            service = PromptService(db)

            loader = PromptLoader(service)

            try:

                template = loader.load(
                    prompt_type,
                    kwargs,
                )

                db_prompt_loaded = True

            except Exception as e:

                logger.warning(
                    "Using fallback prompt for '%s': %s",
                    prompt_type,
                    e,
                )

        # ------------------------------------------
        # Fallback to hardcoded template
        # ------------------------------------------

        if template is None:

            template = PromptManager.TEMPLATES.get(
                prompt_type
            )

            if template is None:

                logger.error(
                    "Missing prompt template: %s",
                    prompt_type,
                )

                raise ValueError(
                    f"Prompt template missing: {prompt_type}"
                )

        # ------------------------------------------
        # Database prompt is already rendered
        # ------------------------------------------

        if db_prompt_loaded:
            return template

        # ------------------------------------------
        # Render fallback template
        # ------------------------------------------

        return PromptRenderer.render(
            template,
            **kwargs,
        )
