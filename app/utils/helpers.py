from typing import Optional


def format_duration(seconds: Optional[int]) -> str:
    """Format duration from seconds to HH:MM:SS"""
    if not seconds:
        return "0:00"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def format_views(views: Optional[int]) -> str:
    """Format view count"""
    if not views:
        return "0"
    
    if views >= 1_000_000_000:
        return f"{views / 1_000_000_000:.1f}B"
    elif views >= 1_000_000:
        return f"{views / 1_000_000:.1f}M"
    elif views >= 1_000:
        return f"{views / 1_000:.1f}K"
    return str(views)


def extract_video_id(url: str) -> Optional[str]:
    """Extract video ID from YouTube URL"""
    import re
    
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None
