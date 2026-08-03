from app.interview_runtime.controller import InterviewController
from app.interview_runtime.manager import runtime_manager


def setup_function():

    runtime_manager.clear()


def test_start_runtime():

    controller = InterviewController()

    runtime = controller.start(1)

    assert runtime.started

    assert runtime_manager.exists(1)


def test_submit_answer():

    controller = InterviewController()

    controller.start(1)

    runtime = controller.submit_answer(
        1,
        8,
    )

    assert runtime.progress.answered_questions == 1

    assert runtime.progress.total_score == 8


def test_skip_question():

    controller = InterviewController()

    controller.start(1)

    runtime = controller.skip_question(1)

    assert runtime.progress.skipped_questions == 1


def test_finish_runtime():

    controller = InterviewController()

    controller.start(1)

    runtime = controller.finish(1)

    assert runtime.finished


def test_remove_runtime():

    controller = InterviewController()

    controller.start(1)

    controller.remove_runtime(1)

    assert runtime_manager.exists(1) is False
