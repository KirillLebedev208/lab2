import os
import stat
from datetime import datetime
from PIL import Image, ImageFilter, ImageOps
def logs(filename, filtername, status):
    log_path = os.path.join("Lab2_Media", "logs", "history.txt")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{now}] Файл: {filename}| Фильтр{filtername}| Статус: {status}\n"
    with open(log_path, "a", encoding = "UTF-8") as log_file:
        log_file.write(log_line)
def main():
    filename = input("Введите имя файла для обработки")
    input_path = os.path.join("Lab2_Media", "data", "input", filename)
    output_path = os.path.join("Lab2_Media", "data", "output", "result.jpg")
    filtername = "Повышение резкости + Автоконтраст"
    try:
        file_attrs = os.stat(input_path).st_file_attributes
        if file_attrs & stat.FILE_ATTRIBUTE_READONLY:
            raise PermissionError("Файл защищён от записи")
        img = Image.open(input_path)
        img = img.filter(ImageFilter.UnsharpMask(radius = 5, percent = 200, threshold = 5))
        img = ImageOps.autocontrast(img)
        img.convert('RGB').save(output_path, "JPEG")
        print(f"Изображение обработано и сохранено в:{output_path}")
        logs(filename, filtername, "Успешно")
    except PermissionError:
        print(f"Ошибка: Нет прав на чтение файла {filename}. Обратитесь к администратору")
        logs(filename, filtername, "Ошибка доступа")
    except FileNotFoundError:
        print("Файл не найден")
        logs (filename, "None", "Ошибка: Файл не найден")
    except Exception as e:
        print (f"Произошла непредвиденная ошибка: {e}")
        logs(filename, filtername, f"Ошибка: {e}")

main()
