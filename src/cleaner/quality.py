from pathlib import Path
import cv2

BLUR_THRESHOLD = 100.0

def blur_score(path: Path) -> float | None:
    try:
        image = cv2.imread(str(path))
        
        if image is None:
            return None
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        score = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        return float(score)
    
    except Exception:
        return None
    
def find_blurry_photos(photos):
    return [
        p for p in photos
        if p.blur is not None and p.blur < BLUR_THRESHOLD
    ]