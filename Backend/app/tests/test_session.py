from app.ai.session import SessionManager


def test_create_session():

    session = SessionManager()

    session.create(
        role="Backend",
        company="Google",
    )

    assert session.exists()


def test_update_session():

    session = SessionManager()

    session.create(
        role="Backend"
    )

    session.update(
        difficulty="Hard"
    )

    assert session.value("difficulty") == "Hard"


def test_clear_session():

    session = SessionManager()

    session.create(
        role="Backend"
    )

    session.clear()

    assert session.exists() is False


def test_set_value():

    session = SessionManager()

    session.set(
        "language",
        "Python",
    )

    assert session.value("language") == "Python"
