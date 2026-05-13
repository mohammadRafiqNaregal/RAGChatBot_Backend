from pydantic import BaseModel, field_validator
from typing import Optional

from models.access_control import normalize_role


class UserCreate(BaseModel):
    username: str
    email: str
    role: str
    password: str

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str) -> str:
        return normalize_role(value)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None

    @field_validator("role")
    @classmethod
    def validate_role(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        return normalize_role(value)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
