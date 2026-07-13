from pydantic import BaseModel


class WeeklyPlan(BaseModel):
    week: int
    focus: str
    topics: list[str]


class LearningRoadmapResponse(BaseModel):
    title: str
    duration: str
    weekly_plan: list[WeeklyPlan]
