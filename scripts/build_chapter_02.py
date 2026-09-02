#!/usr/bin/env python3
"""Строит Главу 2: «Давайте установим Python!» (site/chapters/glava-02/).

Curriculum v2: полноценный курс по сборке рабочего места Python-разработчика —
установка на Windows/macOS/Linux, терминал и PATH, VS Code и PyCharm,
виртуальные окружения, pip/pipx/venv/virtualenv/uv, conda/Anaconda, связи
между IDE/интерпретатором/окружением/пакетами, диагностика типичных проблем.
Существующие маршруты (index.html, 02-01/02-02/02-03, без страниц практики —
эта глава не содержит браузерной практики по конструкции) сохранены; новый
материал добавлен как новые страницы (02-04..02-17) плюс расширение
содержимого существующих трёх страниц.
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
    code_block,
    comparison_table,
    converge_diagram,
    exercise,
    flow_diagram,
    image_figure,
    render_chapter_opener,
    render_page,
    summary_box,
    timeline_diagram,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-02"

PAGES = [
    ("index.html", "Приступаем"),
    ("02-01-govorim-na-yazyke-kompyutera.html", "Что именно мы устанавливаем?"),
    ("02-04-terminal-shell-i-path.html", "Терминал, shell и PATH"),
    ("02-02-windows.html", "Установка на Windows"),
    ("02-03-mac.html", "Установка на macOS"),
    ("02-05-linux.html", "Установка на Linux"),
    ("02-06-kakoj-python-zapushen.html", "Какой Python действительно запущен"),
    ("02-07-vscode-ustanovka-i-rasshireniya.html", "VS Code: установка и расширения"),
    ("02-08-vscode-konfiguraciya.html", "VS Code: интерпретатор и рабочий процесс"),
    ("02-09-pycharm.html", "PyCharm: проект, интерпретатор, окружение"),
    ("02-10-zachem-nuzhny-venv.html", "Виртуальные окружения — зачем они нужны"),
    ("02-11-sozdanie-venv.html", "Создаём .venv"),
    ("02-12-pervyj-paket.html", "Устанавливаем первый пакет"),
    ("02-13-pip-pipx-venv-virtualenv-uv.html", "pip, pipx, venv, virtualenv, uv"),
    ("02-14-conda-i-anaconda.html", "conda, Miniconda, Miniforge, Anaconda"),
    ("02-15-ide-i-okruzheniya.html", "Как IDE, Python и окружение связаны"),
    ("02-16-diagnostika.html", "Типичные проблемы и диагностика"),
    ("02-17-rekomendacii-i-itogi.html", "Рекомендации Cartesian School и итоги"),
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [SidebarGroup("Глава 2 · Установка Python", items)]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


IMG = "../../assets/img"


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=2,
        description="Полноценная сборка рабочего места Python-разработчика: установка на Windows, "
        "macOS и Linux, терминал и PATH, VS Code и PyCharm, виртуальные окружения, "
        "pip/pipx/venv/uv/conda — и как всё это связано между собой.",
        meta_items=["[[icon:timer]] ~3 часа", "[[icon:code]] Windows, macOS или Linux", "[[icon:tools]] local-required — практика на вашем компьютере"],
        sections=[
            ChapterSectionLink("2.1", "Что именно мы устанавливаем?", "02-01-govorim-na-yazyke-kompyutera.html"),
            ChapterSectionLink("2.2", "Терминал, shell и PATH", "02-04-terminal-shell-i-path.html"),
            ChapterSectionLink("2.3", "Установка Python на Windows", "02-02-windows.html"),
            ChapterSectionLink("2.4", "Установка Python на macOS", "02-03-mac.html"),
            ChapterSectionLink("2.5", "Установка Python на Linux", "02-05-linux.html"),
            ChapterSectionLink("2.6", "Какой Python действительно запущен", "02-06-kakoj-python-zapushen.html"),
            ChapterSectionLink("2.7", "VS Code: установка и расширения", "02-07-vscode-ustanovka-i-rasshireniya.html"),
            ChapterSectionLink("2.8", "VS Code: интерпретатор и рабочий процесс", "02-08-vscode-konfiguraciya.html"),
            ChapterSectionLink("2.9", "PyCharm: проект, интерпретатор, окружение", "02-09-pycharm.html"),
            ChapterSectionLink("2.10", "Виртуальные окружения — зачем они нужны", "02-10-zachem-nuzhny-venv.html"),
            ChapterSectionLink("2.11", "Создаём .venv", "02-11-sozdanie-venv.html"),
            ChapterSectionLink("2.12", "Устанавливаем первый пакет", "02-12-pervyj-paket.html"),
            ChapterSectionLink("2.13", "pip, pipx, venv, virtualenv, uv", "02-13-pip-pipx-venv-virtualenv-uv.html"),
            ChapterSectionLink("2.14", "conda, Miniconda, Miniforge, Anaconda", "02-14-conda-i-anaconda.html"),
            ChapterSectionLink("2.15", "Как IDE, Python и окружение связаны", "02-15-ide-i-okruzheniya.html"),
            ChapterSectionLink("2.16", "Типичные проблемы и диагностика", "02-16-diagnostika.html"),
            ChapterSectionLink("2.17", "Рекомендации Cartesian School и итоги", "02-17-rekomendacii-i-itogi.html"),
        ],
    )
    write("index.html", out)


def build_01_layers() -> None:
    layers = timeline_diagram(
        [
            ("Компьютер", "физическое железо"),
            ("Операционная система", "Windows, macOS или Linux"),
            ("Python-интерпретатор", "программа, понимающая .py-файлы"),
            ("Проект", "папка с вашим кодом"),
            ("Виртуальное окружение", "изолированная копия интерпретатора для проекта"),
            ("Пакеты", "сторонний код, который вы устанавливаете"),
            ("Ваш код", "то, что вы пишете и запускаете"),
        ],
        caption="Семь слоёв между «железом» и вашей первой программой",
    )

    body = f"""
    <p>Компьютер невероятно быстрый, но абсолютно несамостоятельный. Сам по себе он не умеет
    вообще ничего — ни открыть игру, ни показать фотографию, ни посчитать сдачу в магазине. Всё,
    что делает компьютер, он делает потому, что кто-то заранее написал для него точную
    последовательность команд. Эта последовательность и называется <strong>программой</strong>,
    а процесс её написания — <strong>программированием</strong>.</p>
    <p>Когда вы устанавливаете Python, вы устанавливаете <strong>интерпретатор</strong> — программу,
    которая умеет читать и выполнять код на Python (мы говорили об этом в главе 1). Но между
    «Python установлен» и «мой код работает» на самом деле выстраивается целая цепочка слоёв,
    и эта глава — про то, чтобы честно разобрать каждый из них.</p>

{layers}

    <h2 id="ne-putat">Четыре вещи, которые легко перепутать</h2>
    <p>Это, пожалуй, самое важное различие во всей главе — и одна из главных причин, почему
    начинающие путаются в установке Python:</p>
    <ul>
      <li><strong>Python-интерпретатор ≠ VS Code.</strong> VS Code — это редактор кода. Он не
        умеет выполнять Python сам по себе — он находит и запускает установленный на компьютере
        интерпретатор.</li>
      <li><strong>Python-интерпретатор ≠ PyCharm.</strong> То же самое: PyCharm — среда разработки,
        которая тоже использует внешний интерпретатор, а не содержит его «внутри себя».</li>
      <li><strong>Python-интерпретатор ≠ pip.</strong> pip — это программа для установки пакетов;
        она сама работает <em>поверх</em> интерпретатора, а не является им.</li>
      <li><strong>Python-интерпретатор ≠ виртуальное окружение.</strong> Виртуальное окружение
        (о нём подробно — в разделах 2.10–2.11) — это лёгкая, изолированная копия интерпретатора
        для конкретного проекта, а не что-то отдельное от него.</li>
    </ul>

{callout(
        "tip",
        "[[icon:idea]] Идея",
        "VS Code и PyCharm — это инструменты, которые <em>используют</em> Python-интерпретатор, "
        "а не заменяют его. Установка редактора кода и установка Python — это два разных, "
        "независимых шага.",
    )}

    <p>Дальше в этой главе мы пройдём весь путь по порядку: установим сам интерпретатор на вашей
    операционной системе (разделы 2.3–2.5), научимся проверять, какой именно Python реально
    запускается (2.6), настроим редактор кода (2.7–2.9), разберёмся с виртуальными окружениями
    (2.10–2.12) и с зоопарком инструментов вокруг них (2.13–2.14), а в конце — соберём всё вместе
    и потренируемся находить и чинить типичные ошибки (2.15–2.17).</p>"""

    out = render_page(
        page_title="Что именно мы устанавливаем?",
        description="Семь слоёв между железом и вашим кодом — и почему интерпретатор Python, "
        "редактор кода, pip и виртуальное окружение — четыре разные вещи.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("Что именно мы устанавливаем?", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="Что именно мы устанавливаем?",
        lede="Прежде чем ставить галочки в установщиках, полезно понять, из каких слоёв "
        "вообще состоит рабочее место Python-разработчика.",
        body_html=body,
        sidebar_groups=sidebar("02-01-govorim-na-yazyke-kompyutera.html"),
        nav=PageNav(prev_href="index.html", prev_label="Приступаем", next_href="02-04-terminal-shell-i-path.html", next_label="Терминал, shell и PATH"),
    )
    write("02-01-govorim-na-yazyke-kompyutera.html", out)


def build_04_terminal_path() -> None:
    lookup_flow = timeline_diagram(
        [
            ("Вы вводите команду", "например, python"),
            ("Shell получает текст", "программа-командная оболочка"),
            ("Поиск по PATH", "shell проверяет папки по очереди"),
            ("Исполняемый файл найден", "первое совпадение побеждает"),
            ("Команда запускается", "или «command not found», если нигде не нашлось"),
        ],
        caption="Что происходит, когда вы нажимаете Enter после команды",
    )

    path_example = code_block(
        "PATH (Linux/macOS, упрощённо)",
        "/usr/local/bin\n/usr/bin\n/bin\n~/.local/bin",
        lang="text",
    )

    body = f"""
    <h2 id="terminal-i-shell">Терминал и shell</h2>
    <p><strong>Терминал</strong> — окно программы, где вы вводите текстовые команды и видите
    текстовый ответ компьютера. <strong>Shell</strong> (командная оболочка) — программа, которая
    внутри терминала на самом деле читает вашу команду и решает, что с ней делать. На Windows это
    обычно PowerShell или классическая cmd, на macOS и Linux — чаще всего <code class="inline">zsh</code>
    или <code class="inline">bash</code>.</p>
    <p>Команда обычно состоит из имени программы и, при необходимости, <strong>аргументов</strong> —
    дополнительных слов после неё: в <code class="inline">python --version</code> само
    <code class="inline">python</code> — команда, а <code class="inline">--version</code> — аргумент.</p>

    <h2 id="puti">Путь, файловая система и текущая папка</h2>
    <p>Shell всегда «стоит» в какой-то одной папке — она называется <strong>текущей рабочей
    папкой</strong> (current directory). <strong>Путь</strong> (path) — это адрес файла или папки
    в файловой системе. Путь бывает:</p>
    <ul>
      <li><strong>абсолютным</strong> — начинается от корня диска, например
        <code class="inline">C:\\Users\\anna\\project</code> или <code class="inline">/home/anna/project</code>,
        и работает откуда угодно;</li>
      <li><strong>относительным</strong> — отсчитывается от текущей папки, например
        <code class="inline">./project</code> или просто <code class="inline">project</code>.</li>
    </ul>

    <h2 id="peremennaya-path">Переменная окружения PATH</h2>
    <p>Когда вы вводите короткую команду вроде <code class="inline">python</code>, компьютер не
    ищет файл по всему диску — это заняло бы слишком много времени. Вместо этого shell смотрит в
    специальный список папок — <strong>переменную окружения PATH</strong> — и проверяет их по
    очереди в заданном порядке, пока не найдёт исполняемый файл с таким именем.</p>

{path_example}

    <p>Если вы наберёте <code class="inline">python</code>, shell проверит
    <code class="inline">/usr/local/bin/python</code>, затем <code class="inline">/usr/bin/python</code>
    и так далее — и запустит первый найденный файл. Если ни в одной из папок PATH такого файла
    нет — вы увидите ошибку вроде <code class="inline">command not found</code> (macOS/Linux) или
    <code class="inline">'python' is not recognized...</code> (Windows).</p>

{lookup_flow}

{callout(
        "warning",
        "[[icon:warning]] Типичная ошибка",
        "Если на компьютере установлено <strong>два разных Python</strong>, а в PATH они "
        "перечислены не в том порядке, который вы ожидаете, — команда "
        "<code class=\"inline\">python</code> может запускать совсем не ту версию, которую вы "
        "только что установили. Раздел 2.6 научит это проверять.",
    )}

{callout(
        "info",
        "[[icon:note]] Официальный источник",
        "Подробное объяснение переменных окружения — в документации вашей операционной системы; "
        "для самого Python — раздел «Using Python on Unix platforms» / «Using Python on Windows» "
        "на docs.python.org.",
    )}"""

    out = render_page(
        page_title="Терминал, shell и PATH",
        description="Что такое терминал, shell, команда и аргумент — и как переменная окружения "
        "PATH решает, какая программа запустится по имени python.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("Терминал, shell и PATH", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="Терминал, shell и PATH",
        lede="Одно из самых важных объяснений этой главы: что на самом деле происходит, когда "
        "вы вводите команду и нажимаете Enter.",
        body_html=body,
        sidebar_groups=sidebar("02-04-terminal-shell-i-path.html"),
        nav=PageNav(prev_href="02-01-govorim-na-yazyke-kompyutera.html", prev_label="Что именно мы устанавливаем?", next_href="02-02-windows.html", next_label="Установка на Windows"),
    )
    write("02-04-terminal-shell-i-path.html", out)


def build_02_windows() -> None:
    steps = flow_diagram(
        [
            ("Скачать", "python.org/downloads"),
            ("Запустить", "установщик .exe"),
            ("Add PATH", "поставить галочку"),
            ("Проверить", "python --version"),
        ],
        caption="Четыре шага установки Python на Windows",
    )

    body = f"""
    <p>На Windows есть два официальных пути поставить Python: классический установщик
    <code class="inline">.exe</code>, который существует уже много лет, и новый
    <strong>Python install manager</strong> — облегчённый инструмент для управления несколькими
    версиями Python, который Python Software Foundation продвигает как основной способ установки
    на Windows начиная с недавних релизов. Traditional-установщик <strong>остаётся доступным на
    протяжении веток 3.14 и 3.15</strong>, так что оба варианта — не ошибка, а два официальных
    пути.</p>

{callout(
        "tip",
        "[[icon:code]] Для этого курса",
        "Мы будем использовать классический установщик <code class=\"inline\">.exe</code> — он "
        "нагляднее для первого знакомства и даёт точь-в-точь тот же результат: работающую команду "
        "<code class=\"inline\">python</code> в терминале.",
    )}

    <h2 id="skachat">Шаг 1. Скачайте установщик</h2>
    <p>Откройте <strong>python.org/downloads</strong> — единственный источник, которому стоит
    доверять при загрузке Python. Сайт сам определяет вашу операционную систему и предлагает
    актуальную стабильную версию.</p>

{image_figure(
        f"{IMG}/screenshots/python-org-windows-downloads.jpg",
        "Страница загрузки Python для Windows на python.org",
        "python.org/downloads/windows — официальная страница загрузки для Windows.",
    )}

{callout(
        "security",
        "[[icon:warning]] Скачивайте только с python.org",
        "Сторонние сайты иногда предлагают «удобные» установщики Python с добавленным "
        "рекламным ПО. Официальный установщик — бесплатный, безопасный и всегда доступен "
        "напрямую на python.org.",
    )}

    <h2 id="ustanovka">Шаг 2. Запустите установщик</h2>
    <p>Запустите скачанный файл. На первом экране установщика — самая важная галочка во всей
    установке:</p>

{callout(
        "warning",
        "[[icon:debug]] Не пропустите: «Add python.exe to PATH»",
        "Внизу первого экрана установщика есть флажок <strong>Add python.exe to PATH</strong>. "
        "Обязательно поставьте его. Если пропустить этот шаг, Python установится, но команда "
        "<code class=\"inline\">python</code> в терминале работать не будет — а причина будет "
        "совершенно не очевидна, если вы ещё не знаете, что такое PATH (мы разбирали это в "
        "разделе 2.2).",
    )}

    <p>Затем нажмите <strong>Install Now</strong> для стандартной установки — она подходит для
    подавляющего большинства случаев и устанавливает Python, pip и стандартную библиотеку в папку
    профиля пользователя.</p>

{steps}

    <h2 id="proverka">Шаг 3. Проверьте установку</h2>
    <p>Откройте PowerShell (или обычную командную строку) и введите:</p>

{code_block("PowerShell", "python --version", lang="text")}

    <p>Вы должны увидеть что-то вроде <code class="inline">Python 3.14.7</code>. Если вместо
    этого терминал отвечает, что команда не распознана — скорее всего, вы пропустили галочку
    «Add python.exe to PATH». Решение — запустить установщик заново и выбрать
    <strong>Modify</strong>, снова отметив эту опцию, либо переустановить с нуля.</p>

{callout(
        "debug",
        "[[icon:debug]] python или py?",
        "На Windows часто работает ещё и команда <code class=\"inline\">py</code> — это отдельный "
        "«лаунчер Python», который штатно ставится вместе с интерпретатором и умеет запускать "
        "нужную версию, даже если их установлено несколько (например, "
        "<code class=\"inline\">py -3.14</code>). Для этого курса используйте "
        "<code class=\"inline\">python</code> — но не пугайтесь, если увидите "
        "<code class=\"inline\">py</code> в чужих инструкциях.",
    )}

    <h2 id="ne-trogat-store">Про Microsoft Store</h2>
    <p>В Microsoft Store тоже есть Python — это официальный пакет, но у него есть особенности
    работы с правами доступа к файлам, которые иногда удивляют новичков. Для этого курса
    рекомендуем установщик с python.org — он предсказуемее и ближе к тому, с чем вы столкнётесь
    на реальных проектах и других операционных системах.</p>"""

    out = render_page(
        page_title="Установка на Windows",
        description="Пошаговая установка Python на Windows: официальный установщик, галочка "
        "Add PATH и проверка через python --version.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("Установка на Windows", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="Установка Python на Windows",
        lede="Четыре шага: скачать с python.org, поставить галочку PATH, установить, проверить.",
        body_html=body,
        sidebar_groups=sidebar("02-02-windows.html"),
        nav=PageNav(prev_href="02-04-terminal-shell-i-path.html", prev_label="Терминал, shell и PATH", next_href="02-03-mac.html", next_label="Установка на macOS"),
    )
    write("02-02-windows.html", out)


def build_03_mac() -> None:
    body = f"""
    <p>На macOS уже есть предустановленный Python — но это <strong>системный Python</strong>,
    который использует сама операционная система для своих внутренних скриптов. Устанавливать
    в него сторонние пакеты или полагаться на его версию для учебных и рабочих проектов —
    плохая идея: система может обновить или использовать его непредсказуемым образом, и вы легко
    можете что-то сломать в macOS.</p>

{callout(
        "warning",
        "[[icon:warning]] Не трогайте системный Python",
        "Никогда не устанавливайте пакеты «поверх» системного Python на macOS "
        "(<code class=\"inline\">/usr/bin/python3</code>) и не удаляйте его. Вместо этого "
        "поставьте отдельную, «вашу собственную» версию Python с python.org — так делают "
        "профессиональные разработчики.",
    )}

    <h2 id="skachat-mac">Шаг 1. Скачайте установщик</h2>
    <p>Откройте <strong>python.org/downloads/macos</strong>. Официальный установщик для macOS —
    <strong>универсальный (universal2)</strong> пакет <code class="inline">.pkg</code>: один и тот
    же файл работает и на Mac с процессором Apple Silicon (M1/M2/M3/M4), и на Mac с процессором
    Intel.</p>

{image_figure(
        f"{IMG}/screenshots/python-org-macos-downloads.jpg",
        "Страница загрузки Python для macOS на python.org",
        "python.org/downloads/macos — официальная страница загрузки для macOS.",
    )}

    <h2 id="ustanovka-mac">Шаг 2. Запустите установщик</h2>
    <p>Откройте скачанный <code class="inline">.pkg</code>-файл и пройдите стандартный мастер
    установки macOS (Введение → Лицензия → Место установки → Установка). В отличие от Windows,
    здесь нет отдельной галочки про PATH — установщик macOS сам настраивает всё необходимое.</p>

    <h2 id="proverka-mac">Шаг 3. Проверьте установку</h2>
    <p>Откройте приложение <strong>Terminal</strong> и введите:</p>

{code_block("zsh", "python3 --version", lang="text")}

{callout(
        "info",
        "[[icon:idea]] Почему python3, а не python?",
        "На macOS (и на Linux) команда <code class=\"inline\">python</code> часто вообще не "
        "существует или указывает на устаревший системный Python 2 — исторически так сложилось "
        "для совместимости со старыми системными скриptами. Поэтому официальный установщик "
        "python.org ставит команду именно как <code class=\"inline\">python3</code>. Мы разберём, "
        "как сделать команду <code class=\"inline\">python</code> удобной внутри виртуального "
        "окружения, в разделе 2.10.",
    )}

    <p>Вы должны увидеть что-то вроде <code class="inline">Python 3.14.7</code>. Если терминал
    показывает более старую версию (например, <code class="inline">Python 3.9.6</code>) — это,
    вероятно, встроенный системный Python, а не тот, что вы только что установили; проверьте, что
    вводите именно <code class="inline">python3</code>, а не одну из более старых команд вроде
    <code class="inline">/usr/bin/python3</code> напрямую.</p>"""

    out = render_page(
        page_title="Установка на macOS",
        description="Установка Python на macOS через официальный universal2-установщик и "
        "почему не стоит трогать системный Python.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("Установка на macOS", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="Установка Python на macOS",
        lede="Официальный универсальный установщик — и почему системный Python лучше не трогать.",
        body_html=body,
        sidebar_groups=sidebar("02-03-mac.html"),
        nav=PageNav(prev_href="02-02-windows.html", prev_label="Установка на Windows", next_href="02-05-linux.html", next_label="Установка на Linux"),
    )
    write("02-03-mac.html", out)


def build_05_linux() -> None:
    body = f"""
    <p>Linux — такая же первоклассная платформа для Python, как Windows и macOS, и во многих
    профессиональных командах именно Linux — основная рабочая система (а ещё почти все серверы,
    на которых работает ваш будущий код, тоже Linux). Как и macOS, большинство дистрибутивов
    Linux уже включают системный Python — и здесь действует то же правило: <strong>не трогайте
    системный Python</strong>.</p>

{callout(
        "warning",
        "[[icon:warning]] PEP 668: «externally-managed-environment»",
        "На современных дистрибутивах (Ubuntu 23.04+, Debian 12+ и других) команда "
        "<code class=\"inline\">pip install</code> без виртуального окружения специально "
        "<strong>откажется работать</strong> и покажет ошибку "
        "<code class=\"inline\">error: externally-managed-environment</code>. Это не баг — это "
        "защита, описанная в официальном стандарте PEP 668, чтобы вы случайно не сломали "
        "системные инструменты, которые тоже написаны на Python. Правильный ответ на эту ошибку "
        "— не «обойти» её флагом, а создать виртуальное окружение (раздел 2.10) и ставить пакеты "
        "туда.",
    )}

    <h2 id="ustanovka-linux">Установка через менеджер пакетов</h2>
    <p>На Linux Python принято устанавливать через системный менеджер пакетов дистрибутива, а не
    скачивать установщик отдельно — это стандартный, официально рекомендуемый способ.</p>

{code_block("Debian / Ubuntu", "sudo apt update\nsudo apt install python3 python3-venv python3-pip", lang="text")}
{code_block("Fedora", "sudo dnf install python3 python3-pip", lang="text")}
{code_block("Arch Linux", "sudo pacman -S python python-pip", lang="text")}

{callout(
        "info",
        "[[icon:idea]] Зачем отдельно ставить python3-venv?",
        "На Debian/Ubuntu модуль для создания виртуальных окружений иногда выносят в отдельный "
        "пакет <code class=\"inline\">python3-venv</code> — без него команда "
        "<code class=\"inline\">python3 -m venv</code> (раздел 2.11) не сработает. Если вы "
        "планируете использовать виртуальные окружения (а мы будем), поставьте его сразу.",
    )}

    <h2 id="proverka-linux">Проверка установки</h2>
{code_block("bash", "python3 --version\npip3 --version", lang="text")}

    <h2 id="pochemu-ne-trogat">Почему это так строго на Linux</h2>
    <p>Сама операционная система на Linux нередко написана частично на Python и использует
    системный интерпретатор для своих инструментов (менеджера пакетов, системных утилит). Если
    вы командой <code class="inline">pip install</code> без окружения замените версию библиотеки,
    от которой зависит сама система, — можно сломать что-то важное в ОС. PEP 668 — это
    общеотраслевой стандарт, который защищает именно от этого сценария, а не прихоть конкретного
    дистрибутива.</p>

{callout(
        "tip",
        "[[icon:launch]] Практический вывод",
        "На Linux правило «всегда работайте внутри виртуального окружения» — не совет, а во "
        "многих случаях техническое требование. Хорошая новость: как только вы освоите "
        "виртуальные окружения (раздел 2.10–2.12), это правило станет привычкой, а не "
        "препятствием.",
    )}"""

    out = render_page(
        page_title="Установка на Linux",
        description="Установка Python на Linux через менеджер пакетов дистрибутива и почему "
        "PEP 668 запрещает pip install в системный Python.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("Установка на Linux", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="Установка Python на Linux",
        lede="Linux — полноценная платформа первого класса для Python, со своими правилами "
        "хорошего тона: системный менеджер пакетов и обязательные виртуальные окружения.",
        body_html=body,
        sidebar_groups=sidebar("02-05-linux.html"),
        nav=PageNav(prev_href="02-03-mac.html", prev_label="Установка на macOS", next_href="02-06-kakoj-python-zapushen.html", next_label="Какой Python действительно запущен"),
    )
    write("02-05-linux.html", out)


def build_06_which_python() -> None:
    body = f"""
    <p>Если на компьютере может быть несколько Python (системный + установленный вами, а позже
    ещё и виртуальные окружения), рано или поздно встаёт вопрос: <strong>какой именно Python
    сейчас запускается командой <code class="inline">python</code></strong>? Хорошая новость —
    сам Python умеет отвечать на этот вопрос.</p>

    <h2 id="sys-executable">sys.executable — самый честный ответ</h2>
    <p>Каждый запущенный интерпретатор Python знает точный путь к своему собственному
    исполняемому файлу. Он хранится в переменной <code class="inline">sys.executable</code>.</p>

{code_block("python", 'import sys\nprint(sys.executable)\nprint(sys.version)')}

    <p>Запустите это двумя способами и сравните результат — из обычного терминала и (когда
    дойдём до VS Code, раздел 2.8) из встроенного терминала редактора. Если пути отличаются —
    значит, в этих двух местах запускаются <em>разные</em> интерпретаторы, и это многое объясняет,
    если пакет «установлен», а импорт всё равно падает (см. диагностику в разделе 2.16).</p>

    <h2 id="which-where">which / where — короткая версия из терминала</h2>
    <p>Не запуская Python вовсе, можно спросить у самого shell, какой файл он найдёт первым по
    PATH (вспомните раздел 2.2):</p>

{code_block("macOS / Linux", "which python3", lang="text")}
{code_block("Windows (PowerShell)", "where.exe python", lang="text")}

{callout(
        "debug",
        "[[icon:debug]] Лаборатория: «два Python»",
        "Если на вашем компьютере одновременно есть системный Python и Python с python.org, "
        "выполните <code class=\"inline\">which python3</code> (или "
        "<code class=\"inline\">where.exe python</code>) и сравните путь с тем, что печатает "
        "<code class=\"inline\">sys.executable</code> изнутри Python. Они должны совпадать — если "
        "нет, значит переменная PATH ссылается не на тот интерпретатор, который вы ожидали.",
    )}

{callout(
        "info",
        "[[icon:note]] Официальный источник",
        "Подробнее про <code class=\"inline\">sys.executable</code> и <code class=\"inline\">sys.version</code> "
        "— в модуле <code class=\"inline\">sys</code> на docs.python.org.",
    )}"""

    out = render_page(
        page_title="Какой Python действительно запущен",
        description="Как узнать точный путь к работающему интерпретатору через sys.executable "
        "и команды which/where.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("Какой Python запущен", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="Какой Python действительно запущен",
        lede="Один и тот же вопрос спасёт вас от половины будущих проблем с окружениями: "
        "«а какой именно интерпретатор сейчас работает?»",
        body_html=body,
        sidebar_groups=sidebar("02-06-kakoj-python-zapushen.html"),
        nav=PageNav(prev_href="02-05-linux.html", prev_label="Установка на Linux", next_href="02-07-vscode-ustanovka-i-rasshireniya.html", next_label="VS Code: установка и расширения"),
    )
    write("02-06-kakoj-python-zapushen.html", out)


def build_07_vscode_install() -> None:
    ext_table = comparison_table(
        ["Расширение", "Издатель", "Зачем нужно", "Статус"],
        [
            ["Python", "Microsoft", "Базовая поддержка языка: подсветка, запуск, отладка, выбор интерпретатора", "Обязательно"],
            ["Pylance", "Microsoft", "Быстрый анализ кода, автодополнение, подсказки типов", "Ставится автоматически вместе с Python"],
            ["Python Debugger", "Microsoft", "Отдельный движок пошаговой отладки (breakpoints, шаг за шагом)", "Ставится автоматически вместе с Python"],
            ["Python Environments", "Microsoft", "Новый интерфейс создания и переключения виртуальных окружений", "Ставится автоматически вместе с Python"],
            ["Jupyter", "Microsoft", "Работа с блокнотами .ipynb внутри VS Code", "Рекомендуется"],
            ["Ruff", "Astral Software", "Мгновенная проверка стиля и авто-форматирование кода", "Рекомендуется"],
        ],
    )

    body = f"""
    <p>VS Code (Visual Studio Code) — бесплатный редактор кода от Microsoft. Сам по себе, «из
    коробки», он ничего не знает о Python — это универсальный текстовый редактор для десятков
    языков. Понимание Python ему дают <strong>расширения</strong> (extensions) — отдельные
    маленькие плагины, которые вы устанавливаете поверх редактора.</p>

{callout(
        "tip",
        "[[icon:idea]] Расширение ≠ пакет",
        "Это разные вещи, хоть слова и похожи. <strong>Расширение VS Code</strong> — плагин, "
        "который устанавливается в сам редактор и добавляет ему новые возможности (подсветку "
        "синтаксиса, автодополнение). <strong>Пакет Python</strong> (раздел 2.12) — библиотека "
        "кода, которую вы устанавливаете через pip внутрь конкретного окружения, чтобы "
        "использовать её функции в своей программе. Расширения не видят и не заменяют пакеты, и "
        "наоборот.",
    )}

    <h2 id="ustanovka-vscode">Установка VS Code</h2>
    <p>Скачайте установщик с официального сайта <strong>code.visualstudio.com</strong> для вашей
    операционной системы и пройдите обычный мастер установки — здесь нет особых ловушек вроде
    флажка PATH из раздела 2.3.</p>

    <h2 id="rasshirenie-python">Расширение Python — и что оно ставит само</h2>
    <p>Откройте вкладку Extensions (значок из четырёх квадратов на боковой панели, или
    <code class="inline">Ctrl+Shift+X</code>) и найдите расширение <strong>Python</strong> от
    Microsoft.</p>

{image_figure(
        f"{IMG}/screenshots/vscode-marketplace-python.jpg",
        "Страница расширения Python (Microsoft) в VS Code Marketplace",
        "Официальное расширение Python от Microsoft на VS Code Marketplace — свыше 232 млн установок.",
    )}

    <p>Когда вы устанавливаете это расширение, VS Code Marketplace автоматически подтягивает ещё
    три расширения вместе с ним:</p>
    <ul>
      <li><strong>Pylance</strong> — быстрый анализатор кода (автодополнение, подсказки типов,
        переход к определению);</li>
      <li><strong>Python Debugger</strong> — отдельный движок для пошаговой отладки;</li>
      <li><strong>Python Environments</strong> — новый интерфейс для создания и переключения
        виртуальных окружений прямо из VS Code.</li>
    </ul>

    <h2 id="jupyter-ext">Расширение Jupyter</h2>
    <p>Если вы планируете работать с блокнотами (notebooks, файлы <code class="inline">.ipynb</code>
    — с ними мы уже встречались в интерактивной практике этого курса), понадобится расширение
    <strong>Jupyter</strong>.</p>

{image_figure(
        f"{IMG}/screenshots/vscode-marketplace-jupyter.jpg",
        "Страница расширения Jupyter в VS Code Marketplace",
        "Официальное расширение Jupyter от Microsoft — свыше 108 млн установок.",
    )}

{callout(
        "info",
        "[[icon:idea]] Расширение Jupyter — это не сам Jupyter",
        "Разработчики честно предупреждают на странице расширения: это <strong>не ядро "
        "Jupyter</strong> (not a Jupyter kernel). Расширение — это только интерфейс внутри "
        "VS Code; чтобы реально запускать блокноты, нужно ещё и окружение Python с установленным "
        "пакетом <code class=\"inline\">jupyter</code> (раздел 2.15) — точно так же, как редактор "
        "и интерпретатор разделены в разделе 2.1.",
    )}

    <h2 id="ruff-ext">Расширение Ruff</h2>
    <p>Ruff — стремительно ставший стандартом инструмент проверки и форматирования кода от
    Astral Software (создателей uv, раздел 2.13). Он заменяет собой сразу несколько старых
    инструментов — Flake8, Black, isort — одним быстрым.</p>

{image_figure(
        f"{IMG}/screenshots/vscode-marketplace-ruff.jpg",
        "Страница расширения Ruff в VS Code Marketplace",
        "Официальное расширение Ruff от Astral Software — свыше 4,3 млн установок.",
    )}

    <h2 id="tablica-rasshirenij">Что ставить: сводная таблица</h2>
{ext_table}

{callout(
        "tip",
        "[[icon:launch]] Минимальный набор для этого курса",
        "Достаточно поставить одно расширение <strong>Python</strong> — оно автоматически "
        "подтянет Pylance, Python Debugger и Python Environments. Jupyter и Ruff — по желанию, "
        "но мы рекомендуем оба.",
    )}"""

    out = render_page(
        page_title="VS Code: установка и расширения",
        description="Установка VS Code и разбор расширений Python, Pylance, Python Debugger, "
        "Python Environments, Jupyter и Ruff — что каждое из них реально делает.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("VS Code: установка и расширения", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="VS Code: установка и расширения",
        lede="VS Code сам по себе не понимает Python — эту способность ему дают расширения. "
        "Разберём, что ставить и зачем каждое из них нужно.",
        body_html=body,
        sidebar_groups=sidebar("02-07-vscode-ustanovka-i-rasshireniya.html"),
        nav=PageNav(prev_href="02-06-kakoj-python-zapushen.html", prev_label="Какой Python запущен", next_href="02-08-vscode-konfiguraciya.html", next_label="VS Code: интерпретатор и рабочий процесс"),
    )
    write("02-07-vscode-ustanovka-i-rasshireniya.html", out)


def build_08_vscode_config() -> None:
    body = f"""
    <p>Установленное расширение Python ещё не знает, <em>какой именно</em> интерпретатор
    использовать для вашего проекта — особенно если на компьютере их несколько (системный,
    с python.org, а скоро ещё и виртуальные окружения). Это нужно указать явно — один раз на
    проект.</p>

    <h2 id="vybor-interpretatora">Выбор интерпретатора</h2>
    <p>Откройте папку проекта в VS Code, затем откройте любой файл <code class="inline">.py</code>.
    В правом нижнем углу окна появится надпись с текущей выбранной версией Python — нажмите на
    неё (или откройте палитру команд <code class="inline">Ctrl+Shift+P</code> / <code class="inline">Cmd+Shift+P</code>
    и наберите «Python: Select Interpreter»).</p>

    <p>Появится список всех интерпретаторов, которые VS Code нашёл на компьютере — с полными
    путями к каждому. Выберите нужный.</p>

{callout(
        "tip",
        "[[icon:idea]] Проверка боем",
        "Выбранный интерпретатор должен совпадать с тем путём, что печатает "
        "<code class=\"inline\">sys.executable</code> (раздел 2.6), если запустить файл через "
        "VS Code. Откройте встроенный терминал VS Code (<code class=\"inline\">Ctrl+`</code>) и "
        "сравните.",
    )}

    <h2 id="workspace-vs-user">USER-настройки и WORKSPACE-настройки</h2>
    <p>У VS Code есть два уровня настроек с одинаковыми именами полей, но разным охватом:</p>
    <ul>
      <li><strong>User settings</strong> — применяются ко всем проектам, которые вы открываете на
        этом компьютере;</li>
      <li><strong>Workspace settings</strong> — применяются только к текущей открытой папке
        (проекту) и хранятся в файле <code class="inline">.vscode/settings.json</code> внутри
        самого проекта.</li>
    </ul>

{converge_diagram(
        ["User settings\n(весь компьютер)", "Workspace settings\n(этот проект)"],
        "settings.json проекта",
        caption="Выбор интерпретатора привязывается к проекту, а не «навсегда» ко всему компьютеру",
    )}

    <p>Когда вы выбираете интерпретатор через «Select Interpreter», выбор привязывается именно к
    этому проекту, а не «навсегда» ко всему компьютеру — у разных проектов на компьютере вполне
    может быть разный Python. Технически расширение <strong>Python Environments</strong> (мы
    ставили его вместе с расширением Python в разделе 2.7) хранит это назначение в
    <code class="inline">.vscode/settings.json</code> проекта — но не как прямой путь к файлу, а
    как ссылку на нужное окружение, которую расширение само находит заново при каждом
    открытии проекта:</p>

{code_block(
        ".vscode/settings.json",
        '{\n  "python-envs.pythonProjects": [\n    { "path": ".", "envManager": "ms-python.python:venv" }\n  ]\n}',
        lang="json",
    )}

{callout(
        "info",
        "[[icon:idea]] А как же python.defaultInterpreterPath?",
        "Более старая настройка <code class=\"inline\">python.defaultInterpreterPath</code> — "
        "это не запись о вашем выборе, а <strong>запасной вариант</strong>: расширение читает её "
        "только тогда, когда для проекта ещё не назначено никакое окружение никаким другим "
        "способом. Ручной выбор через «Select Interpreter» её не создаёт и не изменяет — поэтому "
        "не удивляйтесь, если не найдёте эту строку в своём <code class=\"inline\">settings.json</code> "
        "даже после того, как выбрали интерпретатор.",
    )}

    <h2 id="terminal-vscode">Встроенный терминал</h2>
    <p>Терминал внутри VS Code (<code class="inline">Ctrl+`</code>) — это тот же самый shell, что
    и обычный терминал операционной системы (раздел 2.2), просто открытый прямо внутри редактора,
    в папке проекта. Когда у проекта выбрано виртуальное окружение, VS Code обычно
    <strong>автоматически активирует его</strong> в новом встроенном терминале — вы увидите
    <code class="inline">(.venv)</code> перед приглашением командной строки (подробнее в разделе
    2.11).</p>

    <h2 id="zapusk-i-otladka">Запуск и отладка файла</h2>
    <p>Кнопка ▷ («Run Python File») в правом верхнем углу запускает текущий файл именно тем
    интерпретатором, который выбран для проекта. Кнопка отладки (значок с жуком) делает то же
    самое, но позволяет ставить точки останова (breakpoints) — кликом слева от номера строки — и
    останавливать выполнение построчно, чтобы увидеть текущие значения переменных.</p>

{callout(
        "debug",
        "[[icon:debug]] «Run» использует не тот Python»",
        "Если запуск файла через VS Code ведёт себя иначе, чем запуск того же файла в обычном "
        "терминале — почти всегда причина в том, что выбран не тот интерпретатор. Откройте "
        "«Select Interpreter» ещё раз и сравните выбранный путь с тем, что печатает "
        "<code class=\"inline\">sys.executable</code> (раздел 2.6).",
    )}"""

    out = render_page(
        page_title="VS Code: интерпретатор и рабочий процесс",
        description="Выбор интерпретатора для проекта в VS Code, разница между User- и "
        "Workspace-настройками, встроенный терминал, запуск и отладка.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("VS Code: интерпретатор", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="VS Code: интерпретатор и рабочий процесс",
        lede="Расширение установлено — но VS Code ещё не знает, какой Python использовать для "
        "вашего конкретного проекта. Разберём, как это указать и как это устроено.",
        body_html=body,
        sidebar_groups=sidebar("02-08-vscode-konfiguraciya.html"),
        nav=PageNav(prev_href="02-07-vscode-ustanovka-i-rasshireniya.html", prev_label="VS Code: установка и расширения", next_href="02-09-pycharm.html", next_label="PyCharm"),
    )
    write("02-08-vscode-konfiguraciya.html", out)


def build_09_pycharm() -> None:
    body = f"""
    <p>PyCharm (компания JetBrains) — специализированная среда разработки (IDE) именно для
    Python, в отличие от VS Code, который универсален и понимает Python через расширения.
    Начиная с версии 2025.1 PyCharm — это <strong>единый продукт</strong>: прежнего деления на
    Community- и Professional-редакции больше нет. Основные, «повседневные» возможности (включая
    поддержку Jupyter-блокнотов) бесплатны для всех, а платная подписка <strong>Pro</strong>
    добавляет более продвинутые инструменты (например, для веб-разработки и баз данных); при
    первой установке каждому пользователю даётся бесплатный пробный период Pro. Для этого курса
    полностью достаточно бесплатных возможностей.</p>

{callout(
        "info",
        "[[icon:note]] Если встретите «PyCharm Community» в старых материалах",
        "До объединения в 2025 году у PyCharm действительно были отдельные редакции Community и "
        "Professional — вы ещё можете встретить эти названия в старых статьях и видео. Сути это "
        "не меняет: бесплатные базовые возможности сегодняшнего PyCharm — прямой преемник "
        "прежней Community-редакции.",
    )}

{callout(
        "info",
        "[[icon:idea]] IDE ≠ интерпретатор",
        "Как и с VS Code (раздел 2.1): PyCharm сам не является Python-интерпретатором. Это "
        "программа, которая находит на компьютере уже установленный интерпретатор (или помогает "
        "создать новое виртуальное окружение) и использует его для запуска и анализа вашего кода.",
    )}

    <h2 id="proekt-i-interpretator">Проект и его интерпретатор</h2>
    <p>В PyCharm единица работы — <strong>проект</strong> (Project): папка с кодом плюс
    настройки, привязанные именно к ней. При создании нового проекта PyCharm сразу спрашивает,
    какой интерпретатор использовать, и предлагает удобную кнопку — создать новое виртуальное
    окружение специально для этого проекта (мы разберём, что это значит, в разделе 2.10).</p>

    <p>Изменить интерпретатор позже можно через
    <strong>Settings → Project → Python Interpreter</strong> — там же виден полный список всех
    пакетов, установленных в текущее окружение, что удобно для быстрой проверки.</p>

    <h2 id="plaginy-pycharm">Плагины PyCharm</h2>
    <p>Как и у VS Code, у PyCharm есть система плагинов — но большая часть базовой поддержки
    Python в нём уже встроена «из коробки», без установки дополнительных расширений. Через
    <strong>Settings → Plugins</strong> можно добавить поддержку других языков и инструментов;
    поддержка Jupyter-блокнотов в единый продукт PyCharm тоже входит бесплатно.</p>

    <h2 id="vscode-vs-pycharm">VS Code или PyCharm?</h2>
{comparison_table(
        ["", "VS Code", "PyCharm (бесплатные возможности)"],
        [
            ["Что это", "Универсальный редактор + расширения", "IDE специально для Python"],
            ["Поддержка Python", "Через расширения (раздел 2.7)", "Встроена изначально"],
            ["Вес и скорость запуска", "Легче", "Тяжелее"],
            ["Другие языки", "Отлично — десятки языков", "В основном Python (+плагины)"],
            ["Для этого курса", "Рекомендуем", "Тоже подходит"],
        ],
    )}

{callout(
        "tip",
        "[[icon:launch]] Какой выбрать",
        "Оба варианта — правильный выбор, и оба используются профессионалами. Если вы уже "
        "работали в VS Code — оставайтесь в нём. Если хочется среды, «заточенной» только под "
        "Python из коробки, — попробуйте PyCharm: для этого курса хватит его бесплатных "
        "возможностей, без подписки Pro. Материалы курса не зависят от выбора редактора.",
    )}"""

    out = render_page(
        page_title="PyCharm: проект, интерпретатор, окружение",
        description="Модель работы PyCharm: проекты, интерпретаторы, плагины — и сравнение с "
        "VS Code для выбора редактора.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("PyCharm", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="PyCharm: проект, интерпретатор, окружение",
        lede="Специализированная IDE для Python — с другой моделью работы, чем у VS Code, но "
        "теми же базовыми идеями внутри.",
        body_html=body,
        sidebar_groups=sidebar("02-09-pycharm.html"),
        nav=PageNav(prev_href="02-08-vscode-konfiguraciya.html", prev_label="VS Code: интерпретатор", next_href="02-10-zachem-nuzhny-venv.html", next_label="Виртуальные окружения — зачем они нужны"),
    )
    write("02-09-pycharm.html", out)


def build_10_why_venv() -> None:
    body = f"""
    <p>Прежде чем показывать команду для создания виртуального окружения, разберём, зачем оно
    вообще нужно — на конкретной проблеме, с которой рано или поздно сталкивается каждый.</p>

    <h2 id="problema">Представьте такую ситуацию</h2>
    <p>Вы работаете над двумя проектами на одном компьютере:</p>
    <ul>
      <li><strong>Проект А</strong> — старый учебный проект, который использует библиотеку
        <code class="inline">requests</code> версии 2.25 (написан давно, и обновлять его пока
        незачем);</li>
      <li><strong>Проект Б</strong> — новый проект, для которого нужна свежая
        <code class="inline">requests</code> версии 2.32 — там есть функции, которых не было в
        старой версии.</li>
    </ul>
    <p>Если бы существовал только один, общий на весь компьютер Python со своим единственным
    набором пакетов — установить сразу обе версии одной и той же библиотеки было бы невозможно.
    Установка новой версии для проекта Б автоматически сломала бы проект А.</p>

{callout(
        "warning",
        "[[icon:warning]] Это не гипотетический сценарий",
        "Ровно эта проблема — главная причина, по которой виртуальные окружения стали "
        "стандартом в мире Python. Без них любые два проекта на одном компьютере вынуждены "
        "делить одни и те же версии всех библиотек — а любое обновление одного проекта рискует "
        "тихо сломать другой.",
    )}

    <h2 id="reshenie">Решение: своя копия окружения для каждого проекта</h2>
    <p><strong>Виртуальное окружение</strong> (virtual environment, сокращённо venv) — это лёгкая,
    изолированная «копия» интерпретатора Python вместе с собственным, отдельным набором
    установленных пакетов, привязанная к одному конкретному проекту.</p>

{branch_diagram(
        "Один и тот же Python на компьютере",
        [
            (".venv проекта А", "requests 2.25, только для проекта А"),
            (".venv проекта Б", "requests 2.32, только для проекта Б"),
        ],
        caption="Каждый проект получает свою изолированную копию — версии пакетов не конфликтуют",
    )}

    <p>Технически это не полная копия самого интерпретатора (не тратится гигабайт места на
    каждый проект) — venv переиспользует основной установленный Python, но заводит для проекта
    отдельную, независимую папку с пакетами. Для вас как для разработчика разница неощутима:
    внутри активированного окружения пакеты, установленные для одного проекта, попросту не видны
    другому.</p>

{callout(
        "tip",
        "[[icon:idea]] Аналогия",
        "Виртуальное окружение — как отдельный, промаркированный ящик с инструментами для "
        "каждого проекта, а не одна общая полка на всех. Взяли молоток из ящика проекта А — "
        "проект Б об этом даже не узнает.",
    )}

    <h2 id="ne-tolko-versii">Не только про конфликты версий</h2>
    <p>У виртуальных окружений есть и другие практические плюсы:</p>
    <ul>
      <li><strong>Воспроизводимость</strong> — список пакетов проекта можно сохранить в файл и
        точно восстановить такое же окружение на другом компьютере;</li>
      <li><strong>Чистота</strong> — удалить окружение проекта так же просто, как удалить одну
        папку, не затрагивая остальную систему;</li>
      <li><strong>Безопасность системы</strong> — на macOS и особенно на Linux (раздел 2.5) это
        ещё и способ вообще не трогать системный Python.</li>
    </ul>

    <p>В следующем разделе — команда для создания окружения и разбор того, что она реально
    создаёт на диске.</p>"""

    out = render_page(
        page_title="Виртуальные окружения — зачем они нужны",
        description="Проблема-первым объяснение виртуальных окружений: зачем нужна изолированная "
        "копия Python и набора пакетов для каждого проекта.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("Зачем нужны venv", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="Виртуальные окружения — зачем они нужны",
        lede="Прежде чем вводить команду создания окружения — разберём проблему, которую оно "
        "решает. Без этого команда — просто ещё одна строчка для заучивания наизусть.",
        body_html=body,
        sidebar_groups=sidebar("02-10-zachem-nuzhny-venv.html"),
        nav=PageNav(prev_href="02-09-pycharm.html", prev_label="PyCharm", next_href="02-11-sozdanie-venv.html", next_label="Создаём .venv"),
    )
    write("02-10-zachem-nuzhny-venv.html", out)


def build_11_create_venv() -> None:
    body = f"""
    <p>Теперь, когда понятно зачем — создадим первое виртуальное окружение. Модуль
    <code class="inline">venv</code> входит в стандартную библиотеку Python — отдельно ставить
    ничего не нужно (кроме Linux, где иногда требуется системный пакет
    <code class="inline">python3-venv</code>, см. раздел 2.5).</p>

    <h2 id="sozdanie">Создание окружения</h2>
    <p>Откройте терминал в папке вашего проекта и выполните:</p>

{code_block("Windows / macOS / Linux", "python -m venv .venv", lang="text")}

{callout(
        "info",
        "[[icon:idea]] Что означает точка перед именем",
        "Имя <code class=\"inline\">.venv</code> начинается с точки — на macOS и Linux это "
        "стандартное соглашение для «скрытых» файлов и папок: обычный файловый менеджер и "
        "команда <code class=\"inline\">ls</code> без флагов их не показывают, чтобы не "
        "загромождать список служебными файлами. Папку можно назвать и без точки (например, "
        "просто <code class=\"inline\">venv</code>), но <code class=\"inline\">.venv</code> — "
        "самое распространённое соглашение, и его же по умолчанию узнают VS Code и PyCharm.",
    )}

    <h2 id="chto-vnutri">Что появилось на диске</h2>
    <p>Команда создала папку <code class="inline">.venv</code> со своей внутренней структурой:</p>

{code_block(
        ".venv/ (macOS / Linux)",
        ".venv/\n"
        "├── bin/\n"
        "│   ├── python -> /usr/local/bin/python3.14\n"
        "│   ├── pip\n"
        "│   └── activate\n"
        "├── lib/\n"
        "│   └── python3.14/site-packages/\n"
        "└── pyvenv.cfg",
        lang="text",
    )}

{code_block(
        ".venv\\ (Windows)",
        ".venv\\\n"
        "├── Scripts\\\n"
        "│   ├── python.exe\n"
        "│   ├── pip.exe\n"
        "│   └── activate.bat\n"
        "├── Lib\\\n"
        "│   └── site-packages\\\n"
        "└── pyvenv.cfg",
        lang="text",
    )}

    <p>Главное здесь — <code class="inline">site-packages</code>: именно сюда попадут пакеты,
    которые вы установите для этого проекта, и именно эта папка изолирована от других проектов
    (раздел 2.10). Файл <code class="inline">pyvenv.cfg</code> хранит ссылку на «родительский»
    интерпретатор, из которого было создано окружение.</p>

    <h2 id="aktivaciya">Активация окружения</h2>
    <p>Само по себе создание окружения ещё не значит, что оно используется — его нужно
    <strong>активировать</strong> в текущем терминале:</p>

{code_block("macOS / Linux (bash/zsh)", "source .venv/bin/activate", lang="text")}
{code_block("Windows (PowerShell)", ".venv\\Scripts\\Activate.ps1", lang="text")}
{code_block("Windows (cmd.exe)", ".venv\\Scripts\\activate.bat", lang="text")}

    <p>После активации приглашение командной строки изменится — перед ним появится
    <code class="inline">(.venv)</code>. Это визуальный сигнал: теперь команды
    <code class="inline">python</code> и <code class="inline">pip</code> в этом терминале
    указывают именно на интерпретатор и пакеты этого окружения, а не на системный или глобально
    установленный Python.</p>

{code_block("Терминал после активации", "(.venv) anna@laptop project %", lang="text")}

{callout(
        "warning",
        "[[icon:warning]] Активация — на каждую новую вкладку/окно терминала",
        "Активация действует только в том окне терминала, где вы её выполнили. Открыли новую "
        "вкладку терминала — активируйте окружение заново. VS Code, как правило, делает это "
        "автоматически для встроенного терминала (раздел 2.8), если для проекта выбран этот "
        "интерпретатор.",
    )}

    <h2 id="deaktivaciya">Деактивация</h2>
    <p>Чтобы вернуться к обычному, «глобальному» состоянию терминала:</p>

{code_block("Любая ОС", "deactivate", lang="text")}

{exercise(
        1,
        "Создайте и активируйте своё первое окружение",
        "Создайте папку с любым именем, откройте в ней терминал, выполните "
        "<code class=\"inline\">python -m venv .venv</code>, активируйте его командой для вашей "
        "ОС и убедитесь, что приглашение командной строки изменилось на "
        "<code class=\"inline\">(.venv)</code>.",
    )}"""

    out = render_page(
        page_title="Создаём .venv",
        description="Команда python -m venv, структура папки .venv на диске, активация и "
        "деактивация окружения на Windows, macOS и Linux.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("Создаём .venv", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="Создаём .venv",
        lede="От команды — к тому, что реально появляется на диске, и как включить и "
        "выключить окружение.",
        body_html=body,
        sidebar_groups=sidebar("02-11-sozdanie-venv.html"),
        nav=PageNav(prev_href="02-10-zachem-nuzhny-venv.html", prev_label="Зачем нужны venv", next_href="02-12-pervyj-paket.html", next_label="Устанавливаем первый пакет"),
    )
    write("02-11-sozdanie-venv.html", out)


def build_12_first_package() -> None:
    body = f"""
    <p>С активированным окружением (раздел 2.11) можно установить первый пакет. Мы возьмём
    <code class="inline">requests</code> — популярную библиотеку для запросов к веб-серверам,
    её мы позже используем в проектах курса.</p>

    <h2 id="ustanovka-paketa">pip install</h2>
{code_block("Терминал (окружение активировано)", "(.venv) $ pip install requests", lang="text")}

    <p>pip скачивает пакет с <strong>PyPI</strong> (Python Package Index — мы знакомились с ним в
    главе 1) и распаковывает его прямо в <code class="inline">site-packages</code> вашего
    активного окружения (раздел 2.11).</p>

    <h2 id="proverka-paketa">Проверка установки</h2>
{code_block("Терминал", "pip show requests\npip list", lang="text")}

{code_block("python", 'import requests\nprint(requests.__version__)')}

    <h2 id="ustanovleno-no-ne-importiruetsya">Лаборатория: «Установлено, но import не работает»</h2>
    <p>Одна из самых частых и самых запутывающих проблем новичков: вы только что установили
    пакет, видите его в <code class="inline">pip list</code> — а <code class="inline">import</code>
    в коде всё равно выдаёт <code class="inline">ModuleNotFoundError</code>.</p>

{callout(
        "debug",
        "[[icon:debug]] Почти всегда причина одна",
        "Пакет установлен в <strong>одно</strong> окружение, а код запускается через "
        "<strong>другое</strong>. Например: вы активировали <code class=\"inline\">.venv</code> в "
        "терминале и поставили туда пакет — но VS Code запускает файл через глобальный "
        "интерпретатор, потому что для проекта выбран не тот Python (раздел 2.8).",
    )}

    <p>Порядок диагностики:</p>
    <ol>
      <li>Проверьте <code class="inline">sys.executable</code> (раздел 2.6) прямо из места,
        где падает импорт — какой интерпретатор реально используется?</li>
      <li>Проверьте, что приглашение терминала показывает <code class="inline">(.venv)</code> —
        окружение точно активировано?</li>
      <li>Выполните <code class="inline">pip show requests</code> в этом же терминале — пакет
        точно виден отсюда?</li>
      <li>Если вы в VS Code — откройте «Select Interpreter» (раздел 2.8) и убедитесь, что выбран
        путь именно к <code class="inline">.venv</code>, а не к системному или глобальному Python.</li>
    </ol>

{exercise(
        2,
        "Найдите и почините «два окружения»",
        "Создайте новое окружение <code class=\"inline\">.venv2</code> рядом с существующим "
        "<code class=\"inline\">.venv</code> (но не активируйте его). В активном "
        "<code class=\"inline\">.venv</code> установите <code class=\"inline\">requests</code>. "
        "Деактивируйте окружение, активируйте <code class=\"inline\">.venv2</code> и попробуйте "
        "<code class=\"inline\">import requests</code> — вы должны увидеть "
        "<code class=\"inline\">ModuleNotFoundError</code>. Это тот самый сценарий «установлено, "
        "но не импортируется» — только вы теперь понимаете, почему.",
    )}"""

    out = render_page(
        page_title="Устанавливаем первый пакет",
        description="pip install внутри активированного окружения и разбор частой проблемы: "
        "пакет установлен, но import не работает.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("Первый пакет", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="Устанавливаем первый пакет",
        lede="pip install — и диагностика самой частой ошибки новичков: «установлено, но "
        "почему-то не импортируется».",
        body_html=body,
        sidebar_groups=sidebar("02-12-pervyj-paket.html"),
        nav=PageNav(prev_href="02-11-sozdanie-venv.html", prev_label="Создаём .venv", next_href="02-13-pip-pipx-venv-virtualenv-uv.html", next_label="pip, pipx, venv, virtualenv, uv"),
    )
    write("02-12-pervyj-paket.html", out)


def build_13_pip_pipx_venv_uv() -> None:
    tool_table = comparison_table(
        ["Инструмент", "Что делает", "Устанавливает пакеты", "Создаёт окружения"],
        [
            ["<strong>pip</strong>", "Устанавливает пакеты в текущее активное окружение", "Да", "Нет"],
            ["<strong>venv</strong>", "Создаёт изолированные окружения (входит в стандартную библиотеку)", "Нет", "Да"],
            ["<strong>virtualenv</strong>", "Более старый и быстрый сторонний аналог venv", "Нет", "Да"],
            ["<strong>pipx</strong>", "Устанавливает CLI-приложения на Python глобально, каждое — в своё изолированное окружение", "Да (для приложений)", "Да (по одному на приложение, автоматически)"],
            ["<strong>uv</strong>", "Один быстрый инструмент, заменяющий pip, venv, virtualenv, pipx и другие", "Да", "Да"],
        ],
    )

    decision = flow_diagram(
        [
            ("Нужен пакет\nдля проекта?", "→ pip / uv pip"),
            ("Нужно новое\nокружение?", "→ venv / uv venv"),
            ("Нужна CLI-\nпрограмма?", "→ pipx / uv tool"),
        ],
        caption="Три частых вопроса и инструмент-ответ на каждый",
    )

    body = f"""
    <p>К этому моменту вы уже пользовались <code class="inline">pip</code> и
    <code class="inline">venv</code> (разделы 2.11–2.12). В экосистеме Python есть ещё несколько
    похожих по звучанию инструментов — разберём каждый отдельно, а не единым списком, чтобы не
    путать их друг с другом.</p>

    <h2 id="pip">pip</h2>
    <p><strong>pip</strong> устанавливает, обновляет и удаляет пакеты <em>в уже существующее
    активное окружение</em>. Он ничего не создаёт — только наполняет то, что уже есть.</p>
{code_block("Терминал", "pip install requests\npip install requests==2.31.0\npip uninstall requests", lang="text")}

    <h2 id="venv">venv</h2>
    <p><strong>venv</strong> — модуль стандартной библиотеки (раздел 2.11), который делает ровно
    одну вещь: создаёт новое изолированное окружение. Он входит в сам Python — устанавливать его
    отдельно не нужно.</p>

    <h2 id="virtualenv">virtualenv</h2>
    <p><strong>virtualenv</strong> — сторонний пакет, предшественник <code class="inline">venv</code>
    (модуль venv в стандартной библиотеке во многом вырос именно из него). Он решает ту же
    задачу, но исторически работает быстрее и поддерживает чуть больше сценариев (например,
    старые версии Python, где встроенного venv ещё не было). Для этого курса вам полностью
    хватит обычного <code class="inline">venv</code> — virtualenv стоит знать по имени, если
    встретите его в чужом проекте.</p>

    <h2 id="pipx">pipx</h2>
    <p><strong>pipx</strong> решает другую задачу — не «пакет для моего проекта», а «программа с
    интерфейсом командной строки, которой я хочу пользоваться из любой папки». Пример: инструмент
    форматирования кода <code class="inline">black</code> — вы не импортируете его в свой код, вы
    запускаете его как команду. pipx автоматически создаёт для каждой такой программы своё
    отдельное окружение, но делает саму команду доступной глобально, из любой папки — без
    активации.</p>

{code_block("Терминал", "pipx install black\nblack my_script.py", lang="text")}

    <h2 id="uv">uv</h2>
    <p><strong>uv</strong> (от компании Astral — они же делают Ruff, раздел 2.7) — относительно
    новый инструмент, который сам себя описывает как единую замену сразу для pip, pip-tools,
    pipx, poetry, pyenv, virtualenv и других. Его главное преимущество — скорость: uv в 10–100 раз
    быстрее pip на типичных операциях, потому что написан на Rust и агрессивно кеширует пакеты.</p>

{code_block("Терминал", "uv venv\nuv pip install requests\nuv run my_script.py", lang="text")}

{callout(
        "info",
        "[[icon:note]] Официальный источник",
        "docs.astral.sh/uv — актуальная документация; на момент написания курса стабильная "
        "версия — 0.12.5.",
    )}

    <h2 id="sravnenie">Сравнение</h2>
{tool_table}

{decision}

{callout(
        "tip",
        "[[icon:launch]] Что использовать в этом курсе",
        "Мы будем показывать примеры через <code class=\"inline\">pip</code> и "
        "<code class=\"inline\">venv</code> — это стандарт, который работает везде «из коробки» "
        "и на котором проще всего понять, что происходит на самом деле. Если позже вам "
        "понравится скорость uv — переключиться легко: команды почти зеркальные.",
    )}"""

    out = render_page(
        page_title="pip, pipx, venv, virtualenv, uv",
        description="Разбираем по отдельности pip, venv, virtualenv, pipx и uv — что каждый из "
        "них реально делает, чем отличаются и когда какой использовать.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("pip / pipx / venv / uv", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="pip, pipx, venv, virtualenv, uv",
        lede="Пять похожих по звучанию инструментов — и очень разные задачи, которые каждый "
        "из них решает.",
        body_html=body,
        sidebar_groups=sidebar("02-13-pip-pipx-venv-virtualenv-uv.html"),
        nav=PageNav(prev_href="02-12-pervyj-paket.html", prev_label="Первый пакет", next_href="02-14-conda-i-anaconda.html", next_label="conda, Miniconda, Miniforge, Anaconda"),
    )
    write("02-13-pip-pipx-venv-virtualenv-uv.html", out)


def build_14_conda() -> None:
    conda_family = branch_diagram(
        "Дистрибутивы на основе conda",
        [
            ("Anaconda", "Полный набор: conda + сотни пакетов для данных сразу"),
            ("Miniconda", "Минимальный: только conda, пакеты — по запросу"),
            ("Miniforge", "Как Miniconda, но с открытым сообществом conda-forge по умолчанию"),
        ],
        caption="Все три ставят один и тот же инструмент conda — отличается только то, что идёт «в комплекте»",
    )

    body = f"""
    <p><strong>conda</strong> — ещё один менеджер пакетов и окружений, изначально созданный для
    data science и научных вычислений компанией Anaconda, Inc. Его ключевое отличие от pip:
    conda умеет устанавливать не только Python-пакеты, но и <strong>непитоновские</strong>
    зависимости — например, компиляторы, библиотеки CUDA для видеокарт, системные библиотеки для
    научных вычислений — то, с чем pip в одиночку не справляется.</p>

    <h2 id="semejstvo">Anaconda, Miniconda, Miniforge — в чём разница</h2>
    <p>Все три — это <em>способы получить conda на компьютер</em>, а не три разных инструмента:</p>

{conda_family}

    <ul>
      <li><strong>Anaconda</strong> — самый «тяжёлый» вариант: сразу ставит conda и несколько
        сотен популярных пакетов для анализа данных (несколько гигабайт на диске);</li>
      <li><strong>Miniconda</strong> — официальный минимальный установщик: только сам conda,
        остальное вы ставите по мере необходимости;</li>
      <li><strong>Miniforge</strong> — похож на Miniconda, но по умолчанию использует
        сообщество-репозиторий conda-forge вместо канала по умолчанию от Anaconda, Inc.</li>
    </ul>

    <h2 id="conda-okruzheniya">Окружения в conda</h2>
{code_block("Терминал", "conda create -n my-project python=3.14\nconda activate my-project\nconda install numpy pandas", lang="text")}

    <p>Идея точно та же, что и у venv (раздел 2.10) — изолированное окружение на проект. Отличие
    в деталях: conda хранит окружения не в папке проекта, а в общем месте на диске, и вы
    обращаетесь к ним по имени (<code class="inline">-n my-project</code>), а не по пути.</p>

    <h2 id="conda-i-pip">Как conda и pip уживаются вместе</h2>
    <p>Внутри активированного conda-окружения команда <code class="inline">pip</code> тоже
    работает — и часто используется для пакетов, которых нет в репозиториях conda. Правило
    хорошего тона: сначала ставьте через <code class="inline">conda install</code> всё, что
    доступно этим способом, и только оставшееся — через <code class="inline">pip install</code>,
    чтобы не запутать собственную систему разрешения зависимостей conda.</p>

{callout(
        "warning",
        "[[icon:warning]] Не смешивайте venv и conda для одного окружения",
        "conda и venv — два независимых способа создавать изолированные окружения. Не пытайтесь "
        "активировать venv <em>внутри</em> conda-окружения (или наоборот) для одного и того же "
        "проекта — выберите один инструмент на проект.",
    )}

    <h2 id="kogda-conda">Когда выбирать conda</h2>
{callout(
        "tip",
        "[[icon:launch]] Практический совет",
        "Если вы занимаетесь анализом данных, машинным обучением или научными вычислениями и "
        "используете библиотеки со сложными непитоновскими зависимостями (например, некоторые "
        "версии PyTorch с поддержкой GPU) — conda часто удобнее. Для этого курса и для "
        "большинства обычных проектов на Python вполне достаточно связки venv + pip из разделов "
        "2.10–2.13.",
    )}"""

    out = render_page(
        page_title="conda, Miniconda, Miniforge, Anaconda",
        description="Разбираем conda как менеджер окружений и пакетов для data science, разницу "
        "между Anaconda/Miniconda/Miniforge и взаимодействие conda с pip.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("conda / Anaconda", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="conda, Miniconda, Miniforge, Anaconda",
        lede="Ещё одна семья инструментов, родом из data science — со своей моделью окружений "
        "и своим взглядом на пакеты.",
        body_html=body,
        sidebar_groups=sidebar("02-14-conda-i-anaconda.html"),
        nav=PageNav(prev_href="02-13-pip-pipx-venv-virtualenv-uv.html", prev_label="pip / pipx / venv / uv", next_href="02-15-ide-i-okruzheniya.html", next_label="Как IDE, Python и окружение связаны"),
    )
    write("02-14-conda-i-anaconda.html", out)


def build_15_ide_and_envs() -> None:
    process_flow = flow_diagram(
        [
            ("Вы пишете\nимпорт", "import requests"),
            ("Интерпретатор\nищет пакет", "в site-packages активного окружения"),
            ("Найден", "→ код выполняется"),
        ],
        caption="Простая модель: интерпретатор ищет пакет только в своём собственном окружении",
    )

    body = f"""
    <p>Мы установили Python (2.3–2.5), редактор кода (2.7–2.9) и научились создавать окружения
    (2.10–2.12). Теперь соберём всё это в одну целостную картину — как эти части на самом деле
    связаны друг с другом.</p>

    <h2 id="ide-ne-vladeet">Главная идея: IDE не владеет окружением</h2>
    <p>Это стоит проговорить прямо: <strong>VS Code и PyCharm не «содержат» в себе Python и
    пакеты</strong> — они лишь находят на диске уже существующий интерпретатор (и его окружение)
    и запускают его от своего имени. Одно и то же окружение <code class="inline">.venv</code>
    можно с одинаковым успехом использовать хоть из VS Code, хоть из PyCharm, хоть из обычного
    терминала — и результат будет одинаковым, потому что реально работает не редактор, а
    интерпретатор.</p>

{converge_diagram(
        ["VS Code", "PyCharm", "Обычный терминал"],
        ".venv проекта",
        caption="Три разных «фронтенда» — одно и то же окружение позади них",
    )}

    <h2 id="prostaya-model">Простая модель процесса</h2>
    <p>Когда вы запускаете файл — не важно, из какого редактора или терминала — происходит одно и
    то же:</p>
{process_flow}

    <h2 id="jupyter-kernel">Блокноты: notebook и kernel — тоже не одно и то же</h2>
    <p>С блокнотами (<code class="inline">.ipynb</code>) добавляется ещё один слой, который часто
    путает: <strong>notebook</strong> — это сам файл с ячейками кода и текста, а
    <strong>kernel</strong> (ядро) — это работающий в фоне процесс Python, который реально
    выполняет код из ячеек. Один и тот же файл блокнота можно открыть и подключить к разным
    ядрам — например, к ядру из окружения проекта А или проекта Б.</p>

    <p>Расширение Jupyter в VS Code (раздел 2.7) прямо предупреждает: оно <strong>не является
    ядром</strong> само по себе — это лишь интерфейс, который показывает ячейки и отправляет их
    код выбранному ядру. Чтобы ядро вообще появилось в списке выбора, в соответствующем окружении
    должен быть установлен пакет <code class="inline">jupyter</code>:</p>

{code_block("Терминал (окружение активировано)", "pip install jupyter", lang="text")}

    <p>После этого при открытии <code class="inline">.ipynb</code>-файла в VS Code в правом
    верхнем углу можно выбрать ядро — в списке появится что-то вроде
    <code class="inline">Python 3.14.7 ('.venv': venv)</code>, явно показывая, из какого именно
    окружения оно взято.</p>

{callout(
        "debug",
        "[[icon:debug]] «В блокноте другие пакеты, чем в терминале»",
        "Если <code class=\"inline\">import</code> работает в обычном .py-файле, но не в "
        "блокноте (или наоборот) — почти всегда для блокнота выбрано другое ядро, то есть другое "
        "окружение. Проверьте выбор ядра в правом верхнем углу блокнота так же, как проверяли "
        "«Select Interpreter» в разделе 2.8.",
    )}

    <h2 id="itog-svyazi">Итоговая картина главы</h2>
{summary_box(
        "Кто есть кто",
        [
            "<strong>Интерпретатор Python</strong> — программа, которая реально выполняет код.",
            "<strong>Виртуальное окружение</strong> — изолированный набор пакетов, привязанный к интерпретатору.",
            "<strong>VS Code / PyCharm</strong> — редакторы, которые находят и используют интерпретатор + окружение, но не содержат их внутри себя.",
            "<strong>pip / uv</strong> — устанавливают пакеты в текущее активное окружение.",
            "<strong>Notebook</strong> — файл с ячейками; <strong>kernel</strong> — процесс Python, который их выполняет.",
        ],
    )}"""

    out = render_page(
        page_title="Как IDE, Python и окружение связаны",
        description="Сводная картина: почему IDE не владеет окружением, простая модель процесса "
        "выполнения кода и разница между notebook и kernel в Jupyter.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("IDE и окружения", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="Как IDE, Python и окружение связаны",
        lede="Собираем все части главы в одну целостную картину — включая частый источник "
        "путаницы: разницу между блокнотом и ядром Jupyter.",
        body_html=body,
        sidebar_groups=sidebar("02-15-ide-i-okruzheniya.html"),
        nav=PageNav(prev_href="02-14-conda-i-anaconda.html", prev_label="conda / Anaconda", next_href="02-16-diagnostika.html", next_label="Типичные проблемы и диагностика"),
    )
    write("02-15-ide-i-okruzheniya.html", out)


def build_16_diagnostics() -> None:
    labs = [
        (
            "«command not found: python»",
            "Команда <code class=\"inline\">python</code> не найдена в терминале.",
            "Python не установлен, либо не добавлен в PATH (Windows: галочка «Add python.exe to "
            "PATH», раздел 2.3), либо на macOS/Linux нужно использовать "
            "<code class=\"inline\">python3</code> вместо <code class=\"inline\">python</code> "
            "(раздел 2.4).",
        ),
        (
            "«externally-managed-environment»",
            "<code class=\"inline\">pip install</code> отказывается работать на Linux/macOS.",
            "Это защита PEP 668 (раздел 2.5): создайте и активируйте виртуальное окружение "
            "(раздел 2.11) и ставьте пакеты туда — не в системный Python.",
        ),
        (
            "ModuleNotFoundError после установки",
            "Пакет установлен, но import падает.",
            "Пакет установлен не в то окружение, из которого запускается код. Сверьте "
            "<code class=\"inline\">sys.executable</code> (раздел 2.6) с активным окружением "
            "терминала и с интерпретатором, выбранным в VS Code (раздел 2.8) — см. лабораторию "
            "раздела 2.12.",
        ),
        (
            "VS Code запускает «не тот» Python",
            "Поведение при запуске из VS Code отличается от запуска из терминала.",
            "Проверьте «Select Interpreter» (раздел 2.8) — выбран не тот путь. Сверьтесь с "
            "<code class=\"inline\">.vscode/settings.json</code> проекта.",
        ),
        (
            "Забыли активировать окружение",
            "Приглашение терминала не показывает <code class=\"inline\">(.venv)</code>, пакеты "
            "«пропали».",
            "Окружение не активировано в этом окне терминала — активация не сохраняется между "
            "вкладками (раздел 2.11). Выполните команду активации для вашей ОС заново.",
        ),
        (
            "Два Python — конфликт версий",
            "<code class=\"inline\">python --version</code> показывает не ту версию, что вы "
            "только что установили.",
            "На компьютере несколько интерпретаторов, и PATH находит не тот, что ожидалось "
            "(раздел 2.2). Проверьте порядок через <code class=\"inline\">which</code> / "
            "<code class=\"inline\">where.exe</code> (раздел 2.6).",
        ),
        (
            "Блокнот использует не то ядро",
            "В <code class=\"inline\">.ipynb</code> импорт не находит пакет, который точно "
            "установлен.",
            "У блокнота выбрано другое ядро (kernel) — не то окружение, куда вы ставили пакет "
            "(раздел 2.15). Смените ядро в правом верхнем углу блокнота.",
        ),
        (
            "«pip: command not found» при активном venv",
            "Внутри активированного окружения команда pip всё равно не находится.",
            "Редкий случай повреждённого окружения — пересоздайте его: удалите папку "
            "<code class=\"inline\">.venv</code> и выполните "
            "<code class=\"inline\">python -m venv .venv</code> заново (раздел 2.11).",
        ),
    ]

    lab_html = "".join(
        f"""
        <div class="callout callout-debug">
          <div>
            <div class="callout-title">[[icon:debug]] Лаборатория {i}. {title}</div>
            <div class="callout-body"><p><strong>Симптом:</strong> {symptom}</p><p><strong>Причина и решение:</strong> {fix}</p></div>
          </div>
        </div>"""
        for i, (title, symptom, fix) in enumerate(labs, start=1)
    )

    body = f"""
    <p>Собрали восемь самых частых проблем этой главы в одном месте — как справочник, к которому
    можно будет вернуться, когда что-то пойдёт не так. Каждая уже разбиралась по ходу главы;
    здесь — компактная версия для быстрой диагностики.</p>

{lab_html}

{callout(
        "tip",
        "[[icon:launch]] Общий метод диагностики",
        "Почти все проблемы этой главы сводятся к одному вопросу: <strong>какой именно "
        "интерпретатор и какое окружение сейчас реально используются?</strong> Проверяйте это в "
        "первую очередь — через <code class=\"inline\">sys.executable</code> (раздел 2.6), "
        "приглашение терминала <code class=\"inline\">(.venv)</code> и выбор интерпретатора в "
        "редакторе (раздел 2.8) — прежде чем подозревать что-то более сложное.",
    )}"""

    out = render_page(
        page_title="Типичные проблемы и диагностика",
        description="Восемь именованных лабораторий диагностики: command not found, "
        "externally-managed-environment, ModuleNotFoundError и другие частые проблемы установки.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("Диагностика", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="Типичные проблемы и диагностика",
        lede="Восемь именованных лабораторий — справочник частых проблем этой главы и способов "
        "их решить.",
        body_html=body,
        sidebar_groups=sidebar("02-16-diagnostika.html"),
        nav=PageNav(prev_href="02-15-ide-i-okruzheniya.html", prev_label="IDE и окружения", next_href="02-17-rekomendacii-i-itogi.html", next_label="Рекомендации Cartesian School и итоги"),
    )
    write("02-16-diagnostika.html", out)


def build_17_recommendations_and_lab() -> None:
    paths_table = comparison_table(
        ["Путь", "Редактор", "Управление пакетами", "Кому подходит"],
        [
            [
                "<strong>Стандартный</strong>",
                "VS Code",
                "venv + pip",
                "Рекомендуем для этого курса — минимум движущихся частей, максимум понимания",
            ],
            [
                "<strong>Быстрый</strong>",
                "VS Code или любой другой",
                "uv",
                "Если хочется скорости и единого инструмента с первого дня",
            ],
            [
                "<strong>Data science</strong>",
                "PyCharm, VS Code или Jupyter",
                "conda / Miniforge",
                "Если вы уже нацелены на анализ данных, ML или научные вычисления",
            ],
        ],
    )

    checklist_items = [
        "Python установлен, и <code class=\"inline\">python --version</code> (или "
        "<code class=\"inline\">python3 --version</code>) печатает версию 3.x",
        "Команда работает из <strong>обычного</strong> терминала операционной системы (не только "
        "из редактора)",
        "<code class=\"inline\">sys.executable</code> печатает ожидаемый путь к интерпретатору",
        "VS Code (или PyCharm) установлен и открывается без ошибок",
        "Расширение Python установлено в VS Code (или подтверждена встроенная поддержка PyCharm)",
        "В боковой панели VS Code видно, что вместе с Python подтянулись Pylance, Python Debugger "
        "и Python Environments",
        "Создана тестовая папка проекта",
        "В этой папке выполнено <code class=\"inline\">python -m venv .venv</code>",
        "Окружение <code class=\"inline\">.venv</code> успешно активировано (в приглашении "
        "терминала видно <code class=\"inline\">(.venv)</code>)",
        "В активном окружении выполнено <code class=\"inline\">pip install requests</code> без ошибок",
        "<code class=\"inline\">import requests</code> работает в интерактивном "
        "<code class=\"inline\">python</code>",
        "В VS Code для тестовой папки выбран интерпретатор именно из "
        "<code class=\"inline\">.venv</code> («Select Interpreter», раздел 2.8)",
        "Создан файл <code class=\"inline\">main.py</code> с "
        "<code class=\"inline\">import requests</code>, и запуск через кнопку ▷ в VS Code "
        "проходит без ошибок",
        "Тот же файл успешно запускается и из встроенного терминала VS Code",
        "Поставлена хотя бы одна точка останова, и отладчик VS Code успешно останавливается на ней",
        "Окружение деактивировано командой <code class=\"inline\">deactivate</code>, и после "
        "этого <code class=\"inline\">import requests</code> в обычном терминале уже не работает "
        "(если requests не был установлен глобально) — это подтверждает изоляцию",
        "Окружение активировано заново",
        "Вы можете своими словами объяснить разницу между интерпретатором, редактором, pip и "
        "виртуальным окружением — вслух, партнёру по учёбе или самому себе",
    ]

    checklist_html = "".join(
        f'<li style="margin-bottom:10px"><label style="display:flex;gap:10px;align-items:flex-start;cursor:pointer">'
        f'<input type="checkbox" style="margin-top:4px;flex-shrink:0" /><span>{item}</span></label></li>'
        for item in checklist_items
    )

    body = f"""
    <h2 id="rekomendacii">Три рекомендованных пути Cartesian School</h2>
    <p>Все инструменты этой главы — легитимные, рабочие варианты. Вот три сочетания, которые мы
    рекомендуем в зависимости от ваших целей:</p>

{paths_table}

{callout(
        "tip",
        "[[icon:launch]] Если сомневаетесь",
        "Начните со <strong>стандартного пути</strong> — VS Code + venv + pip. Это ровно то, что "
        "мы использовали во всех примерах этой главы, и на нём проще всего понять, что реально "
        "происходит «под капотом». К uv или conda всегда можно перейти позже — идеи от этого не "
        "изменятся.",
    )}

    <h2 id="local-required-lab">Практика: соберите рабочее место (local-required)</h2>
    <p>Эта практика — <strong>обязательная для выполнения на вашем собственном компьютере</strong>.
    В отличие от интерактивных упражнений в браузере из других глав, установку Python нельзя
    (да и не нужно) эмулировать онлайн — смысл именно в том, чтобы у вас на диске появилось
    настоящее, работающее рабочее место.</p>

{callout(
        "warning",
        "[[icon:code]] local-required",
        "Пройдите каждый пункт по порядку на своём компьютере и отметьте выполненное. Ничего "
        "отправлять на проверку не нужно — это чек-лист для вас самих.",
    )}

    <div class="exercise">
      <div class="exercise-stars">★★★ Обязательная практика главы</div>
      <div class="exercise-title">Чек-лист рабочего места (18 шагов)</div>
      <ul style="list-style:none;padding-left:0;margin-top:16px">
{checklist_html}
      </ul>
    </div>

    <h2 id="itogi">Итоги главы</h2>
{summary_box(
        "Что мы теперь умеем",
        [
            "Понимаем семь слоёв между железом и своим кодом — и что интерпретатор, редактор, pip и окружение — четыре разные вещи.",
            "Понимаем, что такое терминал, shell и переменная PATH, и как компьютер находит команду по имени.",
            "Установили Python на своей операционной системе — Windows, macOS или Linux — и знаем её особенности (PATH-галочка, системный Python, PEP 668).",
            "Умеем проверять, какой именно интерпретатор реально запущен, через sys.executable.",
            "Настроили редактор кода — VS Code или PyCharm — и умеем выбирать интерпретатор для проекта.",
            "Понимаем, зачем нужны виртуальные окружения, умеем их создавать, активировать и устанавливать в них пакеты.",
            "Различаем pip, pipx, venv, virtualenv и uv — и знаем, для какой задачи каждый из них.",
            "Знаем, как работает conda и семейство Anaconda/Miniconda/Miniforge, и когда его стоит выбрать.",
            "Умеем диагностировать восемь самых частых проблем установки и настройки.",
            "Собрали полноценное, работающее рабочее место Python-разработчика на своём компьютере.",
        ],
    )}

{callout(
        "tip",
        "[[icon:launch]] Что дальше",
        "С готовым рабочим местом вы полностью подготовлены к главе 3 — там мы начнём писать "
        "настоящий, содержательный код.",
    )}"""

    out = render_page(
        page_title="Рекомендации Cartesian School и итоги",
        description="Три рекомендованных пути настройки рабочего места, обязательный чек-лист "
        "из 18 шагов и итоги главы 2.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("Итоги", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="Рекомендации Cartesian School и итоги",
        lede="Три пути настройки рабочего места — и финальная практика: полный чек-лист сборки "
        "рабочего места на вашем собственном компьютере.",
        body_html=body,
        sidebar_groups=sidebar("02-17-rekomendacii-i-itogi.html"),
        nav=PageNav(prev_href="02-16-diagnostika.html", prev_label="Диагностика", next_href=None, next_label=None),
    )
    write("02-17-rekomendacii-i-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01_layers()
    build_04_terminal_path()
    build_02_windows()
    build_03_mac()
    build_05_linux()
    build_06_which_python()
    build_07_vscode_install()
    build_08_vscode_config()
    build_09_pycharm()
    build_10_why_venv()
    build_11_create_venv()
    build_12_first_package()
    build_13_pip_pipx_venv_uv()
    build_14_conda()
    build_15_ide_and_envs()
    build_16_diagnostics()
    build_17_recommendations_and_lab()
    print(f"Готово: {len(PAGES)} страниц Главы 2")
