from typing import List
from .models import Photo
import statistics

def find_large_photos(
    photos: List[Photo],
    precentile: float = 90
) -> List[Photo]:
    sizes = [p.size_bytes for p in photos if p.size_bytes]
    
    if not sizes:
        return []

    threshold = statistics.quantiles(sizes, n = 100)[int(precentile) - 1]
    
    large_photos = [
        p for p in photos
        if p.size_bytes >= threshold
    ]
    
    return large_photos