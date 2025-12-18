from pathlib import Path
from tqdm import tqdm
import json
from cleaner.scanner import scan_photos
from cleaner.duplicates import find_exact_duplicates

def main():
    # Знаходимо дирикторію з фотографіями і робимо її шлях абсолютним
    photos_dir = Path("photos").resolve()

    # Перевірка чи існує директорія, якщо ні то виводимо повідомлення (запобігання помилок)
    if not photos_dir.exists():
        print(f"\nPhotos directory {photos_dir} not found")
        return
    
    photos = []

    # Проходимо по всіх фото і обгортаємо в прогрес бар
    for photo in tqdm(scan_photos(photos_dir), desc = "Scaning photos..."):
        photos.append(photo)

    duplicate_groups = find_exact_duplicates(photos)

    # Виводимо результат
    print("\nReady!")
    print(f"Found {len(photos)} photos")
    print(f"Found {len(duplicate_groups)} duplicate groups")

    # Створили список для зберження результатів
    result = []

    # Проходимо по всіх групах
    for group in duplicate_groups:
        # Сортуємо групу за розміром
        sorted_group = sorted(group, key = lambda p: p.size_bytes, reverse = True)
        # Залишаємо найбільшу по розміру фотографію
        keep = sorted_group[0].path
        # Видаляємо всі крім першої
        delete = [p.path for p in sorted_group[1:]]

        result.append({
            "type": "exact_duplicates",
            "keep": keep,
            "suggest_delete": delete,
            "count": len(sorted_group)
        })

        # Зберігаємо результат у JSON-файл в форматі utf-8
        with open("result.json", "w", encoding = "utf-8") as f:
            json.dump(result, f, indent = 2, ensure_ascii = False)

        print("Результат збережено у result.json")

if __name__ =="__main__":
    main()