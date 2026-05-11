from io import BytesIO
from pathlib import Path

from PyPDF2 import PdfReader
from docx import Document


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def _normalize_text(text: str) -> str:
    return " ".join(text.split())


def _extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    content = "\n".join((page.extract_text() or "") for page in reader.pages)
    return _normalize_text(content)


def _extract_text_from_docx_bytes(file_bytes: bytes) -> str:
    document = Document(BytesIO(file_bytes))
    content = "\n".join(paragraph.text for paragraph in document.paragraphs)
    return _normalize_text(content)


def _extract_text_from_txt_bytes(file_bytes: bytes) -> str:
    content = file_bytes.decode("utf-8", errors="ignore")
    return _normalize_text(content)


def parse_bytes_to_text(file_bytes: bytes, filename: str) -> str:
    """Parse file bytes (from frontend uploads) and return extracted plain text."""
    extension = Path(filename).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported extension '{extension}'. Supported: {sorted(SUPPORTED_EXTENSIONS)}")

    if extension == ".pdf":
        return _extract_text_from_pdf_bytes(file_bytes)
    if extension == ".docx":
        return _extract_text_from_docx_bytes(file_bytes)
    return _extract_text_from_txt_bytes(file_bytes)


def parse_file_path_to_text(file_path: str) -> str:
    """Parse a local file path and return extracted plain text."""
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        raise ValueError(f"File not found: {file_path}")

    return parse_bytes_to_text(path.read_bytes(), path.name)


def parse_document_to_text(
    *,
    file_path: str | None = None,
    file_bytes: bytes | None = None,
    filename: str | None = None,
) -> str:
    """
    Parse a document from either file path or in-memory bytes and return plain text.

    Exactly one input mode is allowed:
    1) file_path='...'
    2) file_bytes=b'...' and filename='document.pdf'
    """
    has_path = file_path is not None
    has_bytes = file_bytes is not None

    if has_path == has_bytes:
        raise ValueError("Provide exactly one source: file_path OR file_bytes (+ filename).")

    if has_path:
        return parse_file_path_to_text(file_path=file_path)

    if not filename:
        raise ValueError("filename is required when using file_bytes.")

    return parse_bytes_to_text(file_bytes=file_bytes, filename=filename)
