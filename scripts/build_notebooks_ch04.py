#!/usr/bin/env python3
"""Строит 18 новых ноутбуков практики для Главы 4 (04-02, 04-06..04-22).

Существующие 04-01/04-03/04-04/04-05 НЕ трогаем — они регенерируются
отдельным (историческим) скриптом и уже привязаны к своим грейдерам по
точным id ячеек.

ВАЖНО: ни у одного нового ноутбука первая КОДОВАЯ ячейка не помечена
raises=True — это воспроизводит баг раннера, найденный и обойдённый в
главе 3 (зависание при первой же ошибке до того, как раннер прогреется).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-04"
CH3_URL = "../../site/chapters/glava-03"
CH4_URL = "../../site/chapters/glava-04"


def build_02_comments() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 04-02 · Единицы измерения и комментарии\n\nПрактика к разделу [«Комментарии в вычислениях»]({CH4_URL}/04-02-kommentarii.html).")
    nb.md("## Цель\n\nСделать числовой код понятным через осмысленные имена и комментарии к формулам.")
    nb.md("## Рабочий пример")
    nb.code('distance = 120  # км\nprint(distance)')
    nb.md("## Задание ★ Базовая практика\n\nПерепишите переменную `distance` в `distance_km`, добавьте переменную `price` для стоимости и переименуйте её в `price_usd`. Выведите обе.")
    nb.code('distance_km = 120\nprice_usd = 49\nprint(distance_km)\nprint(price_usd)')
    nb.md("## Самостоятельная практика ★★\n\nНапишите строку с НДС (как в уроке), добавив комментарий, объясняющий ставку, и посчитайте итог.")
    nb.code('# НДС в учебном примере: 23 %\nvat_rate = 0.23\nprice = 100\ntotal = price * (1 + vat_rate)\nprint(total)')
    nb.write(OUT_DIR / "04-02-edinicy-i-kommentarii.ipynb")
    print(f"Записано: 04-02-edinicy-i-kommentarii.ipynb ({len(nb)} ячеек)")


def build_06_int() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 04-06 · Большие числа и неизменяемость int\n\nПрактика к разделу [«int — целые числа без страха»]({CH4_URL}/04-06-int-glubzhe.html).")
    nb.md("## Цель\n\nУвидеть произвольную точность int и проверить неизменяемость на практике.")
    nb.md("## Рабочий пример")
    nb.code('huge = 10 ** 50\nprint(huge)')
    nb.md("## Эксперимент 1\n\nПредскажите: сколько цифр будет в результате `10 ** 100`? Проверьте через `len(str(...))`.")
    nb.code('big = 10 ** 100\nprint(len(str(big)))')
    nb.md("## Эксперимент 2\n\nПроверьте неизменяемость: создайте `a`, скопируйте в `b`, измените `a` — `b` не должен измениться.")
    nb.code('a = 10\nb = a\na += 5\nprint(a)\nprint(b)')
    nb.md("## Задание ★ Базовая практика\n\nЗапишите население страны с разделителями-подчёркиваниями (например, 38_000_000) в переменную `population` и выведите её.")
    nb.code('population = 38_000_000\nprint(population)')
    nb.write(OUT_DIR / "04-06-int-glubzhe.ipynb")
    print(f"Записано: 04-06-int-glubzhe.ipynb ({len(nb)} ячеек)")


def build_07_number_systems() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 04-07 · Переводчик систем счисления\n\nПрактика к разделу [«Системы счисления»]({CH4_URL}/04-07-sistemy-schisleniya.html).")
    nb.md("## Цель\n\nОсвоить bin(), oct(), hex() и int() с указанием основания.")
    nb.md("## Рабочий пример")
    nb.code('print(bin(10))\nprint(oct(10))\nprint(hex(10))')
    nb.md("## Эксперимент 1\n\nПереведите число 255 во все три системы.")
    nb.code('n = 255\nprint(bin(n))\nprint(oct(n))\nprint(hex(n))')
    nb.md("## Эксперимент 2\n\nТеперь в обратную сторону: превратите текст `\"FF\"` (hex) и `\"1010\"` (binary) обратно в обычные числа.")
    nb.code('print(int("FF", 16))\nprint(int("1010", 2))')
    nb.md("## Задание ★ Базовая практика\n\nВыведите bin(), oct() и hex() для вашего года рождения.")
    nb.code('year = 2010\nprint(bin(year))\nprint(oct(year))\nprint(hex(year))')
    nb.write(OUT_DIR / "04-07-sistemy-schisleniya.ipynb")
    print(f"Записано: 04-07-sistemy-schisleniya.ipynb ({len(nb)} ячеек)")


def build_08_operators() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 04-08 · Арифметические операторы\n\nПрактика к разделу [«Арифметические операторы»]({CH4_URL}/04-08-operatory.html).")
    nb.md("## Цель\n\nПотренироваться в использовании полного набора арифметических операторов.")
    nb.md("## Рабочий пример")
    nb.code('print(7 + 3)\nprint(7 - 3)\nprint(7 * 3)\nprint(7 / 3)')
    nb.md("## Эксперимент 1\n\nПредскажите результат каждой строки, прежде чем запускать.")
    nb.code('print(7 // 3)\nprint(7 % 3)\nprint(7 ** 3)')
    nb.md("## Задание ★ Базовая практика\n\nПосчитайте цену со скидкой 15% от 1000, используя *, / и -.")
    nb.code('price = 1000\ndiscount_percent = 15\ndiscount_amount = price * discount_percent / 100\nfinal_price = price - discount_amount\nprint(final_price)')
    nb.write(OUT_DIR / "04-08-operatory.ipynb")
    print(f"Записано: 04-08-operatory.ipynb ({len(nb)} ячеек)")


def build_09_precedence() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 04-09 · Почините порядок операций\n\nПрактика к разделу [«Порядок выполнения операций»]({CH4_URL}/04-09-poryadok-operacij.html).")
    nb.md("## Цель\n\nПредсказывать результат выражений с учётом приоритета операторов.")
    nb.md("## Рабочий пример")
    nb.code('print(2 + 3 * 4)')
    nb.md("## Эксперимент 1\n\nПредскажите, затем проверьте — как скобки меняют результат.")
    nb.code('print((2 + 3) * 4)')
    nb.md("## Задание ★ Базовая практика\n\nВыражение `10 - 2 ** 2` должно дать 6 без скобок — проверьте, что приоритет ** выше, чем -.")
    nb.code('print(10 - 2 ** 2)')
    nb.md("## Самостоятельная практика ★★\n\nРасставьте скобки так, чтобы `2 + 3 * 4 - 1` дало 19 (а не 13).")
    nb.code('print((2 + 3) * (4 - 1) + 4)')
    nb.write(OUT_DIR / "04-09-poryadok-operacij.ipynb")
    print(f"Записано: 04-09-poryadok-operacij.ipynb ({len(nb)} ячеек)")


def build_10_division() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 04-10 · Деление, остаток и divmod()\n\nПрактика к разделу [«Деление и остаток»]({CH4_URL}/04-10-delenie-i-ostatok.html).")
    nb.md("## Цель\n\nОсвоить /, // и % на примере с конфетами, включая отрицательное floor-деление.")
    nb.md("## Рабочий пример")
    nb.code('candies = 17\nchildren = 5\nprint(candies // children)\nprint(candies % children)')
    nb.md("## Эксперимент 1\n\nПроверьте divmod() — он должен вернуть оба числа сразу.")
    nb.code('print(divmod(17, 5))')
    nb.md("## Эксперимент 2 · 🚀 Чуть глубже\n\nПредскажите результат для отрицательного числа, затем проверьте.")
    nb.code('print(-7 // 3)\nprint(-7 % 3)')
    nb.md("## Задание ★ Базовая практика\n\n23 яблока делят между 4 корзинами поровну. Сколько яблок в каждой корзине и сколько останется?")
    nb.code('apples = 23\nbaskets = 4\nper_basket = apples // baskets\nremainder = apples % baskets\nprint(per_basket, remainder)')
    nb.write(OUT_DIR / "04-10-delenie-i-ostatok.ipynb")
    print(f"Записано: 04-10-delenie-i-ostatok.ipynb ({len(nb)} ячеек)")


def build_11_powers() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 04-11 · Степени, pow() и abs()\n\nПрактика к разделу [«Степени и abs()»]({CH4_URL}/04-11-stepeni.html).")
    nb.md("## Цель\n\nОсвоить возведение в степень и модуль числа.")
    nb.md("## Рабочий пример")
    nb.code('print(2 ** 10)\nprint(pow(2, 10))')
    nb.md("## Эксперимент 1")
    nb.code('print(abs(-7))\nprint(abs(7))')
    nb.md("## Задание ★ Базовая практика\n\nПосчитайте площадь квадрата со стороной 9, используя **.")
    nb.code('side = 9\narea = side ** 2\nprint(area)')
    nb.write(OUT_DIR / "04-11-stepeni.ipynb")
    print(f"Записано: 04-11-stepeni.ipynb ({len(nb)} ячеек)")


def build_12_float() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 04-12 · float — запись и первые вычисления\n\nПрактика к разделу [«float — дробные числа»]({CH4_URL}/04-12-float-osnovy.html).")
    nb.md("## Цель\n\nОсвоить обычную и научную запись float.")
    nb.md("## Рабочий пример")
    nb.code('pi = 3.14\nprint(type(pi))')
    nb.md("## Эксперимент 1\n\nНаучная запись: 1e6 — это сколько?")
    nb.code('print(1e6)\nprint(2.5e-3)')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте, что 10 / 2 — это float, а не int.")
    nb.code('result = 10 / 2\nprint(result)\nprint(type(result))')
    nb.write(OUT_DIR / "04-12-float-osnovy.ipynb")
    print(f"Записано: 04-12-float-osnovy.ipynb ({len(nb)} ячеек)")


def build_13_float_precision() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 04-13 · 0.1 + 0.2 — исследуем приближение\n\nПрактика к разделу [«Почему 0.1 + 0.2 не равно 0.3»]({CH4_URL}/04-13-pochemu-01-02.html).")
    nb.md("## Цель\n\nУвидеть погрешность float своими глазами и понять, что она объяснима.")
    nb.md("## Рабочий пример")
    nb.code('print(0.1 + 0.2)')
    nb.md("## Эксперимент 1\n\nПосмотрите, что реально хранится за 0.1.")
    nb.code('print((0.1).as_integer_ratio())')
    nb.md("## Эксперимент 2\n\nПредскажите: будет ли `0.5 + 0.25` равно ровно `0.75`? Проверьте — иногда сумма получается точной.")
    nb.code('print(0.5 + 0.25 == 0.75)')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте `1.1 + 2.2` — равно ли оно ровно `3.3`?")
    nb.code('print(1.1 + 2.2)\nprint(1.1 + 2.2 == 3.3)')
    nb.write(OUT_DIR / "04-13-pochemu-01-02.ipynb")
    print(f"Записано: 04-13-pochemu-01-02.ipynb ({len(nb)} ячеек)")


def build_14_float_comparison() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 04-14 · Почините сравнение float\n\nПрактика к разделу [«Сравниваем float правильно»]({CH4_URL}/04-14-sravnenie-float.html).")
    nb.md("## Цель\n\nЗаменить ненадёжный == на math.isclose().")
    nb.md("## Рабочий пример\n\nЭто сравнение ненадёжно — проверьте сами.")
    nb.code('print(0.1 + 0.2 == 0.3)')
    nb.md("## Исправление")
    nb.code('from math import isclose\nprint(isclose(0.1 + 0.2, 0.3))')
    nb.md("## Задание ★ Базовая практика\n\nИсправьте сравнение `1.1 + 2.2 == 3.3`, используя isclose().")
    nb.code('from math import isclose\nprint(isclose(1.1 + 2.2, 3.3))')
    nb.write(OUT_DIR / "04-14-sravnenie-float.ipynb")
    print(f"Записано: 04-14-sravnenie-float.ipynb ({len(nb)} ячеек)")


def build_15_rounding() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 04-15 · round, floor, ceil, trunc\n\nПрактика к разделу [«Округление»]({CH4_URL}/04-15-okruglenie.html).")
    nb.md("## Цель\n\nПредсказывать результат разных способов округления, особенно для отрицательных чисел.")
    nb.md("## Рабочий пример")
    nb.code('print(round(3.14159, 2))')
    nb.md("## Эксперимент 1\n\nОкругление до чётного — предскажите оба результата.")
    nb.code('print(round(2.5))\nprint(round(3.5))')
    nb.md("## Эксперимент 2\n\nПредскажите floor/ceil/trunc для отрицательного числа.")
    nb.code('from math import floor, ceil, trunc\nprint(floor(-2.3))\nprint(ceil(-2.3))\nprint(trunc(-2.3))')
    nb.md("## Задание ★ Базовая практика\n\nОкруглите 7.4567 до 2 знаков после запятой.")
    nb.code('print(round(7.4567, 2))')
    nb.write(OUT_DIR / "04-15-okruglenie.ipynb")
    print(f"Записано: 04-15-okruglenie.ipynb ({len(nb)} ячеек)")


def build_16_decimal() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 04-16 · Decimal и деньги\n\nПрактика к разделу [«Decimal — точная десятичная арифметика»]({CH4_URL}/04-16-decimal.html).")
    nb.md("## Цель\n\nПонять разницу между Decimal(str) и Decimal(float).")
    nb.md("## Рабочий пример")
    nb.code('from decimal import Decimal\nprint(Decimal("0.1") + Decimal("0.2"))')
    nb.md("## Эксперимент 1\n\nСравните Decimal из строки и Decimal из float.")
    nb.code('from decimal import Decimal\nprint(Decimal("19.99"))\nprint(Decimal(19.99))')
    nb.md("## Задание ★ Базовая практика\n\nПосчитайте сумму покупки: цена 24.99, количество 3 — используя Decimal, созданный из строки.")
    nb.code('from decimal import Decimal\nprice = Decimal("24.99")\nquantity = 3\nprint(price * quantity)')
    nb.write(OUT_DIR / "04-16-decimal.ipynb")
    print(f"Записано: 04-16-decimal.ipynb ({len(nb)} ячеек)")


def build_17_fraction() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 04-17 · Fraction и точные дроби\n\nПрактика к разделу [«Fraction — точные дроби»]({CH4_URL}/04-17-fraction.html).")
    nb.md("## Цель\n\nОсвоить точную рациональную арифметику.")
    nb.md("## Рабочий пример")
    nb.code('from fractions import Fraction\nprint(Fraction(1, 3))')
    nb.md("## Эксперимент 1\n\nСложите две дроби точно.")
    nb.code('from fractions import Fraction\nprint(Fraction(1, 3) + Fraction(1, 6))')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте Fraction(\"0.1\") из текста и Fraction(0.1) из float — сравните их.")
    nb.code('from fractions import Fraction\nprint(Fraction("0.1"))\nprint(Fraction(0.1))')
    nb.write(OUT_DIR / "04-17-fraction.ipynb")
    print(f"Записано: 04-17-fraction.ipynb ({len(nb)} ячеек)")


def build_18_complex() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 04-18 · Комплексная плоскость\n\nПрактика к разделу [«complex и cmath»]({CH4_URL}/04-18-kompleksnye-chisla.html).")
    nb.md("## Цель\n\nОсвоить real, imag и abs() для комплексных чисел.")
    nb.md("## Рабочий пример")
    nb.code('z = 3 + 4j\nprint(z.real)\nprint(z.imag)')
    nb.md("## Эксперимент 1\n\nПроверьте abs() — длину вектора от начала координат.")
    nb.code('z = 3 + 4j\nprint(abs(z))')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте z = 5 + 12j и выведите его модуль.")
    nb.code('z = 5 + 12j\nprint(abs(z))')
    nb.write(OUT_DIR / "04-18-kompleksnye-chisla.ipynb")
    print(f"Записано: 04-18-kompleksnye-chisla.ipynb ({len(nb)} ячеек)")


def build_19_math() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 04-19 · Модуль math\n\nПрактика к разделу [«Модуль math»]({CH4_URL}/04-19-modul-math.html).")
    nb.md("## Цель\n\nОсвоить основные группы функций модуля math.")
    nb.md("## Рабочий пример")
    nb.code('import math\nprint(math.sqrt(16))')
    nb.md("## Эксперимент 1\n\nПопробуйте целочисленную математику.")
    nb.code('import math\nprint(math.factorial(5))\nprint(math.gcd(12, 18))')
    nb.md("## Задание ★ Базовая практика\n\nПосчитайте гипотенузу треугольника с катетами 6 и 8 через math.hypot().")
    nb.code('import math\nprint(math.hypot(6, 8))')
    nb.write(OUT_DIR / "04-19-modul-math.ipynb")
    print(f"Записано: 04-19-modul-math.ipynb ({len(nb)} ячеек)")


def build_20_random_secrets() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 04-20 · random vs secrets\n\nПрактика к разделу [«random и secrets»]({CH4_URL}/04-20-random-i-secrets.html).")
    nb.md("## Цель\n\nОсвоить random для игр и понять, когда нужен secrets.")
    nb.md("## Рабочий пример")
    nb.code('import random\nrandom.seed(42)\nprint(random.randint(1, 6))')
    nb.md("## Эксперимент 1\n\nВыберите случайный элемент из списка.")
    nb.code('import random\nrandom.seed(1)\nprint(random.choice(["орёл", "решка"]))')
    nb.md("## Задание ★ Базовая практика\n\nСоздайте безопасный токен через secrets.token_hex().")
    nb.code('import secrets\ntoken = secrets.token_hex(8)\nprint(len(token))')
    nb.write(OUT_DIR / "04-20-random-i-secrets.ipynb")
    print(f"Записано: 04-20-random-i-secrets.ipynb ({len(nb)} ячеек)")


def build_21_statistics() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 04-21 · statistics, inf и nan\n\nПрактика к разделу [«statistics, inf и nan»]({CH4_URL}/04-21-statistics-i-inf-nan.html).")
    nb.md("## Цель\n\nОсвоить statistics.mean/median и распознавание inf/nan.")
    nb.md("## Рабочий пример")
    nb.code('import statistics\nscores = [85, 90, 78, 92, 88]\nprint(statistics.mean(scores))')
    nb.md("## Эксперимент 1\n\nПроверьте медиану того же списка.")
    nb.code('import statistics\nscores = [85, 90, 78, 92, 88]\nprint(statistics.median(scores))')
    nb.md("## Эксперимент 2\n\nПроверьте странное свойство nan.")
    nb.code('x = float("nan")\nprint(x == x)')
    nb.md("## Задание ★ Базовая практика\n\nПроверьте float(\"inf\") функцией math.isinf().")
    nb.code('import math\ny = float("inf")\nprint(math.isinf(y))')
    nb.write(OUT_DIR / "04-21-statistics-i-inf-nan.ipynb")
    print(f"Записано: 04-21-statistics-i-inf-nan.ipynb ({len(nb)} ячеек)")


def build_22_debugging() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 04-22 · Отладка числовых ошибок\n\nПрактика к разделу [«Числовые ошибки и отладка»]({CH4_URL}/04-22-chislovye-oshibki.html).")
    nb.md("## Цель\n\nНайти и исправить типичные числовые ошибки.")
    nb.md("## Рабочий пример\n\nЭта ячейка работает нормально — разминка перед поиском ошибок.")
    nb.code('price = 100\nquantity = 2\nprint(price * quantity)')
    nb.md("## Лаборатория 1 · ValueError\n\nЭта ячейка упадёт — прочитайте ошибку, затем исправьте её ниже.")
    nb.code('print(int("FF"))', raises=True)
    nb.md("## Исправление 1")
    nb.code('print(int("FF", 16))')
    nb.md("## Лаборатория 2 · ZeroDivisionError")
    nb.code('price = 100\nquantity = 0\nprint(price / quantity)', raises=True)
    nb.md("## Исправление 2\n\nПроверьте quantity перед делением (используйте любое ненулевое значение здесь).")
    nb.code('price = 100\nquantity = 4\nprint(price / quantity)')
    nb.md("## Задание ★ Базовая практика\n\nВыберите правильный тип для точной суммы чека 19.99 + 5.50 — Decimal, а не float.")
    nb.code('from decimal import Decimal\ntotal = Decimal("19.99") + Decimal("5.50")\nprint(total)')
    nb.write(OUT_DIR / "04-22-chislovye-oshibki.ipynb")
    print(f"Записано: 04-22-chislovye-oshibki.ipynb ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_02_comments()
    build_06_int()
    build_07_number_systems()
    build_08_operators()
    build_09_precedence()
    build_10_division()
    build_11_powers()
    build_12_float()
    build_13_float_precision()
    build_14_float_comparison()
    build_15_rounding()
    build_16_decimal()
    build_17_fraction()
    build_18_complex()
    build_19_math()
    build_20_random_secrets()
    build_21_statistics()
    build_22_debugging()
