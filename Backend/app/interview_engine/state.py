"""
Interview State.

Tracks the current interview progress.
"""

from dataclasses import dataclass


@dataclass
class InterviewState:
    current_question: int = 0
    score: float = 0.0
    difficulty: str = "medium"
    completed: bool = False

    def next_question(self):
        self.current_question += 1

    def finish(self):
        self.completed = True

    def update_score(self, value: float):
        self.score += value

    def reset(self):
        self.current_question = 0
        self.score = 0.0
        self.difficulty = "medium"
        self.completed = False
