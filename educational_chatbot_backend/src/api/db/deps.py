from typing import Optional
from .interface import DatabaseInterface, InMemoryDB

_db_instance: Optional[DatabaseInterface] = None


# PUBLIC_INTERFACE
def get_db() -> DatabaseInterface:
    """Return a database interface instance; defaults to in-memory for development."""
    global _db_instance
    if _db_instance is None:
        _db_instance = InMemoryDB()
    return _db_instance
