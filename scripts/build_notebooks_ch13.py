#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 13 (функции)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-13"

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
    nb.md("# 13-01 · Первая функция\n\nПрактика к разделу "
          "[«Настоящая автоматизация»](../../site/chapters/glava-13/13-01-nastoyashaya-avtomatizaciya.html).")
    nb.md("## Цель\n\nОпределить и вызвать первую функцию.")
    nb.md("## Рабочий пример")
    nb.code('''def privetstvie():
    print("Привет, Python!")

privetstvie()
privetstvie()
privetstvie()''')
    nb.md("## Эксперимент 1\n\nОпределите функцию, не вызывая её, — убедитесь, что ничего не "
          "выводится.")
    nb.code('''def nichego_ne_delaet():
    print("Меня никто не вызвал!")

print("Программа выполнилась, а функция — нет.")''')
    nb.md("## Задание ★ Базовая практика\n\nНапишите функцию `poprisdachu()`, которая выводит "
          "короткое прощание, и вызовите её три раза.")
    nb.code('''def poproshchatsya():
    print("До встречи!")

poproshchatsya()
poproshchatsya()
poproshchatsya()''')
    nb.write(OUT_DIR / "13-01-pervaya-funkciya.ipynb")
    print(f"Записано: 13-01 ({len(nb)} ячеек)")


def build_02() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-02 · Зачем нужны функции?\n\nПрактика к разделу "
          "[«Зачем нужны функции?»](../../site/chapters/glava-13/13-02-zachem-funkcii.html).")
    nb.md("## Цель\n\nОсвоить функции с аргументами.")
    nb.md("## Рабочий пример")
    nb.code('''def privetstvie(imya):
    print(f"Привет, {imya}!")

privetstvie("Ада")
privetstvie("Cartesian")''')
    nb.md("## Эксперимент 1 — несколько параметров")
    nb.code('''def summa_i_proizvedenie(a, b):
    print(f"Сумма: {a + b}, произведение: {a * b}")

summa_i_proizvedenie(3, 4)
summa_i_proizvedenie(10, 2)''')
    nb.md("## Задание ★ Базовая практика\n\nНапишите функцию `plosch_pryamougolnika(width, "
          "height)`, которая выводит площадь.")
    nb.code('''def plosch_pryamougolnika(width, height):
    print(f"Площадь: {width * height}")

plosch_pryamougolnika(5, 3)
plosch_pryamougolnika(10, 10)''')
    nb.write(OUT_DIR / "13-02-zachem-funkcii.ipynb")
    print(f"Записано: 13-02 ({len(nb)} ячеек)")


def build_03() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-03 · Возвращаем ответ\n\nПрактика к разделу "
          "[«Возвращаем ответ»](../../site/chapters/glava-13/13-03-vozvrashaem-otvet.html).")
    nb.md("## Цель\n\nОсвоить return и разницу между return и print().")
    nb.md("## Рабочий пример")
    nb.code('''def summa(a, b):
    return a + b

result = summa(5, 7)
print(result)
print(summa(2, 3) * 10)''')
    nb.md("## Эксперимент 1 — разница между print() и return")
    nb.code('''def summa_pechataet(a, b):
    print(a + b)

x = summa_pechataet(5, 7)
print("x =", x)  # None — функция ничего не вернула!''')
    nb.md("## Задание ★ Базовая практика\n\nНапишите функцию `plosch_pryamougolnika(width, "
          "height)` — на этот раз с return вместо print(), и используйте результат.")
    nb.code('''def plosch_pryamougolnika(width, height):
    return width * height

a1 = plosch_pryamougolnika(5, 3)
a2 = plosch_pryamougolnika(10, 10)
print(f"Первая площадь: {a1}, вторая: {a2}, сумма площадей: {a1 + a2}")''')
    nb.md("## Проверка результата")
    nb.code('''def plosch_pryamougolnika(width, height):
    return width * height

assert plosch_pryamougolnika(5, 3) == 15
assert plosch_pryamougolnika(10, 10) == 100
print("Обе проверки пройдены.")''')
    nb.write(OUT_DIR / "13-03-vozvrat.ipynb")
    print(f"Записано: 13-03 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-04 · Аргументы функций\n\nПрактика к разделу "
          "[«Нет аргументов? Слишком много аргументов!»](../../site/chapters/glava-13/13-04-argumenty.html).")
    nb.md("## Цель\n\nОсвоить значения по умолчанию и *args.")
    nb.md("## Рабочий пример")
    nb.code('''def privetstvie(imya="друг"):
    print(f"Привет, {imya}!")

privetstvie()
privetstvie("Ада")''')
    nb.md("## Эксперимент 1 — *args")
    nb.code('''def summa_vseh(*chisla):
    itog = 0
    for n in chisla:
        itog += n
    return itog

print(summa_vseh(1, 2))
print(summa_vseh(1, 2, 3, 4, 5))
print(summa_vseh())''')
    nb.md("## Задание ★ Базовая практика\n\nНапишите функцию `srednee(*chisla)`, которая "
          "возвращает среднее значение произвольного числа аргументов.")
    nb.code('''def srednee(*chisla):
    return sum(chisla) / len(chisla)

print(srednee(1, 2, 3))
print(srednee(10, 20, 30, 40))''')
    nb.md("## Дополнительная задача ★★★\n\nИменованные аргументы в любом порядке.")
    nb.code('''def opisat_cheloveka(imya, vozrast):
    print(f"{imya}, {vozrast} лет")

opisat_cheloveka(vozrast=30, imya="Cartesian")  # порядок не важен с именами''')
    nb.write(OUT_DIR / "13-04-argumenty.ipynb")
    print(f"Записано: 13-04 ({len(nb)} ячеек)")


def build_05() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-05 · Глобальные и локальные переменные\n\nПрактика к разделу "
          "[«Глобальные и локальные переменные»](../../site/chapters/glava-13/13-05-globalnye-lokalnye.html).")
    nb.md("## Цель\n\nПонять область видимости переменных.")
    nb.md("## Рабочий пример")
    nb.code('''ver = "1.0"

def pokazat_versiyu():
    print(f"Версия программы: {ver}")

pokazat_versiyu()''')
    nb.md("## Типичная ошибка\n\nЛокальная переменная недоступна снаружи функции.")
    nb.code('''def moya_funkciya():
    message = "Я живу только внутри функции"
    print(message)

moya_funkciya()
print(message)''', raises=True)
    nb.md("## Исправление\n\nВернуть значение через return, если оно нужно снаружи.")
    nb.code('''def moya_funkciya():
    message = "Теперь я возвращаюсь наружу"
    return message

result = moya_funkciya()
print(result)''')
    nb.md("## Эксперимент 1 — global (осторожно, редкий приём)")
    nb.code('''schet = 0

def uvelichit_schet():
    global schet
    schet += 1

uvelichit_schet()
uvelichit_schet()
print(schet)''')
    nb.write(OUT_DIR / "13-05-oblast-vidimosti.ipynb")
    print(f"Записано: 13-05 ({len(nb)} ячеек)")


def build_06() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-06 · Лямбда-функции\n\nПрактика к разделу "
          "[«Лямбда-функции»](../../site/chapters/glava-13/13-06-lambda.html).")
    nb.md("## Цель\n\nОсвоить lambda и сравнить с def.")
    nb.md("## Рабочий пример")
    nb.code('''kvadrat = lambda x: x ** 2
print(kvadrat(5))''')
    nb.md("## Эксперимент 1 — lambda в sort()")
    nb.code('''slova = ["python", "я", "программирование"]
slova.sort(key=lambda word: len(word))
print(slova)''')
    nb.md("## Задание ★ Базовая практика\n\nНапишите lambda, которая проверяет, чётно ли "
          "число, и используйте её в filter().")
    nb.code('''is_even = lambda n: n % 2 == 0
chisla = [1, 2, 3, 4, 5, 6, 7, 8]
chetnye = list(filter(is_even, chisla))
print(chetnye)''')
    nb.write(OUT_DIR / "13-06-lambda.ipynb")
    print(f"Записано: 13-06 ({len(nb)} ячеек)")


def build_07() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-07 · Домашнее задание по математике\n\nПрактика к разделу "
          "[«Мини-проект — домашнее задание по математике»](../../site/chapters/glava-13/13-07-mini-proekt-domashka.html).")
    nb.md("## Цель\n\nФункции, генерирующие и проверяющие примеры.")
    md, code = input_setup(["42"])
    nb.md(md)
    nb.code(code)
    nb.md("## Рабочий пример")
    nb.code('''import random

random.seed(1)

def sgenerirovat_primer():
    a = random.randint(2, 9)
    b = random.randint(2, 9)
    return a, b, a * b

def proverit_otvet(pravilnyj_otvet, otvet_polzovatelya):
    return pravilnyj_otvet == otvet_polzovatelya

a, b, pravilnyj_otvet = sgenerirovat_primer()
print(f"Пример: {a} x {b} = ? (правильный ответ: {pravilnyj_otvet})")
otvet = int(input(f"Сколько будет {a} x {b}? "))

if proverit_otvet(pravilnyj_otvet, otvet):
    print("Верно!")
else:
    print(f"Неверно — правильный ответ: {pravilnyj_otvet}")''')
    nb.md("## Задание ★★ Самостоятельная задача — счётчик правильных ответов")
    md2, code2 = input_setup(["1", "2", "3", "4", "5"])
    nb.md(md2)
    nb.code(code2)
    nb.code('''import random

random.seed(2)

def sgenerirovat_primer():
    a = random.randint(2, 9)
    b = random.randint(2, 9)
    return a, b, a * b

pravilnyh = 0
for _ in range(5):
    a, b, pravilnyj_otvet = sgenerirovat_primer()
    otvet = int(input(f"Сколько будет {a} x {b}? "))
    if otvet == pravilnyj_otvet:
        pravilnyh += 1

print(f"Правильных ответов: {pravilnyh} из 5")''')
    nb.write(OUT_DIR / "13-07-domashka.ipynb")
    print(f"Записано: 13-07 ({len(nb)} ячеек)")


def build_08() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-08 · Фигуры: новый уровень\n\nПрактика к разделу "
          "[«Мини-проект — автоматизированные фигуры: новый уровень»](../../site/chapters/glava-13/13-08-mini-proekt-figury-itogi.html).")
    nb.md("## Цель\n\nПревратить рисование фигур в переиспользуемую функцию.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''def narisovat_figuru(storony, dlina):
    ugol = 360 / storony
    for _ in range(storony):
        artist.forward(dlina)
        artist.right(ugol)

artist.reset()
narisovat_figuru(4, 100)
print("Квадрат готов.")''')
    nb.md("## Эксперимент 1 — несколько фигур подряд")
    nb.code('''artist.reset()
narisovat_figuru(3, 100)
print("Треугольник готов.")

artist.reset()
narisovat_figuru(8, 60)
print("Восьмиугольник готов.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте параметры x, y со значениями по "
          "умолчанию 0, 0.")
    nb.code('''def narisovat_figuru_v_tochke(storony, dlina, x=0, y=0):
    artist.penup()
    artist.goto(x, y)
    artist.setheading(0)
    artist.pendown()
    ugol = 360 / storony
    for _ in range(storony):
        artist.forward(dlina)
        artist.right(ugol)

artist.reset()
narisovat_figuru_v_tochke(4, 60, x=-100, y=0)
narisovat_figuru_v_tochke(6, 60, x=100, y=0)
print("Две фигуры в разных точках экрана готовы.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "13-08-figury-novyj-uroven.ipynb")
    print(f"Записано: 13-08 ({len(nb)} ячеек)")


def build_09() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-09 · Цикл или функция?\n\nПрактика к разделу "
          "[«Зачем программе функции»](../../site/chapters/glava-13/13-09-zachem-programme-funkcii.html).")
    nb.md("## Цель\n\nОпределить и переиспользовать функцию для вычисления.")
    nb.md("## Рабочий пример")
    nb.code('''def summa_kvadratov(a, b):
    return a ** 2 + b ** 2

def kvadrat_summy(a, b):
    return (a + b) ** 2

print(summa_kvadratov(3, 4))
print(kvadrat_summy(3, 4))''')
    nb.md("## Задание ★ Базовая практика\n\nИспользуйте обе функции, чтобы найти разницу "
          "между квадратом суммы и суммой квадратов для a=3, b=4.")
    nb.code('''raznost = kvadrat_summy(3, 4) - summa_kvadratov(3, 4)
print(raznost)''')
    nb.write(OUT_DIR / "13-09-cikl-ili-funkciya.ipynb")
    print(f"Записано: 13-09 ({len(nb)} ячеек)")


def build_10() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-10 · Порядок вызова\n\nПрактика к разделу "
          "[«Что происходит во время вызова»](../../site/chapters/glava-13/13-10-vyzov-i-vozvrat-upravlenie.html).")
    nb.md("## Цель\n\nПредсказать порядок вывода при вызове функции.")
    nb.md("## Задание ★ Базовая практика\n\nПредскажите порядок строк, прежде чем запускать.")
    nb.code('''def b():
    print("B")

def a():
    print("A1")
    b()
    print("A2")

print("Старт")
a()
print("Конец")''')
    nb.write(OUT_DIR / "13-10-poryadok-vyzova.ipynb")
    print(f"Записано: 13-10 ({len(nb)} ячеек)")


def build_11() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-11 · Rebinding vs mutation\n\nПрактика к разделу "
          "[«Изменяемые и неизменяемые аргументы»](../../site/chapters/glava-13/13-11-izmenyaemye-i-nezmenyaemye-argumenty.html).")
    nb.md("## Цель\n\nПредсказать, что видно снаружи после rebinding и после mutation.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''def add_one(number):
    number += 1
    return number

x = 10
y = add_one(x)

def add_item(items):
    items.append("Python")

skills = ["Git"]
add_item(skills)

print(x, y, skills)''')
    nb.write(OUT_DIR / "13-11-rebinding-vs-mutation.ipynb")
    print(f"Записано: 13-11 ({len(nb)} ячеек)")


def build_12() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-12 · Позиционные и именованные аргументы\n\nПрактика к разделу "
          "[«Позиционные и именованные аргументы»](../../site/chapters/glava-13/13-12-pozicionnye-i-imennye.html).")
    nb.md("## Цель\n\nВызвать функцию и позиционно, и с именованными аргументами.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''def build_profile(name, age, city="Unknown"):
    return f"{name}, {age}, {city}"

p1 = build_profile("Anna", 25)
p2 = build_profile(age=30, name="Bob", city="Warsaw")
print(p1)
print(p2)''')
    nb.write(OUT_DIR / "13-12-pozicionnye-i-imennye.ipynb")
    print(f"Записано: 13-12 ({len(nb)} ячеек)")


def build_13() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-13 · *args, **kwargs и распаковка\n\nПрактика к разделу "
          "[«*args, **kwargs и распаковка»](../../site/chapters/glava-13/13-13-args-kwargs-raspakovka.html).")
    nb.md("## Цель\n\n*args, **kwargs и распаковка аргументов на месте вызова.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''def total(*numbers):
    return sum(numbers)

def show_profile(**fields):
    return fields

def move(x, y):
    return x + y

t1 = total(1, 2, 3, 4)
profile = show_profile(name="Anna", city="Warsaw")

point = (10, 20)
moved = move(*point)

print(t1, profile, moved)''')
    nb.write(OUT_DIR / "13-13-args-kwargs.ipynb")
    print(f"Записано: 13-13 ({len(nb)} ячеек)")


def build_14() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-14 · Keyword-only параметры\n\nПрактика к разделу "
          "[«Positional-only и keyword-only»](../../site/chapters/glava-13/13-14-positional-only-keyword-only.html).")
    nb.md("## Цель\n\nСоздать функцию с keyword-only параметром и проверить, что позиционный "
          "вызов для него запрещён.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''def draw_rectangle(width, height, *, color="blue"):
    return f"{width}x{height} {color}"

r1 = draw_rectangle(10, 20)
r2 = draw_rectangle(10, 20, color="red")

try:
    draw_rectangle(10, 20, "red")
    keyword_only_enforced = False
except TypeError:
    keyword_only_enforced = True

print(r1, r2, keyword_only_enforced)''')
    nb.write(OUT_DIR / "13-14-keyword-only.ipynb")
    print(f"Записано: 13-14 ({len(nb)} ячеек)")


def build_15() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-15 · Чистые функции и побочные эффекты\n\nПрактика к разделу "
          "[«Вход, работа, выход: чистые функции»](../../site/chapters/glava-13/13-15-funkcii-vhod-vyhod.html).")
    nb.md("## Цель\n\nОтличить чистую функцию от функции с побочным эффектом.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''def rectangle_area(width, height):
    return width * height

log = []

def draw_square_effect(size):
    log.append(f"Нарисован квадрат {size}")

area = rectangle_area(4, 5)
draw_square_effect(10)

print(area, log)''')
    nb.write(OUT_DIR / "13-15-chistye-funkcii.ipynb")
    print(f"Записано: 13-15 ({len(nb)} ячеек)")


def build_16() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-16 · nonlocal\n\nПрактика к разделу "
          "[«Вложенные функции и nonlocal»](../../site/chapters/glava-13/13-16-vlozhennye-funkcii-nonlocal.html).")
    nb.md("## Цель\n\nИспользовать nonlocal, чтобы вложенная функция изменяла счётчик "
          "объемлющей функции.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''def outer():
    count = 0

    def inner():
        nonlocal count
        count += 1

    inner()
    inner()
    inner()
    return count

result = outer()
print(result)''')
    nb.write(OUT_DIR / "13-16-nonlocal.ipynb")
    print(f"Записано: 13-16 ({len(nb)} ячеек)")


def build_17() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-17 · Стек вызовов\n\nПрактика к разделу "
          "[«Стек вызовов и traceback»](../../site/chapters/glava-13/13-17-stek-vyzovov.html).")
    nb.md("## Цель\n\nПроследить порядок вызовов и возвратов во вложенных функциях.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''def c():
    print("C")
    return 3

def b():
    print("B")
    return c() + 1

def a():
    print("A")
    return b() + 1

result = a()
print("Итог:", result)''')
    nb.write(OUT_DIR / "13-17-stek-vyzovov.ipynb")
    print(f"Записано: 13-17 ({len(nb)} ячеек)")


def build_18() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-18 · Контракт функции\n\nПрактика к разделу "
          "[«Проектируем хорошую функцию»](../../site/chapters/glava-13/13-18-proektiruem-funkciyu.html).")
    nb.md("## Цель\n\nРеализовать функцию по заданному контракту.")
    nb.md("## Задание ★ Базовая практика\n\nКонтракт: calculate_discount(price, percent) — "
          "цена со скидкой в процентах.")
    nb.code('''def calculate_discount(price, percent):
    return price - price * percent / 100

d1 = calculate_discount(100, 10)
d2 = calculate_discount(200, 50)
print(d1, d2)''')
    nb.write(OUT_DIR / "13-18-kontrakt-funkcii.ipynb")
    print(f"Записано: 13-18 ({len(nb)} ячеек)")


def build_19() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-19 · Докстринги и типы\n\nПрактика к разделу "
          "[«Докстринги и подсказки типов»](../../site/chapters/glava-13/13-19-dokumentaciya-i-tipy.html).")
    nb.md("## Цель\n\nНаписать функцию с докстрингом и аннотациями типов.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''def rectangle_area(width: float, height: float) -> float:
    """Возвращает площадь прямоугольника."""
    return width * height

docstring_present = rectangle_area.__doc__ is not None
area = rectangle_area(3, 4)
print(docstring_present, area)''')
    nb.write(OUT_DIR / "13-19-docstring-i-tipy.ipynb")
    print(f"Записано: 13-19 ({len(nb)} ячеек)")


def build_20() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-20 · Функции как объекты\n\nПрактика к разделу "
          "[«Функции как объекты»](../../site/chapters/glava-13/13-20-funkcii-kak-obekty.html).")
    nb.md("## Цель\n\nСохранить функции в словаре и под другим именем, вызвать через обе "
          "ссылки.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''def double(x):
    return x * 2

def square(x):
    return x ** 2

operations = {"double": double, "square": square}
result_double = operations["double"](5)
result_square = operations["square"](5)

action = double
result_action = action(7)

print(result_double, result_square, result_action)''')
    nb.write(OUT_DIR / "13-20-funkcii-kak-obekty.ipynb")
    print(f"Записано: 13-20 ({len(nb)} ячеек)")


def build_21() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-21 · Конвейер функций\n\nПрактика к разделу "
          "[«Функции как конвейер»](../../site/chapters/glava-13/13-21-funkcii-kak-konvejer.html).")
    nb.md("## Цель\n\nПостроить конвейер: результат одной функции становится входом "
          "следующей.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''def normalize_text(text):
    return text.lower()

def split_words(text):
    return text.split()

def count_words(words):
    return len(words)

pipeline_result = count_words(split_words(normalize_text("Python IS Fun")))
print(pipeline_result)''')
    nb.write(OUT_DIR / "13-21-konvejer.ipynb")
    print(f"Записано: 13-21 ({len(nb)} ячеек)")


def build_22() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-22 · Рефакторинг викторины\n\nПрактика к разделу "
          "[«Рефакторим проекты главы 12»](../../site/chapters/glava-13/13-22-refaktoring-glavy-12.html).")
    nb.md("## Цель\n\nРазбить викторину из главы 12 на функции check_answer и run_quiz.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''def check_answer(user_answer, correct_answer):
    return user_answer.strip().lower() == correct_answer.lower()

def run_quiz(questions, answers):
    score = 0
    for q, given in zip(questions, answers):
        if check_answer(given, q["answer"]):
            score += 1
    return score

questions = [{"answer": "paris"}, {"answer": "56"}]
answers = ["Paris", "56"]
final_score = run_quiz(questions, answers)
print(final_score)''')
    nb.write(OUT_DIR / "13-22-refaktoring-viktoriny.ipynb")
    print(f"Записано: 13-22 ({len(nb)} ячеек)")


def build_23() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-23 · Debug Lab — функции\n\nПрактика к разделу "
          "[«Debug Lab: типичные ошибки функций»](../../site/chapters/glava-13/13-23-debug-lab-funkcii.html).")
    nb.md("## Цель\n\nИсправить непокрытый путь return и return внутри цикла на первой "
          "итерации.")
    nb.md("## Задание ★ Базовая практика — исправленные версии")
    nb.code('''def sign(number):
    if number > 0:
        return "positive"
    elif number < 0:
        return "negative"
    else:
        return "zero"

def contains_even(numbers):
    for n in numbers:
        if n % 2 == 0:
            return True
    return False

s1 = sign(-5)
s2 = sign(0)
c1 = contains_even([1, 3, 5, 6])
c2 = contains_even([1, 3, 5])
print(s1, s2, c1, c2)''')
    nb.write(OUT_DIR / "13-23-debug-lab.ipynb")
    print(f"Записано: 13-23 ({len(nb)} ячеек)")


def build_24() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-24 · Тестируем функцию\n\nПрактика к разделу "
          "[«Тестируем функции»](../../site/chapters/glava-13/13-24-testirovanie-funkcij.html).")
    nb.md("## Цель\n\nПроверить функцию через assert на нескольких примерах.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''def classify_score(score):
    if score >= 90:
        return "отлично"
    elif score >= 70:
        return "хорошо"
    else:
        return "пересдача"

assert classify_score(95) == "отлично"
assert classify_score(75) == "хорошо"
assert classify_score(50) == "пересдача"
tests_passed = True
print(tests_passed)''')
    nb.write(OUT_DIR / "13-24-testirovanie.ipynb")
    print(f"Записано: 13-24 ({len(nb)} ячеек)")


def build_25() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-25 · Анализатор текста v2\n\nПрактика к разделу "
          "[«Мини-проект — анализатор текста v2»](../../site/chapters/glava-13/13-25-mini-proekt-analizator-v2.html).")
    nb.md("## Цель\n\nСобрать анализатор текста из конвейера чистых функций.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''def normalize_text(text):
    return text.lower()

def split_words(text):
    return text.split()

def word_frequency(words):
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts

def build_summary(text):
    clean = normalize_text(text)
    words = split_words(clean)
    counts = word_frequency(words)
    return {
        "total_words": len(words),
        "unique_words": len(set(words)),
        "counts": counts,
    }

summary = build_summary("Python is great and python is fun")
print(summary)''')
    nb.write(OUT_DIR / "13-25-analizator-v2.ipynb")
    print(f"Записано: 13-25 ({len(nb)} ячеек)")


def build_26() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-26 · Конвертер единиц измерения\n\nПрактика к разделу "
          "[«Мини-проекты — конвертер и утилиты коллекций»](../../site/chapters/glava-13/13-26-mini-proekt-konverter-i-utility.html#konverter).")
    nb.md("## Цель\n\nНаписать набор чистых функций-конвертеров и проверить их через assert.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''def celsius_to_fahrenheit(celsius: float) -> float:
    return celsius * 9 / 5 + 32

def fahrenheit_to_celsius(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5 / 9

def km_to_miles(km: float) -> float:
    return km * 0.621371

f1 = celsius_to_fahrenheit(0)
f2 = celsius_to_fahrenheit(100)
c1 = fahrenheit_to_celsius(32)
miles = round(km_to_miles(10), 2)

assert f1 == 32
assert f2 == 212
print(f1, f2, c1, miles)''')
    nb.write(OUT_DIR / "13-26-konverter.ipynb")
    print(f"Записано: 13-26 ({len(nb)} ячеек)")


def build_27() -> None:
    nb = NotebookBuilder()
    nb.md("# 13-27 · Утилиты для коллекций\n\nПрактика к разделу "
          "[«Мини-проекты — конвертер и утилиты коллекций»](../../site/chapters/glava-13/13-26-mini-proekt-konverter-i-utility.html#utility).")
    nb.md("## Цель\n\nНебольшие сфокусированные функции поверх списков, множеств и словарей.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''def average(scores):
    return sum(scores) / len(scores)

def count_above(scores, threshold):
    return len([s for s in scores if s > threshold])

def unique_words(text):
    return set(text.lower().split())

def find_top_score(students):
    return max(students, key=lambda s: s["score"])

avg = average([70, 80, 90])
above = count_above([70, 80, 90], 75)
uniq = unique_words("Python python code")
top = find_top_score([{"name": "Anna", "score": 95}, {"name": "Bob", "score": 82}])

print(avg, above, uniq, top)''')
    nb.write(OUT_DIR / "13-27-utility-kollekcij.ipynb")
    print(f"Записано: 13-27 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_09()
    build_01()
    build_10()
    build_02()
    build_11()
    build_12()
    build_04()
    build_13()
    build_14()
    build_03()
    build_15()
    build_05()
    build_16()
    build_17()
    build_18()
    build_19()
    build_20()
    build_06()
    build_21()
    build_22()
    build_23()
    build_24()
    build_07()
    build_25()
    build_26()
    build_27()
    build_08()
