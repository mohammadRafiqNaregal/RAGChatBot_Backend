from sqlalchemy import func, select

from data.database import Base, SessionLocal, engine
from models.user_entity import UserEntity


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
                password="Rafik@123",
            ),
            UserEntity(
                username="Jane Smith",
                role="User",
                email="jane@example.com",
                password="jane123",
            ),
            UserEntity(
                username="Bob Johnson",
                role="User",
                email="bob@example.com",
                password="bob123",
            ),
        ]

        db.add_all(seed_users)
        db.commit()
