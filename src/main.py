from pathlib import Path
from tqdm import tqdm
import json
from cleaner.scanner import scan_photos
from cleaner.duplicates import find_exact_duplicates
from cleaner.similar import find_similar_photos
from cleaner.burst import find_bursts

def main():
    # Знаходимо дирикторію з фотографіями і робимо її шлях абсолютним
    photos_dir = Path("photos").resolve()

    # Перевірка чи існує директорія, якщо ні то виводимо повідомлення (запобігання помилок)
    if not photos_dir.exists():
        print(f"\nPhotos directory {photos_dir} not found")
        return
    
    photos = []

    # Проходимо по всіх фото і обгортаємо в прогрес бар
    for photo in tqdm(scan_photos(photos_dir), desc = "Scanning photos..."):
        photos.append(photo)

    duplicate_groups = find_exact_duplicates(photos)
    similar_groups = find_similar_photos(photos)
    burst_groups = find_bursts(photos)

    # Виводимо результат
    print("\nReady!")
    print(f"Found {len(photos)} photos")
    print(f"Found {len(duplicate_groups)} duplicate groups")
    print(f"Groups with similar photos: {len(similar_groups)}")
    burst_group_count = len(burst_groups)
    burst_photo_count = sum(len(g) for g in burst_groups)
    print(
        f"Burst groups: {burst_group_count} "
        f"({burst_photo_count} photos total)"
        )



    # Створили список для зберження результатів
    result = []

    # Проходимо по всіх групах
    for dup_group in duplicate_groups:
        # Сортуємо групу за розміром
        sorted_group = sorted(dup_group, key = lambda p: p.size_bytes, reverse = True)
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


    for sim_group in similar_groups:
        sorted_group = sorted(sim_group, key = lambda f: f.size_bytes, reverse = True)
        keep = sorted_group[0].path
        delete = [p.path for p in sorted_group[1:]]

        result.append({
    "type": "similar_photos",
    "keep": keep,
    "suggest_delete": delete,
    "count": len(sorted_group)
    })
        
    for burst in burst_groups:
        sorted_group = sorted(burst, key = lambda p: p.size_bytes, reverse = True)
        keep = sorted_group[0].path
        delete = [p.path for p in sorted_group[1:]]

        result.append({
        "type": "burst_photos",
        "keep": keep,
        "suggest_delete": delete,
        "count": len(sorted_group)
    })

    # Зберігаємо результат у JSON-файл в форматі utf-8
    with open("result.json", "w", encoding = "utf-8") as f:
        json.dump(result, f, indent = 2, ensure_ascii = False)

    print("Result saved to result.json")

if __name__ =="__main__":
    main()