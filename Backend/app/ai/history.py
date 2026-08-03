"""
AI history models.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AIHistory:

    prompt: str

    response: str

    model: str

    provider: str

    created_at: datetime = datetime.utcnow()
