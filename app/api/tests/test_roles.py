import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session
from api.models.role import Role

@pytest.mark.asyncio
async def test_create_role(client: AsyncClient, admin_token: str):
    response = await client.post(
        "/api/v1/roles/",
        json={"name": "newrole"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "newrole"

@pytest.mark.asyncio
async def test_create_role_duplicate(client: AsyncClient, admin_token: str):
    response = await client.post(
        "/api/v1/roles/",
        json={"name": "admin"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Role name already exists"

@pytest.mark.asyncio
async def test_list_roles(client: AsyncClient, admin_token: str):
    response = await client.get(
        "/api/v1/roles/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 3  # admin, editor, viewer

@pytest.mark.asyncio
async def test_get_role(client: AsyncClient, admin_token: str, db_session: Session):
    role = Role(name="testgetrole")
    db_session.add(role)
    db_session.commit()
    
    response = await client.get(
        f"/api/v1/roles/{role.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "testgetrole"

@pytest.mark.asyncio
async def test_update_role(client: AsyncClient, admin_token: str, db_session: Session):
    role = Role(name="testupdaterole")
    db_session.add(role)
    db_session.commit()
    
    response = await client.put(
        f"/api/v1/roles/{role.id}",
        json={"name": "updatedrole"},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "updatedrole"

@pytest.mark.asyncio
async def test_delete_role(client: AsyncClient, admin_token: str, db_session: Session):
    role = Role(name="testdeleterole")
    db_session.add(role)
    db_session.commit()
    
    response = await client.delete(
        f"/api/v1/roles/{role.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 204

@pytest.mark.asyncio
async def test_delete_role_assigned(client: AsyncClient, admin_token: str, db_session: Session):
    # Crear un usuario asignado al rol admin
    response = await client.post(
        "/api/v1/users/",
        json={
            "username": "testuserrole",
            "email": "testuserrole@example.com",
            "password": "testpassword",
            "role_id": 1  # admin role
        },
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
    
    response = await client.delete(
        "/api/v1/roles/1",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Cannot delete role assigned to users"

