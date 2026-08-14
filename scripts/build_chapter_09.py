#!/usr/bin/env python3
"""Строит Главу 9: «Выполняй мою команду!» (site/chapters/glava-09/)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_lib import (
    ChapterSectionLink,
    NavItem,
    PageNav,
    SidebarGroup,
    callout,
    code_block,
    exercise,
    notebook_card,
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-09"

PAGES = [
    ("index.html", "Обзор главы"),
    ("09-01-istina-ili-lozh.html", "Истина или ложь"),
    ("09-02-sravnenie-i-reshenie.html", "Сравниваем и принимаем решение"),
    ("09-03-if-inache.html", "Если это произошло — выполни команду!"),
    ("09-04-neskolko-uslovij.html", "Больше одного условия!"),
    ("09-05-mini-proekt-ugadaj-chislo.html", "Мини-проект: «Угадай число»"),
    ("09-06-nakoplenie-uslovij-itogi.html", "Условия накапливаются и итоги"),
]

NOTEBOOKS = [
    "09-01-istina-lozh.ipynb",
    "09-02-sravnenie.ipynb",
    "09-03-if-else.ipynb",
    "09-04-and-or-not.ipynb",
    "09-05-ugadaj-chislo.ipynb",
    "09-06-elif.ipynb",
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 9 · Условия", items),
        SidebarGroup("Практика", [NavItem(f"📓 {n}", f"../../../notebooks/chapter-09/{n}") for n in NOTEBOOKS]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=9,
        baseline_page=175,
        title="Выполняй мою команду!",
        description="Логические значения, сравнения, условный оператор if/elif/else и первая настоящая игра.",
        meta_items=["⏱ ~2 часа", "🔀 if / elif / else", "📓 6 ноутбуков практики"],
        sections=[
            ChapterSectionLink("9.1", "Истина или ложь", "09-01-istina-ili-lozh.html", "175"),
            ChapterSectionLink("9.2", "Сравниваем и принимаем решение", "09-02-sravnenie-i-reshenie.html", "179"),
            ChapterSectionLink("9.3", "Если это произошло — выполни команду!", "09-03-if-inache.html", "180"),
            ChapterSectionLink("", "А иначе?", "09-03-if-inache.html#inache", "183"),
            ChapterSectionLink("9.4", "Больше одного условия!", "09-04-neskolko-uslovij.html", "184"),
            ChapterSectionLink("9.5", "Мини-проект — игра «Угадай число»", "09-05-mini-proekt-ugadaj-chislo.html", "186"),
            ChapterSectionLink("9.6", "Условия продолжают накапливаться!", "09-06-nakoplenie-uslovij-itogi.html", "189"),
            ChapterSectionLink("", "Итоги", "09-06-nakoplenie-uslovij-itogi.html#itogi", "193"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <p>До сих пор все наши программы выполняли одни и те же команды при каждом запуске. Пора
    научить их <strong>принимать решения</strong> — делать одно, если верно одно условие, и
    другое, если верно другое. Всё начинается с логического типа данных.</p>

    <h2>Логический тип: bool</h2>
    <p>Тип <code class="inline">bool</code> имеет всего два возможных значения:
    <code class="inline">True</code> (истина) и <code class="inline">False</code> (ложь) — с
    заглавной буквы, это ключевые слова Python, а не обычный текст.</p>
    {code_block("bool.py", "is_sunny = True\nis_raining = False\nprint(is_sunny, type(is_sunny))\n")}

    <h2>Как получить bool</h2>
    <p>Чаще всего <code class="inline">True</code>/<code class="inline">False</code> не пишут
    вручную, а получают в результате сравнения:</p>
    {code_block("sravnenie_bool.py", "print(5 > 3)     # True\nprint(5 == 3)    # False\n")}

    <h2>«Истинность» других типов</h2>
    <p>Мы уже видели в главе 8, что пустая строка ведёт себя как <code class="inline">False</code>,
    а непустая — как <code class="inline">True</code>. То же правило работает для чисел и для
    других типов данных, которые мы изучим позже:</p>
    {code_block("istinnost.py", "print(bool(0))      # False — ноль считается «ложью»\nprint(bool(42))     # True — любое ненулевое число — «истина»\nprint(bool(\"\"))     # False — пустая строка\nprint(bool(\"нет\"))  # True — любая непустая строка, даже такая!\n")}

    {callout(
        "warning",
        "bool(\"False\") — это True!",
        "Строка <code class=\"inline\">\"False\"</code> — непустая, значит,"
        " <code class=\"inline\">bool(\"False\")</code> равно <code class=\"inline\">True</code>."
        " Единственная строка, которая ведёт себя как ложь — пустая строка "
        "<code class=\"inline\">\"\"</code>.",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "09-01-istina-lozh.ipynb · тип bool и истинность значений",
        "../../../notebooks/chapter-09/09-01-istina-lozh.ipynb",
    )}
    """
    out = render_page(
        page_title="Истина или ложь",
        description="Логический тип bool в Python и истинность значений разных типов.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("Истина или ложь", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Истина или ложь",
        lede="Прежде чем программа сможет принимать решения, ей нужен способ хранить сам "
        "результат решения — логический тип bool.",
        body_html=body,
        sidebar_groups=sidebar("09-01-istina-ili-lozh.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="09-02-sravnenie-i-reshenie.html", next_label="Сравниваем и принимаем решение"),
    )
    write("09-01-istina-ili-lozh.html", out)


def build_02() -> None:
    body = f"""
    <p>Полный набор операторов сравнения в Python:</p>
    {code_block(
        "operatory_sravneniya.py",
        "print(5 == 5)   # равно\n"
        "print(5 != 3)   # не равно\n"
        "print(5 > 3)    # больше\n"
        "print(5 < 3)    # меньше\n"
        "print(5 >= 5)   # больше или равно\n"
        "print(5 <= 3)   # меньше или равно\n",
    )}

    {callout(
        "warning",
        "= против ==",
        "Одиночный <code class=\"inline\">=</code> — это присваивание (\"положить значение в "
        "переменную\"), а двойной <code class=\"inline\">==</code> — сравнение (\"равны ли "
        "значения\"). Перепутать их — одна из самых частых ошибок у новичков в любом языке "
        "программирования, не только в Python.",
    )}

    <h2>Сравнивать можно и строки</h2>
    <p>Мы видели это в главе 8 — строки сравниваются по алфавиту символ за символом:</p>
    {code_block("sravnenie_strok.py", 'print("apple" < "banana")   # True — "a" идёт раньше "b" в алфавите\nprint("Python" == "python") # False — регистр важен\n')}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "09-02-sravnenie.ipynb · все шесть операторов сравнения",
        "../../../notebooks/chapter-09/09-02-sravnenie.ipynb",
    )}
    """
    out = render_page(
        page_title="Сравниваем и принимаем решение",
        description="Операторы сравнения в Python: ==, !=, <, >, <=, >=.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("Сравниваем и решаем", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Сравниваем и принимаем решение",
        lede="Шесть операторов, которые превращают два значения в один bool.",
        body_html=body,
        sidebar_groups=sidebar("09-02-sravnenie-i-reshenie.html"),
        nav=PageNav(prev_href="09-01-istina-ili-lozh.html", prev_label="Истина или ложь", next_href="09-03-if-inache.html", next_label="Если это произошло — выполни команду!"),
    )
    write("09-02-sravnenie-i-reshenie.html", out)


def build_03() -> None:
    body = f"""
    <h2>Если это произошло — выполни команду!</h2>
    <p>Условный оператор <code class="inline">if</code> выполняет блок кода только тогда, когда
    условие после него истинно (<code class="inline">True</code>). Обратите внимание на
    двоеточие и отступ — они обязательны в Python:</p>
    {code_block(
        "if.py",
        "age = 20\n\n"
        "if age >= 18:\n"
        '    print("Доступ разрешён.")\n',
    )}

    {callout(
        "warning",
        "IndentationError",
        "Строка после <code class=\"inline\">if ...:</code> обязательно должна иметь отступ "
        "(обычно 4 пробела). Без отступа Python выдаст <code class=\"inline\">IndentationError"
        "</code>. Отступ — не просто оформление: именно им Python определяет, какие строки "
        "относятся к блоку <code class=\"inline\">if</code>, а какие уже нет.",
    )}

    <h2 id="inache">А иначе?</h2>
    <p><code class="inline">else</code> задаёт блок кода, который выполнится, если условие
    оказалось ложным:</p>
    {code_block(
        "if_else.py",
        "age = 15\n\n"
        "if age >= 18:\n"
        '    print("Доступ разрешён.")\n'
        "else:\n"
        '    print("Доступ запрещён — вам ещё нет 18.")\n',
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "09-03-if-else.ipynb · условный оператор if/else",
        "../../../notebooks/chapter-09/09-03-if-else.ipynb",
    )}
    """
    out = render_page(
        page_title="Если это произошло — выполни команду!",
        description="Условный оператор if и его альтернативная ветка else.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("if / else", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Если это произошло — выполни команду!",
        lede="Первый настоящий условный оператор: код, который выполняется только при "
        "определённых обстоятельствах.",
        body_html=body,
        sidebar_groups=sidebar("09-03-if-inache.html"),
        nav=PageNav(prev_href="09-02-sravnenie-i-reshenie.html", prev_label="Сравниваем и решаем", next_href="09-04-neskolko-uslovij.html", next_label="Больше одного условия!"),
    )
    write("09-03-if-inache.html", out)


def build_04() -> None:
    body = f"""
    <p>Иногда решение зависит не от одного, а сразу от нескольких условий. Для этого есть три
    логических оператора: <code class="inline">and</code> (и), <code class="inline">or</code>
    (или), <code class="inline">not</code> (не).</p>

    {code_block(
        "logicheskie_operatory.py",
        "age = 20\n"
        "has_ticket = True\n\n"
        "if age >= 18 and has_ticket:\n"
        '    print("Проходите в зал.")\n\n'
        "is_weekend = False\n"
        "is_holiday = True\n"
        "if is_weekend or is_holiday:\n"
        '    print("Сегодня можно не ходить на работу.")\n\n'
        "if not has_ticket:\n"
        '    print("Сначала нужно купить билет.")\n',
    )}

    <table style="width:100%;border-collapse:collapse;margin:24px 0;font-size:15px">
      <tr style="border-bottom:1px solid var(--color-border-default)"><th style="text-align:left;padding:8px">Оператор</th><th style="text-align:left;padding:8px">Истина, когда</th></tr>
      <tr style="border-bottom:1px solid var(--color-border-default)"><td style="padding:8px"><code class="inline">and</code></td><td style="padding:8px">оба условия истинны</td></tr>
      <tr style="border-bottom:1px solid var(--color-border-default)"><td style="padding:8px"><code class="inline">or</code></td><td style="padding:8px">хотя бы одно условие истинно</td></tr>
      <tr><td style="padding:8px"><code class="inline">not</code></td><td style="padding:8px">переворачивает значение на противоположное</td></tr>
    </table>

    {callout(
        "tip",
        "Скобки помогают читать сложные условия",
        "Когда условий много, скобки делают приоритет явным: <code class=\"inline\">(age >= 18 "
        "and has_ticket) or is_vip</code> читается однозначно, в отличие от варианта без "
        "скобок.",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "09-04-and-or-not.ipynb · комбинируем условия",
        "../../../notebooks/chapter-09/09-04-and-or-not.ipynb",
    )}
    """
    out = render_page(
        page_title="Больше одного условия!",
        description="Логические операторы and, or, not для комбинирования условий.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("Больше одного условия", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Больше одного условия! :O",
        lede="and, or и not объединяют несколько условий в одно.",
        body_html=body,
        sidebar_groups=sidebar("09-04-neskolko-uslovij.html"),
        nav=PageNav(prev_href="09-03-if-inache.html", prev_label="if / else", next_href="09-05-mini-proekt-ugadaj-chislo.html", next_label="Мини-проект: «Угадай число»"),
    )
    write("09-04-neskolko-uslovij.html", out)


def build_05() -> None:
    body = f"""
    <p>Первая настоящая игра в этой книге! Компьютер загадывает число, вы вводите один вариант
    — и программа говорит, угадали вы или нет (полноценный повтор попыток в цикле — уже в главе
    10, здесь одна попытка).</p>
    {code_block(
        "ugadaj_chislo.py",
        "import random\n\n"
        "zagadannoe = random.randint(1, 20)\n"
        'popytka = int(input("Угадайте число от 1 до 20: "))\n\n'
        "if popytka == zagadannoe:\n"
        '    print("Поздравляем, вы угадали!")\n'
        "elif popytka < zagadannoe:\n"
        '    print(f"Мимо! Загаданное число больше, чем {popytka}.")\n'
        "else:\n"
        '    print(f"Мимо! Загаданное число меньше, чем {popytka}.")\n\n'
        'print(f"Загаданное число было: {zagadannoe}")\n',
    )}
    {callout(
        "info",
        "elif — «а иначе, если»",
        "<code class=\"inline\">elif</code> (сокращение от <em>else if</em>) добавляет "
        "дополнительное условие между <code class=\"inline\">if</code> и "
        "<code class=\"inline\">else</code>. Подробнее — в следующем разделе.",
    )}

    {exercise(2, "Подсказка «горячо/холодно»", "Добавьте третье условие: если разница между попыткой и загаданным числом меньше 3 — выведите «Очень близко!» перед основным сообщением.")}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "09-05-ugadaj-chislo.ipynb · собираем игру целиком",
        "../../../notebooks/chapter-09/09-05-ugadaj-chislo.ipynb",
    )}
    """
    out = render_page(
        page_title="Мини-проект — игра «Угадай число»",
        description="Первая мини-игра книги: угадать случайное число, используя if/elif/else.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("Угадай число", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Мини-проект — игра «Угадай число»",
        lede="Первая настоящая игра книги — компьютер загадывает число, вы пытаетесь угадать.",
        body_html=body,
        sidebar_groups=sidebar("09-05-mini-proekt-ugadaj-chislo.html"),
        nav=PageNav(prev_href="09-04-neskolko-uslovij.html", prev_label="Больше одного условия", next_href="09-06-nakoplenie-uslovij-itogi.html", next_label="Условия накапливаются и итоги"),
    )
    write("09-05-mini-proekt-ugadaj-chislo.html", out)


def build_06() -> None:
    body = f"""
    <p>Условий может быть сколько угодно — <code class="inline">elif</code> позволяет
    проверить их по очереди, одно за другим, пока одно из них не окажется истинным:</p>
    {code_block(
        "elif_cepochka.py",
        "ocenka = 87\n\n"
        "if ocenka >= 90:\n"
        '    bukva = "A"\n'
        "elif ocenka >= 80:\n"
        '    bukva = "B"\n'
        "elif ocenka >= 70:\n"
        '    bukva = "C"\n'
        "else:\n"
        '    bukva = "D"\n\n'
        'print(f"Оценка: {bukva}")\n',
    )}

    {callout(
        "tip",
        "Порядок условий имеет значение",
        "Python проверяет условия <strong>по порядку</strong> и останавливается на первом "
        "истинном — даже если следующие условия тоже подошли бы. Поэтому в примере выше условия "
        "идут от большего к меньшему: если бы <code class=\"inline\">ocenka >= 70</code> "
        "стояло первым, оценка 87 неверно попала бы в категорию «C».",
    )}

    <h2>Вложенные условия</h2>
    <p>Внутри блока <code class="inline">if</code> может быть ещё один
    <code class="inline">if</code> — это называется <strong>вложенным условием</strong>:</p>
    {code_block(
        "vlozhennye_usloviya.py",
        "age = 25\n"
        "has_license = True\n\n"
        "if age >= 18:\n"
        "    if has_license:\n"
        '        print("Можно водить машину.")\n'
        "    else:\n"
        '        print("Сначала получите права.")\n'
        "else:\n"
        '    print("Ещё рано водить машину.")\n',
    )}

    {exercise(3, "Три вложенных уровня", "Добавьте третий уровень: внутри «можно водить машину» проверьте ещё и наличие топлива в баке (третья переменная has_fuel).")}

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
        "Тип <code class=\"inline\">bool</code> хранит <code class=\"inline\">True</code> или "
        "<code class=\"inline\">False</code>; ноль и пустые значения — «ложь», всё остальное — "
        "«истина».",
        "Шесть операторов сравнения (<code class=\"inline\">== != &lt; &gt; &lt;= &gt;=</code>) "
        "превращают значения в bool.",
        "<code class=\"inline\">if</code> выполняет блок кода при истинном условии; "
        "<code class=\"inline\">else</code> — альтернативу, если условие ложно.",
        "<code class=\"inline\">and</code>, <code class=\"inline\">or</code>, "
        "<code class=\"inline\">not</code> комбинируют несколько условий в одно.",
        "<code class=\"inline\">elif</code> проверяет условия по очереди; условия можно "
        "вкладывать друг в друга.",
    ])}
    """
    out = render_page(
        page_title="Условия продолжают накапливаться!",
        description="Цепочки elif и вложенные условия — и краткие итоги главы 9.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 9", "index.html"), ("elif и итоги", "")],
        kicker="Глава 9 · Выполняй мою команду!",
        h1="Условия продолжают накапливаться!",
        lede="elif и вложенные условия — когда одного if/else уже недостаточно.",
        body_html=body,
        sidebar_groups=sidebar("09-06-nakoplenie-uslovij-itogi.html"),
        nav=PageNav(prev_href="09-05-mini-proekt-ugadaj-chislo.html", prev_label="Угадай число", next_href="../glava-10/index.html", next_label="Глава 10: Немного автоматизации!"),
    )
    write("09-06-nakoplenie-uslovij-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01()
    build_02()
    build_03()
    build_04()
    build_05()
    build_06()
