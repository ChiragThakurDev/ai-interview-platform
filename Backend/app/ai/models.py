"""
Central AI Model Registry

This file is the single source of truth for every AI model
used by the application.

Never hardcode model names anywhere else.

Providers should always import MODEL_REGISTRY.
"""

from app.core.config import settings


# ======================================================
# Individual Models
# ======================================================

CHAT_MODEL = settings.chat_model

CODING_MODEL = settings.coding_model

JSON_MODEL = settings.json_model

FAST_MODEL = settings.fast_model

EMBEDDING_MODEL = settings.embedding_model

VISION_MODEL = settings.vision_model


# ======================================================
# Registry
# ======================================================

MODEL_REGISTRY = {

    "chat": CHAT_MODEL,

    "coding": CODING_MODEL,

    "json": JSON_MODEL,

    "fast": FAST_MODEL,

    "embedding": EMBEDDING_MODEL,

    "vision": VISION_MODEL,

}


# ======================================================
# Helper
# ======================================================

def get_model(task: str) -> str:
    """
    Returns the configured model for a task.

    Example:
        get_model("chat")
        get_model("coding")
    """

    return MODEL_REGISTRY.get(
        task,
        FAST_MODEL,
    )
