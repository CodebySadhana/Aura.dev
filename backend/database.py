"""Storage seam for a production DB. JSON store is deliberately the local default."""
import os
from .crud import JsonStore


def get_store() -> JsonStore:
    # A database adapter can replace this when DATABASE_URL is configured.
    # ponytail: JSON fallback has no distributed write coordination; add a DB adapter for multi-instance deploys.
    return JsonStore(os.getenv("AURA_DATA_DIR", "backend/data/conversations"))
