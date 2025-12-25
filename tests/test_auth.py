import pytest


@pytest.mark.asyncio
async def test_register_user_success(client):
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
    }
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]
    assert "id" in data
    assert data["role"] == "user"


@pytest.mark.asyncio
async def test_register_user_duplicate_username(client):
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
    }
    await client.post("/api/v1/auth/register", json=payload)

    payload2 = {
        "username": "testuser",
        "email": "another@example.com",
        "password": "anotherpassword",
    }
    response = await client.post("/api/v1/auth/register", json=payload2)
    assert response.status_code == 400
    assert response.json()["detail"] == "Username or email already exists"


@pytest.mark.asyncio
async def test_login_success(client):
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
    }
    await client.post("/api/v1/auth/register", json=payload)

    login_payload = {"username": "testuser", "password": "testpassword"}
    response = await client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
    }
    await client.post("/api/v1/auth/register", json=payload)

    login_payload = {"username": "testuser", "password": "wrongpassword"}
    response = await client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"
