from app.interview_runtime.bootstrap import RuntimeBootstrap
from app.interview_runtime.manager import runtime_manager


class DummyInterview:

    def __init__(
        self,
        interview_id,
        current_question,
        status,
    ):
        self.id = interview_id
        self.current_question = current_question
        self.status = status


def setup_function():

    runtime_manager.clear()


def test_bootstrap_new():

    interview = DummyInterview(
        1,
        1,
        "pending",
    )

    runtime = RuntimeBootstrap().build(
        interview,
        10,
    )

    assert runtime.progress.total_questions == 10

    assert runtime.current_question == 1

    assert runtime.started is False


def test_bootstrap_in_progress():

    interview = DummyInterview(
        2,
        4,
        "in_progress",
    )

    runtime = RuntimeBootstrap().build(
        interview,
        15,
    )

    assert runtime.started

    assert runtime.current_question == 4


def test_bootstrap_completed():

    interview = DummyInterview(
        3,
        10,
        "completed",
    )

    runtime = RuntimeBootstrap().build(
        interview,
        10,
    )

    assert runtime.finished
