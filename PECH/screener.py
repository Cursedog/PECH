import pyautogui
import time
from datetime import datetime
import os

# Папка для сохранения скриншотов
save_dir = "screenshots"
os.makedirs(save_dir, exist_ok=True)

print("Начальная дата скриптов каждый 5 секудн.")
print("Нажмите ctrl+c для остановки!")
count = 0

try:
    while True:
        # Делаем снимок
        screenshot = pyautogui.screenshot()
        
        # Формируем имя файла с датой и временем
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = f"{save_dir}/screenshot-{timestamp}.png"
        
        # Сохраняем
        screenshot.save(filename)
        count += 1
        
        print(f"[{count}] Сохранено: {filename}")
        
        # Ждем 5 секунд
        time.sleep(5)
except KeyboardInterrupt:
    print(f"\nРабота завершена. Всего сделано скринов: {count}")