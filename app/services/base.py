from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from app.clients.innertube import InnerTubeClient
from app.services.cache import cache_service
from app.core.logging import get_logger


class BaseService(ABC):
    """Base service class"""
    
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.cache = cache_service
    
    def _get_cached(self, key: str) -> Optional[Dict]:
        """Get from cache"""
        return self.cache.get(key)
    
    def _set_cached(self, key: str, value: Dict, ttl: int = 300):
        """Set in cache"""
        self.cache.set(key, value, ttl)
