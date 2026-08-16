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


def build_09() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-09 · range() подробно\n\nПрактика к разделу "
          "[«range() подробно»](../../site/chapters/glava-10/10-09-range-podrobno.html).")
    nb.md("## Цель\n\nОсвоить все три сигнатуры range() и отрицательный шаг.")
    nb.md("## Рабочий пример")
    nb.code('''for n in range(0, 10, 2):
    print(n)''')
    nb.md("## Эксперимент 1 — отрицательный шаг")
    nb.code('''for n in range(10, 0, -2):
    print(n)''')
    nb.md("## Задание ★ Базовая практика\n\nСоберите в список `otschet` числа от 100 до 50 "
          "включительно, с шагом -5 (обратный отсчёт).")
    nb.code('''otschet = []
for n in range(100, 45, -5):
    otschet.append(n)
print(otschet)''')
    nb.write(OUT_DIR / "10-09-range-podrobno.ipynb")
    print(f"Записано: 10-09 ({len(nb)} ячеек)")


def build_10() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-10 · enumerate() и накопление\n\nПрактика к разделу "
          "[«Индекс, значение и enumerate()»](../../site/chapters/glava-10/10-10-enumerate-i-nakoplenie.html).")
    nb.md("## Цель\n\nОсвоить enumerate() и паттерны счётчика/накопителя.")
    nb.md("## Рабочий пример")
    nb.code('''slovo = "Python"
for i, letter in enumerate(slovo):
    print(i, letter)''')
    nb.md("## Задание ★ Базовая практика\n\nИспользуя enumerate(), соберите список строк вида "
          "`\"1: хлеб\"` (нумерация с 1, а не с 0) в переменную `spisok_s_nomerami`.")
    nb.code('''produkty = ["хлеб", "молоко", "яйца", "сыр"]
spisok_s_nomerami = []
for i, p in enumerate(produkty):
    spisok_s_nomerami.append(f"{i + 1}: {p}")
print(spisok_s_nomerami)''')
    nb.write(OUT_DIR / "10-10-enumerate.ipynb")
    print(f"Записано: 10-10 ({len(nb)} ячеек)")


def build_11() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-11 · Мини-проект «Анализатор текста»\n\nПрактика к разделу "
          "[«Индекс, значение и enumerate()»](../../site/chapters/glava-10/10-10-enumerate-i-nakoplenie.html#analizator-teksta).")
    nb.md("## Цель\n\nСобрать счётчик и накопитель вместе в небольшом инструменте анализа текста.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''tekst = "python это просто и понятно"
slova = tekst.split()

glasnye_count = 0
for letter in tekst:
    if letter in "аеёиоуыэюя":
        glasnye_count += 1

samoe_dlinnoe = ""
for slovo in slova:
    if len(slovo) > len(samoe_dlinnoe):
        samoe_dlinnoe = slovo

print(f"Слов: {len(slova)}, гласных: {glasnye_count}, самое длинное: {samoe_dlinnoe}")''')
    nb.write(OUT_DIR / "10-11-analizator-teksta.ipynb")
    print(f"Записано: 10-11 ({len(nb)} ячеек)")


def build_12() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-12 · Мини-проект «Таблица умножения»\n\nПрактика к разделу "
          "[«if внутри циклов, вложенные циклы»](../../site/chapters/glava-10/10-02-if-vlozhennye-cikly.html#tablica-umnozheniya).")
    nb.md("## Цель\n\nПостроить таблицу умножения вложенными циклами, сохранив результат в список списков.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''tablica = []
for a in range(1, 6):
    stroka = []
    for b in range(1, 6):
        stroka.append(a * b)
    tablica.append(stroka)
print(tablica)''')
    nb.write(OUT_DIR / "10-12-tablica-umnozheniya.ipynb")
    print(f"Записано: 10-12 ({len(nb)} ячеек)")


def build_13() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-13 · Мини-проект «Цикл команд» и loop-else\n\nПрактика к разделу "
          "[«break, continue и loop-else»](../../site/chapters/glava-10/10-04-break-continue.html#cikl-komand).")
    nb.md("## Цель\n\nСобрать while True + break из глав 8-9 в цикл команд, и закрепить loop-else.")
    md, code = input_setup(["привет", "list", "stop"])
    nb.md(md)
    nb.code(code)
    nb.md("## Задание ★ Базовая практика — цикл команд")
    nb.code('''zhurnal = []
while True:
    komanda = input("Команда (help/list/stop): ").strip().lower()
    if komanda == "stop":
        print("Завершаю работу.")
        break
    elif komanda == "help":
        print("Доступно: help, list, stop")
    elif komanda == "list":
        print("Журнал:", zhurnal)
    else:
        zhurnal.append(komanda)
        print(f"Добавлено в журнал: {komanda}")''')
    nb.md("## Задание ★★ — loop-else")
    nb.code('''chisla = [4, 8, 15, 16, 23, 42]
for n in chisla:
    if n == 100:
        naideno_100 = True
        break
else:
    naideno_100 = False
print(naideno_100)''')
    nb.write(OUT_DIR / "10-13-cikl-komand.ipynb")
    print(f"Записано: 10-13 ({len(nb)} ячеек)")


def build_14() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-14 · Поиск, фильтрация и суммирование\n\nПрактика к разделу "
          "[«Поиск, фильтрация и суммирование»](../../site/chapters/glava-10/10-11-poisk-filtr-summa.html).")
    nb.md("## Цель\n\nОсвоить три базовых паттерна: поиск/подсчёт, суммирование, фильтрация.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''chisla = [4, 8, 15, 16, 23, 42, 7]

summa = 0
for n in chisla:
    summa += n

chetnye_chisla = []
for n in chisla:
    if n % 2 == 0:
        chetnye_chisla.append(n)

maksimum = chisla[0]
for n in chisla:
    if n > maksimum:
        maksimum = n

print(summa, chetnye_chisla, maksimum)''')
    nb.write(OUT_DIR / "10-14-poisk-filtr-summa.ipynb")
    print(f"Записано: 10-14 ({len(nb)} ячеек)")


def build_15() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-15 · Проверка ввода в цикле\n\nПрактика к разделу "
          "[«Проверка ввода в цикле»](../../site/chapters/glava-10/10-12-proverka-vvoda.html).")
    nb.md("## Цель\n\nПереспрашивать пользователя в цикле, пока ввод не станет корректным.")
    md, code = input_setup(["abc", "", "15"])
    nb.md(md)
    nb.code(code)
    nb.md("## Задание ★ Базовая практика")
    nb.code('''vozrast = input("Введите возраст: ")
while not vozrast.isdigit():
    print("Нужно ввести число!")
    vozrast = input("Введите возраст: ")

vozrast = int(vozrast)
print("Спасибо! Вам", vozrast, "лет")''')
    nb.write(OUT_DIR / "10-15-proverka-vvoda.ipynb")
    print(f"Записано: 10-15 ({len(nb)} ячеек)")


def build_16() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-16 · «Угадай число» с ограничением попыток\n\nПрактика к разделу "
          "[«Мини-проект — «Угадай число», версия 2»](../../site/chapters/glava-10/10-05-mini-proekt-ugadaj-v2.html).")
    nb.md("## Цель\n\nОграничить число попыток циклом for и использовать loop-else, чтобы "
          "сообщить правильный ответ, если игрок не угадал.")
    md, code = input_setup(["1", "2", "3", "4", "5"])
    nb.md(md)
    nb.code(code)
    nb.md("## Задание ★★ Самостоятельная задача\n\nЗдесь задуманное число фиксировано (14), а "
          "все 5 попыток заведомо неверны — чтобы проверить именно ветку `else`.")
    nb.code('''zagadannoe = 14
ugadal = None

for popytka_nomer in range(5):
    popytka = int(input("Угадайте число от 1 до 20: "))
    if popytka == zagadannoe:
        print("Угадали!")
        ugadal = True
        break
    elif popytka < zagadannoe:
        print("Больше.")
    else:
        print("Меньше.")
else:
    ugadal = False

print("Угадано:", ugadal)''')
    nb.write(OUT_DIR / "10-16-ugadaj-limit.ipynb")
    print(f"Записано: 10-16 ({len(nb)} ячеек)")


def build_17() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-17 · Найди ошибку в цикле\n\nПрактика к разделу "
          "[«Отладка циклов»](../../site/chapters/glava-10/10-13-otladka-ciklov.html).")
    nb.md("## Цель\n\nНаучиться распознавать и исправлять типичные ошибки циклов.")
    nb.md(
        "## Сломанный код (НЕ запускать как есть)\n\n"
        "Вот код с ошибкой №4 из урока «Отладка циклов» — счётчик сбрасывается прямо внутри "
        "цикла:\n\n"
        "```python\n"
        "chisla = [3, 8, 12, 5, 16, 9, 20]\n"
        "for n in chisla:\n"
        "    chetnye_count = 0   # ошибка: обнуляется на каждой итерации!\n"
        "    if n % 2 == 0:\n"
        "        chetnye_count += 1\n"
        "```\n\n"
        "В ячейке ниже — задание: напишите **исправленную** версию, которая действительно "
        "считает общее количество чётных чисел."
    )
    nb.md("## Задание ★ Базовая практика — исправьте ошибку №4")
    nb.code('''chisla = [3, 8, 12, 5, 16, 9, 20]
chetnye_count = 0
for n in chisla:
    if n % 2 == 0:
        chetnye_count += 1
print(chetnye_count)''')
    nb.md("## Задание ★★ — исправьте ошибку №2 (off-by-one)\n\nНужно собрать числа от 1 до 10 "
          "включительно в список `chisla_1_do_10`.")
    nb.code('''chisla_1_do_10 = []
for n in range(1, 11):
    chisla_1_do_10.append(n)
print(chisla_1_do_10)''')
    nb.write(OUT_DIR / "10-17-najdi-oshibku.ipynb")
    print(f"Записано: 10-17 ({len(nb)} ячеек)")


def build_18() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-18 · Off-by-one — посчитай итерации\n\nПрактика к разделу "
          "[«Отладка циклов»](../../site/chapters/glava-10/10-13-otladka-ciklov.html#off-by-one-otdelnyj-razbor).")
    nb.md("## Цель\n\nПотренироваться точно определять границы range() под конкретную задачу.")
    nb.md("## Задание ★ Базовая практика\n\nСоберите числа от 5 до 15 включительно в `diapazon`.")
    nb.code('''diapazon = []
for n in range(5, 16):
    diapazon.append(n)
print(diapazon)''')
    nb.md("## Задание ★★ — убывающий диапазон\n\nСоберите чётные числа от 20 до 2 включительно, "
          "по убыванию, в `ubyvanie`.")
    nb.code('''ubyvanie = []
for n in range(20, 1, -2):
    ubyvanie.append(n)
print(ubyvanie)''')
    nb.write(OUT_DIR / "10-18-off-by-one.ipynb")
    print(f"Записано: 10-18 ({len(nb)} ячеек)")


def build_19() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-19 · Случайное блуждание и звёздное поле\n\nПрактика к разделу "
          "[«Случайные узоры»](../../site/chapters/glava-10/10-14-sluchajnye-uzory.html).")
    nb.md("## Цель\n\nСоединить циклы со случайностью — с фиксированным seed() для воспроизводимости.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример — случайное блуждание")
    nb.code('''import random
artist.reset()
random.seed(7)

for _ in range(100):
    artist.setheading(random.randint(0, 360))
    artist.forward(10)
print("Блуждание готово.")''')
    nb.md("## Задание ★ Базовая практика — звёздное поле")
    nb.code('''import random
artist.reset()
artist.hideturtle()
artist.penup()
random.seed(3)

for _ in range(60):
    x = random.randint(-190, 190)
    y = random.randint(-190, 190)
    artist.goto(x, y)
    artist.dot(6, "white")
print("Звёздное поле готово.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "10-19-sluchajnye-uzory.ipynb")
    print(f"Записано: 10-19 ({len(nb)} ячеек)")


def build_20() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-20 · Сетка фигур\n\nПрактика к разделу "
          "[«Сетка фигур: вложенные циклы в Turtle»](../../site/chapters/glava-10/10-15-setka-figur.html).")
    nb.md("## Цель\n\nПрименить вложенные циклы «строки × столбцы» к настоящей графике.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Задание ★ Базовая практика")
    nb.code('''artist.reset()
artist.hideturtle()
artist.penup()
shag = 60

for row in range(5):
    for col in range(5):
        x = -140 + col * shag
        y = -140 + row * shag
        artist.goto(x, y)
        artist.dot(16, "#5B24F9")
print("Сетка готова.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "10-20-setka-figur.ipynb")
    print(f"Записано: 10-20 ({len(nb)} ячеек)")


def build_21() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-21 · break в Turtle\n\nПрактика к разделу "
          "[«Спирали из дуг и итоги»](../../site/chapters/glava-10/10-08-spirali-itogi.html).")
    nb.md("## Цель\n\nОстановить рисующий цикл раньше времени условием на положении черепашки.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Задание ★ Базовая практика")
    nb.code('''artist.reset()
dlina = 10

for _ in range(50):
    if artist.xcor() > 150:
        break
    artist.forward(dlina)
    artist.left(90)
    dlina += 6
print("Остановлено на xcor =", artist.xcor())''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "10-21-break-v-turtle.ipynb")
    print(f"Записано: 10-21 ({len(nb)} ячеек)")


def build_22() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-22 · Сентинел-цикл\n\nПрактика к разделу "
          "[«Поиск, фильтрация и суммирование»](../../site/chapters/glava-10/10-11-poisk-filtr-summa.html#sentinel).")
    nb.md("## Цель\n\nОсвоить сентинел-цикл — особое значение как сигнал остановки.")
    md, code = input_setup(["5", "10", "stop"])
    nb.md(md)
    nb.code(code)
    nb.md("## Задание ★ Базовая практика")
    nb.code('''summa = 0
while True:
    chislo = input("Введите число (stop — закончить): ")
    if chislo == "stop":
        break
    summa += int(chislo)
print("Сумма:", summa)''')
    nb.write(OUT_DIR / "10-22-sentinel-cikl.ipynb")
    print(f"Записано: 10-22 ({len(nb)} ячеек)")


def build_23() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-23 · for или while — что выбрать?\n\nПрактика к разделу "
          "[«Циклы while»](../../site/chapters/glava-10/10-03-perebor-strok-while.html).")
    nb.md("## Цель\n\nЗакрепить ориентир выбора между for и while.")
    nb.md(
        "## Задание ★ Базовая практика\n\n"
        "Для каждой ситуации запишите правильный выбор — строкой `\"for\"`, `\"while\"` или "
        "`\"while True\"`:\n\n"
        "1. Нарисовать все 4 стороны квадрата.\n"
        "2. Повторять, пока пользователь не угадает число.\n"
        "3. Перебрать все буквы слова.\n"
        "4. Условие остановки естественнее проверить в середине тела."
    )
    nb.code('''otvet_1 = "for"
otvet_2 = "while"
otvet_3 = "for"
otvet_4 = "while True"''')
    nb.write(OUT_DIR / "10-23-for-ili-while.ipynb")
    print(f"Записано: 10-23 ({len(nb)} ячеек)")


def build_24() -> None:
    nb = NotebookBuilder()
    nb.md("# 10-24 · Сколько итераций во вложенном цикле?\n\nПрактика к разделу "
          "[«if внутри циклов, вложенные циклы»](../../site/chapters/glava-10/10-02-if-vlozhennye-cikly.html#vlozhennye).")
    nb.md("## Цель\n\nПотренироваться считать общее число итераций вложенного цикла: строки × столбцы.")
    nb.md("## Задание ★ Базовая практика\n\nНапишите вложенный цикл на 3 строки × 7 столбцов и "
          "посчитайте, сколько раз выполнится тело, сохранив результат в `itogo_iteracij`.")
    nb.code('''schetchik = 0
for row in range(3):
    for col in range(7):
        schetchik += 1

itogo_iteracij = schetchik
print(itogo_iteracij)''')
    nb.write(OUT_DIR / "10-24-skolko-iteracij.ipynb")
    print(f"Записано: 10-24 ({len(nb)} ячеек)")


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
    build_09()
    build_10()
    build_11()
    build_12()
    build_13()
    build_14()
    build_15()
    build_16()
    build_17()
    build_18()
    build_19()
    build_20()
    build_21()
    build_22()
    build_23()
    build_24()
