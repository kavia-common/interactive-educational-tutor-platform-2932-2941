import os
from functools import lru_cache
from typing import List
from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Application settings loaded from environment variables."""

    APP_NAME: str = Field(default="Educational Chatbot Backend", description="Application name")
    ENV: str = Field(default=os.getenv("ENV", "development"), description="Environment mode")
    SECRET_KEY: str = Field(default=os.getenv("SECRET_KEY", "dev-secret-key"), description="JWT signing key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")), description="JWT expiry in minutes")
    ALGORITHM: str = Field(default="HS256", description="JWT signing algorithm")

    # CORS
    ALLOW_ORIGINS: List[str] = Field(
        default_factory=lambda: os.getenv("ALLOW_ORIGINS", "*").split(","),
        description="Allowed CORS origins (comma separated)",
    )

    # Database (abstract interface expected; concrete impl in educational_database container)
    DATABASE_URL: str = Field(default=os.getenv("DATABASE_URL", ""), description="Database URL (provided via environment)")
    DATABASE_USER: str = Field(default=os.getenv("DATABASE_USER", ""), description="Database user")
    DATABASE_PASSWORD: str = Field(default=os.getenv("DATABASE_PASSWORD", ""), description="Database password")
    DATABASE_NAME: str = Field(default=os.getenv("DATABASE_NAME", ""), description="Database name")
    DATABASE_PORT: str = Field(default=os.getenv("DATABASE_PORT", ""), description="Database port")

    # RAG / Vector store settings (abstracted)
    VECTOR_STORE_URL: str = Field(default=os.getenv("VECTOR_STORE_URL", ""), description="Vector store service URL")
    VECTOR_STORE_NAMESPACE: str = Field(default=os.getenv("VECTOR_STORE_NAMESPACE", "edu"), description="Vector namespace")

    # Model configuration placeholder
    MODEL_PROVIDER: str = Field(default=os.getenv("MODEL_PROVIDER", "openai"), description="LLM provider (placeholder)")
    MODEL_NAME: str = Field(default=os.getenv("MODEL_NAME", "gpt-4o-mini"), description="LLM model (placeholder)")


@lru_cache
def get_settings() -> Settings:
    """Load settings once per process."""
    return Settings()
