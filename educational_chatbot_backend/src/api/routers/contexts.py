from fastapi import APIRouter, Depends
from typing import List
from ..models.schemas import SessionInfo, CreateContextRequest, ContextResource
from ..db.deps import get_db
from ..db.interface import DatabaseInterface
from ..core.security import get_current_user_id

router = APIRouter()


# PUBLIC_INTERFACE
@router.get(
    "/sessions",
    summary="List Sessions",
    description="List all chat sessions for the current user.",
    response_model=List[SessionInfo],
)
def list_sessions(user_id: str = Depends(get_current_user_id), db: DatabaseInterface = Depends(get_db)):
    """Return sessions for the current user."""
    sessions = db.list_sessions(user_id=user_id)
    return [
        SessionInfo(
            id=s["id"],
            user_id=s["user_id"],
            created_at=s["created_at"],
            updated_at=s["updated_at"],
            title=s.get("title"),
        )
        for s in sessions
    ]


# PUBLIC_INTERFACE
@router.post(
    "/resources",
    summary="Create Context Resource",
    description="Create a context resource (note, doc, link, snippet) to be used in chat.",
    response_model=ContextResource,
)
def create_context_resource(payload: CreateContextRequest, user_id: str = Depends(get_current_user_id), db: DatabaseInterface = Depends(get_db)):
    """Create a resource for context injection."""
    ctx = db.create_context(user_id=user_id, data=payload.dict())
    return ContextResource(
        id=ctx["id"],
        title=ctx["title"],
        type=ctx["type"],
        content=ctx.get("content"),
        url=ctx.get("url"),
        created_at=ctx["created_at"],
    )


# PUBLIC_INTERFACE
@router.get(
    "/resources",
    summary="List Context Resources",
    description="List context resources for the current user.",
    response_model=List[ContextResource],
)
def list_context_resources(user_id: str = Depends(get_current_user_id), db: DatabaseInterface = Depends(get_db)):
    """Return context resources for the user."""
    ctxs = db.list_contexts(user_id=user_id)
    return [
        ContextResource(
            id=c["id"],
            title=c["title"],
            type=c["type"],
            content=c.get("content"),
            url=c.get("url"),
            created_at=c["created_at"],
        )
        for c in ctxs
    ]
