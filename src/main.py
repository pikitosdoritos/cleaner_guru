from pathlib import Path
from tqdm import tqdm
import json
from cleaner.scanner import scan_photos
from cleaner.duplicates import find_exact_duplicates
from cleaner.similar import find_similar_photos
from cleaner.burst import find_bursts
from cleaner.quality import find_blurry_photos
from cleaner.large import find_large_photos
from cleaner.dark import find_dark_photos
from cleaner.screenshots import find_screenshots
from cleaner.ranking import rank_photos

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
    burst_group_count = len(burst_groups)
    burst_photo_count = sum(len(g) for g in burst_groups)
    blurry_photos = find_blurry_photos(photos)
    large_photos = find_large_photos(photos)
    dark_photos = find_dark_photos(photos)
    screenshots = find_screenshots(photos)

    # Виводимо результат
    print("\nReady!")
    print(f"Found {len(photos)} photos")
    print(f"Found {len(duplicate_groups)} duplicate groups")
    print(f"Groups with similar photos: {len(similar_groups)}")
    print(
        f"Burst groups: {burst_group_count} "
        f"({burst_photo_count} photos total)"
        )
    print(f"Blurry photos: {len(blurry_photos)}")
    print(f"Large photos: {len(large_photos)}")
    print(f"Dark photos: {len(dark_photos)}")
    print(f"Screenshots / messenger images: {len(screenshots)}")

    # Створили список для зберження результатів
    result = []

    # Проходимо по всіх групах
    for dup_group in duplicate_groups:
        # Сортуємо групу за розміром
        ranked = rank_photos(dup_group)
        # Залишаємо найбільшу по розміру фотографію
        keep = ranked[0].path
        # Видаляємо всі крім першої
        delete = [p.path for p in ranked[1:]]
        
        result.append({
            "type": "exact_duplicates",
            "keep": keep,
            "suggest_delete": delete,
            "count": len(ranked)
        })


    for sim_group in similar_groups:
        ranked = rank_photos(sim_group)
        keep = ranked[0].path
        delete = [p.path for p in ranked[1:]]

        result.append({
    "type": "similar_photos",
    "keep": keep,
    "suggest_delete": delete,
    "count": len(ranked)
    })
        
    for burst in burst_groups:
        ranked = rank_photos(burst)
        keep = ranked[0].path
        delete = [p.path for p in ranked[1:]]

        result.append({
        "type": "burst_photos",
        "keep": keep,
        "suggest_delete": delete,
        "count": len(ranked)
    })

    for p in blurry_photos:
        result.append({
            "type": "blurry_photo",
            "path": p.path,
            "blur_score": round(p.blur, 2)
        })
        
    for p in large_photos:
        result.append({
            "type": "large_photo",
            "path": p.path,
            "size_mb": round(p.size_bytes / (1024 * 1024), 2)
    })
        
    for p in dark_photos:
        result.append({
            "type": "dark_photo",
            "path":p.path
        })
        
    for p in screenshots:
        result.append({
            "type": "screenshots",
            "path": p.path,
            "suggest_action": "archive"
        })

    # Зберігаємо результат у JSON-файл в форматі utf-8
    with open("result.json", "w", encoding = "utf-8") as f:
        json.dump(result, f, indent = 2, ensure_ascii = False)

    print("Result saved to result.json")

if __name__ =="__main__":
    main()