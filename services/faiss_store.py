import json
from pathlib import Path
from typing import Any

import faiss
import numpy as np

from services.embedding_utils import generate_embedding, generate_embeddings


class SimpleFaissStore:
    """Minimal FAISS wrapper for adding text chunks and searching them back."""

    def __init__(self, dimension: int) -> None:
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.texts: list[str] = []
        self.metadatas: list[dict[str, Any]] = []

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

        vectors = np.array(generate_embeddings(texts), dtype="float32")
        faiss.normalize_L2(vectors)

        self.index.add(vectors)
        self.texts.extend(texts)
        self.metadatas.extend(metadata_items)

    def search(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        if not self.texts:
            return []

        query_vector = np.array([generate_embedding(query)], dtype="float32")
        faiss.normalize_L2(query_vector)

        scores, indices = self.index.search(query_vector, top_k)
        results: list[dict[str, Any]] = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            results.append(
                {
                    "score": float(score),
                    "text": self.texts[index],
                    "metadata": self.metadatas[index],
                }
            )

        return results

    def save(self, folder_path: str = "data/faiss_store") -> None:
        folder = Path(folder_path)
        folder.mkdir(parents=True, exist_ok=True)

        faiss.write_index(self.index, str(folder / "index.faiss"))
        payload = {
            "dimension": self.dimension,
            "texts": self.texts,
            "metadatas": self.metadatas,
        }
        (folder / "store.json").write_text(
            json.dumps(payload, ensure_ascii=True, indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, folder_path: str = "data/faiss_store") -> "SimpleFaissStore":
        folder = Path(folder_path)
        payload = json.loads((folder / "store.json").read_text(encoding="utf-8"))

        store = cls(dimension=int(payload["dimension"]))
        store.index = faiss.read_index(str(folder / "index.faiss"))
        store.texts = payload.get("texts", [])
        store.metadatas = payload.get("metadatas", [])
        return store
