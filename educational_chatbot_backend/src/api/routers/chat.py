from fastapi import APIRouter, Depends
from ..models.schemas import ChatRequest, ChatResponse
from ..db.deps import get_db
from ..db.interface import DatabaseInterface
from ..core.security import get_current_user_id
from ..services import chat_service

router = APIRouter()


# PUBLIC_INTERFACE
@router.post(
    "/message",
    summary="Send Chat Message",
    description="Send a user message and receive assistant responses orchestrated across selected agents. RAG is used to augment context.",
    response_model=ChatResponse,
    responses={200: {"description": "Chat response with updated messages"}},
)
def send_message(payload: ChatRequest, user_id: str = Depends(get_current_user_id), db: DatabaseInterface = Depends(get_db)):
    """Handle chat message for a session. Creates session if not provided and returns updated messages."""
    result = chat_service.handle_chat(
        db=db,
        user_id=user_id,
        session_id=payload.session_id,
        user_message=payload.user_message,
        agents=payload.agents,
        context_ids=payload.context_ids,
        metadata=payload.metadata,
    )
    return result
