from typing import List, Dict, Any, Callable
from fastapi import FastAPI
from .config import Settings

openapi_tags: List[Dict[str, Any]] = [
    {"name": "Health", "description": "System status and health checks."},
    {"name": "Authentication", "description": "User signup, login, and token management."},
    {"name": "Chat", "description": "Multi-agent chat endpoints for educational assistance."},
    {"name": "Contexts", "description": "Session and context management for conversations."},
    {"name": "RAG", "description": "Retrieval Augmented Generation operations and document management."},
    {"name": "Meta", "description": "Service metadata and theme tokens."},
]


def build_openapi_schema(app: FastAPI, settings: Settings) -> Callable[[], Dict[str, Any]]:
    """Return a function that generates a custom OpenAPI schema including theme metadata."""

    def custom_openapi() -> Dict[str, Any]:
        if app.openapi_schema:
            return app.openapi_schema  # type: ignore[return-value]
        openapi_schema = app.openapi()
        # Inject Ocean Professional theme metadata
        openapi_schema["info"]["x-theme"] = {
            "name": "Ocean Professional",
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
        }
        app.openapi_schema = openapi_schema  # type: ignore[assignment]
        return app.openapi_schema  # type: ignore[return-value]

    return custom_openapi
