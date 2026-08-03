from app.interview_engine.state import InterviewState
from app.interview_engine.scorer import InterviewScorer
from app.interview_engine.difficulty import DifficultyManager


def test_state():

    state = InterviewState()

    state.next_question()

    assert state.current_question == 1


def test_score():

    scorer = InterviewScorer()

    assert scorer.score(9.5) == 9.5


def test_percentage():

    scorer = InterviewScorer()

    assert scorer.percentage(8, 10) == 80.0


def test_difficulty():

    manager = DifficultyManager()

    assert manager.next_level("medium", 9) == "hard"

    assert manager.next_level("medium", 3) == "easy"
