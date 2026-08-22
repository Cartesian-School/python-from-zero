#!/usr/bin/env python3
"""Строит Главу 5: «Давайте поиграем с числами!» (site/chapters/glava-05/).

Curriculum v2: от короткой главы про операторы до полноценного курса
математических вычислений — что такое выражение, базовые и специальные
операторы (с геометрической визуализацией каждого!), приоритет и
ассоциативность, перевод формул из математики в Python, модуль math
(корни, расстояния, gcd/lcm/factorial/comb/perm, геометрия,
тригонометрия, логарифмы), модуль random (концепция псевдослучайности,
randint/randrange/uniform, choice/choices/sample/shuffle, seed), отладка
вычислений, и пять мини-проектов. Существующие маршруты (index,
05-01..05-06) сохранены и расширены на месте; новый материал добавлен как
новые страницы.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_lib import (
    ChapterSectionLink,
    NavItem,
    PageNav,
    SidebarGroup,
    branch_diagram,
    callout,
    capability_map,
    code_block,
    comparison_table,
    coordinate_plane_diagram,
    decision_map,
    exercise,
    expression_tree,
    fraction_bar_diagram,
    grouping_diagram,
    math_formula,
    math_inline,
    number_line_diagram,
    precedence_ladder,
    practice_card,
    rectangle_grid_diagram,
    render_chapter_opener,
    render_page,
    right_triangle_diagram,
    square_area_diagram,
    step_reduction_diagram,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-05"
IMG = "../../assets/img"

PAGES = [
    ("index.html", "Приступаем"),
    ("05-01-osnovnye-operacii.html", "Выражения и основные операции"),
    ("05-07-delenie-s-ostatkom.html", "Деление с остатком"),
    ("05-08-otricatelnoe-delenie.html", "Отрицательное floor-деление"),
    ("05-02-specialnye-operacii.html", "Степени и корни"),
    ("05-09-unarnye-operatory.html", "Унарные операторы"),
    ("05-03-prisvaivanie-poryadok.html", "Присваивание и порядок вычислений"),
    ("05-10-associativnost.html", "Ассоциативность операторов"),
    ("05-11-skobki-i-formuly.html", "Скобки и формулы из переменных"),
    ("05-12-perevod-formul.html", "Перевод формул: математика → Python"),
    ("05-04-matematicheskie-funkcii.html", "Модуль math — карта возможностей"),
    ("05-13-korni-rasstoyaniya.html", "Корни и расстояния"),
    ("05-14-gcd-lcm-faktorial.html", "gcd, lcm, факториал, comb, perm"),
    ("05-15-geometriya-s-math.html", "Геометрия с math"),
    ("05-16-trigonometriya.html", "Тригонометрия без страха"),
    ("05-17-logarifmy.html", "Логарифмы и экспоненты"),
    ("05-05-sluchaynye-chisla.html", "Модуль random: псевдослучайность"),
    ("05-18-randint-randrange-uniform.html", "randint, randrange, uniform"),
    ("05-19-choice-sample-shuffle.html", "choice, choices, sample, shuffle"),
    ("05-20-seed.html", "seed и воспроизводимость"),
    ("05-21-otladka-vychislenij.html", "Отладка вычислений"),
    ("05-06-mini-proekt-itogi.html", "Мини-проекты и итоги"),
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    practice_ids = ["05-01", "05-07", "05-08", "05-02", "05-09", "05-10",
                     "05-11", "05-12", "05-04", "05-13", "05-14", "05-15", "05-16",
                     "05-17", "05-05", "05-18", "05-19", "05-20", "05-21", "05-06"]
    return [
        SidebarGroup("Глава 5 · Числа играют", items),
        SidebarGroup("Практика", [
            NavItem(f"🐍 {pid}: Практика", f"../../practice/{pid}/index.html") for pid in practice_ids
        ]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=5,
        baseline_page=59,
        title="Давайте поиграем с числами!",
        description="Глубокое погружение в математические вычисления Python: выражения, "
        "операторы и их приоритет, перевод формул из математики в код, модуль math "
        "(корни, геометрия, тригонометрия, логарифмы), модуль random "
        "(псевдослучайность, seed, воспроизводимость) и отладка вычислений.",
        meta_items=["⏱ ~4 часа", "🧮 math и random в деталях", "📓 21 практика"],
        sections=[
            ChapterSectionLink("5.1", "Выражения и основные операции", "05-01-osnovnye-operacii.html", "60"),
            ChapterSectionLink("5.2", "Деление с остатком", "05-07-delenie-s-ostatkom.html", "62"),
            ChapterSectionLink("5.3", "Отрицательное floor-деление", "05-08-otricatelnoe-delenie.html", ""),
            ChapterSectionLink("5.4", "Степени и корни", "05-02-specialnye-operacii.html", ""),
            ChapterSectionLink("5.5", "Унарные операторы", "05-09-unarnye-operatory.html", ""),
            ChapterSectionLink("5.6", "Присваивание и порядок вычислений", "05-03-prisvaivanie-poryadok.html", "65"),
            ChapterSectionLink("5.7", "Ассоциативность операторов", "05-10-associativnost.html", ""),
            ChapterSectionLink("5.8", "Скобки и формулы из переменных", "05-11-skobki-i-formuly.html", ""),
            ChapterSectionLink("5.9", "Перевод формул: математика → Python", "05-12-perevod-formul.html", ""),
            ChapterSectionLink("5.10", "Модуль math — карта возможностей", "05-04-matematicheskie-funkcii.html", "70"),
            ChapterSectionLink("5.11", "Корни и расстояния", "05-13-korni-rasstoyaniya.html", ""),
            ChapterSectionLink("5.12", "gcd, lcm, факториал, comb, perm", "05-14-gcd-lcm-faktorial.html", ""),
            ChapterSectionLink("5.13", "Геометрия с math", "05-15-geometriya-s-math.html", ""),
            ChapterSectionLink("5.14", "Тригонометрия без страха", "05-16-trigonometriya.html", ""),
            ChapterSectionLink("5.15", "Логарифмы и экспоненты", "05-17-logarifmy.html", ""),
            ChapterSectionLink("5.16", "Модуль random: псевдослучайность", "05-05-sluchaynye-chisla.html", "75"),
            ChapterSectionLink("5.17", "randint, randrange, uniform", "05-18-randint-randrange-uniform.html", ""),
            ChapterSectionLink("5.18", "choice, choices, sample, shuffle", "05-19-choice-sample-shuffle.html", ""),
            ChapterSectionLink("5.19", "seed и воспроизводимость", "05-20-seed.html", ""),
            ChapterSectionLink("5.20", "Отладка вычислений", "05-21-otladka-vychislenij.html", ""),
            ChapterSectionLink("5.21", "Мини-проекты и итоги", "05-06-mini-proekt-itogi.html", "78"),
        ],
    )
    write("index.html", out)


def build_01_expressions() -> None:
    body = f"""
    <p>В главе 4 мы разобрались, что такое числа. Теперь научим Python по-настоящему с ними
    работать — считать, сравнивать, комбинировать. Начнём с самого главного слова этой главы:
    <strong>выражение</strong>.</p>

    <h2>Что такое выражение</h2>
    <p><code class="inline">5 + 3</code> — это <strong>выражение</strong>: у него есть
    <strong>операнды</strong> (значения, с которыми работаем — <code class="inline">5</code> и
    <code class="inline">3</code>) и <strong>оператор</strong> (действие — <code class="inline">+</code>).
    У любого выражения есть результат — само выражение можно подставить туда, где ожидается значение:</p>
{code_block(
        "vyrazhenie.py",
        "print(5 + 3)        # выражение прямо внутри print()\n"
        "summa = 5 + 3       # результат выражения сохранён в переменную\n"
        "print(summa * 2)    # summa — тоже операнд в новом выражении\n",
    )}
{callout(
        "info",
        "Выражение — не то же самое, что команда (statement)",
        "<code class=\"inline\">summa = 5 + 3</code> целиком — это <strong>инструкция</strong> "
        "(присваивание), а <code class=\"inline\">5 + 3</code> внутри неё — "
        "<strong>выражение</strong>: у выражения всегда есть значение, у инструкции — нет. "
        "Именно поэтому <code class=\"inline\">print(x = 5)</code> — ошибка "
        "(<code class=\"inline\">x = 5</code> ничего не возвращает), а "
        "<code class=\"inline\">print(x == 5)</code> — нормальный код.",
    )}

    <h2>Сложение и вычитание — движение по числовой прямой</h2>
    <p>Самая простая модель для <code class="inline">+</code> и <code class="inline">-</code> —
    прыжок по числовой прямой: сложение прыгает вправо, вычитание — влево.</p>
{number_line_diagram(
        [(3, "3"), (7, "7")],
        lo=0, hi=10,
        jumps=[(3, 7, "+4")],
        caption="3 + 4 = 7 — прыжок на 4 шага вправо от точки 3",
    )}
{code_block("slozhenie.py", "print(3 + 4)    # 7 — прыжок вправо\nprint(3 - 4)    # -1 — прыжок влево, можно уйти в отрицательные числа\n")}

    <h2>Умножение — прямоугольник из клеток</h2>
    <p>Умножение <code class="inline">a * b</code> — это площадь прямоугольника со сторонами
    <code class="inline">a</code> и <code class="inline">b</code>: ряды по <code class="inline">a</code>
    клеток, и таких рядов <code class="inline">b</code> штук.</p>
{rectangle_grid_diagram(4, 3, caption="4 × 3 = 12 — 3 ряда по 4 клетки")}
{code_block("umnozhenie.py", "print(4 * 3)    # 12\nprint(4 * 0)    # 0 — прямоугольник без высоты не имеет площади\n")}

    <h2>Деление — всегда дробное число</h2>
    <p>В Python <code class="inline">/</code> — это <strong>обычное деление</strong>, и оно
    <strong>всегда</strong> возвращает <code class="inline">float</code>, даже если числа делятся
    нацело:</p>
{code_block("delenie.py", "print(6 / 3)    # 2.0 — float, а не 2\nprint(7 / 2)    # 3.5\n")}
{callout(
        "warning",
        "На ноль делить нельзя",
        "<code class=\"inline\">5 / 0</code> вызывает <code class=\"inline\">ZeroDivisionError</code> "
        "— Python не придумывает результат сам, а честно сообщает, что операция не имеет смысла.",
    )}

    <h2>Операторы и реальная жизнь</h2>
{comparison_table(
        ["Оператор", "Что делает", "Пример из жизни"],
        [
            ["<code class=\"inline\">+</code>", "сложение", "сумма чеков в корзине"],
            ["<code class=\"inline\">-</code>", "вычитание", "остаток на счету после покупки"],
            ["<code class=\"inline\">*</code>", "умножение", "цена × количество товара"],
            ["<code class=\"inline\">/</code>", "деление", "сумма счёта, делённая между друзьями"],
        ],
    )}
    <p>Про <code class="inline">//</code> (целочисленное деление) и <code class="inline">%</code>
    (остаток) — в следующем разделе: это отдельная и очень важная тема.</p>

{practice_card(
        "05-01",
        "Практика: выражения и +, -, *, /",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-01/index.html",
    )}
    """
    out = render_page(
        page_title="Выражения и основные операции",
        description="Что такое выражение в Python, и как работают +, -, * и / — с геометрической визуализацией каждой операции.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Выражения и основные операции", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Выражения и основные операции",
        lede="Выражение — операнды плюс оператор. Начнём с четырёх операций, знакомых из школы "
        "— но теперь увидим их не только в коде, а и на числовой прямой, и в виде прямоугольника.",
        body_html=body,
        sidebar_groups=sidebar("05-01-osnovnye-operacii.html"),
        nav=PageNav(prev_href="index.html", prev_label="Приступаем", next_href="05-07-delenie-s-ostatkom.html", next_label="Деление с остатком"),
    )
    write("05-01-osnovnye-operacii.html", out)


def build_07_division_remainder() -> None:
    body = f"""
    <p>Кроме обычного деления <code class="inline">/</code>, у Python есть два оператора, которых
    нет на школьном калькуляторе, но без них не обходится почти ни одна программа.</p>

    <h2>Целочисленное деление <code class="inline">//</code></h2>
    <p>Возвращает только целую часть результата — «сколько раз одно число помещается в другое
    целиком». Представим 17 конфет, которые раскладываем по пакетикам по 5 штук:</p>
{grouping_diagram(17, 5, caption="17 конфет по 5 в пакетике — 3 полных пакетика и 2 конфеты остались")}
{code_block("celochislennoe.py", "print(17 // 5)   # 3 — три полных пакетика\nprint(17 / 5)    # 3.4 — обычное деление, для сравнения\n")}

    <h2>Остаток от деления <code class="inline">%</code></h2>
    <p>Возвращает то, что <strong>осталось</strong> после раскладывания по пакетикам — на схеме
    выше это 2 конфеты. Один из самых полезных операторов в программировании: например, для
    проверки чётности числа.</p>
{code_block("ostatok.py", "print(17 % 5)    # 2 — именно столько осталось\nprint(10 % 2)    # 0 — если остаток 0, число чётное\nprint(11 % 2)    # 1 — а если 1 — нечётное\n")}
{callout(
        "tip",
        "Проверка чётности — классический приём",
        "<code class=\"inline\">число % 2 == 0</code> — самый частый способ проверить, чётное "
        "ли число. Этот приём встретится ещё много раз в курсе.",
    )}

    <h2><code class="inline">divmod()</code> — оба результата сразу</h2>
    <p>Если нужны и целая часть, и остаток одновременно, не обязательно писать
    <code class="inline">//</code> и <code class="inline">%</code> отдельно — есть встроенная
    функция <code class="inline">divmod()</code>:</p>
{code_block("divmod_primer.py", "print(divmod(17, 5))   # (3, 2) — кортеж: целая часть и остаток\nchast, ostatok = divmod(17, 5)\nprint(chast, ostatok)  # 3 2\n")}

    <h2>Реальные примеры</h2>
{comparison_table(
        ["Задача", "Выражение", "Результат"],
        [
            ["Сколько полных команд по 4 человека из 22", "<code class=\"inline\">22 // 4</code>", "5"],
            ["Сколько человек останется без команды", "<code class=\"inline\">22 % 4</code>", "2"],
            ["Сколько часов и минут в 137 минутах", "<code class=\"inline\">divmod(137, 60)</code>", "(2, 17)"],
        ],
    )}

{practice_card(
        "05-07",
        "Практика: //, % и divmod()",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-07/index.html",
    )}
    """
    out = render_page(
        page_title="Деление с остатком",
        description="Целочисленное деление //, остаток % и divmod() в Python — с визуальной моделью группировки.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Деление с остатком", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Деление с остатком",
        lede="Раскладываем числа по группам — и знакомимся с двумя операторами, которых нет на "
        "обычном калькуляторе.",
        body_html=body,
        sidebar_groups=sidebar("05-07-delenie-s-ostatkom.html"),
        nav=PageNav(prev_href="05-01-osnovnye-operacii.html", prev_label="Выражения и основные операции", next_href="05-08-otricatelnoe-delenie.html", next_label="Отрицательное floor-деление"),
    )
    write("05-07-delenie-s-ostatkom.html", out)


def build_08_negative_division() -> None:
    body = f"""
    <p>Что будет, если разделить с остатком <strong>отрицательное</strong> число? Здесь Python
    ведёт себя иначе, чем многие ожидают из школы — и это важно понять сейчас, а не в момент
    отладки.</p>

    <h2>Округление всегда вниз — то есть к минус бесконечности</h2>
    <p><code class="inline">//</code> в Python называется <em>floor division</em> — «деление с
    округлением к полу» (floor). Пол — это округление в сторону <strong>меньшего</strong> числа,
    и для отрицательных чисел «меньшее» означает «более отрицательное»:</p>
{number_line_diagram(
        [(-4, "-4"), (-3.5, "")],
        lo=-6, hi=1,
        highlight=-4,
        caption="-7 // 2 = -4 — округление к полу означает движение ВЛЕВО по числовой прямой, к −∞",
    )}
{code_block("otricatelnoe_floor.py", "print(-7 // 2)    # -4, а не -3! Python округляет к минус бесконечности\nprint(7 // 2)     # 3 — для положительных чисел разницы с округлением 'к нулю' нет\nprint(-7 / 2)     # -3.5 — обычное деление честно показывает дробную часть\n")}
{callout(
        "warning",
        "Не 'округление к нулю', как в некоторых языках",
        "В части других языков программирования <code class=\"inline\">-7 // 2</code> дало бы "
        "<code class=\"inline\">-3</code> (округление к нулю). В Python результат — "
        "<code class=\"inline\">-4</code>: это осознанный выбор языка, чтобы формула ниже "
        "работала всегда, без исключений для отрицательных чисел.",
    )}

    <h2>Остаток при отрицательном делении</h2>
    <p>Знак остатка в Python всегда совпадает со знаком <strong>делителя</strong>:</p>
{code_block("otricatelnyj_ostatok.py", "print(-7 % 2)     # 1 — остаток положителен, потому что делитель (2) положителен\nprint(7 % -2)     # -1 — остаток отрицателен, потому что делитель (-2) отрицателен\n")}

    <h2>Тождество, которое работает всегда</h2>
    <p>Как бы ни менялись знаки, для любых <code class="inline">a</code> и
    <code class="inline">b</code> (кроме деления на 0) верно:</p>
{step_reduction_diagram(
        ["a == (a // b) * b + a % b", "-7 == (-7 // 2) * 2 + (-7 % 2)", "-7 == (-4) * 2 + 1", "-7 == -8 + 1", "-7 == -7  ✓"],
        caption="Тождество деления с остатком проверено на примере -7 и 2",
    )}
{code_block("tozhdestvo.py", "a, b = -7, 2\nprint((a // b) * b + a % b == a)   # True — тождество работает всегда\n")}

{practice_card(
        "05-08",
        "Практика: отрицательное floor-деление",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-08/index.html",
    )}
    """
    out = render_page(
        page_title="Отрицательное floor-деление",
        description="Почему -7 // 2 равно -4, а не -3 — округление к полу (минус бесконечности) в Python.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Отрицательное floor-деление", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Отрицательное floor-деление",
        lede="Самая частая неожиданность в этой теме — что делает // с отрицательными числами. "
        "Разбираемся на числовой прямой.",
        body_html=body,
        sidebar_groups=sidebar("05-08-otricatelnoe-delenie.html"),
        nav=PageNav(prev_href="05-07-delenie-s-ostatkom.html", prev_label="Деление с остатком", next_href="05-02-specialnye-operacii.html", next_label="Степени и корни"),
    )
    write("05-08-otricatelnoe-delenie.html", out)


def build_02_powers_roots() -> None:
    body = f"""
    <p>Теперь — операция, у которой самая красивая геометрическая картинка из всех: возведение в
    степень.</p>

    <h2>Квадрат числа — это площадь квадрата</h2>
    <p><code class="inline">x ** 2</code> — площадь квадрата со стороной <code class="inline">x</code>:</p>
{square_area_diagram(4, caption="4 ** 2 = 16 — площадь квадрата со стороной 4")}
{code_block("kvadrat.py", "print(4 ** 2)    # 16\nprint(4 ** 3)    # 64 — куб: та же идея, но в трёх измерениях (объём)\n")}

    <h2>Квадратный корень — обратная операция: от площади к стороне</h2>
    <p>Если известна площадь квадрата, можно найти длину его стороны — это и есть квадратный
    корень. Та же картинка, только читаем её в обратную сторону: у нас есть число 16 внутри
    квадрата, и мы ищем сторону.</p>
{square_area_diagram(4, caption="√16 = 4 — обратная задача: дана площадь, ищем сторону")}
{code_block("koren.py", "print(16 ** 0.5)     # 4.0 — степень 0.5 и есть квадратный корень\nimport math\nprint(math.sqrt(16))  # 4.0 — то же самое, но явно и понятно для читателя\n")}
{callout(
        "tip",
        "math.sqrt() читается лучше, чем ** 0.5",
        "Оба варианта работают одинаково правильно, но <code class=\"inline\">math.sqrt(16)</code> "
        "сразу говорит читателю кода: «здесь ищут корень». "
        "<code class=\"inline\">16 ** 0.5</code> заставляет вспоминать, что 0.5 — это корень.",
    )}

    <h2>Три способа возвести в степень — и в чём разница</h2>
{comparison_table(
        ["Способ", "Что возвращает", "Пример"],
        [
            ["<code class=\"inline\">**</code>", "int, если оба операнда int; иначе float", "<code class=\"inline\">2 ** 10</code> → <code class=\"inline\">1024</code>"],
            ["<code class=\"inline\">pow(a, b)</code>", "то же самое, что <code class=\"inline\">a ** b</code>", "<code class=\"inline\">pow(2, 10)</code> → <code class=\"inline\">1024</code>"],
            ["<code class=\"inline\">math.pow(a, b)</code>", "всегда float, даже для целых чисел", "<code class=\"inline\">math.pow(2, 10)</code> → <code class=\"inline\">1024.0</code>"],
        ],
    )}
{callout(
        "info",
        "У pow() есть и третий, необязательный аргумент",
        "<code class=\"inline\">pow(a, b, m)</code> считает <code class=\"inline\">(a ** b) % m</code>, "
        "но намного быстрее — для больших чисел это ускоряет работу в тысячи раз. Используется, "
        "например, в криптографии. Пока достаточно знать, что такая возможность существует.",
    )}

{practice_card(
        "05-02",
        "Практика: степени и корни",
        "Тот же ноутбук, что закрепляет //, % и ** вместе — самое время попрактиковать все специальные операторы разом",
        "../../practice/05-02/index.html",
    )}
    """
    out = render_page(
        page_title="Степени и корни",
        description="Возведение в степень ** и квадратный корень в Python — с геометрической визуализацией площади квадрата.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Степени и корни", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Степени и корни",
        lede="Возведение в степень и извлечение корня — одна и та же геометрическая картинка, "
        "прочитанная в двух направлениях.",
        body_html=body,
        sidebar_groups=sidebar("05-02-specialnye-operacii.html"),
        nav=PageNav(prev_href="05-08-otricatelnoe-delenie.html", prev_label="Отрицательное floor-деление", next_href="05-09-unarnye-operatory.html", next_label="Унарные операторы"),
    )
    write("05-02-specialnye-operacii.html", out)


def build_09_unary_operators() -> None:
    ladder = precedence_ladder(
        [
            ("()", "скобки — всегда первыми"),
            ("**", "возведение в степень"),
            ("+x  -x", "унарный плюс/минус"),
            ("*  /  //  %", "умножение, деление, целочисленное деление, остаток"),
            ("+  -", "сложение, вычитание"),
        ],
        caption="** стоит ВЫШЕ унарного минуса — поэтому -2 ** 2 сначала возводит 2 в квадрат",
    )
    body = f"""
    <p><code class="inline">-5</code> — это не «минус пять как отдельное число», а применение
    <strong>унарного</strong> оператора <code class="inline">-</code> к числу <code class="inline">5</code>.
    Унарный — значит «с одним операндом», в отличие от привычного бинарного вычитания
    (<code class="inline">8 - 3</code>).</p>
{code_block("unarnyj.py", "x = 5\nprint(-x)     # -5 — унарный минус меняет знак\nprint(+x)     # 5 — унарный плюс почти ничего не делает (редко используется)\nprint(8 - 3)  # 5 — а это бинарное вычитание, два операнда\n")}

    <h2>Классическая ловушка: <code class="inline">-2 ** 2</code></h2>
    <p>Многие ожидают <code class="inline">-4</code>, но подозревают <code class="inline">4</code>
    (как будто сначала считается <code class="inline">(-2) ** 2</code>). Проверим:</p>
{code_block("lovushka.py", "print(-2 ** 2)     # -4\nprint((-2) ** 2)   # 4 — другое число!\n")}
{ladder}
{step_reduction_diagram(
        ["-2 ** 2", "-(2 ** 2)", "-(4)", "-4"],
        caption="** выполняется раньше унарного минуса — сначала 2 ** 2 = 4, потом применяется минус",
    )}
{callout(
        "warning",
        "** — единственное исключение такого рода",
        "У всех остальных операторов приоритет ведёт себя ожидаемо. Именно из-за этой особенности "
        "<code class=\"inline\">**</code> опытные разработчики почти всегда пишут "
        "<code class=\"inline\">(-2) ** 2</code> явно, скобками — даже когда приоритет формально понятен.",
    )}

{practice_card(
        "05-09",
        "Практика: унарные операторы",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-09/index.html",
    )}
    """
    out = render_page(
        page_title="Унарные операторы",
        description="Унарный плюс и минус в Python, и почему -2 ** 2 равно -4, а не 4.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Унарные операторы", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Унарные операторы",
        lede="Один операнд, а не два — и одна очень известная ловушка приоритета операций.",
        body_html=body,
        sidebar_groups=sidebar("05-09-unarnye-operatory.html"),
        nav=PageNav(prev_href="05-02-specialnye-operacii.html", prev_label="Степени и корни", next_href="05-03-prisvaivanie-poryadok.html", next_label="Присваивание и порядок вычислений"),
    )
    write("05-09-unarnye-operatory.html", out)


def build_03_assignment_precedence() -> None:
    ladder = precedence_ladder(
        [
            ("()", "скобки — всегда первыми"),
            ("**", "возведение в степень"),
            ("+x  -x", "унарный плюс/минус"),
            ("*  /  //  %", "умножение, деление, целочисленное деление, остаток"),
            ("+  -", "сложение, вычитание"),
        ],
        caption="Полная карта приоритета операторов этой главы — от высшего к низшему",
    )
    tree = expression_tree(("+", "2", ("*", "3", "4")), caption="2 + 3 * 4 = 14 — умножение выполняется глубже в дереве, то есть раньше")

    body = f"""
    <h2>Операции присваивания</h2>
    <p>Изменить переменную «на основе самой себя» — очень частое действие: например,
    увеличить счёт в игре. Писать <code class="inline">score = score + 10</code> можно, но
    Python предлагает более короткую запись:</p>
{code_block("prisvaivanie.py", "score = 0\nscore += 10   # то же самое, что score = score + 10\nprint(score)  # 10\n\nscore -= 3    # score = score - 3\nprint(score)  # 7\n")}
{callout(
        "info",
        "Это создаёт НОВЫЙ объект, а не меняет старый",
        "Как мы выяснили в главах 3 и 4, числа в Python неизменяемы. "
        "<code class=\"inline\">score += 10</code> не «дописывает» 10 к существующему объекту "
        "<code class=\"inline\">0</code> — Python вычисляет <code class=\"inline\">score + 10</code>, "
        "создаёт новый объект <code class=\"inline\">10</code> и переподвязывает имя "
        "<code class=\"inline\">score</code> к нему. Снаружи это выглядит как изменение, но "
        "внутри это ровно тот же механизм, что мы видели в главе 4 для <code class=\"inline\">age = age + 1</code>.",
    )}
    <p>Такие сокращения существуют для всех основных операторов:</p>
{comparison_table(
        ["Сокращённая запись", "Полная запись"],
        [
            ["<code class=\"inline\">x += n</code>", "<code class=\"inline\">x = x + n</code>"],
            ["<code class=\"inline\">x -= n</code>", "<code class=\"inline\">x = x - n</code>"],
            ["<code class=\"inline\">x *= n</code>", "<code class=\"inline\">x = x * n</code>"],
            ["<code class=\"inline\">x /= n</code>", "<code class=\"inline\">x = x / n</code>"],
            ["<code class=\"inline\">x //= n</code>", "<code class=\"inline\">x = x // n</code>"],
            ["<code class=\"inline\">x %= n</code>", "<code class=\"inline\">x = x % n</code>"],
            ["<code class=\"inline\">x **= n</code>", "<code class=\"inline\">x = x ** n</code>"],
        ],
    )}

    <h2 id="poryadok">Что выполняется первым?</h2>
    <p>Мы уже видели кусочки этой картины по отдельности — теперь соберём полную карту приоритета
    операторов главы 5, от высшего к низшему:</p>
{ladder}
{code_block("poryadok.py", "print(2 + 3 * 4)     # 14 — сначала 3 * 4 = 12, потом + 2\nprint((2 + 3) * 4)   # 20 — скобки меняют порядок\n")}
{tree}
    <p>Дерево показывает то же самое, что и приоритет: <code class="inline">*</code> вложено
    глубже, поэтому вычисляется первым — его результат становится одним из операндов
    <code class="inline">+</code>.</p>
{callout(
        "warning",
        "Сомневаетесь — используйте скобки",
        "Даже когда порядок формально понятен, скобки делают код честнее для человека, который "
        "будет его читать (в том числе для вас через полгода). "
        "<code class=\"inline\">(a + b) * c</code> читается быстрее, чем "
        "приходится вспоминать правила приоритета.",
    )}

{practice_card(
        "05-02",
        "Практика: присваивание и порядок вычислений",
        "Тот же ноутбук, что и в разделе «Степени и корни» — он охватывает и эту тему",
        "../../practice/05-02/index.html",
    )}
    """
    out = render_page(
        page_title="Присваивание и порядок вычислений",
        description="Сокращённые операторы присваивания (+=, -= и другие) и полная карта приоритета операций в Python.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Присваивание и порядок", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Присваивание и порядок вычислений",
        lede="Более короткая запись для изменения переменных — и полная карта того, что "
        "выполняется раньше, а что позже.",
        body_html=body,
        sidebar_groups=sidebar("05-03-prisvaivanie-poryadok.html"),
        nav=PageNav(prev_href="05-09-unarnye-operatory.html", prev_label="Унарные операторы", next_href="05-10-associativnost.html", next_label="Ассоциативность операторов"),
    )
    write("05-03-prisvaivanie-poryadok.html", out)


def build_10_associativity() -> None:
    left_assoc = expression_tree(("-", ("-", "8", "4"), "2"), caption="8 - 4 - 2 — левоассоциативно: сначала левая пара (8 - 4), потом результат минус 2")
    right_wrong = expression_tree(("**", ("**", "2", "3"), "2"), caption="Если бы ** было левоассоциативным: (2 ** 3) ** 2 = 64 — но это НЕ то, что делает Python")
    right_actual = expression_tree(("**", "2", ("**", "3", "2")), caption="На самом деле ** правоассоциативно: 2 ** (3 ** 2) = 512")

    body = f"""
    <p>Приоритет отвечает на вопрос «какой оператор раньше», а <strong>ассоциативность</strong> —
    на вопрос «в каком порядке считать несколько операторов ОДНОГО приоритета подряд».</p>

    <h2>Большинство операторов — слева направо</h2>
    <p><code class="inline">8 - 4 - 2</code> считается как <code class="inline">(8 - 4) - 2</code>,
    то есть слева направо. Это называется <strong>левой ассоциативностью</strong>, и так ведут себя
    почти все операторы Python: <code class="inline">+ - * / // %</code>.</p>
{left_assoc}
{code_block("levaya.py", "print(8 - 4 - 2)     # 2, потому что это (8 - 4) - 2 = 4 - 2\nprint((8 - 4) - 2)   # 2 — то же самое явно\nprint(8 - (4 - 2))   # 6 — а вот это другое число!\n")}

    <h2>Исключение: <code class="inline">**</code> — справа налево</h2>
    <p>Возведение в степень — единственный оператор в этой главе с <strong>правой</strong>
    ассоциативностью. Сравним, что дал бы каждый вариант для <code class="inline">2 ** 3 ** 2</code>:</p>
{right_wrong}
{right_actual}
{code_block("stepen_associativnost.py", "print(2 ** 3 ** 2)     # 512 — Python считает как 2 ** (3 ** 2)\nprint((2 ** 3) ** 2)   # 64  — левоассоциативный вариант дал бы другое число\nprint(2 ** (3 ** 2))   # 512 — совпадает с реальным поведением Python\n")}
{step_reduction_diagram(
        ["2 ** 3 ** 2", "2 ** (3 ** 2)", "2 ** 9", "512"],
        caption="Правая ассоциативность: сначала считается ВЕРХНИЙ (правый) показатель степени",
    )}
{callout(
        "tip",
        "Зачем ** вообще так сделали",
        "Правая ассоциативность степени совпадает с математической традицией «башни степеней» "
        "(<em>tetration</em>): в математике <em>a<sup>b<sup>c</sup></sup></em> всегда читается "
        "как <em>a<sup>(b<sup>c</sup>)</sup></em>, а не наоборот. Python здесь просто следует "
        "давнему математическому соглашению.",
    )}

{practice_card(
        "05-10",
        "Практика: ассоциативность операторов",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-10/index.html",
    )}
    """
    out = render_page(
        page_title="Ассоциативность операторов",
        description="Левая и правая ассоциативность операторов в Python — почему 2 ** 3 ** 2 равно 512.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Ассоциативность операторов", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Ассоциативность операторов",
        lede="Приоритет говорит, какой оператор раньше. Ассоциативность говорит, в каком порядке "
        "считать несколько одинаковых по приоритету операторов подряд.",
        body_html=body,
        sidebar_groups=sidebar("05-10-associativnost.html"),
        nav=PageNav(prev_href="05-03-prisvaivanie-poryadok.html", prev_label="Присваивание и порядок вычислений", next_href="05-11-skobki-i-formuly.html", next_label="Скобки и формулы из переменных"),
    )
    write("05-10-associativnost.html", out)


def build_11_parentheses_formulas() -> None:
    body = f"""
    <p>Мы уже видели, что скобки меняют порядок вычислений. Но у скобок есть и вторая роль —
    не менее важная: они делают формулы понятными для <strong>человека</strong>, даже когда
    приоритет и так дал бы правильный результат.</p>

    <h2>Скобки для людей, а не только для Python</h2>
{code_block("skobki_dlya_lyudej.py", "# Технически скобки не нужны — приоритет и так верный:\nsrednee = 4 + 7 + 9 / 3\nprint(srednee)      # 12.0 — НЕПРАВИЛЬНО! Это 4 + 7 + (9 / 3), не то, что имелось в виду\n\n# А вот с явными скобками результат соответствует замыслу:\nsrednee = (4 + 7 + 9) / 3\nprint(srednee)      # 6.666... — среднее трёх чисел\n")}
{callout(
        "warning",
        "Забытые скобки — источник реальных ошибок",
        "Пример выше — не выдуманная ловушка: «забыть скобки вокруг суммы перед делением» — одна "
        "из самых частых ошибок начинающих при переводе формулы в код.",
    )}

    <h2>Формулы из именованных переменных</h2>
    <p>Настоящий код почти никогда не пишут с «голыми» числами — используют переменные с понятными
    именами. Это делает формулу читаемой и легко изменяемой:</p>
{code_block(
        "formula_pryamougolnika.py",
        "shirina = 6\nvysota = 3\n\nperimetr = 2 * (shirina + vysota)\nploshad = shirina * vysota\n\nprint(f\"Периметр: {shirina + shirina}\")\nprint(f\"Периметр: {perimetr}\")\nprint(f\"Площадь: {ploshad}\")\n",
    )}
{callout(
        "info",
        "Опечатка выше — специально",
        "Обратите внимание на первую строку <code class=\"inline\">print()</code> в примере: "
        "<code class=\"inline\">shirina + shirina</code> вместо <code class=\"inline\">perimetr</code> "
        "— она не выдаёт ошибку, но выдаёт неверное число. Формула, которая не падает, но считает "
        "не то, что задумано — самая коварная ошибка в вычислениях. Мы разберём такие ошибки "
        "подробно в разделе про отладку вычислений.",
    )}

    <h2>Ещё три классические формулы</h2>
{code_block(
        "eshche_formuly.py",
        "# скорость = расстояние / время\nrasstoyanie_km = 120\nvremya_ch = 2\nskorost = rasstoyanie_km / vremya_ch\nprint(f\"Скорость: {skorost} км/ч\")\n\n"
        "# перевод температуры из Цельсия в Фаренгейт\ncelsius = 20\nfahrenheit = celsius * 9 / 5 + 32\nprint(f\"{celsius}°C = {fahrenheit}°F\")\n\n"
        "# простые проценты: сумма * ставка * годы / 100\nsumma = 1000\nstavka = 5\ngody = 3\nprocenty = summa * stavka * gody / 100\nprint(f\"Проценты: {procenty}\")\n",
    )}
{fraction_bar_diagram(1, 3, caption="Среднее трёх равных долей — та же идея, что и деление на 3 в формуле выше")}

{practice_card(
        "05-11",
        "Практика: скобки и формулы из переменных",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-11/index.html",
    )}
    """
    out = render_page(
        page_title="Скобки и формулы из переменных",
        description="Скобки для читаемости формул, и построение формул из именованных переменных: периметр, скорость, температура, проценты.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Скобки и формулы", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Скобки и формулы из переменных",
        lede="От отдельных операторов — к настоящим формулам с понятными именами, как в реальном коде.",
        body_html=body,
        sidebar_groups=sidebar("05-11-skobki-i-formuly.html"),
        nav=PageNav(prev_href="05-10-associativnost.html", prev_label="Ассоциативность операторов", next_href="05-12-perevod-formul.html", next_label="Перевод формул: математика → Python"),
    )
    write("05-11-skobki-i-formuly.html", out)


def build_12_formula_translation() -> None:
    tree = expression_tree(("/", ("+", "a", "b"), "c"), caption="(a + b) / c — дерево показывает, что вся сумма должна оказаться ПОД чертой дроби")

    frac_ab_c = math_inline(("frac", ("row", "a", ("mo", "+"), "b"), "c"), aria_label="дробь: a плюс b, всё это делённое на c")
    frac_ab_cd = math_inline(("frac", ("row", "a", ("mo", "+"), "b"), ("row", "c", ("mo", "+"), "d")), aria_label="дробь: a плюс b, делённое на c плюс d")
    two_x = math_inline(("row", "2", "x"), aria_label="два икс")
    x_sq = math_inline(("sup", "x", "2"), aria_label="икс в квадрате")
    sqrt_x = math_inline(("sqrt", "x"), aria_label="корень из икс")
    pi_r_sq = math_inline(("row", "π", ("sup", "r", "2")), aria_label="пи эр в квадрате")
    a_bc = math_inline(("row", "a", ("mo", "("), "b", ("mo", "+"), "c", ("mo", ")")), aria_label="a умножить на скобку b плюс c")

    circle_svg = (
        '<figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        'border-radius:var(--radius-lg,20px);overflow-x:auto;display:flex;flex-direction:column;align-items:center">'
        '<svg viewBox="0 0 220 180" xmlns="http://www.w3.org/2000/svg" role="img" '
        'aria-label="Круг радиусом r — радиус соединяет центр с краем окружности" style="width:100%;height:auto;max-width:220px">'
        '<circle cx="110" cy="90" r="70" fill="#FAFAFC" stroke="#5B24F9" stroke-width="2.5"/>'
        '<line x1="110" y1="90" x2="180" y2="90" stroke="#5B24F9" stroke-width="2.5"/>'
        '<circle cx="110" cy="90" r="4" fill="#0D0230"/>'
        '<text x="145" y="83" text-anchor="middle" font-family="JetBrains Mono, monospace" '
        'font-weight="700" font-size="16" fill="#5B24F9">r</text>'
        '</svg>'
        '<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">'
        'Радиус r соединяет центр круга с его краем — из него вычисляется площадь A = πr²</figcaption>'
        '</figure>'
    )

    body = f"""
    <p>Формулы в учебниках математики записаны иначе, чем код Python — умножение часто вообще
    не пишут, степень поднимают над строкой, деление рисуют чертой. Переводить такие формулы в
    Python нужно осторожно.</p>

    <h2>Таблица перевода</h2>
{comparison_table(
        ["В математике", "В Python", "Частая ошибка"],
        [
            [two_x, "<code class=\"inline\">2 * x</code>", "написать <code class=\"inline\">2x</code> — SyntaxError, умножение никогда не подразумевается"],
            [x_sq, "<code class=\"inline\">x ** 2</code>", "написать <code class=\"inline\">x^2</code> — сработает, но даст совсем не то число!"],
            [frac_ab_c, "<code class=\"inline\">(a + b) / c</code>", "написать <code class=\"inline\">a + b / c</code> — разделится только b, не вся сумма"],
            [sqrt_x, "<code class=\"inline\">x ** 0.5</code> или <code class=\"inline\">math.sqrt(x)</code>", "забыть, что корень — это тоже степень (0.5)"],
            [pi_r_sq, "<code class=\"inline\">math.pi * radius ** 2</code>", "забыть импортировать <code class=\"inline\">math</code>, или написать <code class=\"inline\">pi</code> вместо <code class=\"inline\">math.pi</code>"],
            [a_bc, "<code class=\"inline\">a * (b + c)</code>", "написать <code class=\"inline\">a(b + c)</code> — Python решит, что <code class=\"inline\">a</code> это функция, и попытается её вызвать"],
            [frac_ab_cd, "<code class=\"inline\">(a + b) / (c + d)</code>", "написать <code class=\"inline\">a + b / c + d</code> — разделится только b на c"],
        ],
    )}
{callout(
        "warning",
        "^ в Python — это НЕ степень",
        "В математике <code class=\"inline\">^</code> иногда означает возведение в степень. В "
        "Python <code class=\"inline\">^</code> — совсем другой оператор (побитовое исключающее "
        "ИЛИ, разберём его в главе про биты): <code class=\"inline\">5 ^ 3</code> равно "
        "<code class=\"inline\">6</code>, а не <code class=\"inline\">125</code>. Для степени "
        "всегда используйте <code class=\"inline\">**</code>.",
    )}
{code_block("proverka_karety.py", "print(5 ** 3)   # 125 — степень\nprint(5 ^ 3)    # 6 — совсем другая операция!\n")}

    <h2>От математики — через геометрию — к Python</h2>
    <p>Таблица показывает перевод построчно. Но у формулы <math xmlns="http://www.w3.org/1998/Math/MathML" style="font-size:1.15em;color:#0D0230"><mi>A</mi><mo>=</mo><mi>π</mi><msup><mi>r</mi><mn>2</mn></msup></math>
    есть третий, самый наглядный уровень — сама геометрическая фигура, которую формула описывает:</p>
{math_formula(("row", "A", ("mo", "="), "π", ("sup", "r", "2")), caption="A = πr² — площадь круга через его радиус")}
{circle_svg}
{code_block("ploshad_kruga_perevod.py", "import math\n\nradius = 5\nploshad = math.pi * radius ** 2\nprint(round(ploshad, 2))   # 78.54\n")}
{callout(
        "tip",
        "radius ** 2, а не (radius) ** 2",
        "Скобки вокруг одиночной переменной не нужны — <code class=\"inline\">**</code> уже "
        "применяется только к <code class=\"inline\">radius</code>, а не ко всему выражению "
        "<code class=\"inline\">math.pi * radius</code> (умножение и степень — разные уровни "
        "приоритета, степень выше).",
    )}

    <h2>Почему скобки вокруг суммы обязательны</h2>
    <p>Вернёмся к дроби <math xmlns="http://www.w3.org/1998/Math/MathML" style="font-size:1.15em;color:#0D0230"><mfrac><mrow><mi>a</mi><mo>+</mo><mi>b</mi></mrow><mi>c</mi></mfrac></math>
    и посмотрим на неё с трёх сторон: как формулу, как дерево вычислений и как код.</p>
{math_formula(("frac", ("row", "a", ("mo", "+"), "b"), "c"), caption="Черта дроби ГРУППИРУЕТ a + b в один числитель — это визуально очевидно")}
{tree}
    <p>Дерево показывает то же самое, что и черта дроби: <code class="inline">a + b</code> —
    единый блок, который целиком становится числителем. В Python черты нет, поэтому эту
    группировку нужно обозначить явно — круглыми скобками:</p>
{code_block("pochemu_skobki.py", "a, b, c = 8, 4, 3\n\n# ПРАВИЛЬНО — скобки воспроизводят черту дроби:\nprint((a + b) / c)   # 4.0\n\n# НЕПРАВИЛЬНО — без скобок делится только b:\nprint(a + b / c)     # 9.333... — это a + (b / c), совсем другая формула!\n")}

    <h2>Пример перевода: формула среднего</h2>
    <p>Формула среднего трёх чисел <math xmlns="http://www.w3.org/1998/Math/MathML" style="font-size:1.15em;color:#0D0230"><mfrac><mrow><mi>a</mi><mo>+</mo><mi>b</mi><mo>+</mo><mi>c</mi></mrow><mn>3</mn></mfrac></math>
    переводится в Python по тому же правилу — вся сумма должна попасть в скобки, прежде чем делить:</p>
{code_block("srednee_perevod.py", "a, b, c = 4, 7, 9\nsrednee = (a + b + c) / 3\nprint(srednee)   # 6.666...\n")}

{practice_card(
        "05-12",
        "Практика: перевод формул из математики в Python",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-12/index.html",
    )}
    """
    out = render_page(
        page_title="Перевод формул: математика → Python",
        description="Как переводить формулы из математической записи в код Python — умножение, степени, дроби и частые ошибки перевода.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Перевод формул", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Перевод формул: математика → Python",
        lede="Учебник записывает формулы иначе, чем Python. Разбираем правила перевода — и самые "
        "частые ошибки при этом переводе.",
        body_html=body,
        sidebar_groups=sidebar("05-12-perevod-formul.html"),
        nav=PageNav(prev_href="05-11-skobki-i-formuly.html", prev_label="Скобки и формулы из переменных", next_href="05-04-matematicheskie-funkcii.html", next_label="Модуль math — карта возможностей"),
    )
    write("05-12-perevod-formul.html", out)


def build_04_math_module() -> None:
    builtin_vs_module = capability_map(
        [
            ("Встроено в язык — доступно всегда", ["print() · abs()", "round() · pow()", "не требует import"]),
            ("Модуль math — отдельный ящик с инструментами", ["sqrt() · hypot() · gcd()", "sin() · log() · pi", "требует import math"]),
        ],
        title="Python: то, что встроено, и то, что лежит в модулях",
        caption="Модуль — это отдельный, заранее подписанный ящик с инструментами, а не часть самого языка",
    )

    anatomy = (
        '<figure style="margin:24px 0;padding:28px 20px;background:var(--color-bg-surface,#FAFAFC);'
        'border-radius:var(--radius-lg,20px);overflow-x:auto">'
        '<div style="display:flex;justify-content:center;font-family:\'JetBrains Mono\',monospace;'
        'font-size:22px;font-weight:700;color:#0D0230;gap:2px;flex-wrap:wrap">'
        '<span style="color:#5B24F9">math</span><span>.</span><span style="color:#5B24F9">sqrt</span>'
        '<span>(</span><span>25</span><span>)</span></div>'
        '<div style="display:flex;justify-content:center;gap:28px;margin-top:14px;flex-wrap:wrap;text-align:center">'
        '<div><div style="width:2px;height:14px;background:#B9A0FC;margin:0 auto"></div>'
        '<div style="font-family:Sora,sans-serif;font-weight:700;font-size:13px;color:#5B24F9">модуль</div>'
        '<div style="font-size:12px;color:var(--ink-soft,#6B6B7D)">где искать</div></div>'
        '<div><div style="width:2px;height:14px;background:#B9A0FC;margin:0 auto"></div>'
        '<div style="font-family:Sora,sans-serif;font-weight:700;font-size:13px;color:#5B24F9">инструмент</div>'
        '<div style="font-size:12px;color:var(--ink-soft,#6B6B7D)">что делать</div></div>'
        '<div><div style="width:2px;height:14px;background:#B9A0FC;margin:0 auto"></div>'
        '<div style="font-family:Sora,sans-serif;font-weight:700;font-size:13px;color:#5B24F9">аргумент</div>'
        '<div style="font-size:12px;color:var(--ink-soft,#6B6B7D)">с чем работать</div></div>'
        '</div>'
        '<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:14px">'
        'Точка означает «возьми sqrt ИЗ модуля math» — это не украшение синтаксиса, а указание адреса</figcaption>'
        '</figure>'
    )

    cmap = capability_map(
        [
            ("Корни и расстояния", ["sqrt · isqrt", "hypot · dist"]),
            ("Целочисленная математика", ["gcd · lcm", "factorial · comb · perm"]),
            ("Геометрия", ["pi", "hypot · dist"]),
            ("Тригонометрия", ["sin · cos · tan", "radians · degrees"]),
            ("Логарифмы и рост", ["log · log2 · log10 · exp"]),
        ],
        title="Что умеет модуль math",
        caption="Каждая карточка — отдельный раздел ниже, с реальными задачами и картинками",
    )

    body = f"""
    <p>Python уже кое-что умеет считать без всякой подготовки:</p>
{code_block("vstroennoe.py", "print(abs(-7))     # 7\nprint(round(4.5))  # 4\nprint(pow(2, 10))  # 1024\n")}
    <p>Но настоящей математики в мире куда больше, чем четыре встроенные функции: корни, синусы,
    логарифмы, работа с углами и расстояниями. Если бы <strong>все</strong> такие инструменты
    были встроены прямо в язык — Python превратился бы в загромождённый список из сотен имён,
    и запомнить, что вообще доступно, стало бы невозможно.</p>

    <h2>Модуль — это отдельный, подписанный ящик с инструментами</h2>
    <p>Вместо этого стандартная библиотека Python организует связанные инструменты в
    <strong>модули</strong> — отдельные «ящики», которые лежат рядом, но не смешиваются с языком
    напрямую и друг с другом. Один из таких ящиков называется <code class="inline">math</code> —
    в нём собраны математические инструменты: корни, тригонометрия, логарифмы и многое другое.</p>
{builtin_vs_module}

    <h2><code class="inline">import math</code> — открываем ящик</h2>
    <p>Чтобы воспользоваться инструментами из ящика <code class="inline">math</code>, его нужно
    сначала явно <strong>открыть</strong> — командой <code class="inline">import</code>:</p>
{code_block("import_math.py", "import math\n\n# теперь всё содержимое ящика math доступно в этой программе\nprint(math.sqrt(2))\n")}
{callout(
        "info",
        "import math — это не «включить математику»",
        "Строка <code class=\"inline\">import math</code> примерно означает: «сделай содержимое "
        "модуля math доступным в этой программе». Без неё <code class=\"inline\">math.sqrt(25)</code> "
        "вызовет <code class=\"inline\">NameError</code> — Python ещё не знает, где искать "
        "<code class=\"inline\">math</code>.",
    )}

    <h2>Что означает точка</h2>
    <p>Разберём запись <code class="inline">math.sqrt(25)</code> по частям:</p>
{anatomy}
    <p>Точка здесь значит «возьми <code class="inline">sqrt</code> <strong>из</strong> модуля
    <code class="inline">math</code>» — так Python отличает, например, <code class="inline">math.sqrt</code>
    от какой-нибудь другой функции с похожим именем из совсем другого модуля: у каждого
    инструмента есть свой явный адрес.</p>

    <h2>А что если аргумент не нужен: <code class="inline">math.pi</code></h2>
    <p><code class="inline">math.pi</code> — не функция, а готовое <strong>значение</strong>
    (константа): число π уже вычислено и лежит внутри модуля под именем <code class="inline">pi</code>.
    Поэтому у него нет круглых скобок — скобки означают «вызови функцию», а
    <code class="inline">pi</code> вызывать не нужно, его нужно просто прочитать:</p>
{code_block("math_pi.py", "import math\n\nprint(math.pi)        # 3.141592653589793 — значение, не вызов\nprint(math.sqrt(25))  # 5.0 — а это вызов функции, поэтому есть скобки\n")}

    <h2>Первые эксперименты</h2>
    <p>Несколько маленьких примеров — код и его результат:</p>
{code_block("eksperiment_1.py", "import math\n\nprint(math.sqrt(25))\n")}
    <p style="color:var(--ink-soft,#6B6B7D);font-size:14px;margin-top:-12px">РЕЗУЛЬТАТ: <code class="inline">5.0</code> — квадратный корень из 25.</p>
{code_block("eksperiment_2.py", "import math\n\nprint(math.pi)\n")}
    <p style="color:var(--ink-soft,#6B6B7D);font-size:14px;margin-top:-12px">РЕЗУЛЬТАТ: <code class="inline">3.141592653589793</code> — число π с точностью float.</p>
{code_block("eksperiment_3.py", "import math\n\nprint(math.gcd(18, 24))\n")}
    <p style="color:var(--ink-soft,#6B6B7D);font-size:14px;margin-top:-12px">РЕЗУЛЬТАТ: <code class="inline">6</code> — наибольший общий делитель 18 и 24.</p>
{code_block("eksperiment_4.py", "import math\n\nprint(math.hypot(3, 4))\n")}
    <p style="color:var(--ink-soft,#6B6B7D);font-size:14px;margin-top:-12px">РЕЗУЛЬТАТ: <code class="inline">5.0</code> — длина гипотенузы прямоугольного треугольника со сторонами 3 и 4.</p>

    <h2>Встроенное vs math — не путаем</h2>
    <p>Ещё раз проведём чёткую границу — какие инструменты встроены в язык напрямую, а какие
    нужно явно импортировать, и откуда именно:</p>
{comparison_table(
        ["Инструмент", "Откуда", "Нужен import?"],
        [
            ["<code class=\"inline\">abs()</code>, <code class=\"inline\">round()</code>, <code class=\"inline\">pow()</code>", "встроены в язык", "нет"],
            ["<code class=\"inline\">math.sqrt()</code>, <code class=\"inline\">math.floor()</code>, <code class=\"inline\">math.sin()</code>, <code class=\"inline\">math.log()</code>", "модуль <code class=\"inline\">math</code>", "<code class=\"inline\">import math</code>"],
            ["<code class=\"inline\">Decimal</code>", "модуль <code class=\"inline\">decimal</code> (глава 4)", "<code class=\"inline\">from decimal import Decimal</code>"],
            ["<code class=\"inline\">Fraction</code>", "модуль <code class=\"inline\">fractions</code> (глава 4)", "<code class=\"inline\">from fractions import Fraction</code>"],
        ],
    )}
{callout(
        "warning",
        "Decimal и Fraction — НЕ часть math",
        "Это частая путаница: <code class=\"inline\">Decimal</code> и <code class=\"inline\">Fraction</code> "
        "из главы 4 — инструменты для точных чисел, но живут в СВОИХ собственных модулях "
        "(<code class=\"inline\">decimal</code> и <code class=\"inline\">fractions</code>), "
        "отдельно от <code class=\"inline\">math</code>. Три разных ящика — три разных импорта.",
    )}

    <h2>Полная карта: что умеет math</h2>
    <p>Теперь, когда понятно, что такое модуль и зачем нужна точка, можно спокойно посмотреть на
    карту того, что <code class="inline">math</code> предлагает — следующие разделы главы разберут
    каждую карточку подробно, с реальными задачами:</p>
{cmap}

    <h2>Как искать то, чего нет на карте</h2>
    <p>У <code class="inline">math</code> около полусотни функций — эта карта показывает только
    самые полезные для начала. Никто не держит в голове весь список, и это нормально:
    профессиональный навык — не «знать всё наизусть», а знать <strong>примерно</strong>, что
    существует, и уметь быстро найти точную деталь.</p>
{callout(
        "tip",
        "Официальная документация — не враг, а инструмент",
        "Полный и точный список всего, что есть в <code class=\"inline\">math</code>, — на "
        "странице официальной документации Python 3.14: "
        "<a href=\"https://docs.python.org/3.14/library/math.html\" target=\"_blank\" rel=\"noopener\">"
        "docs.python.org/3.14/library/math</a> (Standard Library → math). Опытные разработчики "
        "заглядывают туда постоянно — это не признак незнания, а нормальная часть работы.",
    )}

{practice_card(
        "05-04",
        "Практика: модуль math — что такое модуль и первые вызовы",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-04/index.html",
    )}
    """
    out = render_page(
        page_title="Модуль math — карта возможностей",
        description="Что такое модуль в Python, зачем нужен import math, что означает точка в math.sqrt() — и полная карта возможностей модуля math.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Модуль math", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Модуль math — от каталога к инструментам",
        lede="Что такое модуль, зачем нужен import и что означает точка в math.sqrt() — прежде "
        "чем нырять в конкретные функции, разберёмся, как вообще устроен этот ящик с инструментами.",
        body_html=body,
        sidebar_groups=sidebar("05-04-matematicheskie-funkcii.html"),
        nav=PageNav(prev_href="05-12-perevod-formul.html", prev_label="Перевод формул", next_href="05-13-korni-rasstoyaniya.html", next_label="Корни и расстояния"),
    )
    write("05-04-matematicheskie-funkcii.html", out)


def build_13_roots_distances() -> None:
    triangle = right_triangle_diagram(3, 4, 5, caption="hypot(3, 4) = 5 — классический прямоугольный треугольник 3-4-5")
    plane = coordinate_plane_diagram(
        [(2, 1, "A(2, 1)"), (6, 4, "B(6, 4)")],
        lo=-1, hi=7,
        caption="Расстояние между A и B — это гипотенуза прямоугольного треугольника, построенного на их координатах",
    )
    body = f"""
    <h2><code class="inline">isqrt()</code> — целочисленный корень</h2>
    <p><code class="inline">math.sqrt()</code> всегда возвращает <code class="inline">float</code>.
    Если нужен именно <code class="inline">int</code> — например, для чисел настолько больших,
    что float начинает терять точность — есть <code class="inline">math.isqrt()</code>: он
    отбрасывает дробную часть и работает только с целыми числами.</p>
{code_block("isqrt.py", "import math\n\nprint(math.sqrt(10))     # 3.1622776601683795\nprint(math.isqrt(10))    # 3 — целая часть корня, без дробей и без потери точности\n")}

    <h2><code class="inline">hypot()</code> — гипотенуза без Пифагора вручную</h2>
    <p>Если известны длины двух катетов прямоугольного треугольника, длину гипотенузы можно найти
    формулой <code class="inline">c = sqrt(a**2 + b**2)</code> — но <code class="inline">math</code>
    уже умеет это одной функцией:</p>
{triangle}
{code_block("hypot.py", "import math\n\nprint(math.sqrt(3 ** 2 + 4 ** 2))   # 5.0 — вручную по теореме Пифагора\nprint(math.hypot(3, 4))            # 5.0 — то же самое, короче и точнее\n")}

    <h2><code class="inline">dist()</code> — расстояние между двумя точками</h2>
    <p><code class="inline">math.dist()</code> — это <code class="inline">hypot()</code>, но для
    двух точек на плоскости (или в пространстве), а не для одного треугольника: он сам вычисляет
    катеты как разницу координат.</p>
{plane}
{code_block("dist.py", "import math\n\nA = (2, 1)\nB = (6, 4)\nprint(math.dist(A, B))   # 5.0 — то же самое расстояние, посчитанное из координат\n")}
{callout(
        "info",
        "Откуда взялось число 5.0",
        "Разница по x: 6 − 2 = 4. Разница по y: 4 − 1 = 3. Это ровно катеты треугольника 3-4-5 "
        "выше — <code class=\"inline\">dist()</code> под капотом делает именно то же самое, что "
        "<code class=\"inline\">hypot()</code>, только сам считает катеты за вас.",
    )}

{practice_card(
        "05-13",
        "Практика: корни и расстояния",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-13/index.html",
    )}
    """
    out = render_page(
        page_title="Корни и расстояния",
        description="math.isqrt, math.hypot и math.dist в Python — с геометрической визуализацией треугольника и координатной плоскости.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Корни и расстояния", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Корни и расстояния",
        lede="От теоремы Пифагора вручную — к готовым функциям, которые считают расстояние за вас.",
        body_html=body,
        sidebar_groups=sidebar("05-13-korni-rasstoyaniya.html"),
        nav=PageNav(prev_href="05-04-matematicheskie-funkcii.html", prev_label="Модуль math — карта возможностей", next_href="05-14-gcd-lcm-faktorial.html", next_label="gcd, lcm, факториал, comb, perm"),
    )
    write("05-13-korni-rasstoyaniya.html", out)


def build_14_gcd_lcm_factorial() -> None:
    body = f"""
    <h2><code class="inline">gcd()</code> — наибольший общий делитель</h2>
    <p>Наибольший общий делитель (НОД) двух чисел — самое большое число, на которое оба делятся
    без остатка. Классическое применение — сокращение дробей:</p>
{code_block("gcd.py", "import math\n\nprint(math.gcd(12, 18))   # 6 — и 12, и 18 делятся на 6 без остатка\n\n# сократить дробь 12/18:\nchislitel, znamenatel = 12, 18\nnod = math.gcd(chislitel, znamenatel)\nprint(f\"{chislitel // nod}/{znamenatel // nod}\")   # 2/3 — та же дробь, но в простейшем виде\n")}

    <h2><code class="inline">lcm()</code> — наименьшее общее кратное</h2>
    <p>Наименьшее общее кратное (НОК) — наименьшее число, которое делится на оба числа сразу.
    Пригодится, например, чтобы понять, когда снова совпадут два повторяющихся события:</p>
{code_block("lcm.py", "import math\n\nprint(math.lcm(4, 6))   # 12 — автобус №1 ходит каждые 4 минуты, автобус №2 — каждые 6\n                        # оба будут на остановке одновременно каждые 12 минут\n")}

    <h2><code class="inline">factorial()</code> — считаем перестановки</h2>
    <p>Факториал <code class="inline">n!</code> — произведение всех целых чисел от 1 до
    <code class="inline">n</code>. Отвечает на вопрос «сколькими способами можно расставить
    n разных предметов по порядку»:</p>
{code_block("factorial.py", "import math\n\nprint(math.factorial(5))   # 120 — 5 книг на полке можно расставить 120 разными способами\n")}

    <h2><code class="inline">comb()</code> и <code class="inline">perm()</code> — выбор и порядок</h2>
    <p><code class="inline">comb(n, k)</code> — сколькими способами выбрать <code class="inline">k</code>
    предметов из <code class="inline">n</code>, если порядок выбора <strong>не важен</strong>.
    <code class="inline">perm(n, k)</code> — то же самое, но когда порядок <strong>важен</strong>.</p>
{code_block("comb_perm.py", "import math\n\n# сколько разных троек чисел можно выбрать из лотерейных 49, не важен порядок:\nprint(math.comb(49, 3))   # 18424\n\n# сколько разных подиумов (1, 2, 3 место) можно составить из 10 бегунов, порядок важен:\nprint(math.perm(10, 3))   # 720\n")}
{callout(
        "tip",
        "perm() всегда больше или равен comb()",
        "Для одних и тех же <code class=\"inline\">n</code> и <code class=\"inline\">k</code> "
        "<code class=\"inline\">perm()</code> считает КАЖДЫЙ порядок отдельно, а "
        "<code class=\"inline\">comb()</code> — только уникальные наборы. Если сомневаетесь, какую "
        "функцию использовать, задайте себе вопрос: «важен ли порядок?» — да → "
        "<code class=\"inline\">perm()</code>, нет → <code class=\"inline\">comb()</code>.",
    )}

{practice_card(
        "05-14",
        "Практика: gcd, lcm, факториал, comb, perm",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-14/index.html",
    )}
    """
    out = render_page(
        page_title="gcd, lcm, факториал, comb, perm",
        description="Наибольший общий делитель, наименьшее общее кратное, факториал и комбинаторные функции math в Python.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("gcd, lcm, факториал, comb, perm", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="gcd, lcm, факториал, comb, perm",
        lede="Пять функций для работы с целыми числами и подсчёта вариантов — с реальными задачами "
        "для каждой.",
        body_html=body,
        sidebar_groups=sidebar("05-14-gcd-lcm-faktorial.html"),
        nav=PageNav(prev_href="05-13-korni-rasstoyaniya.html", prev_label="Корни и расстояния", next_href="05-15-geometriya-s-math.html", next_label="Геометрия с math"),
    )
    write("05-14-gcd-lcm-faktorial.html", out)


def build_15_geometry() -> None:
    circle = coordinate_plane_diagram(
        [(3, 0, "R = 3")],
        circle_radius=3,
        lo=-4, hi=4,
        caption="Окружность радиусом 3 — площадь и длина считаются через её радиус",
    )
    body = f"""
    <p>Модуль <code class="inline">math</code> не умеет рисовать круги, но даёт всё нужное, чтобы
    их <strong>посчитать</strong>: константу <code class="inline">math.pi</code> и обычные
    арифметические операторы, которые мы уже знаем.</p>

    <h2>Площадь и длина окружности</h2>
{circle}
{code_block("krug.py", "import math\n\nradius = 3\nploshad = math.pi * radius ** 2\ndlina_okruzhnosti = 2 * math.pi * radius\n\nprint(f\"Площадь: {round(ploshad, 2)}\")               # 28.27\nprint(f\"Длина окружности: {round(dlina_okruzhnosti, 2)}\")  # 18.85\n")}
{callout(
        "info",
        "math.pi — это float с ограниченной точностью",
        "<code class=\"inline\">math.pi</code> хранит π с точностью, достаточной для практических "
        "задач (15-16 значащих цифр) — но это не «настоящее» бесконечное π, а его "
        "<code class=\"inline\">float</code>-представление. Мы подробно разбирали, почему у float "
        "есть предел точности, в главе 4.",
    )}

    <h2>Комбинируем несколько формул: площадь кольца</h2>
    <p>Настоящие геометрические задачи часто требуют комбинировать несколько формул. Площадь
    кольца между двумя окружностями — площадь большого круга минус площадь маленького:</p>
{code_block("kolco.py", "import math\n\nvneshnij_radius = 5\nvnutrennij_radius = 3\n\nploshad_kolca = math.pi * vneshnij_radius ** 2 - math.pi * vnutrennij_radius ** 2\nprint(round(ploshad_kolca, 2))   # 50.27\n")}

    <h2>Полезные помощники: <code class="inline">prod()</code> и <code class="inline">fsum()</code></h2>
    <p>Для перемножения или точного суммирования нескольких чисел сразу — например, объёма
    параллелепипеда по трём измерениям:</p>
{code_block("prod_fsum.py", "import math\n\nizmereniya = [4, 5, 6]\nobyom = math.prod(izmereniya)\nprint(obyom)   # 120 — как 4 * 5 * 6\n\n# fsum складывает float точнее, чем обычный sum() — меньше накопленной ошибки округления\nchisla = [1, 1e16, -1e16]\nprint(sum(chisla))         # 0.0 — обычный sum() потерял единицу из-за порядка сложения\nprint(math.fsum(chisla))   # 1.0 — fsum() считает точнее именно для таких случаев\n")}

{practice_card(
        "05-15",
        "Практика: геометрия с math",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-15/index.html",
    )}
    """
    out = render_page(
        page_title="Геометрия с math",
        description="Площадь и длина окружности, комбинирование формул и math.prod / math.fsum в Python.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Геометрия с math", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Геометрия с math",
        lede="math не рисует круги — но даёт всё, чтобы их точно посчитать.",
        body_html=body,
        sidebar_groups=sidebar("05-15-geometriya-s-math.html"),
        nav=PageNav(prev_href="05-14-gcd-lcm-faktorial.html", prev_label="gcd, lcm, факториал, comb, perm", next_href="05-16-trigonometriya.html", next_label="Тригонометрия без страха"),
    )
    write("05-15-geometriya-s-math.html", out)


def build_16_trigonometry() -> None:
    unit_circle = coordinate_plane_diagram(
        [(1, 0, "0°"), (0.71, 0.71, "45°"), (0, 1, "90°")],
        circle_radius=1,
        lo=-1.3, hi=1.3,
        caption="Единичная окружность (радиус 1) — координаты точки равны (cos угла, sin угла)",
    )
    body = f"""
    <p>Тригонометрия пугает многих не самой математикой, а обозначениями. На деле идея простая:
    для любой точки на окружности радиусом 1 (единичной окружности) координаты этой точки — это
    и есть <code class="inline">cos</code> и <code class="inline">sin</code> угла.</p>

    <h2>Градусы и радианы</h2>
    <p>Python (как и почти вся математика за пределами школьной геометрии) считает углы в
    <strong>радианах</strong>, не в градусах. Полный круг — это 360° или, что то же самое,
    <code class="inline">2π</code> радиан:</p>
{code_block("gradusy_radiany.py", "import math\n\nprint(math.radians(180))    # 3.141592653589793 — то есть π\nprint(math.degrees(math.pi)) # 180.0\n")}
{callout(
        "warning",
        "math.sin(90) — это НЕ то, что вы думаете",
        "<code class=\"inline\">math.sin(90)</code> считает синус угла в 90 <strong>радиан</strong> "
        "(это огромный угол, много полных оборотов), а не 90 градусов! Перед тригонометрическими "
        "функциями почти всегда нужен <code class=\"inline\">math.radians()</code>: "
        "<code class=\"inline\">math.sin(math.radians(90))</code>.",
    )}

    <h2>Единичная окружность</h2>
{unit_circle}
{code_block("edinichnaya_okruzhnost.py", "import math\n\nugol_gradusy = 30\nugol_radiany = math.radians(ugol_gradusy)\n\nprint(round(math.cos(ugol_radiany), 3))   # 0.866 — координата x точки на окружности\nprint(round(math.sin(ugol_radiany), 3))   # 0.5   — координата y точки на окружности\n")}
{callout(
        "info",
        "round() здесь не случаен",
        "Без <code class=\"inline\">round()</code> <code class=\"inline\">math.sin(math.radians(30))</code> "
        "выдаёт <code class=\"inline\">0.49999999999999994</code>, а не ровно "
        "<code class=\"inline\">0.5</code> — та же особенность float, которую мы разбирали в главе 4. "
        "Для сравнения углов тоже стоит использовать допуск (например, <code class=\"inline\">math.isclose()</code>), "
        "а не <code class=\"inline\">==</code>.",
    )}

    <h2><code class="inline">tan()</code> и обратные функции</h2>
{code_block("tan_obratnye.py", "import math\n\nprint(round(math.tan(math.radians(45)), 3))   # 1.0\n\n# обратная задача: известен tan, ищем угол\nugol = math.degrees(math.atan(1))\nprint(ugol)   # 45.0\n")}

{practice_card(
        "05-16",
        "Практика: тригонометрия без страха",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-16/index.html",
    )}
    """
    out = render_page(
        page_title="Тригонометрия без страха",
        description="Градусы и радианы, единичная окружность, sin, cos, tan и обратные функции в Python.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Тригонометрия", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Тригонометрия без страха",
        lede="sin и cos — это просто координаты точки на окружности радиусом 1. Вся тригонометрия "
        "строится вокруг этой одной картинки.",
        body_html=body,
        sidebar_groups=sidebar("05-16-trigonometriya.html"),
        nav=PageNav(prev_href="05-15-geometriya-s-math.html", prev_label="Геометрия с math", next_href="05-17-logarifmy.html", next_label="Логарифмы и экспоненты"),
    )
    write("05-16-trigonometriya.html", out)


def build_17_logarithms() -> None:
    body = f"""
    <p>Логарифм отвечает на вопрос, обратный степени: не «2 в какой степени даёт 8», а «в какую
    степень нужно возвести 2, чтобы получить 8».</p>
{step_reduction_diagram(
        ["2 ** x = 8", "x = log₂(8)", "x = 3"],
        caption="Логарифм — обратная операция к степени: ищем показатель, а не результат",
    )}
{code_block("log.py", "import math\n\nprint(2 ** 3)          # 8 — прямая задача: степень известна, ищем результат\nprint(math.log2(8))   # 3.0 — обратная задача: результат известен, ищем степень\n")}

    <h2>Три варианта основания</h2>
{comparison_table(
        ["Функция", "Основание", "Когда используется"],
        [
            ["<code class=\"inline\">math.log2(x)</code>", "2", "информатика: сколько битов нужно для x значений"],
            ["<code class=\"inline\">math.log10(x)</code>", "10", "порядок величины числа (сколько в нём разрядов)"],
            ["<code class=\"inline\">math.log(x)</code>", "e ≈ 2.718 (натуральный)", "рост/распад, финансы, наука"],
            ["<code class=\"inline\">math.log(x, base)</code>", "любое, задаётся вторым аргументом", "произвольное основание"],
        ],
    )}
{code_block("osnovaniya.py", "import math\n\nprint(math.log10(1000))   # 3.0 — в числе 1000 три нуля\nprint(math.log(8, 2))     # 3.0 — то же самое, что log2(8), но через общую функцию\n")}

    <h2><code class="inline">exp()</code> — обратная операция к логарифму</h2>
    <p><code class="inline">math.exp(x)</code> считает <code class="inline">e ** x</code> — то,
    во что логарифм и степень превращаются друг в друга:</p>
{code_block("exp.py", "import math\n\nx = 2\nprint(math.exp(x))          # 7.38905609893065\nprint(math.log(math.exp(x)))  # 2.0 — log и exp отменяют друг друга\n")}
{callout(
        "tip",
        "Где логарифмы встретятся снова",
        "Логарифмы понадобятся не сразу, но встретятся ещё не раз: в оценке сложности алгоритмов "
        "(почему поиск в отсортированном списке быстрый), в анализе данных, в шкалах вроде "
        "децибел или землетрясений по шкале Рихтера. Пока достаточно понимать саму идею — "
        "«обратная операция к степени».",
    )}

{practice_card(
        "05-17",
        "Практика: логарифмы и экспоненты",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-17/index.html",
    )}
    """
    out = render_page(
        page_title="Логарифмы и экспоненты",
        description="Логарифм как обратная операция к степени: math.log, math.log2, math.log10, math.exp в Python.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Логарифмы и экспоненты", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Логарифмы и экспоненты",
        lede="Логарифм — просто обратная операция к степени: не «результат возведения», а "
        "«какая нужна степень».",
        body_html=body,
        sidebar_groups=sidebar("05-17-logarifmy.html"),
        nav=PageNav(prev_href="05-16-trigonometriya.html", prev_label="Тригонометрия без страха", next_href="05-05-sluchaynye-chisla.html", next_label="Модуль random: псевдослучайность"),
    )
    write("05-17-logarifmy.html", out)


def build_05_random_module() -> None:
    body = f"""
    <p>Модуль <code class="inline">random</code> добавляет в Python элемент случайности —
    без него не обходится почти ни одна игра: случайный противник, случайная карта, случайное
    число для игры «Угадай число» в главе 9.</p>

    <h2>«Случайное» число — на самом деле не совсем случайное</h2>
    <p>Компьютер не умеет создавать настоящую случайность из ничего — вместо этого
    <code class="inline">random</code> использует <strong>псевдослучайный генератор</strong>:
    формулу, которая по одному числу («состоянию») вычисляет следующее число, выглядящее
    беспорядочным, а затем обновляет своё состояние для следующего вызова. Числа выглядят
    случайными, но получены полностью детерминированной формулой.</p>
{code_block("psevdosluchajnost.py", "import random\n\nprint(random.random())   # случайное дробное число от 0.0 до 1.0 (не включая 1.0)\nprint(random.random())   # другое число — состояние генератора обновилось\n")}
{callout(
        "info",
        "Зачем это знать, если можно просто пользоваться?",
        "Потому что из этого следует важное практическое свойство: генератор можно "
        "<strong>перезапустить</strong> с того же самого состояния — и тогда он выдаст ту же самую "
        "последовательность чисел заново. Это называется воспроизводимостью, и мы разберём её "
        "подробно через несколько разделов — она незаменима при отладке программ со случайностью.",
    )}

    <h2>Что дальше в этом разделе</h2>
{capability_map(
        [
            ("randint · randrange · uniform", ["случайные числа в диапазоне"]),
            ("choice · choices · sample · shuffle", ["случайный выбор из набора"]),
            ("seed", ["воспроизводимость и random vs secrets"]),
        ],
        caption="Каждая карточка — отдельный раздел ниже",
    )}

{practice_card(
        "05-05",
        "Практика: основы random",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-05/index.html",
    )}
    """
    out = render_page(
        page_title="Модуль random: псевдослучайность",
        description="Что такое псевдослучайный генератор в Python, и почему random() не создаёт настоящую случайность.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Модуль random", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Модуль random: псевдослучайность",
        lede="Без капли случайности сложно представить хоть одну игру — но эта «случайность» "
        "устроена куда интереснее, чем кажется.",
        body_html=body,
        sidebar_groups=sidebar("05-05-sluchaynye-chisla.html"),
        nav=PageNav(prev_href="05-17-logarifmy.html", prev_label="Логарифмы и экспоненты", next_href="05-18-randint-randrange-uniform.html", next_label="randint, randrange, uniform"),
    )
    write("05-05-sluchaynye-chisla.html", out)


def build_18_randint_randrange_uniform() -> None:
    incl = number_line_diagram(
        [(1, "1"), (6, "6")],
        lo=0, hi=7,
        jumps=[(1, 6, "randint(1, 6)")],
        caption="randint(1, 6) может вернуть 1, может вернуть 6 — обе границы включены",
    )
    body = f"""
    <h2><code class="inline">randint(a, b)</code> — случайное целое, обе границы включены</h2>
{incl}
{code_block("randint.py", "import random\n\nkubik = random.randint(1, 6)   # может быть 1, 2, 3, 4, 5 ИЛИ 6\nprint(kubik)\n")}
{callout(
        "warning",
        "Частая ошибка «на единицу» (off-by-one)",
        "Если нужны числа от 1 до 5 (не включая 6), а написать <code class=\"inline\">random.randint(1, 6)</code>"
        " — программа иногда будет неверно выдавать 6. Обе границы <code class=\"inline\">randint()</code> "
        "включены — это стоит держать в голове каждый раз.",
    )}

    <h2><code class="inline">randrange(start, stop, step)</code> — как <code class="inline">range()</code>, но случайно</h2>
    <p>В отличие от <code class="inline">randint()</code>, у <code class="inline">randrange()</code>
    верхняя граница <strong>не включена</strong> — совсем как у обычного <code class="inline">range()</code>,
    который мы разберём подробно в главе 10. Плюс есть необязательный шаг:</p>
{code_block("randrange.py", "import random\n\nprint(random.randrange(1, 7))       # от 1 до 6 включительно — 7 НЕ входит, аналог randint(1, 6)\nprint(random.randrange(0, 10, 2))   # случайное чётное число: 0, 2, 4, 6 или 8\n")}
{comparison_table(
        ["Функция", "Верхняя граница", "Шаг"],
        [
            ["<code class=\"inline\">randint(a, b)</code>", "включена", "нет — только соседние целые"],
            ["<code class=\"inline\">randrange(a, b)</code>", "НЕ включена", "нет (по умолчанию 1)"],
            ["<code class=\"inline\">randrange(a, b, step)</code>", "НЕ включена", "да — можно перескакивать"],
        ],
    )}

    <h2><code class="inline">uniform(a, b)</code> — случайное дробное число</h2>
    <p>Работает как <code class="inline">randint()</code>, но для <code class="inline">float</code>
    — любое дробное значение в диапазоне, а не только целые:</p>
{code_block("uniform.py", "import random\n\ntemperatura = random.uniform(18.0, 24.0)\nprint(round(temperatura, 1))   # например, 21.3\n")}

{practice_card(
        "05-18",
        "Практика: randint, randrange, uniform",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-18/index.html",
    )}
    """
    out = render_page(
        page_title="randint, randrange, uniform",
        description="Три функции случайных чисел в диапазоне: randint (обе границы включены), randrange (как range) и uniform (для float).",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("randint, randrange, uniform", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="randint, randrange, uniform",
        lede="Три похожих функции с тремя разными правилами насчёт границ диапазона — и одна "
        "классическая ошибка, которая случается, если их перепутать.",
        body_html=body,
        sidebar_groups=sidebar("05-18-randint-randrange-uniform.html"),
        nav=PageNav(prev_href="05-05-sluchaynye-chisla.html", prev_label="Модуль random: псевдослучайность", next_href="05-19-choice-sample-shuffle.html", next_label="choice, choices, sample, shuffle"),
    )
    write("05-18-randint-randrange-uniform.html", out)


def build_19_choice_sample_shuffle() -> None:
    body = f"""
    <p>Кроме случайных <em>чисел</em>, <code class="inline">random</code> умеет случайно выбирать
    из <strong>готового набора</strong> значений — списка вариантов, колоды карт, списка имён.</p>

    <h2>Четыре похожих, но разных инструмента</h2>
{comparison_table(
        ["Функция", "Сколько выбирает", "Повторы возможны?", "Меняет исходный набор?"],
        [
            ["<code class=\"inline\">choice(seq)</code>", "1 элемент", "—", "нет"],
            ["<code class=\"inline\">choices(seq, k=n)</code>", "n элементов", "да — один и тот же элемент может повториться", "нет"],
            ["<code class=\"inline\">sample(seq, k=n)</code>", "n элементов", "нет — все разные", "нет"],
            ["<code class=\"inline\">shuffle(seq)</code>", "все элементы", "—", "да, перемешивает на месте"],
        ],
    )}

    <h2><code class="inline">choice()</code> — один случайный элемент</h2>
{code_block("choice.py", 'import random\n\nvarianty = ["камень", "ножницы", "бумага"]\nprint(random.choice(varianty))\n')}

    <h2><code class="inline">choices()</code> — несколько, с возможными повторами</h2>
    <p>Представим колесо рулетки с призами — один и тот же приз может выпасть снова:</p>
{code_block("choices.py", 'import random\n\nprizy = ["🎁", "🎈", "🎉"]\nvypavshie = random.choices(prizy, k=5)\nprint(vypavshie)   # например, ["🎈", "🎈", "🎁", "🎉", "🎈"] — повторы допустимы\n')}
{callout(
        "tip",
        "У choices() есть необязательные веса",
        "<code class=\"inline\">random.choices(prizy, weights=[1, 1, 10], k=5)</code> сделает "
        "третий приз в десять раз вероятнее остальных — полезно для «нечестных» кубиков или "
        "систем с разной редкостью наград.",
    )}

    <h2><code class="inline">sample()</code> — несколько, без повторов</h2>
    <p>Представим розыгрыш призов среди участников — один и тот же участник не может выиграть
    дважды в одном розыгрыше:</p>
{code_block("sample.py", 'import random\n\nuchastniki = ["Аня", "Борис", "Вера", "Глеб", "Дана"]\npobediteli = random.sample(uchastniki, k=2)\nprint(pobediteli)   # например, ["Вера", "Аня"] — все разные\n')}
{callout(
        "warning",
        "k не может быть больше длины набора",
        "<code class=\"inline\">random.sample(uchastniki, k=10)</code> при 5 участниках вызовет "
        "<code class=\"inline\">ValueError</code> — без повторов невозможно выбрать больше "
        "элементов, чем есть в наборе. У <code class=\"inline\">choices()</code> такого "
        "ограничения нет, потому что повторы разрешены.",
    )}

    <h2><code class="inline">shuffle()</code> — перемешать всё на месте</h2>
    <p>В отличие от трёх функций выше, <code class="inline">shuffle()</code> не выбирает
    подмножество — она перемешивает <strong>весь</strong> список и ничего не возвращает
    (<code class="inline">None</code>), потому что изменяет список прямо «на месте»:</p>
{code_block("shuffle.py", "import random\n\nkoloda = [1, 2, 3, 4, 5]\nrandom.shuffle(koloda)\nprint(koloda)   # например, [3, 1, 5, 2, 4] — тот же список, новый порядок\n")}
{callout(
        "warning",
        "shuffle() возвращает None — не переприсваивайте результат",
        "<code class=\"inline\">koloda = random.shuffle(koloda)</code> — частая ошибка: после "
        "неё <code class=\"inline\">koloda</code> станет <code class=\"inline\">None</code>, "
        "хотя перемешивание уже прошло успешно ДО присваивания. Просто вызовите "
        "<code class=\"inline\">random.shuffle(koloda)</code> отдельной строкой.",
    )}

{practice_card(
        "05-19",
        "Практика: choice, choices, sample, shuffle",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-19/index.html",
    )}
    """
    out = render_page(
        page_title="choice, choices, sample, shuffle",
        description="Случайный выбор из набора значений в Python: choice, choices (с повторами), sample (без повторов) и shuffle.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("choice, choices, sample, shuffle", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="choice, choices, sample, shuffle",
        lede="Четыре похожих инструмента для случайного выбора — отличаются тем, сколько элементов "
        "выбирают и можно ли повторяться.",
        body_html=body,
        sidebar_groups=sidebar("05-19-choice-sample-shuffle.html"),
        nav=PageNav(prev_href="05-18-randint-randrange-uniform.html", prev_label="randint, randrange, uniform", next_href="05-20-seed.html", next_label="seed и воспроизводимость"),
    )
    write("05-19-choice-sample-shuffle.html", out)


def build_20_seed() -> None:
    dmap = decision_map(
        [
            ("Нужна случайность для игры, симуляции, тестового примера?", "используйте <code class=\"inline\">random</code>"),
            ("Нужна случайность для пароля, токена, ключа безопасности?", "используйте <code class=\"inline\">secrets</code>"),
        ],
        title="random или secrets?",
        caption="random оптимизирован для скорости и предсказуемости при том же seed — это НЕ подходит для защиты данных",
    )
    body = f"""
    <h2><code class="inline">seed()</code> — задаём начальное состояние генератора</h2>
    <p>Раз псевдослучайный генератор — это формула с состоянием, то, задав одно и то же начальное
    состояние («зерно», seed), можно заставить его выдать ровно ту же последовательность чисел
    снова:</p>
{code_block("seed.py", "import random\n\nrandom.seed(42)\nprint(random.randint(1, 100))   # всегда одно и то же число при seed(42)\n\nrandom.seed(42)                 # сбрасываем состояние заново\nprint(random.randint(1, 100))   # то же самое число, что и в первый раз\n")}
{callout(
        "tip",
        "Зачем это нужно на практике",
        "Воспроизводимость критична при отладке: если баг проявляется только «иногда», "
        "<code class=\"inline\">random.seed()</code> позволяет зафиксировать конкретную "
        "«случайную» последовательность и повторно воспроизвести баг столько раз, сколько нужно "
        "для его исправления. Она же используется для автоматической проверки практик этой главы "
        "— без фиксированного seed автоматически проверить случайный результат было бы невозможно.",
    )}

    <h2>Независимые генераторы: <code class="inline">random.Random()</code></h2>
    <p>Все функции модуля <code class="inline">random</code>, которые мы использовали, работают с
    одним общим, «глобальным» генератором. Если нужен отдельный, независимый генератор —
    например, чтобы одна часть программы не влияла на случайность другой — можно создать
    собственный экземпляр:</p>
{code_block("random_instance.py", "import random\n\ngenerator_a = random.Random(1)\ngenerator_b = random.Random(1)\n\nprint(generator_a.randint(1, 100))   # оба генератора созданы с одним и тем же seed —\nprint(generator_b.randint(1, 100))   # значит, дадут одинаковый результат независимо друг от друга\n")}

    <h2>random — это не безопасно для паролей и ключей</h2>
    <p>Раз <code class="inline">random</code> — <strong>предсказуемый</strong> генератор (тот же
    seed → та же последовательность), его нельзя использовать там, где случайность защищает от
    взлома: пароли, токены сессий, ключи шифрования. Для этого в стандартной библиотеке Python
    есть отдельный модуль — <code class="inline">secrets</code>, спроектированный именно для
    безопасности, а не для скорости.</p>
{dmap}
{code_block("secrets_primer.py", "import secrets\n\ntoken = secrets.token_hex(16)   # криптографически надёжный случайный токен\nprint(token)\n")}
{callout(
        "info",
        "Мы не будем глубоко изучать secrets в этой главе",
        "Достаточно запомнить сам принцип: <code class=\"inline\">random</code> — для игр, "
        "симуляций и учебных задач; <code class=\"inline\">secrets</code> — там, где случайность "
        "защищает что-то ценное. Подробнее о безопасности мы поговорим в более поздних главах.",
    )}

{practice_card(
        "05-20",
        "Практика: seed и воспроизводимость",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-20/index.html",
    )}
    """
    out = render_page(
        page_title="seed и воспроизводимость",
        description="random.seed() для воспроизводимости, независимые генераторы random.Random(), и почему random не подходит для паролей.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("seed и воспроизводимость", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="seed и воспроизводимость",
        lede="Псевдослучайность можно «заморозить» — и это не баг, а важнейшая возможность для "
        "отладки и тестирования.",
        body_html=body,
        sidebar_groups=sidebar("05-20-seed.html"),
        nav=PageNav(prev_href="05-19-choice-sample-shuffle.html", prev_label="choice, choices, sample, shuffle", next_href="05-21-otladka-vychislenij.html", next_label="Отладка вычислений"),
    )
    write("05-20-seed.html", out)


def build_21_debugging() -> None:
    taxonomy = branch_diagram(
        "Вычисление даёт не тот результат, что ожидалось",
        [
            ("Синтаксическая ошибка", "программа вообще не запускается — Python указывает на строку до выполнения"),
            ("Ошибка в формуле", "программа работает, но считает не то, что задумано — приоритет, скобки, не та переменная"),
            ("Особенность представления чисел", "программа работает и вроде бы права, но сравнение или округление ведёт себя неожиданно"),
        ],
        caption="Три разных типа проблем — и три разных способа их искать",
    )
    body = f"""
    <p>Формула, которая выдаёт неверное число, — гораздо коварнее, чем ошибка, которая роняет
    программу: Python не подскажет, что что-то не так. Разберём, как искать такие проблемы
    осознанно, а не методом «поменял и посмотрел».</p>

{taxonomy}

    <h2>1. Синтаксическая ошибка</h2>
    <p>Самый простой случай — программа не запускается вовсе, и Python указывает на конкретную
    строку и символ ещё до начала выполнения:</p>
{code_block("sintaksicheskaya.py", "# itog = (a + b * c\n# SyntaxError: '(' was never closed — не хватает закрывающей скобки\n")}
{callout(
        "tip",
        "Считайте скобки парами",
        "Самый надёжный способ найти незакрытую скобку — считать открывающие и закрывающие "
        "скобки в подозрительной строке отдельно; их должно быть поровну.",
    )}

    <h2>2. Ошибка в формуле</h2>
    <p>Самая опасная категория — программа выполняется без единой ошибки, но результат неверен.
    Обычно за этим стоит одна из трёх причин, которые мы уже разбирали в этой главе:</p>
{comparison_table(
        ["Причина", "Пример", "Где мы это уже видели"],
        [
            ["забытые скобки", "<code class=\"inline\">4 + 7 + 9 / 3</code> вместо <code class=\"inline\">(4 + 7 + 9) / 3</code>", "раздел «Скобки и формулы»"],
            ["не та переменная", "<code class=\"inline\">print(shirina + shirina)</code> вместо <code class=\"inline\">print(perimetr)</code>", "раздел «Скобки и формулы»"],
            ["перепутанный приоритет", "<code class=\"inline\">-2 ** 2</code> — не то же самое, что <code class=\"inline\">(-2) ** 2</code>", "раздел «Унарные операторы»"],
        ],
    )}

    <h2>Приём: трассировка формулы через именованные шаги</h2>
    <p>Когда одна длинная формула даёт подозрительный результат, самый надёжный способ найти
    проблему — разбить её на именованные промежуточные шаги и напечатать каждый:</p>
{code_block(
        "trassirovka.py",
        "# было — одна строка, непонятно, что пошло не так:\n"
        "itog = (cena - skidka) * kolichestvo + dostavka / kolichestvo\n\n"
        "# стало — видно каждый промежуточный результат:\n"
        "cena_so_skidkoj = cena - skidka\n"
        "print(\"Цена со скидкой:\", cena_so_skidkoj)\n\n"
        "summa_za_tovar = cena_so_skidkoj * kolichestvo\n"
        "print(\"Сумма за товар:\", summa_za_tovar)\n\n"
        "dostavka_na_edinicu = dostavka / kolichestvo\n"
        "print(\"Доставка на единицу:\", dostavka_na_edinicu)\n\n"
        "itog = summa_za_tovar + dostavka_na_edinicu\n"
        "print(\"Итог:\", itog)\n",
    )}
{step_reduction_diagram(
        ["итог = (100 − 10) × 3 + 15 / 3", "цена со скидкой = 90", "сумма за товар = 270", "доставка на единицу = 5.0", "итог = 275.0"],
        caption="Трассировка превращает одну загадочную строку в последовательность понятных, проверяемых шагов",
    )}
{callout(
        "tip",
        "Это временный код, а не постоянный",
        "Разбиение на именованные шаги — приём именно для <strong>отладки</strong>. Когда формула "
        "заработает верно, промежуточные <code class=\"inline\">print()</code> обычно убирают, "
        "но иногда осмысленные имена промежуточных переменных стоит оставить — они делают код "
        "понятнее, даже если он больше не в отладке.",
    )}

    <h2>3. Особенность представления чисел</h2>
    <p>Третья категория — код синтаксически верен, формула тоже верна, но результат всё равно
    удивляет. Обычно причина в том, что мы уже подробно разбирали в главе 4:</p>
{code_block("float_lovushka.py", "print(0.1 + 0.2 == 0.3)          # False! — не баг, а особенность float\nprint(round(0.1 + 0.2, 10) == 0.3)  # True — сравнение с допуском работает верно\n")}
{callout(
        "info",
        "Подробности — в главе 4",
        "Почему так происходит и как сравнивать float правильно — подробно разобрано в разделе "
        "«Сравниваем float правильно» главы 4. Здесь достаточно узнавать симптом: сравнение "
        "<code class=\"inline\">==</code> между float ведёт себя неожиданно — значит, дело в "
        "представлении чисел, а не в ошибке формулы.",
    )}

    <h2>Предскажите, прежде чем запускать</h2>
    <p>Лучшая привычка для отладки — формировать её ещё до появления багов: прежде чем запускать
    код, предскажите результат. Если предсказание не совпало с реальностью — вы либо нашли баг,
    либо неверно понимаете код. Оба случая стоит разобрать, не запуская код дальше не глядя.</p>
{exercise(
        1,
        "Предскажите результат",
        "Не запуская код, определите результат: <code class=\"inline\">итог = 2 + 3 * 4 ** 2 // 5</code>. "
        "Затем проверьте себя.",
    )}
{exercise(
        2,
        "Найдите ошибку в формуле",
        "В коде <code class=\"inline\">srednyaya_ocenka = ocenka1 + ocenka2 + ocenka3 / 3</code> "
        "есть ошибка приоритета. Найдите и исправьте её.",
    )}
{exercise(
        3,
        "Трассируйте формулу",
        "Возьмите формулу расчёта итоговой суммы заказа с учётом скидки и доставки из примера выше "
        "и добавьте к ней трассировку с понятными именами промежуточных переменных.",
    )}

{practice_card(
        "05-21",
        "Практика: отладка вычислений",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-21/index.html",
    )}
    """
    out = render_page(
        page_title="Отладка вычислений",
        description="Три типа ошибок в вычислениях Python — синтаксические, формульные и связанные с представлением чисел — и приём трассировки формулы.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Отладка вычислений", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Отладка вычислений",
        lede="Неверное число без единой ошибки — самый коварный тип бага. Разберём три причины и "
        "надёжный способ их искать.",
        body_html=body,
        sidebar_groups=sidebar("05-21-otladka-vychislenij.html"),
        nav=PageNav(prev_href="05-20-seed.html", prev_label="seed и воспроизводимость", next_href="05-06-mini-proekt-itogi.html", next_label="Мини-проекты и итоги"),
    )
    write("05-21-otladka-vychislenij.html", out)


def build_06_mini_projects() -> None:
    final_map = decision_map(
        [
            ("Нужен остаток или проверка кратности?", "// и %"),
            ("Нужна степень или корень?", "** или math.sqrt()"),
            ("Формула не помещается в одну понятную строку?", "именованные промежуточные шаги"),
            ("Нужна геометрия — расстояние, площадь, угол?", "math.hypot() / math.dist() / math.pi"),
            ("Нужна случайность для игры?", "random"),
            ("Нужно повторить один и тот же случайный результат?", "random.seed()"),
        ],
        title="Какой инструмент главы 5 мне нужен?",
        caption="Возвращайтесь к этой карте в будущих проектах — она собирает всю главу в шесть вопросов",
    )
    body = f"""
    <p>Пять небольших, но настоящих проектов — каждый использует только то, что мы уже прошли в
    этой главе.</p>

    <h2 id="proekt-1">Проект 1: умный калькулятор</h2>
    <p>Считаем результат в зависимости от того, какой оператор выбран — <code class="inline">+</code>,
    <code class="inline">-</code>, <code class="inline">*</code> или <code class="inline">/</code>:</p>
{callout(
        "info",
        "Забегаем вперёд",
        "Здесь использована конструкция <code class=\"inline\">if / elif</code> — мы разберём её "
        "подробно в главе 8. Пока достаточно прочитать её как обычный текст: «если оператор "
        "такой-то — сделай так, а если другой — иначе».",
    )}
{code_block(
        "umnyj_kalkulyator.py",
        "a, b = 12, 4\noperator = \"+\"\n\n"
        "if operator == \"+\":\n    rezultat = a + b\n"
        "elif operator == \"-\":\n    rezultat = a - b\n"
        "elif operator == \"*\":\n    rezultat = a * b\n"
        "elif operator == \"/\":\n    rezultat = a / b\n\n"
        "print(rezultat)   # 16\n",
    )}
{exercise(1, "Добавьте //, % и **", "Расширьте калькулятор так, чтобы он умел также целочисленное деление, остаток и возведение в степень.")}

    <h2 id="proekt-2">Проект 2: конвертер времени — версия короче</h2>
    <p>Мы уже решали эту задачу в главе 4 — через <code class="inline">//</code> и
    <code class="inline">%</code> по отдельности. Теперь, когда мы знаем <code class="inline">divmod()</code>
    (раздел «Деление с остатком»), можно решить её вдвое короче:</p>
{code_block(
        "konverter_vremeni_divmod.py",
        "total_seconds = 3725\n\n"
        "hours, ostatok = divmod(total_seconds, 3600)\n"
        "minutes, seconds = divmod(ostatok, 60)\n\n"
        "print(f\"{hours}ч {minutes}м {seconds}с\")   # 1ч 2м 5с\n",
    )}
{exercise(2, "Challenge", "Проверьте свой конвертер на 0 секунд и на 90000 секунд (больше суток).")}

    <h2 id="proekt-3">Проект 3: лаборатория кубика</h2>
    <p>Бросаем два кубика и считаем сумму и среднее — используем <code class="inline">random.randint()</code>
    и уже знакомые операторы:</p>
{code_block(
        "laboratoriya_kubika.py",
        "import random\n\n"
        "kub1 = random.randint(1, 6)\n"
        "kub2 = random.randint(1, 6)\n"
        "summa = kub1 + kub2\n"
        "srednee = summa / 2\n\n"
        "print(f\"Кубик 1: {kub1}, кубик 2: {kub2}\")\n"
        "print(f\"Сумма: {summa}, среднее: {srednee}\")\n",
    )}
{exercise(2, "Дубль!", "Добавьте проверку: если оба кубика выпали одинаковыми — выведите «Дубль!» (используйте == из главы 3).")}

    <h2 id="proekt-4">Проект 4: случайный челлендж — кратные числа</h2>
    <p>Программа, которая находит все числа, кратные случайно выбранному — используем
    <code class="inline">random</code> и <code class="inline">%</code> вместе:</p>
{code_block(
        "kratnye_chisla.py",
        "import random\n\n"
        "# случайное число, кратности которого мы ищем\n"
        "kratnoe_chemu = random.randint(2, 9)\n"
        "print(f\"Ищем числа, кратные {kratnoe_chemu}, от 1 до 50\")\n\n"
        "chislo = 1\n"
        "while chislo <= 50:\n"
        "    if chislo % kratnoe_chemu == 0:\n"
        "        print(chislo)\n"
        "    chislo += 1\n",
    )}
{callout(
        "info",
        "Забегаем вперёд ещё раз",
        "Цикл <code class=\"inline\">while</code> мы разберём подробно в главе 10. Здесь важно "
        "увидеть, как оператор <code class=\"inline\">%</code> из этой главы находит все числа, "
        "кратные заданному: остаток от деления равен нулю именно тогда, когда число делится "
        "нацело.",
    )}
{exercise(3, "Свой диапазон", "Измените границы поиска на 1–100 вместо 1–50.")}

    <h2 id="proekt-5">Проект 5: геометрическая лаборатория</h2>
    <p>Собираем сразу несколько формул этой главы: расстояние между двумя точками и площадь круга
    такого радиуса:</p>
{code_block(
        "geometricheskaya_laboratoriya.py",
        "import math\n\n"
        "tochka_a = (0, 0)\n"
        "tochka_b = (3, 4)\n\n"
        "radius = math.dist(tochka_a, tochka_b)\n"
        "ploshad_kruga = math.pi * radius ** 2\n\n"
        "print(f\"Расстояние между точками: {radius}\")\n"
        "print(f\"Площадь круга такого радиуса: {round(ploshad_kruga, 2)}\")\n",
    )}
{exercise(3, "Периметр треугольника", "Добавьте третью точку и посчитайте периметр треугольника, образованного всеми тремя точками, используя math.dist() трижды.")}

{practice_card(
        "05-06",
        "Практика: мини-проекты главы 5",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-06/index.html",
    )}

    <h2 id="finalnaya-karta">Финальная карта главы</h2>
{final_map}

    <h2 id="itogi">Итоги главы</h2>
{summary_box("Что мы теперь умеем", [
        "Выражение — операнды плюс оператор; отличаем выражение от инструкции (statement).",
        "Основные операторы <code class=\"inline\">+ - * /</code> и их геометрические модели: "
        "числовая прямая для +/-, прямоугольник для умножения.",
        "<code class=\"inline\">//</code>, <code class=\"inline\">%</code> и "
        "<code class=\"inline\">divmod()</code> — включая то, как они работают с отрицательными "
        "числами (округление к минус бесконечности).",
        "<code class=\"inline\">**</code>, <code class=\"inline\">pow()</code> и "
        "<code class=\"inline\">math.pow()</code> — и классическая ловушка "
        "<code class=\"inline\">-2 ** 2</code>.",
        "Сокращённые операторы присваивания, полная карта приоритета и ассоциативность "
        "(включая правоассоциативность <code class=\"inline\">**</code>).",
        "Перевод формул из математической записи в Python — и типичные ошибки перевода.",
        "Глубокий модуль <code class=\"inline\">math</code>: корни и расстояния, "
        "gcd/lcm/factorial/comb/perm, геометрия, тригонометрия, логарифмы.",
        "Глубокий модуль <code class=\"inline\">random</code>: псевдослучайность, "
        "randint/randrange/uniform, choice/choices/sample/shuffle, seed и random vs secrets.",
        "Отладка вычислений: три типа ошибок и приём трассировки формулы через именованные шаги.",
    ])}

    <h2 id="dalshe">Что дальше</h2>
    <p>В главе 6 мы возьмём числа, которые теперь умеем считать, и начнём их <strong>рисовать</strong>
    — познакомимся с модулем <code class="inline">turtle</code> и нарисуем первые фигуры на экране.
    Координаты, углы и расстояния из этой главы там сразу пригодятся.</p>
    """
    out = render_page(
        page_title="Мини-проекты и итоги",
        description="Пять мини-проектов главы 5: умный калькулятор, конвертер времени, лаборатория кубика, случайный челлендж и геометрическая лаборатория — и итоги главы.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Мини-проекты и итоги", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Мини-проекты и итоги",
        lede="Собираем всю главу в пяти небольших, но настоящих проектах — и подводим итоги.",
        body_html=body,
        sidebar_groups=sidebar("05-06-mini-proekt-itogi.html"),
        nav=PageNav(prev_href="05-21-otladka-vychislenij.html", prev_label="Отладка вычислений", next_href="../glava-06/index.html", next_label="Глава 6: Рисуем классные вещи с помощью Turtle"),
    )
    write("05-06-mini-proekt-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01_expressions()
    build_07_division_remainder()
    build_08_negative_division()
    build_02_powers_roots()
    build_09_unary_operators()
    build_03_assignment_precedence()
    build_10_associativity()
    build_11_parentheses_formulas()
    build_12_formula_translation()
    build_04_math_module()
    build_13_roots_distances()
    build_14_gcd_lcm_factorial()
    build_15_geometry()
    build_16_trigonometry()
    build_17_logarithms()
    build_05_random_module()
    build_18_randint_randrange_uniform()
    build_19_choice_sample_shuffle()
    build_20_seed()
    build_21_debugging()
    build_06_mini_projects()
    print("Глава 5 полностью собрана.")
