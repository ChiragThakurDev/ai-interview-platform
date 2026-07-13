from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict



# AI output schema
class AIInterviewReportResponse(BaseModel):

    overall_score: int = Field(
        ...,
        ge=0,
        le=100,
    )

    technical_level: str

    communication: str

    strengths: list[str]

    weaknesses: list[str]

    recommendation: str

    summary: str




# Database response schema
class InterviewReportResponse(BaseModel):

    id: int

    interview_id: int

    overall_score: int = Field(
        ...,
        ge=0,
        le=100,
    )

    technical_level: str

    communication: str

    strengths: list[str]

    weaknesses: list[str]

    recommendation: str

    summary: str

    created_at: datetime


    model_config = ConfigDict(
        from_attributes=True,
    )
