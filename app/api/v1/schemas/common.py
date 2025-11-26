from pydantic import BaseModel
from typing import Optional, Any, Dict, List
from datetime import datetime


class APIResponse(BaseModel):
    """Standard API response"""
    success: bool
    data: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None
    meta: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {"key": "value"},
                "meta": {"cached": False, "timestamp": "2024-01-01T00:00:00Z"}
            }
        }


class PaginatedResponse(BaseModel):
    """Paginated response"""
    items: List[Any]
    total: Optional[int] = None
    continuation: Optional[str] = None
    has_more: bool = False


class Thumbnail(BaseModel):
    """Thumbnail model"""
    url: str
    width: Optional[int] = None
    height: Optional[int] = None


class ErrorDetail(BaseModel):
    """Error detail model"""
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None
