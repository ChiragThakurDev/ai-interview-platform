from datetime import datetime

from pydantic import BaseModel


class RecentInterviewResponse(BaseModel):

    id: int

    role: str

    difficulty: str

    score: float | None = None

    created_at: datetime


    class Config:
        from_attributes = True



class DashboardResponse(BaseModel):

    total_interviews: int

    average_score: float

    highest_score: float

    total_questions_answered: int

    recent_interviews: list[RecentInterviewResponse]
