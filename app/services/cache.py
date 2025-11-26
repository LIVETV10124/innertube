from cachetools import TTLCache
from typing import Optional, Any
import threading

from app.config import settings


class CacheService:
    """In-memory cache service"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._cache = TTLCache(
                        maxsize=settings.CACHE_MAX_SIZE,
                        ttl=settings.CACHE_TTL
                    )
        return cls._instance
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        return self._cache.get(key)
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        """Set value in cache"""
        self._cache[key] = value
    
    def delete(self, key: str):
        """Delete from cache"""
        self._cache.pop(key, None)
    
    def clear(self):
        """Clear all cache"""
        self._cache.clear()
    
    def stats(self) -> dict:
        """Get cache statistics"""
        return {
            "size": len(self._cache),
            "maxsize": self._cache.maxsize,
            "ttl": self._cache.ttl
        }


cache_service = CacheService()
