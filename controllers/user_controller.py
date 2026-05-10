from fastapi import HTTPException, status
from data.fake_db import users_db, next_id
from models.user_model import UserCreate, UserUpdate


# ── helpers ────────────────────────────────────────────────────────────────

def _find(user_id: int):
    return next((u for u in users_db if u["id"] == user_id), None)

def _find_index(user_id: int):
    return next((i for i, u in enumerate(users_db) if u["id"] == user_id), None)


def _find_by_email(email: str):
    return next((u for u in users_db if u["email"].lower() == email.lower()), None)


# ── controller functions ────────────────────────────────────────────────────

def get_all_users():
    return users_db


def get_user_by_id(user_id: int):
    user = _find(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    return user


def create_user(body: UserCreate):
    if _find_by_email(body.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{body.email}' already exists",
        )

    new_user = {
        "id":    next_id[0],
        "name":  body.name,
        "email": body.email,
        "age":   body.age,
        "password": body.password,
    }
    users_db.append(new_user)
    next_id[0] += 1
    return new_user


def update_user(user_id: int, body: UserUpdate):
    index = _find_index(user_id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    # Only update fields that were actually sent
    user = users_db[index]
    if body.name  is not None: user["name"]  = body.name
    if body.email is not None:
        existing = _find_by_email(body.email)
        if existing and existing["id"] != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User with email '{body.email}' already exists",
            )
        user["email"] = body.email
    if body.age   is not None: user["age"]   = body.age
    if body.password is not None: user["password"] = body.password
    return user


def delete_user(user_id: int):
    index = _find_index(user_id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    users_db.pop(index)
