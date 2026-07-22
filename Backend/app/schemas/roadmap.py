from datetime import datetime

from pydantic import BaseModel


# ==========================
# Weekly Plan
# ==========================

class WeeklyPlan(BaseModel):
    week: int
    focus: str
    topics: list[str]


# ==========================
# Generate Roadmap Request
# ==========================

class RoadmapCreate(BaseModel):
    skill_report_id: int


# ==========================
# AI Roadmap Response
# ==========================

class LearningRoadmapResponse(BaseModel):
    title: str
    duration: str
    weekly_plan: list[WeeklyPlan]


# ==========================
# Database Response
# ==========================

class RoadmapResponse(BaseModel):
    id: int
    user_id: int
    skill_report_id: int

    title: str
    duration: str
    weekly_plan: str

    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
