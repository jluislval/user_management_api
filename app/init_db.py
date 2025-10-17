from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.core.config import settings
from api.database.database import Base
from api.models.role import Role
from api.models.user import User
from api.core.security import get_password_hash

# Configuración de la base de datos
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    # Crear las tablas si no existen
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Crear roles predeterminados si no existen
        roles = ['admin', 'editor', 'viewer']
        for role_name in roles:
            existing_role = db.query(Role).filter(Role.name == role_name).first()
            if not existing_role:
                new_role = Role(name=role_name)
                db.add(new_role)
                print(f"Rol '{role_name}' creado.")
            else:
                print(f"Rol '{role_name}' ya existe.")
        
        # Crear usuario admin predeterminado si no existe
        admin_username = "admin"
        admin_email = "admin@example.com"
        admin_password = "adminpassword"  # Cambia esto por una contraseña segura en producción
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        
        if admin_role:
            existing_user = db.query(User).filter(User.username == admin_username).first()
            if not existing_user:
                hashed_password = get_password_hash(admin_password)
                new_user = User(
                    username=admin_username,
                    email=admin_email,
                    hashed_password=hashed_password,
                    role_id=admin_role.id
                )
                db.add(new_user)
                print("Usuario admin creado.")
            else:
                print("Usuario admin ya existe.")
        else:
            print("Error: Rol 'admin' no encontrado.")
        
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error durante la inicialización: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()