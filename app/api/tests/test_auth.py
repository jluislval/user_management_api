import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    response = await client.post("/api/v1/auth/login", json={
        "username": "admin",
        "password": "adminpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    response = await client.post("/api/v1/auth/login", json={
        "username": "admin",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    response = await client.post("/api/v1/auth/login", json={
        "username": "nonexistent",
        "password": "somepassword"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

