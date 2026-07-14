from pydantic import BaseModel


class DifficultyStats(BaseModel):
    easy: float
    medium: float
    hard: float


class AnalyticsResponse(BaseModel):
    score_distribution: dict[str, int]
    difficulty_stats: DifficultyStats
    role_stats: dict[str, int]
