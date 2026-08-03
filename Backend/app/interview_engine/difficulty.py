"""
Adaptive interview difficulty.
"""


class DifficultyManager:

    LEVELS = [
        "easy",
        "medium",
        "hard",
    ]

    def increase(
        self,
        level: str,
    ) -> str:

        if level == "easy":
            return "medium"

        if level == "medium":
            return "hard"

        return "hard"

    def decrease(
        self,
        level: str,
    ) -> str:

        if level == "hard":
            return "medium"

        if level == "medium":
            return "easy"

        return "easy"

    def next_level(
        self,
        current: str,
        score: float,
    ) -> str:

        if score >= 8:
            return self.increase(current)

        if score <= 4:
            return self.decrease(current)

        return current
