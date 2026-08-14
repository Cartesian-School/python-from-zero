#!/usr/bin/env python3
"""Строит ноутбуки практики для Главы 9 (условия)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-09"


def input_setup(answers: list[str]) -> tuple[str, str]:
    md = (
        "## Про input() в этом ноутбуке\n\n"
        "Этот ноутбук выполняется автоматически, без живого человека за клавиатурой — поэтому "
        "здесь `input()` временно подменён на заранее заготовленные ответы. Сам код с `input()` "
        "ниже выглядит и работает точно так же, как в обычном файле."
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
    nb.md("# 09-01 · Истина или ложь\n\nПрактика к разделу "
          "[«Истина или ложь»](../../site/chapters/glava-09/09-01-istina-ili-lozh.html).")
    nb.md("## Цель\n\nОсвоить тип bool и истинность значений разных типов.")
    nb.md("## Рабочий пример")
    nb.code('''is_sunny = True
print(is_sunny, type(is_sunny))''')
    nb.md("## Эксперимент 1")
    nb.code('''print(bool(0))
print(bool(42))
print(bool(""))
print(bool("нет"))''')
    nb.md("## Эксперимент 2 — неожиданный случай")
    nb.code('''print(bool("False"))   # True! строка непустая, значит "истина"
print(bool([]))        # пустой список — тоже "ложь", забегаем немного вперёд (глава 11)''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте истинность пяти разных значений на свой "
          "выбор — включая хотя бы одно, для которого результат неочевиден заранее.")
    nb.code('''for value in [0, 1, -1, "", " ", "0"]:
    print(repr(value), "->", bool(value))''')
    nb.write(OUT_DIR / "09-01-istina-lozh.ipynb")
    print(f"Записано: 09-01 ({len(nb)} ячеек)")


def build_02() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-02 · Сравниваем и принимаем решение\n\nПрактика к разделу "
          "[«Сравниваем и принимаем решение»](../../site/chapters/glava-09/09-02-sravnenie-i-reshenie.html).")
    nb.md("## Цель\n\nОсвоить все шесть операторов сравнения.")
    nb.md("## Рабочий пример")
    nb.code('''print(5 == 5)
print(5 != 3)
print(5 > 3, 5 < 3)
print(5 >= 5, 5 <= 3)''')
    nb.md("## Типичная ошибка\n\nПутаница между `=` (присваивание) и `==` (сравнение).")
    nb.code('''age = 20
if age = 20:
    print("Совпадает")''', raises=True)
    nb.md("## Исправление")
    nb.code('''age = 20
if age == 20:
    print("Совпадает")''')
    nb.md("## Задание ★ Базовая практика\n\nСравните две строки по алфавиту.")
    nb.code('''print("apple" < "banana")
print("Python" == "python")''')
    nb.write(OUT_DIR / "09-02-sravnenie.ipynb")
    print(f"Записано: 09-02 ({len(nb)} ячеек)")


def build_03() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-03 · if / else\n\nПрактика к разделу "
          "[«Если это произошло — выполни команду!»](../../site/chapters/glava-09/09-03-if-inache.html).")
    nb.md("## Цель\n\nОсвоить условный оператор if и его альтернативу else.")
    nb.md("## Рабочий пример")
    nb.code('''age = 20
if age >= 18:
    print("Доступ разрешён.")''')
    nb.md("## Эксперимент 1")
    nb.code('''age = 15
if age >= 18:
    print("Доступ разрешён.")
else:
    print("Доступ запрещён — вам ещё нет 18.")''')
    nb.md("## Типичная ошибка\n\nПропущенный отступ вызывает IndentationError.")
    nb.code('''age = 20
if age >= 18:
print("Доступ разрешён.")''', raises=True)
    nb.md("## Исправление")
    nb.code('''age = 20
if age >= 18:
    print("Доступ разрешён.")''')
    nb.md("## Задание ★ Базовая практика\n\nНапишите проверку чётности числа с if/else "
          "(используем `%` из главы 5).")
    nb.code('''number = 17
if number % 2 == 0:
    print(f"{number} — чётное")
else:
    print(f"{number} — нечётное")''')
    nb.write(OUT_DIR / "09-03-if-else.ipynb")
    print(f"Записано: 09-03 ({len(nb)} ячеек)")


def build_04() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-04 · and, or, not\n\nПрактика к разделу "
          "[«Больше одного условия!»](../../site/chapters/glava-09/09-04-neskolko-uslovij.html).")
    nb.md("## Цель\n\nКомбинировать условия логическими операторами.")
    nb.md("## Рабочий пример")
    nb.code('''age = 20
has_ticket = True
if age >= 18 and has_ticket:
    print("Проходите в зал.")''')
    nb.md("## Эксперимент 1 — or")
    nb.code('''is_weekend = False
is_holiday = True
if is_weekend or is_holiday:
    print("Сегодня можно не ходить на работу.")''')
    nb.md("## Эксперимент 2 — таблица истинности")
    nb.code('''for a in [True, False]:
    for b in [True, False]:
        print(a, "and", b, "=", a and b, " | ", a, "or", b, "=", a or b)''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте, подходит ли кандидат: возраст от 18 до "
          "65 включительно (два условия через and).")
    nb.code('''age = 30
if age >= 18 and age <= 65:
    print("Подходит по возрасту.")
else:
    print("Не подходит по возрасту.")''')
    nb.md("## Дополнительная задача ★★★\n\nТо же самое, но через сцепленное сравнение Python "
          "`18 <= age <= 65` — более короткая и «питоничная» форма того же условия.")
    nb.code('''age = 30
if 18 <= age <= 65:
    print("Подходит по возрасту (сцепленное сравнение).")''')
    nb.write(OUT_DIR / "09-04-and-or-not.ipynb")
    print(f"Записано: 09-04 ({len(nb)} ячеек)")


def build_05() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-05 · Мини-проект — «Угадай число»\n\nПрактика к разделу "
          "[«Мини-проект — игра «Угадай число»»](../../site/chapters/glava-09/09-05-mini-proekt-ugadaj-chislo.html).")
    nb.md("## Цель\n\nСобрать первую мини-игру книги.")
    nb.md("""\
## О случайности в этом ноутбуке

Игра использует `random.randint()`, поэтому результат зависит от случайного числа. Чтобы
ноутбук выполнялся предсказуемо (и его можно было автоматически проверить), здесь мы
дополнительно закрепляем случайность через `random.seed()` — в обычной игре это не нужно.""")
    md, code = input_setup(["10"])
    nb.md(md)
    nb.code(code)
    nb.md("## Рабочий пример")
    nb.code('''import random

random.seed(42)  # закрепляем случайность для повторяемого результата в ноутбуке
zagadannoe = random.randint(1, 20)
popytka = int(input("Угадайте число от 1 до 20: "))

if popytka == zagadannoe:
    print("Поздравляем, вы угадали!")
elif popytka < zagadannoe:
    print(f"Мимо! Загаданное число больше, чем {popytka}.")
else:
    print(f"Мимо! Загаданное число меньше, чем {popytka}.")

print(f"Загаданное число было: {zagadannoe}")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте подсказку «Очень близко!», если "
          "разница между попыткой и загаданным числом меньше 3.")
    md2, code2 = input_setup(["8"])
    nb.md(md2)
    nb.code(code2)
    nb.code('''import random

random.seed(42)
zagadannoe = random.randint(1, 20)
popytka = int(input("Угадайте число от 1 до 20: "))

if popytka == zagadannoe:
    print("Поздравляем, вы угадали!")
elif abs(popytka - zagadannoe) < 3:
    print("Очень близко!")
elif popytka < zagadannoe:
    print(f"Мимо! Загаданное число больше, чем {popytka}.")
else:
    print(f"Мимо! Загаданное число меньше, чем {popytka}.")

print(f"Загаданное число было: {zagadannoe}")''')
    nb.write(OUT_DIR / "09-05-ugadaj-chislo.ipynb")
    print(f"Записано: 09-05 ({len(nb)} ячеек)")


def build_06() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-06 · elif и вложенные условия\n\nПрактика к разделу "
          "[«Условия продолжают накапливаться!»](../../site/chapters/glava-09/09-06-nakoplenie-uslovij-itogi.html).")
    nb.md("## Цель\n\nОсвоить цепочки elif и вложенные условия.")
    nb.md("## Рабочий пример")
    nb.code('''ocenka = 87
if ocenka >= 90:
    bukva = "A"
elif ocenka >= 80:
    bukva = "B"
elif ocenka >= 70:
    bukva = "C"
else:
    bukva = "D"

print(f"Оценка: {bukva}")''')
    nb.md("## Эксперимент 1\n\nПроверьте несколько разных оценок через цикл (забегая немного "
          "вперёд, глава 10).")
    nb.code('''for ocenka in [95, 82, 71, 40]:
    if ocenka >= 90:
        bukva = "A"
    elif ocenka >= 80:
        bukva = "B"
    elif ocenka >= 70:
        bukva = "C"
    else:
        bukva = "D"
    print(ocenka, "->", bukva)''')
    nb.md("## Эксперимент 2 — вложенные условия")
    nb.code('''age = 25
has_license = True

if age >= 18:
    if has_license:
        print("Можно водить машину.")
    else:
        print("Сначала получите права.")
else:
    print("Ещё рано водить машину.")''')
    nb.md("## Задание ★★ Самостоятельная задача\n\nДобавьте третий уровень вложенности: "
          "проверку наличия топлива (`has_fuel`).")
    nb.code('''age = 25
has_license = True
has_fuel = False

if age >= 18:
    if has_license:
        if has_fuel:
            print("Можно ехать!")
        else:
            print("Права есть, но бак пуст.")
    else:
        print("Сначала получите права.")
else:
    print("Ещё рано водить машину.")''')
    nb.write(OUT_DIR / "09-06-elif.ipynb")
    print(f"Записано: 09-06 ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_01()
    build_02()
    build_03()
    build_04()
    build_05()
    build_06()
