from pydantic import BaseModel


# =====================================================
# CLIENT -> SERVER
# =====================================================

class SubmitCodeMessage(BaseModel):
    type: str
    question_id: int
    language: str
    code: str


# =====================================================
# SERVER -> CLIENT
# =====================================================

class ExecutionResponse(BaseModel):
    success: bool
    stdout: str
    stderr: str
    return_code: int


class EvaluationResponse(BaseModel):
    passed: bool
    score: int
    correctness: int
    code_quality: int
    time_complexity: str
    space_complexity: str
    strengths: list[str]
    weaknesses: list[str]
    bugs: list[str]
    optimization_suggestions: list[str]
    feedback: str


class SubmissionResultMessage(BaseModel):
    type: str
    execution: ExecutionResponse
    evaluation: EvaluationResponse
