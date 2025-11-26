from fastapi import APIRouter, Query, Depends
from typing import Optional

from app.services.youtube import YouTubeService
from app.api.v1.schemas.youtube import (
    VideoResponse,
    ChannelResponse,
    PlaylistResponse,
    SearchResponse
)
from app.api.v1.schemas.common import APIResponse

router = APIRouter()


def get_youtube_service() -> YouTubeService:
    return YouTubeService()


@router.get("/video/{video_id}", response_model=APIResponse)
async def get_video(
    video_id: str,
    service: YouTubeService = Depends(get_youtube_service)
):
    """
    Get video details
    
    - **video_id**: YouTube video ID (e.g., dQw4w9WgXcQ)
    """
    result = await service.get_video(video_id)
    return APIResponse(success=True, data=result)


@router.get("/video/{video_id}/related", response_model=APIResponse)
async def get_related_videos(
    video_id: str,
    limit: int = Query(20, ge=1, le=50),
    service: YouTubeService = Depends(get_youtube_service)
):
    """Get related videos"""
    result = await service.get_related(video_id, limit)
    return APIResponse(success=True, data=result)


@router.get("/video/{video_id}/comments", response_model=APIResponse)
async def get_comments(
    video_id: str,
    limit: int = Query(20, ge=1, le=100),
    service: YouTubeService = Depends(get_youtube_service)
):
    """Get video comments"""
    result = await service.get_comments(video_id, limit)
    return APIResponse(success=True, data=result)


@router.get("/channel/{channel_id}", response_model=APIResponse)
async def get_channel(
    channel_id: str,
    service: YouTubeService = Depends(get_youtube_service)
):
    """
    Get channel details
    
    - **channel_id**: YouTube channel ID (e.g., UCuAXFkgsw1L7xaCfnd5JJOw)
    """
    result = await service.get_channel(channel_id)
    return APIResponse(success=True, data=result)


@router.get("/channel/{channel_id}/videos", response_model=APIResponse)
async def get_channel_videos(
    channel_id: str,
    limit: int = Query(30, ge=1, le=50),
    service: YouTubeService = Depends(get_youtube_service)
):
    """Get channel videos"""
    result = await service.get_channel_videos(channel_id, limit)
    return APIResponse(success=True, data=result)


@router.get("/playlist/{playlist_id}", response_model=APIResponse)
async def get_playlist(
    playlist_id: str,
    service: YouTubeService = Depends(get_youtube_service)
):
    """
    Get playlist details and videos
    
    - **playlist_id**: YouTube playlist ID
    """
    result = await service.get_playlist(playlist_id)
    return APIResponse(success=True, data=result)


@router.get("/trending", response_model=APIResponse)
async def get_trending(
    region: str = Query("US", description="Country code"),
    category: Optional[str] = Query(None, description="Category: music, gaming, movies"),
    service: YouTubeService = Depends(get_youtube_service)
):
    """Get trending videos"""
    result = await service.get_trending(region, category)
    return APIResponse(success=True, data=result)


@router.get("/search", response_model=APIResponse)
async def search_youtube(
    q: str = Query(..., description="Search query"),
    filter: Optional[str] = Query(None, description="Filter: video, channel, playlist"),
    limit: int = Query(20, ge=1, le=50),
    service: YouTubeService = Depends(get_youtube_service)
):
    """Search YouTube"""
    result = await service.search(q, filter, limit)
    return APIResponse(success=True, data=result)
