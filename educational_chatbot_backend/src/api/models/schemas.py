from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr


# --- Auth Schemas ---

class SignupRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="Password (min 8 chars)")
    name: Optional[str] = Field(None, description="Full name")


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="Password")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Expiry in seconds")


class UserProfile(BaseModel):
    id: str = Field(..., description="User ID")
    email: EmailStr = Field(..., description="Email")
    name: Optional[str] = Field(None, description="User display name")
    created_at: datetime = Field(..., description="Creation timestamp")


# --- Chat Schemas ---

class ChatMessage(BaseModel):
    role: str = Field(..., description="Message role: user|assistant|system|tool")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(None, description="Existing session ID, if continuing a chat")
    user_message: str = Field(..., description="User message content")
    context_ids: Optional[List[str]] = Field(default=None, description="Context resource IDs to inject")
    agents: Optional[List[str]] = Field(default=None, description="Agents to participate (e.g., tutor, grader, coach)")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata for orchestration")


class ChatResponse(BaseModel):
    session_id: str = Field(..., description="Session ID for the conversation")
    messages: List[ChatMessage] = Field(..., description="Ordered messages including system and tool outputs")
    used_contexts: List[str] = Field(default_factory=list, description="Context IDs used for this response")


# --- Context Schemas ---

class ContextResource(BaseModel):
    id: str = Field(..., description="Resource ID")
    title: str = Field(..., description="Resource title")
    type: str = Field(..., description="Type: note|doc|link|snippet")
    content: Optional[str] = Field(None, description="Resource content or summary")
    url: Optional[str] = Field(None, description="External URL, if applicable")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")


class CreateContextRequest(BaseModel):
    title: str = Field(..., description="Resource title")
    type: str = Field(..., description="Type: note|doc|link|snippet")
    content: Optional[str] = Field(None, description="Resource content")
    url: Optional[str] = Field(None, description="External URL")


class SessionInfo(BaseModel):
    id: str = Field(..., description="Session ID")
    user_id: str = Field(..., description="Owner user ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    title: Optional[str] = Field(None, description="Optional session title")


# --- RAG Schemas ---

class RAGIngestRequest(BaseModel):
    source_id: Optional[str] = Field(None, description="Optional caller-provided source id")
    title: Optional[str] = Field(None, description="Title of the document")
    text: str = Field(..., description="Raw text to index")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Extra metadata (course, topic, etc.)")


class RAGIngestResponse(BaseModel):
    id: str = Field(..., description="Indexed document id")
    chunks_indexed: int = Field(..., description="Number of chunks stored")
    vector_namespace: str = Field(..., description="Namespace used for storage")


class RAGQueryRequest(BaseModel):
    query: str = Field(..., description="Natural language query")
    top_k: int = Field(default=5, description="Number of passages to retrieve")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Metadata filters")


class RAGPassage(BaseModel):
    id: str = Field(..., description="Chunk or doc id")
    score: float = Field(..., description="Similarity score")
    text: str = Field(..., description="Passage text")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadata")


class RAGQueryResponse(BaseModel):
    query: str = Field(..., description="Original query")
    results: list[RAGPassage] = Field(..., description="Top passages")
