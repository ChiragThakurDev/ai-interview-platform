"""
Question selector.
"""

import random


class QuestionSelector:

    def choose(self, questions):

        if not questions:
            return None

        return random.choice(questions)

    def choose_by_difficulty(
        self,
        questions,
        difficulty,
    ):

        filtered = [
            q
            for q in questions
            if q.difficulty == difficulty
        ]

        if not filtered:
            return None

        return random.choice(filtered)
