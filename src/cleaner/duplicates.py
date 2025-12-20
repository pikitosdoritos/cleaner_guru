from collections import defaultdict
from typing import List
from .models import Photo

# Групуємо фото з однаковим хешем (в нашому випадку SHA-256) і знаходимо дублікати
def find_exact_duplicates(photos: List[Photo]):
    groups = defaultdict(list)
    # Проходимо по всіх фото. Додаєм їх у групи за хешем
    for photo in photos:
        if photo.sha256:
            groups[photo.sha256].append(photo)
    # Повертаємо лиш ті групи, де більше одного фото з однаковим SHA-256
    return [group for group in groups.values() if len(group) > 1]