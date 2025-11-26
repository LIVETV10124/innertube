from pydantic import BaseModel
from typing import Optional, List


class SongResponse(BaseModel):
    """Song response model"""
    video_id: str
    title: str
    artist: Optional[str] = None
    album: Optional[str] = None
    duration: Optional[int] = None
    thumbnail: Optional[str] = None
    is_explicit: bool = False


class AlbumResponse(BaseModel):
    """Album response model"""
    browse_id: str
    title: str
    artist: Optional[str] = None
    year: Optional[str] = None
    thumbnail: Optional[str] = None
    track_count: Optional[int] = None
    tracks: Optional[List[SongResponse]] = None


class ArtistResponse(BaseModel):
    """Artist response model"""
    channel_id: str
    name: str
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    subscribers: Optional[str] = None


class LyricsResponse(BaseModel):
    """Lyrics response model"""
    lyrics: Optional[str] = None
    source: Optional[str] = None


class StreamResponse(BaseModel):
    """Stream response model"""
    url: str
    mime_type: str
    bitrate: int
    quality: str
    itag: int
