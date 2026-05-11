from threading import Lock

from fastapi import BackgroundTasks

from data.database import SessionLocal
from models.document_entity import DocumentEntity
from services.chunking_utils import chunk_content
from services.embedding_utils import DEFAULT_EMBEDDING_DIMENSION
from services.faiss_store import SimpleFaissStore
from services.file_parser_utils import parse_document_to_text


_INDEX_LOCK = Lock()
_FAISS_FOLDER = "data/faiss_store"


def _load_or_create_store() -> SimpleFaissStore:
    try:
        return SimpleFaissStore.load(_FAISS_FOLDER)
    except FileNotFoundError:
        return SimpleFaissStore(dimension=DEFAULT_EMBEDDING_DIMENSION)


def _index_document(document_id: int) -> None:
    db = SessionLocal()
    try:
        document = db.get(DocumentEntity, document_id)
        if document is None:
            return

        text = parse_document_to_text(file_path=document.file_path)
        chunks = chunk_content(text)
        if not chunks:
            return

        metadatas = [
            {
                "document_id": document.id,
                "title": document.title,
                "filename": document.filename,
                "department": document.department,
                "section": document.section,
                "uploaded_by": document.uploaded_by,
                "allowed_roles": document.allowed_roles or [],
                "chunk_index": chunk_index,
            }
            for chunk_index, _ in enumerate(chunks)
        ]

        with _INDEX_LOCK:
            store = _load_or_create_store()
            store.add_texts(chunks, metadatas)
            store.save(_FAISS_FOLDER)
    finally:
        db.close()


def schedule_document_indexing(background_tasks: BackgroundTasks, document_id: int) -> None:
    """Queue document parsing, chunking, embedding, and FAISS storage after upload response."""
    background_tasks.add_task(_index_document, document_id)
