from fastapi import APIRouter, Query, Depends
from fastapi.responses import RedirectResponse
from typing import Optional

from app.services.stream import StreamService
from app.api.v1.schemas.common import APIResponse

router = APIRouter()


def get_stream_service() -> StreamService:
    return StreamService()


@router.get("/{video_id}", response_model=APIResponse)
async def get_streams(
    video_id: str,
    service: StreamService = Depends(get_stream_service)
):
    """
    Get all available streams for a video
    
    Returns both video and audio streams with URLs
    """
    result = await service.get_streams(video_id)
    return APIResponse(success=True, data=result)


@router.get("/{video_id}/audio", response_model=APIResponse)
async def get_audio_stream(
    video_id: str,
    quality: str = Query("best", description="Quality: best, medium, low"),
    service: StreamService = Depends(get_stream_service)
):
    """Get audio-only stream"""
    result = await service.get_audio_stream(video_id, quality)
    return APIResponse(success=True, data=result)


@router.get("/{video_id}/video", response_model=APIResponse)
async def get_video_stream(
    video_id: str,
    quality: str = Query("best", description="Quality: 1080p, 720p, 480p, 360p"),
    service: StreamService = Depends(get_stream_service)
):
    """Get video stream"""
    result = await service.get_video_stream(video_id, quality)
    return APIResponse(success=True, data=result)


@router.get("/{video_id}/audio/redirect")
async def redirect_audio(
    video_id: str,
    quality: str = Query("best"),
    service: StreamService = Depends(get_stream_service)
):
    """Redirect to audio stream URL"""
    result = await service.get_audio_stream(video_id, quality)
    if result and result.get("url"):
        return RedirectResponse(url=result["url"])
    return APIResponse(success=False, error="Stream not found")


@router.get("/{video_id}/formats", response_model=APIResponse)
async def get_formats(
    video_id: str,
    service: StreamService = Depends(get_stream_service)
):
    """Get available formats/qualities"""
    result = await service.get_formats(video_id)
    return APIResponse(success=True, data=result)
