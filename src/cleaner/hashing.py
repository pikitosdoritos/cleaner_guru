import hashlib
from pathlib import Path

# Створюємо функцію для обчислення хеша. Файл читається частинами, щоб не вантажити памʼять.
def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    hasher = hashlib.sha256()

    # Зчитуємо файли частинами 
    with path.open("rb") as f:
        # Проходимо по всіх  частинами
        while True:
            # Читаємо частину
            chunk = f.read(chunk_size)
            # Якщо частина порожня, закінчуємо
            if not chunk:
                break
            hasher.update(chunk)
    # Повертаємо хеш переведений у hex-рядок
    return hasher.hexdigest()