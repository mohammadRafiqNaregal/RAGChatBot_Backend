from langchain_openai import OpenAIEmbeddings


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_EMBEDDING_DIMENSION = 1536


def _normalize_text(text: str) -> str:
    return text.replace("\n", " ")


def generate_embedding(
    text: str,
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> list[float]:
    """Generate a single embedding vector from text using OpenAI via LangChain."""
    embedding_client = OpenAIEmbeddings(model=model)
    return embedding_client.embed_query(_normalize_text(text))


def generate_embeddings(
    texts: list[str],
    model: str = DEFAULT_EMBEDDING_MODEL,
) -> list[list[float]]:
    """Generate embedding vectors for multiple texts using OpenAI via LangChain."""
    embedding_client = OpenAIEmbeddings(model=model)
    normalized_inputs = [_normalize_text(text) for text in texts]
    return embedding_client.embed_documents(normalized_inputs)
