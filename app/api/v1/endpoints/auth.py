from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...database.database import get_db
from ...models.user import User
from ...schemas.auth import Login, Token
from ...core.security import verify_password, create_access_token

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
)

@router.post("/login", response_model=Token)
def login_for_access_token(login: Login, db: Session = Depends(get_db)):
    # Buscar el usuario por username
    user = db.query(User).filter(User.username == login.username).first()
    if not user or not verify_password(login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generar token JWT
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}