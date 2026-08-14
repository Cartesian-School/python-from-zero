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
