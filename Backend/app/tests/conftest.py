import os

os.environ["ENV_FILE"] = ".env.test"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.dependencies import get_db
from app.db.session import engine
from app.tests.factories import (create_test_user, create_second_user,)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db):
    return create_test_user(db)


@pytest.fixture
def admin_user(db):
    user = create_test_user(
        db,
        name="Admin",
        email="admin@example.com",
        password="123@chirag",
    )

    user.role = "admin"
    db.commit()
    db.refresh(user)

    return user

@pytest.fixture
def second_user(db):
    return create_second_user(db)
