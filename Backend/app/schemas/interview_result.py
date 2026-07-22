from datetime import datetime

from pydantic import BaseModel, ConfigDict


# =====================================================
# Question Result
# =====================================================

class QuestionResultResponse(BaseModel):

    id: int
    question: str
    answer: str | None
    score: float | None
    feedback: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )


# =====================================================
# Interview Information
# =====================================================

class InterviewInfoResponse(BaseModel):

    id: int
    role: str
    difficulty: str
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# =====================================================
# Interview Report
# =====================================================

class InterviewReportResponse(BaseModel):

    overall_score: float | None
    strengths: str | None
    weaknesses: str | None
    recommendations: str | None
    summary: str | None

    model_config = ConfigDict(
        from_attributes=True,
    )


# =====================================================
# Final Response
# =====================================================

class InterviewResultResponse(BaseModel):

    interview: InterviewInfoResponse
    questions: list[QuestionResultResponse]
    report: InterviewReportResponse | None
