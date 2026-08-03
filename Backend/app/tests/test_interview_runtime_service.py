from app.services.interview_runtime_service import (
    InterviewRuntimeService,
)
from app.interview_runtime.manager import runtime_manager


def setup_function():
    runtime_manager.clear()


def test_start_runtime():

    service = InterviewRuntimeService()

    runtime = service.start_runtime(1)

    assert runtime.started


def test_submit_answer():

    service = InterviewRuntimeService()

    service.start_runtime(1)

    runtime = service.submit_answer(
        1,
        9,
    )

    assert runtime.progress.answered_questions == 1

    assert runtime.progress.total_score == 9


def test_skip_question():

    service = InterviewRuntimeService()

    service.start_runtime(1)

    runtime = service.skip_question(1)

    assert runtime.progress.skipped_questions == 1


def test_finish_runtime():

    service = InterviewRuntimeService()

    service.start_runtime(1)

    runtime = service.finish_runtime(1)

    assert runtime.finished


def test_remove_runtime():

    service = InterviewRuntimeService()

    service.start_runtime(1)

    service.remove_runtime(1)

    assert runtime_manager.exists(1) is False
