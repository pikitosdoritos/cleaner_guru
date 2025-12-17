from pathlib import Path
from typing import Iterable
from PIL import Image
from .models import Photo
from .hashing import sha256_file

# Список підтримуваних розширень
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}

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

        #  Повертаємо результати, але по одному (щоб не вантажити пам'ять)
        yield Photo(
            path = str(path),
            size_bytes = size_bytes,
            width = width,
            height = height,
            sha256 = sha256
        )
        
        