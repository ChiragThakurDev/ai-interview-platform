from pydantic import BaseModel


class LeaderboardEntry(BaseModel):
    user_id: int
    user_name: str
    total_interviews: int
    best_score: int
    average_score: float


class LeaderboardResponse(BaseModel):
    leaderboard: list[LeaderboardEntry]
