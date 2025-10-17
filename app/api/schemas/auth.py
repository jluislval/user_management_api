from pydantic import BaseModel, constr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class Login(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=8)