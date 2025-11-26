from typing import Dict, Any, List, Optional
from app.parsers.base import BaseParser


class YouTubeParser(BaseParser):
    """YouTube response parser"""
    
    def parse_search(self, data: Dict, limit: int = 20) -> Dict[str, Any]:
        """Parse search results"""
        results = []
        
        try:
            contents = self.safe_get(
                data,
                "contents",
                "twoColumnSearchResultsRenderer",
                "primaryContents",
                "sectionListRenderer",
                "contents",
                default=[]
            )
            
            for section in contents:
                items = self.safe_get(
                    section, "itemSectionRenderer", "contents", default=[]
                )
                
                for item in items:
                    if len(results) >= limit:
                        break
                    
                    parsed = self._parse_search_item(item)
                    if parsed:
                        results.append(parsed)
        
        except Exception as e:
            return {"results": [], "error": str(e), "raw": data}
        
        return {"results": results, "total": len(results)}
    
    def _parse_search_item(self, item: Dict) -> Optional[Dict]:
        """Parse individual search item"""
        if "videoRenderer" in item:
            return self._parse_video_renderer(item["videoRenderer"])
        elif "channelRenderer" in item:
            return self._parse_channel_renderer(item["channelRenderer"])
        elif "playlistRenderer" in item:
            return self._parse_playlist_renderer(item["playlistRenderer"])
        return None
    
    def _parse_video_renderer(self, video: Dict) -> Dict:
        """Parse video renderer"""
        return {
            "type": "video",
            "videoId": video.get("videoId"),
            "title": self.get_text(video.get("title")),
            "description": self.get_text(video.get("descriptionSnippet")),
            "thumbnail": self.get_thumbnail(video.get("thumbnail")),
            "duration": self.get_text(video.get("lengthText")),
            "views": self.get_text(video.get("viewCountText")),
            "published": self.get_text(video.get("publishedTimeText")),
            "channel": {
                "name": self.get_text(video.get("ownerText")),
                "id": self.safe_get(
                    video, "ownerText", "runs", 0, 
                    "navigationEndpoint", "browseEndpoint", "browseId"
                ),
                "thumbnail": self.get_thumbnail(
                    video.get("channelThumbnailSupportedRenderers", {}).get(
                        "channelThumbnailWithLinkRenderer", {}
                    ).get("thumbnail")
                )
            }
        }
    
    def _parse_channel_renderer(self, channel: Dict) -> Dict:
        """Parse channel renderer"""
        return {
            "type": "channel",
            "channelId": channel.get("channelId"),
            "title": self.get_text(channel.get("title")),
            "description": self.get_text(channel.get("descriptionSnippet")),
            "thumbnail": self.get_thumbnail(channel.get("thumbnail")),
            "subscribers": self.get_text(channel.get("subscriberCountText")),
            "videoCount": self.get_text(channel.get("videoCountText"))
        }
    
    def _parse_playlist_renderer(self, playlist: Dict) -> Dict:
        """Parse playlist renderer"""
        return {
            "type": "playlist",
            "playlistId": playlist.get("playlistId"),
            "title": self.get_text(playlist.get("title")),
            "thumbnail": self.get_thumbnail(
                {"thumbnails": playlist.get("thumbnails", [])}
            ),
            "videoCount": playlist.get("videoCount"),
            "channel": self.get_text(playlist.get("shortBylineText"))
        }
    
    def parse_video(self, player: Dict, next_data: Dict) -> Dict[str, Any]:
        """Parse video details"""
        video_details = player.get("videoDetails", {})
        streaming_data = player.get("streamingData", {})
        
        return {
            "videoId": video_details.get("videoId"),
            "title": video_details.get("title"),
            "description": video_details.get("shortDescription"),
            "duration": self.get_int(video_details.get("lengthSeconds")),
            "views": self.get_int(video_details.get("viewCount")),
            "author": video_details.get("author"),
            "channelId": video_details.get("channelId"),
            "thumbnail": self.get_thumbnail(video_details.get("thumbnail")),
            "isLive": video_details.get("isLiveContent", False),
            "isPrivate": video_details.get("isPrivate", False),
            "keywords": video_details.get("keywords", []),
            "category": video_details.get("category"),
            "hasStreams": bool(streaming_data.get("formats") or 
                              streaming_data.get("adaptiveFormats"))
        }
    
    def parse_related(self, data: Dict, limit: int = 20) -> Dict[str, Any]:
        """Parse related videos"""
        results = []
        
        contents = self.safe_get(
            data,
            "contents",
            "twoColumnWatchNextResults",
            "secondaryResults",
            "secondaryResults",
            "results",
            default=[]
        )
        
        for item in contents:
            if len(results) >= limit:
                break
            
            if "compactVideoRenderer" in item:
                video = item["compactVideoRenderer"]
                results.append({
                    "videoId": video.get("videoId"),
                    "title": self.get_text(video.get("title")),
                    "thumbnail": self.get_thumbnail(video.get("thumbnail")),
                    "duration": self.get_text(video.get("lengthText")),
                    "views": self.get_text(video.get("viewCountText")),
                    "channel": self.get_text(video.get("shortBylineText"))
                })
        
        return {"results": results}
    
    def parse_comments(self, data: Dict, limit: int = 20) -> Dict[str, Any]:
        """Parse comments"""
        # Comments parsing is complex, returning raw for now
        return {"raw": data, "note": "Comments parsing not implemented"}
    
    def parse_channel(self, data: Dict) -> Dict[str, Any]:
        """Parse channel data"""
        header = self.safe_get(data, "header", "c4TabbedHeaderRenderer", default={})
        metadata = self.safe_get(data, "metadata", "channelMetadataRenderer", default={})
        
        return {
            "channelId": header.get("channelId") or metadata.get("externalId"),
            "title": header.get("title") or metadata.get("title"),
            "description": metadata.get("description"),
            "thumbnail": self.get_thumbnail(header.get("avatar")),
            "banner": self.get_thumbnail(header.get("banner")),
            "subscribers": self.get_text(header.get("subscriberCountText")),
            "keywords": metadata.get("keywords"),
            "vanityUrl": metadata.get("vanityChannelUrl"),
            "isFamilySafe": metadata.get("isFamilySafe")
        }
    
    def parse_channel_videos(self, data: Dict, limit: int = 30) -> Dict[str, Any]:
        """Parse channel videos"""
        # Implementation depends on channel structure
        return {"raw": data}
    
    def parse_playlist(self, data: Dict) -> Dict[str, Any]:
        """Parse playlist data"""
        header = self.safe_get(data, "header", "playlistHeaderRenderer", default={})
        
        videos = []
        contents = self.safe_get(
            data,
            "contents",
            "twoColumnBrowseResultsRenderer",
            "tabs", 0,
            "tabRenderer",
            "content",
            "sectionListRenderer",
            "contents", 0,
            "itemSectionRenderer",
            "contents", 0,
            "playlistVideoListRenderer",
            "contents",
            default=[]
        )
        
        for item in contents:
            if "playlistVideoRenderer" in item:
                video = item["playlistVideoRenderer"]
                videos.append({
                    "videoId": video.get("videoId"),
                    "title": self.get_text(video.get("title")),
                    "thumbnail": self.get_thumbnail(video.get("thumbnail")),
                    "duration": self.get_text(video.get("lengthText")),
                    "channel": self.get_text(video.get("shortBylineText"))
                })
        
        return {
            "playlistId": header.get("playlistId"),
            "title": self.get_text(header.get("title")),
            "description": self.get_text(header.get("descriptionText")),
            "videoCount": self.safe_get(
                header, "numVideosText", "runs", 0, "text"
            ),
            "views": self.get_text(header.get("viewCountText")),
            "videos": videos
        }
    
    def parse_trending(self, data: Dict) -> Dict[str, Any]:
        """Parse trending data"""
        return {"raw": data}
