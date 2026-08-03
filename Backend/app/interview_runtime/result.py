"""
Interview Result.

Represents the final interview outcome.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class InterviewResult:

    total_score: float = 0.0

    average_score: float = 0.0

    answered_questions: int = 0

    skipped_questions: int = 0

    duration_seconds: int = 0

    feedback: str = ""

    completed: bool = False

    created_at: datetime = field(default_factory=datetime.utcnow)

    def mark_completed(self):

        self.completed = True

    def to_dict(self):

        return {
            "total_score": self.total_score,
            "average_score": self.average_score,
            "answered_questions": self.answered_questions,
            "skipped_questions": self.skipped_questions,
            "duration_seconds": self.duration_seconds,
            "feedback": self.feedback,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
        }
