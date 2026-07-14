from app.models.user import User
from app.models.resume import Resume
from app.models.interview import Interview
from app.models.interview_question import InterviewQuestion
from app.models.interview_answer import InterviewAnswer
from app.models.interview_report import InterviewReport

from app.utils.security import hash_password


# ----------------------------------------------------
# Users
# ----------------------------------------------------

def create_test_user(
    db,
    name="Chirag",
    email="chiragthakur2103@gmail.com",
    password="123@chirag",
    role="user",
    is_active=True,
    is_verified=False,
):
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user:
        return user

    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password),
        role=role,
        is_active=is_active,
        is_verified=is_verified,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def create_second_user(db):
    return create_test_user(
        db,
        name="Second User",
        email="second@example.com",
        password="123@chirag",
    )


# ----------------------------------------------------
# Resume
# ----------------------------------------------------

def create_test_resume(
    db,
    user,
):
    resume = Resume(
        filename="resume.pdf",
        file_path="/tmp/resume.pdf",
        file_size=1024,
        content_type="application/pdf",
        user_id=user.id,
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


# ----------------------------------------------------
# Interview
# ----------------------------------------------------

def create_test_interview(
    db,
    user,
    resume,
    role="Backend Developer",
    difficulty="hard",
):
    interview = Interview(
        user_id=user.id,
        resume_id=resume.id,
        title=f"{role} Interview",
        role=role,
        difficulty=difficulty,
    )

    db.add(interview)
    db.commit()
    db.refresh(interview)

    return interview


# ----------------------------------------------------
# Question
# ----------------------------------------------------

def create_test_question(
    db,
    interview,
    question="Explain dependency injection.",
    category="Backend",
    difficulty="hard",
):
    obj = InterviewQuestion(
        interview_id=interview.id,
        question=question,
        category=category,
        difficulty=difficulty,
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


# ----------------------------------------------------
# Answer
# ----------------------------------------------------

def create_test_answer(
    db,
    question,
    answer="Sample answer",
    score=80,
    feedback="Good explanation.",
):
    obj = InterviewAnswer(
        question_id=question.id,
        answer=answer,
        score=score,
        feedback=feedback,
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


# ----------------------------------------------------
# Report
# ----------------------------------------------------

def create_test_report(
    db,
    interview,
    score=80,
):
    report = InterviewReport(
        interview_id=interview.id,
        overall_score=score,
        technical_level="Intermediate",
        communication="Good",
        strengths=[
            "Problem Solving",
            "Python",
        ],
        weaknesses=[
            "System Design",
        ],
        recommendation="Practice more system design.",
        summary="Overall good interview performance.",
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report
