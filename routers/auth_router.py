from fastapi import APIRouter, Depends
from typing import Annotated
from sqlalchemy.orm import Session

import controllers.auth_controller as auth_controller
from data.database import get_db
from dependencies.auth import get_current_user
from models.auth_model import AuthUserResponse, LoginRequest, TokenResponse

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Annotated[Session, Depends(get_db)]):
    print(f"Received login request for username: {payload.username} {payload.password}")
    return auth_controller.login(db, payload)


@router.get("/me", response_model=AuthUserResponse)
def me(current_user: Annotated[dict, Depends(get_current_user)]):
    print(f"Retrieved current user: {current_user}")
    return current_user
