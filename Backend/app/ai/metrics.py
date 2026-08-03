"""
AI Metrics

Tracks AI performance across the application.
"""

from dataclasses import dataclass
from time import perf_counter


@dataclass
class AIMetrics:

    model: str

    provider: str

    start_time: float

    end_time: float | None = None

    success: bool = True

    error: str | None = None

    @property
    def duration(self) -> float:

        if self.end_time is None:
            return 0.0

        return round(
            self.end_time - self.start_time,
            3,
        )


class Timer:

    def __init__(self):

        self.start = perf_counter()

    def stop(self):

        return perf_counter() - self.start
