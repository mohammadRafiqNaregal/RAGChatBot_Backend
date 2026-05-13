from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, UploadFile, status
from typing import Annotated, List
from sqlalchemy.orm import Session

from data.database import get_db
from dependencies.auth import get_current_user
from models.access_control import ROLE_EMPLOYEE
from models.document_model import DocumentCreate, DocumentResponse, DocumentListResponse
import controllers.document_controller as document_controller

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "/",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a new document"
)
async def upload_document(
    file: Annotated[UploadFile, File(description="Document file (PDF, DOCX, TXT)")],
    title: Annotated[str, Form(description="Document title")],
    department: Annotated[str, Form(description="Department: HR, Finance, IT")],
    section: Annotated[str, Form(description="Document section")] = "",
    tags: Annotated[str, Form(description="Comma-separated tags")] = "",
    allowed_roles: Annotated[str, Form(description="Comma-separated allowed roles")] = "",
    background_tasks: BackgroundTasks = None,
    db: Annotated[Session, Depends(get_db)] = None,
    current_user: Annotated[dict, Depends(get_current_user)] = None,
):
    """
    Upload a new document with metadata.
    
    **Required Permissions:** Admin only
    
    **Supported Formats:** PDF, DOCX, TXT
    
    **Parameters:**
    - `file`: Document file to upload
    - `title`: Document title
    - `department`: HR, Finance, or IT
    - `section`: Document section (optional)
    - `tags`: Comma-separated tags (optional)
    - `allowed_roles`: Comma-separated roles that can access this document
    
    **Example:**
    ```
    POST /api/documents/
    file: <binary-file>
    title: "Company Benefits Guide"
    department: "HR"
    section: "Insurance"
    tags: "benefits,health,policy"
    allowed_roles: "Admin,HR User,Employee"
    ```
    """
    # Parse comma-separated values
    tags_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    allowed_roles_list = [r.strip() for r in allowed_roles.split(",") if r.strip()] if allowed_roles else [ROLE_EMPLOYEE]
    
    metadata = DocumentCreate(
        title=title,
        department=department,
        section=section if section else None,
        tags=tags_list,
        allowed_roles=allowed_roles_list,
    )
    
    return await document_controller.upload_document(
        db,
        file,
        metadata,
        current_user,
        background_tasks,
    )


@router.get(
    "/",
    response_model=List[DocumentListResponse],
    summary="List all accessible documents"
)
def get_all_documents(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """
    Get all documents accessible to the current user.
    
    **Admin:** Sees all documents
    **Other Roles:** See only documents with their role in `allowed_roles`
    
    **Response:** List of document metadata
    """
    return document_controller.get_all_documents(db, current_user)


@router.get(
    "/department/{department}",
    response_model=List[DocumentListResponse],
    summary="Get documents by department"
)
def get_documents_by_department(
    department: str,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """
    Get documents for a specific department (HR, Finance, IT).
    
    **Access Control:** User's role must be in document's `allowed_roles`
    
    **Parameters:**
    - `department`: HR, Finance, or IT
    
    **Response:** List of documents for the specified department
    """
    return document_controller.get_documents_by_department(db, department, current_user)


@router.get(
    "/{document_id}",
    response_model=DocumentResponse,
    summary="Get document by ID"
)
def get_document_by_id(
    document_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """
    Get a specific stored document by ID.
    
    **Access Control:** User must be Admin or have their role in document's `allowed_roles`
    
    **Parameters:**
    - `document_id`: Document ID
    
    **Response:** Full document metadata including the stored file path
    """
    return document_controller.get_document_by_id(db, document_id, current_user)


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a document"
)
def delete_document(
    document_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """
    Delete a document (Admin only).
    
    **Required Permissions:** Admin only
    
    **Parameters:**
    - `document_id`: Document ID to delete
    
    **Response:** 204 No Content
    """
    document_controller.delete_document(db, document_id, current_user)
