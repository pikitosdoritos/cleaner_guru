from typing import List
from .models import Photo
import cv2
import numpy as np

DARK_THRESHOLD = 40

def find_dark_photos(photos: List[Photo]) -> List[Photo]:
    dark_photos = []

    for p in photos:
        try:
            img = cv2.imread(p.path)
            
            if img is None:
                continue

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            brightness = float(np.mean(gray))

            if brightness < DARK_THRESHOLD:
                dark_photos.append(p)

        except Exception:
            continue

    return dark_photos
