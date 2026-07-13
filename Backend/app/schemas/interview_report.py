from pydantic import BaseModel, Field


class InterviewReportResponse(BaseModel):
    overall_score: int = Field(..., ge=0, le=100)

    technical_level: str

    communication: str

    strengths: list[str]

    weaknesses: list[str]

    recommendation: str

    summary: str
