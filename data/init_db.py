from sqlalchemy import func, select

from data.database import Base, SessionLocal, engine
from dependencies.auth import hash_password
from models.access_control import ROLE_ADMIN, ROLE_EMPLOYEE, ROLE_HR_USER
from models.chat_history_entity import ChatHistoryEntity
from models.user_entity import UserEntity
from models.document_entity import DocumentEntity


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        user_count = db.scalar(select(func.count(UserEntity.id))) or 0
        if user_count > 0:
            legacy_users = db.scalars(select(UserEntity).where(UserEntity.role == "User")).all()
            if legacy_users:
                for user in legacy_users:
                    user.role = ROLE_EMPLOYEE
                db.commit()
            return

        seed_users = [
            UserEntity(
                username="Rafik",
                role=ROLE_ADMIN,
                email="mdrafik.naregal@gmail.com",
                password=hash_password("Rafik@123"),
            ),
            UserEntity(
                username="Jane Smith",
                role=ROLE_HR_USER,
                email="jane@example.com",
                password=hash_password("jane123"),
            ),
            UserEntity(
                username="Bob Johnson",
                role=ROLE_EMPLOYEE,
                email="bob@example.com",
                password=hash_password("bob123"),
            ),
        ]

        db.add_all(seed_users)
        db.commit()
