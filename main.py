import time
import pyautogui
from PIL import Image
import easyocr
import numpy as np
import re

# Настройка области экрана, где отображается выражение.
# Координаты должны быть настроены под конкретное окно игры в Telegram.
EXPRESSION_REGION = (769, 522, 382, 67)

# Настройка координат для клика по вариантам ответа (1, 2, 3).
# Эти координаты должны соответствовать кнопкам в игре.
DOT_COORDINATES = {
    1: (957, 608),  # координаты для кнопки "1"
    2: (957, 658),  # координаты для кнопки "2"
    3: (957, 708)   # координаты для кнопки "3"
}

# Инициализация EasyOCR (если выражение на русском, можно использовать ['ru'])
reader = easyocr.Reader(['en'], gpu=False)


def capture_expression():
    """
    Делает скриншот заданной области экрана.
    """
    screenshot = pyautogui.screenshot(region=EXPRESSION_REGION)
    return screenshot


def extract_expression(image):
    """
    Распознаёт текст на изображении с помощью EasyOCR.
    Возвращает первую найденную строку.
    """
    image_np = np.array(image)
    results = reader.readtext(image_np, detail=0)
    if results:
        expression = results[0].strip()
        print("Распознано выражение:", expression)
        return expression
    else:
        print("Текст не распознан.")
        return ''


def parse_and_evaluate(expression_text):
    """
    Очищает строку выражения, оставляя только цифры, операторы и скобки,
    затем вычисляет выражение.
    """
    # Удаляем пробелы
    expr = expression_text.replace(" ", "")
    # Если найден символ '=', берём всё до него
    if '=' in expr:
        expr = expr.split('=')[0]
    # Оставляем только допустимые символы (цифры, точки, операторы, скобки)
    expr = re.sub(r'[^0-9+\-*/().]', '', expr)

    # Удаляем завершающие операторы или незакрывающие скобки
    while expr and expr[-1] in "+-*/(":
        expr = expr[:-1]

    print("Очищенное выражение для вычисления:", expr)

    try:
        # Вычисление выражения (eval используйте только с доверенными данными)
        result = eval(expr)
        print("Вычисленный результат:", result)
        return result
    except Exception as e:
        print("Ошибка при вычислении выражения:", e)
        return None


def click_result(result):
    """
    В зависимости от результата (1, 2 или 3) имитирует клик по соответствующей кнопке.
    """
    if result in DOT_COORDINATES:
        x, y = DOT_COORDINATES[result]
        pyautogui.click(x, y)
        print(f"Нажата кнопка для результата {result} по координатам ({x}, {y})")
    else:
        print("Результат не равен 1, 2 или 3. Клик не выполнен.")


def main():
    """
    Основной цикл программы для автоматической игры в Telegram.
    """
    while True:
        # Захват изображения с областью выражения
        image = capture_expression()
        # Распознавание текста
        expression_text = extract_expression(image)
        if expression_text:
            # Очистка и вычисление выражения
            result = parse_and_evaluate(expression_text)
            if result is not None:
                # Преобразуем результат в целое число, если это возможно
                rounded_result = int(round(result))
                click_result(rounded_result)
        else:
            print("Выражение не получено.")
        # Пауза перед следующим циклом (можно настроить в зависимости от скорости игры)
        time.sleep(1.5)


if __name__ == "__main__":
    main()
