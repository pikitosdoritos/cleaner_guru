from typing import List
from .models import Photo
import imagehash

# Порогове значення для порівняння phash
PHASH_THRESHOLD = 6

def find_similar_photos(photos: List[Photo]):
    # Створюємо список для зберігання груп і множини використаних фото
    groups = []
    used = set()
    # Проходимо по всіх фото
    for i, p1 in enumerate(photos):
        # Пропускаємо ті, які вже були використані або не мають phash
        if p1.path in used or not p1.phash:
            continue
        # Створюємо групу і використовуємо множину для зберігання використаних фото
        group = [p1]
        used.add(p1.path)
        # Перетворення pHash зі строки в обʼєкт
        h1 = imagehash.hex_to_hash(p1.phash)
        # Проходимо по всіх фото після поточного
        for p2 in photos[i + 1:]:
            # Пропускаємо ті, які вже були використані або не мають phash
            if p2.path in used or not p2.phash:
                continue
            # Перетворення pHash зі строки в обʼєкт
            h2 = imagehash.hex_to_hash(p2.phash)
            # Обчислюємо відстань між фотографіями за phash (покаже різницю між фотографіями)
            distance = h1 - h2   
            # Перевірка чи відстань між фотографіями менша за поріг
            if distance <= PHASH_THRESHOLD:
                group.append(p2)
                used.add(p2.path)

        if len(group) > 1:
            groups.append(group)

    return groups