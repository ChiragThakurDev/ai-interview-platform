from pydantic import BaseModel


class TopicItem(BaseModel):
    topic: str
    average_score: float
    total_questions: int


class TopicAnalysisResponse(BaseModel):
    topics: list[TopicItem]
