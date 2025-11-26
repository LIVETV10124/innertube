from typing import Optional, Dict, Any, List
import asyncio

from app.services.base import BaseService
from app.clients.innertube import InnerTubeClient
from app.parsers.youtube import YouTubeParser


class YouTubeService(BaseService):
    """YouTube service"""
    
    def __init__(self):
        super().__init__()
        self.client = InnerTubeClient("WEB")
        self.android_client = InnerTubeClient("ANDROID")
        self.parser = YouTubeParser()
    
    async def search(
        self, 
        query: str, 
        filter_type: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """Search YouTube"""
        cache_key = f"yt:search:{query}:{filter_type}:{limit}"
        cached = self._get_cached(cache_key)
        if cached:
            return {**cached, "cached": True}
        
        result = await asyncio.to_thread(
            self.client.search, query, filter_type
        )
        parsed = self.parser.parse_search(result, limit)
        
        self._set_cached(cache_key, parsed)
        return {**parsed, "cached": False}
    
    async def get_video(self, video_id: str) -> Dict[str, Any]:
        """Get video details"""
        cache_key = f"yt:video:{video_id}"
        cached = self._get_cached(cache_key)
        if cached:
            return {**cached, "cached": True}
        
        player = await asyncio.to_thread(self.client.player, video_id)
        next_data = await asyncio.to_thread(self.client.next, video_id)
        
        parsed = self.parser.parse_video(player, next_data)
        
        self._set_cached(cache_key, parsed)
        return {**parsed, "cached": False}
    
    async def get_related(self, video_id: str, limit: int = 20) -> Dict[str, Any]:
        """Get related videos"""
        cache_key = f"yt:related:{video_id}:{limit}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        result = await asyncio.to_thread(self.client.next, video_id)
        parsed = self.parser.parse_related(result, limit)
        
        self._set_cached(cache_key, parsed)
        return parsed
    
    async def get_comments(self, video_id: str, limit: int = 20) -> Dict[str, Any]:
        """Get video comments"""
        result = await asyncio.to_thread(self.client.next, video_id)
        return self.parser.parse_comments(result, limit)
    
    async def get_channel(self, channel_id: str) -> Dict[str, Any]:
        """Get channel details"""
        cache_key = f"yt:channel:{channel_id}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        result = await asyncio.to_thread(self.client.browse, channel_id)
        parsed = self.parser.parse_channel(result)
        
        self._set_cached(cache_key, parsed)
        return parsed
    
    async def get_channel_videos(
        self, 
        channel_id: str, 
        limit: int = 30
    ) -> Dict[str, Any]:
        """Get channel videos"""
        # Videos tab
        browse_id = f"{channel_id}/videos"
        result = await asyncio.to_thread(self.client.browse, channel_id)
        return self.parser.parse_channel_videos(result, limit)
    
    async def get_playlist(self, playlist_id: str) -> Dict[str, Any]:
        """Get playlist details and videos"""
        cache_key = f"yt:playlist:{playlist_id}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        browse_id = f"VL{playlist_id}" if not playlist_id.startswith("VL") else playlist_id
        result = await asyncio.to_thread(self.client.browse, browse_id)
        parsed = self.parser.parse_playlist(result)
        
        self._set_cached(cache_key, parsed)
        return parsed
    
    async def get_trending(
        self, 
        region: str = "US",
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get trending videos"""
        cache_key = f"yt:trending:{region}:{category}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        result = await asyncio.to_thread(self.client.browse, "FEtrending")
        parsed = self.parser.parse_trending(result)
        
        self._set_cached(cache_key, parsed, ttl=600)  # 10 min cache
        return parsed
