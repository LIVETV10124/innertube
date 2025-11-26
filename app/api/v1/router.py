from fastapi import APIRouter

from app.api.v1.endpoints import youtube, music, stream, search

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(
    youtube.router,
    prefix="/youtube",
    tags=["YouTube"]
)

api_router.include_router(
    music.router,
    prefix="/music",
    tags=["YouTube Music"]
)

api_router.include_router(
    stream.router,
    prefix="/stream",
    tags=["Streaming"]
)

api_router.include_router(
    search.router,
    prefix="/search",
    tags=["Search"]
)
