from fastapi import APIRouter, Query, Depends
from typing import Optional

from app.services.youtube import YouTubeService
from app.services.music import MusicService
from app.api.v1.schemas.common import APIResponse

router = APIRouter()


@router.get("/suggestions", response_model=APIResponse)
async def get_suggestions(
    q: str = Query(..., description="Query for suggestions"),
    type: str = Query("youtube", description="Type: youtube, music")
):
    """Get search suggestions"""
    import httpx
    
    if type == "music":
        url = "https://music.youtube.com/youtubei/v1/music/get_search_suggestions"
    else:
        url = "https://suggestqueries-clients6.youtube.com/complete/search"
        params = {"client": "youtube", "q": q, "ds": "yt"}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            return APIResponse(success=True, data={"raw": response.text})
    
    return APIResponse(success=True, data={"query": q})


@router.get("/combined", response_model=APIResponse)
async def combined_search(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=20)
):
    """Search both YouTube and YouTube Music"""
    yt_service = YouTubeService()
    music_service = MusicService()
    
    yt_results = await yt_service.search(q, None, limit)
    music_results = await music_service.search(q, None, limit)
    
    return APIResponse(
        success=True,
        data={
            "youtube": yt_results,
            "music": music_results
        }
    )
