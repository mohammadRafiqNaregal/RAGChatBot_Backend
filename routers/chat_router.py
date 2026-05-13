from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import controllers.chat_controller as chat_controller
from data.database import get_db
from dependencies.auth import get_current_user
from models.chat_history_model import ChatHistoryListResponse
from models.chat_model import ChatRequest, ChatResponse, SearchRequest, SearchResponse


router = APIRouter(
    prefix="/api",
    tags=["RAG"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/search", summary="Semantic search over indexed document chunks")
def semantic_search(
    payload: SearchRequest,
    current_user: Annotated[dict, Depends(get_current_user)],
) -> SearchResponse:
    return chat_controller.semantic_search(payload, current_user)


@router.post("/chat", summary="Ask questions against indexed documents using local RAG")
def chat_with_documents(
    payload: ChatRequest,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[dict, Depends(get_current_user)],
) -> ChatResponse:
    return chat_controller.chat_with_documents(db, payload, current_user)


@router.get("/chat/history", summary="Get chat history for the current user")
def get_chat_history(
    limit: int = 20,
    db: Annotated[Session, Depends(get_db)] = None,
    current_user: Annotated[dict, Depends(get_current_user)] = None,
) -> ChatHistoryListResponse:
    return chat_controller.get_chat_history(db, current_user, limit)