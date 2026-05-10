from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    # email: EmailStr
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    role: str
    token_type: str = "bearer"
    expires_in: int


class AuthUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
