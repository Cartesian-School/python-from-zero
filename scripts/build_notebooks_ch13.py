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
