from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.chat_history_entity import ChatHistoryEntity
from models.chat_history_model import ChatHistoryListResponse, ChatHistoryResponse
from models.chat_model import ChatRequest, ChatResponse, SearchRequest, SearchResponse, SearchResult
from services.rag_service import answer_question_with_rag
from services.retrieval_service import retrieve_relevant_chunks


def _to_chat_history_response(item: ChatHistoryEntity) -> ChatHistoryResponse:
    return ChatHistoryResponse.model_validate(item)


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


def chat_with_documents(db: Session, payload: ChatRequest, current_user: dict) -> ChatResponse:
    answer, sources, context_count = answer_question_with_rag(
        message=payload.message,
        current_user=current_user,
        top_k=payload.top_k,
        department=payload.department,
    )

    # Generate or use provided conversation_id
    conversation_id = payload.conversation_id or str(uuid4())

    history_item = ChatHistoryEntity(
        user_id=current_user["id"],
        conversation_id=conversation_id,
        question=payload.message,
        response=answer,
    )
    db.add(history_item)
    db.commit()

    return ChatResponse(
        answer=answer,
        sources=sources,
        context_count=context_count,
        conversation_id=conversation_id,
    )


def get_chat_history(db: Session, current_user: dict, limit: int = 20) -> ChatHistoryListResponse:
    statement = (
        select(ChatHistoryEntity)
        .where(ChatHistoryEntity.user_id == current_user["id"])
        .order_by(ChatHistoryEntity.timestamp.desc())
        .limit(limit)
    )
    items = db.scalars(statement).all()
    history = [_to_chat_history_response(item) for item in items]
    return ChatHistoryListResponse(count=len(history), items=history)