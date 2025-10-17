import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from api.models.user import User

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient, admin_token: str, db_session: Session):
    response = await client.post(
        "/api/v1/users/",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword",
            "role_id": 2  # Editor role
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "testuser@example.com"
    assert response.json()["role_id"] == 2

@pytest.mark.asyncio
async def test_create_user_duplicate_username(client: AsyncClient, admin_token: str):
    response = await client.post(
        "/api/v1/users/",
        json={
            "username": "admin",
            "email": "newemail@example.com",
            "password": "testpassword",
            "role_id": 2
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

@pytest.mark.asyncio
async def test_list_users(client: AsyncClient, admin_token: str):
    response = await client.get(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1  # Al menos el admin existe

@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, admin_token: str, db_session: Session):
    # Crear un usuario para probar
    user = User(
        username="testgetuser",
        email="testgetuser@example.com",
        hashed_password="hashedpassword",
        role_id=2
    )
    db_session.add(user)
    db_session.commit()
    
    response = await client.get(
        f"/api/v1/users/{user.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testgetuser"

@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, admin_token: str, db_session: Session):
    # Crear un usuario para probar
    user = User(
        username="testupdateuser",
        email="testupdateuser@example.com",
        hashed_password="hashedpassword",
        role_id=2
    )
    db_session.add(user)
    db_session.commit()
    
    response = await client.put(
        f"/api/v1/users/{user.id}",
        json={"email": "updated@example.com", "role_id": 3},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "updated@example.com"
    assert response.json()["role_id"] == 3

@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, admin_token: str, db_session: Session):
    # Crear un usuario para probar
    user = User(
        username="testdeleteuser",
        email="testdeleteuser@example.com",
        hashed_password="hashedpassword",
        role_id=2
    )
    db_session.add(user)
    db_session.commit()
    
    response = await client.delete(
        f"/api/v1/users/{user.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    response = await client.get("/api/v1/users/")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

