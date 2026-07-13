from datetime import datetime

from pydantic import BaseModel, ConfigDict



class SkillReportResponse(BaseModel):

    id: int

    user_id: int

    strong_skills: list[str]

    weak_skills: list[str]

    recommended_topics: list[str]

    summary: str

    created_at: datetime


    model_config = ConfigDict(
        from_attributes=True,
    )
