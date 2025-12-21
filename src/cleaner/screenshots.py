from typing import List
from .models import Photo

KEYWORDS = [
    "screenshot", "screen",
    "telegram", "whatsapp",
    "viber", "signal",
    "snapchat"
]

ASPECT_RATIO_THRESHOLD = 1.6

def is_screenshot(photo: Photo) -> bool:
    name = photo.path.lower()
    
    if any(k in name for k in KEYWORDS):
        return True
    
    if photo.width and photo.height:
        ratio = photo.height / photo.width
        
        if ratio >= ASPECT_RATIO_THRESHOLD:
            return True
        
    return False

def find_screenshots(photos: List[Photo]) -> List[Photo]:
    return [p for p in photos if is_screenshot(p)]