from fastapi import APIRouter, Depends
from ..models.schemas import RAGIngestRequest, RAGIngestResponse, RAGQueryRequest, RAGQueryResponse, RAGPassage
from ..core.security import get_current_user_id
from ..services.rag_service import ingest_text, retrieve_passages

router = APIRouter()


# PUBLIC_INTERFACE
@router.post(
    "/ingest",
    summary="Ingest Text",
    description="Ingest raw text for later retrieval. Internally chunked and stored in a simple in-memory vector-like index.",
    response_model=RAGIngestResponse,
)
def rag_ingest(payload: RAGIngestRequest, user_id: str = Depends(get_current_user_id)):
    """Ingest a document into the RAG store."""
    res = ingest_text(text=payload.text, title=payload.title, metadata=payload.metadata or {})
    return RAGIngestResponse(id=res["id"], chunks_indexed=res["chunks_indexed"], vector_namespace=res["vector_namespace"])


# PUBLIC_INTERFACE
@router.post(
    "/query",
    summary="Query RAG",
    description="Retrieve top passages relevant to a query using a simple token overlap score.",
    response_model=RAGQueryResponse,
)
def rag_query(payload: RAGQueryRequest, user_id: str = Depends(get_current_user_id)):
    """Query the RAG store and return top-k passages."""
    results = retrieve_passages(query=payload.query, top_k=payload.top_k, filters=payload.filters)
    return RAGQueryResponse(
        query=payload.query,
        results=[RAGPassage(id=r["id"], score=r["score"], text=r["text"], metadata=r.get("metadata")) for r in results],
    )
