from typing import List
from .models import Photo

def quality_score(photo: Photo) -> float:
    score = 0.0
    
    if photo.blur is not None:
        score += min(photo.blur / 100.0, 3.0) * 2.0
        
    if photo.width and photo.height:
        megapixels = (photo.width * photo.height) / 1_000_000
        score += min(megapixels, 12.0) * 0.5
        
    score += min(photo.size_bytes / (5 * 1024 * 1024), 3.0)
    
    return score

def rank_photos(photos: List[Photo]) -> List[Photo]:
    return sorted(
        photos, 
        key = quality_score, 
        reverse = True
)