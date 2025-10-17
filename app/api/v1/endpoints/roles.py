from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...database.database import get_db
from ...models.role import Role
from ...models.user import User
from ...schemas.role import RoleCreate, RoleUpdate, RoleOut
from ...schemas.auth import TokenData
from ...dependencies.auth import get_current_user

""" INSERT INTO roles (name) VALUES ('admin');
INSERT INTO roles (name) VALUES ('editor');
INSERT INTO roles (name) VALUES ('viewer'); """


router = APIRouter(
    prefix="/api/v1/roles",
    tags=["roles"],
)

@router.post("/", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
def create_role(role: RoleCreate, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    # Solo admin puede crear roles
    user = db.query(User).filter(User.username == current_user.username).first()
    if not user or db.query(Role).filter(Role.id == user.role_id, Role.name == "admin").first() is None:
        raise HTTPException(status_code=403, detail="Not authorized to create roles")
    
    # Verificar si el nombre del rol ya existe
    if db.query(Role).filter(Role.name == role.name).first():
        raise HTTPException(status_code=400, detail="Role name already exists")
    
    # Crear el rol
    db_role = Role(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.get("/", response_model=List[RoleOut])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    # Solo admin puede listar todos los roles
    user = db.query(User).filter(User.username == current_user.username).first()
    if not user or db.query(Role).filter(Role.id == user.role_id, Role.name == "admin").first() is None:
        raise HTTPException(status_code=403, detail="Not authorized to list roles")
    
    roles = db.query(Role).offset(skip).limit(limit).all()
    return roles

@router.get("/{role_id}", response_model=RoleOut)
def read_role(role_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    # Solo admin puede ver detalles de un rol
    user = db.query(User).filter(User.username == current_user.username).first()
    if not user or db.query(Role).filter(Role.id == user.role_id, Role.name == "admin").first() is None:
        raise HTTPException(status_code=403, detail="Not authorized to view this role")
    
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    return role

@router.put("/{role_id}", response_model=RoleOut)
def update_role(role_id: int, role_update: RoleUpdate, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    # Solo admin puede actualizar roles
    user = db.query(User).filter(User.username == current_user.username).first()
    if not user or db.query(Role).filter(Role.id == user.role_id, Role.name == "admin").first() is None:
        raise HTTPException(status_code=403, detail="Not authorized to update roles")
    
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # Actualizar solo los campos proporcionados
    if role_update.name:
        if db.query(Role).filter(Role.name == role_update.name, Role.id != role_id).first():
            raise HTTPException(status_code=400, detail="Role name already exists")
        db_role.name = role_update.name
    
    db.commit()
    db.refresh(db_role)
    return db_role

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    # Solo admin puede eliminar roles
    user = db.query(User).filter(User.username == current_user.username).first()
    if not user or db.query(Role).filter(Role.id == user.role_id, Role.name == "admin").first() is None:
        raise HTTPException(status_code=403, detail="Not authorized to delete roles")
    
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # Verificar si el rol está asignado a algún usuario
    if db.query(User).filter(User.role_id == role_id).first():
        raise HTTPException(status_code=400, detail="Cannot delete role assigned to users")
    
    db.delete(role)
    db.commit()
    return None