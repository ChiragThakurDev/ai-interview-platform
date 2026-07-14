import pytest

from app.tests.factories import (
    create_test_resume,
    create_test_interview,
    create_test_question,
    create_test_answer,
    create_test_report,
)


# =====================================================
# Dashboard Summary
# =====================================================

def test_dashboard_summary_success(
    client,
    db,
    test_user,
    auth_headers,
):

    resume = create_test_resume(
        db,
        test_user,
    )

    interview = create_test_interview(
        db,
        test_user,
        resume,
    )

    question = create_test_question(
        db,
        interview,
    )

    create_test_answer(
        db,
        question,
        score=80,
    )

    create_test_report(
        db,
        interview,
        score=80,
    )

    response = client.get(
        "/dashboard",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_interviews"] == 1
    assert data["average_score"] == 80
    assert data["highest_score"] == 80
    assert data["total_questions_answered"] == 1

    assert len(
        data["recent_interviews"]
    ) == 1

    recent = data["recent_interviews"][0]

    assert recent["role"] == "Backend Developer"
    assert recent["difficulty"] == "hard"
    assert recent["score"] == 80


# =====================================================
# Empty Dashboard
# =====================================================

def test_dashboard_empty(
    client,
    auth_headers,
):

    response = client.get(
        "/dashboard",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_interviews"] == 0
    assert data["average_score"] == 0
    assert data["highest_score"] == 0
    assert data["total_questions_answered"] == 0
    assert data["recent_interviews"] == []


# =====================================================
# Authentication
# =====================================================

def test_dashboard_requires_auth(
    client,
):

    response = client.get(
        "/dashboard",
    )

    assert response.status_code == 401
