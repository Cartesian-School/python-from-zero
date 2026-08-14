#!/usr/bin/env python3
"""Строит 5 ноутбуков практики для Главы 5."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-05"


def build_01() -> None:
    nb = NotebookBuilder()
    nb.md("# 05-01 · Основные математические операции\n\nПрактика к разделу "
          "[«Основные математические операции»](../../site/chapters/glava-05/05-01-osnovnye-operacii.html).")
    nb.md("## Цель\n\nПотренировать +, -, *, / на разных числах.")
    nb.md("## Рабочий пример")
    nb.code('''print(5 + 3)
print(5 - 3)
print(5 * 3)
print(5 / 3)''')
    nb.md("## Эксперимент 1\n\nПроверьте те же операции с отрицательными числами.")
    nb.code('''print(-5 + 3)
print(-5 * 3)''')
    nb.md("## Эксперимент 2\n\nСмешайте переменные и операторы: посчитайте площадь "
          "прямоугольника 12 × 7.")
    nb.code('''width = 12
height = 7
area = width * height
print(area)''')
    nb.md("## Задание ★ Базовая практика\n\nПосчитайте, сколько получится сдачи, если товар "
          "стоит 350, а вы дали купюру в 500.")
    nb.code('''price = 350
paid = 500
change = paid - price
print(change)''')
    nb.write(OUT_DIR / "05-01-osnovnye-operacii.ipynb")
    print(f"Записано: 05-01 ({len(nb)} ячеек)")


def build_02() -> None:
    nb = NotebookBuilder()
    nb.md("# 05-02 · Специальные операции, присваивание и порядок\n\nПрактика к разделам "
          "[«Специальные операции»](../../site/chapters/glava-05/05-02-specialnye-operacii.html) и "
          "[«Присваивание и порядок»](../../site/chapters/glava-05/05-03-prisvaivanie-poryadok.html).")
    nb.md("## Цель\n\nОсвоить //, %, ** и сокращённые операторы присваивания.")
    nb.md("## Рабочий пример")
    nb.code('''print(17 // 5)
print(17 % 5)
print(2 ** 10)''')
    nb.md("## Эксперимент 1\n\nПроверьте чётность нескольких чисел через `% 2`.")
    nb.code('''for n in [4, 7, 10, 13]:
    print(n, n % 2 == 0)''')
    nb.md("## Эксперимент 2\n\nИспользуйте `+=` для накопления счёта в игре за три хода.")
    nb.code('''score = 0
score += 10
score += 25
score += 7
print(score)''')
    nb.md("## Типичная ошибка\n\nЛегко перепутать `//` (целочисленное деление) и `/` (обычное) "
          "— они дают разные типы результата.")
    nb.code('''print(10 // 3, type(10 // 3))
print(10 / 3, type(10 / 3))''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте порядок вычислений: посчитайте "
          "`2 + 3 * 4 ** 2` и сравните со своим предсказанием на бумаге.")
    nb.code('''print(2 + 3 * 4 ** 2)''')
    nb.md("## Проверка результата")
    nb.code('''assert 2 + 3 * 4 ** 2 == 50
print("Верно: 4 ** 2 = 16, 3 * 16 = 48, 48 + 2 = 50")''')
    nb.write(OUT_DIR / "05-02-operatory.ipynb")
    print(f"Записано: 05-02 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 05-04 · Математические функции\n\nПрактика к разделу "
          "[«Интересные возможности работы с числами»](../../site/chapters/glava-05/05-04-matematicheskie-funkcii.html).")
    nb.md("## Цель\n\nОсвоить модуль `math`: floor, ceil, sqrt, factorial, тригонометрию.")
    nb.md("## Рабочий пример")
    nb.code('''import math

print(math.floor(4.7))
print(math.ceil(4.2))
print(math.sqrt(64))''')
    nb.md("## Эксперимент 1\n\nПосчитайте факториалы нескольких чисел подряд.")
    nb.code('''import math

for n in range(1, 6):
    print(n, "! =", math.factorial(n))''')
    nb.md("## Эксперимент 2\n\n`round()` — встроенная функция (не из math). Сравните её с "
          "floor/ceil на одном и том же числе.")
    nb.code('''import math

x = 4.5
print(round(x), math.floor(x), math.ceil(x))''')
    nb.md("## Задание ★ Базовая практика\n\nНайдите длину гипотенузы прямоугольного треугольника "
          "с катетами 3 и 4, используя `math.sqrt`.")
    nb.code('''import math

a, b = 3, 4
hypotenuse = math.sqrt(a ** 2 + b ** 2)
print(hypotenuse)''')
    nb.md("## Проверка результата")
    nb.code('''import math

assert math.sqrt(3 ** 2 + 4 ** 2) == 5.0
print("Верно: классический треугольник 3-4-5.")''')
    nb.write(OUT_DIR / "05-04-matematicheskie-funkcii.ipynb")
    print(f"Записано: 05-04 ({len(nb)} ячеек)")


def build_05() -> None:
    nb = NotebookBuilder()
    nb.md("# 05-05 · Случайные числа\n\nПрактика к разделу "
          "[«Работа со случайными числами»](../../site/chapters/glava-05/05-05-sluchaynye-chisla.html).")
    nb.md("## Цель\n\nОсвоить модуль `random`: random(), randint(), uniform(), choice().")
    nb.md("## Рабочий пример")
    nb.code('''import random

print(random.randint(1, 6))''')
    nb.md("## Эксперимент 1\n\n`randint` включает обе границы — запустите ячейку много раз (или "
          "в цикле) и убедитесь, что среди результатов встречаются и 1, и 6.")
    nb.code('''import random

results = [random.randint(1, 6) for _ in range(20)]
print(results)
print("Минимум:", min(results), "Максимум:", max(results))''')
    nb.md("## Эксперимент 2\n\nВыберите случайный элемент из своего списка вариантов.")
    nb.code('''import random

variants = ["камень", "ножницы", "бумага"]
print(random.choice(variants))''')
    nb.md("## Задание ★ Базовая практика\n\nСимулируйте бросок двух кубиков и выведите сумму "
          "очков.")
    nb.code('''import random

dice1 = random.randint(1, 6)
dice2 = random.randint(1, 6)
print(dice1, "+", dice2, "=", dice1 + dice2)''')
    nb.md("## Дополнительная задача ★★★\n\nСимулируйте 1000 бросков одного кубика и посчитайте, "
          "сколько раз выпала каждая грань — числа должны быть примерно равны.")
    nb.code('''import random

counts = {n: 0 for n in range(1, 7)}
for _ in range(1000):
    roll = random.randint(1, 6)
    counts[roll] += 1

print(counts)''')
    nb.write(OUT_DIR / "05-05-sluchaynye-chisla.ipynb")
    print(f"Записано: 05-05 ({len(nb)} ячеек)")


def build_06() -> None:
    nb = NotebookBuilder()
    nb.md("# 05-06 · Мини-проект — кратные числа\n\nПрактика к разделу "
          "[«Мини-проект — кратные числа»](../../site/chapters/glava-05/05-06-mini-proekt-itogi.html).")
    nb.md("## Цель\n\nСобрать оператор `%` в готовую небольшую программу.")
    nb.md("## Рабочий пример")
    nb.code('''kratnoe_chemu = 3
chislo = 1
while chislo <= 50:
    if chislo % kratnoe_chemu == 0:
        print(chislo)
    chislo += 1''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nИзмените диапазон поиска на 1–100 и "
          "кратность — на 7.")
    nb.code('''kratnoe_chemu = 7
chislo = 1
while chislo <= 100:
    if chislo % kratnoe_chemu == 0:
        print(chislo)
    chislo += 1''')
    nb.md("## Дополнительная задача ★★★\n\nПосчитайте не только сами числа, но и их количество "
          "— выведите его в конце.")
    nb.code('''kratnoe_chemu = 5
chislo = 1
count = 0
while chislo <= 50:
    if chislo % kratnoe_chemu == 0:
        count += 1
    chislo += 1

print("Найдено чисел:", count)''')
    nb.md("## Проверка результата")
    nb.code('''kratnoe_chemu = 5
count = sum(1 for n in range(1, 51) if n % kratnoe_chemu == 0)
assert count == 10
print("Верно: от 1 до 50 ровно 10 чисел, кратных 5.")''')
    nb.write(OUT_DIR / "05-06-mini-proekt-kratnye.ipynb")
    print(f"Записано: 05-06 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_01()
    build_02()
    build_04()
    build_05()
    build_06()
