from langchain_huggingface import HuggingFaceEmbeddings

'''NOTES'''
'''for my reference this is : hugging face model: sentence-transformers/all-MiniLM-L6-v2
    - 384-dimensional embeddings'''
'''model is not working remotely so need to download and use locally'''

DEFAULT_EMBEDDING_MODEL = "models/manual_model"
DEFAULT_EMBEDDING_DIMENSION = 384


_embedding_model: HuggingFaceEmbeddings | None = None


def _get_embedding_model(model_name: str = DEFAULT_EMBEDDING_MODEL) -> HuggingFaceEmbeddings:
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={"local_files_only": True},
            encode_kwargs={"normalize_embeddings": False},
        )
    return _embedding_model


def get_langchain_embeddings() -> HuggingFaceEmbeddings:
    return _get_embedding_model(DEFAULT_EMBEDDING_MODEL)


def _normalize_text(text: str) -> str:
    return text.replace("\n", " ")


def generate_embedding(
    text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> list[float]:
    """Generate a single embedding vector locally using LangChain HuggingFace embeddings."""
    embedding_model = _get_embedding_model(model)
    return embedding_model.embed_query(_normalize_text(text))


def generate_embeddings(
    texts: list[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> list[list[float]]:
    """Generate embedding vectors locally for multiple texts using LangChain HuggingFace embeddings."""
    embedding_model = _get_embedding_model(model)
    normalized_inputs = [_normalize_text(text) for text in texts]
    return embedding_model.embed_documents(normalized_inputs)
