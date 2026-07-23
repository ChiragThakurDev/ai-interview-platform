from datetime import datetime

from pydantic import BaseModel, ConfigDict



# =====================================================
# Create Coding Interview Request
# =====================================================

class CreateCodingInterviewRequest(BaseModel):

    role: str

    company: str | None = None

    language: str = "python"

    difficulty: str = "medium"

    number_of_questions: int = 5




# =====================================================
# Coding Question Response
# =====================================================

class CodingQuestionResponse(BaseModel):

    id: int

    title: str

    description: str

    starter_code: str | None = None

    difficulty: str


    model_config = ConfigDict(
        from_attributes=True,
    )





# =====================================================
# Coding Interview Response
# =====================================================

class CodingInterviewResponse(BaseModel):

    id: int

    user_id: int

    role: str

    company: str | None = None

    language: str

    difficulty: str

    status: str

    score: int | None = None

    created_at: datetime


    model_config = ConfigDict(
        from_attributes=True,
    )





# =====================================================
# Create Interview Response
# =====================================================

class CreateCodingInterviewResponse(BaseModel):

    interview: CodingInterviewResponse

    questions: list[CodingQuestionResponse]





# =====================================================
# Submit Code Request
# =====================================================

class SubmitCodeRequest(BaseModel):

    question_id: int

    language: str

    code: str





# =====================================================
# Submission Response
# =====================================================

class SubmissionResponse(BaseModel):

    passed: bool

    score: int

    feedback: str | None = None

    output: str | None = None





# =====================================================
# Coding Interview Result
# =====================================================

class CodingInterviewResultResponse(BaseModel):

    interview_id: int

    status: str

    score: int | None = None

    completed_at: datetime | None = None


# =====================================================
# CODING INTERVIEW PROGRESS
# =====================================================

class CodingInterviewProgressResponse(BaseModel):

    interview_id: int

    status: str

    total_questions: int

    answered_questions: int

    remaining_questions: int

    current_score: int

    progress_percentage: int



# =====================================================
# CODING INTERVIEW REPORT
# =====================================================

class CodingInterviewReportResponse(BaseModel):

    overall_score: int

    technical_level: str

    strengths: list[str]

    weaknesses: list[str]

    recommendation: str

    summary: str
