import pytest
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.database.database import Base, get_db
from api.models.user import User
from api.models.role import Role
from api.core.security import get_password_hash
from app.main import app
from httpx import AsyncClient
from typing import Generator

# Configuración de la base de datos de prueba
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    return engine

@pytest.fixture(scope="session")
def test_db(test_engine):
    Base.metadata.create_all(bind=test_engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    
    # Inicializar datos de prueba
    db = TestingSessionLocal()
    try:
        # Crear roles
        roles = ['admin', 'editor', 'viewer']
        for role_name in roles:
            if not db.query(Role).filter(Role.name == role_name).first():
                db.add(Role(name=role_name))
        
        # Crear usuario admin
        if not db.query(User).filter(User.username == "admin").first():
            hashed_password = get_password_hash("adminpassword")
            db.add(User(
                username="admin",
                email="admin@example.com",
                hashed_password=hashed_password,
                role_id=db.query(Role).filter(Role.name == "admin").first().id
            ))
        
        db.commit()
    finally:
        db.close()
    
    yield TestingSessionLocal
    
    # Limpiar la base de datos después de las pruebas
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def db_session(test_db) -> Generator:
    db = test_db()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def override_get_db(db_session):
    def _override_get_db():
        yield db_session
    return _override_get_db

@pytest.fixture
async def client(override_get_db):
    # Sobrescribir la dependencia get_db para usar la base de datos de prueba
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture
async def admin_token(client):
    # Obtener token JWT para el usuario admin
    response = await client.post("/api/v1/auth/login", json={
        "username": "admin",
        "password": "adminpassword"
    })
    return response.json()["access_token"]
