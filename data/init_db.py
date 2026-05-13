from sqlalchemy import func, select

from data.database import Base, SessionLocal, engine
from dependencies.auth import hash_password
from models.chat_history_entity import ChatHistoryEntity
from models.user_entity import UserEntity
from models.document_entity import DocumentEntity


def init_db() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        user_count = db.scalar(select(func.count(UserEntity.id))) or 0
        if user_count > 0:
            return

        seed_users = [
            UserEntity(
                username="Rafik",
                role="Admin",
                email="mdrafik.naregal@gmail.com",
                password=hash_password("Rafik@123"),
            ),
            UserEntity(
                username="Jane Smith",
                role="User",
                email="jane@example.com",
                password=hash_password("jane123"),
            ),
            UserEntity(
                username="Bob Johnson",
                role="User",
                email="bob@example.com",
                password=hash_password("bob123"),
            ),
        ]

        db.add_all(seed_users)
        db.commit()
