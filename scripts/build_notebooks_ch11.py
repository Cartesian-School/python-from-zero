#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 11 (списки, кортежи, множества, словари)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-11"

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
    nb.md("# 11-01 · Списки: основы\n\nПрактика к разделу "
          "[«Списки: основы»](../../site/chapters/glava-11/11-01-spiski-osnovy.html).")
    nb.md("## Цель\n\nСоздавать списки и обращаться к элементам по индексу.")
    nb.md("## Рабочий пример")
    nb.code('''fruits = ["яблоко", "банан", "вишня"]
print(fruits)
print(fruits[0])
print(fruits[-1])''')
    nb.md("## Эксперимент 1")
    nb.code('''smeshannyj = ["Cartesian", 5, 3.14, True]
for item in smeshannyj:
    print(item, type(item))''')
    nb.md("## Типичная ошибка\n\nИндекс за пределами списка вызывает IndexError.")
    nb.code('''fruits = ["яблоко", "банан", "вишня"]
fruits[10]''', raises=True)
    nb.md("## Задание ★ Базовая практика\n\nСоздайте список из пяти любимых чисел и выведите "
          "первое, последнее и третье с конца.")
    nb.code('''numbers = [7, 14, 21, 42, 100]
print(numbers[0], numbers[-1], numbers[-3])''')
    nb.write(OUT_DIR / "11-01-spiski-osnovy.ipynb")
    print(f"Записано: 11-01 ({len(nb)} ячеек)")


def build_02() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-02 · Срезы списков\n\nПрактика к разделу "
          "[«Делаем срез списка!»](../../site/chapters/glava-11/11-02-srezy-spiskov.html).")
    nb.md("## Цель\n\nОсвоить срезы списков.")
    nb.md("## Рабочий пример")
    nb.code('''chisla = [10, 20, 30, 40, 50]
print(chisla[1:3])
print(chisla[:2])
print(chisla[2:])
print(chisla[::-1])''')
    nb.md("## Задание ★ Базовая практика\n\nДостаньте средние три числа из списка `[1, 2, 3, 4, "
          "5, 6, 7]`.")
    nb.code('''numbers = [1, 2, 3, 4, 5, 6, 7]
print(numbers[2:5])''')
    nb.md("## Проверка результата")
    nb.code('''assert [1,2,3,4,5,6,7][2:5] == [3, 4, 5]
print("Верно.")''')
    nb.write(OUT_DIR / "11-02-srezy.ipynb")
    print(f"Записано: 11-02 ({len(nb)} ячеек)")


def build_03() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-03 · Мощные операции со списками\n\nПрактика к разделу "
          "[«Мощные операции со списками!»](../../site/chapters/glava-11/11-03-operacii-so-spiskami.html).")
    nb.md("## Цель\n\nОсвоить copy, append, count, clear, конкатенацию, index, insert, remove, "
          "pop, sort, reverse.")
    nb.md("## Рабочий пример")
    nb.code('''original = [1, 2, 3]
kopiya = original.copy()
kopiya.append(4)
print(original)
print(kopiya)''')
    nb.md("## Эксперимент 1 — почему copy() важен")
    nb.code('''a = [1, 2, 3]
b = a          # НЕ копия — та же ссылка!
b.append(4)
print(a)        # тоже изменился!
print(b)''')
    nb.md("## Эксперимент 2 — добавление и удаление")
    nb.code('''fruits = ["яблоко", "банан"]
fruits.append("вишня")
fruits.insert(0, "манго")
print(fruits)

fruits.remove("банан")
last = fruits.pop()
print(fruits, last)''')
    nb.md("## Задание ★ Базовая практика\n\nОтсортируйте список [5, 2, 8, 1, 9] по возрастанию "
          "и разверните.")
    nb.code('''numbers = [5, 2, 8, 1, 9]
numbers.sort()
print(numbers)
numbers.reverse()
print(numbers)''')
    nb.write(OUT_DIR / "11-03-operacii-so-spiskami.ipynb")
    print(f"Записано: 11-03 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-04 · Ещё больше о списках\n\nПрактика к разделу "
          "[«Ещё больше интересного со списками!»](../../site/chapters/glava-11/11-04-eshche-o-spiskah.html).")
    nb.md("## Цель\n\nОсвоить len/min/max/sum, вложенные списки и list comprehension.")
    nb.md("## Рабочий пример")
    nb.code('''chisla = [4, 8, 15, 16, 23, 42]
print(len(chisla), min(chisla), max(chisla), sum(chisla))''')
    nb.md("## Эксперимент 1 — вложенные списки")
    nb.code('''matrix = [[1, 2, 3], [4, 5, 6]]
print(matrix[0])
print(matrix[0][1])
print(matrix[1][2])''')
    nb.md("## Эксперимент 2 — list comprehension")
    nb.code('''kvadraty = [n ** 2 for n in range(1, 6)]
print(kvadraty)

chetnye = [n for n in range(1, 20) if n % 2 == 0]
print(chetnye)''')
    nb.md("## Задание ★ Базовая практика\n\nПостройте список кубов чисел от 1 до 10 двумя "
          "способами: циклом с append() и генератором списков.")
    nb.code('''kuby_v1 = []
for n in range(1, 11):
    kuby_v1.append(n ** 3)

kuby_v2 = [n ** 3 for n in range(1, 11)]

print(kuby_v1)
print(kuby_v1 == kuby_v2)''')
    nb.write(OUT_DIR / "11-04-eshche-o-spiskah.ipynb")
    print(f"Записано: 11-04 ({len(nb)} ячеек)")


def build_05() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-05 · Мини-проект — разноцветная звезда\n\nПрактика к разделу "
          "[«Мини-проект — автоматическая разноцветная звезда»](../../site/chapters/glava-11/11-05-mini-proekt-zvezda.html).")
    nb.md("## Цель\n\nСписок цветов + Turtle.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''artist.reset()
cveta = ["red", "orange", "yellow", "green", "blue"]

for cvet in cveta:
    artist.pencolor(cvet)
    artist.forward(150)
    artist.right(144)

artist.pencolor("black")
print("Звезда готова, лучей:", len(cveta))''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте ещё цвета в список — проверьте, что "
          "звезда автоматически подстраивается.")
    nb.code('''artist.reset()
cveta = ["red", "orange", "yellow", "green", "blue", "purple", "pink"]

for cvet in cveta:
    artist.pencolor(cvet)
    artist.forward(150)
    artist.right(144)

artist.pencolor("black")
print("Звезда с", len(cveta), "лучами готова.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "11-05-zvezda.ipynb")
    print(f"Записано: 11-05 ({len(nb)} ячеек)")


def build_06() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-06 · Кортежи\n\nПрактика к разделу "
          "[«Кортежи»](../../site/chapters/glava-11/11-06-kortezhi.html).")
    nb.md("## Цель\n\nОсвоить кортежи и распаковку.")
    nb.md("## Рабочий пример")
    nb.code('''coords = (10, 20)
print(coords)
print(coords[0])''')
    nb.md("## Типичная ошибка\n\nКортежи неизменяемы.")
    nb.code('''coords = (10, 20)
coords[0] = 99''', raises=True)
    nb.md("## Эксперимент 1 — распаковка")
    nb.code('''coords = (10, 20)
x, y = coords
print(x, y)''')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте кортеж RGB-цвета (255, 0, 128) и "
          "распакуйте его в r, g, b.")
    nb.code('''color = (255, 0, 128)
r, g, b = color
print(f"r={r}, g={g}, b={b}")''')
    nb.write(OUT_DIR / "11-06-kortezhi.ipynb")
    print(f"Записано: 11-06 ({len(nb)} ячеек)")


def build_07() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-07 · Множества\n\nПрактика к разделу "
          "[«Множества»](../../site/chapters/glava-11/11-07-mnozhestva.html).")
    nb.md("## Цель\n\nОсвоить set и операции над множествами.")
    nb.md("## Рабочий пример")
    nb.code('''chisla = {1, 2, 2, 3, 3, 3}
print(chisla)''')
    nb.md("## Эксперимент 1 — убираем повторы из списка")
    nb.code('''spisok_s_povtorami = [1, 2, 2, 3, 1, 4, 4, 4]
unikalnye = set(spisok_s_povtorami)
print(unikalnye)
print(len(unikalnye), "уникальных значений")''')
    nb.md("## Эксперимент 2 — операции над множествами")
    nb.code('''a = {1, 2, 3}
b = {2, 3, 4}
print("Объединение:", a | b)
print("Пересечение:", a & b)
print("Разность a-b:", a - b)
print("Разность b-a:", b - a)''')
    nb.md("## Задание ★ Базовая практика\n\nНайдите общих участников двух списков "
          "(пересечение множеств).")
    nb.code('''group_a = ["Аня", "Боря", "Вера", "Гриша"]
group_b = ["Вера", "Гриша", "Даша"]
common = set(group_a) & set(group_b)
print(common)''')
    nb.write(OUT_DIR / "11-07-mnozhestva.ipynb")
    print(f"Записано: 11-07 ({len(nb)} ячеек)")


def build_08() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-08 · Словари\n\nПрактика к разделу "
          "[«Словари»](../../site/chapters/glava-11/11-08-slovari.html).")
    nb.md("## Цель\n\nОсвоить создание, изменение и перебор словарей.")
    nb.md("## Рабочий пример")
    nb.code('''student = {"name": "Cartesian", "age": 12, "city": "Москва"}
print(student["name"])''')
    nb.md("## Эксперимент 1 — изменение")
    nb.code('''student["age"] = 13
student["grade"] = "7 класс"
print(student)''')
    nb.md("## Эксперимент 2 — перебор")
    nb.code('''for key, value in student.items():
    print(f"{key}: {value}")''')
    nb.md("## Типичная ошибка\n\nОбращение к несуществующему ключу вызывает KeyError.")
    nb.code('''student["phone"]''', raises=True)
    nb.md("## Исправление\n\n`.get()` безопасно возвращает None вместо ошибки.")
    nb.code('''print(student.get("phone"))
print(student.get("phone", "не указан"))  # с значением по умолчанию''')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте словарь с тремя любимыми фильмами и годами "
          "их выхода, выведите каждую пару.")
    nb.code('''films = {"Матрица": 1999, "Начало": 2010, "Интерстеллар": 2014}
for name, year in films.items():
    print(f"{name} — {year}")''')
    nb.write(OUT_DIR / "11-08-slovari.ipynb")
    print(f"Записано: 11-08 ({len(nb)} ячеек)")


def build_09() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-09 · Мини-проект — бесконечные цвета\n\nПрактика к разделу "
          "[«Мини-проект — бесконечные цвета»](../../site/chapters/glava-11/11-09-mini-proekt-cveta.html).")
    nb.md("## Цель\n\nСловарь как карта соответствий + Turtle.")
    nb.md(SETUP_MD)
    nb.code(SETUP_CODE)
    nb.md("## Рабочий пример")
    nb.code('''artist.reset()
cvetovaya_karta = {"огонь": "red", "трава": "green", "небо": "blue"}

zapros = "небо"
artist.pencolor(cvetovaya_karta[zapros])
artist.circle(50)
print("Нарисовано цветом:", cvetovaya_karta[zapros])''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте свои пары слово-цвет и нарисуйте "
          "фигуру для каждой.")
    nb.code('''artist.reset()
cvetovaya_karta = {
    "огонь": "red", "трава": "green", "небо": "blue",
    "солнце": "yellow", "ночь": "purple",
}

artist.penup()
for i, (slovo, cvet) in enumerate(cvetovaya_karta.items()):
    artist.goto(i * 60 - 120, 0)
    artist.pendown()
    artist.pencolor(cvet)
    artist.circle(20)
    artist.penup()

print("Нарисовано", len(cvetovaya_karta), "кругов.")''')
    nb.md(TEARDOWN_MD)
    nb.code(TEARDOWN_CODE)
    nb.write(OUT_DIR / "11-09-cveta.ipynb")
    print(f"Записано: 11-09 ({len(nb)} ячеек)")


def build_10() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-10 · Мини-проект — перестановка имени\n\nПрактика к разделу "
          "[«Мини-проект — перестановка имени и фамилии»](../../site/chapters/glava-11/11-10-mini-proekt-perestanovka-itogi.html).")
    nb.md("## Цель\n\nsplit() + распаковка списка.")
    md, code = input_setup(["Ада Лавлейс"])
    nb.md(md)
    nb.code(code)
    nb.md("## Рабочий пример")
    nb.code('''full_name = input("Введите имя и фамилию через пробел: ")
parts = full_name.split()
name, surname = parts

print(f"{surname} {name}")''')
    nb.md("## Задание ★★ Самостоятельная задача — три части имени")
    md2, code2 = input_setup(["Ада Августовна Лавлейс"])
    nb.md(md2)
    nb.code(code2)
    nb.code('''full_name = input("Введите имя, отчество и фамилию через пробел: ")
name, patronymic, surname = full_name.split()
initials = f"{name[0]}.{patronymic[0]}."
print(f"{surname} {initials}")''')
    nb.write(OUT_DIR / "11-10-perestanovka.ipynb")
    print(f"Записано: 11-10 ({len(nb)} ячеек)")


def build_11() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-11 · Зачем хранить много значений\n\nПрактика к разделу "
          "[«Зачем хранить много значений»](../../site/chapters/glava-11/11-11-zachem-hranit-mnogo.html).")
    nb.md("## Цель\n\nПревратить пять отдельных переменных в один список.")
    nb.md("## Рабочий пример")
    nb.code('''score_1 = 95
score_2 = 82
score_3 = 91
score_4 = 77
score_5 = 88
print(score_1, score_2, score_3, score_4, score_5)''')
    nb.md("## Задание ★ Базовая практика\n\nСоберите те же пять чисел в список `ocenki` и "
          "выведите его длину.")
    nb.code('''ocenki = [95, 82, 91, 77, 88]
print(ocenki)
print(len(ocenki))''')
    nb.write(OUT_DIR / "11-11-pyat-v-odin-spisok.ipynb")
    print(f"Записано: 11-11 ({len(nb)} ячеек)")


def build_12() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-12 · Изменяем список\n\nПрактика к разделу "
          "[«Изменяем список»](../../site/chapters/glava-11/11-12-izmenyaem-spisok.html).")
    nb.md("## Цель\n\nИзменить элемент списка по индексу.")
    nb.md("## Рабочий пример")
    nb.code('''numbers = [10, 20, 30]
numbers[1] = 999
print(numbers)''')
    nb.md("## Задание ★ Базовая практика\n\nВ списке температур на третий день (индекс 2) "
          "закралась ошибка измерения — должно быть 23, а не 19. Исправьте его на месте.")
    nb.code('''temperatures = [18, 21, 19, 25, 17]
temperatures[2] = 23
print(temperatures)''')
    nb.write(OUT_DIR / "11-12-izmenyaem-spisok.ipynb")
    print(f"Записано: 11-12 ({len(nb)} ячеек)")


def build_13() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-13 · append, extend, insert\n\nПрактика к разделу "
          "[«append, extend, insert»](../../site/chapters/glava-11/11-13-append-extend-insert.html).")
    nb.md("## Цель\n\nПравильно выбрать между append(), extend() и insert().")
    nb.md("## Рабочий пример — ловушка append() vs extend()")
    nb.code('''a = [1, 2]
a.append([3, 4])
print(a)

b = [1, 2]
b.extend([3, 4])
print(b)''')
    nb.md("## Задание ★ Базовая практика\n\nСоберите список покупок: начните с "
          "`[\"хлеб\", \"молоко\"]`, добавьте `\"яйца\"` одним элементом, добавьте элементы "
          "из `[\"сыр\", \"масло\"]`, а затем вставьте `\"вода\"` в самое начало.")
    nb.code('''cart = ["хлеб", "молоко"]
cart.append("яйца")
cart.extend(["сыр", "масло"])
cart.insert(0, "вода")
print(cart)''')
    nb.write(OUT_DIR / "11-13-append-extend-insert.ipynb")
    print(f"Записано: 11-13 ({len(nb)} ячеек)")


def build_14() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-14 · remove, pop, clear, del\n\nПрактика к разделу "
          "[«remove, pop, clear, del»](../../site/chapters/glava-11/11-14-remove-pop-clear.html).")
    nb.md("## Цель\n\nПравильно выбрать между remove(), pop() и del.")
    nb.md("## Рабочий пример")
    nb.code('''names = ["Anna", "Oleg", "Maria"]
names.remove("Oleg")
print(names)''')
    nb.md("## Задание ★ Базовая практика\n\nДано `names = [\"Anna\", \"Oleg\", \"Maria\", "
          "\"Leo\"]`. Удалите `\"Oleg\"` по значению, затем удалите и сохраните в `last` "
          "последний элемент через pop(), затем удалите первый элемент через `del`.")
    nb.code('''names = ["Anna", "Oleg", "Maria", "Leo"]
names.remove("Oleg")
last = names.pop()
del names[0]
print(names, last)''')
    nb.write(OUT_DIR / "11-14-remove-pop-clear.ipynb")
    print(f"Записано: 11-14 ({len(nb)} ячеек)")


def build_15() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-15 · Списки и циклы\n\nПрактика к разделу "
          "[«Списки и циклы»](../../site/chapters/glava-11/11-15-spiski-i-cikly.html).")
    nb.md("## Цель\n\nПеребор списка, enumerate() и фильтрация по условию.")
    nb.md("## Рабочий пример")
    nb.code('''scores = [95, 82, 91, 58, 77]
for score in scores:
    if score >= 90:
        print(score, "— отлично!")''')
    nb.md("## Задание ★ Базовая практика\n\nИз `scores` соберите список `otlichniki` (только "
          "оценки ≥ 90), и список пар `otlichniki_s_indeksami` — (индекс, оценка) для тех же "
          "значений, используя enumerate().")
    nb.code('''scores = [95, 82, 91, 58, 77]

otlichniki = []
for score in scores:
    if score >= 90:
        otlichniki.append(score)

otlichniki_s_indeksami = []
for i, score in enumerate(scores):
    if score >= 90:
        otlichniki_s_indeksami.append((i, score))

print(otlichniki)
print(otlichniki_s_indeksami)''')
    nb.write(OUT_DIR / "11-15-spiski-i-cikly.ipynb")
    print(f"Записано: 11-15 ({len(nb)} ячеек)")


def build_16() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-16 · Ссылки, aliasing, == и is\n\nПрактика к разделу "
          "[«Ссылки, aliasing, == и is»](../../site/chapters/glava-11/11-16-ssylki-aliasing.html).")
    nb.md("## Цель\n\nОтличить aliasing от копирования, == от is.")
    nb.md("## Рабочий пример")
    nb.code('''a = [1, 2, 3]
b = a
b.append(4)
print(a)
print(b)''')
    nb.md("## Задание ★ Базовая практика\n\nДано `x = [10, 20]`. Создайте `y` как "
          "НАСТОЯЩУЮ копию x через `.copy()`, добавьте в y значение 30. Затем создайте "
          "`z = [10, 20, 30]` и сравните `z` с `y` через `==` и `is`.")
    nb.code('''x = [10, 20]
y = x.copy()
y.append(30)

z = [10, 20, 30]
ravny = (z == y)
odin_i_tot_zhe = (z is y)

print(x, y, ravny, odin_i_tot_zhe)''')
    nb.write(OUT_DIR / "11-16-aliasing.ipynb")
    print(f"Записано: 11-16 ({len(nb)} ячеек)")


def build_17() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-17 · Копирование списков\n\nПрактика к разделу "
          "[«Копирование списков»](../../site/chapters/glava-11/11-17-kopirovanie-spiskov.html).")
    nb.md("## Цель\n\nУвидеть разницу между поверхностной и глубокой копией на вложенном "
          "списке.")
    nb.md("## Задание ★ Базовая практика\n\nСравните .copy() и copy.deepcopy() на списке "
          "списков: после изменения вложенного элемента через копию проверьте, изменился ли "
          "оригинал в каждом случае.")
    nb.code('''original = [["Anna", 10], ["Bob", 20]]
melkaya_kopiya = original.copy()
melkaya_kopiya[0][1] = 999
posle_melkoy = original[0][1]

import copy
original2 = [["Anna", 10], ["Bob", 20]]
glubokaya_kopiya = copy.deepcopy(original2)
glubokaya_kopiya[0][1] = 999
posle_glubokoy = original2[0][1]

print("После поверхностной копии:", posle_melkoy)
print("После глубокой копии:", posle_glubokoy)''')
    nb.write(OUT_DIR / "11-17-kopirovanie.ipynb")
    print(f"Записано: 11-17 ({len(nb)} ячеек)")


def build_18() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-18 · zip() и распаковка\n\nПрактика к разделу "
          "[«zip() и распаковка»](../../site/chapters/glava-11/11-18-zip-i-raspakovka.html).")
    nb.md("## Цель\n\nСобрать словарь через zip() и распаковать пары в цикле.")
    nb.md("## Рабочий пример")
    nb.code('''names = ["Anna", "Bob"]
scores = [95, 82]
for name, score in zip(names, scores):
    print(name, "—", score)''')
    nb.md("## Задание ★ Базовая практика\n\nСоберите словарь `itogi` из `names` и `scores` "
          "через `dict(zip(...))`, затем постройте список строк `stroki` вида "
          "`\"Имя: балл\"`, перебирая `itogi.items()`.")
    nb.code('''names = ["Anna", "Bob", "Maria"]
scores = [95, 82, 91]
itogi = dict(zip(names, scores))

stroki = []
for name, score in itogi.items():
    stroki.append(f"{name}: {score}")

print(itogi)
print(stroki)''')
    nb.write(OUT_DIR / "11-18-zip.ipynb")
    print(f"Записано: 11-18 ({len(nb)} ячеек)")


def build_19() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-19 · Операции множеств и хешируемость\n\nПрактика к разделу "
          "[«Операции множеств и хешируемость»](../../site/chapters/glava-11/11-19-mnozhestva-operacii.html).")
    nb.md("## Цель\n\nПрименить объединение, пересечение, разность и проверку подмножества.")
    nb.md("## Задание ★ Базовая практика\n\nДано `required = {\"python\", \"git\", \"sql\"}` "
          "и `available = {\"python\", \"git\", \"docker\"}`. Найдите, каких навыков не "
          "хватает (`missing`), какие уже есть (`common`), объединение всех навыков (`vse`), "
          "и проверьте, является ли `{\"python\", \"git\"}` подмножеством `available` "
          "(`podmnozhestvo`).")
    nb.code('''required = {"python", "git", "sql"}
available = {"python", "git", "docker"}

missing = required - available
common = required & available
vse = required | available
podmnozhestvo = {"python", "git"} <= available

print(missing)
print(common)
print(vse)
print(podmnozhestvo)''')
    nb.write(OUT_DIR / "11-19-mnozhestva-operacii.ipynb")
    print(f"Записано: 11-19 ({len(nb)} ячеек)")


def build_20() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-20 · Методы словарей\n\nПрактика к разделу "
          "[«Методы словарей»](../../site/chapters/glava-11/11-20-slovari-metody.html).")
    nb.md("## Цель\n\nОсвоить setdefault(), pop() и keys().")
    nb.md("## Задание ★ Базовая практика\n\nПодсчитайте, сколько раз встречается каждое "
          "слово в списке `words`, используя `setdefault()`. Сохраните отсортированный список "
          "ключей ДО удаления в `vse_klyuchi`, затем удалите ключ `\"b\"` через `.pop()`, "
          "сохранив удалённое значение в `udalyonnoe`.")
    nb.code('''words = ["a", "b", "a", "c", "b", "a"]
counts = {}
for word in words:
    counts.setdefault(word, 0)
    counts[word] += 1

vse_klyuchi = sorted(counts.keys())
udalyonnoe = counts.pop("b")

print(counts)
print(vse_klyuchi)
print(udalyonnoe)''')
    nb.write(OUT_DIR / "11-20-slovari-metody.ipynb")
    print(f"Записано: 11-20 ({len(nb)} ячеек)")


def build_21() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-21 · Вложенные структуры\n\nПрактика к разделу "
          "[«Вложенные структуры»](../../site/chapters/glava-11/11-21-vlozhennye-struktury.html).")
    nb.md("## Цель\n\nЧитать данные из списка словарей с вложенными словарями.")
    nb.md("## Задание ★ Базовая практика\n\nДостаньте оценку Anna по python, оценку Bob по "
          "математике, и соберите список всех имён.")
    nb.code('''students = [
    {"name": "Anna", "scores": {"math": 95, "python": 100}},
    {"name": "Bob", "scores": {"math": 82, "python": 78}},
]

anna_python = students[0]["scores"]["python"]
bob_math = students[1]["scores"]["math"]
imena = [student["name"] for student in students]

print(anna_python, bob_math, imena)''')
    nb.write(OUT_DIR / "11-21-vlozhennye.ipynb")
    print(f"Записано: 11-21 ({len(nb)} ячеек)")


def build_22() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-22 · Преобразования и comprehensions\n\nПрактика к разделу "
          "[«Преобразования и comprehensions»](../../site/chapters/glava-11/11-22-preobrazovaniya-i-comprehensions.html).")
    nb.md("## Цель\n\nПостроить list/set/dict comprehension.")
    nb.md("## Задание ★ Базовая практика\n\nПостройте: список квадратов чётных чисел от 1 до "
          "10 (`kvadraty_chetnyh`), множество уникальных строчных букв слова `\"Programming\"` "
          "(`bukvy`), и словарь «слово → длина» для `[\"python\", \"git\", \"sql\"]` "
          "(`slovar_dlin`) — всё через comprehension.")
    nb.code('''kvadraty_chetnyh = [n ** 2 for n in range(1, 11) if n % 2 == 0]
bukvy = {ch.lower() for ch in "Programming"}
slovar_dlin = {word: len(word) for word in ["python", "git", "sql"]}

print(kvadraty_chetnyh)
print(sorted(bukvy))
print(slovar_dlin)''')
    nb.write(OUT_DIR / "11-22-comprehensions.ipynb")
    print(f"Записано: 11-22 ({len(nb)} ячеек)")


def build_23() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-23 · Как выбрать правильную структуру\n\nПрактика к разделу "
          "[«Как выбрать правильную структуру»](../../site/chapters/glava-11/11-23-vybor-struktury.html).")
    nb.md("## Цель\n\nВыбрать подходящую коллекцию под сценарий.")
    nb.md("## Задание ★ Базовая практика\n\nДля каждого сценария запишите название "
          "подходящего типа (`\"list\"`, `\"tuple\"`, `\"set\"` или `\"dict\"`) в "
          "соответствующую переменную:\n\n"
          "1. `otvet_1` — хранение профиля пользователя: имя → email.\n"
          "2. `otvet_2` — список уникальных ID посетителей, порядок не важен.\n"
          "3. `otvet_3` — координата точки, которая не должна меняться.\n"
          "4. `otvet_4` — список покупок, который будем пополнять и вычёркивать.")
    nb.code('''otvet_1 = "dict"
otvet_2 = "set"
otvet_3 = "tuple"
otvet_4 = "list"
print(otvet_1, otvet_2, otvet_3, otvet_4)''')
    nb.write(OUT_DIR / "11-23-vybor-struktury.ipynb")
    print(f"Записано: 11-23 ({len(nb)} ячеек)")


def build_24() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-24 · Отладка коллекций\n\nПрактика к разделу "
          "[«Отладка коллекций: 14 типичных ошибок»](../../site/chapters/glava-11/11-24-debugging-kollekcij.html).")
    nb.md("## Цель\n\nНайти и исправить типичные ошибки в коде с коллекциями.")
    nb.md("## Сломанный код (не выполняем)\n\n```python\ntovary = [\"хлеб\"]\n"
          "tovary.append([\"молоко\", \"яйца\"])   # баг: список внутри списка\n```")
    nb.md("## Задание ★ Базовая практика — исправьте append() → extend()")
    nb.code('''tovary = ["хлеб"]
tovary.extend(["молоко", "яйца"])
print(tovary)''')
    nb.md("## Задание ★★ Самостоятельная задача — исправьте потерю списка через "
          "`x = x.sort()`")
    nb.code('''chisla = [5, 3, 1, 4]
chisla.sort()
print(chisla)''')
    nb.write(OUT_DIR / "11-24-najdi-oshibku.ipynb")
    print(f"Записано: 11-24 ({len(nb)} ячеек)")


def build_25() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-25 · Мини-проект — частота слов\n\nПрактика к разделу "
          "[«Мини-проект — подсчёт частоты слов»](../../site/chapters/glava-11/11-25-slovar-chastoty-slov.html).")
    nb.md("## Цель\n\nПодсчитать частоту слов в тексте через словарь.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''text = "python is great and python is fun and simple"
words = text.lower().split()

counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1

print(counts)''')
    nb.write(OUT_DIR / "11-25-chastota-slov.ipynb")
    print(f"Записано: 11-25 ({len(nb)} ячеек)")


def build_26() -> None:
    nb = NotebookBuilder()
    nb.md("# 11-26 · Мини-проекты с коллекциями\n\nПрактика к разделу "
          "[«Мини-проекты с коллекциями»](../../site/chapters/glava-11/11-26-mini-proekty-kollekcii.html).")
    nb.md("## Цель\n\nЗаписная книжка (dict) + сравнение множеств навыков в одном задании.")
    nb.md("## Задание ★ Базовая практика")
    nb.code('''contacts = {"Anna": "anna@example.com", "Bob": "bob@example.com"}
contacts["Maria"] = "maria@example.com"
contacts["Anna"] = "anna.new@example.com"
del contacts["Bob"]

required = {"python", "git", "sql"}
available = {"python", "git"}
missing = required - available

print(contacts)
print(missing)''')
    nb.write(OUT_DIR / "11-26-mini-proekty.ipynb")
    print(f"Записано: 11-26 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_11()
    build_01()
    build_02()
    build_12()
    build_13()
    build_14()
    build_03()
    build_15()
    build_16()
    build_17()
    build_04()
    build_05()
    build_06()
    build_18()
    build_07()
    build_19()
    build_08()
    build_20()
    build_21()
    build_22()
    build_09()
    build_23()
    build_24()
    build_25()
    build_26()
    build_10()
