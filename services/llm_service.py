import json
from urllib import error, request

from fastapi import HTTPException, status


DEFAULT_OLLAMA_MODEL = "qwen2.5:3b"
DEFAULT_OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_with_ollama(prompt: str, model: str = DEFAULT_OLLAMA_MODEL) -> str:
    payload = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "stream": False,
        }
    ).encode("utf-8")

    req = request.Request(
        DEFAULT_OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=120) as response:
            body = json.loads(response.read().decode("utf-8"))
    except error.URLError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Could not reach Ollama at http://localhost:11434. "
                "Start Ollama and pull the configured model first."
            ),
        ) from exc

    answer = (body.get("response") or "").strip()
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Ollama returned an empty response.",
        )
    return answer