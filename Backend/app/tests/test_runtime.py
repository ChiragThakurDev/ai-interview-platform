from app.interview_runtime.result import InterviewResult


def test_result_defaults():

    result = InterviewResult()

    assert result.total_score == 0

    assert result.completed is False


def test_result_completed():

    result = InterviewResult()

    result.mark_completed()

    assert result.completed


def test_result_dict():

    result = InterviewResult(
        total_score=80,
        average_score=8,
        answered_questions=10,
        skipped_questions=1,
        duration_seconds=1800,
        feedback="Excellent interview",
    )

    data = result.to_dict()

    assert data["total_score"] == 80

    assert data["average_score"] == 8

    assert data["feedback"] == "Excellent interview"

    assert "created_at" in data
