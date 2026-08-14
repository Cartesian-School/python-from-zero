#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 10 (циклы)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-10"

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
    md = (
        "## Про input() в этом ноутбуке\n\n"
        "Этот ноутбук выполняется автоматически, без живого человека за клавиатурой — поэтому "
        "здесь `input()` временно подменён на заранее заготовленные ответы."
    )
    answers_repr = ", ".join(repr(a) for a in answers)
    code = f"""_answers = iter([{answers_repr}])

def input(prompt=""):
    answer = next(_answers)
    print(prompt + answer)
    return answer"""
    return md, code


def build_01() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-01 · Циклы for\n\nПрактика к разделу "
          "[«Волшебные циклы! Циклы for»](../../site/chapters/glava-10/10-01-cikly-for.html).")
    nb.md("## Цель\n\nОсвоить цикл for и range().")
    nb.md("## Рабочий пример")
    nb.code('''for i in range(5):
    print(i)''')
    nb.md("## Эксперимент 1 — range с началом и концом")
    nb.code('''for i in range(2, 8):
    print(i)''')
    nb.md("## Эксперимент 2 — range с шагом")
    nb.code('''for i in range(0, 10, 2):
    print(i)''')
    nb.md("## Задание ★ Базовая практика\n\nВыведите таблицу умножения числа 7 (7×1 до 7×10).")
    nb.code('''for i in range(1, 11):
    print(f"7 x {i} = {7 * i}")''')
    nb.md("## Дополнительная задача ★★★\n\nПосчитайте сумму всех чисел от 1 до 100 циклом (без "
          "формулы).")
    nb.code('''total = 0
for i in range(1, 101):
    total += i
print(total)''')
    nb.md("## Проверка результата")
    nb.code('''assert sum(range(1, 101)) == 5050
print("Верно: сумма чисел от 1 до 100 равна 5050.")''')
    nb.write(OUT_DIR / "10-01-cikly-for.ipynb")
    print(f"Записано: 10-01 ({len(nb)} ячеек)")


def build_02() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-02 · if внутри циклов, вложенные циклы\n\nПрактика к разделу "
          "[«Условия if внутри циклов for»](../../site/chapters/glava-10/10-02-if-vlozhennye-cikly.html).")
    nb.md("## Цель\n\nСочетать if с for и вкладывать циклы друг в друга.")
    nb.md("## Рабочий пример")
    nb.code('''for number in range(1, 11):
    if number % 2 == 0:
        print(number, "— чётное")''')
    nb.md("## Эксперимент 1 — вложенные циклы")
    nb.code('''for row in range(3):
    for col in range(4):
        print(f"({row}, {col})", end=" ")
    print()''')
    nb.md("## Задание ★ Базовая практика\n\nВыведите треугольник из звёздочек: 1 звезда в "
          "первой строке, 2 во второй, ..., 5 в пятой.")
    nb.code('''for row in range(1, 6):
    print("*" * row)''')
    nb.md("## Дополнительная задача ★★★\n\nВыведите таблицу умножения 1-5 x 1-5 вложенными "
          "циклами.")
    nb.code('''for a in range(1, 6):
    for b in range(1, 6):
        print(f"{a * b:3}", end=" ")
    print()''')
    nb.write(OUT_DIR / "10-02-if-vlozhennye.ipynb")
    print(f"Записано: 10-02 ({len(nb)} ячеек)")


def build_03() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-03 · Перебор строк и while\n\nПрактика к разделу "
          "[«Перебор строк и циклы while»](../../site/chapters/glava-10/10-03-perebor-strok-while.html).")
    nb.md("## Цель\n\nПеребирать строки циклом for и освоить цикл while.")
    nb.md("## Рабочий пример")
    nb.code('''for letter in "Python":
    print(letter)''')
    nb.md("## Эксперимент 1 — while")
    nb.code('''count = 0
while count < 5:
    print(count)
    count += 1''')
    nb.md("## Типичная ошибка — забыли увеличить счётчик\n\nЗдесь используем ограничитель "
          "предохранителем (`safety`), чтобы демонстрационная ячейка не зависла по-настоящему "
          "в автоматическом выполнении.")
    nb.code('''count = 0
safety = 0
while count < 5:
    print(count)
    safety += 1
    if safety > 1000:
        print("Похоже на бесконечный цикл — останавливаем принудительно.")
        break''')
    nb.md("## Задание ★ Базовая практика\n\nПосчитайте гласные буквы в слове с помощью for по "
          "строке.")
    nb.code('''word = "программирование"
glasnye = "аеёиоуыэюя"
count = 0
for letter in word:
    if letter in glasnye:
        count += 1
print(f"Гласных букв: {count}")''')
    nb.write(OUT_DIR / "10-03-while.ipynb")
    print(f"Записано: 10-03 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-04 · break и continue\n\nПрактика к разделу "
          "[«Прервать миссию! break и continue»](../../site/chapters/glava-10/10-04-break-continue.html).")
    nb.md("## Цель\n\nОсвоить break и continue.")
    nb.md("## Рабочий пример — break")
    nb.code('''for number in range(1, 100):
    if number == 5:
        break
    print(number)''')
    nb.md("## Эксперимент 1 — continue")
    nb.code('''for number in range(1, 6):
    if number == 3:
        continue
    print(number)''')
    nb.md("## Задание ★ Базовая практика\n\nНайдите первое число от 1 до 100, которое делится "
          "и на 3, и на 7 — используя break.")
    nb.code('''for number in range(1, 101):
    if number % 3 == 0 and number % 7 == 0:
        print("Нашли:", number)
        break''')
    nb.md("## Проверка результата")
    nb.code('''assert 21 % 3 == 0 and 21 % 7 == 0
print("Верно: 21 — первое число, делящееся и на 3, и на 7.")''')
    nb.write(OUT_DIR / "10-04-break-continue.ipynb")
    print(f"Записано: 10-04 ({len(nb)} ячеек)")


def build_05() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-05 · «Угадай число», версия 2\n\nПрактика к разделу "
          "[«Мини-проект — «Угадай число», версия 2»](../../site/chapters/glava-10/10-05-mini-proekt-ugadaj-v2.html).")
    nb.md("## Цель\n\nПереписать игру из главы 9 с неограниченным числом попыток.")
    md, code = input_setup(["10", "15", "11"])
    nb.md(md)
    nb.code(code)
    nb.md("## Рабочий пример")
    nb.code('''import random

random.seed(7)
zagadannoe = random.randint(1, 20)
popytki = 0

while True:
    popytka = int(input("Угадайте число от 1 до 20: "))
    popytki += 1

    if popytka == zagadannoe:
        print(f"Поздравляем, вы угадали за {popytki} попыток(ки)!")
        break
    elif popytka < zagadannoe:
        print("Загаданное число больше.")
    else:
        print("Загаданное число меньше.")''')
    nb.write(OUT_DIR / "10-05-ugadaj-v2.ipynb")
    print(f"Записано: 10-05 ({len(nb)} ячеек)")


def build_06() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-06 · Автоматизируем фигуры\n\nПрактика к разделу "
          "[«Автоматизируем квадрат и любую фигуру»](../../site/chapters/glava-10/10-06-avtomatiziruem-figury.html).")
    nb.md("## Цель\n\nПереписать фигуры из главы 6 с циклами.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример — квадрат")
    nb.code('''artist.reset()
for _ in range(4):
    artist.forward(100)
    artist.right(90)
print("Квадрат готов.")''')
    nb.md("## Эксперимент 1 — любая фигура")
    nb.code('''artist.reset()
storony = 8
dlina = 60
ugol = 360 / storony

for _ in range(storony):
    artist.forward(dlina)
    artist.right(ugol)
print(f"{storony}-угольник готов.")''')
    nb.md("## Задание ★ Базовая практика\n\nНарисуйте фигуры с 3, 5 и 10 сторонами подряд, "
          "используя одну и ту же функцию-подобную схему.")
    nb.code('''for storony in [3, 5, 10]:
    artist.reset()
    dlina = 50
    ugol = 360 / storony
    for _ in range(storony):
        artist.forward(dlina)
        artist.right(ugol)
    print(f"{storony}-угольник нарисован, угол поворота {ugol}")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "10-06-avto-figury.ipynb")
    print(f"Записано: 10-06 ({len(nb)} ячеек)")


def build_07() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-07 · Автоматическая мандала\n\nПрактика к разделу "
          "[«Мини-проект — автоматически рисуем мандалу»](../../site/chapters/glava-10/10-07-avtomatiziruem-mandalu.html).")
    nb.md("## Цель\n\nПереписать мандалу из главы 6 с for + range() вместо while.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''artist.reset()
shag_ugla = 10

for ugol in range(0, 360, shag_ugla):
    artist.setheading(ugol)
    artist.forward(150)
    artist.backward(150)

print("Мандала готова, лучей:", 360 // shag_ugla)''')
    nb.md("## Эксперимент 1\n\nПопробуйте разные значения shag_ugla: 5, 20, 45.")
    nb.code('''for shag_ugla in [5, 20, 45]:
    artist.reset()
    for ugol in range(0, 360, shag_ugla):
        artist.setheading(ugol)
        artist.forward(150)
        artist.backward(150)
    print(f"shag_ugla={shag_ugla}: лучей {360 // shag_ugla}")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "10-07-avto-mandala.ipynb")
    print(f"Записано: 10-07 ({len(nb)} ячеек)")


def build_08() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-08 · Спирали из дуг\n\nПрактика к разделу "
          "[«Мини-проект — спирали из дуг»](../../site/chapters/glava-10/10-08-spirali-itogi.html).")
    nb.md("## Цель\n\nНарисовать спираль с растущим радиусом.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''artist.reset()
radius = 5

for _ in range(60):
    artist.circle(radius, 90)
    radius += 3

print("Спираль готова, финальный радиус:", radius)''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nНарисуйте спираль из квадратов, "
          "увеличивающихся на каждом шаге.")
    nb.code('''artist.reset()
storona = 5

for _ in range(30):
    for _ in range(4):
        artist.forward(storona)
        artist.right(90)
    artist.right(15)   # немного поворачиваем всю фигуру для эффекта спирали
    storona += 3

print("Спираль из квадратов готова.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "10-08-spirali.ipynb")
    print(f"Записано: 10-08 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_01()
    build_02()
    build_03()
    build_04()
    build_05()
    build_06()
    build_07()
    build_08()
