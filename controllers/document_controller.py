import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List

from fastapi import BackgroundTasks, HTTPException, UploadFile, status
from fastapi.concurrency import run_in_threadpool
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.document_model import DocumentCreate, DocumentResponse, DocumentListResponse
from models.access_control import ROLE_ADMIN, normalize_department
from models.document_entity import DocumentEntity
from services.document_indexing_service import schedule_document_indexing


# Upload directory configuration
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def _get_upload_path(filename: str) -> str:
    """Generate safe upload path for file"""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_")
    safe_filename = f"{timestamp}{filename}"
    file_path = UPLOAD_DIR / safe_filename
    return str(file_path)


def _find_document(db: Session, document_id: int) -> DocumentEntity:
    """Find document by ID, raise 404 if not found"""
    doc = db.get(DocumentEntity, document_id)
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document {document_id} not found"
        )
    return doc


def _to_document_response(doc: DocumentEntity) -> dict:
    """Convert DocumentEntity to response dict"""
    return {
        "id": doc.id,
        "filename": doc.filename,
        "title": doc.title,
        "file_path": doc.file_path,
        "department": doc.department,
        "section": doc.section,
        "tags": doc.tags or [],
        "allowed_roles": doc.allowed_roles or [],
        "uploaded_by": doc.uploaded_by,
        "file_type": doc.file_type,
        "created_at": doc.created_at,
        "updated_at": doc.updated_at,
    }


def _to_document_list_response(doc: DocumentEntity) -> dict:
    """Convert DocumentEntity to lightweight list response"""
    return {
        "id": doc.id,
        "filename": doc.filename,
        "title": doc.title,
        "department": doc.department,
        "section": doc.section,
        "tags": doc.tags or [],
        "file_type": doc.file_type,
        "created_at": doc.created_at,
    }


async def upload_document(
    db: Session,
    file: UploadFile,
    metadata: DocumentCreate,
    current_user: dict,
    background_tasks: BackgroundTasks,
) -> dict:
    """
    Upload a document file and store it with metadata
    
    Args:
        db: Database session
        file: Uploaded file
        metadata: Document metadata
        current_user: Current authenticated user
        
    Returns:
        Created document response
    """
    # Only Admin can upload
    if current_user.get("role") != ROLE_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Admin users can upload documents"
        )
    
    # Validate file
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required"
        )
    
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in [".pdf", ".docx", ".txt"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file_ext}. Allowed: .pdf, .docx, .txt"
        )
    
    upload_path = _get_upload_path(file.filename)
    
    try:
        # Write uploaded file to disk
        content = await file.read()
        await run_in_threadpool(Path(upload_path).write_bytes, content)

        # Create document entity
        new_doc = DocumentEntity(
            filename=file.filename,
            title=metadata.title,
            file_path=upload_path,
            department=metadata.department,
            section=metadata.section,
            tags=metadata.tags or [],
            allowed_roles=metadata.allowed_roles,
            uploaded_by=current_user.get("id"),
            file_type=file_ext[1:].upper(),  # PDF, DOCX, TXT
        )
        
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)
        schedule_document_indexing(background_tasks, new_doc.id)
        
        return _to_document_response(new_doc)
    
    except Exception:
        # Clean up on error
        if os.path.exists(upload_path):
            os.remove(upload_path)
        raise


def get_all_documents(
    db: Session,
    current_user: dict,
) -> List[dict]:
    """
    Get all documents accessible by current user
    
    Admins see all documents.
    Other users see only documents with their role in allowed_roles.
    """
    user_role = current_user.get("role")
    
    if user_role == ROLE_ADMIN:
        # Admin sees all documents
        documents = db.scalars(select(DocumentEntity)).all()
    else:
        # Other users see only documents they have access to
    
        # Fetch all documents and filter in Python (SQLite JSON support limitation)
        all_documents = db.scalars(select(DocumentEntity)).all()
        documents = [d for d in all_documents if d.allowed_roles and user_role in d.allowed_roles]
    return [_to_document_list_response(doc) for doc in documents]


def get_document_by_id(
    db: Session,
    document_id: int,
    current_user: dict,
) -> dict:
    """
    Get document by ID with access control
    
    Args:
        db: Database session
        document_id: Document ID
        current_user: Current authenticated user
        
    Returns:
        Document response
    """
    doc = _find_document(db, document_id)
    
    # Check access control
    user_role = current_user.get("role")
    if user_role != ROLE_ADMIN and user_role not in doc.allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to access this document"
        )
    
    return _to_document_response(doc)


def delete_document(
    db: Session,
    document_id: int,
    current_user: dict,
) -> None:
    """
    Delete a document (Admin only)
    
    Args:
        db: Database session
        document_id: Document ID
        current_user: Current authenticated user
    """
    # Only Admin can delete
    if current_user.get("role") != ROLE_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Admin users can delete documents"
        )
    
    doc = _find_document(db, document_id)
    
    # Delete file from disk
    if os.path.exists(doc.file_path):
        try:
            os.remove(doc.file_path)
        except Exception as e:
            print(f"Warning: Could not delete file {doc.file_path}: {str(e)}")
    
    # Delete from database
    db.delete(doc)
    db.commit()


def get_documents_by_department(
    db: Session,
    department: str,
    current_user: dict,
) -> List[dict]:
    """
    Get documents filtered by department
    
    Args:
        db: Database session
        department: Department name (HR, Finance, IT)
        current_user: Current authenticated user
        
    Returns:
        List of documents
    """
    department = normalize_department(department)
    user_role = current_user.get("role")
    
    query = select(DocumentEntity).where(DocumentEntity.department == department)
    
    if user_role != ROLE_ADMIN:
        # Only show docs the user has access to
        docs = db.scalars(query).all()
        docs = [d for d in docs if d.allowed_roles and user_role in d.allowed_roles]
    else:
        docs = db.scalars(query).all()
    
    return [_to_document_list_response(doc) for doc in docs]
