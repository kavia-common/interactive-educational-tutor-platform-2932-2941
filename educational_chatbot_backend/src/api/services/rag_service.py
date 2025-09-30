from typing import Dict, Any, List, Optional
import uuid
import math

# Very simple in-memory "vector store" for demonstration (BM25-like scoring using term overlap)
_VECTOR_NS: Dict[str, Dict[str, Any]] = {
    "edu": {
        "docs": {},  # id -> {"text": str, "metadata": dict}
        "chunks": {},  # id -> {"text": str, "metadata": dict}
    }
}


def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in text.split() if t.strip()]


def _score(query_tokens: List[str], text_tokens: List[str]) -> float:
    if not query_tokens or not text_tokens:
        return 0.0
    overlap = sum(1 for qt in query_tokens if qt in text_tokens)
    return overlap / math.sqrt(len(text_tokens) + 1)


# PUBLIC_INTERFACE
def ingest_text(text: str, title: Optional[str], metadata: Optional[Dict[str, Any]], namespace: str = "edu") -> Dict[str, Any]:
    """Ingest text into a simple in-memory store by chunking into ~120 tokens."""
    ns = _VECTOR_NS.setdefault(namespace, {"docs": {}, "chunks": {}})
    doc_id = str(uuid.uuid4())
    ns["docs"][doc_id] = {"text": text, "title": title, "metadata": metadata or {}}

    tokens = _tokenize(text)
    chunk_size = 120  # small to keep demos light
    chunks_indexed = 0
    for i in range(0, len(tokens), chunk_size):
        chunk_tokens = tokens[i : i + chunk_size]
        chunk_text = " ".join(chunk_tokens)
        chunk_id = f"{doc_id}-c{i//chunk_size}"
        ns["chunks"][chunk_id] = {"text": chunk_text, "metadata": {"doc_id": doc_id, **(metadata or {})}}
        chunks_indexed += 1

    return {"id": doc_id, "chunks_indexed": chunks_indexed, "vector_namespace": namespace}


# PUBLIC_INTERFACE
def retrieve_passages(query: str, top_k: int = 5, filters: Optional[Dict[str, Any]] = None, namespace: str = "edu") -> List[Dict[str, Any]]:
    """Retrieve top_k passages by simple token overlap scoring with optional filters."""
    ns = _VECTOR_NS.get(namespace)
    if not ns:
        return []
    query_tokens = _tokenize(query)
    results: List[Dict[str, Any]] = []

    for cid, entry in ns["chunks"].items():
        if filters:
            ok = all(entry.get("metadata", {}).get(k) == v for k, v in (filters or {}).items())
            if not ok:
                continue
        score = _score(query_tokens, _tokenize(entry["text"]))
        if score <= 0:
            continue
        results.append({"id": cid, "score": score, "text": entry["text"], "metadata": entry.get("metadata", {})})

    results.sort(key=lambda r: r["score"], reverse=True)
    return results[:top_k]
