from models.chat_model import ChatRequest, ChatResponse, SearchRequest, SearchResponse, SearchResult
from services.rag_service import answer_question_with_rag
from services.retrieval_service import retrieve_relevant_chunks


def semantic_search(payload: SearchRequest, current_user: dict) -> SearchResponse:
    results = retrieve_relevant_chunks(
        query=payload.query,
        current_user=current_user,
        top_k=payload.top_k,
        department=payload.department,
    )
    return SearchResponse(
        count=len(results),
        results=[SearchResult(**item) for item in results],
    )


def chat_with_documents(payload: ChatRequest, current_user: dict) -> ChatResponse:
    answer, sources, context_count = answer_question_with_rag(
        message=payload.message,
        current_user=current_user,
        top_k=payload.top_k,
        department=payload.department,
    )
    return ChatResponse(answer=answer, sources=sources, context_count=context_count)