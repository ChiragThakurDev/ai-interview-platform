from app.ai.history import HistoryManager


def test_history_append():

    history = HistoryManager()

    history.append(
        "user",
        "Hello"
    )

    assert history.count() == 1


def test_history_clear():

    history = HistoryManager()

    history.append(
        "user",
        "Hello"
    )

    history.clear()

    assert history.count() == 0


def test_history_last():

    history = HistoryManager()

    history.append(
        "user",
        "Hello"
    )

    assert history.last()["content"] == "Hello"
