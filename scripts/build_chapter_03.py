#!/usr/bin/env python3
"""Строит Главу 3: «Ваша первая программа на Python» (site/chapters/glava-03/)."""

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
OUT_DIR = ROOT / "site" / "chapters" / "glava-03"

PAGES = [
    ("index.html", "Приступаем"),
    ("03-01-sozdanie-i-zapusk-programm.html", "Создание и запуск программ"),
    ("03-02-interaktivny-rezhim.html", "Интерактивный режим (Shell)"),
    ("03-03-vyvod-dannyh.html", "Вывод данных с помощью Python"),
    ("03-04-idle.html", "Режим сценариев IDLE"),
    ("03-05-praktika-itogi.html", "Практика и итоги"),
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 3 · Первая программа", items),
        SidebarGroup("Практика", [
            NavItem("🐍 03-01: Практика", "../../practice/03-01/index.html"),
            NavItem("🐍 03-02: Практика", "../../practice/03-02/index.html"),
            NavItem("🐍 03-03: Практика", "../../practice/03-03/index.html"),
            NavItem("🐍 03-04: Практика", "../../practice/03-04/index.html"),
        ]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=3,
        baseline_page=27,
        title="Ваша первая программа на Python",
        description="Пишем и запускаем первую программу — в VS Code, в PyCharm и в интерактивной оболочке.",
        meta_items=["⏱ ~1 час", "💻 VS Code или PyCharm", "📓 4 ноутбука практики"],
        sections=[
            ChapterSectionLink("3.1", "Создание и запуск программ на Python", "03-01-sozdanie-i-zapusk-programm.html", "27"),
            ChapterSectionLink("3.2", "Интерактивный режим Python (Python Shell)", "03-02-interaktivny-rezhim.html", "30"),
            ChapterSectionLink("", "Ваша оболочка умеет считать", "03-02-interaktivny-rezhim.html#schitaet", "30"),
            ChapterSectionLink("3.3", "Вывод данных с помощью Python", "03-03-vyvod-dannyh.html", "32"),
            ChapterSectionLink("3.4", "Режим сценариев IDLE", "03-04-idle.html", "33"),
            ChapterSectionLink("3.5", "Практика: выведите своё имя (и кое-что ещё)", "03-05-praktika-itogi.html", "36"),
            ChapterSectionLink("", "Итоги", "03-05-praktika-itogi.html#itogi", "37"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <p>Программа на Python — это обычный текстовый файл с расширением
    <code class="inline">.py</code>. Чтобы его написать и запустить, нужен редактор кода. В этой
    книге мы используем два: <strong>Visual Studio Code</strong> и <strong>PyCharm</strong> —
    оба бесплатны (PyCharm — в редакции Community) и оба отлично подходят для Python.</p>

    <h2>Вариант A: Visual Studio Code</h2>
    <ol>
      <li>Установите VS Code с <a href="https://code.visualstudio.com" target="_blank" rel="noopener">code.visualstudio.com</a>
        и расширение <strong>Python</strong> (от Microsoft) через панель Extensions.</li>
      <li>Создайте папку для проекта книги, например <code class="inline">python-s-nulya</code>, и
        откройте её через <strong>File → Open Folder</strong>.</li>
      <li>Создайте новый файл <code class="inline">privet.py</code>.</li>
      <li>В правом нижнем углу окна нажмите на индикатор версии Python и выберите установленный
        Python 3.14 в качестве интерпретатора — если индикатора нет, откройте палитру команд
        (<code class="inline">Ctrl+Shift+P</code> / <code class="inline">Cmd+Shift+P</code>) и
        выполните «Python: Select Interpreter».</li>
      <li>Напишите код (пример — ниже) и нажмите на треугольник ▷ «Run Python File» в правом
        верхнем углу, либо откройте встроенный терминал (<code class="inline">Ctrl+`</code>) и
        наберите <code class="inline">python privet.py</code>.</li>
    </ol>

    <h2>Вариант B: PyCharm</h2>
    <ol>
      <li>Установите PyCharm Community с <a href="https://www.jetbrains.com/pycharm/download/" target="_blank" rel="noopener">jetbrains.com/pycharm/download</a>.</li>
      <li>При создании проекта (<strong>New Project</strong>) укажите папку проекта и Python 3.14
        в качестве интерпретатора — PyCharm покажет список найденных версий автоматически.</li>
      <li>Щёлкните правой кнопкой по папке проекта в панели слева → <strong>New → Python File</strong>,
        назовите его <code class="inline">privet</code>.</li>
      <li>Напишите код и нажмите на зелёный треугольник ▷ рядом со строкой
        <code class="inline">if __name__ ==</code> или в верхней панели — либо кликните правой
        кнопкой в редакторе и выберите «Run».</li>
    </ol>

    <h2>Ваша первая программа</h2>
    {code_block("privet.py", 'print("Привет, Python!")\n')}
    <p>После запуска — любым из двух способов — вы должны увидеть в терминале:</p>
    {code_block("вывод программы", 'Привет, Python!')}

    {callout(
        "tip",
        "Терминал внутри редактора",
        "И VS Code, и PyCharm показывают вывод программы во встроенном терминале внизу окна — "
        "не нужно переключаться в отдельное приложение. Именно этим встроенным терминалом мы "
        "будем пользоваться на протяжении всей книги.",
    )}

    {practice_card(
        "03-01",
        "Практика: создайте и запустите свою первую программу",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/03-01/index.html",
    )}
    """

    out = render_page(
        page_title="Создание и запуск программ на Python",
        description="Как создать .py-файл и запустить его в VS Code и в PyCharm.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("Создание и запуск программ", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="Создание и запуск программ на Python",
        lede="Программа на Python начинается с обычного текстового файла. Разберём, как создать "
        "его и запустить — в VS Code и в PyCharm.",
        body_html=body,
        sidebar_groups=sidebar("03-01-sozdanie-i-zapusk-programm.html"),
        nav=PageNav(prev_href="index.html", prev_label="Приступаем", next_href="03-02-interaktivny-rezhim.html", next_label="Интерактивный режим (Shell)"),
    )
    write("03-01-sozdanie-i-zapusk-programm.html", out)


def build_02() -> None:
    body = f"""
    <h2>Интерактивный режим Python (Python Shell)</h2>
    <p>Кроме запуска файлов, у Python есть второй, не менее полезный режим —
    <strong>интерактивная оболочка</strong> (Python Shell, или REPL — Read-Eval-Print Loop:
    «прочитать — выполнить — напечатать — повторить»). В ней вы вводите код по одной строке и
    сразу видите результат — без файла и без «запуска» в привычном смысле.</p>
    <p>Открыть её можно прямо в терминале VS Code или PyCharm, набрав <code class="inline">python</code>
    (Windows) или <code class="inline">python3</code> (Mac). Появится приглашение
    <code class="inline">&gt;&gt;&gt;</code> — это значит, что оболочка ждёт вашу команду.</p>

    {code_block(
        "терминал",
        '$ python\nPython 3.14.0 (main, ...) \n>>> print("Привет!")\nПривет!\n>>> ',
    )}

    {callout(
        "info",
        "Как выйти",
        "Наберите <code class=\"inline\">exit()</code> и нажмите Enter, либо нажмите "
        "<code class=\"inline\">Ctrl+Z</code> затем Enter (Windows) или "
        "<code class=\"inline\">Ctrl+D</code> (Mac/Linux).",
    )}

    {practice_card(
        "03-02",
        "Практика: интерактивный режим в ноутбуке",
        "Интерактивный ноутбук прямо в браузере — сравните ячейку Jupyter с Python Shell",
        "../../practice/03-02/index.html",
    )}

    <h2 id="schitaet">Ваша оболочка умеет считать</h2>
    <p>Раз оболочка сразу показывает результат каждой строки, её удобно использовать как быстрый
    калькулятор — без единого <code class="inline">print()</code>:</p>
    {code_block("Python Shell", '>>> 2 + 2\n4\n>>> 10 / 4\n2.5\n>>> 3 * 7\n21\n')}
    <p>Это работает только в самой оболочке: в обычном <code class="inline">.py</code>-файле
    строка <code class="inline">2 + 2</code> сама по себе ничего не выведет — файл выполняется
    целиком и молча, если явно не попросить вывод через <code class="inline">print()</code>.
    Подробно об этом — в следующем разделе.</p>

    {practice_card(
        "03-03",
        "Практика: используйте Python как калькулятор",
        "Интерактивный ноутбук прямо в браузере — сложение, вычитание, умножение, деление",
        "../../practice/03-03/index.html",
    )}
    """

    out = render_page(
        page_title="Интерактивный режим Python (Python Shell)",
        description="Что такое интерактивная оболочка Python (REPL) и почему в ней можно "
        "использовать Python как калькулятор.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("Интерактивный режим (Shell)", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="Интерактивный режим Python (Python Shell)",
        lede="Второй способ работать с Python — вводить код по одной строке и сразу видеть "
        "результат, без файла и без print().",
        body_html=body,
        sidebar_groups=sidebar("03-02-interaktivny-rezhim.html"),
        nav=PageNav(prev_href="03-01-sozdanie-i-zapusk-programm.html", prev_label="Создание и запуск программ", next_href="03-03-vyvod-dannyh.html", next_label="Вывод данных с помощью Python"),
    )
    write("03-02-interaktivny-rezhim.html", out)


def build_03() -> None:
    body = f"""
    <p>В файле <code class="inline">.py</code> ничего не выводится на экран само по себе — нужно
    явно попросить об этом командой <code class="inline">print()</code>. Мы уже пользовались ей в
    главе 1, теперь разберём подробнее.</p>

    <h2>Несколько значений в одной команде</h2>
    {code_block("print_demo.py", 'print("Возраст:", 10, "лет")\n')}
    <p>Через запятую можно передать сколько угодно значений — <code class="inline">print()</code>
    сам вставит между ними пробел и выведет всё в одну строку.</p>

    <h2>Параметр <code class="inline">sep</code> — разделитель</h2>
    <p>По умолчанию значения разделяются пробелом. Это можно изменить параметром
    <code class="inline">sep</code>:</p>
    {code_block("print_sep.py", 'print("2024", "01", "15", sep="-")\n')}
    {code_block("вывод программы", '2024-01-15')}

    <h2>Параметр <code class="inline">end</code> — чем закончить строку</h2>
    <p>По умолчанию каждый <code class="inline">print()</code> завершается переводом строки —
    поэтому следующий вызов начинается с новой строки. Параметр <code class="inline">end</code>
    позволяет это изменить:</p>
    {code_block("print_end.py", 'print("Загрузка", end="")\nprint("...", end="")\nprint("готово!")\n')}
    {code_block("вывод программы", 'Загрузка...готово!')}

    {callout(
        "tip",
        "Пустая строка",
        "Вызов <code class=\"inline\">print()</code> без аргументов просто выводит пустую строку "
        "— удобно, чтобы отделить блоки текста друг от друга.",
    )}

    {practice_card(
        "03-04",
        "Практика: sep, end и форматирование вывода",
        "Интерактивный ноутбук прямо в браузере — параметры print() на практике",
        "../../practice/03-04/index.html",
    )}
    """

    out = render_page(
        page_title="Вывод данных с помощью Python",
        description="Подробно о print(): несколько значений, параметры sep и end.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("Вывод данных с помощью Python", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="Вывод данных с помощью Python",
        lede="print() умеет больше, чем кажется на первый взгляд — несколько значений сразу, "
        "свои разделители и управление концом строки.",
        body_html=body,
        sidebar_groups=sidebar("03-03-vyvod-dannyh.html"),
        nav=PageNav(prev_href="03-02-interaktivny-rezhim.html", prev_label="Интерактивный режим (Shell)", next_href="03-04-idle.html", next_label="Режим сценариев IDLE"),
    )
    write("03-03-vyvod-dannyh.html", out)


def build_04() -> None:
    cvm = classic_vs_modern(
        "IDLE → современная разработка",
        "IDLE (входит в Python «из коробки»)",
        'print("Привет из IDLE!")\n'
        "# запуск: меню Run -> Run Module (F5)\n"
        "# один файл, минимум настроек",
        "VS Code / PyCharm",
        'print("Привет из VS Code!")\n'
        "# запуск: кнопка Run или встроенный терминал\n"
        "# подсветка ошибок на лету, автодополнение,\n"
        "# отладчик, git, множество расширений",
        "IDLE отлично подходит, чтобы буквально за одну минуту после установки Python "
        "написать и запустить первую строку кода — устанавливать ничего дополнительно не "
        "нужно. Но как только проекты вырастают за пределы одного файла, заметно не хватает "
        "автодополнения, отладчика и подсветки ошибок на лету. Начиная со следующей главы мы "
        "будем пользоваться VS Code или PyCharm — но IDLE стоит знать: именно её вы увидите, "
        "если попробуете Python на чужом компьютере без дополнительной настройки.",
    )

    body = f"""
    <p>У Python есть встроенный простой редактор кода, который устанавливается автоматически
    вместе с самим Python, — <strong>IDLE</strong> (Integrated Development and Learning
    Environment). Открыть его можно, найдя «IDLE» в меню Пуск (Windows) или Launchpad (Mac).</p>

    <h2>Режим сценариев (Script Mode)</h2>
    <p>При запуске IDLE открывается интерактивная оболочка — та же самая, что мы видели в
    предыдущем разделе, только в собственном окне. Чтобы написать полноценную программу, нужен
    отдельный файл: <strong>File → New File</strong> откроет пустое окно редактора — это и есть
    «режим сценариев».</p>
    <ol>
      <li>Наберите код в новом окне редактора.</li>
      <li>Сохраните файл: <strong>File → Save</strong> (расширение <code class="inline">.py</code>
        подставится само).</li>
      <li>Запустите: <strong>Run → Run Module</strong>, либо просто нажмите клавишу
        <code class="inline">F5</code>.</li>
      <li>Результат появится в окне интерактивной оболочки IDLE.</li>
    </ol>

    {cvm}
    """

    out = render_page(
        page_title="Режим сценариев IDLE",
        description="Знакомимся с IDLE — встроенным редактором Python — и сравниваем его с VS Code и PyCharm.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("Режим сценариев IDLE", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="Режим сценариев IDLE",
        lede="Python сам приносит с собой простой редактор — IDLE. Разберёмся, как им "
        "пользоваться и когда стоит перейти на более мощный инструмент.",
        body_html=body,
        sidebar_groups=sidebar("03-04-idle.html"),
        nav=PageNav(prev_href="03-03-vyvod-dannyh.html", prev_label="Вывод данных с помощью Python", next_href="03-05-praktika-itogi.html", next_label="Практика и итоги"),
    )
    write("03-04-idle.html", out)


def build_05() -> None:
    body = f"""
    <p>Пора применить все четыре инструмента раздела на практике: файл, оболочку, print и IDLE
    (или VS Code/PyCharm — на ваш выбор) — в одном небольшом упражнении.</p>

    {exercise(
        1,
        "Выведите своё имя",
        "Создайте файл <code class=\"inline\">o_sebe.py</code> и одной командой "
        "<code class=\"inline\">print()</code> выведите своё имя.",
    )}
    {exercise(
        2,
        "И кое-что ещё",
        "В том же файле добавьте ещё две строки: одну — с вашим городом, вторую — с "
        "любым числом, использовав <code class=\"inline\">sep</code>, чтобы вывести имя, город "
        "и число в одну строку через « · ».",
    )}
    {exercise(
        3,
        "Тот же результат тремя способами",
        "Получите один и тот же вывод тремя разными способами: запустив файл из терминала "
        "(<code class=\"inline\">python o_sebe.py</code>), через кнопку Run в VS Code/PyCharm, "
        "и через Run Module в IDLE.",
    )}

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
        "Программа на Python — обычный текстовый файл <code class=\"inline\">.py</code>, который "
        "запускают командой <code class=\"inline\">python имя_файла.py</code>.",
        "VS Code и PyCharm — два основных инструмента этой книги для написания и запуска кода.",
        "Интерактивная оболочка (Python Shell) выполняет код построчно и сразу показывает "
        "результат — удобно как калькулятор.",
        "<code class=\"inline\">print()</code> умеет выводить несколько значений сразу и "
        "принимает параметры <code class=\"inline\">sep</code> и <code class=\"inline\">end</code>.",
        "IDLE — простой редактор, который устанавливается вместе с Python; полезно знать, но "
        "для реальных проектов удобнее VS Code или PyCharm.",
    ])}
    """

    out = render_page(
        page_title="Практика: выведите своё имя (и кое-что ещё)",
        description="Итоговая практика главы 3 и краткое резюме пройденного материала.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("Практика и итоги", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="Практика: выведите своё имя (и кое-что ещё)",
        lede="Собираем всё вместе: файл, терминал, print и выбор редактора — в одном небольшом "
        "упражнении.",
        body_html=body,
        sidebar_groups=sidebar("03-05-praktika-itogi.html"),
        nav=PageNav(prev_href="03-04-idle.html", prev_label="Режим сценариев IDLE", next_href="../glava-04/index.html", next_label="Глава 4: Python любит числа"),
    )
    write("03-05-praktika-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01()
    build_02()
    build_03()
    build_04()
    build_05()
