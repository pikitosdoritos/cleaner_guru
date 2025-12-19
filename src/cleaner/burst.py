from typing import List
from datetime import timedelta
from .models import Photo

BURST_DELTA = timedelta(seconds = 2)
MIN_BURST_SIZE = 3

def find_bursts(photos: List[Photo]):
    photos = [p for p in photos if p.timestamp is not None]
    photos.sort(key = lambda p: p.timestamp)

    bursts = []
    current = []

    for photo in photos:
        if not current:
            current = [photo]
            continue

        if photo.timestamp - current[-1].timestamp <= BURST_DELTA:
            current.append(photo)
        else:
            if len(current) >= MIN_BURST_SIZE:
                bursts.append(current)
            current = [photo]

    if len(current) >= MIN_BURST_SIZE:
        bursts.append(current)

    return bursts