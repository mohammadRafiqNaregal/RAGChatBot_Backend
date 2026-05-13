from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from dependencies.auth import hash_password
from models.access_control import normalize_role
from models.user_model import UserCreate, UserUpdate
from models.user_entity import UserEntity


# ── helpers ──────────────────────────────────────────────────────────────

def _to_user_response(user: UserEntity) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }


def _find(db: Session, user_id: int):
    return db.get(UserEntity, user_id)


def _find_by_email(db: Session, email: str):
    statement = select(UserEntity).where(UserEntity.email.ilike(email))
    return db.scalar(statement)


def _find_by_username(db: Session, username: str):
    statement = select(UserEntity).where(UserEntity.username.ilike(username))
    return db.scalar(statement)


# ── controller functions ────────────────────────────────────────────────────

def get_all_users(db: Session):
    users = db.scalars(select(UserEntity)).all()
    return [_to_user_response(user) for user in users]


def get_user_by_id(db: Session, user_id: int):
    user = _find(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    return _to_user_response(user)


def create_user(db: Session, body: UserCreate):
    if _find_by_username(db, body.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with username '{body.username}' already exists",
        )

    if _find_by_email(db, body.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{body.email}' already exists",
        )

    new_user = UserEntity(
        username=body.username,
        email=body.email,
        role=normalize_role(body.role),
        password=hash_password(body.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return _to_user_response(new_user)


def update_user(db: Session, user_id: int, body: UserUpdate):
    user = _find(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    if body.username is not None:
        existing = _find_by_username(db, body.username)
        if existing and existing.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with username '{body.username}' already exists",
            )
        user.username = body.username
    if body.email is not None:
        existing = _find_by_email(db, body.email)
        if existing and existing.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email '{body.email}' already exists",
            )
        user.email = body.email
    if body.role is not None:
        user.role = normalize_role(body.role)
    if body.password is not None:
        user.password = hash_password(body.password)

    db.commit()
    db.refresh(user)
    return _to_user_response(user)


def delete_user(db: Session, user_id: int):
    user = _find(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    db.delete(user)
    db.commit()
