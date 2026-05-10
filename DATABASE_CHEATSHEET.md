# Database Cheatsheet (SQLite vs PostgreSQL, Prisma vs SQLAlchemy)

This project currently uses:

- SQLite (database)
- SQLAlchemy ORM (Python/FastAPI)

## 1. Core Concepts

### What is a database engine?

A database engine is the "brain" that:

- Parses and runs SQL queries
- Reads/writes data safely
- Enforces constraints (unique, FK, etc.)
- Handles transactions

### SQLite in one line

SQLite is an embedded database engine that stores all data in a single file (for example `app.db`).

### PostgreSQL in one line

PostgreSQL is a server-based database engine running as a separate service process.

## 2. SQLite vs PostgreSQL

| Area        | SQLite                          | PostgreSQL                                |
| ----------- | ------------------------------- | ----------------------------------------- |
| Setup       | No server setup                 | Requires DB server install/setup          |
| Runtime     | File-based, embedded            | Separate running service                  |
| Connection  | Direct file access              | Network connection (host/port)            |
| Scale       | Great for MVP/local/small teams | Best for production and heavy concurrency |
| Ops         | Very low maintenance            | More operational overhead                 |
| Typical use | Prototyping, local development  | Production, large/team workloads          |

## 3. Prisma vs SQLAlchemy Mental Mapping

| Goal          | Prisma (Node/Express) | SQLAlchemy (Python/FastAPI)            |
| ------------- | --------------------- | -------------------------------------- |
| Define schema | `schema.prisma`       | Python model classes                   |
| Create row    | `prisma.user.create`  | `db.add(user); db.commit()`            |
| Find by ID    | `findUnique`          | `db.get(UserEntity, id)`               |
| Find many     | `findMany`            | `db.scalars(select(UserEntity)).all()` |
| Update        | `update`              | set fields + `db.commit()`             |
| Delete        | `delete`              | `db.delete(obj); db.commit()`          |
| Count         | `count`               | `select(func.count(...))`              |
| Migrations    | Prisma migrate        | Alembic (recommended)                  |

## 4. SQLAlchemy Basics Used in This Repo

### Session dependency (FastAPI)

```python
# data/database.py
from sqlalchemy.orm import Session

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Model example

```python
class UserEntity(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
```

### Create

```python
user = UserEntity(username="rafik", email="r@example.com", role="Admin", password="...")
db.add(user)
db.commit()
db.refresh(user)
```

### Read

```python
from sqlalchemy import select

user = db.get(UserEntity, 1)
admins = db.scalars(select(UserEntity).where(UserEntity.role == "Admin")).all()
```

### Update

```python
user = db.get(UserEntity, 1)
user.role = "HR User"
db.commit()
db.refresh(user)
```

### Delete

```python
user = db.get(UserEntity, 1)
db.delete(user)
db.commit()
```

## 5. Practical Commands

### Check DB file

```bash
ls -lh app.db
```

### Open SQLite shell

```bash
sqlite3 app.db
```

Inside sqlite shell:

```sql
.tables
.schema users
SELECT * FROM users;
```

### Compile check for Python modules

```bash
/Users/rafihiq.innov.con/Desktop/AI/enterprise-knowledge-assistant/fastapi-clean/.venv/bin/python -m py_compile \
controllers/user_controller.py controllers/auth_controller.py \
routers/user_router.py routers/auth_router.py dependencies/auth.py
```

## 6. Why SQLite for Phase 1 MVP?

- Minimal setup and faster development
- Works great for demos and early iterations
- Easy upgrade path to PostgreSQL later by changing DB URL and running migrations

## 7. Migration Path to PostgreSQL (Later)

1. Install PostgreSQL
2. Create DB/user credentials
3. Update SQLAlchemy `DATABASE_URL` to PostgreSQL URI
4. Use Alembic migrations for schema management
5. Test auth/user/document flows

## 8. Recommended Next Improvements

- Hash passwords (do not store plain text)
- Add Alembic migrations
- Add document and chunk tables with foreign keys
- Add chat history table and citations
- Add role-based document filtering in retrieval pipeline
