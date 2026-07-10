from app.models.user import User
from app.utils.security import hash_password


def create_test_user(
    db,
    name="Chirag",
    email="chiragthakur2103@gmail.com",
    password="123@chirag",
    role="user",
    is_active=True,
    is_verified=False,
):
    user = db.query(User).filter(
        User.email == email
    ).first()

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

def create_second_user(
    db,
):
    return create_test_user(
        db,
        name="Second User",
        email="second@example.com",
        password="123@chirag",
    )
