from fastapi import APIRouter, Query, Depends
from typing import Optional

from app.services.music import MusicService
from app.api.v1.schemas.common import APIResponse

router = APIRouter()


def get_music_service() -> MusicService:
    return MusicService()


@router.get("/search", response_model=APIResponse)
async def search_music(
    q: str = Query(..., description="Search query"),
    filter: Optional[str] = Query(
        None, 
        description="Filter: songs, videos, albums, artists, playlists"
    ),
    limit: int = Query(20, ge=1, le=50),
    service: MusicService = Depends(get_music_service)
):
    """
    Search YouTube Music
    
    - **q**: Search query
    - **filter**: Optional filter type
    """
    result = await service.search(q, filter, limit)
    return APIResponse(success=True, data=result)


@router.get("/song/{video_id}", response_model=APIResponse)
async def get_song(
    video_id: str,
    service: MusicService = Depends(get_music_service)
):
    """Get song details"""
    result = await service.get_song(video_id)
    return APIResponse(success=True, data=result)


@router.get("/song/{video_id}/lyrics", response_model=APIResponse)
async def get_lyrics(
    video_id: str,
    service: MusicService = Depends(get_music_service)
):
    """Get song lyrics"""
    result = await service.get_lyrics(video_id)
    return APIResponse(success=True, data=result)


@router.get("/song/{video_id}/related", response_model=APIResponse)
async def get_related_songs(
    video_id: str,
    limit: int = Query(20, ge=1, le=50),
    service: MusicService = Depends(get_music_service)
):
    """Get related songs (radio)"""
    result = await service.get_related(video_id, limit)
    return APIResponse(success=True, data=result)


@router.get("/album/{browse_id}", response_model=APIResponse)
async def get_album(
    browse_id: str,
    service: MusicService = Depends(get_music_service)
):
    """
    Get album details and tracks
    
    - **browse_id**: Album browse ID (starts with MPREb_)
    """
    result = await service.get_album(browse_id)
    return APIResponse(success=True, data=result)


@router.get("/artist/{channel_id}", response_model=APIResponse)
async def get_artist(
    channel_id: str,
    service: MusicService = Depends(get_music_service)
):
    """
    Get artist details
    
    - **channel_id**: Artist channel ID (starts with UC)
    """
    result = await service.get_artist(channel_id)
    return APIResponse(success=True, data=result)


@router.get("/artist/{channel_id}/albums", response_model=APIResponse)
async def get_artist_albums(
    channel_id: str,
    service: MusicService = Depends(get_music_service)
):
    """Get artist albums"""
    result = await service.get_artist_albums(channel_id)
    return APIResponse(success=True, data=result)


@router.get("/playlist/{playlist_id}", response_model=APIResponse)
async def get_playlist(
    playlist_id: str,
    service: MusicService = Depends(get_music_service)
):
    """Get music playlist"""
    result = await service.get_playlist(playlist_id)
    return APIResponse(success=True, data=result)


@router.get("/home", response_model=APIResponse)
async def get_home(
    service: MusicService = Depends(get_music_service)
):
    """Get YouTube Music home page content"""
    result = await service.get_home()
    return APIResponse(success=True, data=result)


@router.get("/charts", response_model=APIResponse)
async def get_charts(
    region: str = Query("US", description="Country code"),
    service: MusicService = Depends(get_music_service)
):
    """Get music charts"""
    result = await service.get_charts(region)
    return APIResponse(success=True, data=result)


@router.get("/moods", response_model=APIResponse)
async def get_moods(
    service: MusicService = Depends(get_music_service)
):
    """Get moods and genres"""
    result = await service.get_moods()
    return APIResponse(success=True, data=result)


@router.get("/new-releases", response_model=APIResponse)
async def get_new_releases(
    service: MusicService = Depends(get_music_service)
):
    """Get new album releases"""
    result = await service.get_new_releases()
    return APIResponse(success=True, data=result)
