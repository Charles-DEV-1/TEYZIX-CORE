"""
Redis Extension Module

PURPOSE:
    Initialize and manage Redis connection for JWT blocklisting and session tracking.
"""

import os
from datetime import datetime, timedelta

redis_client = None


class DummyRedisClient:
    """In-memory fallback for development when Redis is unavailable."""

    def __init__(self):
        self._store = {}

    def _cleanup_expired(self, key):
        item = self._store.get(key)
        if not item:
            return
        _, expiry = item
        if datetime.utcnow() >= expiry:
            del self._store[key]

    def setex(self, key, seconds, value):
        expiry = datetime.utcnow() + timedelta(seconds=int(seconds))
        self._store[key] = (value, expiry)
        return True

    def get(self, key):
        self._cleanup_expired(key)
        item = self._store.get(key)
        if not item:
            return None
        return item[0]

    def exists(self, key):
        self._cleanup_expired(key)
        return 1 if key in self._store else 0

    def delete(self, key):
        self._store.pop(key, None)
        return 1

    def ping(self):
        return True


def init_redis(require_connection=False, redis_url=None):
    """Initialize the Redis client. Raises if Redis is required but unreachable."""
    global redis_client

    url = redis_url or os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    try:
        import redis
        client = redis.from_url(url, decode_responses=True)
        client.ping()
        redis_client = client
        return client
    except Exception as exc:
        if require_connection:
            raise RuntimeError(
                f'Redis is required but connection failed ({url}): {exc}'
            ) from exc
        redis_client = DummyRedisClient()
        return redis_client


def _auto_init():
    require = os.getenv("REDIS_REQUIRED", "false").lower() == "true"
    init_redis(require_connection=require)


_auto_init()
