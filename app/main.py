from fastapi import FastAPI
from .api.database.database import engine, Base
from .api.v1.endpoints import users, roles, auth


# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Management API")

# Incluir los routers
app.include_router(users.router)
app.include_router(roles.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the User Management API"}