from typing import Dict, Any, List
from app.parsers.base import BaseParser


class StreamParser(BaseParser):
    """Stream data parser"""
    
    def parse_all_streams(self, data: Dict) -> Dict[str, Any]:
        """Parse all available streams"""
        streaming_data = data.get("streamingData", {})
        
        formats = streaming_data.get("formats", [])
        adaptive = streaming_data.get("adaptiveFormats", [])
        
        combined = []
        video_streams = []
        audio_streams = []
        
        # Parse combined formats
        for fmt in formats:
            combined.append(self._parse_format(fmt))
        
        # Parse adaptive formats
        for fmt in adaptive:
            parsed = self._parse_format(fmt)
            mime_type = fmt.get("mimeType", "")
            
            if "video" in mime_type:
                video_streams.append(parsed)
            elif "audio" in mime_type:
                audio_streams.append(parsed)
        
        # Sort by quality
        video_streams.sort(key=lambda x: x.get("height", 0), reverse=True)
        audio_streams.sort(key=lambda x: x.get("bitrate", 0), reverse=True)
        
        return {
            "combined": combined,
            "video": video_streams,
            "audio": audio_streams,
            "expiresIn": streaming_data.get("expiresInSeconds")
        }
    
    def _parse_format(self, fmt: Dict) -> Dict[str, Any]:
        """Parse individual format"""
        return {
            "itag": fmt.get("itag"),
            "url": fmt.get("url"),
            "mimeType": fmt.get("mimeType"),
            "bitrate": fmt.get("bitrate"),
            "width": fmt.get("width"),
            "height": fmt.get("height"),
            "fps": fmt.get("fps"),
            "quality": fmt.get("quality"),
            "qualityLabel": fmt.get("qualityLabel"),
            "audioQuality": fmt.get("audioQuality"),
            "audioSampleRate": fmt.get("audioSampleRate"),
            "audioChannels": fmt.get("audioChannels"),
            "contentLength": fmt.get("contentLength"),
            "approxDurationMs": fmt.get("approxDurationMs"),
        }
