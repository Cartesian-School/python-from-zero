#!/usr/bin/env python3
"""Строит Главу 13: «Автоматизация с помощью функций» (site/chapters/glava-13/)."""

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
    notebook_card,
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-13"

PAGES = [
    ("index.html", "Обзор главы"),
    ("13-01-nastoyashaya-avtomatizaciya.html", "Настоящая автоматизация. Первая функция"),
    ("13-02-zachem-funkcii.html", "Зачем нужны функции?"),
    ("13-03-vozvrashaem-otvet.html", "Возвращаем ответ"),
    ("13-04-argumenty.html", "Аргументы функций"),
    ("13-05-globalnye-lokalnye.html", "Глобальные и локальные переменные"),
    ("13-06-lambda.html", "Лямбда-функции"),
    ("13-07-mini-proekt-domashka.html", "Мини-проект: домашнее задание по математике"),
    ("13-08-mini-proekt-figury-itogi.html", "Мини-проект: автоматизированные фигуры и итоги"),
]

NOTEBOOKS = [
    "13-01-pervaya-funkciya.ipynb",
    "13-02-zachem-funkcii.ipynb",
    "13-03-vozvrat.ipynb",
    "13-04-argumenty.ipynb",
    "13-05-oblast-vidimosti.ipynb",
    "13-06-lambda.ipynb",
    "13-07-domashka.ipynb",
    "13-08-figury-novyj-uroven.ipynb",
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 13 · Функции", items),
        SidebarGroup("Практика", [NavItem(f"📓 {n}", f"../../../notebooks/chapter-13/{n}") for n in NOTEBOOKS]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=13,
        baseline_page=283,
        title="Автоматизация с помощью функций",
        description="Определение функций, аргументы, return, область видимости переменных и лямбда-функции.",
        meta_items=["⏱ ~3 часа", "🧩 def и return", "📓 8 ноутбуков практики"],
        sections=[
            ChapterSectionLink("13.1", "Настоящая автоматизация. Наша первая функция", "13-01-nastoyashaya-avtomatizaciya.html", "283"),
            ChapterSectionLink("13.2", "Зачем нужны функции?", "13-02-zachem-funkcii.html", "286"),
            ChapterSectionLink("13.3", "Возвращаем ответ", "13-03-vozvrashaem-otvet.html", "292"),
            ChapterSectionLink("13.4", "Нет аргументов? Слишком много аргументов!", "13-04-argumenty.html", "295"),
            ChapterSectionLink("13.5", "Глобальные и локальные переменные", "13-05-globalnye-lokalnye.html", "297"),
            ChapterSectionLink("13.6", "Лямбда-функции", "13-06-lambda.html", "301"),
            ChapterSectionLink("13.7", "Мини-проект — домашнее задание по математике", "13-07-mini-proekt-domashka.html", "302"),
            ChapterSectionLink("13.8", "Мини-проект — автоматизированные фигуры: новый уровень", "13-08-mini-proekt-figury-itogi.html", "306"),
            ChapterSectionLink("", "Итоги", "13-08-mini-proekt-figury-itogi.html#itogi", "309"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <h2>Настоящая автоматизация</h2>
    <p>Циклы из главы 10 автоматизировали повторение одного и того же кода. Но что если один и
    тот же <em>набор действий</em> нужен в разных местах программы — не подряд, а время от
    времени? Копировать код каждый раз — плохая идея: любое исправление придётся вносить
    во все копии. <strong>Функции</strong> решают эту проблему раз и навсегда.</p>

    <h2>Наша первая функция</h2>
    {code_block(
        "pervaya_funkciya.py",
        "def privetstvie():\n"
        '    print("Привет, Python!")\n\n'
        "privetstvie()\n"
        "privetstvie()\n"
        "privetstvie()\n",
    )}
    <p><code class="inline">def</code> <strong>определяет</strong> функцию — записывает её код,
    но пока не выполняет его. Функция выполняется только тогда, когда вы её
    <strong>вызываете</strong> — по имени со скобками: <code class="inline">privetstvie()</code>.</p>

    {callout(
        "warning",
        "Определение — это ещё не вызов",
        "Если написать только <code class=\"inline\">def privetstvie(): ...</code> и не "
        "добавить <code class=\"inline\">privetstvie()</code> ниже, программа не выведет "
        "ничего — Python просто запомнит функцию, но не запустит её.",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "13-01-pervaya-funkciya.ipynb · определяем и вызываем первую функцию",
        "../../../notebooks/chapter-13/13-01-pervaya-funkciya.ipynb",
    )}
    """
    out = render_page(
        page_title="Настоящая автоматизация. Наша первая функция",
        description="Введение в функции Python: определение через def и вызов функции.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 13", "index.html"), ("Первая функция", "")],
        kicker="Глава 13 · Автоматизация с помощью функций",
        h1="Настоящая автоматизация",
        lede="Функции переиспользуют набор действий столько раз, сколько нужно — без "
        "копирования кода.",
        body_html=body,
        sidebar_groups=sidebar("13-01-nastoyashaya-avtomatizaciya.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="13-02-zachem-funkcii.html", next_label="Зачем нужны функции?"),
    )
    write("13-01-nastoyashaya-avtomatizaciya.html", out)


def build_02() -> None:
    body = f"""
    <h2>Зачем нужны функции?</h2>
    <ul>
      <li><strong>Код не повторяется</strong> — исправление вносится в одном месте.</li>
      <li><strong>Программу легче читать</strong> — имя функции объясняет, что происходит, не
        заставляя вникать в детали реализации.</li>
      <li><strong>Легче искать ошибки</strong> — если что-то сломалось в приветствии, вы точно
        знаете, где искать: внутри <code class="inline">privetstvie()</code>.</li>
    </ul>

    <h2>Каждый раз делаем что-то новое!</h2>
    <p>Функция без входных данных всегда делает одно и то же. Чтобы функция вела себя по-разному
    в зависимости от ситуации, ей передают <strong>аргументы</strong> — значения в скобках при
    вызове:</p>
    {code_block(
        "argumenty.py",
        "def privetstvie(imya):\n"
        '    print(f"Привет, {imya}!")\n\n'
        'privetstvie("Ада")\n'
        'privetstvie("Cartesian")\n',
    )}
    <p><code class="inline">imya</code> — <strong>параметр</strong> функции: имя, под которым
    переданное значение доступно внутри функции. При каждом вызове можно передать своё значение
    (<strong>аргумент</strong>).</p>

    <h2>Без аргументов?</h2>
    <p>Функция без параметров в скобках — например, <code class="inline">privetstvie()</code>
    из первого раздела — тоже совершенно нормальна: не каждой функции нужны входные данные.</p>

    {notebook_card(
        "Практика в Jupyter Notebook",
        "13-02-zachem-funkcii.ipynb · функции с аргументами",
        "../../../notebooks/chapter-13/13-02-zachem-funkcii.ipynb",
    )}
    """
    out = render_page(
        page_title="Зачем нужны функции?",
        description="Преимущества функций и передача аргументов для разного поведения при каждом вызове.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 13", "index.html"), ("Зачем функции?", "")],
        kicker="Глава 13 · Автоматизация с помощью функций",
        h1="Зачем нужны функции?",
        lede="Аргументы позволяют одной и той же функции каждый раз делать что-то немного "
        "своё.",
        body_html=body,
        sidebar_groups=sidebar("13-02-zachem-funkcii.html"),
        nav=PageNav(prev_href="13-01-nastoyashaya-avtomatizaciya.html", prev_label="Первая функция", next_href="13-03-vozvrashaem-otvet.html", next_label="Возвращаем ответ"),
    )
    write("13-02-zachem-funkcii.html", out)


def build_03() -> None:
    body = f"""
    <p>До сих пор наши функции только печатали текст. Но часто нужно не вывести результат на
    экран, а <strong>вернуть</strong> его — чтобы использовать дальше в программе.
    Ключевое слово <code class="inline">return</code> делает именно это:</p>
    {code_block(
        "return.py",
        "def summa(a, b):\n"
        "    return a + b\n\n"
        "result = summa(5, 7)\n"
        "print(result)         # 12\n"
        "print(summa(2, 3) * 10)  # результат функции можно использовать сразу — 50\n",
    )}
    {callout(
        "warning",
        "print() внутри функции — это не то же самое, что return",
        "Функция, которая только печатает результат, ничего не <em>возвращает</em> — попытка "
        "сохранить её результат в переменную даст <code class=\"inline\">None</code>:",
    )}
    {code_block(
        "print_vs_return.py",
        "def summa_pechataet(a, b):\n"
        "    print(a + b)   # выводит на экран, но не возвращает\n\n"
        "x = summa_pechataet(5, 7)  # на экране появится 12\n"
        "print(x)                    # но x — это None!\n",
    )}

    {callout(
        "tip",
        "return сразу завершает функцию",
        "Как только выполняется <code class=\"inline\">return</code>, функция немедленно "
        "заканчивает работу — код после него внутри функции не выполнится.",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "13-03-vozvrat.ipynb · return и разница с print()",
        "../../../notebooks/chapter-13/13-03-vozvrat.ipynb",
    )}
    """
    out = render_page(
        page_title="Возвращаем ответ",
        description="Ключевое слово return — как функции возвращают значения для дальнейшего использования.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 13", "index.html"), ("Возвращаем ответ", "")],
        kicker="Глава 13 · Автоматизация с помощью функций",
        h1="Возвращаем ответ",
        lede="return передаёт результат работы функции обратно туда, откуда она была вызвана.",
        body_html=body,
        sidebar_groups=sidebar("13-03-vozvrashaem-otvet.html"),
        nav=PageNav(prev_href="13-02-zachem-funkcii.html", prev_label="Зачем функции?", next_href="13-04-argumenty.html", next_label="Аргументы функций"),
    )
    write("13-03-vozvrashaem-otvet.html", out)


def build_04() -> None:
    body = f"""
    <h2>Нет аргументов? Что делать!</h2>
    <p>Если вызвать функцию без обязательного аргумента, Python сообщит об ошибке. Чтобы
    аргумент можно было пропустить, ему задают <strong>значение по умолчанию</strong>:</p>
    {code_block(
        "znachenie_po_umolchaniyu.py",
        "def privetstvie(imya=\"друг\"):\n"
        '    print(f"Привет, {imya}!")\n\n'
        "privetstvie()          # Привет, друг!\n"
        'privetstvie("Ада")     # Привет, Ада!\n',
    )}

    <h2>Слишком много аргументов!</h2>
    <p>Иногда заранее неизвестно, сколько аргументов понадобится передать. Символ
    <code class="inline">*</code> перед именем параметра собирает <strong>любое</strong>
    количество аргументов в один кортеж (глава 11):</p>
    {code_block(
        "args.py",
        "def summa_vseh(*chisla):\n"
        "    itog = 0\n"
        "    for n in chisla:\n"
        "        itog += n\n"
        "    return itog\n\n"
        "print(summa_vseh(1, 2))           # 3\n"
        "print(summa_vseh(1, 2, 3, 4, 5))  # 15 — сколько угодно аргументов\n",
    )}

    {callout(
        "info",
        "Именованные аргументы",
        "Аргументы можно передавать и по имени, а не только по порядку: "
        "<code class=\"inline\">privetstvie(imya=\"Ада\")</code> — это особенно удобно, когда у "
        "функции много параметров и легко перепутать порядок.",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "13-04-argumenty.ipynb · значения по умолчанию и *args",
        "../../../notebooks/chapter-13/13-04-argumenty.ipynb",
    )}
    """
    out = render_page(
        page_title="Аргументы функций",
        description="Значения по умолчанию для необязательных аргументов и *args для произвольного числа аргументов.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 13", "index.html"), ("Аргументы функций", "")],
        kicker="Глава 13 · Автоматизация с помощью функций",
        h1="Нет аргументов? Слишком много аргументов!",
        lede="Значения по умолчанию делают аргумент необязательным; *args принимает их сколько "
        "угодно.",
        body_html=body,
        sidebar_groups=sidebar("13-04-argumenty.html"),
        nav=PageNav(prev_href="13-03-vozvrashaem-otvet.html", prev_label="Возвращаем ответ", next_href="13-05-globalnye-lokalnye.html", next_label="Глобальные и локальные переменные"),
    )
    write("13-04-argumenty.html", out)


def build_05() -> None:
    body = f"""
    <h2>Переменные внутри функций</h2>
    <p>Переменная, созданная внутри функции, называется <strong>локальной</strong> — она
    существует только пока функция выполняется и недоступна снаружи:</p>
    {code_block(
        "lokalnye_peremennye.py",
        "def moya_funkciya():\n"
        '    message = "Я живу только внутри функции"\n'
        "    print(message)\n\n"
        "moya_funkciya()\n"
        "print(message)   # NameError: message не определена здесь\n",
    )}

    <h2>Возвращаем локальные переменные</h2>
    <p>Чтобы значение, вычисленное внутри функции, стало доступно снаружи, его нужно вернуть
    через <code class="inline">return</code> — это единственный «официальный» способ передать
    что-то из функции наружу.</p>

    <h2>Глобальные переменные</h2>
    <p><strong>Глобальная</strong> переменная объявлена вне всех функций — и доступна для чтения
    внутри любой из них:</p>
    {code_block(
        "globalnye_peremennye.py",
        'ver = "1.0"   # глобальная переменная\n\n'
        "def pokazat_versiyu():\n"
        '    print(f"Версия программы: {ver}")   # чтение глобальной переменной — работает\n\n'
        "pokazat_versiyu()\n",
    )}
    {callout(
        "warning",
        "Изменить глобальную переменную изнутри функции — не так просто",
        "Присваивание <code class=\"inline\">ver = \"2.0\"</code> внутри функции создаст "
        "<strong>новую локальную</strong> переменную <code class=\"inline\">ver</code>, а не "
        "изменит глобальную. Для настоящего изменения нужно ключевое слово "
        "<code class=\"inline\">global</code> — но в реальном коде такое встречается редко: "
        "гораздо чище вернуть новое значение через <code class=\"inline\">return</code>.",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "13-05-oblast-vidimosti.ipynb · локальные и глобальные переменные",
        "../../../notebooks/chapter-13/13-05-oblast-vidimosti.ipynb",
    )}
    """
    out = render_page(
        page_title="Глобальные и локальные переменные",
        description="Область видимости переменных в Python: локальные переменные функций и глобальные переменные.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 13", "index.html"), ("Область видимости", "")],
        kicker="Глава 13 · Автоматизация с помощью функций",
        h1="Глобальные и локальные переменные",
        lede="Где «живёт» переменная и кто может её увидеть — важное правило, которое избавит "
        "от многих загадочных ошибок.",
        body_html=body,
        sidebar_groups=sidebar("13-05-globalnye-lokalnye.html"),
        nav=PageNav(prev_href="13-04-argumenty.html", prev_label="Аргументы функций", next_href="13-06-lambda.html", next_label="Лямбда-функции"),
    )
    write("13-05-globalnye-lokalnye.html", out)


def build_06() -> None:
    cvm = classic_vs_modern(
        "Простая функция: def → lambda",
        "Обычная функция (def)",
        "def kvadrat(x):\n"
        "    return x ** 2\n\n"
        "print(kvadrat(5))",
        "Лямбда-функция",
        "kvadrat = lambda x: x ** 2\n\n"
        "print(kvadrat(5))",
        "обычную функцию с <code class=\"inline\">def</code> — она читается яснее, у неё есть "
        "нормальное имя для отладки, и в неё легко добавить несколько строк логики или "
        "комментарий. <code class=\"inline\">lambda</code> удобна только для одной короткой "
        "строки без имени — например, как аргумент функции <code class=\"inline\">sorted()</code> "
        "или <code class=\"inline\">max()</code>. Использовать lambda ради самой lambda, когда "
        "подошла бы обычная функция, — плохой стиль, а не «более современный».",
    )

    body = f"""
    <p><strong>Лямбда-функция</strong> — это способ создать маленькую безымянную функцию в одну
    строку. Тот же результат, что и через <code class="inline">def</code>, но короче:</p>
    {code_block("lambda.py", "kvadrat = lambda x: x ** 2\nprint(kvadrat(5))   # 25\n")}
    <p>Слева от двоеточия — параметры (без скобок), справа — единственное выражение, результат
    которого автоматически возвращается (без явного <code class="inline">return</code>).</p>

    <h2>Где лямбда действительно полезна</h2>
    <p>Чаще всего лямбда-функции передают <strong>как аргумент</strong> в другую функцию —
    например, чтобы задать правило сортировки:</p>
    {code_block(
        "lambda_sortirovka.py",
        'slova = ["python", "я", "программирование"]\n'
        "slova.sort(key=lambda word: len(word))\n"
        'print(slova)   # ["я", "python", "программирование"] — от короткого к длинному\n',
    )}

    {cvm}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "13-06-lambda.ipynb · лямбда-функции на практике",
        "../../../notebooks/chapter-13/13-06-lambda.ipynb",
    )}
    """
    out = render_page(
        page_title="Лямбда-функции",
        description="Короткие безымянные функции lambda в Python — когда их использовать, а когда предпочесть def.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 13", "index.html"), ("Лямбда-функции", "")],
        kicker="Глава 13 · Автоматизация с помощью функций",
        h1="Лямбда-функции",
        lede="Маленькие безымянные функции в одну строку — удобны в конкретных, узких "
        "случаях.",
        body_html=body,
        sidebar_groups=sidebar("13-06-lambda.html"),
        nav=PageNav(prev_href="13-05-globalnye-lokalnye.html", prev_label="Область видимости", next_href="13-07-mini-proekt-domashka.html", next_label="Домашнее задание по математике"),
    )
    write("13-06-lambda.html", out)


def build_07() -> None:
    body = f"""
    <p>Соберём функции, аргументы и return в одном полезном инструменте: генераторе примеров
    для тренировки таблицы умножения.</p>
    {code_block(
        "domashnee_zadanie.py",
        "import random\n\n"
        "def sgenerirovat_primer():\n"
        "    a = random.randint(2, 9)\n"
        "    b = random.randint(2, 9)\n"
        "    return a, b, a * b\n\n"
        "def proverit_otvet(pravilnyj_otvet, otvet_polzovatelya):\n"
        "    return pravilnyj_otvet == otvet_polzovatelya\n\n"
        "a, b, pravilnyj_otvet = sgenerirovat_primer()\n"
        'otvet = int(input(f"Сколько будет {a} x {b}? "))\n\n'
        "if proverit_otvet(pravilnyj_otvet, otvet):\n"
        '    print("Верно!")\n'
        "else:\n"
        '    print(f"Неверно — правильный ответ: {pravilnyj_otvet}")\n',
    )}
    {callout(
        "info",
        "Функция возвращает сразу три значения",
        "<code class=\"inline\">return a, b, a * b</code> на самом деле возвращает один кортеж "
        "<code class=\"inline\">(a, b, a * b)</code> — мы распаковываем его в три переменные "
        "сразу, как в главе 11.",
    )}
    {exercise(2, "Счётчик правильных ответов", "Оберните генерацию примера в цикл на 5 вопросов подряд и посчитайте, сколько из них решено верно.")}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "13-07-domashka.ipynb · генератор примеров по математике",
        "../../../notebooks/chapter-13/13-07-domashka.ipynb",
    )}
    """
    out = render_page(
        page_title="Мини-проект — домашнее задание по математике",
        description="Мини-проект: генератор примеров на умножение с использованием функций.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 13", "index.html"), ("Домашнее задание", "")],
        kicker="Глава 13 · Автоматизация с помощью функций",
        h1="Мини-проект — выполняем домашнее задание по математике с Python",
        lede="Функции для генерации и проверки примеров на умножение — практика на все приёмы "
        "главы.",
        body_html=body,
        sidebar_groups=sidebar("13-07-mini-proekt-domashka.html"),
        nav=PageNav(prev_href="13-06-lambda.html", prev_label="Лямбда-функции", next_href="13-08-mini-proekt-figury-itogi.html", next_label="Фигуры: новый уровень и итоги"),
    )
    write("13-07-mini-proekt-domashka.html", out)


def build_08() -> None:
    body = f"""
    <p>Финальный проект главы: превратим повторяющийся код рисования фигур из главы 10 в
    настоящую функцию с аргументами.</p>
    {code_block(
        "figura_funkciya.py",
        "def narisovat_figuru(storony, dlina):\n"
        "    ugol = 360 / storony\n"
        "    for _ in range(storony):\n"
        "        artist.forward(dlina)\n"
        "        artist.right(ugol)\n\n"
        "narisovat_figuru(4, 100)    # квадрат\n"
        "narisovat_figuru(3, 100)    # треугольник, без повторения кода!\n"
        "narisovat_figuru(8, 60)     # восьмиугольник\n",
    )}
    {callout(
        "tip",
        "Сравните с главой 10",
        "В главе 10 для каждой фигуры пришлось бы менять переменные <code class=\"inline\">"
        "storony</code> и <code class=\"inline\">dlina</code> вручную перед каждым запуском. "
        "Теперь то же самое — параметры функции, и три фигуры рисуются тремя короткими "
        "строками подряд.",
    )}
    {exercise(3, "Функция с позицией", "Добавьте функции параметры x, y (со значениями по умолчанию 0, 0) — чтобы можно было указать, откуда начинать рисовать фигуру.")}

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
        "<code class=\"inline\">def имя(параметры):</code> определяет функцию; вызов "
        "<code class=\"inline\">имя(аргументы)</code> её запускает.",
        "<code class=\"inline\">return</code> передаёt результат функции наружу — это не то "
        "же самое, что <code class=\"inline\">print()</code> внутри функции.",
        "Параметрам можно задать значение по умолчанию; <code class=\"inline\">*args</code> "
        "принимает произвольное число аргументов.",
        "Переменные внутри функции — локальные; переменные вне всех функций — глобальные и "
        "доступны для чтения изнутри функций.",
        "<code class=\"inline\">lambda</code> — короткая безымянная функция для простых "
        "случаев, чаще всего как аргумент другой функции.",
    ])}
    """
    out = render_page(
        page_title="Мини-проект — автоматизированные фигуры: новый уровень",
        description="Итоговый мини-проект главы 13: универсальная функция рисования фигур — и краткие итоги.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 13", "index.html"), ("Фигуры: новый уровень", "")],
        kicker="Глава 13 · Автоматизация с помощью функций",
        h1="Мини-проект — автоматизированные фигуры: новый уровень",
        lede="Фигуры из главы 10 становятся настоящей переиспользуемой функцией — и подводим "
        "итоги.",
        body_html=body,
        sidebar_groups=sidebar("13-08-mini-proekt-figury-itogi.html"),
        nav=PageNav(prev_href="13-07-mini-proekt-domashka.html", prev_label="Домашнее задание", next_href="../glava-14/index.html", next_label="Глава 14: Создаём объекты реального мира"),
    )
    write("13-08-mini-proekt-figury-itogi.html", out)


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
