"""
Interview scoring.
"""


class InterviewScorer:

    def score(
        self,
        ai_score: float,
        max_score: float = 10.0,
    ) -> float:

        if ai_score < 0:
            ai_score = 0

        if ai_score > max_score:
            ai_score = max_score

        return round(ai_score, 2)

    def percentage(
        self,
        score: float,
        total: float,
    ) -> float:

        if total == 0:
            return 0.0

        return round(score / total * 100, 2)
