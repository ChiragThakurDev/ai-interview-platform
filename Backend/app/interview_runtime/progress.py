"""
Interview Progress Tracker.
"""

from dataclasses import dataclass


@dataclass
class InterviewProgress:
    total_questions: int = 0
    answered_questions: int = 0
    skipped_questions: int = 0
    correct_answers: int = 0
    wrong_answers: int = 0
    total_score: float = 0.0

    def answer(self, score: float):
        self.answered_questions += 1
        self.total_score += score

        if score >= 6:
            self.correct_answers += 1
        else:
            self.wrong_answers += 1

    def skip(self):
        self.skipped_questions += 1

    @property
    def average_score(self):

        if self.answered_questions == 0:
            return 0.0

        return round(
            self.total_score / self.answered_questions,
            2,
        )

    @property
    def completion(self):

        if self.total_questions == 0:
            return 0

        return round(
            self.answered_questions
            / self.total_questions
            * 100,
            2,
        )

    def reset(self):

        self.answered_questions = 0
        self.skipped_questions = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        self.total_score = 0.0
