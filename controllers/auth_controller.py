from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from dependencies.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    hash_password,
    is_password_hashed,
    verify_password,
)
from models.auth_model import LoginRequest
from models.user_entity import UserEntity


def _find_by_username(db: Session, username: str):
    statement = select(UserEntity).where(UserEntity.username.ilike(username))
    return db.scalar(statement)


def login(db: Session, payload: LoginRequest):
    print(f"Attempting login for username: {payload.username} {payload.password}")
    user = _find_by_username(db, payload.username)
    if user is None or not verify_password(payload.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not is_password_hashed(user.password):
        user.password = hash_password(payload.password)
        db.commit()

    token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {
        "access_token": token,
        "role": user.role,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }
