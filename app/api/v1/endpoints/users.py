from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...database.database import get_db
from ...models.user import User
from ...models.role import Role
from ...schemas.user import UserCreate, UserUpdate, UserOut
from ...schemas.auth import TokenData
from ...core.security import get_password_hash, verify_password
from ...dependencies.auth import get_current_user
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)

# Dependencia para OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el username o email ya existen
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Verificar si el role_id existe
    if not db.query(Role).filter(Role.id == user.role_id).first():
        raise HTTPException(status_code=400, detail="Role does not exist")
    
    # Crear el usuario
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role_id=user.role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    # Solo admin puede listar todos los usuarios
    user = db.query(User).filter(User.username == current_user.username).first()
    if not user or db.query(Role).filter(Role.id == user.role_id, Role.name == "admin").first() is None:
        raise HTTPException(status_code=403, detail="Not authorized to list users")
    
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    # El usuario puede ver su propio perfil o un admin puede ver cualquier perfil
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_user_db = db.query(User).filter(User.username == current_user.username).first()
    if current_user_db.id != user_id and db.query(Role).filter(Role.id == current_user_db.role_id, Role.name == "admin").first() is None:
        raise HTTPException(status_code=403, detail="Not authorized to view this user")
    
    return user

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    # El usuario puede actualizar su propio perfil o un admin puede actualizar cualquier perfil
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_user_db = db.query(User).filter(User.username == current_user.username).first()
    if current_user_db.id != user_id and db.query(Role).filter(Role.id == current_user_db.role_id, Role.name == "admin").first() is None:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")
    
    # Actualizar solo los campos proporcionados
    if user_update.username:
        if db.query(User).filter(User.username == user_update.username, User.id != user_id).first():
            raise HTTPException(status_code=400, detail="Username already registered")
        db_user.username = user_update.username
    if user_update.email:
        if db.query(User).filter(User.email == user_update.email, User.id != user_id).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        db_user.email = user_update.email
    if user_update.password:
        db_user.hashed_password = get_password_hash(user_update.password)
    if user_update.role_id:
        if not db.query(Role).filter(Role.id == user_update.role_id).first():
            raise HTTPException(status_code=400, detail="Role does not exist")
        db_user.role_id = user_update.role_id
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    # Solo admin puede eliminar usuarios
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_user_db = db.query(User).filter(User.username == current_user.username).first()
    if db.query(Role).filter(Role.id == current_user_db.role_id, Role.name == "admin").first() is None:
        raise HTTPException(status_code=403, detail="Not authorized to delete users")
    
    db.delete(user)
    db.commit()
    return None