from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session

from data.database import get_db
from models.user_entity import UserEntity

SECRET_KEY = "super-secret-jwt-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

bearer_scheme = HTTPBearer(auto_error=False)
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def hash_password(password: str) -> str:
    return password_context.hash(password)


def is_password_hashed(password: str) -> bool:
    return password.startswith(("$2a$", "$2b$", "$2y$"))


def verify_password(plain_password: str, stored_password: str) -> bool:
    if is_password_hashed(stored_password):
        return password_context.verify(plain_password, stored_password)
    return plain_password == stored_password


def _serialize_user(user: UserEntity) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }


def _find_by_email(db: Session, email: str):
    statement = select(UserEntity).where(UserEntity.email.ilike(email))
    return db.scalar(statement)


def _find_by_username(db: Session, username: str):
    statement = select(UserEntity).where(UserEntity.username.ilike(username))
    return db.scalar(statement)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )

    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc

    user_subject = payload.get("sub")
    if not user_subject:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload missing subject",
        )

    # Current tokens use username in `sub`; fallback supports previously issued email-based tokens.
    user = _find_by_username(db, user_subject) or _find_by_email(db, user_subject)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return _serialize_user(user)


def require_role(*allowed_roles: str):
    """Dependency factory — usage: Depends(require_role('admin', 'editor'))"""
    def check_role(current_user: dict = Depends(get_current_user)) -> dict:
        user_role = current_user.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: requires one of {list(allowed_roles)}, got '{user_role}'",
            )
        return current_user
    return check_role