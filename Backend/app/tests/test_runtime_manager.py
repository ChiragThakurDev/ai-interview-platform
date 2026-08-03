from app.interview_runtime.manager import runtime_manager


def setup_function():
    runtime_manager.clear()


def test_create_runtime():

    runtime = runtime_manager.create(1)

    assert runtime_manager.exists(1)

    assert runtime_manager.count() == 1

    assert runtime is runtime_manager.get(1)


def test_get_same_runtime():

    first = runtime_manager.get(100)

    second = runtime_manager.get(100)

    assert first is second


def test_delete_runtime():

    runtime_manager.create(5)

    runtime_manager.delete(5)

    assert runtime_manager.exists(5) is False


def test_clear_manager():

    runtime_manager.create(1)

    runtime_manager.create(2)

    runtime_manager.clear()

    assert runtime_manager.count() == 0
