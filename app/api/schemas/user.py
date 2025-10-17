from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)  # Username entre 3 y 50 caracteres
    email: EmailStr  # Validación de formato de correo electrónico
    role_id: int  # ID del rol asociado

class UserCreate(UserBase):
    password: constr(min_length=8)  # Contraseña con mínimo 8 caracteres

class UserUpdate(BaseModel):
    username: Optional[constr(min_length=3, max_length=50)] = None
    email: Optional[EmailStr] = None
    role_id: Optional[int] = None
    password: Optional[constr(min_length=8)] = None

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True  # Permite mapear desde objetos SQLAlchemy