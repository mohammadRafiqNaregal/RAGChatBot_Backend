from datetime import datetime

from sqlalchemy import DateTime, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from data.database import Base


class DocumentEntity(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    department: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # HR, Finance, IT
    section: Mapped[str] = mapped_column(String(255), nullable=True)
    tags: Mapped[list] = mapped_column(JSON, nullable=True, default=list)  # e.g., ["policy", "benefits"]
    allowed_roles: Mapped[list] = mapped_column(JSON, nullable=False, default=list)  # e.g., ["Admin", "HR User", "Employee"]
    uploaded_by: Mapped[int] = mapped_column(Integer, nullable=False, index=True)  # User ID
    file_type: Mapped[str] = mapped_column(String(10), nullable=False)  # PDF, DOCX, TXT
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
