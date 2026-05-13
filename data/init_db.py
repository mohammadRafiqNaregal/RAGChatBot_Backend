from sqlalchemy import select

from data.database import Base, SessionLocal, engine
from dependencies.auth import hash_password
from models.access_control import (
    ROLE_ADMIN,
    ROLE_EMPLOYEE,
    ROLE_FINANCE_USER,
    ROLE_HR_USER,
    ROLE_IT_USER,
)
from models.chat_history_entity import ChatHistoryEntity
from models.user_entity import UserEntity
from models.document_entity import DocumentEntity


def _ensure_demo_user(
    db,
    *,
    username: str,
    email: str,
    role: str,
    password: str,
) -> None:
    existing_user = db.scalar(
        select(UserEntity).where(
            (UserEntity.username == username) | (UserEntity.email == email)
        )
    )
    if existing_user is not None:
        if existing_user.role != role:
            existing_user.role = role
            db.commit()
        return

    db.add(
        UserEntity(
            username=username,
            role=role,
            email=email,
            password=hash_password(password),
        )
    )
    db.commit()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        legacy_users = db.scalars(select(UserEntity).where(UserEntity.role == "User")).all()
        if legacy_users:
            for user in legacy_users:
                user.role = ROLE_EMPLOYEE
            db.commit()

        _ensure_demo_user(
            db,
            username="Rafik",
            email="mdrafik.naregal@gmail.com",
            role=ROLE_ADMIN,
            password="Rafik@123",
        )
        _ensure_demo_user(
            db,
            username="Jane Smith",
            email="jane@example.com",
            role=ROLE_HR_USER,
            password="jane123",
        )
        _ensure_demo_user(
            db,
            username="Bob Johnson",
            email="bob@example.com",
            role=ROLE_EMPLOYEE,
            password="bob123",
        )
        _ensure_demo_user(
            db,
            username="Farah Finance",
            email="finance@example.com",
            role=ROLE_FINANCE_USER,
            password="finance123",
        )
        _ensure_demo_user(
            db,
            username="Ivan IT",
            email="it@example.com",
            role=ROLE_IT_USER,
            password="it123",
        )
