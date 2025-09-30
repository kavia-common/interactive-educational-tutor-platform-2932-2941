import hashlib
from typing import Optional, Dict, Any
from ..db.interface import DatabaseInterface
from ..core.security import create_access_token
from ..core.config import get_settings


def _hash_password(password: str) -> str:
    # Simple salted hash (for demo only). In production, use bcrypt/argon2.
    salt = "edu-salt"
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


def _check_password(password: str, password_hash: str) -> bool:
    return _hash_password(password) == password_hash


# PUBLIC_INTERFACE
def signup(db: DatabaseInterface, email: str, password: str, name: Optional[str]) -> Dict[str, Any]:
    """Create a new user and return token + profile."""
    pwd_hash = _hash_password(password)
    profile = db.create_user(email=email, password_hash=pwd_hash, name=name)
    settings = get_settings()
    token = create_access_token(subject=profile["id"], expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {"token": token, "profile": {k: v for k, v in profile.items() if k != "password_hash"}}


# PUBLIC_INTERFACE
def login(db: DatabaseInterface, email: str, password: str) -> Dict[str, Any]:
    """Authenticate a user and return token + profile."""
    user = db.get_user_by_email(email)
    if not user or not _check_password(password, user.get("password_hash", "")):
        raise ValueError("Invalid credentials")
    settings = get_settings()
    token = create_access_token(subject=user["id"], expires_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {"token": token, "profile": {k: v for k, v in user.items() if k != "password_hash"}}
