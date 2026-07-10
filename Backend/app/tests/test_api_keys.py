from app.utils.jwt import create_access_token

def test_create_api_key(client, test_user):
    access_token = create_access_token(
        {"sub": test_user.email}
    )

    response = client.post(
        "/api-keys/",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "name": "My API Key",
            "permissions": "read",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "My API Key"
    assert data["permissions"] == "read"
    assert "api_key" in data

def test_list_api_keys(client, test_user):
    access_token = create_access_token(
        {"sub": test_user.email}
    )

    client.post(
        "/api-keys/",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "name": "My API Key",
            "permissions": "read",
        },
    )

    response = client.get(
        "/api-keys/",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "My API Key"
    assert data[0]["permissions"] == "read"

def test_revoke_api_key(client, test_user):
    access_token = create_access_token(
        {"sub": test_user.email}
    )

    create_response = client.post(
        "/api-keys/",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "name": "Temporary Key",
            "permissions": "read",
        },
    )

    api_key_id = create_response.json()["id"]

    response = client.delete(
        f"/api-keys/{api_key_id}",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "API Key revoked successfully."

def test_revoke_api_key_not_found(client, test_user):
    access_token = create_access_token(
        {"sub": test_user.email}
    )

    response = client.delete(
        "/api-keys/99999",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
    )

    assert response.status_code == 404


def test_revoke_other_users_api_key(
    client,
    test_user,
    second_user,
):
    first_token = create_access_token(
        {"sub": test_user.email}
    )

    second_token = create_access_token(
        {"sub": second_user.email}
    )

    create_response = client.post(
        "/api-keys/",
        headers={
            "Authorization": f"Bearer {first_token}"
        },
        json={
            "name": "Secret Key",
            "permissions": "read",
        },
    )

    api_key_id = create_response.json()["id"]

    response = client.delete(
        f"/api-keys/{api_key_id}",
        headers={
            "Authorization": f"Bearer {second_token}"
        },
    )

    assert response.status_code == 404

def test_api_key_profile(client, test_user):
    access_token = create_access_token(
        {"sub": test_user.email}
    )

    create_response = client.post(
        "/api-keys/",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        json={
            "name": "Profile Key",
            "permissions": "read",
        },
    )

    api_key = create_response.json()["api_key"]

    response = client.get(
        "/api-keys/profile",
        headers={
            "X-API-Key": api_key
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == test_user.email
    assert data["name"] == test_user.name
    assert data["role"] == test_user.role
