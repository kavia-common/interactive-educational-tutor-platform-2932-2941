from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import base64
import hmac
import hashlib
import json

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .config import get_settings

security = HTTPBearer(auto_error=False)


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _b64url_decode(data: str) -> bytes:
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _sign(message: bytes, secret: str) -> str:
    sig = hmac.new(secret.encode("utf-8"), message, hashlib.sha256).digest()
    return _b64url_encode(sig)


def create_access_token(subject: str, expires_minutes: int = 60) -> str:
    """Create a compact JWT-like token (HS256)."""
    settings = get_settings()
    header = {"alg": "HS256", "typ": "JWT"}
    now = datetime.now(tz=timezone.utc)
    payload = {"sub": subject, "iat": int(now.timestamp()), "exp": int((now + timedelta(minutes=expires_minutes)).timestamp())}
    h = _b64url_encode(json.dumps(header, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
    p = _b64url_encode(json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
    msg = f"{h}.{p}".encode("utf-8")
    s = _sign(msg, settings.SECRET_KEY)
    return f"{h}.{p}.{s}"


def verify_token(token: str) -> Dict[str, Any]:
    """Verify token signature and expiry; return payload."""
    settings = get_settings()
    parts = token.split(".")
    if len(parts) != 3:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    h, p, s = parts
    expected_sig = _sign(f"{h}.{p}".encode("utf-8"), settings.SECRET_KEY)
    if not hmac.compare_digest(expected_sig, s):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")
    payload = json.loads(_b64url_decode(p))
    exp = int(payload.get("exp", 0))
    now = int(datetime.now(tz=timezone.utc).timestamp())
    if now >= exp:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    return payload


# PUBLIC_INTERFACE
def get_current_user_id(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> str:
    """Extract and validate current user id from Authorization header Bearer token."""
    if credentials is None or not credentials.scheme.lower() == "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    payload = verify_token(credentials.credentials)
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")
    return str(sub)
