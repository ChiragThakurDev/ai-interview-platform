from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RecentInterviewResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    role: str

    difficulty: str

    score: float | None = None

    created_at: datetime



class DashboardResponse(BaseModel):

    total_interviews: int

    average_score: float

    highest_score: float

    total_questions_answered: int

    recent_interviews: list[RecentInterviewResponse]
