from pathlib import Path
from tqdm import tqdm
from cleaner.scanner import scan_photos

def main():
    # Знаходимо дирикторію з фотографіями і робимо її шлях абсолютним
    photos_dir = Path("photos").resolve()

    # Перевірка чи існує директорія, якщо ні то виводимо повідомлення (запобігання помилок)
    if not photos_dir.exists():
        print(f"\nPhotos directory {photos_dir} not found")
        return
    
    # Створюємо лічильники в які будуть записуватись результати(кількість знайдених фото, сумарни1 розмір усіх фото)
    count = 0
    total_bytes = 0

    # Проходимо по всіх фото і обгортаємо в прогрес бар
    for photo in tqdm(scan_photos(photos_dir), desc = "Scaning photos..."):
        count += 1
        total_bytes += photo.size_bytes

    # Виводимо результат
    print("\nReady!")
    print(f"Found {count} photos with total size {total_bytes / (1024 ** 3): .2f} GB")

if __name__ =="__main__":
    main()