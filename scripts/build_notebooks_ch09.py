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


def build_07() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-07 · Алгоритмы и команды\n\nПрактика к разделу "
          "[«Алгоритмы и команды»](../../site/chapters/glava-09/09-07-algoritmy-i-komandy.html).")
    nb.md("## Цель\n\nПроследить последовательное выполнение команд и предсказать значения переменных.")
    nb.md("## Рабочий пример")
    nb.code('''print("Старт")
x = 5
print(x)
print("Конец")''')
    nb.md("## Задание ★ Базовая практика\n\nПроследите программу вручную (не запуская), "
          "предскажите значения `b` и `c`, затем проверьте себя.")
    nb.code('''a = 5
b = a + 3
c = b * 2
print(b, c)''')
    nb.write(OUT_DIR / "09-07-algoritmy-i-komandy.ipynb")
    print(f"Записано: 09-07 ({len(nb)} ячеек)")


def build_08() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-08 · Три структуры алгоритма и ветвление\n\nПрактика к разделу "
          "[«Три структуры алгоритма и ветвление»](../../site/chapters/glava-09/09-08-tri-struktury-i-vetvlenie.html).")
    nb.md("## Цель\n\nОтличить последовательный алгоритм от ветвящегося и построить первую развилку.")
    nb.md("## Рабочий пример")
    nb.code('''is_raining = True
if is_raining:
    action = "взять зонт"
else:
    action = "без зонта"
print(action)''')
    nb.md("## Задание ★ Базовая практика\n\nПостройте ту же развилку для `is_raining = True` и "
          "зафиксируйте, что в программе есть ветвление (`has_branch`).")
    nb.code('''is_raining = True
if is_raining:
    action = "взять зонт"
else:
    action = "без зонта"
has_branch = True
print(action, has_branch)''')
    nb.write(OUT_DIR / "09-08-tri-struktury-i-vetvlenie.ipynb")
    print(f"Записано: 09-08 ({len(nb)} ячеек)")


def build_09() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-09 · Чем отличаются = и ==, и как сравнивать строки\n\nПрактика к разделу "
          "[«Чем отличаются = и ==, и как сравнивать строки»](../../site/chapters/glava-09/09-09-ravno-i-sravnenie-strok.html).")
    nb.md("## Цель\n\nНе путать = и ==, освоить != и сравнение строк.")
    nb.md("## Рабочий пример")
    nb.code('''name = "Anna"
print(name == "Anna")''')
    nb.md("## Типичная ошибка\n\nОдиночный `=` внутри условия — синтаксическая ошибка.")
    nb.code('''age = 20
if age = 20:
    print("Совпадает")''', raises=True)
    nb.md("## Исправление")
    nb.code('''age = 20
if age == 20:
    print("Совпадает")''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте возраст через `==`, сравните два слова по "
          "алфавиту и сравните строки без учёта регистра через `.lower()`.")
    nb.code('''age = 20
is_adult = age == 20
apple_before_banana = "apple" < "banana"
same_case_insensitive = "Python".lower() == "python".lower()
print(is_adult, apple_before_banana, same_case_insensitive)''')
    nb.write(OUT_DIR / "09-09-ravno-i-sravnenie-strok.ipynb")
    print(f"Записано: 09-09 ({len(nb)} ячеек)")


def build_10() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-10 · Цепочки сравнений\n\nПрактика к разделу "
          "[«Цепочки сравнений»](../../site/chapters/glava-09/09-10-cepochki-sravnenij.html).")
    nb.md("## Цель\n\nОсвоить запись вида a <= x <= b для проверки диапазона.")
    nb.md("## Рабочий пример")
    nb.code('''age = 30
print(18 <= age <= 65)''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте, входит ли age=30 в диапазон 18..65, и "
          "входит ли score=105 в диапазон 0..100.")
    nb.code('''age = 30
in_range = 18 <= age <= 65

score = 105
valid_score = 0 <= score <= 100
print(in_range, valid_score)''')
    nb.write(OUT_DIR / "09-10-cepochki-sravnenij.ipynb")
    print(f"Записано: 09-10 ({len(nb)} ячеек)")


def build_11() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-11 · Truthiness и None\n\nПрактика к разделу "
          "[«Truthiness и None»](../../site/chapters/glava-09/09-11-truthiness-i-none.html).")
    nb.md("## Цель\n\nОсвоить truthiness и правильную проверку на None.")
    nb.md("## Рабочий пример")
    nb.code('''value = None
print(value is None)
print(bool(value))''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте value на None через `is`, и проверьте "
          "truthiness строки \"False\" и числа 0.")
    nb.code('''value = None
is_none = value is None
truthy_check = bool("False")
falsy_check = bool(0)
print(is_none, truthy_check, falsy_check)''')
    nb.write(OUT_DIR / "09-11-truthiness-i-none.ipynb")
    print(f"Записано: 09-11 ({len(nb)} ячеек)")


def build_12() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-12 · elif-лестница\n\nПрактика к разделу "
          "[«elif — несколько вариантов»](../../site/chapters/glava-09/09-12-elif-lestnica.html).")
    nb.md("## Цель\n\nПостроить цепочку elif и убедиться, что порядок условий важен.")
    nb.md("## Рабочий пример")
    nb.code('''temperature = -5
if temperature < 0:
    result = "мороз"
elif temperature < 15:
    result = "прохладно"
elif temperature < 25:
    result = "комфортно"
else:
    result = "жарко"
print(result)''')
    nb.md("## Задание ★ Базовая практика\n\nПрогоните ту же лестницу для temperature = 10 и "
          "предскажите результат заранее.")
    nb.code('''temperature = 10
if temperature < 0:
    result = "мороз"
elif temperature < 15:
    result = "прохладно"
elif temperature < 25:
    result = "комфортно"
else:
    result = "жарко"
print(result)''')
    nb.write(OUT_DIR / "09-12-elif-lestnica.ipynb")
    print(f"Записано: 09-12 ({len(nb)} ячеек)")


def build_13() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-13 · Несколько if ≠ if/elif/else\n\nПрактика к разделу "
          "[«Несколько if ≠ if/elif/else»](../../site/chapters/glava-09/09-13-neskolko-if-protiv-elif.html).")
    nb.md("## Цель\n\nУвидеть разницу между независимыми if и цепочкой elif.")
    nb.md("## Рабочий пример")
    nb.code('''temperature = 30
if temperature > 20:
    print("тепло")
if temperature > 25:
    print("жарко")''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте, сработают ли ОБА независимых условия "
          "одновременно для temperature = 30.")
    nb.code('''temperature = 30
warm_triggered = temperature > 20
hot_triggered = temperature > 25
both_triggered = warm_triggered and hot_triggered
print(warm_triggered, hot_triggered, both_triggered)''')
    nb.write(OUT_DIR / "09-13-neskolko-if-protiv-elif.ipynb")
    print(f"Записано: 09-13 ({len(nb)} ячеек)")


def build_14() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-14 · and\n\nПрактика к разделу "
          "[«and — все условия сразу»](../../site/chapters/glava-09/09-14-and.html).")
    nb.md("## Цель\n\nОсвоить and — все условия должны быть True.")
    nb.md("## Рабочий пример")
    nb.code('''age = 20
has_ticket = True
print(age >= 18 and has_ticket)''')
    nb.md("## Задание ★ Базовая практика\n\nПостройте can_enter — True, только если age >= 18 "
          "И has_ticket одновременно.")
    nb.code('''age = 20
has_ticket = True
can_enter = age >= 18 and has_ticket
print(can_enter)''')
    nb.write(OUT_DIR / "09-14-and.ipynb")
    print(f"Записано: 09-14 ({len(nb)} ячеек)")


def build_15() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-15 · or\n\nПрактика к разделу "
          "[«or — хотя бы одно»](../../site/chapters/glava-09/09-15-or.html).")
    nb.md("## Цель\n\nОсвоить or — достаточно одного истинного условия.")
    nb.md("## Рабочий пример")
    nb.code('''is_student = False
is_senior = True
print(is_student or is_senior)''')
    nb.md("## Задание ★ Базовая практика\n\nПостройте can_rest — True, если is_weekend ИЛИ "
          "is_holiday истинно.")
    nb.code('''is_weekend = False
is_holiday = True
can_rest = is_weekend or is_holiday
print(can_rest)''')
    nb.write(OUT_DIR / "09-15-or.ipynb")
    print(f"Записано: 09-15 ({len(nb)} ячеек)")


def build_16() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-16 · not\n\nПрактика к разделу "
          "[«not — переворачиваем условие»](../../site/chapters/glava-09/09-16-not.html).")
    nb.md("## Цель\n\nОсвоить not — инверсию логического значения.")
    nb.md("## Рабочий пример")
    nb.code('''is_raining = False
print(not is_raining)''')
    nb.md("## Задание ★ Базовая практика\n\nПостройте can_walk через not, и проверьте двойное "
          "not.")
    nb.code('''is_raining = False
can_walk = not is_raining
double_negative = not not True
print(can_walk, double_negative)''')
    nb.write(OUT_DIR / "09-16-not.ipynb")
    print(f"Записано: 09-16 ({len(nb)} ячеек)")


def build_17() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-17 · Short-circuit\n\nПрактика к разделу "
          "[«Short-circuit: Python иногда ленится»](../../site/chapters/glava-09/09-17-short-circuit.html).")
    nb.md("## Цель\n\nУвидеть, как short-circuit защищает от IndexError.")
    nb.md("## Рабочий пример")
    nb.code('''name = "Anna"
print(name and name[0] == "A")''')
    nb.md("## Типичная ошибка\n\nБез short-circuit порядок операндов может вызвать IndexError.")
    nb.code('''name = ""
print(name[0] == "A" and name)''', raises=True)
    nb.md("## Исправление")
    nb.code('''name = ""
safe_check = name and name[0] == "A"
print(bool(safe_check))''')
    nb.md("## Задание ★ Базовая практика\n\nПовторите безопасную проверку для пустой строки — "
          "убедитесь, что она НЕ вызывает ошибку.")
    nb.code('''name = ""
safe_check = name and name[0] == "A"
print(bool(safe_check))''')
    nb.write(OUT_DIR / "09-17-short-circuit.ipynb")
    print(f"Записано: 09-17 ({len(nb)} ячеек)")


def build_18() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-18 · in / not in\n\nПрактика к разделу "
          "[«in / not in как условие»](../../site/chapters/glava-09/09-18-in-not-in.html).")
    nb.md("## Цель\n\nИспользовать in/not in прямо в условиях.")
    nb.md("## Рабочий пример")
    nb.code('''text = "python"
print("py" in text)''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте вхождение подстроки и проверьте ответ "
          "пользователя на принадлежность группе допустимых значений.")
    nb.code('''text = "python"
has_py = "py" in text

answer = "да"
is_yes = answer in ("да", "yes", "y")
print(has_py, is_yes)''')
    nb.write(OUT_DIR / "09-18-in-not-in.ipynb")
    print(f"Записано: 09-18 ({len(nb)} ячеек)")


def build_19() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-19 · is против ==\n\nПрактика к разделу "
          "[«is против ==»](../../site/chapters/glava-09/09-19-is-vs-ravno.html).")
    nb.md("## Цель\n\nПравильно использовать is для None и == для значений.")
    nb.md("## Рабочий пример")
    nb.code('''value = None
print(value is None)''')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте None через is, и обычное числовое "
          "значение через ==.")
    nb.code('''value = None
is_none_check = value is None

value2 = 5
equals_check = value2 == 5
print(is_none_check, equals_check)''')
    nb.write(OUT_DIR / "09-19-is-vs-ravno.ipynb")
    print(f"Записано: 09-19 ({len(nb)} ячеек)")


def build_20() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-20 · Вложенные условия\n\nПрактика к разделу "
          "[«Вложенные условия»](../../site/chapters/glava-09/09-20-vlozhennye-uslovija.html).")
    nb.md("## Цель\n\nПостроить вложенное условие для проверки входа в аккаунт.")
    nb.md("## Рабочий пример")
    nb.code('''has_account = True
password_ok = True
if has_account:
    if password_ok:
        print("Добро пожаловать")
    else:
        print("Неверный пароль")
else:
    print("Зарегистрируйтесь")''')
    nb.md("## Задание ★ Базовая практика\n\nПовторите с password_ok = False и убедитесь, что "
          "выбирается правильная вложенная ветка.")
    nb.code('''has_account = True
password_ok = False
if has_account:
    if password_ok:
        result = "Добро пожаловать"
    else:
        result = "Неверный пароль"
else:
    result = "Зарегистрируйтесь"
print(result)''')
    nb.write(OUT_DIR / "09-20-vlozhennye-uslovija.ipynb")
    print(f"Записано: 09-20 ({len(nb)} ячеек)")


def build_21() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-21 · Проектируем условие\n\nПрактика к разделу "
          "[«Проектируем условие: ввод, валидация, границы»](../../site/chapters/glava-09/09-21-proektirovanie-uslovij.html).")
    nb.md("## Цель\n\nУвидеть off-by-one ошибку на границах диапазона.")
    nb.md("## Рабочий пример")
    nb.code('''number = 1
print(1 <= number <= 10)
print(1 < number < 10)''')
    nb.md("## Задание ★ Базовая практика\n\nСравните правильную (включительно) и ошибочную "
          "(строгую) проверку границы для number = 1.")
    nb.code('''number = 1
in_range_correct = 1 <= number <= 10
in_range_buggy = 1 < number < 10
print(in_range_correct, in_range_buggy)''')
    nb.write(OUT_DIR / "09-21-proektirovanie-uslovij.ipynb")
    print(f"Записано: 09-21 ({len(nb)} ячеек)")


def build_22() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-22 · Отладка логических ошибок\n\nПрактика к разделу "
          "[«Отладка логических ошибок»](../../site/chapters/glava-09/09-22-otladka-logiki.html).")
    nb.md("## Цель\n\nРазложить сложное условие на части, чтобы найти причину неверного результата.")
    nb.md("## Рабочий пример")
    nb.code('''age = 20
has_ticket = False
eligible = age >= 18 and has_ticket
print("age >= 18:", age >= 18)
print("has_ticket:", has_ticket)
print("eligible:", eligible)''')
    nb.md("## Задание ★ Базовая практика\n\nПовторите разбор условия по частям — сохраните "
          "промежуточный результат age_ok отдельно от итогового eligible.")
    nb.code('''age = 20
has_ticket = False
age_ok = age >= 18
eligible = age_ok and has_ticket
print(age_ok, eligible)''')
    nb.write(OUT_DIR / "09-22-otladka-logiki.ipynb")
    print(f"Записано: 09-22 ({len(nb)} ячеек)")


def build_23() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-23 · Клуб и советчик погоды\n\nПрактика к разделу "
          "[«Мини-проекты: клуб и погода»](../../site/chapters/glava-09/09-23-mini-proekt-klub-i-pogoda.html).")
    nb.md("## Цель\n\nСобрать два мини-проекта на комбинирование условий.")
    md, code = input_setup(["20", "да"])
    nb.md(md)
    nb.code(code)
    nb.md("## Рабочий пример — клуб")
    nb.code('''age = int(input("Ваш возраст: "))
has_ticket = input("У вас есть билет? (да/нет): ").strip().lower() == "да"
club_access = age >= 18 and has_ticket
print(club_access)''')
    nb.md("## Задание ★ Базовая практика — советчик погоды\n\nПостройте рекомендацию по погоде "
          "для temperature = 5, is_raining = True.")
    nb.code('''temperature = 5
is_raining = True
if temperature < 10 and is_raining:
    advice = "тёплая куртка и зонт"
elif temperature < 10:
    advice = "тёплая куртка"
elif is_raining:
    advice = "просто зонт"
else:
    advice = "лёгкая одежда"
print(advice)''')
    nb.write(OUT_DIR / "09-23-mini-proekt-klub-i-pogoda.ipynb")
    print(f"Записано: 09-23 ({len(nb)} ячеек)")


def build_24() -> None:
    nb = NotebookBuilder()
    nb.md("# 09-24 · Оценки и команды\n\nПрактика к разделу "
          "[«Мини-проекты: оценки и команды»](../../site/chapters/glava-09/09-24-mini-proekt-ocenki-i-komandy.html).")
    nb.md("## Цель\n\nСобрать классификатор баллов и текстовый интерпретатор команд.")
    nb.md("## Рабочий пример")
    nb.code('''score = 82
if score >= 90:
    level = "отлично"
elif score >= 75:
    level = "хорошо"
elif score >= 50:
    level = "удовлетворительно"
else:
    level = "неудовлетворительно"
print(level)''')
    nb.md("## Задание ★ Базовая практика\n\nПовторите классификацию для score = 82, и постройте "
          "интерпретатор команд для command = \"START\" (с нормализацией регистра).")
    nb.code('''score = 82
if score >= 90:
    level = "отлично"
elif score >= 75:
    level = "хорошо"
elif score >= 50:
    level = "удовлетворительно"
else:
    level = "неудовлетворительно"

command = "START".strip().lower()
if command == "start":
    action = "Запуск..."
elif command == "stop":
    action = "Остановка..."
else:
    action = "Неизвестная команда"
print(level, action)''')
    nb.write(OUT_DIR / "09-24-mini-proekt-ocenki-i-komandy.ipynb")
    print(f"Записано: 09-24 ({len(nb)} ячеек)")


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
