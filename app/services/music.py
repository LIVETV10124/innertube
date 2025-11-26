from typing import Optional, Dict, Any
import asyncio

from app.services.base import BaseService
from app.clients.innertube import InnerTubeClient
from app.parsers.music import MusicParser


class MusicService(BaseService):
    """YouTube Music service"""
    
    def __init__(self):
        super().__init__()
        self.client = InnerTubeClient("WEB_REMIX")
        self.android_client = InnerTubeClient("ANDROID_MUSIC")
        self.parser = MusicParser()
    
    async def search(
        self,
        query: str,
        filter_type: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """Search YouTube Music"""
        cache_key = f"music:search:{query}:{filter_type}:{limit}"
        cached = self._get_cached(cache_key)
        if cached:
            return {**cached, "cached": True}
        
        params = self._get_search_params(filter_type)
        result = await asyncio.to_thread(
            self.client.search, query, params
        )
        parsed = self.parser.parse_search(result, limit)
        
        self._set_cached(cache_key, parsed)
        return {**parsed, "cached": False}
    
    def _get_search_params(self, filter_type: Optional[str]) -> Optional[str]:
        """Get search filter params"""
        params_map = {
            "songs": "EgWKAQIIAWoKEAoQAxAEEAkQBQ%3D%3D",
            "videos": "EgWKAQIQAWoKEAoQAxAEEAkQBQ%3D%3D",
            "albums": "EgWKAQIYAWoKEAoQAxAEEAkQBQ%3D%3D",
            "artists": "EgWKAQIgAWoKEAoQAxAEEAkQBQ%3D%3D",
            "playlists": "EgWKAQIoAWoKEAoQAxAEEAkQBQ%3D%3D",
        }
        return params_map.get(filter_type)
    
    async def get_song(self, video_id: str) -> Dict[str, Any]:
        """Get song details"""
        cache_key = f"music:song:{video_id}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        player = await asyncio.to_thread(self.client.player, video_id)
        next_data = await asyncio.to_thread(self.client.next, video_id)
        
        parsed = self.parser.parse_song(player, next_data)
        
        self._set_cached(cache_key, parsed)
        return parsed
    
    async def get_lyrics(self, video_id: str) -> Dict[str, Any]:
        """Get song lyrics"""
        cache_key = f"music:lyrics:{video_id}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        # Get next data to find lyrics browse ID
        next_data = await asyncio.to_thread(self.client.next, video_id)
        lyrics_browse_id = self.parser.extract_lyrics_browse_id(next_data)
        
        if not lyrics_browse_id:
            return {"lyrics": None, "source": None, "error": "Lyrics not available"}
        
        lyrics_data = await asyncio.to_thread(
            self.client.browse, lyrics_browse_id
        )
        parsed = self.parser.parse_lyrics(lyrics_data)
        
        self._set_cached(cache_key, parsed)
        return parsed
    
    async def get_related(self, video_id: str, limit: int = 20) -> Dict[str, Any]:
        """Get related songs"""
        next_data = await asyncio.to_thread(self.client.next, video_id)
        return self.parser.parse_related(next_data, limit)
    
    async def get_album(self, browse_id: str) -> Dict[str, Any]:
        """Get album details"""
        cache_key = f"music:album:{browse_id}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        result = await asyncio.to_thread(self.client.browse, browse_id)
        parsed = self.parser.parse_album(result)
        
        self._set_cached(cache_key, parsed)
        return parsed
    
    async def get_artist(self, channel_id: str) -> Dict[str, Any]:
        """Get artist details"""
        cache_key = f"music:artist:{channel_id}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        result = await asyncio.to_thread(self.client.browse, channel_id)
        parsed = self.parser.parse_artist(result)
        
        self._set_cached(cache_key, parsed)
        return parsed
    
    async def get_artist_albums(self, channel_id: str) -> Dict[str, Any]:
        """Get artist albums"""
        artist = await self.get_artist(channel_id)
        # Extract albums from artist data or make additional request
        return {"albums": artist.get("albums", [])}
    
    async def get_playlist(self, playlist_id: str) -> Dict[str, Any]:
        """Get music playlist"""
        cache_key = f"music:playlist:{playlist_id}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        browse_id = f"VL{playlist_id}" if not playlist_id.startswith("VL") else playlist_id
        result = await asyncio.to_thread(self.client.browse, browse_id)
        parsed = self.parser.parse_playlist(result)
        
        self._set_cached(cache_key, parsed)
        return parsed
    
    async def get_home(self) -> Dict[str, Any]:
        """Get home page content"""
        cache_key = "music:home"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        result = await asyncio.to_thread(
            self.client.browse, "FEmusic_home"
        )
        parsed = self.parser.parse_home(result)
        
        self._set_cached(cache_key, parsed, ttl=600)
        return parsed
    
    async def get_charts(self, region: str = "US") -> Dict[str, Any]:
        """Get music charts"""
        cache_key = f"music:charts:{region}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        result = await asyncio.to_thread(
            self.client.browse, "FEmusic_charts"
        )
        parsed = self.parser.parse_charts(result)
        
        self._set_cached(cache_key, parsed, ttl=3600)  # 1 hour
        return parsed
    
    async def get_moods(self) -> Dict[str, Any]:
        """Get moods and genres"""
        cache_key = "music:moods"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        result = await asyncio.to_thread(
            self.client.browse, "FEmusic_moods_and_genres"
        )
        parsed = self.parser.parse_moods(result)
        
        self._set_cached(cache_key, parsed, ttl=3600)
        return parsed
    
    async def get_new_releases(self) -> Dict[str, Any]:
        """Get new releases"""
        cache_key = "music:new_releases"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        result = await asyncio.to_thread(
            self.client.browse, "FEmusic_new_releases"
        )
        
        self._set_cached(cache_key, result, ttl=3600)
        return result
