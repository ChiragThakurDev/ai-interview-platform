import os

os.environ["ENV_FILE"] = ".env.test"


import pytest

from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from app.main import app

from app.db.dependencies import get_db
from app.db.session import engine
from app.db.base import Base

from app.utils.jwt import create_access_token


# Import models so SQLAlchemy registers all tables
from app.models.user import User
from app.models.resume import Resume
from app.models.resume_analysis import ResumeAnalysis
from app.models.interview import Interview
from app.models.interview_answer import InterviewAnswer
from app.models.interview_report import InterviewReport
from app.models.skill_report import SkillReport


from app.tests.factories import (
    create_test_user,
    create_second_user,
)



TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)



@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """
    Create test database tables before running tests.
    """

    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)




@pytest.fixture
def db():

    connection = engine.connect()

    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)


    try:
        yield session

    finally:

        session.close()

        if transaction.is_active:
            transaction.rollback()

        connection.close()




@pytest.fixture
def client(db):

    def override_get_db():

        yield db


    app.dependency_overrides[get_db] = override_get_db


    with TestClient(app) as test_client:

        yield test_client


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




@pytest.fixture
def auth_headers(test_user):

    token = create_access_token(
        {
            "sub": test_user.email,
        }
    )


    return {
        "Authorization": f"Bearer {token}",
    }




@pytest.fixture
def admin_headers(admin_user):

    token = create_access_token(
        {
            "sub": admin_user.email,
        }
    )


    return {
        "Authorization": f"Bearer {token}",
    }
