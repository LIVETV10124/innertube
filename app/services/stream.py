from typing import Optional, Dict, Any, List
import asyncio

from app.services.base import BaseService
from app.clients.innertube import InnerTubeClient
from app.parsers.stream import StreamParser


class StreamService(BaseService):
    """Streaming service"""
    
    def __init__(self):
        super().__init__()
        # Use Android client for better stream availability
        self.client = InnerTubeClient("ANDROID")
        self.ios_client = InnerTubeClient("IOS")
        self.parser = StreamParser()
    
    async def get_streams(self, video_id: str) -> Dict[str, Any]:
        """Get all available streams"""
        cache_key = f"stream:all:{video_id}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached
        
        result = await asyncio.to_thread(self.client.player, video_id)
        parsed = self.parser.parse_all_streams(result)
        
        # Shorter cache for streams (URLs expire)
        self._set_cached(cache_key, parsed, ttl=180)
        return parsed
    
    async def get_audio_stream(
        self, 
        video_id: str, 
        quality: str = "best"
    ) -> Dict[str, Any]:
        """Get audio stream"""
        streams = await self.get_streams(video_id)
        audio_streams = streams.get("audio", [])
        
        if not audio_streams:
            return {"error": "No audio streams available"}
        
        if quality == "best":
            return audio_streams[0]
        elif quality == "medium":
            mid = len(audio_streams) // 2
            return audio_streams[mid]
        elif quality == "low":
            return audio_streams[-1]
        
        return audio_streams[0]
    
    async def get_video_stream(
        self, 
        video_id: str, 
        quality: str = "best"
    ) -> Dict[str, Any]:
        """Get video stream"""
        streams = await self.get_streams(video_id)
        video_streams = streams.get("video", [])
        
        if not video_streams:
            return {"error": "No video streams available"}
        
        quality_map = {
            "1080p": 1080,
            "720p": 720,
            "480p": 480,
            "360p": 360,
            "240p": 240,
            "144p": 144
        }
        
        if quality == "best":
            return video_streams[0]
        
        target = quality_map.get(quality, 720)
        
        for stream in video_streams:
            if stream.get("height", 0) <= target:
                return stream
        
        return video_streams[-1]
    
    async def get_formats(self, video_id: str) -> Dict[str, Any]:
        """Get available formats"""
        streams = await self.get_streams(video_id)
        
        audio_formats = [
            {
                "itag": s.get("itag"),
                "quality": s.get("audioQuality"),
                "bitrate": s.get("bitrate"),
                "mimeType": s.get("mimeType")
            }
            for s in streams.get("audio", [])
        ]
        
        video_formats = [
            {
                "itag": s.get("itag"),
                "quality": s.get("qualityLabel"),
                "resolution": f"{s.get('width')}x{s.get('height')}",
                "fps": s.get("fps"),
                "mimeType": s.get("mimeType")
            }
            for s in streams.get("video", [])
        ]
        
        return {
            "audio": audio_formats,
            "video": video_formats
        }
