from typing import Any

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Natural language search query")
    top_k: int = Field(default=5, ge=1, le=10, description="Maximum number of chunks to return")
    department: str | None = Field(default=None, description="Optional department filter")


class SearchResult(BaseModel):
    score: float
    text: str
    metadata: dict[str, Any]


class SearchResponse(BaseModel):
    count: int
    results: list[SearchResult]


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User question to answer from indexed documents")
    top_k: int = Field(default=4, ge=1, le=10, description="Maximum number of chunks to use as context")
    department: str | None = Field(default=None, description="Optional department filter")


class ChatSource(BaseModel):
    score: float
    document_id: int | None = None
    title: str | None = None
    filename: str | None = None
    department: str | None = None
    chunk_index: int | None = None


class ChatResponse(BaseModel):
    answer: str
    sources: list[ChatSource]
    context_count: int