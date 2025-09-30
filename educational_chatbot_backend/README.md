# Educational Chatbot Backend (FastAPI)

Multi-agent educational chatbot with RAG scaffolding, authentication, context management, and OpenAPI docs using the Ocean Professional style.

## Quick start

1. Install dependencies
   pip install -r requirements.txt

2. Run server
   uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

3. Docs
   http://localhost:8000/docs

## Environment variables

See `.env.example` for required variables. Do not commit `.env`.

- ENV
- SECRET_KEY
- ACCESS_TOKEN_EXPIRE_MINUTES
- ALLOW_ORIGINS
- DATABASE_URL, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_PORT
- VECTOR_STORE_URL, VECTOR_STORE_NAMESPACE
- MODEL_PROVIDER, MODEL_NAME

## Notes

- Database layer uses an abstract interface with a default in-memory implementation to unblock development.
- Replace with real educational_database integration by implementing DatabaseInterface in src/api/db/interface.py and wiring it in src/api/db/deps.py.
- Tokens are simple HS256 JWT-like; replace with a hardened implementation (e.g., python-jose, auth provider) for production.
