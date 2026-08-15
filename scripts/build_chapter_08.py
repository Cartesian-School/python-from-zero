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
    practice_card,
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-08"

PAGES = [
    ("index.html", "Обзор главы"),
    ("08-01-chto-takoe-stroki.html", "Что такое строки?"),
    ("08-02-kavychki-konkatenaciya.html", "Кавычки и объединение строк"),
    ("08-03-dostup-k-simvolam.html", "Доступ к символам и срезы"),
    ("08-04-metody-strok.html", "Методы строк"),
    ("08-05-istina-lozh.html", "Истина? Ложь?"),
    ("08-06-formatirovanie-strok.html", "Форматирование строк"),
    ("08-07-vvod-polzovatelya.html", "Ввод от пользователя"),
    ("08-08-mini-proekt-turtle-tekst.html", "Мини-проект: текст Turtle"),
    ("08-09-mini-proekty-krik-perevorot.html", "Мини-проекты: крик и переворот имени"),
    ("08-10-mini-proekt-matematika-itogi.html", "Мини-проект: динамическая математика и итоги"),
]

LESSON_IDS = ["08-01", "08-03", "08-04", "08-06", "08-07", "08-09", "08-10"]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 8 · Строки", items),
        SidebarGroup("Практика", [
            NavItem(f"🐍 {lid}: Практика", f"../../practice/{lid}/index.html") for lid in LESSON_IDS
        ]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=8,
        baseline_page=137,
        title="Играем с буквами и словами",
        description="Строки в Python: создание, индексы и срезы, методы, форматирование, ввод от пользователя.",
        meta_items=["⏱ ~3 часа", "🔤 str и его методы", "📓 7 ноутбуков практики"],
        sections=[
            ChapterSectionLink("8.1", "Что такое строки?", "08-01-chto-takoe-stroki.html", "137"),
            ChapterSectionLink("8.2", "В моей строке есть кавычки!", "08-02-kavychki-konkatenaciya.html", "141"),
            ChapterSectionLink("8.3", "Доступ к символам строки", "08-03-dostup-k-simvolam.html", "145"),
            ChapterSectionLink("8.4", "Методы строк — магия работы со строками!", "08-04-metody-strok.html", "149"),
            ChapterSectionLink("8.5", "Истина? Ложь?", "08-05-istina-lozh.html", "155"),
            ChapterSectionLink("8.6", "Форматирование строк", "08-06-formatirovanie-strok.html", "157"),
            ChapterSectionLink("8.7", "Получение ввода от пользователей", "08-07-vvod-polzovatelya.html", "161"),
            ChapterSectionLink("8.8", "Мини-проект — текст Turtle на новый уровень", "08-08-mini-proekt-turtle-tekst.html", "164"),
            ChapterSectionLink("8.9", "Мини-проект — кричим на экран", "08-09-mini-proekty-krik-perevorot.html", "166"),
            ChapterSectionLink("", "Мини-проект — переворачиваем своё имя", "08-09-mini-proekty-krik-perevorot.html#perevorot", "169"),
            ChapterSectionLink("8.10", "Мини-проект — динамическая математика", "08-10-mini-proekt-matematika-itogi.html", "171"),
            ChapterSectionLink("", "Итоги", "08-10-mini-proekt-matematika-itogi.html#itogi", "174"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <h2>Что такое строки?</h2>
    <p><strong>Строка</strong> (<code class="inline">str</code>) — это текст: последовательность
    символов — букв, цифр, знаков препинания, пробелов — заключённая в кавычки. Мы уже
    пользовались строками с самой первой программы в главе 1, теперь разберём их подробно.</p>

    <h2>Создаём строки</h2>
    {code_block("sozdaem_stroki.py", "greeting = \"Привет\"\nname = 'Cartesian'\nprint(greeting, name)\n")}
    <p>Одинарные и двойные кавычки в Python равнозначны — выбирайте любые, главное быть
    последовательным в рамках одной строки.</p>

    <h2>Хочу много-много строк!</h2>
    <p>Если текст должен занимать несколько строк, используют <strong>тройные кавычки</strong>
    — тогда переносы строк внутри текста сохраняются как есть:</p>
    {code_block("mnogo_strok.py", 'poem = """Код за кодом,\nшаг за шагом —\nтак рождается\nпрограмма."""\nprint(poem)\n')}

    {practice_card(
        "08-01",
        "Практика: создание строк и многострочный текст",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-01/index.html",
    )}
    """
    out = render_page(
        page_title="Что такое строки?",
        description="Введение в строки Python: создание, одинарные/двойные и тройные кавычки.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Что такое строки?", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Что такое строки?",
        lede="Текст в Python — это строки. Разберёмся, как их создавать: в одну строку и в "
        "несколько сразу.",
        body_html=body,
        sidebar_groups=sidebar("08-01-chto-takoe-stroki.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="08-02-kavychki-konkatenaciya.html", next_label="Кавычки и объединение строк"),
    )
    write("08-01-chto-takoe-stroki.html", out)


def build_02() -> None:
    body = f"""
    <h2>В моей строке есть кавычки! :O</h2>
    <p>Что делать, если внутри текста нужна кавычка того же типа, что обрамляет строку? Самый
    простой способ — обрамить строку кавычками <strong>другого</strong> типа:</p>
    {code_block("kavychki.py", "quote = \"Она сказала: 'Привет!'\"\nquote2 = 'Она сказала: \"Привет!\"'\nprint(quote)\nprint(quote2)\n")}
    <p>Если нужны именно такие же кавычки, как обрамляющие, — их экранируют обратной косой
    чертой <code class="inline">\\</code>:</p>
    {code_block("ekranirovanie.py", 'quote = "Она сказала: \\"Привет!\\""\nprint(quote)\n')}

    <h2>Объединяем две или несколько строк</h2>
    <p>Строки, как и числа, можно складывать оператором <code class="inline">+</code> —
    это называется <strong>конкатенацией</strong>:</p>
    {code_block("konkatenaciya.py", 'first_name = "Ада"\nlast_name = "Лавлейс"\nfull_name = first_name + " " + last_name\nprint(full_name)\n')}

    {callout(
        "warning",
        "Строку с числом напрямую не сложить",
        "<code class=\"inline\">\"Возраст: \" + 10</code> вызовет <code class=\"inline\">TypeError"
        "</code> — мы уже видели это в главе 4. Нужно либо <code class=\"inline\">str(10)</code>, "
        "либо f-строка (раздел 8.6).",
    )}

    <h2>Конкатенация в print()</h2>
    <p>Напомним: у <code class="inline">print()</code> есть более простой способ вывести
    несколько значений — через запятую, без явного <code class="inline">+</code> (мы делали это в
    главе 3):</p>
    {code_block("print_konkatenaciya.py", 'print(first_name, last_name)          # через запятую — сам добавит пробел\nprint(first_name + " " + last_name)   # через + — нужно добавлять пробел самому\n')}

    <h2>Пустая строка</h2>
    <p>Строка может не содержать ни одного символа — это тоже допустимая, «пустая» строка
    <code class="inline">""</code>. Она отличается от отсутствия значения и часто используется
    как стартовое значение перед накоплением текста.</p>

    {practice_card(
        "08-01",
        "Практика: кавычки и конкатенация",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-01/index.html",
    )}
    """
    out = render_page(
        page_title="В моей строке есть кавычки!",
        description="Экранирование кавычек, конкатенация строк оператором + и пустая строка.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Кавычки и объединение", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="В моей строке есть кавычки! :O",
        lede="Что делать с кавычками внутри строки — и как объединять несколько строк в одну.",
        body_html=body,
        sidebar_groups=sidebar("08-02-kavychki-konkatenaciya.html"),
        nav=PageNav(prev_href="08-01-chto-takoe-stroki.html", prev_label="Что такое строки?", next_href="08-03-dostup-k-simvolam.html", next_label="Доступ к символам и срезы"),
    )
    write("08-02-kavychki-konkatenaciya.html", out)


def build_03() -> None:
    body = f"""
    <h2>Доступ к символам строки</h2>
    <p>Строка — это последовательность символов, и к каждому символу можно обратиться по его
    <strong>индексу</strong> (порядковому номеру) в квадратных скобках. Индексация в Python
    начинается с <strong>нуля</strong>:</p>
    {code_block("indeksy.py", 'word = "Python"\nprint(word[0])   # P — первый символ\nprint(word[1])   # y — второй символ\nprint(word[5])   # n — шестой (и последний) символ\n')}

    <h2>Отрицательные индексы</h2>
    <p>Отрицательные индексы отсчитываются с конца строки — <code class="inline">-1</code>
    означает «последний символ»:</p>
    {code_block("otricatelnye_indeksy.py", 'word = "Python"\nprint(word[-1])   # n — последний символ\nprint(word[-2])   # o — предпоследний\n')}

    {callout(
        "warning",
        "IndexError — индекс за пределами строки",
        "<code class=\"inline\">word[10]</code> для шестибуквенного слова вызовет "
        "<code class=\"inline\">IndexError: string index out of range</code>. Индексы "
        "существуют только от <code class=\"inline\">0</code> до "
        "<code class=\"inline\">len(word) - 1</code> (и от -1 до -len(word) с конца).",
    )}

    <h2>Получение среза строки</h2>
    <p><strong>Срез</strong> (slice) возвращает часть строки — от одного индекса до другого
    (не включая последний):</p>
    {code_block("srezy.py", 'word = "Python"\nprint(word[0:3])   # Pyt — символы с индексами 0, 1, 2\nprint(word[2:])    # thon — от индекса 2 и до конца\nprint(word[:3])    # Pyt — от начала до индекса 3 (не включая)\nprint(word[::-1])  # nohtyP — весь текст задом наперёд!\n')}

    {callout(
        "tip",
        "Разворот строки одним срезом",
        "<code class=\"inline\">строка[::-1]</code> — самый короткий способ развернуть строку "
        "задом наперёд. Третий параметр среза — «шаг»; шаг -1 проходит строку в обратном "
        "порядке. Мы воспользуемся этим в мини-проекте 8.9.",
    )}

    {practice_card(
        "08-03",
        "Практика: индексы, отрицательные индексы и срезы",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-03/index.html",
    )}
    """
    out = render_page(
        page_title="Доступ к символам строки",
        description="Индексы, отрицательные индексы и срезы строк в Python.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Символы и срезы", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Доступ к символам строки",
        lede="Каждый символ строки можно достать по номеру — а срезы позволяют достать сразу "
        "целый кусок.",
        body_html=body,
        sidebar_groups=sidebar("08-03-dostup-k-simvolam.html"),
        nav=PageNav(prev_href="08-02-kavychki-konkatenaciya.html", prev_label="Кавычки и объединение", next_href="08-04-metody-strok.html", next_label="Методы строк"),
    )
    write("08-03-dostup-k-simvolam.html", out)


def build_04() -> None:
    body = f"""
    <p>У каждой строки в Python есть встроенные <strong>методы</strong> — готовые действия,
    которые можно выполнить над ней через точку: <code class="inline">строка.метод()</code>.</p>

    <h2>Верхний и нижний регистр</h2>
    {code_block("registr.py", 'text = "Python с нуля"\nprint(text.upper())   # ПРОГРАММИРОВАНИЕ КАПСОМ\nprint(text.lower())   # питон с нуля\nprint(text.title())   # Python С Нуля — Первая Буква Каждого Слова\n')}

    <h2>Разные методы</h2>
    {code_block(
        "raznye_metody.py",
        'text = "  Python с нуля  "\n'
        "print(text.strip())              # убирает пробелы по краям\n"
        'print(text.replace("нуля", "начала"))  # замена подстроки\n'
        'print(text.count("н"))            # сколько раз встречается символ\n'
        'print("Python".startswith("Py"))  # True\n'
        'print("Python".endswith("on"))    # True\n'
        'print(text.split())               # разбивает строку на список слов\n',
    )}

    {callout(
        "info",
        "Методы строк не меняют исходную строку",
        "Строки в Python <strong>неизменяемы</strong> — <code class=\"inline\">text.upper()</code> "
        "возвращает <em>новую</em> строку, а исходная переменная <code class=\"inline\">text"
        "</code> остаётся прежней, если не переприсвоить: <code class=\"inline\">text = text.upper()</code>.",
    )}

    {practice_card(
        "08-04",
        "Практика: методы строк",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-04/index.html",
    )}
    """
    out = render_page(
        page_title="Методы строк — магия работы со строками!",
        description="Встроенные методы строк Python: upper, lower, strip, replace, count, split и другие.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Методы строк", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Методы строк — магия работы со строками!",
        lede="Готовые действия над строками, вызываемые через точку — от смены регистра до "
        "разбиения на слова.",
        body_html=body,
        sidebar_groups=sidebar("08-04-metody-strok.html"),
        nav=PageNav(prev_href="08-03-dostup-k-simvolam.html", prev_label="Символы и срезы", next_href="08-05-istina-lozh.html", next_label="Истина? Ложь?"),
    )
    write("08-04-metody-strok.html", out)


def build_05() -> None:
    body = f"""
    <p>Строки можно сравнивать друг с другом и проверять, содержится ли одна строка внутри
    другой — результатом всегда будет <code class="inline">True</code> или
    <code class="inline">False</code>.</p>

    {code_block(
        "istina_lozh.py",
        'print("Python" == "Python")     # True — строки совпадают полностью\n'
        'print("Python" == "python")     # False — регистр важен\n'
        'print("thon" in "Python")       # True — "thon" встречается внутри "Python"\n'
        'print("java" in "Python")       # False\n',
    )}

    {callout(
        "warning",
        "== сравнивает значение, is сравнивает объект",
        "Для строк почти всегда нужен именно <code class=\"inline\">==</code>. Оператор "
        "<code class=\"inline\">is</code> проверяет, один ли это объект в памяти, — гораздо "
        "более редкий и специфичный случай, к которому мы вернёмся в главе 14.",
    )}

    <h2>Пустая строка — это «ложь»</h2>
    <p>В логических проверках (например, <code class="inline">if</code> — подробно в главе 9)
    пустая строка ведёт себя как <code class="inline">False</code>, а любая непустая строка —
    как <code class="inline">True</code>:</p>
    {code_block("pustaya_stroka_logika.py", 'print(bool(""))         # False\nprint(bool("Python"))   # True\nprint(bool(" "))        # True — пробел — это тоже символ!\n')}

    {practice_card(
        "08-03",
        "Практика: сравнение строк и in",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-03/index.html",
    )}
    """
    out = render_page(
        page_title="Истина? Ложь?",
        description="Сравнение строк, оператор in и логическое значение (истинность) строк.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Истина? Ложь?", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Истина? Ложь?",
        lede="Сравниваем строки друг с другом и проверяем, входит ли одна строка в другую.",
        body_html=body,
        sidebar_groups=sidebar("08-05-istina-lozh.html"),
        nav=PageNav(prev_href="08-04-metody-strok.html", prev_label="Методы строк", next_href="08-06-formatirovanie-strok.html", next_label="Форматирование строк"),
    )
    write("08-05-istina-lozh.html", out)


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
    полностью, включая исторический контекст: в старом коде вы неизбежно встретите и другие
    способы.</p>

    {cvm}

    <h2>Форматирование чисел внутри f-строк</h2>
    <p>Внутри фигурных скобок f-строки можно не только подставить значение, но и указать, как
    именно его отформатировать — например, сколько знаков после запятой:</p>
    {code_block("format_specifikatory.py", 'pi = 3.14159265\nprint(f"Пи округлённо: {pi:.2f}")   # Пи округлённо: 3.14\nprint(f"{1234567:,}")               # 1,234,567 — разделитель тысяч\n')}

    {practice_card(
        "08-06",
        "Практика: %, .format() и f-строки",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/08-06/index.html",
    )}
    """
    out = render_page(
        page_title="Форматирование строк",
        description="Три способа форматирования строк в Python: %, .format() и современные f-строки.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Форматирование строк", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Форматирование строк",
        lede="Три поколения одного и того же инструмента — вставить значение внутрь текста.",
        body_html=body,
        sidebar_groups=sidebar("08-06-formatirovanie-strok.html"),
        nav=PageNav(prev_href="08-05-istina-lozh.html", prev_label="Истина? Ложь?", next_href="08-07-vvod-polzovatelya.html", next_label="Ввод от пользователя"),
    )
    write("08-06-formatirovanie-strok.html", out)


def build_07() -> None:
    body = f"""
    <p>До сих пор все данные в программах были «зашиты» прямо в код. Пора научиться получать
    данные от самого пользователя во время выполнения программы — с этого момента ваши программы
    становятся по-настоящему интерактивными.</p>

    {code_block("vvod.py", 'name = input("Как вас зовут? ")\nprint(f"Привет, {name}!")\n')}
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

    <h2>Преобразование строки в int или float</h2>
    <p><code class="inline">input()</code> <strong>всегда</strong> возвращает строку — даже
    если пользователь ввёл число. Чтобы посчитать что-то с этим значением, его нужно
    преобразовать (как мы делали в главе 4):</p>
    {code_block("vvod_chisla.py", 'age_text = input("Сколько вам лет? ")\nage = int(age_text)\nprint(f"Через 5 лет вам будет {age + 5}.")\n')}

    {callout(
        "warning",
        "Частая ошибка новичков",
        "Если забыть про <code class=\"inline\">int()</code> и написать "
        "<code class=\"inline\">age + 5</code>, где <code class=\"inline\">age</code> — строка "
        "из <code class=\"inline\">input()</code>, Python выдаст <code class=\"inline\">TypeError"
        "</code>: складывать строку и число напрямую нельзя.",
    )}

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
        nav=PageNav(prev_href="08-06-formatirovanie-strok.html", prev_label="Форматирование строк", next_href="08-08-mini-proekt-turtle-tekst.html", next_label="Мини-проект: текст Turtle"),
    )
    write("08-07-vvod-polzovatelya.html", out)


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
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
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
        lede="Объединяем input() из предыдущего раздела с write() из главы 7 — персональное "
        "приветствие прямо на холсте.",
        body_html=body,
        sidebar_groups=sidebar("08-08-mini-proekt-turtle-tekst.html"),
        nav=PageNav(prev_href="08-07-vvod-polzovatelya.html", prev_label="Ввод от пользователя", next_href="08-09-mini-proekty-krik-perevorot.html", next_label="Мини-проекты: крик и переворот"),
    )
    write("08-08-mini-proekt-turtle-tekst.html", out)


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
    <p>Используем срез <code class="inline">[::-1]</code> из раздела 8.3, чтобы развернуть
    введённое имя задом наперёд:</p>
    {code_block(
        "perevorot_imeni.py",
        'name = input("Как вас зовут? ")\n'
        "perevernutoe = name[::-1]\n"
        'print(f"Ваше имя задом наперёд: {perevernutoe}")\n',
    )}

    {exercise(1, "Крик с ограничением", "Измените krik.py так, чтобы восклицательных знаков было столько же, сколько букв во фразе (подсказка: умножение строки на число — str * n — повторяет её n раз).")}
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
        nav=PageNav(prev_href="08-08-mini-proekt-turtle-tekst.html", prev_label="Текст Turtle", next_href="08-10-mini-proekt-matematika-itogi.html", next_label="Динамическая математика и итоги"),
    )
    write("08-09-mini-proekty-krik-perevorot.html", out)


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
        "строк.",
        "Оператор <code class=\"inline\">+</code> объединяет строки (конкатенация); "
        "<code class=\"inline\">print(a, b)</code> — более простая альтернатива для вывода.",
        "Символы строки доступны по индексу (с нуля) и отрицательному индексу (с конца); срез "
        "<code class=\"inline\">[a:b]</code> достаёт часть строки, <code class=\"inline\">[::-1]"
        "</code> — разворачивает её.",
        "У строк десятки готовых методов: <code class=\"inline\">upper()</code>, "
        "<code class=\"inline\">lower()</code>, <code class=\"inline\">strip()</code>, "
        "<code class=\"inline\">replace()</code>, <code class=\"inline\">split()</code> и "
        "другие — все они возвращают новую строку, не меняя исходную.",
        "f-строки — современный способ форматирования; <code class=\"inline\">%</code> и "
        "<code class=\"inline\">.format()</code> — более старые, но всё ещё встречаются.",
        "<code class=\"inline\">input()</code> всегда возвращает строку — для чисел нужно "
        "явное преобразование <code class=\"inline\">int()</code>/<code class=\"inline\">float()</code>.",
    ])}
    """
    out = render_page(
        page_title="Мини-проект — красочная и динамическая математика",
        description="Итоговый мини-проект главы 8: интерактивный калькулятор на Turtle — и краткие итоги.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 8", "index.html"), ("Динамическая математика", "")],
        kicker="Глава 8 · Играем с буквами и словами",
        h1="Мини-проект — красочная и динамическая математика",
        lede="Собираем главу воедино: ввод пользователя, числа, строки и Turtle — в одном "
        "интерактивном мини-калькуляторе.",
        body_html=body,
        sidebar_groups=sidebar("08-10-mini-proekt-matematika-itogi.html"),
        nav=PageNav(prev_href="08-09-mini-proekty-krik-perevorot.html", prev_label="Крик и переворот", next_href="../glava-09/index.html", next_label="Глава 9: Выполняй мою команду!"),
    )
    write("08-10-mini-proekt-matematika-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
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
