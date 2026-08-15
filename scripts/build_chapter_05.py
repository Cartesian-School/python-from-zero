#!/usr/bin/env python3
"""Строит Главу 5: «Давайте поиграем с числами!» (site/chapters/glava-05/)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_lib import (
    ChapterSectionLink,
    NavItem,
    PageNav,
    SidebarGroup,
    callout,
    classic_vs_modern,
    code_block,
    exercise,
    practice_card,
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-05"

PAGES = [
    ("index.html", "Приступаем"),
    ("05-01-osnovnye-operacii.html", "Основные математические операции"),
    ("05-02-specialnye-operacii.html", "Специальные математические операции"),
    ("05-03-prisvaivanie-poryadok.html", "Операции присваивания и порядок вычислений"),
    ("05-04-matematicheskie-funkcii.html", "Интересные возможности работы с числами"),
    ("05-05-sluchaynye-chisla.html", "Работа со случайными числами"),
    ("05-06-mini-proekt-itogi.html", "Мини-проект и итоги"),
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 5 · Числа играют", items),
        SidebarGroup("Практика", [
            NavItem("🐍 05-01: Практика", "../../practice/05-01/index.html"),
            NavItem("🐍 05-02: Практика", "../../practice/05-02/index.html"),
            NavItem("🐍 05-04: Практика", "../../practice/05-04/index.html"),
            NavItem("🐍 05-05: Практика", "../../practice/05-05/index.html"),
            NavItem("🐍 05-06: Практика", "../../practice/05-06/index.html"),
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
        description="Математические операторы, порядок вычислений, модули math и random.",
        meta_items=["⏱ ~1.5 часа", "🧮 math и random", "📓 5 ноутбуков практики"],
        sections=[
            ChapterSectionLink("5.1", "Основные математические операции", "05-01-osnovnye-operacii.html", "60"),
            ChapterSectionLink("5.2", "Специальные математические операции", "05-02-specialnye-operacii.html", "62"),
            ChapterSectionLink("5.3", "Операции присваивания", "05-03-prisvaivanie-poryadok.html", "65"),
            ChapterSectionLink("", "Что выполняется первым?", "05-03-prisvaivanie-poryadok.html#poryadok", "67"),
            ChapterSectionLink("5.4", "Интересные возможности работы с числами", "05-04-matematicheskie-funkcii.html", "70"),
            ChapterSectionLink("5.5", "Работа со случайными числами", "05-05-sluchaynye-chisla.html", "75"),
            ChapterSectionLink("5.6", "Мини-проект — кратные числа", "05-06-mini-proekt-itogi.html", "78"),
            ChapterSectionLink("", "Итоги", "05-06-mini-proekt-itogi.html#itogi", "81"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <p>В главе 4 мы познакомились с числами. Теперь научим Python по-настоящему с ними
    работать — считать, сравнивать, комбинировать. Начнём с четырёх операций, знакомых из
    школьной математики.</p>

    {code_block(
        "osnovnye_operacii.py",
        "print(5 + 3)   # сложение\n"
        "print(5 - 3)   # вычитание\n"
        "print(5 * 3)   # умножение\n"
        "print(5 / 3)   # деление — всегда float\n",
    )}

    {callout(
        "tip",
        "Числа и переменные — как в главе 4",
        "Все эти операторы работают и с переменными, не только с числами напрямую: "
        "<code class=\"inline\">a + b</code> работает точно так же, как "
        "<code class=\"inline\">5 + 3</code>, если <code class=\"inline\">a</code> и "
        "<code class=\"inline\">b</code> — числа.",
    )}

    {practice_card(
        "05-01",
        "Практика: +, -, *, / на практике",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-01/index.html",
    )}
    """
    out = render_page(
        page_title="Основные математические операции",
        description="Сложение, вычитание, умножение и деление в Python.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Основные операции", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Основные математические операции",
        lede="Четыре оператора, знакомые со школы — но у деления в Python есть особенность, "
        "которую мы уже видели в главе 3.",
        body_html=body,
        sidebar_groups=sidebar("05-01-osnovnye-operacii.html"),
        nav=PageNav(prev_href="index.html", prev_label="Приступаем", next_href="05-02-specialnye-operacii.html", next_label="Специальные операции"),
    )
    write("05-01-osnovnye-operacii.html", out)


def build_02() -> None:
    body = f"""
    <p>Кроме четырёх основных операций, у Python есть три специальных, которых нет в
    привычном калькуляторе, но которые невероятно полезны в программировании.</p>

    <h2>Целочисленное деление <code class="inline">//</code></h2>
    <p>Возвращает только целую часть результата деления, отбрасывая остаток:</p>
    {code_block("celochislennoe.py", "print(17 // 5)   # 3 — сколько раз 5 помещается в 17 целиком\nprint(17 / 5)    # 3.4 — обычное деление, для сравнения\n")}

    <h2>Остаток от деления <code class="inline">%</code></h2>
    <p>Возвращает то, что <em>осталось</em> после целочисленного деления. Один из самых полезных
    операторов в программировании — например, для проверки чётности числа:</p>
    {code_block("ostatok.py", "print(17 % 5)    # 2 — именно столько осталось\nprint(10 % 2)    # 0 — если остаток 0, число чётное\nprint(11 % 2)    # 1 — а если 1 — нечётное\n")}

    {callout(
        "tip",
        "Проверка чётности — классический приём",
        "<code class=\"inline\">число % 2 == 0</code> — самый частый способ проверить, чётное "
        "ли число. Мы воспользуемся им в мини-проекте главы 9.",
    )}

    <h2>Возведение в степень <code class="inline">**</code></h2>
    {code_block("stepen.py", "print(2 ** 10)    # 1024\nprint(9 ** 0.5)   # 3.0 — дробная степень 0.5 = квадратный корень\n")}

    {practice_card(
        "05-02",
        "Практика: //, % и ** на практике",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-02/index.html",
    )}
    """
    out = render_page(
        page_title="Специальные математические операции",
        description="Целочисленное деление //, остаток от деления % и возведение в степень ** в Python.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Специальные операции", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Специальные математические операции в Python",
        lede="Три оператора, которых нет на обычном калькуляторе — но без них не обходится "
        "почти ни одна программа.",
        body_html=body,
        sidebar_groups=sidebar("05-02-specialnye-operacii.html"),
        nav=PageNav(prev_href="05-01-osnovnye-operacii.html", prev_label="Основные операции", next_href="05-03-prisvaivanie-poryadok.html", next_label="Присваивание и порядок вычислений"),
    )
    write("05-02-specialnye-operacii.html", out)


def build_03() -> None:
    body = f"""
    <h2>Операции присваивания</h2>
    <p>Изменить переменную «на основе самой себя» — очень частое действие: например,
    увеличить счёт в игре. Писать <code class="inline">score = score + 10</code> можно, но
    Python предлагает более короткую запись:</p>
    {code_block("prisvaivanie.py", "score = 0\nscore += 10   # то же самое, что score = score + 10\nprint(score)  # 10\n\nscore -= 3    # score = score - 3\nprint(score)  # 7\n")}
    <p>Такие сокращения существуют для всех основных операторов:
    <code class="inline">+=</code>, <code class="inline">-=</code>,
    <code class="inline">*=</code>, <code class="inline">/=</code>,
    <code class="inline">//=</code>, <code class="inline">%=</code>,
    <code class="inline">**=</code>.</p>

    <h2 id="poryadok">Что выполняется первым?</h2>
    <p>Как и в математике, у операторов в Python есть порядок выполнения: сначала — степень,
    затем — умножение, деление, целочисленное деление и остаток (слева направо), и в конце —
    сложение и вычитание.</p>
    {code_block("poryadok.py", "print(2 + 3 * 4)     # 14 — сначала 3 * 4 = 12, потом + 2\nprint((2 + 3) * 4)   # 20 — скобки меняют порядок\nprint(2 ** 3 ** 2)   # 512 — возведение в степень выполняется справа налево: 2 ** (3 ** 2)\n")}

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
        "Тот же ноутбук, что и в разделе «Специальные операции» — он охватывает обе темы",
        "../../practice/05-02/index.html",
    )}
    """
    out = render_page(
        page_title="Операции присваивания и порядок вычислений",
        description="Сокращённые операторы присваивания (+=, -= и другие) и порядок выполнения операций в Python.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Присваивание и порядок", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Операции присваивания",
        lede="Более короткая запись для изменения переменных — и правила о том, что "
        "выполняется раньше, а что позже.",
        body_html=body,
        sidebar_groups=sidebar("05-03-prisvaivanie-poryadok.html"),
        nav=PageNav(prev_href="05-02-specialnye-operacii.html", prev_label="Специальные операции", next_href="05-04-matematicheskie-funkcii.html", next_label="Интересные возможности"),
    )
    write("05-03-prisvaivanie-poryadok.html", out)


def build_04() -> None:
    body = f"""
    <p>Для более сложной математики в Python есть встроенный модуль <code class="inline">math</code>
    — набор готовых функций, который нужно сначала подключить командой
    <code class="inline">import math</code>.</p>

    <h2 id="pol-potolok">Пол и потолок числа</h2>
    <p><strong>Пол</strong> (floor) — ближайшее целое число снизу, <strong>потолок</strong>
    (ceil) — ближайшее целое число сверху.</p>
    {code_block("pol_potolok.py", "import math\n\nprint(math.floor(4.3))   # 4\nprint(math.floor(4.9))   # 4 — всегда вниз, даже если дробь большая\nprint(math.ceil(4.1))    # 5 — всегда вверх, даже если дробь маленькая\n")}

    {callout(
        "info",
        "А как же обычное округление?",
        "Для округления «как в школе» (0.5 и выше — вверх) в Python есть встроенная функция "
        "<code class=\"inline\">round()</code> — её не нужно импортировать из "
        "<code class=\"inline\">math</code>: <code class=\"inline\">round(4.5)</code> → "
        "<code class=\"inline\">4</code> (осторожно: из-за особого банковского округления "
        "Python иногда округляет «．5» к ближайшему чётному числу).",
    )}

    <h2>Степень и квадратный корень</h2>
    {code_block("koren.py", "import math\n\nprint(math.pow(2, 10))   # 1024.0 — всегда возвращает float, в отличие от **\nprint(math.sqrt(81))     # 9.0\n")}

    <h2>Факториал числа</h2>
    <p>Факториал числа <code class="inline">n</code> (обозначается <code class="inline">n!</code>)
    — произведение всех целых чисел от 1 до <code class="inline">n</code>. Используется, например,
    для подсчёта числа возможных перестановок.</p>
    {code_block("faktorial.py", "import math\n\nprint(math.factorial(5))   # 5! = 1 * 2 * 3 * 4 * 5 = 120\n")}

    <h2>Синус, косинус, тангенс и многое другое</h2>
    <p>Модуль <code class="inline">math</code> включает и тригонометрические функции — они
    понадобятся, например, при рисовании окружностей и дуг в главе 7.</p>
    {code_block("trigonometriya.py", "import math\n\nprint(math.sin(math.pi / 2))   # 1.0\nprint(math.cos(0))             # 1.0\nprint(math.tan(math.pi / 4))   # приблизительно 1.0\n")}

    <h2>Другие числовые операции</h2>
    <p>Ещё несколько полезных инструментов, которые не требуют импорта: встроенные функции
    <code class="inline">abs()</code> (модуль числа), <code class="inline">min()</code> и
    <code class="inline">max()</code> (наименьшее и наибольшее из нескольких значений):</p>
    {code_block("drugie.py", "print(abs(-7))         # 7\nprint(min(4, 9, 2))    # 2\nprint(max(4, 9, 2))    # 9\n")}

    {practice_card(
        "05-04",
        "Практика: модуль math на практике",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-04/index.html",
    )}
    """
    out = render_page(
        page_title="Интересные возможности работы с числами",
        description="Модуль math в Python: floor, ceil, sqrt, factorial, тригонометрия и другие функции.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Интересные возможности", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Интересные возможности работы с числами",
        lede="Модуль math открывает пол и потолок числа, корни, факториалы и тригонометрию — "
        "всё то, чего не хватает базовым операторам.",
        body_html=body,
        sidebar_groups=sidebar("05-04-matematicheskie-funkcii.html"),
        nav=PageNav(prev_href="05-03-prisvaivanie-poryadok.html", prev_label="Присваивание и порядок", next_href="05-05-sluchaynye-chisla.html", next_label="Случайные числа"),
    )
    write("05-04-matematicheskie-funkcii.html", out)


def build_05() -> None:
    cvm = classic_vs_modern(
        "Диапазон случайных чисел: вручную → готовая функция",
        "Классический подход",
        "import random\n\n"
        "# случайное целое от 1 до 6 вручную:\n"
        "roll = int(random.random() * 6) + 1\n"
        "print(roll)",
        "Современный Python 3.14",
        "import random\n\n"
        "# то же самое — готовой функцией\n"
        "roll = random.randint(1, 6)\n"
        "print(roll)",
        "готовые функции вроде <code class=\"inline\">randint()</code> и "
        "<code class=\"inline\">uniform()</code> — они существовали в модуле random ещё в "
        "старых версиях Python, но начинающие часто сначала пытаются собрать диапазон вручную "
        "через <code class=\"inline\">random.random()</code>, не зная о них. Готовые функции "
        "короче и меньше подвержены ошибкам — особенно на границах диапазона.",
    )

    body = f"""
    <p>Модуль <code class="inline">random</code> добавляет в Python элемент случайности —
    без него не обходится почти ни одна игра: случайный противник, случайная карта, случайное
    число для игры «Угадай число» в главе 9.</p>

    {code_block("sluchaynye.py", "import random\n\nprint(random.random())          # случайное дробное число от 0.0 до 1.0 (не включая 1.0)\nprint(random.randint(1, 6))     # случайное целое от 1 до 6 включительно — как кубик\nprint(random.uniform(1, 10))    # случайное дробное от 1 до 10\n")}

    {callout(
        "warning",
        "randint включает обе границы",
        "<code class=\"inline\">random.randint(1, 6)</code> может вернуть и "
        "<code class=\"inline\">1</code>, и <code class=\"inline\">6</code> — обе границы "
        "включены. Это частая причина ошибок «на единицу» (off-by-one), если забыть об этом.",
    )}

    <h2>Случайный выбор из списка</h2>
    <p>Забегая немного вперёд (списки подробно разберём в главе 11) — <code class="inline">random.choice()</code>
    умеет выбрать случайный элемент из готового набора значений:</p>
    {code_block("sluchaynyj_vybor.py", 'import random\n\nvariants = ["камень", "ножницы", "бумага"]\nprint(random.choice(variants))\n')}

    {cvm}

    {practice_card(
        "05-05",
        "Практика: модуль random на практике",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-05/index.html",
    )}
    """
    out = render_page(
        page_title="Работа со случайными числами",
        description="Модуль random в Python: random(), randint(), uniform(), choice().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Случайные числа", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Работа со случайными числами",
        lede="Без капли случайности сложно представить хоть одну игру — знакомимся с модулем "
        "random.",
        body_html=body,
        sidebar_groups=sidebar("05-05-sluchaynye-chisla.html"),
        nav=PageNav(prev_href="05-04-matematicheskie-funkcii.html", prev_label="Интересные возможности", next_href="05-06-mini-proekt-itogi.html", next_label="Мини-проект и итоги"),
    )
    write("05-05-sluchaynye-chisla.html", out)


def build_06() -> None:
    body = f"""
    <p>Соберём операторы этой главы в один мини-проект: программу, которая находит все числа,
    кратные заданному, в диапазоне.</p>

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
        "Забегаем вперёд",
        "В этом примере использован цикл <code class=\"inline\">while</code> — мы разберём его "
        "подробно в главе 10. Здесь достаточно увидеть, как оператор <code class=\"inline\">%</code> "
        "из этой главы находит все числа, кратные заданному: остаток от деления равен нулю "
        "именно тогда, когда число делится нацело.",
    )}

    {exercise(
        1,
        "Кратные тройке",
        "Измените программу так, чтобы она всегда искала числа, кратные 3, без "
        "<code class=\"inline\">random</code>.",
    )}
    {exercise(
        2,
        "Свой диапазон",
        "Измените границы поиска на 1–100 вместо 1–50.",
    )}
    {exercise(
        3,
        "Считаем количество",
        "Добавьте переменную-счётчик, которая считает, сколько кратных чисел было найдено, и "
        "выведите её значение в конце.",
    )}
{practice_card(
        "05-06",
        "Практика: кратные числа",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/05-06/index.html",
    )}

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
        "Основные операторы: <code class=\"inline\">+ - * /</code>; специальные: "
        "<code class=\"inline\">// % **</code>.",
        "<code class=\"inline\">%</code> (остаток от деления) — классический способ проверить "
        "чётность и кратность числа.",
        "Сокращённые операторы присваивания (<code class=\"inline\">+=</code> и другие) "
        "изменяют переменную короче, чем <code class=\"inline\">x = x + ...</code>.",
        "Порядок вычислений совпадает со школьной математикой; скобки — самый надёжный способ "
        "сделать порядок явным.",
        "Модуль <code class=\"inline\">math</code> добавляет floor, ceil, sqrt, factorial и "
        "тригонометрию.",
        "Модуль <code class=\"inline\">random</code> добавляет случайность — основу для игр из "
        "следующих глав.",
    ])}
    """
    out = render_page(
        page_title="Мини-проект — кратные числа",
        description="Итоговый мини-проект главы 5: поиск чисел, кратных заданному — и краткие итоги.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 5", "index.html"), ("Мини-проект и итоги", "")],
        kicker="Глава 5 · Давайте поиграем с числами!",
        h1="Мини-проект — кратные числа",
        lede="Собираем операторы главы вместе в одной небольшой программе — и подводим итоги.",
        body_html=body,
        sidebar_groups=sidebar("05-06-mini-proekt-itogi.html"),
        nav=PageNav(prev_href="05-05-sluchaynye-chisla.html", prev_label="Случайные числа", next_href="../glava-06/index.html", next_label="Глава 6: Рисуем классные вещи с помощью Turtle"),
    )
    write("05-06-mini-proekt-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01()
    build_02()
    build_03()
    build_04()
    build_05()
    build_06()
