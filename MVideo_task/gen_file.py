import csv
import random
import codecs
num_rows = 1000  # Количество строк (данных) для генерации
filename = r"C:\Users\Credu\Downloads\Статистика1.csv"

with codecs.open(filename, mode="w", encoding="utf-8", errors="ignore") as file:
    writer = csv.writer(file)
    writer.writerow(["Количество больничных дней", "Возраст", "Пол"])  # Записываем заголовки столбцо

    for _ in range(num_rows):
        sick_days = random.randint(1, 9)  # Генерируем случайное количество больничных дней от 1 до 5
        age = random.randint(18, 65)  # Генерируем случайный возраст от 20 до 60
        gender = random.choice(["М", "Ж"])  # Генерируем случайный пол (М или Ж)

        writer.writerow([sick_days, age, gender])  # Записываем сгенерированную строку данных

print(f"Файл {filename} успешно создан.")