from langchain_core.prompts import PromptTemplate

from services.llm_service import get_langchain_ollama
from services.retrieval_service import retrieve_relevant_chunks


def _build_context(results: list[dict]) -> str:
    context_blocks: list[str] = []

    for idx, item in enumerate(results, start=1):
        metadata = item.get("metadata", {})
        text = (item.get("text") or "").strip()

        title = metadata.get("title") or metadata.get("filename") or "Untitled"
        department = metadata.get("department") or "Unknown"

        context_blocks.append(
            f"[{idx}] title={title} department={department}\n{text}"
        )

    return "\n\n".join(context_blocks)


def _build_sources(results: list[dict]) -> list[dict]:
    sources: list[dict] = []

    for item in results:
        metadata = item.get("metadata", {})
        sources.append(
            {
                "score": float(item.get("score", 0.0)),
                "document_id": metadata.get("document_id"),
                "title": metadata.get("title"),
                "filename": metadata.get("filename"),
                "department": metadata.get("department"),
                "chunk_index": metadata.get("chunk_index"),
            }
        )

    return sources


def answer_question_with_rag(
    message: str,
    current_user: dict,
    top_k: int = 4,
    department: str | None = None,
) -> tuple[str, list[dict], int]:
    results = retrieve_relevant_chunks(
        query=message,
        current_user=current_user,
        top_k=top_k,
        department=department,
    )

    if not results:
        return (
            "I could not find relevant indexed context for your question.",
            [],
            0,
        )

    context = _build_context(results)

    prompt_template = PromptTemplate.from_template(
        "You are a helpful enterprise knowledge assistant. "
        "Answer only from the provided context. If the context is insufficient, say so clearly.\n\n"
        "Question:\n{question}\n\n"
        "Context:\n{context}\n\n"
        "Give a concise answer and mention key supporting points from context."
    )

    filled_prompt = prompt_template.format(question=message, context=context)
    answer = get_langchain_ollama().invoke(filled_prompt)
    sources = _build_sources(results)
    return answer, sources, len(results)
