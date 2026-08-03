"""
Central Interview Engine.
"""

from app.interview_engine.difficulty import DifficultyManager
from app.interview_engine.flow import InterviewFlow
from app.interview_engine.question_selector import QuestionSelector
from app.interview_engine.scorer import InterviewScorer


class InterviewEngine:

    def __init__(self):

        self.flow = InterviewFlow()

        self.scorer = InterviewScorer()

        self.selector = QuestionSelector()

        self.difficulty = DifficultyManager()
