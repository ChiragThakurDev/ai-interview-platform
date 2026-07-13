from pydantic import BaseModel


class ProgressResponse(BaseModel):
    current_score: int
    previous_score: int | None
    improvement: int
    trend: str
