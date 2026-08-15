#!/usr/bin/env python3
"""Строит Главу 4: «Python любит числа» (site/chapters/glava-04/)."""

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
OUT_DIR = ROOT / "site" / "chapters" / "glava-04"

PAGES = [
    ("index.html", "Приступаем"),
    ("04-01-chisla-i-peremennye.html", "Числа в Python, сохраняем числа"),
    ("04-02-kommentarii.html", "Комментарии"),
    ("04-03-vidy-chisel.html", "Числа бывают разных видов"),
    ("04-04-preobrazovanie-tipov.html", "Преобразование типов чисел"),
    ("04-05-mini-proekt-itogi.html", "Мини-проект и итоги"),
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 4 · Числа", items),
        SidebarGroup("Практика", [
            NavItem("🐍 04-01: Практика", "../../practice/04-01/index.html"),
            NavItem("🐍 04-03: Практика", "../../practice/04-03/index.html"),
            NavItem("🐍 04-04: Практика", "../../practice/04-04/index.html"),
            NavItem("🐍 04-05: Практика", "../../practice/04-05/index.html"),
        ]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=4,
        baseline_page=39,
        title="Python любит числа",
        description="Переменные, комментарии, три вида чисел и преобразование между ними.",
        meta_items=["⏱ ~1 час", "🔢 int, float, complex", "📓 4 ноутбука практики"],
        sections=[
            ChapterSectionLink("4.1", "Числа в Python", "04-01-chisla-i-peremennye.html", "39"),
            ChapterSectionLink("", "Сохраняем числа", "04-01-chisla-i-peremennye.html#sohranyaem", "40"),
            ChapterSectionLink("4.2", "Комментарии", "04-02-kommentarii.html", "46"),
            ChapterSectionLink("4.3", "Числа бывают разных видов", "04-03-vidy-chisel.html", "47"),
            ChapterSectionLink("", "Целые числа", "04-03-vidy-chisel.html#celye", "48"),
            ChapterSectionLink("", "Числа с плавающей точкой", "04-03-vidy-chisel.html#plavayuschie", "49"),
            ChapterSectionLink("", "Комплексные числа", "04-03-vidy-chisel.html#kompleksnye", "50"),
            ChapterSectionLink("4.4", "Преобразование типов чисел", "04-04-preobrazovanie-tipov.html", "53"),
            ChapterSectionLink("4.5", "Мини-проект — Понимаете ли вы числа?", "04-05-mini-proekt-itogi.html", "57"),
            ChapterSectionLink("", "Итоги", "04-05-mini-proekt-itogi.html#itogi", "58"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    cvm = classic_vs_modern(
        "Без подсказки типа → с подсказкой типа (Python 3.14)",
        "Классический подход",
        "age = 10\nprice = 19.99\nname = \"Cartesian\"\n"
        "# тип виден только по значению",
        "Современный Python 3.14",
        "age: int = 10\nprice: float = 19.99\nname: str = \"Cartesian\"\n"
        "# тип виден прямо в коде — подсказка (type hint)",
        "и то, и другое работает одинаково — подсказки типов не влияют на выполнение "
        "программы. В маленьких учебных примерах классический вариант проще и короче, поэтому "
        "в первых главах книги мы обычно пишем без подсказок. Но как только код вырастает, "
        "подсказки типов делают его понятнее — редакторы вроде VS Code и PyCharm используют "
        "их, чтобы подсвечивать ошибки ещё до запуска программы. Мы вернёмся к ним подробнее "
        "в главе 13.",
    )

    body = f"""
    <h2>Числа в Python</h2>
    <p>Числа — один из самых часто используемых видов данных в программировании: возраст, цена,
    счёт в игре, координаты на экране. Python умеет работать с числами «из коробки», без
    каких-либо дополнительных приготовлений.</p>
    {code_block("chisla.py", "print(7)\nprint(3.5)\nprint(7 + 3.5)\n")}

    <h2 id="sohranyaem">Сохраняем числа</h2>
    <p>Чтобы использовать число не один раз, а много, его удобно сохранить в
    <strong>переменную</strong> — именованную «коробку» в памяти компьютера. Значение
    записывают знаком <code class="inline">=</code>:</p>
    {code_block("peremennye.py", 'age = 10\nprint(age)\n\nage = 11  # значение можно заменить в любой момент\nprint(age)\n')}

    <h2>Правила именования переменных</h2>
    <ul>
      <li>Имя может содержать буквы, цифры и знак подчёркивания <code class="inline">_</code>,
        но не может <strong>начинаться</strong> с цифры.</li>
      <li>Python различает регистр: <code class="inline">age</code> и <code class="inline">Age</code>
        — разные переменные.</li>
      <li>Нельзя использовать зарезервированные слова языка — например,
        <code class="inline">for</code>, <code class="inline">if</code>,
        <code class="inline">print</code> лучше тоже не использовать как имя переменной, хотя
        формально это не ключевое слово.</li>
      <li>По соглашению имена переменных в Python пишут в стиле
        <code class="inline">snake_case</code>: словами через нижнее подчёркивание, например
        <code class="inline">user_age</code>, а не <code class="inline">userAge</code>.</li>
    </ul>

    {callout(
        "warning",
        "Частая ошибка новичков",
        "<code class=\"inline\">1_place = \"Cartesian\"</code> — SyntaxError: имя переменной не "
        "может начинаться с цифры. Решение: переставьте слова местами —"
        " <code class=\"inline\">place_1</code>.",
    )}

    {cvm}

    {practice_card(
        "04-01",
        "Практика: переменные и первые числа",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/04-01/index.html",
    )}
    """

    out = render_page(
        page_title="Числа в Python, сохраняем числа",
        description="Работа с числами и переменными в Python: присваивание, правила именования, подсказки типов.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Числа и переменные", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Числа в Python",
        lede="Числа — самый естественный вид данных для компьютера. Разберёмся, как их сохранять "
        "в переменные и как их правильно называть.",
        body_html=body,
        sidebar_groups=sidebar("04-01-chisla-i-peremennye.html"),
        nav=PageNav(prev_href="index.html", prev_label="Приступаем", next_href="04-02-kommentarii.html", next_label="Комментарии"),
    )
    write("04-01-chisla-i-peremennye.html", out)


def build_02() -> None:
    body = f"""
    <p><strong>Комментарий</strong> — это текст в коде, который Python полностью игнорирует при
    выполнении. Он нужен не компьютеру, а человеку: объяснить, зачем нужна эта строка, оставить
    напоминание себе или коллеге.</p>
    {code_block("kommentarii.py", '# Это комментарий — Python его не выполняет\nage = 10  # а это комментарий в конце строки\nprint(age)\n')}
    <p>Комментарий начинается со знака <code class="inline">#</code> и продолжается до конца
    строки.</p>

    {callout(
        "tip",
        "Хороший комментарий объясняет «почему», а не «что»",
        "Строка <code class=\"inline\">age = 10  # присваиваем age значение 10</code> — "
        "бесполезный комментарий: и так понятно из кода. А "
        "<code class=\"inline\">age = 10  # минимальный возраст по умолчанию</code> "
        "объясняет то, чего в самом коде не видно.",
    )}

    <p>В этой книге мы придерживаемся именно такого стиля: комментарии на русском языке
    объясняют идею, а не пересказывают код построчно.</p>
    """

    out = render_page(
        page_title="Комментарии",
        description="Зачем нужны комментарии в коде и как писать хорошие комментарии.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Комментарии", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Комментарии",
        lede="Текст в коде, который читает только человек — компьютер его полностью пропускает.",
        body_html=body,
        sidebar_groups=sidebar("04-02-kommentarii.html"),
        nav=PageNav(prev_href="04-01-chisla-i-peremennye.html", prev_label="Числа и переменные", next_href="04-03-vidy-chisel.html", next_label="Числа бывают разных видов"),
    )
    write("04-02-kommentarii.html", out)


def build_03() -> None:
    body = f"""
    <p>В Python есть несколько встроенных видов («типов») чисел. Три основных вы встретите чаще
    всего:</p>

    <h2 id="celye">Целые числа</h2>
    <p>Тип <code class="inline">int</code> (от <em>integer</em>) — числа без дробной части:
    <code class="inline">-3, 0, 42, 1000000</code>. В Python размер целого числа практически не
    ограничен — можно работать даже с числами из сотен цифр.</p>
    {code_block("celye.py", "big = 10 ** 20\nprint(big)\nprint(type(big))\n")}

    <h2 id="plavayuschie">Числа с плавающей точкой</h2>
    <p>Тип <code class="inline">float</code> — числа с дробной частью:
    <code class="inline">3.14, -0.5, 2.0</code>. Даже если дробная часть равна нулю, точка делает
    число <code class="inline">float</code>, а не <code class="inline">int</code>.</p>
    {code_block("plavayuschie.py", "pi = 3.14\nprint(type(pi))\n\nwhole = 2.0\nprint(type(whole))  # float, несмотря на нулевую дробную часть\n")}

    {callout(
        "info",
        "Деление всегда даёт float",
        "Оператор <code class=\"inline\">/</code> в Python всегда возвращает "
        "<code class=\"inline\">float</code>, даже если числа делятся нацело: "
        "<code class=\"inline\">10 / 2</code> равно <code class=\"inline\">5.0</code>, а не "
        "<code class=\"inline\">5</code>. Мы уже видели это в главе 3.",
    )}

    <h2 id="kompleksnye">Комплексные числа</h2>
    <p>Тип <code class="inline">complex</code> — числа вида «действительная часть + мнимая
    часть», где мнимая часть отмечена буквой <code class="inline">j</code>. Такие числа нужны
    в основном в инженерных и научных расчётах (например, при обработке сигналов) — в
    большинстве обычных программ вы их не встретите, но полезно знать, что Python поддерживает
    их «из коробки».</p>
    {code_block("kompleksnye.py", "z = 3 + 4j\nprint(z)\nprint(type(z))\nprint(z.real, z.imag)\n")}

    {practice_card(
        "04-03",
        "Практика: int, float и complex на практике",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/04-03/index.html",
    )}
    """

    out = render_page(
        page_title="Числа бывают разных видов",
        description="Три числовых типа Python: int, float и complex.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Числа бывают разных видов", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Числа бывают разных видов",
        lede="Python различает целые числа, числа с плавающей точкой и комплексные числа — и "
        "у каждого вида свои особенности.",
        body_html=body,
        sidebar_groups=sidebar("04-03-vidy-chisel.html"),
        nav=PageNav(prev_href="04-02-kommentarii.html", prev_label="Комментарии", next_href="04-04-preobrazovanie-tipov.html", next_label="Преобразование типов чисел"),
    )
    write("04-03-vidy-chisel.html", out)


def build_04() -> None:
    cvm = classic_vs_modern(
        "Сборка строки из чисел: конкатенация → f-строка",
        "Классический подход",
        'age = 10\nmessage = "Возраст: " + str(age) + " лет"\nprint(message)\n'
        "# обязательно вручную оборачивать число в str()",
        "Современный Python 3.14",
        'age = 10\nmessage = f"Возраст: {age} лет"\nprint(message)\n'
        "# f-строка сама выполняет преобразование внутри {}",
        "f-строки (f-strings), появившиеся в Python 3.6 и с тех пор ставшие стандартом. Они "
        "короче, меньше подвержены ошибкам (не нужно помнить о str()) и позволяют сразу писать "
        "выражения внутри фигурных скобок. Классический способ через + всё ещё встречается в "
        "старом коде и стоит уметь его читать, но для нового кода используйте f-строки.",
    )

    body = f"""
    <p>У каждого числового типа есть своя функция-преобразователь с тем же именем:
    <code class="inline">int()</code>, <code class="inline">float()</code>,
    <code class="inline">complex()</code>. Кроме того, любое число можно превратить в текст
    функцией <code class="inline">str()</code> — и наоборот, текст, похожий на число, можно
    превратить обратно.</p>

    {code_block("preobrazovanie.py", 'whole = int(3.99)\nprint(whole)      # 3 — дробная часть отбрасывается, а не округляется\n\ndecimal = float(7)\nprint(decimal)    # 7.0\n\ntext = str(42)\nprint(text, type(text))   # "42" <class \'str\'>\n')}

    {callout(
        "warning",
        "int() не округляет, а отбрасывает дробную часть",
        "<code class=\"inline\">int(3.99)</code> равно <code class=\"inline\">3</code>, а не "
        "<code class=\"inline\">4</code>. Для настоящего округления нужна отдельная функция "
        "<code class=\"inline\">round()</code> — о ней в главе 5.",
    )}

    <h2>Преобразование текста в число</h2>
    <p>Если строка действительно выглядит как число, её можно превратить обратно:</p>
    {code_block("tekst_v_chislo.py", 'age_text = "10"\nage = int(age_text)\nprint(age + 5)   # 15 — теперь это настоящее число\n')}

    {callout(
        "warning",
        "Не любой текст получится преобразовать",
        "<code class=\"inline\">int(\"десять\")</code> вызовет <code class=\"inline\">ValueError</code> "
        "— Python не умеет читать числа словами. Преобразовать можно только текст, который "
        "выглядит как число: цифры, возможно со знаком и точкой.",
    )}

    {cvm}

    {practice_card(
        "04-04",
        "Практика: int(), float(), str() на практике",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/04-04/index.html",
    )}
    """

    out = render_page(
        page_title="Преобразование типов чисел",
        description="int(), float(), str() и типичные ошибки при преобразовании типов в Python.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Преобразование типов чисел", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Преобразование типов чисел",
        lede="Числа можно превращать друг в друга и в текст — но не всегда наоборот, и не "
        "всегда так, как кажется на первый взгляд.",
        body_html=body,
        sidebar_groups=sidebar("04-04-preobrazovanie-tipov.html"),
        nav=PageNav(prev_href="04-03-vidy-chisel.html", prev_label="Числа бывают разных видов", next_href="04-05-mini-proekt-itogi.html", next_label="Мини-проект и итоги"),
    )
    write("04-04-preobrazovanie-tipov.html", out)


def build_05() -> None:
    body = f"""
    <p>Проверим, насколько хорошо вы понимаете числа в Python — без запуска кода, только
    рассуждением. Ответы — в ноутбуке практики.</p>

    {exercise(
        1,
        "Угадайте тип",
        "Определите тип каждого значения, не запуская код: "
        "<code class=\"inline\">10</code>, <code class=\"inline\">10.0</code>, "
        "<code class=\"inline\">10 / 2</code>, <code class=\"inline\">10 // 2</code>, "
        "<code class=\"inline\">\"10\"</code>.",
    )}
    {exercise(
        2,
        "Угадайте результат",
        "Что выведет <code class=\"inline\">print(int(7.9))</code>? А "
        "<code class=\"inline\">print(str(7) + str(9))</code> — одно число 16 или что-то "
        "другое?",
    )}
    {exercise(
        3,
        "Найдите ошибку",
        "Строка <code class=\"inline\">total = \"Итого: \" + 100</code> вызывает "
        "<code class=\"inline\">TypeError</code>. Почему, и как её исправить двумя разными "
        "способами (через <code class=\"inline\">str()</code> и через f-строку)?",
    )}

    {practice_card(
        "04-05",
        "Практика: понимаете ли вы числа?",
        "Интерактивный ноутбук прямо в браузере — сверьте свои ответы запуском кода",
        "../../practice/04-05/index.html",
    )}

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
        "Числа сохраняют в <strong>переменных</strong> знаком <code class=\"inline\">=</code>; "
        "имена переменных пишут в стиле <code class=\"inline\">snake_case</code> и не начинают "
        "с цифры.",
        "<code class=\"inline\"># комментарий</code> — текст, который Python игнорирует; он "
        "объясняет код человеку.",
        "Три числовых типа: <code class=\"inline\">int</code> (целые), "
        "<code class=\"inline\">float</code> (дробные), <code class=\"inline\">complex</code> "
        "(комплексные, для науки и инженерии).",
        "<code class=\"inline\">int()</code>, <code class=\"inline\">float()</code>, "
        "<code class=\"inline\">str()</code> преобразуют значения между типами — но "
        "<code class=\"inline\">int()</code> отбрасывает дробную часть, а не округляет.",
        "f-строки (<code class=\"inline\">f\"...{значение}\"</code>) — современный и самый "
        "удобный способ вставлять числа в текст.",
    ])}
    """

    out = render_page(
        page_title="Мини-проект — Понимаете ли вы числа?",
        description="Итоговая практика и резюме главы 4 — числа, переменные и типы в Python.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 4", "index.html"), ("Мини-проект и итоги", "")],
        kicker="Глава 4 · Python любит числа",
        h1="Мини-проект — Понимаете ли вы числа?",
        lede="Небольшая проверка понимания — без единого запуска кода, только рассуждением — и "
        "краткие итоги главы.",
        body_html=body,
        sidebar_groups=sidebar("04-05-mini-proekt-itogi.html"),
        nav=PageNav(prev_href="04-04-preobrazovanie-tipov.html", prev_label="Преобразование типов чисел", next_href="../glava-05/index.html", next_label="Глава 5: Давайте поиграем с числами!"),
    )
    write("04-05-mini-proekt-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01()
    build_02()
    build_03()
    build_04()
    build_05()
