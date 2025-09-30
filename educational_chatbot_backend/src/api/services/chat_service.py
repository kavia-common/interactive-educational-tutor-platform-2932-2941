from typing import List, Dict, Any, Optional

from ..db.interface import DatabaseInterface
from .rag_service import retrieve_passages


def _agent_responder(agent: str, user_message: str, passages: List[Dict[str, Any]]) -> str:
    """Placeholder agent logic that cites retrieved passages."""
    context_snippets = " ".join([p["text"][:120] for p in passages[:2]]) if passages else ""
    if agent == "tutor":
        return f"As your tutor, here's a helpful explanation. {('Context: ' + context_snippets) if context_snippets else ''}"
    if agent == "grader":
        return f"As a grader, I'll evaluate your understanding. {('Reference: ' + context_snippets) if context_snippets else ''}"
    if agent == "coach":
        return f"As a coach, let's plan your next steps. {('Tip source: ' + context_snippets) if context_snippets else ''}"
    return f"Assistant response. {('Based on: ' + context_snippets) if context_snippets else ''}"


# PUBLIC_INTERFACE
def handle_chat(
    db: DatabaseInterface,
    user_id: str,
    session_id: Optional[str],
    user_message: str,
    agents: Optional[List[str]],
    context_ids: Optional[List[str]],
    metadata: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Handle chat by creating/reusing a session, storing messages, retrieving context via RAG, and orchestrating agents."""
    # Ensure session
    if not session_id:
        title = None
        if metadata and isinstance(metadata, dict):
            title = metadata.get("title")
        session = db.create_session(user_id=user_id, title=title)
        session_id = session["id"]

    # Store user message
    db.append_message(session_id=session_id, role="user", content=user_message)

    # Retrieve context via RAG
    filters: Optional[Dict[str, Any]] = None
    if context_ids:
        # Simple filter shape for demo purposes
        filters = {"context_ids": context_ids}
    passages = retrieve_passages(query=user_message, top_k=5, filters=filters)

    # Orchestrate agents (simple serial aggregation)
    selected_agents = agents or ["tutor"]
    for agent in selected_agents:
        reply = _agent_responder(agent, user_message, passages)
        db.append_message(session_id=session_id, role="assistant", content=f"[{agent}] {reply}")

    messages = db.list_messages(session_id=session_id)
    used_contexts = [p.get("id", "") for p in passages]

    return {
        "session_id": session_id,
        "messages": [{"role": m["role"], "content": m["content"]} for m in messages],
        "used_contexts": used_contexts,
    }
