#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 12 (мини-проекты)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-12"

SETUP_MD = "## Настройка (выполнить один раз)"
SETUP_CODE = '''import turtle

screen = turtle.Screen()
artist = turtle.Turtle()
artist.speed(0)
print("Окно Turtle готово.")'''
TEARDOWN_MD = "## Завершение (выполнить один раз, в самом конце)"
TEARDOWN_CODE = '''screen.bye()
print("Окно Turtle закрыто.")'''


def input_setup(answers: list[str]) -> tuple[str, str]:
    md = ("## Про input() в этом ноутбуке\n\nЭтот ноутбук выполняется автоматически, поэтому "
          "`input()` временно подменён на заранее заготовленные ответы.")
    answers_repr = ", ".join(repr(a) for a in answers)
    code = f"""_answers = iter([{answers_repr}])

def input(prompt=""):
    answer = next(_answers)
    print(prompt + answer)
    return answer"""
    return md, code


def build_01() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-01 · Чётное или нечётное\n\nПрактика к разделу "
          "[«Проект 12-1»](../../site/chapters/glava-12/12-01-chetnoe-ili-nechetnoe.html).")
    nb.md("## Цель\n\nЗакрепить условия и оператор %.")
    md, code = input_setup(["17"])
    nb.md(md)
    nb.code(code)
    nb.md("## Часть 1 — одно число")
    nb.code('''number = int(input("Введите число: "))
if number % 2 == 0:
    print(f"{number} — чётное.")
else:
    print(f"{number} — нечётное.")''')
    nb.md("## Часть 2 — диапазон")
    md2, code2 = input_setup(["1", "20"])
    nb.md(md2)
    nb.code(code2)
    nb.code('''nachalo = int(input("Начало диапазона: "))
konec = int(input("Конец диапазона: "))

chetnye = [n for n in range(nachalo, konec + 1) if n % 2 == 0]
print("Чётные числа:", chetnye)''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nВыведите нечётные числа из того же "
          "диапазона.")
    nb.code('''nachalo, konec = 1, 20
nechetnye = [n for n in range(nachalo, konec + 1) if n % 2 != 0]
print("Нечётные числа:", nechetnye)''')
    nb.write(OUT_DIR / "12-01-chetnoe-nechetnoe.ipynb")
    print(f"Записано: 12-01 ({len(nb)} ячеек)")


def build_02() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-02 · Достаточно ли чаевых?\n\nПрактика к разделу "
          "[«Проект 12-2»](../../site/chapters/glava-12/12-02-chaevye.html).")
    nb.md("## Цель\n\nЗакрепить арифметику, форматирование и elif.")
    md, code = input_setup(["1000", "150"])
    nb.md(md)
    nb.code(code)
    nb.md("## Рабочий пример")
    nb.code('''schet = float(input("Сумма счёта: "))
chaevye = float(input("Сумма чаевых: "))

procent = (chaevye / schet) * 100

if procent < 15:
    print(f"Маловато — всего {procent:.1f}%. Обычно оставляют 15-20%.")
elif procent <= 20:
    print(f"В самый раз — {procent:.1f}%!")
else:
    print(f"Очень щедро — целых {procent:.1f}%!")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте категорию «сказочно щедро» для "
          "чаевых больше 30%.")
    md2, code2 = input_setup(["1000", "350"])
    nb.md(md2)
    nb.code(code2)
    nb.code('''schet = float(input("Сумма счёта: "))
chaevye = float(input("Сумма чаевых: "))
procent = (chaevye / schet) * 100

if procent < 15:
    print(f"Маловато — всего {procent:.1f}%.")
elif procent <= 20:
    print(f"В самый раз — {procent:.1f}%!")
elif procent <= 30:
    print(f"Очень щедро — целых {procent:.1f}%!")
else:
    print(f"Сказочно щедро — {procent:.1f}%!")''')
    nb.write(OUT_DIR / "12-02-chaevye.ipynb")
    print(f"Записано: 12-02 ({len(nb)} ячеек)")


def build_03() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-03 · Рождественская ёлка\n\nПрактика к разделу "
          "[«Проект 12-3»](../../site/chapters/glava-12/12-03-elka.html).")
    nb.md("## Цель\n\nНарисовать ёлку из уменьшающихся треугольных ярусов.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''artist.reset()
artist.pencolor("green")
artist.fillcolor("green")

yarusy = 4
shirina = 120

artist.penup()
artist.goto(0, 100)
artist.pendown()

for yarus in range(yarusy):
    artist.begin_fill()
    artist.setheading(240)
    artist.forward(shirina)
    artist.setheading(0)
    artist.forward(shirina)
    artist.setheading(120)
    artist.forward(shirina)
    artist.end_fill()

    artist.penup()
    artist.setheading(270)
    artist.forward(30)
    artist.pendown()
    shirina -= 20

print("Ёлка из", yarusy, "ярусов готова.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nИзмените число ярусов на 6 и начальную "
          "ширину — на 150.")
    nb.code('''artist.reset()
artist.pencolor("green")
artist.fillcolor("green")

yarusy = 6
shirina = 150

artist.penup()
artist.goto(0, 130)
artist.pendown()

for yarus in range(yarusy):
    artist.begin_fill()
    artist.setheading(240)
    artist.forward(shirina)
    artist.setheading(0)
    artist.forward(shirina)
    artist.setheading(120)
    artist.forward(shirina)
    artist.end_fill()

    artist.penup()
    artist.setheading(270)
    artist.forward(25)
    artist.pendown()
    shirina -= 20

print("Ёлка из", yarusy, "ярусов готова.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "12-03-elka.ipynb")
    print(f"Записано: 12-03 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-04 · Спирали!\n\nПрактика к разделу "
          "[«Проект 12-4»](../../site/chapters/glava-12/12-04-spirali.html).")
    nb.md("## Цель\n\nНарисовать все пять вариантов спирали.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Квадратная спираль")
    nb.code('''artist.reset()
dlina = 5
for _ in range(60):
    artist.forward(dlina)
    artist.right(90)
    dlina += 3
print("Квадратная спираль готова.")''')
    nb.md("## Случайная спираль")
    nb.code('''import random

artist.reset()
dlina = 5
for _ in range(60):
    artist.forward(dlina)
    artist.right(random.randint(80, 100))
    dlina += 3
print("Случайная спираль готова.")''')
    nb.md("## Треугольная спираль")
    nb.code('''artist.reset()
dlina = 5
for _ in range(60):
    artist.forward(dlina)
    artist.right(120)
    dlina += 3
print("Треугольная спираль готова.")''')
    nb.md("## Звёздная спираль")
    nb.code('''artist.reset()
dlina = 5
for _ in range(100):
    artist.forward(dlina)
    artist.right(144)
    dlina += 2
print("Звёздная спираль готова.")''')
    nb.md("## Круговая спираль")
    nb.code('''artist.reset()
radius = 5
for _ in range(60):
    artist.circle(radius, 90)
    radius += 3
print("Круговая спираль готова.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "12-04-spirali.ipynb")
    print(f"Записано: 12-04 ({len(nb)} ячеек)")


def build_05() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-05 · Сложная мандала\n\nПрактика к разделу "
          "[«Проект 12-5»](../../site/chapters/glava-12/12-05-slozhnaya-mandala.html).")
    nb.md("## Цель\n\nПолностью автоматизированная мандала со случайными цветами.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''import random

artist.reset()
luchi = 36
shag_ugla = 360 / luchi
cveta = ["red", "orange", "purple", "blue", "green"]

for i in range(luchi):
    artist.pencolor(random.choice(cveta))
    artist.setheading(i * shag_ugla)
    artist.forward(150)
    artist.circle(20)
    artist.forward(-150)

print("Мандала готова, лучей:", luchi)''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nИзмените `luchi` на 12 — реже расставленные "
          "лучи, но тот же принцип.")
    nb.code('''import random

artist.reset()
luchi = 12
shag_ugla = 360 / luchi
cveta = ["red", "orange", "purple", "blue", "green"]
for i in range(luchi):
    artist.pencolor(random.choice(cveta))
    artist.setheading(i * shag_ugla)
    artist.forward(150)
    artist.circle(20)
    artist.forward(-150)
print(f"luchi={luchi}: готово")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "12-05-slozhnaya-mandala.ipynb")
    print(f"Записано: 12-05 ({len(nb)} ячеек)")


def build_06() -> None:
    nb = NotebookBuilder()
    nb.md("# 12-06 · Гонка Turtle\n\nПрактика к разделу "
          "[«Проект 12-6»](../../site/chapters/glava-12/12-06-gonka-turtle-itogi.html).")
    nb.md("## Цель\n\nНесколько черепашек на одном экране одновременно.")
    nb.md("""\
## О случайности в этом ноутбуке

Гонка использует `random.randint()` для шага каждой черепашки — результат может отличаться
при каждом запуске. Чтобы ноутбук выполнялся предсказуемо, здесь дополнительно закрепляем
случайность через `random.seed()`.""")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''import random

random.seed(3)
screen.setup(500, 400)

cveta = ["red", "blue", "green", "orange"]
uchastniki = []

for i, cvet in enumerate(cveta):
    t = turtle.Turtle()
    t.shape("turtle")
    t.color(cvet)
    t.penup()
    t.goto(-200, i * 40 - 60)
    uchastniki.append(t)

finish_line = 200
pobeditel = None

while pobeditel is None:
    for t in uchastniki:
        t.forward(random.randint(1, 10))
        if t.xcor() >= finish_line:
            pobeditel = t.pencolor()
            break

print(f"Победила черепашка цвета {pobeditel}!")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "12-06-gonka-turtle.ipynb")
    print(f"Записано: 12-06 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_01()
    build_02()
    build_03()
    build_04()
    build_05()
    build_06()
