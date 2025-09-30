from typing import Dict, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, chat, contexts, rag, health
from .core.config import get_settings, Settings
from .core.openapi import build_openapi_schema, openapi_tags

# Initialize settings and app with metadata and Ocean Professional theme hints
settings: Settings = get_settings()

app = FastAPI(
    title="Educational Chatbot Backend",
    description=(
        "Multi-agent educational chatbot platform with Retrieval-Augmented Generation (RAG), "
        "user authentication, session/context management, and REST APIs for frontend integration.\n\n"
        "Style: Ocean Professional (Blue & amber accents)."
    ),
    version="0.1.0",
    contact={"name": "Educational Platform", "email": "support@example.com"},
    license_info={"name": "MIT License"},
    openapi_tags=openapi_tags,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router, prefix="", tags=["Health"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(contexts.router, prefix="/contexts", tags=["Contexts"])
app.include_router(rag.router, prefix="/rag", tags=["RAG"])

# Customize OpenAPI generation to include Ocean Professional theme metadata
app.openapi = build_openapi_schema(app, settings)  # type: ignore[assignment]


# PUBLIC_INTERFACE
@app.get(
    "/theme",
    summary="Get UI Theme",
    description="Returns Ocean Professional style theme tokens for frontend usage.",
    response_model=Dict[str, Any],
    tags=["Meta"],
)
def get_theme_tokens() -> Dict[str, Any]:
    """This endpoint provides UI style tokens for the Ocean Professional theme to support consistent frontend styling."""
    return {
        "name": "Ocean Professional",
        "description": "Blue & amber accents",
        "colors": {
            "primary": "#2563EB",
            "secondary": "#F59E0B",
            "success": "#F59E0B",
            "error": "#EF4444",
            "background": "#f9fafb",
            "surface": "#ffffff",
            "text": "#111827",
        },
        "gradient": "from-blue-500/10 to-gray-50",
        "applicationStyle": "Modern",
        "layout": "Top nav, left menu, central chat, optional right sidebar",
    }
