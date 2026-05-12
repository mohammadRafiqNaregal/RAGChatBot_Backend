from sentence_transformers import SentenceTransformer

'''NOTES'''
'''for my reference this is : hugging face model: sentence-transformers/all-MiniLM-L6-v2
    - 384-dimensional embeddings'''
'''model is not working remotely so need to download and use locally'''

DEFAULT_EMBEDDING_MODEL = "models/manual_model"
DEFAULT_EMBEDDING_DIMENSION = 384


_embedding_model: SentenceTransformer | None = None


def _get_embedding_model(model_name: str = DEFAULT_EMBEDDING_MODEL) -> SentenceTransformer:
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(model_name, local_files_only=True)
    return _embedding_model


def _normalize_text(text: str) -> str:
    return text.replace("\n", " ")


def generate_embedding(
    text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> list[float]:
    """Generate a single embedding vector locally using a sentence-transformers model."""
    embedding_model = _get_embedding_model(model)
    vector = embedding_model.encode(_normalize_text(text), normalize_embeddings=False)
    return vector.tolist()


def generate_embeddings(
    texts: list[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> list[list[float]]:
    """Generate embedding vectors locally for multiple texts using a sentence-transformers model."""
    embedding_model = _get_embedding_model(model)
    normalized_inputs = [_normalize_text(text) for text in texts]
    vectors = embedding_model.encode(normalized_inputs, normalize_embeddings=False)
    return vectors.tolist()
