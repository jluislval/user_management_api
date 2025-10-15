Vamos a definir la estructura del proyecto para una API REST en Python con las funcionalidades solicitadas. Usaremos **FastAPI** para la API, **SQLAlchemy** con **SQLite** para la base de datos, **Pydantic** para validación, **Passlib** para autenticación, **PyJWT** para JWT, **Swagger** (integrado en FastAPI) para documentación, y **Pytest** para pruebas. A continuación, detallo la estructura del proyecto y las dependencias necesarias.

<xaiArtifact artifact_id="6baa08de-e617-4ef9-a70b-5e2d8e3a3000" artifact_version_id="90f7b900-e8d5-4ca9-9466-46cafaca942c" title="project_structure.md" contentType="text/markdown">

# Estructura del Proyecto

```
user_management_api/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada de la API (FastAPI)
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── users.py    # Endpoints CRUD para usuarios
│   │   │   │   ├── auth.py     # Endpoints para autenticación
│   │   │   │   ├── roles.py    # Endpoints para gestión de roles
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuraciones (variables de entorno, claves JWT, etc.)
│   │   ├── security.py         # Lógica de autenticación (JWT, hashing)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # Modelos SQLAlchemy para usuarios
│   │   ├── role.py             # Modelos SQLAlchemy para roles
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # Esquemas Pydantic para usuarios
│   │   ├── role.py             # Esquemas Pydantic para roles
│   │   ├── auth.py             # Esquemas Pydantic para autenticación
│   ├── database/
│   │   ├── __init__.py
│   │   ├── database.py         # Configuración de la base de datos (SQLAlchemy)
│   ├── dependencies/
│   │   ├── __init__.py
│   │   ├── auth.py             # Dependencias de autenticación (FastAPI)
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_users.py       # Pruebas para endpoints de usuarios
│   │   ├── test_auth.py        # Pruebas para autenticación
│   │   ├── test_roles.py       # Pruebas para endpoints de roles
│
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Documentación del proyecto
├── .env                        # Variables de entorno (no versionado)
├── .gitignore                  # Archivos ignorados por Git
```

# Dependencias Necesarias

Crea un archivo `requirements.txt` con las siguientes dependencias:

```
fastapi==0.115.2
uvicorn==0.32.0
sqlalchemy==2.0.35
pydantic==2.9.2
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
pytest==8.3.3
httpx==0.27.2
python-dotenv==1.0.1
```

# Instrucciones de Instalación

1. **Crea un entorno virtual**:
   ```bash:disable-run
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Crea el archivo `.env`** para variables de entorno (por ejemplo, clave secreta para JWT):
   ```
   SECRET_KEY=tu_clave_secreta_aqui
   DATABASE_URL=sqlite:///./users.db
   ```

4. **Inicializa el proyecto**:
   - Crea las carpetas y archivos según la estructura anterior.
   - Configura Git e incluye un `.gitignore` con:
     ```
     venv/
     __pycache__/
     *.pyc
     .env
     *.db
     ```

# Próximos Pasos
- Configurar la base de datos (`database.py`) y los modelos (`user.py`, `role.py`).
- Definir esquemas Pydantic para validación (`user.py`, `role.py`, `auth.py`).
- Implementar endpoints CRUD y autenticación.
- Configurar Swagger (automático con FastAPI en `/docs`).
- Escribir pruebas con Pytest.

</xaiArtifact>
```