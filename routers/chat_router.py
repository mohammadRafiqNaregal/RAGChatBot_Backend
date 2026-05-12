from typing import Annotated

from fastapi import APIRouter, Depends

import controllers.chat_controller as chat_controller
from dependencies.auth import get_current_user
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
    current_user: Annotated[dict, Depends(get_current_user)],
) -> ChatResponse:
    return chat_controller.chat_with_documents(payload, current_user)