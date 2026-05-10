from datetime import timedelta

from fastapi import HTTPException, status

from data.fake_db import users_db
from dependencies.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from models.auth_model import LoginRequest


def _find_by_email(email: str):
    return next((u for u in users_db if u["email"].lower() == email.lower()), None)


def login(payload: LoginRequest):
    print(f"Attempting login for email: {payload.email} {payload.password}")
    user = _find_by_email(payload.email)
    if user is None or user.get("password") != payload.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }
