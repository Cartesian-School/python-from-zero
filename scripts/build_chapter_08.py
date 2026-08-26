#!/usr/bin/env python3
"""Строит Главу 8: «Играем с буквами и словами» (site/chapters/glava-08/)."""

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
    flow_diagram,
    practice_card,
    render_chapter_opener,
    render_page,
    string_index_diagram,
    string_slice_diagram,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-08"

PAGES = [
    ("index.html", "Обзор главы"),
    ("08-01-chto-takoe-stroki.html", "Что такое строки?"),
    ("08-11-ekranirovanie.html", "Экранирование: \\n, \\t и другие"),
    ("08-12-mnogostrochnye-i-raw-stroki.html", "Многострочные и raw-строки"),
    ("08-02-kavychki-konkatenaciya.html", "Кавычки, склеивание, повторение"),
    ("08-13-dlina-stroki.html", "Длина строки: len()"),
    ("08-03-dostup-k-simvolam.html", "Индексы строки"),
    ("08-14-srezy-stroki.html", "Срезы строки"),
    ("08-15-neizmenyaemost.html", "Строки нельзя изменить"),
    ("08-04-metody-strok.html", "Методы строк: регистр и пробелы"),
    ("08-16-metody-strok-poisk-i-razbor.html", "Методы строк: поиск и разбор"),
    ("08-17-metody-proverki.html", "Методы проверки: isalpha и другие"),
    ("08-05-istina-lozh.html", "in, сравнение и истинность"),
    ("08-18-cikl-po-stroke.html", "Перебираем строку в цикле"),
    ("08-06-formatirovanie-strok.html", "Форматирование строк"),
    ("08-07-vvod-polzovatelya.html", "Ввод от пользователя"),
    ("08-19-unikod-i-emodzi.html", "Кириллица, юникод и эмодзи"),
    ("08-20-otladka-strok.html", "Отладка проблем со строками"),
    ("08-08-mini-proekt-turtle-tekst.html", "Мини-проект: текст Turtle"),
    ("08-21-mini-proekt-privetstvie-i-imya.html", "Мини-проект: приветствие и ФИО"),
    ("08-09-mini-proekty-krik-perevorot.html", "Мини-проекты: крик и переворот"),
    ("08-22-mini-proekt-parol-i-email.html", "Мини-проект: пароль и e-mail"),
    ("08-23-mini-proekt-schetchik-slov.html", "Мини-проект: счётчик слов"),
    ("08-10-mini-proekt-matematika-itogi.html", "Мини-проект: динамическая математика и итоги"),
]

PRACTICE_IDS = [
    "08-01", "08-11", "08-12", "08-13", "08-14", "08-04", "08-16", "08-17",
    "08-03", "08-18", "08-06", "08-07", "08-20", "08-21", "08-09", "08-22",
    "08-23", "08-10",
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 8 · Строки", items),
        SidebarGroup("Практика", [
            NavItem(f"[[icon:practice]] {lid}: Практика", f"../../practice/{lid}/index.html") for lid in PRACTICE_IDS
        ]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    clean = "\n".join(line.rstrip() for line in html_out.split("\n"))
    path.write_text(clean, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=8,
        description="Строки в Python на полную глубину: создание и кавычки, экранирование, "
        "многострочные и raw-строки, индексы и срезы с наглядными диаграммами, неизменяемость, "
        "десятки методов, форматирование f-строками, ввод от пользователя, юникод, отладка — и "
        "восемь мини-проектов.",
        meta_items=["[[icon:timer]] ~6–7 часов", "[[icon:code]] str и его методы", "[[icon:practice]] 18 практик", "[[icon:palette]] диаграммы для индексов и срезов"],
        sections=[
            ChapterSectionLink("8.1", "Что такое строки?", "08-01-chto-takoe-stroki.html"),
            ChapterSectionLink("8.2", "Экранирование: \\n, \\t и другие", "08-11-ekranirovanie.html"),
            ChapterSectionLink("8.3", "Многострочные и raw-строки", "08-12-mnogostrochnye-i-raw-stroki.html"),
            ChapterSectionLink("8.4", "Кавычки, склеивание, повторение", "08-02-kavychki-konkatenaciya.html"),
            ChapterSectionLink("8.5", "Длина строки: len()", "08-13-dlina-stroki.html"),
            ChapterSectionLink("8.6", "Индексы строки", "08-03-dostup-k-simvolam.html"),
            ChapterSectionLink("8.7", "Срезы строки", "08-14-srezy-stroki.html"),
            ChapterSectionLink("8.8", "Строки нельзя изменить", "08-15-neizmenyaemost.html"),
            ChapterSectionLink("8.9", "Методы строк: регистр и пробелы", "08-04-metody-strok.html"),
            ChapterSectionLink("8.10", "Методы строк: поиск и разбор", "08-16-metody-strok-poisk-i-razbor.html"),
            ChapterSectionLink("8.11", "Методы проверки: isalpha и другие", "08-17-metody-proverki.html"),
            ChapterSectionLink("8.12", "in, сравнение и истинность", "08-05-istina-lozh.html"),
            ChapterSectionLink("8.13", "Перебираем строку в цикле", "08-18-cikl-po-stroke.html"),
            ChapterSectionLink("8.14", "Форматирование строк", "08-06-formatirovanie-strok.html"),
            ChapterSectionLink("8.15", "Ввод от пользователя", "08-07-vvod-polzovatelya.html"),
            ChapterSectionLink("8.16", "Кириллица, юникод и эмодзи", "08-19-unikod-i-emodzi.html"),
            ChapterSectionLink("8.17", "Отладка проблем со строками", "08-20-otladka-strok.html"),
            ChapterSectionLink("8.18", "Мини-проект — текст Turtle", "08-08-mini-proekt-turtle-tekst.html"),
            ChapterSectionLink("8.19", "Мини-проект — приветствие и ФИО", "08-21-mini-proekt-privetstvie-i-imya.html"),
            ChapterSectionLink("8.20", "Мини-проекты — крик и переворот", "08-09-mini-proekty-krik-perevorot.html"),
            ChapterSectionLink("8.21", "Мини-проект — пароль и e-mail", "08-22-mini-proekt-parol-i-email.html"),
            ChapterSectionLink("8.22", "Мини-проект — счётчик слов", "08-23-mini-proekt-schetchik-slov.html"),
            ChapterSectionLink("8.23", "Мини-проект — динамическая математика", "08-10-mini-proekt-matematika-itogi.html"),
            ChapterSectionLink("", "Итоги", "08-10-mini-proekt-matematika-itogi.html#itogi"),
        ],
    )
    write("index.html", out)


# ---------------------------------------------------------------------------
# 8.1 — Что такое строки?
# ---------------------------------------------------------------------------

def build_01() -> None:
    body = f"""
    <h2>Текст — тоже данные</h2>
    <p>Почти любая программа работает с текстом: имя пользователя, сообщение в чате, название
    файла, адрес сайта, команда терминала. В Python текст хранится в специальном типе данных —
    <strong>строке</strong> (<code class="inline">str</code>). Строка — это
    <strong>последовательность символов</strong>: букв, цифр, знаков препинания, пробелов,
    эмодзи — идущих друг за другом по порядку, как бусины на нитке.</p>

    {code_block("primery_strok.py", 'imya = "Ада"\nsoobshchenie = "Привет, как дела?"\nfaijl = "otchet_2026.pdf"\nadres = "https://cartesianschool.org"\nkomanda = "git commit -m fix"\n')}

    <p>Всё, что вы вводите с клавиатуры через <code class="inline">input()</code> (раздел 8.15),
    тоже приходит в виде строки — даже если это выглядит как число.</p>

    <h2>Создаём строку</h2>
    <p>Строку заключают в кавычки — одинарные <code class="inline">'...'</code> или двойные
    <code class="inline">"..."</code>. В Python они полностью равнозначны: выбирайте любые,
    главное — не смешивать тип кавычек внутри одной пары.</p>
    {code_block("sozdaem_stroki.py", 'greeting = "Привет"\nname = \'Cartesian\'\nprint(greeting, name)\n# Привет Cartesian\n')}

    {callout(
        "tip",
        "Когда какие кавычки удобнее",
        "Разницы для Python нет, но людям иногда удобнее один тип: если в тексте будет "
        "апостроф — <code class=\"inline\">it's</code> — проще обернуть его двойными "
        "кавычками; если внутри будет прямая речь в кавычках — проще обернуть одинарными. "
        "Подробно об этом — в разделе 8.4.",
    )}

    <h2>Пустая строка</h2>
    <p>Строка может не содержать ни одного символа — это тоже полноценная строка, просто
    <strong>пустая</strong>: <code class="inline">""</code> или <code class="inline">''</code>.
    Она часто служит стартовым значением, к которому потом что-то добавляют.</p>
    {code_block("pustaya_stroka.py", 'pusto = ""\nprint(pusto)          # (ничего не выведется — строка пуста)\nprint(len(pusto))     # 0\n')}

    <h2>type() — как узнать, что перед вами строка</h2>
    {code_block("proverka_tipa.py", 'print(type("Python"))   # <class \'str\'>\nprint(type(5))          # <class \'int\'>\nprint(type("5"))        # <class \'str\'> — цифра в кавычках всё равно строка!\n')}

    {callout(
        "warning",
        "\"5\" — это не число",
        "Строка <code class=\"inline\">\"5\"</code> состоит из символа «пятёрка», а не хранит "
        "числовое значение 5. С ней нельзя напрямую выполнять арифметику — подробнее в "
        "разделе 8.15, когда мы будем разбирать <code class=\"inline\">input()</code>.",
    )}

    {practice_card(
        "08-01",
        "Практика: создание строк и type()",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-01/index.html",
    )}
    """
    out = render_page(
        page_title="Что такое строки?",
        description="Введение в строки Python: текст как данные, создание строк, пустая строка и type().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Что такое строки?", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Что такое строки?",
        lede="Текст в Python — это строки: последовательность символов, с которой можно "
        "работать так же уверенно, как с числами.",
        body_html=body,
        sidebar_groups=sidebar("08-01-chto-takoe-stroki.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="08-11-ekranirovanie.html", next_label="Экранирование"),
    )
    write("08-01-chto-takoe-stroki.html", out)


# ---------------------------------------------------------------------------
# 8.2 — Экранирование
# ---------------------------------------------------------------------------

def build_11() -> None:
    body = f"""
    <h2>Символы, которые нельзя напечатать прямо</h2>
    <p>Иногда внутри строки нужен символ, у которого нет своей клавиши — например, «конец
    строки» (перенос) или «табуляция». Для них в Python есть <strong>служебные
    последовательности</strong> (escape-последовательности) — обратная косая черта
    <code class="inline">\\</code> плюс буква:</p>

    <div class="compare-table-wrap" style="overflow-x:auto">
    <table class="compare-table">
      <thead><tr><th>Пишем</th><th>Означает</th></tr></thead>
      <tbody>
        <tr><td><code class="inline">\\n</code></td><td>перенос строки (new line)</td></tr>
        <tr><td><code class="inline">\\t</code></td><td>табуляция (отступ)</td></tr>
        <tr><td><code class="inline">\\\\</code></td><td>сама обратная косая черта</td></tr>
        <tr><td><code class="inline">\\"</code></td><td>двойная кавычка внутри строки в двойных кавычках</td></tr>
        <tr><td><code class="inline">\\'</code></td><td>одинарная кавычка внутри строки в одинарных кавычках</td></tr>
      </tbody>
    </table>
    </div>

    <h2>Исходный текст vs напечатанный результат</h2>
    <p>Ключевая идея: то, что вы <strong>пишете</strong> в коде (с обратными чертами), и то,
    что реально <strong>печатается</strong> на экране (уже без них), — два разных текста:</p>
    {code_block("escape_primer.py", 'print("Первая строка\\nВторая строка")\n# Первая строка\n# Вторая строка\n\nprint("Имя:\\tВозраст:")\nprint("Ада:\\t28")\n# Имя:    Возраст:\n# Ада:    28\n')}

    <p>Символ <code class="inline">\\n</code> в исходном коде — это ДВА символа (косая черта и
    «n»), но Python понимает их как ОДИН специальный символ «перенос строки», который при
    печати превращается в настоящий перенос — на экране обратной черты уже не видно.</p>

    {callout(
        "info",
        "Зачем вообще экранировать",
        "Обратная косая черта — служебный символ Python внутри строк. Экранирование "
        "объясняет Python: «дальше идёт не команда, а именно этот символ». Без этого "
        "механизма было бы невозможно вставить в строку кавычку того же типа, что "
        "обрамляет саму строку, или напечатать перенос строки одной командой "
        "<code class=\"inline\">print()</code>.",
    )}

    <h2>repr() — увидеть служебные символы «как есть»</h2>
    <p><code class="inline">repr()</code> печатает строку так, как она выглядит в коде — со
    всеми обратными чертами, а не с их результатом. Это отличный инструмент отладки, к
    которому мы ещё вернёмся в разделе 8.17:</p>
    {code_block("repr_vs_print.py", 'text = "Строка 1\\nСтрока 2"\nprint(text)          # печатает ДВЕ настоящие строки\nprint(repr(text))    # \'Строка 1\\nСтрока 2\' — видно \\n как текст\n')}

    {exercise(1, "Табличка из трёх строк", "Одной командой print() с \\n выведите три строки: «Имя: Ада», «Профессия: программист», «Год: 1843».")}

    {practice_card(
        "08-11",
        "Практика: экранирование и repr()",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-11/index.html",
    )}
    """
    out = render_page(
        page_title="Экранирование: \\n, \\t и другие",
        description="Служебные последовательности \\n, \\t, \\\\, \\\" и \\' — разница между исходным текстом и напечатанным результатом.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Экранирование", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Экранирование: \\n, \\t и другие",
        lede="Как вставить в строку символ, у которого нет своей клавиши — и почему написанное "
        "в коде не всегда совпадает с напечатанным на экране.",
        body_html=body,
        sidebar_groups=sidebar("08-11-ekranirovanie.html"),
        nav=PageNav(prev_href="08-01-chto-takoe-stroki.html", prev_label="Что такое строки?", next_href="08-12-mnogostrochnye-i-raw-stroki.html", next_label="Многострочные и raw-строки"),
    )
    write("08-11-ekranirovanie.html", out)


# ---------------------------------------------------------------------------
# 8.3 — Многострочные и raw-строки
# ---------------------------------------------------------------------------

def build_12() -> None:
    body = f"""
    <h2>Многострочные строки: тройные кавычки</h2>
    <p>Вместо того чтобы вставлять <code class="inline">\\n</code> вручную, можно написать текст
    сразу в несколько строк — если обернуть его <strong>тройными кавычками</strong>
    <code class="inline">\"""</code> или <code class="inline">'''</code>. Все переносы строк
    внутри сохраняются такими, какие они есть:</p>
    {code_block("mnogostrochnaya.py", 'poem = """Код за кодом,\nшаг за шагом —\nтак рождается\nпрограмма."""\nprint(poem)\n# Код за кодом,\n# шаг за шагом —\n# так рождается\n# программа.\n')}

    {callout(
        "warning",
        "Осторожно с отступами",
        "Если код внутри функции или блока имеет отступ, а тройная строка написана с тем же "
        "отступом, эти пробелы попадут ВНУТРЬ текста — Python не убирает их автоматически. "
        "Для простых учебных программ, где тройная строка начинается с начала строки кода, "
        "это не проблема; в реальных проектах для этого существуют специальные приёмы "
        "(например, модуль <code class=\"inline\">textwrap</code>), которые нам пока не нужны.",
    )}

    <h2>Raw-строки: r"..."</h2>
    <p>Иногда обратных чёрточек в тексте должно быть МНОГО, и экранировать каждую — утомительно
    и трудно читать. Классический пример — путь к файлу в Windows:</p>
    {code_block("bez_raw.py", 'path = "C:\\\\Users\\\\Cartesian\\\\Documents"\nprint(path)\n# C:\\Users\\Cartesian\\Documents\n')}
    <p>Каждую обратную черту пришлось задваивать. Если поставить перед открывающей кавычкой
    букву <code class="inline">r</code> (от <em>raw</em> — «сырой»), Python перестаёт понимать
    <code class="inline">\\</code> как начало служебной последовательности и берёт текст ровно
    таким, каким он написан:</p>
    {code_block("s_raw.py", 'path = r"C:\\Users\\Cartesian\\Documents"\nprint(path)\n# C:\\Users\\Cartesian\\Documents — тот же результат, но без задвоенных чёрточек\n')}

    {callout(
        "tip",
        "Raw-строки убирают «шум» экранирования",
        "Raw-строки часто используют для путей к файлам и для шаблонов регулярных выражений "
        "(тема для будущих глав) — там обратных чёрточек особенно много, и без "
        "<code class=\"inline\">r\"...\"</code> код было бы тяжело читать.",
    )}

    {exercise(1, "Свой путь", "Выведите путь r\"D:\\Projects\\python-from-zero\\notebooks\" через raw-строку и через обычную строку с экранированием — убедитесь, что print() печатает одно и то же.")}

    {practice_card(
        "08-12",
        "Практика: тройные и raw-строки",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-12/index.html",
    )}
    """
    out = render_page(
        page_title="Многострочные и raw-строки",
        description="Тройные кавычки для многострочного текста и raw-строки r\"...\" для текста с большим числом обратных чёрточек.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Многострочные и raw", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Многострочные и raw-строки",
        lede="Два особых способа создать строку: тройные кавычки — для текста в несколько "
        "строк, буква r — для текста без экранирования.",
        body_html=body,
        sidebar_groups=sidebar("08-12-mnogostrochnye-i-raw-stroki.html"),
        nav=PageNav(prev_href="08-11-ekranirovanie.html", prev_label="Экранирование", next_href="08-02-kavychki-konkatenaciya.html", next_label="Кавычки, склеивание, повторение"),
    )
    write("08-12-mnogostrochnye-i-raw-stroki.html", out)


# ---------------------------------------------------------------------------
# 8.4 — Кавычки, конкатенация, повторение (существующий, расширяем)
# ---------------------------------------------------------------------------

def build_02() -> None:
    body = f"""
    <h2>В моей строке есть кавычки! :O</h2>
    <p>Что делать, если внутри текста нужна кавычка того же типа, что обрамляет строку? Самый
    простой способ — обрамить строку кавычками <strong>другого</strong> типа:</p>
    {code_block("kavychki.py", "quote = \"Она сказала: 'Привет!'\"\nquote2 = 'Она сказала: \"Привет!\"'\nprint(quote)\nprint(quote2)\n# Она сказала: 'Привет!'\n# Она сказала: \"Привет!\"\n")}
    <p>Если нужны именно такие же кавычки, как обрамляющие, — их экранируют (раздел 8.2)
    обратной косой чертой <code class="inline">\\</code>:</p>
    {code_block("ekranirovanie_kavychek.py", 'quote = "Она сказала: \\"Привет!\\""\nprint(quote)\n# Она сказала: "Привет!"\n')}

    <h2>Объединяем строки: +</h2>
    <p>Строки, как и числа, можно складывать оператором <code class="inline">+</code> —
    это называется <strong>конкатенацией</strong> («склеиванием»):</p>
    {code_block("konkatenaciya.py", 'first_name = "Ада"\nlast_name = "Лавлейс"\nfull_name = first_name + " " + last_name\nprint(full_name)\n# Ада Лавлейс\n')}

    {callout(
        "warning",
        "Строку с числом напрямую не сложить",
        "<code class=\"inline\">\"Возраст: \" + 10</code> вызовет <code class=\"inline\">TypeError"
        "</code> — Python не знает, что вы имели в виду: приклеить цифру «10» как текст или "
        "сложить числа. Нужно явно сказать: либо <code class=\"inline\">str(10)</code>, либо "
        "f-строка (раздел 8.14).",
    )}
    {code_block("tipeerror_i_ispravlenie.py", '# print("Возраст: " + 10)     # TypeError!\nprint("Возраст: " + str(10))  # Возраст: 10 — исправлено\n')}

    <h2>Повторяем строку: *</h2>
    <p>Строку можно умножить на целое число — она повторится столько раз:</p>
    {code_block("povtorenie.py", 'stroka = "Ha" * 3\nprint(stroka)     # HaHaHa\n\nrazdelitel = "-" * 20\nprint(razdelitel) # --------------------\n')}

    <h2>Конкатенация в print()</h2>
    <p>Напомним: у <code class="inline">print()</code> есть более простой способ вывести
    несколько значений — через запятую, без явного <code class="inline">+</code>:</p>
    {code_block("print_konkatenaciya.py", 'print(first_name, last_name)          # Ада Лавлейс — сам добавит пробел\nprint(first_name + " " + last_name)   # Ада Лавлейс — пробел нужно добавлять самому\n')}

    {exercise(1, "Рамка из повторения", "Соберите строкой из символа «=», умноженного на 30, верхнюю и нижнюю рамку для заголовка «ГЛАВА 8», и выведите три строки: рамка, заголовок, рамка.")}

    {practice_card(
        "08-01",
        "Практика: кавычки, конкатенация и повторение",
        "Тот же ноутбук, что и в разделе «Что такое строки?» — он охватывает и эту тему",
        "../../practice/08-01/index.html",
    )}
    """
    out = render_page(
        page_title="Кавычки, склеивание, повторение",
        description="Экранирование кавычек, конкатенация строк оператором + и повторение строк оператором *.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Кавычки и объединение", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="В моей строке есть кавычки! :O",
        lede="Кавычки внутри строки, склеивание строк оператором + и их повторение оператором *.",
        body_html=body,
        sidebar_groups=sidebar("08-02-kavychki-konkatenaciya.html"),
        nav=PageNav(prev_href="08-12-mnogostrochnye-i-raw-stroki.html", prev_label="Многострочные и raw-строки", next_href="08-13-dlina-stroki.html", next_label="Длина строки"),
    )
    write("08-02-kavychki-konkatenaciya.html", out)


# ---------------------------------------------------------------------------
# 8.5 — len()
# ---------------------------------------------------------------------------

def build_13() -> None:
    body = f"""
    <h2>Сколько символов в строке?</h2>
    <p>Функция <code class="inline">len()</code> («length» — длина) считает, сколько символов
    в строке — и пробелы считаются наравне с буквами:</p>
    {code_block("dlina.py", 'word = "Python"\nprint(len(word))         # 6\n\nphrase = "Python с нуля"\nprint(len(phrase))       # 13 — пробелы тоже считаются!\n')}

    {callout(
        "tip",
        "Посчитайте пробелы сами",
        "«Python с нуля» — это П-y-t-h-o-n (6) + пробел (1) + с (1) + пробел (1) + н-у-л-я (4) "
        "= 13 символов. Легко случайно забыть посчитать пробелы «на глаз» — len() никогда не "
        "ошибается.",
    )}

    <h2>Зачем нужна длина строки</h2>
    <p><code class="inline">len()</code> пригодится уже в следующем разделе: чтобы понимать,
    какие индексы вообще существуют у строки. У строки длиной <code class="inline">n</code>
    символов индексы идут от <code class="inline">0</code> до
    <code class="inline">n - 1</code> — это и есть главная причина знать длину строки заранее.</p>
    {code_block("dlina_i_indeks.py", 'word = "Python"\nprint(len(word))     # 6\nprint(word[len(word) - 1])   # n — последний символ, индекс "длина минус один"\n')}

    {exercise(1, "Самое длинное слово", "Даны три строки: \"Python\", \"программирование\", \"код\". Выведите длину каждой и определите (по выведенным числам), какая строка самая длинная.")}

    {practice_card(
        "08-13",
        "Практика: len() и границы строки",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-13/index.html",
    )}
    """
    out = render_page(
        page_title="Длина строки: len()",
        description="Функция len() для подсчёта символов строки — и почему это важно для индексов.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Длина строки", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Длина строки: len()",
        lede="Считаем символы строки — включая пробелы — и готовимся к индексам.",
        body_html=body,
        sidebar_groups=sidebar("08-13-dlina-stroki.html"),
        nav=PageNav(prev_href="08-02-kavychki-konkatenaciya.html", prev_label="Кавычки, склеивание, повторение", next_href="08-03-dostup-k-simvolam.html", next_label="Индексы строки"),
    )
    write("08-13-dlina-stroki.html", out)


# ---------------------------------------------------------------------------
# 8.6 — Индексы (КРИТИЧЕСКИ ВАЖНО)
# ---------------------------------------------------------------------------

def build_03() -> None:
    idx_python = string_index_diagram("Python", caption="«Python»: сверху — индекс с начала (0, 1, 2, …), снизу — индекс с конца (-6, -5, …, -1)")
    idx_mandala = string_index_diagram("мандала", caption="Тот же принцип работает и для кириллицы — «мандала», 7 символов, индексы 0…6 и -7…-1")

    body = f"""
    <h2>Индекс — это номер места</h2>
    <p>Строка — это последовательность символов, и у каждого символа есть свой
    <strong>порядковый номер</strong> — <strong>индекс</strong>. Индекс пишут в квадратных
    скобках сразу после строки: <code class="inline">строка[индекс]</code>.</p>

    {callout(
        "warning",
        "Счёт начинается с нуля!",
        "Это самая важная деталь этого раздела. Первый символ строки имеет индекс "
        "<strong>0</strong>, а не 1. Второй символ — индекс 1. И так далее. Такой способ счёта "
        "называется <strong>индексацией с нуля</strong> (zero-based indexing) — его используют "
        "почти все языки программирования, и к нему быстро привыкаешь.",
    )}

    {idx_python}

    {code_block("indeksy.py", 'word = "Python"\nprint(word[0])   # P — первый символ (индекс 0)\nprint(word[1])   # y — второй символ (индекс 1)\nprint(word[5])   # n — шестой символ (индекс 5 — последний, т.к. всего 6 символов)\n')}

    <h2>Отрицательные индексы: считаем с конца</h2>
    <p>Индекс <code class="inline">-1</code> означает «последний символ», <code class="inline">-2</code>
    — «предпоследний», и так далее. Это тот же самый ряд символов, просто прочитанный с другого
    конца — обратите внимание на нижний ряд чисел на диаграмме выше.</p>
    {code_block("otricatelnye_indeksy.py", 'word = "Python"\nprint(word[-1])   # n — последний символ\nprint(word[-2])   # o — предпоследний\nprint(word[-6])   # P — тот же символ, что и word[0]!\n')}

    {idx_mandala}

    {callout(
        "warning",
        "IndexError — индекс за пределами строки",
        "<code class=\"inline\">word[10]</code> для шестибуквенного слова вызовет "
        "<code class=\"inline\">IndexError: string index out of range</code>. Индексы "
        "существуют только от <code class=\"inline\">0</code> до "
        "<code class=\"inline\">len(word) - 1</code> (раздел 8.5), и от "
        "<code class=\"inline\">-1</code> до <code class=\"inline\">-len(word)</code> с конца.",
    )}
    {code_block("indexerror.py", 'word = "Python"\n# word[10]   # IndexError: string index out of range\nprint(len(word))          # 6 — значит, максимальный индекс 5\n')}

    {exercise(1, "Первая и последняя буква", "Для слова «Cartesian» выведите его первую букву через индекс 0 и последнюю — двумя способами: через положительный индекс (с len()) и через отрицательный индекс -1. Все три способа должны дать одинаковый результат для последней буквы.")}

    {practice_card(
        "08-03",
        "Практика: индексы и отрицательные индексы",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-03/index.html",
    )}
    """
    out = render_page(
        page_title="Индексы строки",
        description="Индексация строк с нуля, отрицательные индексы и диаграммы символ-в-коробке для наглядного понимания.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Индексы строки", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Индексы строки",
        lede="Каждый символ строки можно достать по номеру — с начала или с конца. Разберём это "
        "по-настоящему наглядно.",
        body_html=body,
        sidebar_groups=sidebar("08-03-dostup-k-simvolam.html"),
        nav=PageNav(prev_href="08-13-dlina-stroki.html", prev_label="Длина строки", next_href="08-14-srezy-stroki.html", next_label="Срезы строки"),
    )
    write("08-03-dostup-k-simvolam.html", out)


# ---------------------------------------------------------------------------
# 8.7 — Срезы (КРИТИЧЕСКИ ВАЖНО)
# ---------------------------------------------------------------------------

def build_14() -> None:
    word = "Cartesian"
    slice_first3 = string_slice_diagram(word, 0, 3, caption='word[0:3] — от границы 0 до границы 3 (не включая её)')
    slice_last3 = string_slice_diagram(word, 6, 9, caption='word[6:9] — от границы 6 до конца строки (границы 9)')
    slice_middle = string_slice_diagram(word, 3, 6, caption='word[3:6] — «средний» кусок, от границы 3 до границы 6')

    body = f"""
    <h2>Срез — это кусок строки</h2>
    <p><strong>Срез</strong> (slice) достаёт из строки сразу несколько символов подряд:
    <code class="inline">строка[start:stop]</code>. Здесь <code class="inline">start</code> —
    индекс, с которого срез <strong>начинается</strong> (включительно), а
    <code class="inline">stop</code> — индекс, на котором срез <strong>заканчивается</strong>
    (НЕ включительно).</p>

    {callout(
        "warning",
        "stop не включается — и это специально",
        "Правая граница среза не входит в результат. Звучит странно, но у этого есть удобное "
        "следствие: длина среза всегда равна <code class=\"inline\">stop - start</code>. "
        "Мысленно удобно представлять индексы не как номера БУКВ, а как номера ГРАНИЦ МЕЖДУ "
        "буквами — посмотрите на числа над коробками ниже: они стоят ровно в промежутках.",
    )}

    <h2>Первые три символа</h2>
    {code_block("srez_pervye_tri.py", 'word = "Cartesian"\nprint(word[0:3])   # Car\n')}
    {slice_first3}

    <h2>Последние три символа</h2>
    {code_block("srez_poslednie_tri.py", 'word = "Cartesian"\nprint(word[6:9])   # ian\n')}
    {slice_last3}

    <h2>Кусок из середины</h2>
    {code_block("srez_seredina.py", 'word = "Cartesian"\nprint(word[3:6])   # tes\n')}
    {slice_middle}

    <h2>Пропущенные границы</h2>
    <p>Если <code class="inline">start</code> пропустить — срез начинается с самого начала
    строки. Если пропустить <code class="inline">stop</code> — срез идёт до самого конца.
    Пропустить можно и обе границы сразу — тогда получится копия всей строки:</p>
    {code_block("propushchennye_granicy.py", 'word = "Cartesian"\nprint(word[:3])    # Car  — то же самое, что word[0:3]\nprint(word[6:])    # ian  — то же самое, что word[6:9]\nprint(word[:])     # Cartesian — копия строки целиком\n')}

    <h2>Шаг среза</h2>
    <p>У среза есть и третий, необязательный параметр — <strong>шаг</strong>:
    <code class="inline">строка[start:stop:step]</code>. Шаг 2 значит «берём каждый второй
    символ»:</p>
    {code_block("shag_sreza.py", 'word = "Cartesian"\nprint(word[::2])    # Craea — каждый второй символ, с начала до конца\n')}

    <h2>Разворот строки: [::-1]</h2>
    <p>Отрицательный шаг проходит строку в обратном направлении. Если пропустить и
    <code class="inline">start</code>, и <code class="inline">stop</code>, а шаг поставить
    <code class="inline">-1</code> — получится строка задом наперёд:</p>
    {code_block("razvorot_sreza.py", 'word = "Cartesian"\nprint(word[::-1])   # naisetraC\n')}

    {callout(
        "tip",
        "Самый короткий способ развернуть строку",
        "<code class=\"inline\">строка[::-1]</code> — классический приём Python. Третий "
        "параметр среза — «шаг»; шаг -1 проходит строку с конца в начало. Мы воспользуемся "
        "этим в мини-проекте 8.20.",
    )}

    {exercise(2, "Средние буквы через шаг", "Для слова «программирование» получите срезом каждую третью букву (шаг 3), а затем — само слово, развёрнутое задом наперёд.")}

    {practice_card(
        "08-14",
        "Практика: срезы строки",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-14/index.html",
    )}
    """
    out = render_page(
        page_title="Срезы строки",
        description="Срезы строк [start:stop:step]: границы включительно/не включительно, пропущенные границы, шаг и разворот строки.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Срезы строки", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Срезы строки",
        lede="Срез достаёт из строки сразу целый кусок — а не один символ. Разберём границы "
        "среза наглядно, по коробочкам.",
        body_html=body,
        sidebar_groups=sidebar("08-14-srezy-stroki.html"),
        nav=PageNav(prev_href="08-03-dostup-k-simvolam.html", prev_label="Индексы строки", next_href="08-15-neizmenyaemost.html", next_label="Строки нельзя изменить"),
    )
    write("08-14-srezy-stroki.html", out)


# ---------------------------------------------------------------------------
# 8.8 — Неизменяемость
# ---------------------------------------------------------------------------

def build_15() -> None:
    body = f"""
    <h2>Строку нельзя изменить «на месте»</h2>
    <p>Может показаться, что раз мы умеем доставать символ по индексу
    (<code class="inline">word[0]</code>), то можно и <strong>заменить</strong> его тем же
    способом. Это не так — строки в Python <strong>неизменяемы</strong> (immutable):</p>
    {code_block("popytka_izmenit.py", 'word = "Cat"\nword[0] = "B"\n# TypeError: \'str\' object does not support item assignment\n')}

    {callout(
        "warning",
        "Почему так странно?",
        "Это осознанное устройство языка, а не ограничение. Неизменяемые строки проще и "
        "безопаснее передавать между разными частями программы — можно быть уверенным, что "
        "никакая другая часть кода «незаметно» не поменяет ваш текст, пока вы с ним работаете. "
        "Мы ещё вернёмся к этой идее в главе про списки, которые, наоборот, изменяемы.",
    )}

    <h2>Правильный способ: создать новую строку</h2>
    <p>Вместо изменения «на месте» строим НОВУЮ строку — из кусочков старой — и сохраняем её в
    переменную (можно в ту же самую):</p>
    {code_block("pravilnyj_sposob.py", 'word = "Cat"\nword = "B" + word[1:]     # склеиваем "B" с "at" — получаем новую строку\nprint(word)                # Bat\n')}

    <p>Именно поэтому все методы строк — <code class="inline">upper()</code>,
    <code class="inline">replace()</code> и другие (разделы 8.9–8.10) — не меняют исходную
    строку, а <strong>возвращают новую</strong>. Если результат нужно сохранить, его нужно
    явно присвоить переменной:</p>
    {code_block("metody_ne_menyayut.py", 'text = "python"\ntext.upper()          # результат создан, но никуда не сохранён — и потерян!\nprint(text)            # python — исходная строка не изменилась\n\ntext = text.upper()   # а вот так — сохранили результат обратно в text\nprint(text)            # PYTHON\n')}

    {exercise(1, "Замена первой буквы", "Для строки «home» постройте новую строку «dome», заменив первый символ через срез и конкатенацию — так, как показано выше для «Cat» → «Bat».")}

    {practice_card(
        "08-14",
        "Практика: неизменяемость строк",
        "Тот же ноутбук, что и в разделе «Срезы строки» — он охватывает и эту тему",
        "../../practice/08-14/index.html",
    )}
    """
    out = render_page(
        page_title="Строки нельзя изменить",
        description="Неизменяемость строк в Python: почему word[0] = ... не работает и как правильно строить изменённую строку.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Неизменяемость", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Строки нельзя изменить",
        lede="Строку невозможно поменять «на месте» — но можно построить новую. Разберём, "
        "почему это так и как это влияет на все методы строк.",
        body_html=body,
        sidebar_groups=sidebar("08-15-neizmenyaemost.html"),
        nav=PageNav(prev_href="08-14-srezy-stroki.html", prev_label="Срезы строки", next_href="08-04-metody-strok.html", next_label="Методы строк: регистр и пробелы"),
    )
    write("08-15-neizmenyaemost.html", out)


# ---------------------------------------------------------------------------
# 8.9 — Методы строк: регистр и пробелы (существующий, расширяем)
# ---------------------------------------------------------------------------

def build_04() -> None:
    case_flow = flow_diagram(
        [
            ("Исходная строка", '"Python С Нуля"'),
            (".upper()", "все буквы —\nЗАГЛАВНЫЕ"),
            ("Результат", '"PYTHON С НУЛЯ"'),
        ],
        caption="upper() возвращает НОВУЮ строку (раздел 8.8) — исходная переменная не меняется",
    )
    strip_flow = flow_diagram(
        [
            ("Исходная строка", '"  Python  "'),
            (".strip()", "пробелы\nпо краям — прочь"),
            ("Результат", '"Python"'),
        ],
        caption="strip() убирает пробелы только по краям — не внутри строки",
    )

    body = f"""
    <p>У каждой строки в Python есть встроенные <strong>методы</strong> — готовые действия,
    которые можно выполнить над ней через точку: <code class="inline">строка.метод()</code>. Как
    мы выяснили в разделе 8.8, все они возвращают НОВУЮ строку, не трогая исходную.</p>

    <h2>Регистр букв: upper, lower, title, capitalize, swapcase</h2>
    {code_block("registr.py", 'text = "Python с нуля"\nprint(text.upper())      # PYTHON С НУЛЯ\nprint(text.lower())      # python с нуля\nprint(text.title())      # Python С Нуля — первая буква каждого слова заглавная\nprint(text.capitalize()) # Python с нуля — заглавная только у самого первого слова\nprint(text.swapcase())   # pYTHON С НУЛЯ — регистр каждой буквы наоборот\n')}
    {case_flow}

    <h2>Лишние пробелы: strip, lstrip, rstrip</h2>
    <p>Текст, введённый пользователем или взятый из файла, часто содержит случайные пробелы по
    краям. <code class="inline">strip()</code> убирает их с обеих сторон,
    <code class="inline">lstrip()</code> — только слева (left), <code class="inline">rstrip()</code>
    — только справа (right):</p>
    {code_block("probely.py", 'text = "   Python   "\nprint(repr(text.strip()))    # \'Python\'\nprint(repr(text.lstrip()))   # \'Python   \'\nprint(repr(text.rstrip()))   # \'   Python\'\n')}
    {strip_flow}

    {callout(
        "tip",
        "repr() снова пригодился",
        "Мы используем <code class=\"inline\">repr()</code> из раздела 8.2, чтобы увидеть "
        "пробелы по краям строки — обычный <code class=\"inline\">print()</code> их «съедает» "
        "визуально, и не всегда понятно, остались ли они.",
    )}

    {exercise(2, "Чистим и оформляем имя", "Дана строка ⁠«   ада лавлейс   » (с лишними пробелами и строчными буквами). Одной цепочкой методов приведите её к виду «Ада Лавлейс» — уберите пробелы по краям и примените нужный метод регистра.")}

    {practice_card(
        "08-04",
        "Практика: методы регистра и пробелов",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-04/index.html",
    )}
    """
    out = render_page(
        page_title="Методы строк: регистр и пробелы",
        description="Методы строк upper, lower, title, capitalize, swapcase, strip, lstrip, rstrip — с примерами до/после.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Методы: регистр и пробелы", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Методы строк — магия работы со строками!",
        lede="Готовые действия над строками, вызываемые через точку — от смены регистра до "
        "чистки пробелов.",
        body_html=body,
        sidebar_groups=sidebar("08-04-metody-strok.html"),
        nav=PageNav(prev_href="08-15-neizmenyaemost.html", prev_label="Строки нельзя изменить", next_href="08-16-metody-strok-poisk-i-razbor.html", next_label="Методы строк: поиск и разбор"),
    )
    write("08-04-metody-strok.html", out)


# ---------------------------------------------------------------------------
# 8.10 — Методы строк: поиск и разбор
# ---------------------------------------------------------------------------

def build_16() -> None:
    replace_flow = flow_diagram(
        [
            ("Исходная строка", '"я люблю Java"'),
            (".replace(...)", '"Java" →\n"Python"'),
            ("Результат", '"я люблю Python"'),
        ],
        caption='text.replace("Java", "Python") — заменяет ВСЕ вхождения подстроки',
    )
    split_flow = flow_diagram(
        [
            ("Исходная строка", '"кот и пёс"'),
            (".split()", "разбить\nпо пробелам"),
            ("Список слов", "['кот', 'и', 'пёс']"),
        ],
        caption="split() превращает строку в список слов (со списками подробно познакомимся в главе 10)",
    )
    join_flow = flow_diagram(
        [
            ("Список слов", "['кот', 'и', 'пёс']"),
            ('"-".join(...)', "склеить\nчерез дефис"),
            ("Строка", '"кот-и-пёс"'),
        ],
        caption='join() — действие, обратное split(): склеивает список обратно в строку',
    )

    body = f"""
    <h2>replace() — замена подстроки</h2>
    {code_block("replace.py", 'text = "я люблю Java"\nprint(text.replace("Java", "Python"))   # я люблю Python\n')}
    {replace_flow}

    <h2>split() — разбить строку на части</h2>
    <p><code class="inline">split()</code> без аргументов разбивает строку по пробелам (и
    группам пробелов) на список отдельных слов:</p>
    {code_block("split.py", 'sentence = "кот  и пёс"\nwords = sentence.split()\nprint(words)          # [\'кот\', \'и\', \'пёс\']\nprint(len(words))     # 3 слова\n')}
    {split_flow}
    <p>Можно указать свой разделитель — например, запятую:</p>
    {code_block("split_razdelitel.py", 'csv_row = "Ада,28,программист"\nfields = csv_row.split(",")\nprint(fields)          # [\'Ада\', \'28\', \'программист\']\n')}

    <h2>join() — обратная операция: склеить список в строку</h2>
    {code_block("join.py", 'words = ["кот", "и", "пёс"]\nresult = "-".join(words)\nprint(result)          # кот-и-пёс\n')}
    {join_flow}

    <h2>count() — сколько раз встречается</h2>
    {code_block("count.py", 'text = "миссисипи"\nprint(text.count("с"))     # 4\nprint(text.count("си"))    # 2\n')}

    <h2>find() и index() — где встречается</h2>
    <p>Оба метода ищут подстроку и возвращают индекс её первого символа. Разница — в поведении,
    когда подстрока не найдена:</p>
    {code_block("find_i_index.py", 'text = "Python"\nprint(text.find("th"))     # 2 — нашли, начинается с индекса 2\nprint(text.find("zz"))     # -1 — не нашли, find() возвращает -1\n\nprint(text.index("th"))    # 2 — то же самое, что find(), если найдено\n# text.index("zz")         # ValueError: substring not found — index() «падает» с ошибкой!\n')}

    {callout(
        "tip",
        "Когда что выбрать",
        "Если подстроки может не оказаться в тексте — используйте <code class=\"inline\">find()"
        "</code> и проверяйте результат на <code class=\"inline\">-1</code>. Если вы уверены, "
        "что подстрока обязана быть (и хотите узнать сразу, если это не так), — "
        "<code class=\"inline\">index()</code> сообщит об ошибке явно, а не тихо вернёт -1.",
    )}

    <h2>startswith() и endswith()</h2>
    {code_block("startswith_endswith.py", 'filename = "otchet_2026.pdf"\nprint(filename.startswith("otchet"))   # True\nprint(filename.endswith(".pdf"))       # True\nprint(filename.endswith(".docx"))      # False\n')}

    {exercise(2, "Разбираем имя файла", "Для строки «report_final_v2.pdf» проверьте endswith(\".pdf\"), найдите позицию символа «_» методом find(), и через split(\"_\") получите список частей имени.")}

    {practice_card(
        "08-16",
        "Практика: поиск и разбор строк",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-16/index.html",
    )}
    """
    out = render_page(
        page_title="Методы строк: поиск и разбор",
        description="Методы строк replace, split, join, count, find, index, startswith, endswith — с наглядными диаграммами до/после.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Методы: поиск и разбор", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Методы строк: поиск и разбор",
        lede="Заменяем подстроки, разбиваем строку на части и снова склеиваем — а ещё ищем "
        "подстроки внутри текста.",
        body_html=body,
        sidebar_groups=sidebar("08-16-metody-strok-poisk-i-razbor.html"),
        nav=PageNav(prev_href="08-04-metody-strok.html", prev_label="Методы: регистр и пробелы", next_href="08-17-metody-proverki.html", next_label="Методы проверки"),
    )
    write("08-16-metody-strok-poisk-i-razbor.html", out)


# ---------------------------------------------------------------------------
# 8.11 — Методы проверки
# ---------------------------------------------------------------------------

def build_17() -> None:
    body = f"""
    <h2>Методы, которые отвечают True или False</h2>
    <p>У строк есть целая группа методов, которые проверяют, ИЗ ЧЕГО состоит строка, и отвечают
    <code class="inline">True</code> или <code class="inline">False</code>. Они особенно
    полезны для проверки ввода пользователя (раздел 8.15) — до того, как пытаться
    преобразовать текст в число.</p>

    {code_block("metody_proverki.py", 'print("Python".isalpha())     # True — только буквы\nprint("Python3".isalpha())    # False — есть цифра\n\nprint("2026".isdigit())       # True — только цифры\nprint("28 лет".isdigit())     # False — есть пробел и буквы\n\nprint("Python3".isalnum())    # True — только буквы и/или цифры\nprint("Python 3".isalnum())   # False — есть пробел\n\nprint("   ".isspace())        # True — только пробельные символы\nprint("".isspace())           # False — пустая строка не считается\n')}

    <div class="compare-table-wrap" style="overflow-x:auto">
    <table class="compare-table">
      <thead><tr><th>Метод</th><th>Проверяет</th></tr></thead>
      <tbody>
        <tr><td><code class="inline">isalpha()</code></td><td>только буквы (любого алфавита)</td></tr>
        <tr><td><code class="inline">isdigit()</code></td><td>только цифры 0–9</td></tr>
        <tr><td><code class="inline">isalnum()</code></td><td>только буквы и/или цифры</td></tr>
        <tr><td><code class="inline">isspace()</code></td><td>только пробелы/табуляции/переносы</td></tr>
      </tbody>
    </table>
    </div>

    {callout(
        "info",
        "isnumeric() и isdecimal() — родственники isdigit()",
        "Это более редкие варианты той же идеи: <code class=\"inline\">isdecimal()</code> — "
        "самый строгий (только обычные цифры 0-9), <code class=\"inline\">isdigit()</code> — "
        "чуть шире (включает и некоторые специальные цифровые символы), "
        "<code class=\"inline\">isnumeric()</code> — самый широкий (понимает и текстовые "
        "числительные вроде римских цифр в некоторых системах письма). Для учебных задач и "
        "проверки обычного пользовательского ввода <code class=\"inline\">isdigit()</code> "
        "достаточно почти всегда.",
    )}

    <h2>Практическое применение: проверка перед преобразованием</h2>
    {code_block("proverka_pered_int.py", 'age_text = "28"\nif age_text.isdigit():\n    age = int(age_text)\n    print(f"Через 5 лет: {age + 5}")\nelse:\n    print("Это не похоже на число")\n')}
    <p>Полный оператор <code class="inline">if</code> подробно разберём в главе 9 — но уже
    сейчас видно, как <code class="inline">isdigit()</code> помогает не дать программе упасть
    с ошибкой при попытке <code class="inline">int()</code> от нечислового текста.</p>

    {exercise(1, "Что за строка?", "Для трёх строк «Python3», «2026», «   » выведите результат isalpha(), isdigit() и isspace() для каждой — и убедитесь, что понимаете, почему получился именно такой результат.")}

    {practice_card(
        "08-17",
        "Практика: методы проверки строки",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-17/index.html",
    )}
    """
    out = render_page(
        page_title="Методы проверки: isalpha и другие",
        description="Методы проверки строк isalpha, isdigit, isalnum, isspace — и как использовать их перед преобразованием текста в число.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Методы проверки", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Методы проверки: isalpha и другие",
        lede="Методы, которые отвечают True/False о том, из чего состоит строка — незаменимы "
        "перед преобразованием текста в число.",
        body_html=body,
        sidebar_groups=sidebar("08-17-metody-proverki.html"),
        nav=PageNav(prev_href="08-16-metody-strok-poisk-i-razbor.html", prev_label="Методы: поиск и разбор", next_href="08-05-istina-lozh.html", next_label="in, сравнение и истинность"),
    )
    write("08-17-metody-proverki.html", out)


# ---------------------------------------------------------------------------
# 8.12 — in / сравнение / истинность (существующий, лёгкая правка)
# ---------------------------------------------------------------------------

def build_05() -> None:
    body = f"""
    <h2>in и not in — проверка вхождения</h2>
    <p>Оператор <code class="inline">in</code> проверяет, содержится ли одна строка внутри
    другой — очень частая и полезная проверка:</p>
    {code_block("in_i_not_in.py", 'print("thon" in "Python")       # True — "thon" встречается внутри "Python"\nprint("java" in "Python")       # False\nprint("java" not in "Python")   # True — обратная проверка\n')}

    <h2>Сравнение строк</h2>
    <p>Строки можно сравнивать друг с другом оператором <code class="inline">==</code> —
    результатом всегда будет <code class="inline">True</code> или <code class="inline">False</code>:</p>
    {code_block("sravnenie_strok.py", 'print("Python" == "Python")     # True — строки совпадают полностью\nprint("Python" == "python")     # False — регистр важен!\n')}

    {callout(
        "warning",
        "== сравнивает значение, is сравнивает объект",
        "Для строк почти всегда нужен именно <code class=\"inline\">==</code>. Оператор "
        "<code class=\"inline\">is</code> проверяет, один ли это объект в памяти, — гораздо "
        "более редкий и специфичный случай, к которому мы вернёмся в главе 14.",
    )}

    <h2>Пустая строка — это «ложь»</h2>
    <p>В логических проверках (полноценный <code class="inline">if</code> — в главе 9) пустая
    строка ведёт себя как <code class="inline">False</code>, а любая непустая строка — как
    <code class="inline">True</code>:</p>
    {code_block("pustaya_stroka_logika.py", 'print(bool(""))         # False\nprint(bool("Python"))   # True\nprint(bool(" "))        # True — пробел — это тоже символ!\n')}

    {exercise(1, "Проверка домена", "Для адреса «support@cartesianschool.org» проверьте через in, содержится ли в нём «@» и содержится ли «.ru».")}

    {practice_card(
        "08-03",
        "Практика: in, сравнение и истинность строк",
        "Тот же ноутбук, что и в разделе «Индексы строки» — он охватывает и эту тему",
        "../../practice/08-03/index.html",
    )}
    """
    out = render_page(
        page_title="in, сравнение и истинность",
        description="Оператор in/not in для проверки вхождения подстроки, сравнение строк и логическое значение (истинность) строк.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("in и сравнение", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="in, сравнение строк и истинность",
        lede="Проверяем, входит ли одна строка в другую, сравниваем строки друг с другом — и "
        "выясняем, когда строка ведёт себя как «ложь».",
        body_html=body,
        sidebar_groups=sidebar("08-05-istina-lozh.html"),
        nav=PageNav(prev_href="08-17-metody-proverki.html", prev_label="Методы проверки", next_href="08-18-cikl-po-stroke.html", next_label="Перебираем строку в цикле"),
    )
    write("08-05-istina-lozh.html", out)


# ---------------------------------------------------------------------------
# 8.13 — for ch in text
# ---------------------------------------------------------------------------

def build_18() -> None:
    body = f"""
    {callout(
        "info",
        "[[icon:launch]] Забегаем вперёд",
        "Мы ещё не проходили циклы подробно — это тема главы 9. Здесь достаточно понимать "
        "<code class=\"inline\">for ch in text:</code> буквально: «повтори блок кода для "
        "каждого символа text по очереди, каждый раз кладя очередной символ в переменную "
        "ch». Полное устройство цикла <code class=\"inline\">for</code> разберём позже.",
    )}

    <h2>Строка — это последовательность, по которой можно пройтись</h2>
    <p>Раз строка — это набор символов по порядку (раздел 8.1), по ней можно
    <strong>перебирать</strong> — то есть заглянуть в каждый символ по очереди:</p>
    {code_block("perebor_stroki.py", 'word = "Python"\nfor ch in word:\n    print(ch)\n# P\n# y\n# t\n# h\n# o\n# n\n')}

    <h2>Практический пример: считаем гласные</h2>
    {code_block("schitaem_glasnye.py", 'text = "программирование"\nglasnye = "аеёиоуыэюя"\ncount = 0\nfor ch in text:\n    if ch in glasnye:\n        count += 1\nprint(f"Гласных букв: {count}")\n# Гласных букв: 7\n')}
    <p>Здесь мы уже заглянули немного вперёд и на <code class="inline">if</code> (глава 9), но
    сама идея «пройтись по каждому символу и что-то с ним сделать» — это именно перебор
    строки, ключевая мысль этого раздела.</p>

    {exercise(1, "Считаем конкретную букву", "Переберите строку «миссисипи» в цикле for и посчитайте, сколько раз встречается буква «и» — вручную, без использования count() из раздела 8.10.")}

    {practice_card(
        "08-18",
        "Практика: перебор строки в цикле",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-18/index.html",
    )}
    """
    out = render_page(
        page_title="Перебираем строку в цикле",
        description="Перебор строки циклом for ch in text — базовая интуиция для дальнейшей темы циклов.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Цикл по строке", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Перебираем строку в цикле",
        lede="Строка — последовательность символов, по которой можно пройтись один за другим — "
        "первое знакомство с идеей цикла.",
        body_html=body,
        sidebar_groups=sidebar("08-18-cikl-po-stroke.html"),
        nav=PageNav(prev_href="08-05-istina-lozh.html", prev_label="in, сравнение и истинность", next_href="08-06-formatirovanie-strok.html", next_label="Форматирование строк"),
    )
    write("08-18-cikl-po-stroke.html", out)


# ---------------------------------------------------------------------------
# 8.14 — Форматирование строк (существующий, СИЛЬНО расширяем)
# ---------------------------------------------------------------------------

def build_06() -> None:
    cvm = classic_vs_modern(
        "Форматирование строк: % → .format() → f-строки",
        "Классический подход (% и .format())",
        'name = "Cartesian"\nage = 5\n\n'
        '# оператор % — самый старый способ\n'
        'print("Привет, %s! Тебе %d лет." % (name, age))\n\n'
        '# .format() — более новый, но всё ещё многословный\n'
        'print("Привет, {}! Тебе {} лет.".format(name, age))',
        "Современный Python 3.14 (f-строки)",
        'name = "Cartesian"\nage = 5\n\n'
        '# f-строка — значения прямо внутри {}\n'
        'print(f"Привет, {name}! Тебе {age} лет.")\n\n'
        '# работают и выражения, не только переменные:\n'
        'print(f"Через год будет {age + 1}.")',
        "f-строки — они появились в Python 3.6 и с тех пор являются стандартом. Оператор "
        "<code class=\"inline\">%</code> — самый старый способ, доставшийся от языка Си, "
        "всё ещё встречается в старом коде. <code class=\"inline\">.format()</code> — "
        "промежуточный шаг между ними. f-строки читаются лучше всего: значение видно прямо "
        "там, где оно будет подставлено, и можно писать любые выражения, а не только имена "
        "переменных.",
    )

    body = f"""
    <p>Мы уже пользовались f-строками начиная с главы 4 — теперь разберём форматирование строк
    по-настоящему полно.</p>

    <h2>f-строка — простая подстановка</h2>
    <p>Перед открывающей кавычкой ставится буква <code class="inline">f</code>, а внутри
    фигурных скобок <code class="inline">{{}}</code> — имя переменной. Python сам подставит
    туда значение:</p>
    {code_block("f_stroka_prostaya.py", 'name = "Ада"\nprint(f"Привет, {name}!")\n# Привет, Ада!\n')}

    <h2>Внутри {{}} можно писать выражения</h2>
    <p>Это не просто подстановка имени — внутри скобок работает ЛЮБОЕ Python-выражение:
    арифметика, вызов метода, что угодно:</p>
    {code_block("f_stroka_vyrazheniya.py", 'age = 5\nprint(f"Через год будет {age + 1}.")           # Через год будет 6.\n\nname = "cartesian"\nprint(f"Заглавными: {name.upper()}")            # Заглавными: CARTESIAN\n')}

    <h2>Форматирование чисел: точность и разделители</h2>
    <p>После значения можно поставить двоеточие и <strong>спецификатор формата</strong> — как
    именно отобразить число:</p>
    {code_block("format_specifikatory.py", 'pi = 3.14159265\nprint(f"Пи округлённо: {pi:.2f}")   # Пи округлённо: 3.14 — 2 знака после запятой\nprint(f"{1234567:,}")               # 1,234,567 — разделитель тысяч\nprint(f"{0.4567:.1%}")              # 45.7% — доля как проценты\n')}
    <p><code class="inline">.2f</code> читается так: <code class="inline">f</code> — число с
    плавающей точкой, <code class="inline">.2</code> — округлить до 2 знаков после запятой.</p>

    <h2>Выравнивание и ширина</h2>
    <p>Число после двоеточия (без точки) задаёт минимальную ширину поля — удобно для
    выравнивания текста в столбик:</p>
    {code_block("vyravnivanie.py", 'for name, score in [("Ада", 98), ("Алан", 87), ("Грейс", 100)]:\n    print(f"{name:<8} {score:>5}")\n# Ада        98\n# Алан       87\n# Грейс     100\n')}

    <div class="compare-table-wrap" style="overflow-x:auto">
    <table class="compare-table">
      <thead><tr><th>Спецификатор</th><th>Значение</th></tr></thead>
      <tbody>
        <tr><td><code class="inline">{{value:&lt;10}}</code></td><td>по левому краю, ширина поля 10</td></tr>
        <tr><td><code class="inline">{{value:&gt;10}}</code></td><td>по правому краю, ширина поля 10</td></tr>
        <tr><td><code class="inline">{{value:^10}}</code></td><td>по центру, ширина поля 10</td></tr>
        <tr><td><code class="inline">{{value:.2f}}</code></td><td>дробное число, 2 знака после запятой</td></tr>
        <tr><td><code class="inline">{{value:,}}</code></td><td>разделитель тысяч запятой</td></tr>
      </tbody>
    </table>
    </div>

    {callout(
        "tip",
        "Отладочный приём: f\"{{value=}}\"",
        "Если внутри f-строки после выражения поставить знак <code class=\"inline\">=</code> "
        "— Python выведет и само выражение, и его значение. Отлично подходит для быстрой "
        "проверки: <code class=\"inline\">print(f\"{{age=}}\")</code> выведет "
        "<code class=\"inline\">age=28</code> — без ручного набора текста «age =».",
    )}

    {cvm}

    {exercise(2, "Чек «на столе»", "Выведите строку «Итого: 1234.5 → 1 234.50 ₽» (используя :,.2f) для суммы 1234.5, и отдельно — «Скидка: 15.0%» для доли 0.15 (используя :.1%).")}

    {practice_card(
        "08-06",
        "Практика: %, .format() и f-строки",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-06/index.html",
    )}
    """
    out = render_page(
        page_title="Форматирование строк",
        description="f-строки в глубину: подстановка, выражения, форматирование чисел, ширина и выравнивание — плюс исторический контекст % и .format().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Форматирование строк", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Форматирование строк",
        lede="f-строки — главный современный инструмент вставки значений в текст. Разберём их "
        "по-настоящему полно: от простой подстановки до выравнивания в столбик.",
        body_html=body,
        sidebar_groups=sidebar("08-06-formatirovanie-strok.html"),
        nav=PageNav(prev_href="08-18-cikl-po-stroke.html", prev_label="Цикл по строке", next_href="08-07-vvod-polzovatelya.html", next_label="Ввод от пользователя"),
    )
    write("08-06-formatirovanie-strok.html", out)


# ---------------------------------------------------------------------------
# 8.15 — input() (существующий, расширяем)
# ---------------------------------------------------------------------------

def build_07() -> None:
    body = f"""
    <p>До сих пор все данные в программах были «зашиты» прямо в код. Пора научиться получать
    данные от самого пользователя во время выполнения программы — с этого момента ваши программы
    становятся по-настоящему интерактивными.</p>

    {code_block("vvod.py", 'name = input("Как вас зовут? ")\nprint(f"Привет, {name}!")\n\n# Диалог в терминале:\n# Как вас зовут? Ада\n# Привет, Ада!\n')}
    <p><code class="inline">input()</code> останавливает программу и ждёт, пока пользователь
    наберёт текст и нажмёт Enter — то, что он ввёл, возвращается как обычная строка.</p>

    {callout(
        "info",
        "input() в браузерной практике — по-настоящему интерактивный",
        "Наш браузерный ноутбук практики умеет по-настоящему ждать ваш ответ на "
        "<code class=\"inline\">input()</code> — прямо как обычный <code class=\"inline\">.py</code>-файл, "
        "запущенный на компьютере: программа останавливается, показывает подсказку и ждёт, "
        "пока вы наберёте текст.",
    )}

    <h2>Простое правило: input → строка → преобразовать, если нужно число</h2>
    <p><code class="inline">input()</code> <strong>всегда</strong> возвращает строку — даже
    если пользователь ввёл число. Чтобы посчитать что-то с этим значением, его нужно
    преобразовать (как мы делали в главе 4):</p>
    {code_block("vvod_chisla.py", 'age_text = input("Сколько вам лет? ")\nprint(type(age_text))     # <class \'str\'> — даже если ввели "28"\n\nage = int(age_text)\nprint(f"Через 5 лет вам будет {age + 5}.")\n')}

    {callout(
        "warning",
        "Частая ошибка новичков",
        "Если забыть про <code class=\"inline\">int()</code> и написать "
        "<code class=\"inline\">age + 5</code>, где <code class=\"inline\">age</code> — строка "
        "из <code class=\"inline\">input()</code>, Python выдаст <code class=\"inline\">TypeError"
        "</code>: складывать строку и число напрямую нельзя.",
    )}

    <h2>Ещё несколько диалогов</h2>
    {code_block("dialogi.py", 'city = input("В каком городе вы живёте? ")\nprint(f"{city} — отличный город!")\n\nheight_text = input("Ваш рост в см? ")\nheight = float(height_text)\nprint(f"Ваш рост в метрах: {height / 100:.2f}")\n')}

    {exercise(1, "Приветствие с проверкой", "Спросите имя через input(), а затем проверьте (через isalpha() из раздела 8.11), состоит ли оно только из букв — выведите разный текст в зависимости от результата.")}

    {practice_card(
        "08-07",
        "Практика: input() и преобразование типов",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-07/index.html",
    )}
    """
    out = render_page(
        page_title="Получение ввода от пользователей",
        description="input() и преобразование введённого текста в int/float — начало автоматизации взаимодействия с пользователем.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Ввод от пользователя", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Получение ввода от пользователей",
        lede="Начало автоматизации: программа, которая спрашивает — и реагирует на ответ.",
        body_html=body,
        sidebar_groups=sidebar("08-07-vvod-polzovatelya.html"),
        nav=PageNav(prev_href="08-06-formatirovanie-strok.html", prev_label="Форматирование строк", next_href="08-19-unikod-i-emodzi.html", next_label="Кириллица, юникод и эмодзи"),
    )
    write("08-07-vvod-polzovatelya.html", out)


# ---------------------------------------------------------------------------
# 8.16 — Юникод
# ---------------------------------------------------------------------------

def build_19() -> None:
    body = f"""
    <h2>Python дружит с любым языком</h2>
    <p>Строки Python умеют хранить символы ЛЮБОГО языка мира — кириллицу, латиницу, иероглифы,
    даже эмодзи — благодаря системе кодирования <strong>Юникод</strong> (Unicode), встроенной в
    Python «из коробки». Не нужно ничего специально настраивать:</p>
    {code_block("unikod_primery.py", 'russkij = "Привет, мир!"\nenglish = "Hello, world!"\nsmajlik = "Python — это 🐍 и 🎉"\nprint(russkij)\nprint(english)\nprint(smajlik)\n')}

    <h2>Длина строки с эмодзи</h2>
    {code_block("dlina_s_emodzi.py", 'text = "код 🐍"\nprint(len(text))    # 6 — "к","о","д"," ","🐍" — но пробел + эмодзи считаются отдельно\n')}

    {callout(
        "info",
        "Достаточно знать на этом уровне",
        "Полная теория кодировок (UTF-8, байты, таблицы символов) — тема для будущих, более "
        "продвинутых глав. Сейчас важно только одно: в Python 3 кириллица, латиница и эмодзи "
        "работают одинаково хорошо и без специальной настройки — можно свободно писать "
        "код и тексты программ на русском.",
    )}

    <h2>Всё, что мы уже умеем, работает и здесь</h2>
    {code_block("metody_na_kirillice.py", 'text = "Привет, Мир"\nprint(text.upper())     # ПРИВЕТ, МИР\nprint(text.lower())     # привет, мир\nprint(text[::-1])       # риМ ,тевирП\n')}

    {exercise(1, "Эмодзи-приветствие", "Соберите строку с помощью конкатенации из трёх частей: «Добро пожаловать» + пробел + эмодзи по вашему выбору, и выведите её длину через len().")}

    {practice_card(
        "08-01",
        "Практика: строки на разных языках",
        "Тот же ноутбук, что и в разделе «Что такое строки?» — он охватывает и эту тему",
        "../../practice/08-01/index.html",
    )}
    """
    out = render_page(
        page_title="Кириллица, юникод и эмодзи",
        description="Python и Юникод: кириллица, латиница и эмодзи в строках работают без специальной настройки.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Юникод и эмодзи", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Кириллица, юникод и эмодзи",
        lede="Строки Python одинаково хорошо понимают любой язык мира — и даже эмодзи.",
        body_html=body,
        sidebar_groups=sidebar("08-19-unikod-i-emodzi.html"),
        nav=PageNav(prev_href="08-07-vvod-polzovatelya.html", prev_label="Ввод от пользователя", next_href="08-20-otladka-strok.html", next_label="Отладка проблем со строками"),
    )
    write("08-19-unikod-i-emodzi.html", out)


# ---------------------------------------------------------------------------
# 8.17 — Отладка
# ---------------------------------------------------------------------------

def build_20() -> None:
    body = f"""
    <p>Строки — источник особенно коварных ошибок: они часто выглядят правильно на глаз, а
    ломаются из-за одного невидимого символа. Разберём самые частые ситуации.</p>

    <h2>Невидимые пробелы</h2>
    {code_block("nevidimye_probely.py", 'password = "секрет "     # случайный пробел в конце!\nprint(password == "секрет")   # False — а на глаз не отличить\nprint(repr(password))          # \'секрет \' — repr() выдаёт пробел\n')}
    {callout("tip", "repr() — ваш главный инструмент", "Мы уже видели repr() в разделе 8.2 — он показывает строку «как есть», включая пробелы и служебные символы, которые print() визуально скрывает.")}

    <h2>Забытая кавычка</h2>
    {code_block("zabytaya_kavychka.py", '# text = "Привет, мир!    # забыли закрывающую кавычку\n# SyntaxError: unterminated string literal\n')}

    <h2>Неправильное экранирование</h2>
    {code_block("nepravilnoe_ekranirovanie.py", '# path = "C:\\new_folder"   # \\n здесь превратится в перенос строки!\nprint("C:\\new_folder")\n# C:\n# ew_folder   — совсем не то, что хотели\n\nprint(r"C:\\new_folder")    # C:\\new_folder — raw-строка (раздел 8.3) решает проблему\n')}

    <h2>Склеивание строки с числом</h2>
    {code_block("stroka_plyus_chislo.py", 'score = 95\n# print("Результат: " + score)   # TypeError\nprint("Результат: " + str(score))   # исправлено — явное преобразование\nprint(f"Результат: {score}")        # ещё лучше — f-строка сама преобразует\n')}

    <h2>find() vs index() при отсутствии подстроки</h2>
    {code_block("find_vs_index_oshibka.py", 'text = "Python"\nprint(text.find("java"))    # -1 — тихо возвращает -1, легко пропустить в коде\n# text.index("java")        # ValueError — а вот index() сразу сообщает об ошибке\n')}
    <p>Частая ошибка — забыть, что <code class="inline">find()</code> при отсутствии подстроки
    возвращает <code class="inline">-1</code>, а не <code class="inline">False</code> или
    <code class="inline">None</code>. Проверка вроде <code class="inline">if text.find("java"):</code>
    сработает неверно, потому что <code class="inline">-1</code> — это истина в логической
    проверке! Правильно — сравнивать явно: <code class="inline">if text.find("java") != -1:</code>.</p>

    <h2>input() «на самом деле» не число</h2>
    {code_block("input_ne_chislo.py", 'age = input("Возраст? ")   # даже если ввели "28" — это строка "28"\n# print(age + 1)           # TypeError — забыли int()\nprint(int(age) + 1)         # правильно\n')}

    <h2>Итоговая шпаргалка отладки строк</h2>
    <div class="compare-table-wrap" style="overflow-x:auto">
    <table class="compare-table">
      <thead><tr><th>Симптом</th><th>Причина</th><th>Как исправить</th></tr></thead>
      <tbody>
        <tr><td>Сравнение <code class="inline">==</code> неожиданно False</td><td>невидимый пробел или другой регистр</td><td><code class="inline">repr()</code>, <code class="inline">.strip()</code>, <code class="inline">.lower()</code></td></tr>
        <tr><td><code class="inline">SyntaxError: unterminated string</code></td><td>забыта закрывающая кавычка</td><td>проверить парность кавычек</td></tr>
        <tr><td>Текст «сломался», появился неожиданный перенос строки</td><td>случайный <code class="inline">\\n</code> в пути/тексте</td><td>raw-строка <code class="inline">r"..."</code></td></tr>
        <tr><td><code class="inline">TypeError: can only concatenate str</code></td><td>сложение строки с числом через +</td><td><code class="inline">str()</code> или f-строка</td></tr>
        <tr><td><code class="inline">if text.find(...)</code> ведёт себя странно</td><td>-1 — это истина в булевой проверке</td><td>сравнивать <code class="inline">!= -1</code> явно</td></tr>
        <tr><td><code class="inline">TypeError</code> при арифметике с input()</td><td>input() всегда возвращает строку</td><td><code class="inline">int()</code>/<code class="inline">float()</code></td></tr>
      </tbody>
    </table>
    </div>

    {exercise(2, "Найдите ошибку", "В строке `total = \"Сумма: \" + 100` есть ошибка. Определите её тип, объясните причину и перепишите строку двумя разными способами, чтобы она работала.")}

    {practice_card(
        "08-20",
        "Практика: отладка строковых ошибок",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-20/index.html",
    )}
    """
    out = render_page(
        page_title="Отладка проблем со строками",
        description="Частые ошибки со строками: невидимые пробелы, неверное экранирование, str+int, find/index, input() — симптом, причина, исправление.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Отладка строк", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Отладка проблем со строками",
        lede="Строки часто выглядят правильными на глаз, а ломаются из-за одного невидимого "
        "символа. Учимся находить и чинить такие ошибки.",
        body_html=body,
        sidebar_groups=sidebar("08-20-otladka-strok.html"),
        nav=PageNav(prev_href="08-19-unikod-i-emodzi.html", prev_label="Юникод и эмодзи", next_href="08-08-mini-proekt-turtle-tekst.html", next_label="Мини-проект: текст Turtle"),
    )
    write("08-20-otladka-strok.html", out)


# ---------------------------------------------------------------------------
# 8.18 — Мини-проект: текст Turtle (существующий)
# ---------------------------------------------------------------------------

def build_08() -> None:
    body = f"""
    <p>Соединим строки, ввод от пользователя и Turtle из глав 6–7: спросим имя и выведем
    персональное приветствие прямо на холсте.</p>
    {code_block(
        "turtle_tekst_imya.py",
        "import turtle\n\n"
        "screen = turtle.Screen()\n"
        "artist = turtle.Turtle()\n"
        "artist.hideturtle()\n\n"
        'name = input("Как вас зовут? ")\n\n'
        "artist.penup()\n"
        "artist.goto(0, 0)\n"
        'artist.write(f"Привет, {name}!", align="center", font=("Arial", 24, "bold"))\n\n'
        "screen.exitonclick()\n",
    )}
    {exercise(2, "Приветствие по времени суток", "Спросите у пользователя число (час дня) через input() + int(), и выведите разный текст в зависимости от значения — используя пока лишь то, что уже знаете о строках (полноценный if будет в главе 9, здесь достаточно вывести один текст с подставленным часом).")}

    {practice_card(
        "08-07",
        "Практика: ввод имени (логика, без окна Turtle)",
        "Тот же ноутбук, что и в разделе «Ввод от пользователя» — он охватывает и эту тему",
        "../../practice/08-07/index.html",
    )}
    """
    out = render_page(
        page_title="Мини-проект — текст Turtle на новый уровень!",
        description="Объединяем ввод пользователя, строки и Turtle: персональное приветствие на холсте.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Текст Turtle", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Мини-проект — выводим текст Turtle на новый уровень!",
        lede="Объединяем input() из раздела 8.15 с write() из главы 7 — персональное "
        "приветствие прямо на холсте.",
        body_html=body,
        sidebar_groups=sidebar("08-08-mini-proekt-turtle-tekst.html"),
        nav=PageNav(prev_href="08-20-otladka-strok.html", prev_label="Отладка проблем со строками", next_href="08-21-mini-proekt-privetstvie-i-imya.html", next_label="Мини-проект: приветствие и ФИО"),
    )
    write("08-08-mini-proekt-turtle-tekst.html", out)


# ---------------------------------------------------------------------------
# 8.19 — Мини-проект: генератор приветствий и форматирование ФИО
# ---------------------------------------------------------------------------

def build_21() -> None:
    body = f"""
    <h2>Мини-проект — генератор приветствий</h2>
    <p>Собираем время суток и имя в одно вежливое приветствие — используя f-строки (раздел
    8.14) и методы регистра (раздел 8.9):</p>
    {code_block(
        "generator_privetstvij.py",
        'daytime = input("Сейчас утро, день, вечер или ночь? ")\n'
        'name = input("Как вас зовут? ")\n\n'
        'privetstviya = {\n'
        '    "утро": "Доброе утро",\n'
        '    "день": "Добрый день",\n'
        '    "вечер": "Добрый вечер",\n'
        '    "ночь": "Доброй ночи",\n'
        '}\n'
        'privetstvie = privetstviya.get(daytime.lower().strip(), "Здравствуйте")\n'
        'print(f"{privetstvie}, {name.strip().title()}!")\n'
        '# Доброе утро, Ада!\n',
    )}
    {callout(
        "info",
        "[[icon:launch]] Забегаем вперёд",
        "Здесь мы уже используем словарь <code class=\"inline\">{...}</code> — структуру "
        "«ключ → значение», которую подробно разберём в главе 11. Сейчас достаточно понимать "
        "<code class=\"inline\">.get(ключ, значение_по_умолчанию)</code>: «найди ключ, а если "
        "его нет — верни запасной вариант».",
    )}

    <h2 id="fio">Мини-проект — форматировщик ФИО</h2>
    <p>Частая практическая задача: привести введённое имя и фамилию к аккуратному виду
    независимо от того, как их ввёл пользователь — капсом, строчными, с лишними пробелами:</p>
    {code_block(
        "formatirovshik_fio.py",
        'raw_first = input("Имя: ")\n'
        'raw_last = input("Фамилия: ")\n\n'
        'first = raw_first.strip().capitalize()\n'
        'last = raw_last.strip().capitalize()\n'
        'full_name = f"{first} {last}"\n'
        'initials = f"{first[0]}. {last[0]}."\n\n'
        'print(f"Полное имя: {full_name}")\n'
        'print(f"Инициалы: {initials}")\n'
        '# ввод: "  ада  " / "ЛАВЛЕЙС"\n'
        '# Полное имя: Ада Лавлейс\n'
        '# Инициалы: А. Л.\n',
    )}

    {exercise(2, "Электронная подпись", "Расширьте формировщик ФИО: добавьте третий input() для профессии, и соберите e-mail-подпись вида «Ада Лавлейс, программист» одной f-строкой.")}

    {practice_card(
        "08-21",
        "Практика: генератор приветствий и ФИО",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-21/index.html",
    )}
    """
    out = render_page(
        page_title="Мини-проект: приветствие и ФИО",
        description="Два мини-проекта на строки: генератор приветствий по времени суток и форматировщик ФИО с инициалами.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Приветствие и ФИО", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Мини-проект — приветствие и форматирование ФИО",
        lede="Собираем f-строки, методы регистра и strip() в двух практичных мини-проектах.",
        body_html=body,
        sidebar_groups=sidebar("08-21-mini-proekt-privetstvie-i-imya.html"),
        nav=PageNav(prev_href="08-08-mini-proekt-turtle-tekst.html", prev_label="Текст Turtle", next_href="08-09-mini-proekty-krik-perevorot.html", next_label="Крик и переворот"),
    )
    write("08-21-mini-proekt-privetstvie-i-imya.html", out)


# ---------------------------------------------------------------------------
# 8.20 — Мини-проекты: крик и переворот (существующий)
# ---------------------------------------------------------------------------

def build_09() -> None:
    body = f"""
    <h2>Мини-проект — кричим на экран</h2>
    <p>Простая, но забавная программа: превращает любую фразу в «крик» — капсом и с кучей
    восклицательных знаков.</p>
    {code_block(
        "krik.py",
        'phrase = input("Что вы хотите прокричать? ")\n'
        "krik = phrase.upper() + \"!!!\"\n"
        "print(krik)\n",
    )}

    <h2 id="perevorot">Мини-проект — переворачиваем своё имя</h2>
    <p>Используем срез <code class="inline">[::-1]</code> из раздела 8.7, чтобы развернуть
    введённое имя задом наперёд:</p>
    {code_block(
        "perevorot_imeni.py",
        'name = input("Как вас зовут? ")\n'
        "perevernutoe = name[::-1]\n"
        'print(f"Ваше имя задом наперёд: {perevernutoe}")\n',
    )}

    {exercise(1, "Крик с ограничением", "Измените krik.py так, чтобы восклицательных знаков было столько же, сколько букв во фразе (подсказка: умножение строки на число — str * n — повторяет её n раз, раздел 8.4).")}
    {exercise(2, "Палиндром?", "Допишите perevorot_imeni.py так, чтобы он сообщал, является ли введённое слово палиндромом — читается ли оно одинаково в обе стороны (сравните name с перевёрнутой версией).")}

    {practice_card(
        "08-09",
        "Практика: крик и переворот имени",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-09/index.html",
    )}
    """
    out = render_page(
        page_title="Мини-проекты: крик и переворот имени",
        description="Два коротких мини-проекта: превращаем фразу в крик и разворачиваем имя задом наперёд.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Крик и переворот", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Мини-проект — кричим на экран",
        lede="Два коротких, но показательных мини-проекта на методы и срезы строк.",
        body_html=body,
        sidebar_groups=sidebar("08-09-mini-proekty-krik-perevorot.html"),
        nav=PageNav(prev_href="08-21-mini-proekt-privetstvie-i-imya.html", prev_label="Приветствие и ФИО", next_href="08-22-mini-proekt-parol-i-email.html", next_label="Пароль и e-mail"),
    )
    write("08-09-mini-proekty-krik-perevorot.html", out)


# ---------------------------------------------------------------------------
# 8.21 — Мини-проект: проверка пароля и e-mail
# ---------------------------------------------------------------------------

def build_22() -> None:
    body = f"""
    <h2>Мини-проект — простая проверка пароля</h2>
    <p>Соберём несколько правил (длина, наличие цифры, наличие буквы) в одну проверку —
    используя методы проверки из раздела 8.11:</p>
    {code_block(
        "proverka_parolya.py",
        'password = input("Придумайте пароль: ")\n\n'
        'dostatochno_dlinnyj = len(password) >= 8\n'
        'est_cifra = any(ch.isdigit() for ch in password)\n'
        'est_bukva = any(ch.isalpha() for ch in password)\n\n'
        'print(f"Длина от 8 символов: {dostatochno_dlinnyj}")\n'
        'print(f"Есть цифра: {est_cifra}")\n'
        'print(f"Есть буква: {est_bukva}")\n\n'
        'nadyozhnyj = dostatochno_dlinnyj and est_cifra and est_bukva\n'
        'print(f"Пароль надёжный: {nadyozhnyj}")\n',
    )}
    {callout(
        "info",
        "[[icon:launch]] Забегаем вперёд",
        "<code class=\"inline\">any(...)</code> с выражением внутри — это компактная форма "
        "цикла из раздела 8.13: «есть ли хотя бы один символ, для которого условие верно». "
        "Подробно операторы <code class=\"inline\">and</code>/<code class=\"inline\">or</code> "
        "и такие компактные конструкции разберём в главах 9–10.",
    )}

    <h2 id="email">Мини-проект — простая проверка e-mail</h2>
    <p>Настоящая проверка email — сложная задача (для неё существуют специальные библиотеки), но
    базовые «здравые» проверки уже можно сделать тем, что мы знаем: <code class="inline">in</code>
    (раздел 8.12), <code class="inline">count()</code> и <code class="inline">find()</code>
    (раздел 8.10):</p>
    {code_block(
        "proverka_email.py",
        'email = input("Ваш e-mail: ").strip()\n\n'
        'est_sobachka = "@" in email\n'
        'odna_sobachka = email.count("@") == 1\n'
        'est_tochka_posle = "." in email[email.find("@"):] if est_sobachka else False\n\n'
        'pohozhe_na_email = est_sobachka and odna_sobachka and est_tochka_posle\n'
        'print(f"Похоже на e-mail: {pohozhe_na_email}")\n'
        '# ввод: "ada@cartesianschool.org"\n'
        '# Похоже на e-mail: True\n',
    )}

    {exercise(2, "Своё правило", "Добавьте к проверке пароля ещё одно правило: пароль не должен содержать пробелов (используйте isspace() или in \" \"). Проверьте программу на пароле с пробелом и без.")}

    {practice_card(
        "08-22",
        "Практика: проверка пароля и e-mail",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-22/index.html",
    )}
    """
    out = render_page(
        page_title="Мини-проект: пароль и e-mail",
        description="Мини-проекты: простая проверка надёжности пароля и базовая проверка формата e-mail.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Пароль и e-mail", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Мини-проект — проверка пароля и e-mail",
        lede="Собираем методы проверки строк в две практичные программы валидации ввода.",
        body_html=body,
        sidebar_groups=sidebar("08-22-mini-proekt-parol-i-email.html"),
        nav=PageNav(prev_href="08-09-mini-proekty-krik-perevorot.html", prev_label="Крик и переворот", next_href="08-23-mini-proekt-schetchik-slov.html", next_label="Счётчик слов"),
    )
    write("08-22-mini-proekt-parol-i-email.html", out)


# ---------------------------------------------------------------------------
# 8.22 — Мини-проект: счётчик слов и чистка предложения
# ---------------------------------------------------------------------------

def build_23() -> None:
    body = f"""
    <h2>Мини-проект — счётчик слов</h2>
    <p>Считаем, сколько слов в тексте и сколько раз встречается каждое — с помощью
    <code class="inline">split()</code> (раздел 8.10) и подсчёта в цикле (раздел 8.13):</p>
    {code_block(
        "schetchik_slov.py",
        'text = input("Введите предложение: ")\n'
        'words = text.lower().split()\n\n'
        'print(f"Всего слов: {len(words)}")\n\n'
        'schetchik = {}\n'
        'for word in words:\n'
        '    schetchik[word] = schetchik.get(word, 0) + 1\n\n'
        'for word, count in schetchik.items():\n'
        '    print(f"{word}: {count}")\n'
        '# ввод: "кот и пёс и кот"\n'
        '# Всего слов: 5\n'
        '# кот: 2\n'
        '# и: 2\n'
        '# пёс: 1\n',
    )}
    {callout(
        "info",
        "[[icon:launch]] Забегаем вперёд",
        "Словарь <code class=\"inline\">schetchik</code> — структура «слово → сколько раз "
        "встретилось», подробно разберём в главе 11. Сейчас достаточно понимать: "
        "<code class=\"inline\">.get(word, 0)</code> возвращает текущий счётчик слова (или 0, "
        "если слово встретилось впервые), а мы прибавляем к нему единицу.",
    )}

    <h2 id="cenzor">Мини-проект — чистка предложения (текстовый цензор)</h2>
    <p>Заменяем «запрещённые» слова звёздочками той же длины — используя
    <code class="inline">replace()</code> (раздел 8.10) и повторение строки
    (раздел 8.4):</p>
    {code_block(
        "cenzor.py",
        'text = input("Введите текст: ")\n'
        'zapreshchennye = ["плохое_слово", "секрет"]\n\n'
        'ochishchennyj = text\n'
        'for word in zapreshchennye:\n'
        '    zamena = "*" * len(word)\n'
        '    ochishchennyj = ochishchennyj.replace(word, zamena)\n\n'
        'print(ochishchennyj)\n'
        '# ввод: "это секрет, никому не говори"\n'
        '# это ******, никому не говори\n',
    )}

    {exercise(2, "Самое частое слово", "Расширьте счётчик слов: найдите слово с максимальным count и выведите его отдельной строкой «Самое частое слово: ...». Подсказка — переберите словарь schetchik.items() и запоминайте текущего лидера.")}

    {practice_card(
        "08-23",
        "Практика: счётчик слов и цензор текста",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-23/index.html",
    )}
    """
    out = render_page(
        page_title="Мини-проект: счётчик слов",
        description="Мини-проекты: счётчик слов в предложении и текстовый цензор, заменяющий запрещённые слова звёздочками.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Счётчик слов", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Мини-проект — счётчик слов и чистка предложения",
        lede="Считаем слова в тексте и учимся автоматически заменять нежелательные слова.",
        body_html=body,
        sidebar_groups=sidebar("08-23-mini-proekt-schetchik-slov.html"),
        nav=PageNav(prev_href="08-22-mini-proekt-parol-i-email.html", prev_label="Пароль и e-mail", next_href="08-10-mini-proekt-matematika-itogi.html", next_label="Динамическая математика и итоги"),
    )
    write("08-23-mini-proekt-schetchik-slov.html", out)


# ---------------------------------------------------------------------------
# 8.23 — Финальный мини-проект и итоги (существующий, обновляем итоги)
# ---------------------------------------------------------------------------

def build_10() -> None:
    body = f"""
    <p>Финальный мини-проект главы объединяет практически всё: ввод от пользователя, числа из
    глав 4–5, строки и Turtle из глав 6–7 — маленький «калькулятор с характером».</p>
    {code_block(
        "dinamicheskaya_matematika.py",
        "import turtle\n\n"
        "screen = turtle.Screen()\n"
        "artist = turtle.Turtle()\n"
        "artist.hideturtle()\n\n"
        'a = float(input(\"Первое число: \"))\n'
        'b = float(input(\"Второе число: \"))\n\n'
        "artist.penup()\n"
        "artist.goto(0, 60)\n"
        'artist.pencolor(\"purple\")\n'
        'artist.write(f\"{a} + {b} = {a + b}\", align=\"center\", font=(\"Arial\", 18, \"bold\"))\n\n'
        "artist.goto(0, 0)\n"
        'artist.pencolor(\"blue\")\n'
        'artist.write(f\"{a} * {b} = {a * b}\", align=\"center\", font=(\"Arial\", 18, \"bold\"))\n\n'
        "screen.exitonclick()\n",
    )}

    {exercise(3, "Ещё две операции", "Добавьте на холст ещё две строки: результат вычитания и деления — своим цветом для каждой.")}
{practice_card(
        "08-10",
        "Практика: динамическая математика (логика, без окна Turtle)",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-10/index.html",
    )}

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
        "Строки создают в одинарных, двойных или тройных кавычках; тройные сохраняют переносы "
        "строк, raw-строки (<code class=\"inline\">r\"...\"</code>) отключают экранирование.",
        "Служебные последовательности вроде <code class=\"inline\">\\n</code> и "
        "<code class=\"inline\">\\t</code> вставляют символы, у которых нет своей клавиши; "
        "<code class=\"inline\">repr()</code> показывает строку «как в коде».",
        "Символы строки доступны по индексу с нуля и по отрицательному индексу с конца — "
        "первый символ всегда имеет индекс 0.",
        "Срез <code class=\"inline\">[start:stop:step]</code> достаёт часть строки: "
        "<code class=\"inline\">start</code> включён, <code class=\"inline\">stop</code> — нет; "
        "<code class=\"inline\">[::-1]</code> разворачивает строку.",
        "Строки неизменяемы: методы вроде <code class=\"inline\">upper()</code> возвращают "
        "НОВУЮ строку, не трогая исходную.",
        "У строк десятки готовых методов — от регистра (<code class=\"inline\">upper()</code>, "
        "<code class=\"inline\">strip()</code>) до поиска и разбора (<code class=\"inline\">split()</code>, "
        "<code class=\"inline\">replace()</code>, <code class=\"inline\">find()</code>) и "
        "проверки состава (<code class=\"inline\">isdigit()</code>, <code class=\"inline\">isalpha()</code>).",
        "<code class=\"inline\">in</code> проверяет вхождение подстроки; строку можно "
        "перебрать циклом <code class=\"inline\">for ch in text</code>.",
        "f-строки — современный способ форматирования, с поддержкой выражений, точности и "
        "выравнивания; <code class=\"inline\">%</code> и <code class=\"inline\">.format()</code> "
        "— более старые, но всё ещё встречаются в реальном коде.",
        "<code class=\"inline\">input()</code> всегда возвращает строку — для чисел нужно "
        "явное преобразование <code class=\"inline\">int()</code>/<code class=\"inline\">float()</code>.",
        "Python одинаково хорошо работает с кириллицей, латиницей и эмодзи без специальной "
        "настройки.",
    ])}
    """
    out = render_page(
        page_title="Мини-проект — красочная и динамическая математика",
        description="Итоговый мини-проект главы 8: интерактивный калькулятор на Turtle — и краткие итоги главы про строки.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Динамическая математика", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Мини-проект — красочная и динамическая математика",
        lede="Собираем главу воедино: ввод пользователя, числа, строки и Turtle — в одном "
        "интерактивном мини-калькуляторе.",
        body_html=body,
        sidebar_groups=sidebar("08-10-mini-proekt-matematika-itogi.html"),
        nav=PageNav(prev_href="08-23-mini-proekt-schetchik-slov.html", prev_label="Счётчик слов", next_href="../glava-09/index.html", next_label="Глава 9: Выполняй мою команду!"),
    )
    write("08-10-mini-proekt-matematika-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01()
    build_11()
    build_12()
    build_02()
    build_13()
    build_03()
    build_14()
    build_15()
    build_04()
    build_16()
    build_17()
    build_05()
    build_18()
    build_06()
    build_07()
    build_19()
    build_20()
    build_08()
    build_21()
    build_09()
    build_22()
    build_23()
    build_10()
