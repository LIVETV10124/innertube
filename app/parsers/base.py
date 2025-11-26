from typing import Optional, Dict, Any, List


class BaseParser:
    """Base parser with common utilities"""
    
    @staticmethod
    def get_text(obj: Optional[Dict]) -> str:
        """Extract text from YouTube text object"""
        if not obj:
            return ""
        if isinstance(obj, str):
            return obj
        if "simpleText" in obj:
            return obj["simpleText"]
        if "runs" in obj:
            return "".join(run.get("text", "") for run in obj["runs"])
        return ""
    
    @staticmethod
    def get_thumbnail(obj: Optional[Dict], size: str = "high") -> str:
        """Extract thumbnail URL"""
        if not obj:
            return ""
        
        thumbnails = obj.get("thumbnails", [])
        if not thumbnails:
            # Try nested structure
            thumbnails = obj.get("thumbnail", {}).get("thumbnails", [])
        if not thumbnails:
            thumbnails = obj.get("musicThumbnailRenderer", {}).get(
                "thumbnail", {}
            ).get("thumbnails", [])
        
        if not thumbnails:
            return ""
        
        if size == "high":
            return thumbnails[-1].get("url", "")
        elif size == "low":
            return thumbnails[0].get("url", "")
        else:
            mid = len(thumbnails) // 2
            return thumbnails[mid].get("url", "")
    
    @staticmethod
    def get_int(value: Any) -> Optional[int]:
        """Safely convert to int"""
        if value is None:
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            # Remove commas and non-numeric chars
            cleaned = ''.join(c for c in value if c.isdigit())
            return int(cleaned) if cleaned else None
        return None
    
    @staticmethod
    def safe_get(obj: Dict, *keys, default=None):
        """Safely get nested dict values"""
        for key in keys:
            if isinstance(obj, dict):
                obj = obj.get(key, default)
            elif isinstance(obj, list) and isinstance(key, int):
                obj = obj[key] if len(obj) > key else default
            else:
                return default
        return obj
