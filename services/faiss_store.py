from pathlib import Path
from typing import Any

from langchain_community.vectorstores import FAISS

from services.embedding_utils import get_langchain_embeddings


class SimpleFaissStore:
    """Thin wrapper around LangChain FAISS for adding text chunks and searching them back."""

    def __init__(self, dimension: int | None = None) -> None:
        self.dimension = dimension
        self.vector_store: FAISS | None = None

    def add_texts(
        self,
        texts: list[str],
        metadatas: list[dict[str, Any]] | None = None,
    ) -> None:
        if not texts:
            return

        metadata_items = metadatas or [{} for _ in texts]
        if len(metadata_items) != len(texts):
            raise ValueError("texts and metadatas must have the same length.")

        embeddings = get_langchain_embeddings()
        if self.vector_store is None:
            self.vector_store = FAISS.from_texts(
                texts=texts,
                embedding=embeddings,
                metadatas=metadata_items,
            )
            return

        self.vector_store.add_texts(texts=texts, metadatas=metadata_items)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        if self.vector_store is None:
            return []

        docs_with_scores = self.vector_store.similarity_search_with_score(query, k=top_k)
        return [
            {
                "score": float(score),
                "text": doc.page_content,
                "metadata": doc.metadata or {},
            }
            for doc, score in docs_with_scores
        ]

    def save(self, folder_path: str = "data/faiss_store") -> None:
        if self.vector_store is None:
            return

        folder = Path(folder_path)
        folder.mkdir(parents=True, exist_ok=True)
        self.vector_store.save_local(folder_path)

    @classmethod
    def load(cls, folder_path: str = "data/faiss_store") -> "SimpleFaissStore":
        folder = Path(folder_path)
        store = cls()

        # LangChain FAISS persists both files; fall back to rebuilding from legacy store.json if needed.
        if (folder / "index.faiss").exists() and (folder / "index.pkl").exists():
            store.vector_store = FAISS.load_local(
                folder_path,
                get_langchain_embeddings(),
                allow_dangerous_deserialization=True,
            )
            return store

        legacy_store_file = folder / "store.json"
        if not legacy_store_file.exists():
            raise FileNotFoundError(f"No FAISS index found in {folder_path}")

        import json

        payload = json.loads(legacy_store_file.read_text(encoding="utf-8"))
        texts = payload.get("texts", [])
        metadatas = payload.get("metadatas", [])
        if not texts:
            raise FileNotFoundError(f"Legacy FAISS store in {folder_path} does not contain any texts")

        store.add_texts(texts=texts, metadatas=metadatas)
        store.save(folder_path)
        return store
