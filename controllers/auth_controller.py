from datetime import timedelta

from fastapi import HTTPException, status

from data.fake_db import users_db
from dependencies.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from models.auth_model import LoginRequest


def _find_by_username(username: str):
    return next((u for u in users_db if u["username"].lower() == username.lower()), None)


def login(payload: LoginRequest):
    print(f"Attempting login for username: {payload.username} {payload.password}")
    user = _find_by_username(payload.username)
    if user is None or user.get("password") != payload.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {
        "access_token": token,
        "role": user["role"],
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }
