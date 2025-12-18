from pathlib import Path
from PIL import Image
import imagehash 

# Функція для обчислення phash
def compute_phash(path: Path):
    # Відкриваємо зображення і обчислюємо phash
    with Image.open(path) as img:
        return imagehash.phash(img)