# Document Upload API - Testing Guide

## Overview

The document upload APIs allow Admin users to upload PDF, DOCX, and TXT files with metadata. The system stores the original file and its metadata in the database and manages access control based on user roles.

## New Endpoints

### 1. Upload Document (Admin Only)

**Endpoint:** `POST /api/documents/`
**Authentication:** Required (Bearer token)
**Role Required:** Admin

**Request Format:** Form-data (multipart/form-data)

**Parameters:**

- `file` (required): Document file (.pdf, .docx, or .txt)
- `title` (required): Document title
- `department` (required): HR, Finance, or IT
- `section` (optional): Document section
- `tags` (optional): Comma-separated tags (e.g., "benefits,policy,2024")
- `allowed_roles` (optional): Comma-separated roles that can access this document

**Response (201 Created):**

```json
{
  "id": 1,
  "filename": "company_handbook.pdf",
  "title": "Company Handbook 2024",
  "file_path": "/path/to/uploads/20250510_143022_company_handbook.pdf",
  "department": "HR",
  "section": "Policies",
  "tags": ["policy", "handbook", "2024"],
  "allowed_roles": ["Admin", "HR User", "Employee"],
  "uploaded_by": 1,
  "file_type": "PDF",
  "created_at": "2025-05-10T14:30:22.123456",
  "updated_at": "2025-05-10T14:30:22.123456"
}
```

**cURL Example:**

```bash
curl -X POST http://localhost:8000/api/documents/ \
  -H "Authorization: Bearer <your-jwt-token>" \
  -F "file=@company_handbook.pdf" \
  -F "title=Company Handbook 2024" \
  -F "department=HR" \
  -F "section=Policies" \
  -F "tags=policy,handbook,2024" \
  -F "allowed_roles=Admin,HR User,Employee"
```

---

### 2. List All Documents (Accessible by User)

**Endpoint:** `GET /api/documents/`
**Authentication:** Required (Bearer token)

**Response (200 OK):**
Returns list of documents accessible to the user. Admins see all documents; other roles see only documents with their role in `allowed_roles`.

```json
[
  {
    "id": 1,
    "filename": "company_handbook.pdf",
    "title": "Company Handbook 2024",
    "department": "HR",
    "section": "Policies",
    "tags": ["policy", "handbook", "2024"],
    "file_type": "PDF",
    "created_at": "2025-05-10T14:30:22.123456"
  },
  {
    "id": 2,
    "filename": "budget_2024.docx",
    "title": "Annual Budget 2024",
    "department": "Finance",
    "section": "Planning",
    "tags": ["budget", "financial"],
    "file_type": "DOCX",
    "created_at": "2025-05-10T14:35:12.654321"
  }
]
```

**cURL Example:**

```bash
curl -X GET http://localhost:8000/api/documents/ \
  -H "Authorization: Bearer <your-jwt-token>"
```

---

### 3. Get Documents by Department

**Endpoint:** `GET /api/documents/department/{department}`
**Authentication:** Required (Bearer token)

**Parameters:**

- `department` (path): HR, Finance, or IT

**Response (200 OK):**

```json
[
  {
    "id": 1,
    "filename": "company_handbook.pdf",
    "title": "Company Handbook 2024",
    "department": "HR",
    "section": "Policies",
    "tags": ["policy", "handbook", "2024"],
    "file_type": "PDF",
    "created_at": "2025-05-10T14:30:22.123456"
  }
]
```

**cURL Example:**

```bash
curl -X GET http://localhost:8000/api/documents/department/HR \
  -H "Authorization: Bearer <your-jwt-token>"
```

---

### 4. Get Document by ID

**Endpoint:** `GET /api/documents/{document_id}`
**Authentication:** Required (Bearer token)

**Parameters:**

- `document_id` (path): Document ID

**Response (200 OK):**

```json
{
  "id": 1,
  "filename": "company_handbook.pdf",
  "title": "Company Handbook 2024",
  "file_path": "/path/to/uploads/20250510_143022_company_handbook.pdf",
  "department": "HR",
  "section": "Policies",
  "tags": ["policy", "handbook", "2024"],
  "allowed_roles": ["Admin", "HR User", "Employee"],
  "uploaded_by": 1,
  "file_type": "PDF",
  "created_at": "2025-05-10T14:30:22.123456",
  "updated_at": "2025-05-10T14:30:22.123456"
}
```

**cURL Example:**

```bash
curl -X GET http://localhost:8000/api/documents/1 \
  -H "Authorization: Bearer <your-jwt-token>"
```

---

### 5. Delete Document (Admin Only)

**Endpoint:** `DELETE /api/documents/{document_id}`
**Authentication:** Required (Bearer token)
**Role Required:** Admin

**Parameters:**

- `document_id` (path): Document ID

**Response (204 No Content):**

```
[No response body]
```

**cURL Example:**

```bash
curl -X DELETE http://localhost:8000/api/documents/1 \
  -H "Authorization: Bearer <your-jwt-token>"
```

---

## Test Flow

### 1. Get Auth Token

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"Rafik","password":"Rafik@123"}'

# Response:
# {"access_token":"eyJ...", "token_type":"bearer", "expires_in":3600, "role":"Admin"}
```

### 2. Upload a Document (as Admin)

```bash
# Create a test file first
echo "This is a test document for HR department." > /tmp/test_hr_policy.txt

# Upload it
curl -X POST http://localhost:8000/api/documents/ \
  -H "Authorization: Bearer eyJ..." \
  -F "file=@/tmp/test_hr_policy.txt" \
  -F "title=Test HR Policy" \
  -F "department=HR" \
  -F "section=Policies" \
  -F "tags=test,policy,hr" \
  -F "allowed_roles=Admin,HR User,Employee"
```

### 3. List Documents

```bash
curl -X GET http://localhost:8000/api/documents/ \
  -H "Authorization: Bearer eyJ..."
```

### 4. Get Document by ID

```bash
curl -X GET http://localhost:8000/api/documents/1 \
  -H "Authorization: Bearer eyJ..."
```

### 5. Delete Document (as Admin)

```bash
curl -X DELETE http://localhost:8000/api/documents/1 \
  -H "Authorization: Bearer eyJ..."
```

---

## Error Handling

### Invalid File Format

```
POST /api/documents/ with .exe file

Response (400 Bad Request):
{
  "detail": "Unsupported file type: .exe. Allowed: .pdf, .docx, .txt"
}
```

### Permission Denied (Non-Admin Upload)

```
POST /api/documents/ with HR User role

Response (403 Forbidden):
{
  "detail": "Only Admin users can upload documents"
}
```

### Document Not Found

```
GET /api/documents/999

Response (404 Not Found):
{
  "detail": "Document 999 not found"
}
```

### Access Denied (Unauthorized Role)

```
GET /api/documents/1 (document only allows Finance User)
with HR User role

Response (403 Forbidden):
{
  "detail": "You are not authorized to access this document"
}
```

## File Types Supported

### PDF (.pdf)

- Accepted for upload and stored as-is

### DOCX (.docx)

- Accepted for upload and stored as-is

### TXT (.txt)

- Accepted for upload and stored as-is

---

## Access Control Rules

### Admin Role

- Can upload documents
- Can delete documents
- Can see all documents
- Can access any document

### HR User / Finance User / IT User

- Cannot upload or delete
- Can only see documents with their role in `allowed_roles`
- Department filtering based on document metadata

### Employee

- Cannot upload or delete
- Can only see documents with "Employee" in `allowed_roles`
- Use for general company policies and information

---

## Metadata Structure

**allowed_roles:** Array of roles that can query and access this document

```json
"allowed_roles": ["Admin", "HR User", "Employee"]
```

**tags:** Searchable tags for categorization

```json
"tags": ["policy", "benefits", "2024", "health-insurance"]
```

**file_type:** Normalized file type

- "PDF"
- "DOCX"
- "TXT"

## Database Schema

```sql
CREATE TABLE documents (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  filename VARCHAR(255) NOT NULL,
  title VARCHAR(255) NOT NULL,
  file_path VARCHAR(500) NOT NULL,
  department VARCHAR(50) NOT NULL,
  section VARCHAR(255),
  tags JSON,
  allowed_roles JSON NOT NULL,
  uploaded_by INTEGER NOT NULL,
  file_type VARCHAR(10) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for faster queries
CREATE INDEX idx_documents_department ON documents(department);
CREATE INDEX idx_documents_uploaded_by ON documents(uploaded_by);
CREATE INDEX idx_documents_created_at ON documents(created_at);
```

---

## Next Steps

1. **Phase 2:** Implement embeddings and vector search
2. **Phase 3:** Build chat endpoint that uses documents
3. **Phase 3:** Create frontend UI for upload and document browsing
4. **Future:** Add OCR support for scanned PDFs
