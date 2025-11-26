from typing import Dict, Any, List, Optional
from app.parsers.base import BaseParser


class MusicParser(BaseParser):
    """YouTube Music response parser"""
    
    def parse_search(self, data: Dict, limit: int = 20) -> Dict[str, Any]:
        """Parse music search results"""
        results = []
        
        try:
            contents = self.safe_get(
                data,
                "contents",
                "tabbedSearchResultsRenderer",
                "tabs", 0,
                "tabRenderer",
                "content",
                "sectionListRenderer",
                "contents",
                default=[]
            )
            
            for section in contents:
                shelf = section.get("musicShelfRenderer", {})
                items = shelf.get("contents", [])
                
                for item in items:
                    if len(results) >= limit:
                        break
                    
                    parsed = self._parse_music_item(item)
                    if parsed:
                        results.append(parsed)
        
        except Exception as e:
            return {"results": [], "error": str(e)}
        
        return {"results": results, "total": len(results)}
    
    def _parse_music_item(self, item: Dict) -> Optional[Dict]:
        """Parse music search item"""
        renderer = item.get("musicResponsiveListItemRenderer", {})
        if not renderer:
            return None
        
        flex_columns = renderer.get("flexColumns", [])
        
        result = {
            "title": self._get_flex_text(flex_columns, 0),
            "subtitle": self._get_flex_text(flex_columns, 1),
            "thumbnail": self._get_music_thumbnail(renderer.get("thumbnail")),
        }
        
        # Video ID
        overlay = renderer.get("overlay", {}).get("musicItemThumbnailOverlayRenderer", {})
        play_endpoint = self.safe_get(
            overlay, "content", "musicPlayButtonRenderer", 
            "playNavigationEndpoint", "watchEndpoint", default={}
        )
        if play_endpoint.get("videoId"):
            result["videoId"] = play_endpoint["videoId"]
        
        # Browse ID (for albums, artists)
        browse_endpoint = self.safe_get(
            renderer, "navigationEndpoint", "browseEndpoint", default={}
        )
        if browse_endpoint.get("browseId"):
            result["browseId"] = browse_endpoint["browseId"]
            result["type"] = self._get_type_from_browse_id(browse_endpoint["browseId"])
        
        return result
    
    def _get_flex_text(self, columns: List, index: int) -> str:
        """Get text from flex column"""
        try:
            return self.safe_get(
                columns, index,
                "musicResponsiveListItemFlexColumnRenderer",
                "text", "runs", 0, "text",
                default=""
            )
        except:
            return ""
    
    def _get_music_thumbnail(self, obj: Optional[Dict]) -> str:
        """Get music thumbnail"""
        if not obj:
            return ""
        
        thumbnails = self.safe_get(
            obj, "musicThumbnailRenderer", "thumbnail", "thumbnails",
            default=[]
        )
        
        if thumbnails:
            return thumbnails[-1].get("url", "")
        return ""
    
    def _get_type_from_browse_id(self, browse_id: str) -> str:
        """Determine type from browse ID"""
        if browse_id.startswith("UC"):
            return "artist"
        elif browse_id.startswith("MPREb_"):
            return "album"
        elif browse_id.startswith("VL") or browse_id.startswith("PL"):
            return "playlist"
        return "unknown"
    
    def parse_song(self, player: Dict, next_data: Dict) -> Dict[str, Any]:
        """Parse song details"""
        video_details = player.get("videoDetails", {})
        
        return {
            "videoId": video_details.get("videoId"),
            "title": video_details.get("title"),
            "artist": video_details.get("author"),
            "duration": self.get_int(video_details.get("lengthSeconds")),
            "thumbnail": self.get_thumbnail(video_details.get("thumbnail")),
            "isLive": video_details.get("isLiveContent", False),
        }
    
    def extract_lyrics_browse_id(self, next_data: Dict) -> Optional[str]:
        """Extract lyrics browse ID from next data"""
        try:
            tabs = self.safe_get(
                next_data,
                "contents",
                "singleColumnMusicWatchNextResultsRenderer",
                "tabbedRenderer",
                "watchNextTabbedResultsRenderer",
                "tabs",
                default=[]
            )
            
            for tab in tabs:
                renderer = tab.get("tabRenderer", {})
                if renderer.get("title") == "Lyrics":
                    return self.safe_get(
                        renderer, "endpoint", "browseEndpoint", "browseId"
                    )
        except:
            pass
        return None
    
    def parse_lyrics(self, data: Dict) -> Dict[str, Any]:
        """Parse lyrics data"""
        try:
            contents = self.safe_get(
                data, "contents", "sectionListRenderer", "contents", 0,
                default={}
            )
            renderer = contents.get("musicDescriptionShelfRenderer", {})
            
            return {
                "lyrics": self.get_text(renderer.get("description")),
                "source": self.get_text(renderer.get("footer"))
            }
        except:
            return {"lyrics": None, "source": None}
    
    def parse_related(self, data: Dict, limit: int = 20) -> Dict[str, Any]:
        """Parse related songs"""
        return {"raw": data}
    
    def parse_album(self, data: Dict) -> Dict[str, Any]:
        """Parse album data"""
        header = self.safe_get(data, "header", "musicDetailHeaderRenderer", default={})
        
        tracks = []
        contents = self.safe_get(
            data,
            "contents",
            "singleColumnBrowseResultsRenderer",
            "tabs", 0,
            "tabRenderer",
            "content",
            "sectionListRenderer",
            "contents", 0,
            "musicShelfRenderer",
            "contents",
            default=[]
        )
        
        for item in contents:
            renderer = item.get("musicResponsiveListItemRenderer", {})
            flex_columns = renderer.get("flexColumns", [])
            
            video_id = self.safe_get(
                renderer, "overlay", "musicItemThumbnailOverlayRenderer",
                "content", "musicPlayButtonRenderer",
                "playNavigationEndpoint", "watchEndpoint", "videoId"
            )
            
            tracks.append({
                "title": self._get_flex_text(flex_columns, 0),
                "artist": self._get_flex_text(flex_columns, 1),
                "videoId": video_id
            })
        
        return {
            "title": self.get_text(header.get("title")),
            "artist": self.get_text(header.get("subtitle")),
            "thumbnail": self._get_music_thumbnail(header.get("thumbnail")),
            "trackCount": len(tracks),
            "tracks": tracks
        }
    
    def parse_artist(self, data: Dict) -> Dict[str, Any]:
        """Parse artist data"""
        header = self.safe_get(
            data, "header", "musicImmersiveHeaderRenderer", default={}
        )
        
        return {
            "name": self.get_text(header.get("title")),
            "description": self.get_text(header.get("description")),
            "thumbnail": self._get_music_thumbnail(header.get("thumbnail")),
            "subscribers": self.get_text(
                self.safe_get(
                    header, "subscriptionButton", 
                    "subscribeButtonRenderer", "subscriberCountText"
                )
            )
        }
    
    def parse_playlist(self, data: Dict) -> Dict[str, Any]:
        """Parse music playlist"""
        header = self.safe_get(
            data, "header", "musicDetailHeaderRenderer", default={}
        )
        
        return {
            "title": self.get_text(header.get("title")),
            "subtitle": self.get_text(header.get("subtitle")),
            "thumbnail": self._get_music_thumbnail(header.get("thumbnail")),
        }
    
    def parse_home(self, data: Dict) -> Dict[str, Any]:
        """Parse home page"""
        return {"raw": data}
    
    def parse_charts(self, data: Dict) -> Dict[str, Any]:
        """Parse charts"""
        return {"raw": data}
    
    def parse_moods(self, data: Dict) -> Dict[str, Any]:
        """Parse moods and genres"""
        return {"raw": data}
