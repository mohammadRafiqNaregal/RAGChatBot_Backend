from langchain_huggingface import HuggingFaceEmbeddings

'''NOTES'''
'''for my reference this is : hugging face model: sentence-transformers/all-MiniLM-L6-v2
    - 384-dimensional embeddings'''
'''model is not working remotely so need to download and use locally'''

# =============================================================================
# ALTERNATIVE: HuggingFace Inference API (server call) — NOT active, for reference
# =============================================================================
# Instead of loading the model locally, you call HuggingFace's hosted API.
# Requires: pip install requests
# Requires: HF_API_TOKEN set in environment (from huggingface.co/settings/tokens)
#
# import os
# import requests
#
# HF_API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
# HF_API_TOKEN = os.environ.get("HF_API_TOKEN")   # set in .env or environment
#
# def _call_hf_api(texts: list[str]) -> list[list[float]]:
#     """Call HuggingFace Inference API to get embeddings for a list of texts."""
#     headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
#     payload = {
#         "inputs": texts,
#         "options": {"wait_for_model": True},   # waits if model is cold-starting
#     }
#     response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
#     response.raise_for_status()   # raises HTTPError on 4xx/5xx
#     return response.json()        # returns list of vectors e.g. [[0.12, -0.34, ...], ...]
#
# def generate_embedding(text: str, model: str = None) -> list[float]:
#     """Single text → single vector via HF API."""
#     return _call_hf_api([text])[0]
#
# def generate_embeddings(texts: list[str], model: str = None) -> list[list[float]]:
#     """Multiple texts → list of vectors via HF API."""
#     return _call_hf_api(texts)
#
# NOTE: Differences from local model approach:
#   - No GPU/CPU load on your server — HF hosts the model
#   - Requires internet connection on every request
#   - Rate limits apply on free tier (slow for bulk indexing)
#   - Paid tier (Inference Endpoints) gives dedicated throughput
#   - Cold start delay (~10-20s) if model hasn't been used recently on free tier
#   - Same 384-dimensional output as all-MiniLM-L6-v2 local model
# =============================================================================

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
