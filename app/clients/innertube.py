import innertube
from typing import Optional, Dict, Any


class InnerTubeClient:
    """InnerTube client wrapper"""
    
    CLIENT_TYPES = {
        "WEB": "WEB",
        "WEB_REMIX": "WEB_REMIX",  # YouTube Music
        "ANDROID": "ANDROID",
        "ANDROID_MUSIC": "ANDROID_MUSIC",
        "IOS": "IOS",
        "IOS_MUSIC": "IOS_MUSIC",
        "TVHTML5": "TVHTML5",
        "TVHTML5_SIMPLY_EMBEDDED_PLAYER": "TVHTML5_SIMPLY_EMBEDDED_PLAYER"
    }
    
    def __init__(self, client_type: str = "WEB"):
        if client_type not in self.CLIENT_TYPES:
            raise ValueError(f"Invalid client type: {client_type}")
        
        self._client = innertube.InnerTube(client_type)
        self.client_type = client_type
    
    def search(self, query: str, params: Optional[str] = None) -> Dict[str, Any]:
        """Search"""
        return self._client.search(query=query, params=params)
    
    def player(self, video_id: str) -> Dict[str, Any]:
        """Get player data"""
        return self._client.player(video_id=video_id)
    
    def next(self, video_id: str) -> Dict[str, Any]:
        """Get next/watch data"""
        return self._client.next(video_id=video_id)
    
    def browse(self, browse_id: str) -> Dict[str, Any]:
        """Browse endpoint"""
        return self._client.browse(browse_id=browse_id)
    
    def resolve_url(self, url: str) -> Dict[str, Any]:
        """Resolve YouTube URL"""
        return self._client.resolve_url(url=url)
