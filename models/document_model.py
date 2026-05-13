from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

from models.access_control import normalize_department, normalize_roles, normalize_optional_department


class DocumentCreate(BaseModel):
    """Schema for creating/uploading a document"""
    title: str = Field(..., min_length=1, max_length=255, description="Document title")
    department: str = Field(..., description="Department: HR, Finance, IT")
    section: Optional[str] = Field(None, max_length=255, description="Document section")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for document")
    allowed_roles: List[str] = Field(..., description="Roles that can access this document")

    @field_validator("department")
    @classmethod
    def validate_department(cls, value: str) -> str:
        return normalize_department(value)

    @field_validator("allowed_roles")
    @classmethod
    def validate_allowed_roles(cls, value: List[str]) -> List[str]:
        return normalize_roles(value)


class DocumentMetadata(BaseModel):
    """Schema for document metadata without content"""
    id: int
    filename: str
    title: str
    department: str
    section: Optional[str] = None
    tags: Optional[List[str]] = None
    allowed_roles: List[str]
    uploaded_by: int
    file_type: str
    created_at: datetime
    updated_at: datetime

    @field_validator("department")
    @classmethod
    def validate_department(cls, value: str) -> str:
        return normalize_department(value)

    @field_validator("allowed_roles")
    @classmethod
    def validate_allowed_roles(cls, value: List[str]) -> List[str]:
        return normalize_roles(value)


class DocumentResponse(BaseModel):
    """Full document response for a stored upload"""
    id: int
    filename: str
    title: str
    file_path: str
    department: str
    section: Optional[str] = None
    tags: Optional[List[str]] = None
    allowed_roles: List[str]
    uploaded_by: int
    file_type: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @field_validator("department")
    @classmethod
    def validate_department(cls, value: str) -> str:
        return normalize_department(value)

    @field_validator("allowed_roles")
    @classmethod
    def validate_allowed_roles(cls, value: List[str]) -> List[str]:
        return normalize_roles(value)


class DocumentListResponse(BaseModel):
    """Lightweight document response for list endpoints"""
    id: int
    filename: str
    title: str
    department: str
    section: Optional[str] = None
    tags: Optional[List[str]] = None
    file_type: str
    created_at: datetime

    class Config:
        from_attributes = True

    @field_validator("department")
    @classmethod
    def validate_department(cls, value: str) -> str:
        return normalize_department(value)
