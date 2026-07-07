def test_login_without_credentials(client):
    response = client.post("/auth/login")
    
    assert response.status_code == 422


def test_login_success(client):
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
