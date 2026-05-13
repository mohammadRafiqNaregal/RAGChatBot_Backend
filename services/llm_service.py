from fastapi import HTTPException, status
from langchain_ollama import OllamaLLM


DEFAULT_OLLAMA_MODEL = "qwen2.5:3b"
DEFAULT_OLLAMA_URL = "http://localhost:11434"


_llm_clients: dict[str, OllamaLLM] = {}


def _get_ollama_client(model: str, base_url: str = DEFAULT_OLLAMA_URL) -> OllamaLLM:
    cache_key = f"{base_url}|{model}"
    if cache_key not in _llm_clients:
        _llm_clients[cache_key] = OllamaLLM(
            model=model,
            base_url=base_url,
            temperature=0,
        )
    return _llm_clients[cache_key]


def get_langchain_ollama(model: str = DEFAULT_OLLAMA_MODEL) -> OllamaLLM:
    return _get_ollama_client(model=model)


def generate_with_ollama(prompt: str, model: str = DEFAULT_OLLAMA_MODEL) -> str:
    try:
        client = _get_ollama_client(model=model)
        answer = (client.invoke(prompt) or "").strip()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Could not reach Ollama at http://localhost:11434. "
                "Start Ollama and pull the configured model first."
            ),
        ) from exc

    if not answer:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Ollama returned an empty response.",
        )
    return answer