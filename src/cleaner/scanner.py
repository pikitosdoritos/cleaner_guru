from pathlib import Path
from typing import Optional
from typing import Iterable
from PIL import Image
from datetime import datetime
from .models import Photo
from .hashing import sha256_file
from .phash import compute_phash

# Список підтримуваних розширень
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}
# Функція для витягування дати та часу з EXIF
def extract_timestamp(path: Path) -> Optional[datetime]:
    try:
        with Image.open(path) as img:
            exif = img._getexif()

            if not exif:
                return None

            dt = exif.get(36867)

            if not dt:
                return None

            return datetime.strptime(dt, "%Y:%m:%d %H:%M:%S")
    except Exception:
        return None

def scan_photos(folder: Path) -> Iterable[Photo]:
    # Generator - буде повертати фото по одному
    for path in folder.rglob("*"):
        # Перевірка чи це файл
        if not path.is_file():
            continue
        # Перевірка чи це фото
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        # Дістаємо вагу файлу
        size_bytes = path.stat().st_size

        timestamp = extract_timestamp(path)

        if timestamp is None:
            timestamp = datetime.fromtimestamp(path.stat().st_mtime)
        # Дістаємо розміри (одразу захищаємося від помилок)
        try:
            with Image.open(path) as img:
                width, height = img.size
        except Exception:
            width, height = None, None
        #  Дістаємо хеш (одразу захищаємося від помилок)
        try:
            sha256 = sha256_file(path)
        except Exception:
            sha256 = None
        #  Дістаємо phash (одразу захищаємося від помилок)
        try:
            phash = str(compute_phash(path))
        except Exception:
            phash = None
        #  Повертаємо результати, але по одному (щоб не вантажити пам'ять)
        yield Photo(
            path = str(path),
            size_bytes = size_bytes,
            width = width,
            height = height,
            sha256 = sha256,
            phash = phash,
            timestamp = timestamp
        )
        
        