from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid


class DatabaseInterface(ABC):
    """Abstract database interface expected to be implemented by educational_database container."""
    # PUBLIC_INTERFACE
    @abstractmethod
    def create_user(self, email: str, password_hash: str, name: Optional[str]) -> Dict[str, Any]:
        """Create a new user and return profile dict."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Return user dict by email or None."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    @abstractmethod
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Return user dict by id or None."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    @abstractmethod
    def create_session(self, user_id: str, title: Optional[str] = None) -> Dict[str, Any]:
        """Create a chat session."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    @abstractmethod
    def append_message(self, session_id: str, role: str, content: str) -> Dict[str, Any]:
        """Append a message to a session."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    @abstractmethod
    def list_messages(self, session_id: str) -> List[Dict[str, Any]]:
        """List messages for a session."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    @abstractmethod
    def list_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """List sessions for a user."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    @abstractmethod
    def create_context(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a context resource."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    @abstractmethod
    def list_contexts(self, user_id: str) -> List[Dict[str, Any]]:
        """List context resources."""
        raise NotImplementedError


class InMemoryDB(DatabaseInterface):
    """Simple in-memory implementation for development and CI without external DB."""
    def __init__(self) -> None:
        self.users: Dict[str, Dict[str, Any]] = {}
        self.users_by_email: Dict[str, str] = {}
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.messages: Dict[str, List[Dict[str, Any]]] = {}
        self.contexts: Dict[str, Dict[str, Any]] = {}

    def create_user(self, email: str, password_hash: str, name: Optional[str]) -> Dict[str, Any]:
        if email in self.users_by_email:
            raise ValueError("User already exists")
        uid = str(uuid.uuid4())
        now = datetime.utcnow()
        profile = {"id": uid, "email": email, "name": name, "password_hash": password_hash, "created_at": now}
        self.users[uid] = profile
        self.users_by_email[email] = uid
        return profile

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        uid = self.users_by_email.get(email)
        if not uid:
            return None
        return self.users.get(uid)

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.users.get(user_id)

    def create_session(self, user_id: str, title: Optional[str] = None) -> Dict[str, Any]:
        sid = str(uuid.uuid4())
        now = datetime.utcnow()
        session = {"id": sid, "user_id": user_id, "created_at": now, "updated_at": now, "title": title}
        self.sessions[sid] = session
        self.messages[sid] = []
        return session

    def append_message(self, session_id: str, role: str, content: str) -> Dict[str, Any]:
        msg = {"role": role, "content": content, "timestamp": datetime.utcnow()}
        if session_id not in self.messages:
            self.messages[session_id] = []
        self.messages[session_id].append(msg)
        if session_id in self.sessions:
            self.sessions[session_id]["updated_at"] = datetime.utcnow()
        return msg

    def list_messages(self, session_id: str) -> List[Dict[str, Any]]:
        return list(self.messages.get(session_id, []))

    def list_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        return [s for s in self.sessions.values() if s.get("user_id") == user_id]

    def create_context(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        rid = str(uuid.uuid4())
        now = datetime.utcnow()
        ctx = {"id": rid, "user_id": user_id, "created_at": now, **data}
        self.contexts[rid] = ctx
        return ctx

    def list_contexts(self, user_id: str) -> List[Dict[str, Any]]:
        return [c for c in self.contexts.values() if c.get("user_id") == user_id]
