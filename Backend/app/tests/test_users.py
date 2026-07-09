from app.utils.jwt import create_access_token

def test_register_user(client):
    response = client.post(
        "/users/register",
        json={
            "name": "John",
            "email": "john@example.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "John"
    assert data["email"] == "john@example.com"


def test_register_duplicate_email(client, test_user):
    response = client.post(
        "/users/register",
        json={
            "name": "Another",
            "email": test_user.email,
            "password": "Password@123",
        },
    )

    assert response.status_code == 400

def test_get_current_user(client, test_user):
    access_token = create_access_token(
        {"sub": test_user.email}
    )

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == test_user.email
    assert data["name"] == test_user.name
    assert data["role"] == test_user.role

def test_get_current_user_missing_token(client):
    response = client.get("/users/me")

    assert response.status_code == 401

def test_get_current_user_invalid_token(client):
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer invalid-token"
        },
    )

    assert response.status_code == 401



def test_admin_get_all_users(client, admin_user):
    access_token = create_access_token(
        {"sub": admin_user.email}
    )

    response = client.get(
        "/users/",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_admin_activate_user(client, admin_user, test_user):
    access_token = create_access_token(
        {"sub": admin_user.email}
    )

    response = client.patch(
        f"/users/{test_user.id}/activate",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert response.status_code == 200
    assert (
        response.json()["message"]
        == "User activated successfully"
    )

def test_admin_deactivate_user(client, admin_user, test_user):
    access_token = create_access_token(
        {"sub": admin_user.email}
    )

    response = client.patch(
        f"/users/{test_user.id}/deactivate",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert response.status_code == 200
    assert (
        response.json()["message"]
        == "User deactivated successfully"
    )

def test_admin_delete_user(client, admin_user):
    response = client.post(
        "/users/register",
        json={
            "name": "Delete Me",
            "email": "deleteme@example.com",
            "password": "Password@123",
        },
    )

    user_id = response.json()["id"]

    access_token = create_access_token(
        {"sub": admin_user.email}
    )

    response = client.delete(
        f"/users/{user_id}",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert response.status_code == 200
    assert (
        response.json()["message"]
        == "User deleted successfully"
    )

def test_non_admin_cannot_get_all_users(client, test_user):
    access_token = create_access_token(
        {"sub": test_user.email}
    )

    response = client.get(
        "/users/",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert response.status_code == 403


def test_non_admin_cannot_activate_user(client, test_user):
    access_token = create_access_token(
        {"sub": test_user.email}
    )

    response = client.patch(
        f"/users/{test_user.id}/activate",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert response.status_code == 403


def test_non_admin_cannot_deactivate_user(client, test_user):
    access_token = create_access_token(
        {"sub": test_user.email}
    )

    response = client.patch(
        f"/users/{test_user.id}/deactivate",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert response.status_code == 403


def test_non_admin_cannot_delete_user(client, test_user):
    access_token = create_access_token(
        {"sub": test_user.email}
    )

    response = client.delete(
        f"/users/{test_user.id}",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert response.status_code == 403
