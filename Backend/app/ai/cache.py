"""
AI Cache Manager.

Central cache abstraction.

Current backend:
    Redis

Future backends:
    DragonflyDB
    KeyDB
    Memory Cache
"""

from __future__ import annotations

import json
import logging

from app.db.redis import redis_client

logger = logging.getLogger(__name__)


class CacheManager:

    # =====================================================
    # Get
    # =====================================================

    def get(
        self,
        key: str,
    ):

        value = redis_client.get(key)

        if value is None:
            return None

        try:
            return json.loads(value)
        except Exception:
            return value

    # =====================================================
    # Set
    # =====================================================

    def set(
        self,
        key: str,
        value,
        ttl: int | None = None,
    ):

        if isinstance(
            value,
            (dict, list),
        ):
            value = json.dumps(value)

        if ttl:

            redis_client.set(
                key,
                value,
                ex=ttl,
            )

        else:

            redis_client.set(
                key,
                value,
            )

    # =====================================================
    # Delete
    # =====================================================

    def delete(
        self,
        key: str,
    ):

        redis_client.delete(key)

    # =====================================================
    # Exists
    # =====================================================

    def exists(
        self,
        key: str,
    ) -> bool:

        return bool(
            redis_client.exists(key)
        )

    # =====================================================
    # Clear
    # =====================================================

    def clear(self):

        redis_client.flushdb()

        logger.warning(
            "Cache cleared."
        )
