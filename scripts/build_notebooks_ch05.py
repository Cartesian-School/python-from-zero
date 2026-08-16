#!/usr/bin/env python3
"""Строит 15 новых ноутбуков практики для Главы 5 (05-07..05-21, кроме уже
существующих 05-01/05-02/05-04/05-05/05-06 — их НЕ трогаем).

ВАЖНО: ни у одного нового ноутбука первая КОДОВАЯ ячейка не помечена
raises=True — воспроизводит баг раннера из главы 3 (зависание при первой же
ошибке до того, как раннер прогреется).

Для ноутбуков, завязанных на random, «Задание» всегда начинается с
random.seed(N) — фиксированный seed делает результат воспроизводимым и
пригодным для нефлакового грейдера (см. секцию 66 спецификации).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from notebook_lib import NotebookBuilder

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "notebooks" / "chapter-05"
CH5_URL = "../../site/chapters/glava-05"


def build_07_division_remainder() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 05-07 · Деление с остатком\n\nПрактика к разделу [«Деление с остатком»]({CH5_URL}/05-07-delenie-s-ostatkom.html).")
    nb.md("## Цель\n\nОсвоить //, % и divmod() на реальных задачах группировки.")
    nb.md("## Рабочий пример")
    nb.code("candies = 17\ngroup_size = 5\nprint(candies // group_size)\nprint(candies % group_size)")
    nb.md("## Эксперимент 1\n\nПроверьте divmod() — он должен вернуть оба числа сразу, как кортеж.")
    nb.code("print(divmod(17, 5))")
    nb.md("## Задание ★ Базовая практика\n\n22 участника делят на команды по 4 человека. Сколько получится полных команд и сколько человек останется без команды? Выведите оба числа через пробел одним print().")
    nb.code("uchastniki = 22\nrazmer_komandy = 4\nkomand, ostatok = divmod(uchastniki, razmer_komandy)\nprint(komand, ostatok)")
    nb.write(OUT_DIR / "05-07-delenie-s-ostatkom.ipynb")
    print(f"Записано: 05-07-delenie-s-ostatkom.ipynb ({len(nb)} ячеек)")


def build_08_negative_division() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 05-08 · Отрицательное floor-деление\n\nПрактика к разделу [«Отрицательное floor-деление»]({CH5_URL}/05-08-otricatelnoe-delenie.html).")
    nb.md("## Цель\n\nПредсказывать результат // и % для отрицательных чисел.")
    nb.md("## Рабочий пример")
    nb.code("print(-7 // 2)\nprint(-7 % 2)")
    nb.md("## Эксперимент 1 · Предскажите перед запуском\n\nПредскажите результат, затем проверьте.")
    nb.code("print(7 // -2)\nprint(7 % -2)")
    nb.md("## Задание ★ Базовая практика\n\nВыведите `-17 // 5` и `-17 % 5` через пробел одним print().")
    nb.code("print(-17 // 5, -17 % 5)")
    nb.write(OUT_DIR / "05-08-otricatelnoe-delenie.ipynb")
    print(f"Записано: 05-08-otricatelnoe-delenie.ipynb ({len(nb)} ячеек)")


def build_09_unary_operators() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 05-09 · Унарные операторы\n\nПрактика к разделу [«Унарные операторы»]({CH5_URL}/05-09-unarnye-operatory.html).")
    nb.md("## Цель\n\nРазобраться, почему -2 ** 2 не равно (-2) ** 2.")
    nb.md("## Рабочий пример")
    nb.code("print(-2 ** 2)\nprint((-2) ** 2)")
    nb.md("## Задание ★ Базовая практика\n\nВыведите `-3 ** 2` и `(-3) ** 2` через пробел одним print() — числа должны быть разными.")
    nb.code("print(-3 ** 2, (-3) ** 2)")
    nb.write(OUT_DIR / "05-09-unarnye-operatory.ipynb")
    print(f"Записано: 05-09-unarnye-operatory.ipynb ({len(nb)} ячеек)")


def build_10_associativity() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 05-10 · Ассоциативность операторов\n\nПрактика к разделу [«Ассоциативность операторов»]({CH5_URL}/05-10-associativnost.html).")
    nb.md("## Цель\n\nУвидеть на практике, что ** — правоассоциативно, а большинство операторов — левоассоциативны.")
    nb.md("## Рабочий пример")
    nb.code("print(2 ** 3 ** 2)     # 512, а не 64")
    nb.md("## Эксперимент 1\n\nСравните левую ассоциативность вычитания.")
    nb.code("print(20 - 5 - 3)      # (20 - 5) - 3 = 12, а не 20 - (5 - 3) = 18")
    nb.md("## Задание ★ Базовая практика\n\nВыведите `2 ** 2 ** 3` — из-за правой ассоциативности это 2 ** (2 ** 3), а не (2 ** 2) ** 3.")
    nb.code("print(2 ** 2 ** 3)")
    nb.write(OUT_DIR / "05-10-associativnost.ipynb")
    print(f"Записано: 05-10-associativnost.ipynb ({len(nb)} ячеек)")


def build_11_parentheses_formulas() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 05-11 · Скобки и формулы из переменных\n\nПрактика к разделу [«Скобки и формулы из переменных»]({CH5_URL}/05-11-skobki-i-formuly.html).")
    nb.md("## Цель\n\nСтроить формулы из именованных переменных и не забывать скобки там, где они меняют смысл.")
    nb.md("## Рабочий пример")
    nb.code("shirina = 6\nvysota = 3\nperimetr = 2 * (shirina + vysota)\nprint(perimetr)")
    nb.md("## Задание ★ Базовая практика\n\nПосчитайте среднее трёх чисел a, b, c = 10, 20, 30 (не забудьте скобки вокруг суммы!) и выведите результат.")
    nb.code("a, b, c = 10, 20, 30\nsrednee = (a + b + c) / 3\nprint(srednee)")
    nb.write(OUT_DIR / "05-11-skobki-i-formuly.ipynb")
    print(f"Записано: 05-11-skobki-i-formuly.ipynb ({len(nb)} ячеек)")


def build_12_formula_translation() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 05-12 · Перевод формул: математика → Python\n\nПрактика к разделу [«Перевод формул: математика → Python»]({CH5_URL}/05-12-perevod-formul.html).")
    nb.md("## Цель\n\nПеревести формулу x² + 2x + 1 из математической записи в Python.")
    nb.md("## Рабочий пример")
    nb.code("x = 3\nprint(x ** 2 + 2 * x + 1)")
    nb.md("## Задание ★ Базовая практика\n\nПереведите формулу x² + 2x + 1 в Python для x = 5 и выведите результат (ожидается 36).")
    nb.code("x = 5\nrezultat = x ** 2 + 2 * x + 1\nprint(rezultat)")
    nb.write(OUT_DIR / "05-12-perevod-formul.ipynb")
    print(f"Записано: 05-12-perevod-formul.ipynb ({len(nb)} ячеек)")


def build_13_roots_distances() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 05-13 · Корни и расстояния\n\nПрактика к разделу [«Корни и расстояния»]({CH5_URL}/05-13-korni-rasstoyaniya.html).")
    nb.md("## Цель\n\nОсвоить math.isqrt(), math.hypot() и math.dist() на геометрических задачах.")
    nb.md("## Рабочий пример")
    nb.code("import math\nprint(math.hypot(3, 4))")
    nb.md("## Эксперимент 1\n\nСравните isqrt() с обычным sqrt().")
    nb.code("import math\nprint(math.sqrt(10))\nprint(math.isqrt(10))")
    nb.md("## Задание ★ Базовая практика\n\nНайдите расстояние между точками (0, 0) и (6, 8) через math.dist() и выведите результат.")
    nb.code("import math\nA = (0, 0)\nB = (6, 8)\nprint(math.dist(A, B))")
    nb.write(OUT_DIR / "05-13-korni-rasstoyaniya.ipynb")
    print(f"Записано: 05-13-korni-rasstoyaniya.ipynb ({len(nb)} ячеек)")


def build_14_gcd_lcm_factorial() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 05-14 · gcd, lcm, факториал, comb, perm\n\nПрактика к разделу [«gcd, lcm, факториал, comb, perm»]({CH5_URL}/05-14-gcd-lcm-faktorial.html).")
    nb.md("## Цель\n\nОсвоить пять функций math для целых чисел и подсчёта вариантов.")
    nb.md("## Рабочий пример")
    nb.code("import math\nprint(math.gcd(12, 18))\nprint(math.lcm(4, 6))")
    nb.md("## Эксперимент 1\n\nСравните comb() и perm() для одних и тех же чисел.")
    nb.code("import math\nprint(math.comb(6, 2))\nprint(math.perm(6, 2))")
    nb.md("## Задание ★ Базовая практика\n\nНайдите НОД(48, 18) и число сочетаний из 6 по 2 — выведите оба числа через пробел одним print() (ожидается `6 15`).")
    nb.code("import math\nprint(math.gcd(48, 18), math.comb(6, 2))")
    nb.write(OUT_DIR / "05-14-gcd-lcm-faktorial.ipynb")
    print(f"Записано: 05-14-gcd-lcm-faktorial.ipynb ({len(nb)} ячеек)")


def build_15_geometry() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 05-15 · Геометрия с math\n\nПрактика к разделу [«Геометрия с math»]({CH5_URL}/05-15-geometriya-s-math.html).")
    nb.md("## Цель\n\nСчитать площадь и длину окружности через math.pi.")
    nb.md("## Рабочий пример")
    nb.code("import math\nradius = 4\nprint(round(math.pi * radius ** 2, 2))")
    nb.md("## Задание ★ Базовая практика\n\nПосчитайте площадь круга радиусом 10, округлите до 2 знаков и выведите (ожидается 314.16).")
    nb.code("import math\nradius = 10\nploshad = math.pi * radius ** 2\nprint(round(ploshad, 2))")
    nb.write(OUT_DIR / "05-15-geometriya-s-math.ipynb")
    print(f"Записано: 05-15-geometriya-s-math.ipynb ({len(nb)} ячеек)")


def build_16_trigonometry() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 05-16 · Тригонометрия без страха\n\nПрактика к разделу [«Тригонометрия без страха»]({CH5_URL}/05-16-trigonometriya.html).")
    nb.md("## Цель\n\nПеревести градусы в радианы и посчитать sin/cos ключевых углов.")
    nb.md("## Рабочий пример")
    nb.code("import math\nprint(math.radians(180))\nprint(math.degrees(math.pi))")
    nb.md("## Задание ★ Базовая практика\n\nПосчитайте sin(90°), округлив до 2 знаков (не забудьте перевести градусы в радианы!). Ожидается 1.0.")
    nb.code("import math\nugol_radiany = math.radians(90)\nprint(round(math.sin(ugol_radiany), 2))")
    nb.write(OUT_DIR / "05-16-trigonometriya.ipynb")
    print(f"Записано: 05-16-trigonometriya.ipynb ({len(nb)} ячеек)")


def build_17_logarithms() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 05-17 · Логарифмы и экспоненты\n\nПрактика к разделу [«Логарифмы и экспоненты»]({CH5_URL}/05-17-logarifmy.html).")
    nb.md("## Цель\n\nПонять логарифм как обратную операцию к степени.")
    nb.md("## Рабочий пример")
    nb.code("import math\nprint(2 ** 3)\nprint(math.log2(8))")
    nb.md("## Задание ★ Базовая практика\n\nПосчитайте log2(1024) и выведите результат (ожидается 10.0).")
    nb.code("import math\nprint(math.log2(1024))")
    nb.write(OUT_DIR / "05-17-logarifmy.ipynb")
    print(f"Записано: 05-17-logarifmy.ipynb ({len(nb)} ячеек)")


def build_18_randint_randrange_uniform() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 05-18 · randint, randrange, uniform\n\nПрактика к разделу [«randint, randrange, uniform»]({CH5_URL}/05-18-randint-randrange-uniform.html).")
    nb.md("## Цель\n\nОсвоить разницу между randint() (обе границы включены) и randrange() (верхняя не включена).")
    nb.md("## Рабочий пример")
    nb.code("import random\nprint(random.randint(1, 6))")
    nb.md("## Эксперимент 1\n\nrandrange(1, 7) — аналог randint(1, 6), потому что верхняя граница не включена.")
    nb.code("import random\nprint(random.randrange(1, 7))")
    nb.md("## Задание ★ Базовая практика\n\nЗафиксируйте `random.seed(1)`, затем выведите `random.randint(1, 10)` — с этим seed результат всегда одинаковый (ожидается 3), что позволяет проверить задание автоматически.")
    nb.code("import random\nrandom.seed(1)\nprint(random.randint(1, 10))")
    nb.write(OUT_DIR / "05-18-randint-randrange-uniform.ipynb")
    print(f"Записано: 05-18-randint-randrange-uniform.ipynb ({len(nb)} ячеек)")


def build_19_choice_sample_shuffle() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 05-19 · choice, choices, sample, shuffle\n\nПрактика к разделу [«choice, choices, sample, shuffle»]({CH5_URL}/05-19-choice-sample-shuffle.html).")
    nb.md("## Цель\n\nРазличать выбор с повторами (choices) и без повторов (sample).")
    nb.md("## Рабочий пример")
    nb.code('import random\nvarianty = ["камень", "ножницы", "бумага"]\nprint(random.choice(varianty))')
    nb.md("## Задание ★ Базовая практика\n\nЗафиксируйте `random.seed(3)`, затем выведите `random.sample(range(1, 6), k=3)` — три разных числа без повторов (ожидается `[2, 5, 4]`).")
    nb.code("import random\nrandom.seed(3)\nprint(random.sample(range(1, 6), k=3))")
    nb.write(OUT_DIR / "05-19-choice-sample-shuffle.ipynb")
    print(f"Записано: 05-19-choice-sample-shuffle.ipynb ({len(nb)} ячеек)")


def build_20_seed() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 05-20 · seed и воспроизводимость\n\nПрактика к разделу [«seed и воспроизводимость»]({CH5_URL}/05-20-seed.html).")
    nb.md("## Цель\n\nУбедиться, что одинаковый seed даёт одинаковую последовательность случайных чисел.")
    nb.md("## Рабочий пример")
    nb.code("import random\nrandom.seed(42)\nprint(random.randint(1, 100))\nrandom.seed(42)\nprint(random.randint(1, 100))")
    nb.md("## Задание ★ Базовая практика\n\nЗафиксируйте `random.seed(5)`, затем выведите `random.randint(1, 100)` (ожидается 80 — тот же результат каждый раз при этом seed).")
    nb.code("import random\nrandom.seed(5)\nprint(random.randint(1, 100))")
    nb.write(OUT_DIR / "05-20-seed.ipynb")
    print(f"Записано: 05-20-seed.ipynb ({len(nb)} ячеек)")


def build_21_debugging() -> None:
    nb = NotebookBuilder()
    nb.md(f"# 05-21 · Отладка вычислений\n\nПрактика к разделу [«Отладка вычислений»]({CH5_URL}/05-21-otladka-vychislenij.html).")
    nb.md("## Цель\n\nНайти и исправить ошибку приоритета операций в готовой формуле.")
    nb.md("## Типичная ошибка\n\nЭта формула должна была посчитать среднее трёх оценок, но забыла скобки — результат неверен.")
    nb.code("ocenka1, ocenka2, ocenka3 = 4, 5, 3\nsrednyaya_s_oshibkoj = ocenka1 + ocenka2 + ocenka3 / 3\nprint(srednyaya_s_oshibkoj)   # 10.0 — неверно! это НЕ среднее трёх оценок")
    nb.md("## Задание ★ Базовая практика\n\nИсправьте формулу так, чтобы она правильно считала среднее трёх оценок (добавьте скобки вокруг суммы). Ожидается 4.0.")
    nb.code("ocenka1, ocenka2, ocenka3 = 4, 5, 3\nsrednyaya = (ocenka1 + ocenka2 + ocenka3) / 3\nprint(srednyaya)")
    nb.write(OUT_DIR / "05-21-otladka-vychislenij.ipynb")
    print(f"Записано: 05-21-otladka-vychislenij.ipynb ({len(nb)} ячеек)")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_07_division_remainder()
    build_08_negative_division()
    build_09_unary_operators()
    build_10_associativity()
    build_11_parentheses_formulas()
    build_12_formula_translation()
    build_13_roots_distances()
    build_14_gcd_lcm_factorial()
    build_15_geometry()
    build_16_trigonometry()
    build_17_logarithms()
    build_18_randint_randrange_uniform()
    build_19_choice_sample_shuffle()
    build_20_seed()
    build_21_debugging()
    print("Все 15 новых ноутбуков главы 5 собраны.")
