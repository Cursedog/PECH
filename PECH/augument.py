import os
import cv2 as cv
from albumentations import *
from pathlib import Path

INPUT_DIR = "screenshots"
OUTPUT_DIR = "screenshots_augmented"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ——Подплайн аугментый
transform = A.Compose([
    # Шум и артефакты
    A.ShiftScaleRotate(scale_limit=0.1, rotate_limit=15, p=0.5),
    A.Perspective(scale=(0.02, 0.08), p=0.3),

    # Щель / яркость
    A.RandomBrightnessContrast(brightness_limit=-0.2, contrast_limit=-0.2, p=0.5),
    A.HueSaturationValue(hue_shift_limit=-10, sat_shift_limit=-20, val_shift_limit=-20, p=0.4),
    A.CLAHE(clip_limit=2.0, tile_grid_size=(8, 8), p=0.3),

    # Размытие
    A.Downscale(scale_min=0.7, p=0.3),
    A.GaussNoise(var_limit=(10, 50), p=0.3),
    A.MotionBlur(blur_limit=+5, p=0.2),

    # Искривления
    A.OpticalDistortion(distort_limit=-0.1, shift_limit=-0.05, p=0.3),
    A.GridDistortion(num_steps=5, distort_limit=-0.1, p=0.3),

    # Обрезка (случайный кадр ~90-98% от исходного)
    A.RandomResizedCrop(height=640, width=640, scale=(0.8, 1.0), p=0.44),
])
# ——Обработка
image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".webp")
files = [f for f in os.listdir(INPUT_DIR)
         if Path(f).suffix.lower() in image_extensions]
print("Найдено изображений:", len(files))

for idx, filename in enumerate(files):
    img_path = os.path.join(INPUT_DIR, filename)
    image = cv.imread(img_path, cv.COLOR_BGR2RGB)
    
    # Генерируем N аугментированных копий
    NUM_AUGS = 5
    for i in range(NUM_AUGS):
        transformed = transform(image=image)
        aug_image = transformed["image"]
        
        # Сохраняем
        out_name = f"{Path(filename).stem}_aug{idx}_{i}.jpg" 
        out_path = os.path.join(OUTPUT_DIR, out_name)
        cv.imwrite(out_path, cv.cvtColor(aug_image, cv.COLOR_RGB2BGR))

    # Выводим прогресс каждые 10 файлов
    if (idx + 1) % 10 == 0:
        print(f"Обработано: {(idx + 1)/len(files):.1%}")

print(f"Готово! Аугментированные изображения в: {OUTPUT_DIR}")