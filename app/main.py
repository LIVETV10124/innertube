from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time

from app.config import settings
from app.api.v1.router import api_router
from app.core.exceptions import APIException
from app.core.middleware import LoggingMiddleware, RateLimitMiddleware
from app.core.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    setup_logging()
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    yield
    # Shutdown
    print(f"👋 Shutting down {settings.APP_NAME}")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
    ## YouTube & YouTube Music API
    
    Unofficial API for YouTube and YouTube Music using InnerTube.
    
    ### Features
    - 🔍 Search videos, songs, albums, artists, playlists
    - 🎵 Get audio/video streaming URLs
    - 📝 Fetch lyrics
    - 📊 Get trending and charts
    - 💾 Built-in caching
    
    ### Rate Limits
    - 60 requests per minute per IP
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)

# Exception handlers
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": str(exc) if settings.DEBUG else None
            }
        }
    )

# Include routers
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Root endpoints
@app.get("/", tags=["Root"])
async def root():
    """API root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "documentation": "/docs",
        "health": "/health",
        "endpoints": {
            "youtube": f"{settings.API_V1_PREFIX}/youtube",
            "music": f"{settings.API_V1_PREFIX}/music"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": settings.APP_VERSION
    }
