from pydantic import BaseModel
from typing import Optional, List
from app.api.v1.schemas.common import Thumbnail


class VideoResponse(BaseModel):
    """Video response model"""
    video_id: str
    title: str
    description: Optional[str] = None
    duration: Optional[int] = None
    views: Optional[int] = None
    likes: Optional[int] = None
    author: Optional[str] = None
    channel_id: Optional[str] = None
    thumbnail: Optional[str] = None
    thumbnails: Optional[List[Thumbnail]] = None
    is_live: bool = False
    keywords: Optional[List[str]] = None
    published: Optional[str] = None


class ChannelResponse(BaseModel):
    """Channel response model"""
    channel_id: str
    title: str
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    banner: Optional[str] = None
    subscribers: Optional[str] = None
    video_count: Optional[int] = None


class PlaylistResponse(BaseModel):
    """Playlist response model"""
    playlist_id: str
    title: str
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    video_count: Optional[int] = None
    author: Optional[str] = None
    videos: Optional[List[VideoResponse]] = None


class SearchResult(BaseModel):
    """Search result item"""
    type: str  # video, channel, playlist
    id: str
    title: str
    thumbnail: Optional[str] = None
    description: Optional[str] = None


class SearchResponse(BaseModel):
    """Search response model"""
    query: str
    results: List[SearchResult]
    continuation: Optional[str] = None
