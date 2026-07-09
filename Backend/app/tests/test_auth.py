from app.utils.jwt import (
    create_access_token,
    create_email_verification_token,
    create_password_reset_token,
)
# -------------------------
# LOGIN
# -------------------------

def test_login_without_credentials(client):
    response = client.post("/auth/login")

    assert response.status_code == 422


def test_login_success(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": "chiragthakur2103@gmail.com",
            "password": "123@chirag",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password(client, test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": "chiragthakur2103@gmail.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401


def test_login_user_not_found(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "nouser@example.com",
            "password": "123@chirag",
        },
    )

    assert response.status_code == 401


# -------------------------
# REFRESH TOKEN
# -------------------------

def test_refresh_token_success(client, test_user):
    login_response = client.post(
        "/auth/login",
        data={
            "username": test_user.email,
            "password": "123@chirag",
        },
    )

    assert login_response.status_code == 200

    refresh_token = login_response.json()["refresh_token"]

    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": refresh_token
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_token_invalid(client):
    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": "invalid-token"
        },
    )

    assert response.status_code == 401


def test_refresh_token_missing(client):
    response = client.post(
        "/auth/refresh",
        json={},
    )

    assert response.status_code == 422


# -------------------------
# FORGOT PASSWORD
# -------------------------

def test_forgot_password_existing_email(client, test_user):
    response = client.post(
        "/auth/forgot-password",
        json={
            "email": test_user.email
        },
    )

    assert response.status_code == 200
    assert (
        response.json()["message"]
        == "If the email exists, a password reset link has been sent."
    )


def test_forgot_password_unknown_email(client):
    response = client.post(
        "/auth/forgot-password",
        json={
            "email": "unknown@example.com"
        },
    )

    assert response.status_code == 200
    assert (
        response.json()["message"]
        == "If the email exists, a password reset link has been sent."
    )


# -------------------------
# LOGOUT
# -------------------------

def test_logout_success(client, test_user):
    access_token = create_access_token(
        {"sub": test_user.email}
    )

    response = client.post(
        "/auth/logout",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"


def test_logout_invalid_token(client):
    response = client.post(
        "/auth/logout",
        headers={
            "Authorization": "Bearer invalid-token"
        },
    )

    assert response.status_code == 401


def test_logout_missing_token(client):
    response = client.post("/auth/logout")

    assert response.status_code == 401




# -------------------------
# VERIFY EMAIL
# -------------------------

def test_verify_email_success(client, test_user):
    token = create_email_verification_token(
        {"sub": test_user.email}
    )

    response = client.get(
        "/auth/verify-email",
        params={"token": token},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Email verified successfully"


def test_verify_email_already_verified(client, test_user, db):
    test_user.is_verified = True
    db.commit()

    token = create_email_verification_token(
        {"sub": test_user.email}
    )

    response = client.get(
        "/auth/verify-email",
        params={"token": token},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Email already verified"


def test_verify_email_invalid_token(client):
    response = client.get(
        "/auth/verify-email",
        params={"token": "invalid-token"},
    )

    assert response.status_code == 401


def test_verify_email_wrong_token_type(client, test_user):
    access_token = create_access_token(
        {"sub": test_user.email}
    )

    response = client.get(
        "/auth/verify-email",
        params={"token": access_token},
    )

    assert response.status_code == 401


# -------------------------
# RESET PASSWORD
# -------------------------

def test_reset_password_success(client, test_user):
    token = create_password_reset_token(
        {"sub": test_user.email}
    )

    response = client.post(
        "/auth/reset-password",
        json={
            "token": token,
            "new_password": "NewPassword@123",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Password reset successfully"


def test_reset_password_invalid_token(client):
    response = client.post(
        "/auth/reset-password",
        json={
            "token": "invalid-token",
            "new_password": "NewPassword@123",
        },
    )

    assert response.status_code == 401


def test_reset_password_wrong_token_type(client, test_user):
    access_token = create_access_token(
        {"sub": test_user.email}
    )

    response = client.post(
        "/auth/reset-password",
        json={
            "token": access_token,
            "new_password": "NewPassword@123",
        },
    )

    assert response.status_code == 401


def test_reset_password_user_not_found(client):
    token = create_password_reset_token(
        {"sub": "nouser@example.com"}
    )

    response = client.post(
        "/auth/reset-password",
        json={
            "token": token,
            "new_password": "NewPassword@123",
        },
    )

    assert response.status_code == 404

