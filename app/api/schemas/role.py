from pydantic import BaseModel, constr
from typing import Optional

class RoleBase(BaseModel):
    name: constr(min_length=3, max_length=20)  # Nombre del rol (ej. admin, editor, viewer)

class RoleCreate(RoleBase):
    pass  # No se necesitan campos adicionales para crear un rol

class RoleUpdate(BaseModel):
    name: Optional[constr(min_length=3, max_length=20)] = None

class RoleOut(RoleBase):
    id: int

    class Config:
        from_attributes = True  # Permite mapear desde objetos SQLAlchemy