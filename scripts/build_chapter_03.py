#!/usr/bin/env python3
"""Строит Главу 3: «Ваша первая программа на Python» (site/chapters/glava-03/).

Curriculum v2: от короткой главы об установке до полноценного курса о том,
как разговаривать с Python — файлы и их запуск, терминал/shell/Python REPL,
семейство командных оболочек и PySH, REPL как инструмент исследования,
print()/input(), имена и значения, комментарии и стиль, IDLE, ошибки и
traceback, отладка и отладчик IDE, Jupyter notebook/kernel, и первый
мини-проект. Существующие маршруты (index.html, 03-01..03-05) сохранены и
расширены на месте; новый материал добавлен как новые страницы 03-06..03-17.
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
    classic_vs_modern,
    code_block,
    comparison_table,
    converge_diagram,
    exercise,
    flow_diagram,
    image_figure,
    name_value_diagram,
    namespace_diagram,
    practice_card,
    render_chapter_opener,
    render_page,
    summary_box,
    timeline_diagram,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-03"
IMG = "../../assets/img"

PAGES = [
    ("index.html", "Приступаем"),
    ("03-01-sozdanie-i-zapusk-programm.html", "Создание и запуск программ"),
    ("03-06-terminal-shell-i-python-repl.html", "Терминал, shell и Python REPL"),
    ("03-07-semejstvo-obolochek.html", "Семейство командных оболочек"),
    ("03-08-pysh.html", "PySH: Python-first оболочка"),
    ("03-02-interaktivny-rezhim.html", "Интерактивный режим (Python REPL)"),
    ("03-09-repl-kak-instrument.html", "REPL как инструмент исследования"),
    ("03-03-vyvod-dannyh.html", "Вывод данных с помощью Python"),
    ("03-10-input-i-dialog.html", "input(): первый диалог"),
    ("03-11-imena-i-znacheniya.html", "Имена и значения"),
    ("03-12-kommentarii-i-stil.html", "Комментарии и читаемый код"),
    ("03-04-idle.html", "Режим сценариев IDLE"),
    ("03-05-praktika-itogi.html", "Практика: выведите своё имя"),
    ("03-13-oshibki-i-traceback.html", "Ошибки, traceback и как их читать"),
    ("03-14-debug-laboratorii.html", "Лаборатории отладки"),
    ("03-15-otladchik-v-ide.html", "Первый отладчик в IDE"),
    ("03-16-notebook-i-kernel.html", "Notebook и kernel"),
    ("03-17-mini-proekt-i-itogi.html", "Мини-проект и итоги главы"),
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 3 · Первая программа", items),
        SidebarGroup("Практика", [
            NavItem("[[icon:practice]] 03-01: Практика", "../../practice/03-01/index.html"),
            NavItem("[[icon:practice]] 03-02: Практика", "../../practice/03-02/index.html"),
            NavItem("[[icon:practice]] 03-03: Практика", "../../practice/03-03/index.html"),
            NavItem("[[icon:practice]] 03-04: Практика", "../../practice/03-04/index.html"),
            NavItem("[[icon:practice]] 03-05: Практика", "../../practice/03-05/index.html"),
            NavItem("[[icon:practice]] 03-06: Практика", "../../practice/03-06/index.html"),
            NavItem("[[icon:practice]] 03-07: Практика", "../../practice/03-07/index.html"),
            NavItem("[[icon:practice]] 03-08: Практика", "../../practice/03-08/index.html"),
            NavItem("[[icon:practice]] 03-09: Практика", "../../practice/03-09/index.html"),
            NavItem("[[icon:practice]] 03-10: Практика", "../../practice/03-10/index.html"),
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
        description="Как по-настоящему разговаривать с Python: файлы и их запуск, терминал и "
        "командные оболочки, PySH, интерактивный REPL, print()/input(), имена, ошибки и "
        "traceback, отладчик, Jupyter — и первый маленький проект.",
        meta_items=["[[icon:timer]] ~2.5 часа", "[[icon:code]] VS Code, PyCharm или браузер", "[[icon:practice]] 10 ноутбуков практики"],
        brand_html='<div style="display:flex;align-items:center;gap:16px;margin-bottom:18px;flex-wrap:wrap">'
        f'<img src="{IMG}/brand/python-logo-mark.svg" alt="Python" width="30" height="30" style="display:block" />'
        f'<img src="{IMG}/brand/vscode-logo.png" alt="VS Code" width="28" height="28" style="display:block" />'
        f'<img src="{IMG}/brand/pycharm-logo.png" alt="PyCharm" width="28" height="28" style="display:block" />'
        f'<img src="{IMG}/brand/jupyter-logo.png" alt="Jupyter" width="28" height="28" style="display:block" />'
        f'<img src="{IMG}/brand/pysh-logo.png" alt="PySH" width="28" height="28" style="display:block" />'
        '<span style="font-family:\'JetBrains Mono\',monospace;font-size:12px;color:var(--blue-300);'
        'letter-spacing:.03em">Технологии главы: официальные логотипы использованы для идентификации, '
        'без заявления о партнёрстве</span></div>',
        sections=[
            ChapterSectionLink("3.1", "Создание и запуск программ на Python", "03-01-sozdanie-i-zapusk-programm.html", "27"),
            ChapterSectionLink("3.2", "Терминал, shell и Python REPL", "03-06-terminal-shell-i-python-repl.html", ""),
            ChapterSectionLink("3.3", "Семейство командных оболочек", "03-07-semejstvo-obolochek.html", ""),
            ChapterSectionLink("3.4", "PySH: Python-first оболочка", "03-08-pysh.html", ""),
            ChapterSectionLink("3.5", "Интерактивный режим Python (REPL)", "03-02-interaktivny-rezhim.html", "30"),
            ChapterSectionLink("", "Ваша оболочка умеет считать", "03-02-interaktivny-rezhim.html#schitaet", "30"),
            ChapterSectionLink("3.6", "REPL как инструмент исследования", "03-09-repl-kak-instrument.html", ""),
            ChapterSectionLink("3.7", "Вывод данных с помощью Python", "03-03-vyvod-dannyh.html", "32"),
            ChapterSectionLink("3.8", "input(): первый диалог", "03-10-input-i-dialog.html", ""),
            ChapterSectionLink("3.9", "Имена и значения", "03-11-imena-i-znacheniya.html", ""),
            ChapterSectionLink("3.10", "Комментарии и читаемый код", "03-12-kommentarii-i-stil.html", ""),
            ChapterSectionLink("3.11", "Режим сценариев IDLE", "03-04-idle.html", "33"),
            ChapterSectionLink("3.12", "Практика: выведите своё имя", "03-05-praktika-itogi.html", "36"),
            ChapterSectionLink("3.13", "Ошибки, traceback и как их читать", "03-13-oshibki-i-traceback.html", ""),
            ChapterSectionLink("3.14", "Лаборатории отладки", "03-14-debug-laboratorii.html", ""),
            ChapterSectionLink("3.15", "Первый отладчик в IDE", "03-15-otladchik-v-ide.html", ""),
            ChapterSectionLink("3.16", "Notebook и kernel", "03-16-notebook-i-kernel.html", ""),
            ChapterSectionLink("3.17", "Мини-проект и итоги главы", "03-17-mini-proekt-i-itogi.html", "37"),
        ],
    )
    write("index.html", out)


def build_01_create_and_run() -> None:
    layer1 = flow_diagram(
        [
            ("privet.py", "текстовый файл на диске"),
            ("Python", "интерпретатор читает файл"),
            ("Программа работает", "результат на экране"),
        ],
        caption="Уровень 1: от файла к результату",
    )

    layer2 = flow_diagram(
        [
            ("Исходный код", ".py файл, обычный текст"),
            ("Байт-код", "компактные инструкции CPython"),
            ("Python VM", "выполняет байт-код"),
        ],
        caption="Уровень 2: что CPython делает внутри — компилирует, а затем выполняет",
    )

    body = f"""
    <p>Программа на Python — это <strong>обычный текстовый файл</strong>. Ничего волшебного:
    те же байты, что и в любом <code class="inline">.txt</code>-файле, только Python умеет их
    читать и превращать в действия.</p>

    <h2 id="chto-takoe-fajl">Что такое файл программы .py</h2>
    <p>У файла программы есть несколько частей, которые стоит различать:</p>
    <ul>
      <li><strong>Исходный код</strong> (source code) — сам текст программы, который пишет
        человек;</li>
      <li><strong>Имя файла</strong> — например, <code class="inline">privet.py</code>;
        расширение <code class="inline">.py</code> — соглашение, по которому редакторы и сам
        Python узнают файл с кодом на Python;</li>
      <li><strong>Папка проекта</strong> — место на диске, где лежит файл (и, возможно, другие
        файлы того же проекта);</li>
      <li><strong>Кодировка</strong> — то, как текст хранится в виде байтов. Python по умолчанию
        читает исходный код в <strong>UTF-8</strong> — универсальной кодировке, которая
        поддерживает практически любой алфавит, включая кириллицу. Именно поэтому в исходном
        коде Python можно свободно писать русские строки и комментарии — никаких специальных
        настроек не нужно.</li>
    </ul>

{callout(
        "info",
        "[[icon:idea]] Файл — это не программа, которая «уже работает»",
        "Пока файл просто лежит на диске, ничего не происходит — это только текст. Программа "
        "начинает работать только в момент, когда её ЗАПУСКАЮТ — передают интерпретатору Python "
        "на выполнение. Разница между «файл существует» и «файл выполняется» — то же самое "
        "различие, что между рецептом на бумаге и настоящим приготовлением блюда.",
    )}

    <h2 id="tekushaya-papka">Текущая папка и путь к файлу</h2>
    <p>Чтобы запустить файл, shell (раздел 3.2) должен знать, где он лежит. Если вы находитесь
    <em>в той же папке</em>, что и файл, достаточно его имени. Если нет — нужен путь: полный
    (от корня диска) или относительный (от текущей папки). Мы разбирали путь и текущую папку
    подробнее в главе 2.</p>

    <h2 id="model-vypolneniya">Простая модель: как Python запускает программу</h2>
{layer1}
    <p>Внутри «Python работает» скрывается ещё один уровень, который полезно знать хотя бы в
    общих чертах:</p>
{layer2}

{callout(
        "tip",
        "[[icon:experiment]] Что происходит на самом деле",
        "CPython (реализация Python, которой мы пользуемся) сначала переводит ваш исходный код в "
        "промежуточный, более компактный формат — <strong>байт-код</strong> — а затем выполняет "
        "именно его на собственной виртуальной машине. Это не значит, что Python «никогда не "
        "компилируется» — как раз наоборот: компиляция в байт-код происходит практически всегда, "
        "просто незаметно для вас, за долю секунды перед выполнением.",
    )}

{callout(
        "info",
        "[[icon:note]] А как же __pycache__?",
        "Когда вы позже начнёте <em>импортировать</em> свои файлы как модули в другие файлы "
        "(главы про функции и модули), вы заметите папку <code class=\"inline\">__pycache__</code> "
        "— туда Python сохраняет уже скомпилированный байт-код, чтобы не пересчитывать его "
        "заново при каждом запуске. Для файла, который вы просто запускаете напрямую (как "
        "<code class=\"inline\">privet.py</code> ниже), эта папка обычно не создаётся — не "
        "удивляйтесь, если сейчас её не будет видно.",
    )}

    <h2 id="vasha-pervaya-programma">Ваша первая программа</h2>
{code_block("privet.py", 'print("Привет, Python!")\n')}
    <p>Разберём команду запуска по частям:</p>
{code_block("Терминал", "python privet.py", lang="text")}
    <ul>
      <li><code class="inline">python</code> — исполняемый файл интерпретатора (мы устанавливали
        его в главе 2);</li>
      <li><code class="inline">privet.py</code> — аргумент: какой именно файл выполнить.</li>
    </ul>
    <p>После запуска вы должны увидеть:</p>
{code_block("вывод программы", 'Привет, Python!', lang="text")}

    <h2 id="vscode">Создание и запуск в VS Code</h2>
    <ol>
      <li>Откройте папку проекта через <strong>File → Open Folder</strong> (мы настраивали VS
        Code в главе 2 — интерпретатор уже должен быть выбран для этой папки).</li>
      <li>Создайте новый файл <code class="inline">privet.py</code>.</li>
      <li>Наберите код и нажмите на треугольник ▷ «Run Python File» в правом верхнем углу — либо
        откройте встроенный терминал (<code class="inline">Ctrl+`</code>) и наберите
        <code class="inline">python privet.py</code>.</li>
    </ol>

    <h2 id="pycharm">Создание и запуск в PyCharm</h2>
    <ol>
      <li>Откройте или создайте проект с выбранным интерпретатором Python (глава 2).</li>
      <li>Щёлкните правой кнопкой по папке проекта в панели слева → <strong>New → Python
        File</strong>, назовите его <code class="inline">privet</code>.</li>
      <li>Наберите код и запустите через <strong>Run → Run 'privet'</strong> в верхнем меню, либо
        кликните правой кнопкой в редакторе и выберите <strong>Run</strong>.</li>
    </ol>

{callout(
        "warning",
        "[[icon:warning]] Про зелёный треугольник рядом с if __name__",
        "В некоторых чужих самоучителях просят искать зелёный треугольник ▷ именно рядом со "
        "строкой <code class=\"inline\">if __name__ == \"__main__\":</code> — но для такой "
        "простой программы, как <code class=\"inline\">privet.py</code>, эта конструкция вообще "
        "не нужна. Пока запускайте файл через <strong>Run</strong> в верхнем меню или клик правой "
        "кнопкой — этого достаточно. Что означает <code class=\"inline\">if __name__ == "
        "\"__main__\":</code>, мы разберём позже, когда до неё дойдёт очередь по-настоящему.",
    )}

{practice_card(
        "03-01",
        "Практика: создайте и запустите свою первую программу",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/03-01/index.html",
    )}"""

    out = render_page(
        page_title="Создание и запуск программ на Python",
        description="Что такое файл программы .py, простая модель выполнения (source → байт-код "
        "→ VM), и как создать и запустить первую программу в VS Code и PyCharm.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("Создание и запуск программ", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="Создание и запуск программ на Python",
        lede="Программа на Python начинается с обычного текстового файла. Разберём, что это "
        "значит на самом деле — и как создать такой файл и запустить его.",
        body_html=body,
        sidebar_groups=sidebar("03-01-sozdanie-i-zapusk-programm.html"),
        nav=PageNav(prev_href="index.html", prev_label="Приступаем", next_href="03-06-terminal-shell-i-python-repl.html", next_label="Терминал, shell и Python REPL"),
    )
    write("03-01-sozdanie-i-zapusk-programm.html", out)


def build_06_terminal_shell_repl() -> None:
    shell_branch = converge_diagram(
        ["Bash", "Zsh", "PowerShell", "cmd.exe", "Fish", "PySH"],
        "Терминал",
        caption="Разные shell — один и тот же терминал-«экран» вокруг них",
    )

    repl_flow = flow_diagram(
        [
            ("Терминал", "окно с текстом"),
            ("python", "запускаем интерпретатор"),
            ("Python REPL", "приглашение >>>"),
        ],
        caption="Отдельный путь: терминал → интерпретатор → Python REPL",
    )

    body = f"""
    <p>Мы уже встречали слова «терминал» и «shell» в главе 2 — но, чтобы уверенно двигаться
    дальше, важно окончательно закрепить это различие и добавить к нему третье понятие: сам
    <strong>Python REPL</strong>. Путаница между этими тремя вещами — одна из самых частых причин,
    почему новичкам кажется, что «командная строка» — это что-то одно большое и запутанное.</p>

    <h2 id="tri-veshi">Три разные вещи</h2>
    <ul>
      <li><strong>Терминал</strong> (terminal) — окно приложения, где вообще происходит
        текстовый ввод/вывод. Сам по себе терминал ничего не «понимает» — это просто экран и
        клавиатура.</li>
      <li><strong>Shell</strong> (командная оболочка) — программа ВНУТРИ терминала, которая
        читает ваши команды операционной системы: <code class="inline">cd</code>,
        <code class="inline">ls</code>, запуск программ. Bash, Zsh, PowerShell, cmd.exe, Fish,
        PySH — это всё разные shell.</li>
      <li><strong>Python REPL</strong> (он же Python Shell) — это отдельная программа
        (сам интерпретатор Python в интерактивном режиме), которую вы ЗАПУСКАЕТЕ из shell
        командой <code class="inline">python</code>. У неё своё собственное приглашение
        <code class="inline">&gt;&gt;&gt;</code>, и она понимает уже не команды операционной
        системы, а код на Python.</li>
    </ul>

{shell_branch}

{repl_flow}

{callout(
        "warning",
        "[[icon:warning]] Почему все путают «shell» и «Shell»",
        "Есть досадное историческое совпадение: интерактивный режим Python в англоязычной "
        "документации часто называют «Python Shell» — тем же словом, что и обычную командную "
        "оболочку (Bash Shell, PowerShell). Это два РАЗНЫХ значения одного и того же слова. "
        "Когда сомневаетесь — смотрите на приглашение: <code class=\"inline\">$</code> или "
        "<code class=\"inline\">&gt;</code> обычно означает обычный shell операционной системы, "
        "а <code class=\"inline\">&gt;&gt;&gt;</code> — именно Python REPL.",
    )}

    <h2 id="kak-otlichit">Как отличить на глаз</h2>
{comparison_table(
        ["", "Обычный shell (Bash/PowerShell/…)", "Python REPL"],
        [
            ["Приглашение", "<code class=\"inline\">$</code>, <code class=\"inline\">%</code> или <code class=\"inline\">&gt;</code>", "<code class=\"inline\">&gt;&gt;&gt;</code>"],
            ["Понимает", "Команды ОС: <code class=\"inline\">cd</code>, <code class=\"inline\">ls</code>, запуск программ", "Код на Python: выражения, присваивания, вызовы функций"],
            ["Как попасть", "Открыть терминал — вы уже внутри", "Набрать <code class=\"inline\">python</code> внутри shell"],
            ["Как выйти", "Закрыть терминал или <code class=\"inline\">exit</code>", "<code class=\"inline\">exit()</code> или Ctrl+D / Ctrl+Z"],
        ],
    )}

{callout(
        "tip",
        "[[icon:practice]] Проверьте сами",
        "Откройте терминал и наберите <code class=\"inline\">python</code>. Приглашение "
        "изменится с обычного (например, <code class=\"inline\">$</code>) на "
        "<code class=\"inline\">&gt;&gt;&gt;</code> — это верный признак, что вы только что "
        "перешли из shell операционной системы в Python REPL. Наберите "
        "<code class=\"inline\">exit()</code>, чтобы вернуться обратно.",
    )}"""

    out = render_page(
        page_title="Терминал, shell и Python REPL",
        description="Три разные вещи, которые часто путают: терминал (окно), shell (командная "
        "оболочка ОС) и Python REPL (интерактивный интерпретатор).",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("Терминал, shell и Python REPL", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="Терминал, shell и Python REPL — это разные вещи",
        lede="Одна из самых частых причин путаницы у новичков — эти три понятия. Разберём их "
        "раз и навсегда.",
        body_html=body,
        sidebar_groups=sidebar("03-06-terminal-shell-i-python-repl.html"),
        nav=PageNav(prev_href="03-01-sozdanie-i-zapusk-programm.html", prev_label="Создание и запуск программ", next_href="03-07-semejstvo-obolochek.html", next_label="Семейство командных оболочек"),
    )
    write("03-06-terminal-shell-i-python-repl.html", out)


def build_07_shell_family() -> None:
    body = f"""
    <p>Раз уж мы заговорили про shell — коротко познакомимся с самыми распространёнными. Цель
    этого раздела не в том, чтобы выучить синтаксис каждой из них, а в том, чтобы узнавать их по
    имени и понимать, где вы их встретите.</p>

{comparison_table(
        ["Shell", "Где встречается", "Что это"],
        [
            [
                "<strong>cmd.exe</strong>",
                "Windows (классическая, «Командная строка»)",
                "Старейшая командная оболочка Windows; всё ещё встречается в старых инструкциях и корпоративных системах",
            ],
            [
                "<strong>PowerShell</strong>",
                "Windows (современная по умолчанию)",
                "Более мощная оболочка от Microsoft с объектно-ориентированным подходом к командам; то, что мы использовали в главе 2 для Windows",
            ],
            [
                "<strong>Bash</strong>",
                "Linux (часто по умолчанию), macOS (более старые версии)",
                "Один из самых распространённых shell в мире — почти любой сервер и учебник её знает",
            ],
            [
                "<strong>Zsh</strong>",
                "macOS (по умолчанию с 2019 года), популярна на Linux",
                "Похожа на Bash, но с более удобными возможностями «из коробки» (автодополнение, темы оформления)",
            ],
            [
                "<strong>Fish</strong>",
                "Linux/macOS (по выбору пользователя)",
                "Дружелюбная к новичкам оболочка с подсказками и подсветкой прямо во время набора команды",
            ],
            [
                "<strong>PySH</strong>",
                "Linux/macOS/Windows (устанавливается отдельно)",
                "Python-first оболочка — вместо собственного мини-языка команд использует настоящий Python (раздел 3.4)",
            ],
        ],
    )}

{callout(
        "info",
        "[[icon:idea]] Зачем Python-разработчику вообще это знать",
        "Вы не обязаны учить синтаксис всех shell — но полезно узнавать их по приглашению и "
        "названию, когда встречаете в чужих статьях, логах CI/CD или инструкциях по установке. "
        "Часто инструкция говорит «выполните в Bash» или «в PowerShell» — и теперь вы точно "
        "знаете, что имеется в виду.",
    )}

    <div style="display:flex;align-items:center;gap:14px;margin:24px 0;padding:16px 20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px)">
      <img src="{IMG}/brand/pysh-logo.png" alt="Логотип PySH" width="40" height="40" style="display:block;flex-shrink:0" />
      <div>
        <strong>PySH</strong> — последняя строка таблицы выше, и ей посвящён следующий раздел:
        единственная оболочка здесь, написанная как Python-first альтернатива, а не как ещё один
        вариант классического shell-языка.
      </div>
    </div>

    <p>Мы не будем подробно разбирать синтаксис каждой оболочки — это не входит в задачи курса
    Python. Вместо этого в следующем разделе познакомимся с PySH — оболочкой, которая устроена
    иначе: вместо своего мини-языка команд она использует настоящий Python.</p>"""

    out = render_page(
        page_title="Семейство командных оболочек",
        description="Краткий обзор cmd.exe, PowerShell, Bash, Zsh и Fish — где их можно "
        "встретить и зачем Python-разработчику знать их по имени.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("Семейство командных оболочек", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="Семейство командных оболочек",
        lede="cmd.exe, PowerShell, Bash, Zsh, Fish — коротко о том, где вы их встретите и что "
        "это вообще такое.",
        body_html=body,
        sidebar_groups=sidebar("03-07-semejstvo-obolochek.html"),
        nav=PageNav(prev_href="03-06-terminal-shell-i-python-repl.html", prev_label="Терминал, shell и Python REPL", next_href="03-08-pysh.html", next_label="PySH"),
    )
    write("03-07-semejstvo-obolochek.html", out)


def build_08_pysh() -> None:
    traditional_flow = flow_diagram(
        [
            ("Терминал", "окно"),
            ("Bash / Zsh", "shell-язык команд"),
            ("Скрипт", "pipes, спецсимволы"),
        ],
        caption="Традиционный подход: терминал → shell-язык → shell-скрипт",
    )

    pysh_converge = converge_diagram(
        ["pathlib", "исключения", "logging", "pytest", "PyPI"],
        "PySH",
        caption="Python-first подход PySH: обычные Python-инструменты прямо в командной строке",
    )

    body = f"""
    <div style="display:flex;align-items:center;gap:16px;margin-bottom:20px">
      <img src="{IMG}/brand/pysh-logo.png" alt="Логотип PySH" width="56" height="56" style="display:block;flex-shrink:0" />
      <div style="font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--color-text-muted,#6B6B7D)">
        Официальный логотип проекта PySH (pysh-shell.com) — использован для идентификации
        технологии, обсуждаемой в этом курсе, без заявления о партнёрстве или спонсорстве.
      </div>
    </div>

    <p>PySH — это реальная, установленная на этом компьютере программа, и все примеры на этой
    странице — настоящий, проверенный вывод именно этой установки, а не выдуманный текст.</p>

{image_figure(
        f"{IMG}/screenshots/pysh-shell-com-homepage.jpg",
        "Главная страница официального сайта pysh-shell.com",
        "pysh-shell.com — официальный сайт проекта PySH («The Python-Native Automation "
        "Platform»). Версия на сайте (0.8.2) совпадает с версией, установленной на этом "
        "компьютере.",
    )}

{callout(
        "warning",
        "[[icon:warning]] Только этот проект",
        "В мире существует несколько пакетов с похожим названием «pysh». Этот раздел — именно "
        "про проект pysh-shell.com (пакет на PyPI называется <code class=\"inline\">pysh-shell</code>, "
        "команда — <code class=\"inline\">pysh</code>), а не про другие одноимённые "
        "инструменты.",
    )}

    <h2 id="chto-eto">Что такое PySH</h2>
    <p>PySH — это интерактивная командная оболочка (shell — раздел 3.3), написанная на чистом
    Python и позиционирующая себя как <strong>Python-first альтернатива</strong> традиционным
    shell вроде Bash. Официальное описание с сайта: «The Python-Native Automation Platform for
    Developers, System Administrators, and DevOps Engineers».</p>

    <h2 id="dva-podhoda">Два подхода к командной строке</h2>
{traditional_flow}
{pysh_converge}
    <p>Традиционный shell отлично подходит для коротких интерактивных команд — но чем сложнее
    становится скрипт, тем сильнее чувствуется нехватка настоящего языка программирования:
    структурных исключений, тестов, читаемых модулей. PySH предлагает другое направление: писать
    автоматизацию сразу на Python, не переключаясь между двумя разными языками.</p>

{callout(
        "info",
        "[[icon:idea]] Не путайте с полной заменой Bash",
        "PySH сам честно указывает в официальной документации: это <strong>не</strong> полная "
        "POSIX-совместимая замена <code class=\"inline\">/bin/sh</code>, не клон Zsh и не "
        "гарантированно совместим с любым существующим Bash-скриптом. Это самостоятельное "
        "направление с собственным, Python-ориентированным подходом — а не притворство, что "
        "внутри спрятан настоящий Bash.",
    )}

    <h2 id="zapusk">Запуск PySH — реальный вывод</h2>
    <p>На этом компьютере PySH уже установлен. Проверим это теми же командами, которыми вы
    проверяли бы любую другую программу:</p>

{code_block("Терминал", "command -v pysh\npysh --version", lang="text")}
{code_block("Реальный вывод", "/usr/bin/pysh\npysh 0.8.2", lang="text")}

    <p>Запустим PySH и посмотрим на настоящий баннер и приглашение:</p>

{code_block(
        "Терминал — реальная сессия PySH",
        "🐍 PySH 0.8.2 | Python 3.13.5 | GPL-2.0-only\n"
        "System: Debian GNU/Linux 13 | Kernel 6.12.101 | 11th Gen Intel Core i3-1115G4 | RAM 19 GiB\n"
        "Type 'exit' or press Ctrl+D to quit.\n"
        "┌─🐍 astra@soi ─ [~/Projects/Python_001] ─ git:feat/curriculum-v2-chapter-03\n"
        "│  py3.13 · uv0.11.24 · ruff0.15.20 · rust1.85.0 · node26.3.1 · npm11.16.0\n"
        "└─❯ ",
        lang="text",
    )}

{callout(
        "info",
        "[[icon:code]] О скриншотах на этой странице",
        "Эта страница показывает настоящий, дословно скопированный вывод реальной установленной "
        "PySH — терминальный вывод воспроизведён как текст, а не как фотография экрана, потому "
        "что окружение, в котором собирался этот курс, технически не может делать снимки экрана "
        "графических окон. Каждая команда на этой странице была выполнена по-настоящему.",
    )}

    <p>Приглашение PySH — двухстрочное и информативное: имя пользователя, хост, текущая папка,
    ветка git — и вторая строка с версиями инструментов проекта (Python, uv, ruff, и другие,
    если они найдены). Это тот же дух, что и у «продвинутых» тем оформления для Bash/Zsh, только
    встроенный по умолчанию.</p>

    <h2 id="obychnye-komandy">PySH понимает обычные команды</h2>
    <p>Несмотря на Python-first философию, привычные команды тоже работают — PySH умеет запускать
    внешние программы, пайпы и базовые операторы, как обычный shell:</p>

{code_block(
        "Реальная сессия",
        "└─❯ pwd\n/home/astra/Projects/Python_001\n"
        "└─❯ ls scripts | head -3\nbuild_book.py\nbuild_chapter_01.py\nbuild_chapter_02.py",
        lang="text",
    )}

    <h2 id="python-native">Python прямо в командной строке</h2>
    <p>А вот это уже отличает PySH от обычного shell: команда <code class="inline">py</code>
    выполняет настоящий Python прямо на месте, в постоянном (сохраняющемся между вызовами)
    контексте:</p>

{code_block(
        "Реальная сессия",
        "└─❯ py print(\"hello from python\")\nhello from python\n"
        "└─❯ py x = 10\n"
        "└─❯ py print(x)\n10",
        lang="text",
    )}

    <p>Переменные и импорты сохраняются между отдельными вызовами <code class="inline">py</code>
    — <code class="inline">x</code> из первой команды доступен во второй. Для более длинного кода
    есть и многострочный блок:</p>

{code_block(
        "Реальная сессия",
        "└─❯ py {\n"
        "import os\n"
        "targets = [p for p in os.environ.get(\"PATH\", \"\").split(\":\") if p]\n"
        "print(f\"PATH entries: {len(targets)}\")\n"
        "}\n"
        "PATH entries: 43",
        lang="text",
    )}

    <p>Есть и третий, более «тяжёлый» режим — полноценный вложенный Python REPL со своим
    <code class="inline">&gt;&gt;&gt;</code> приглашением, который включается командой
    <code class="inline">#py</code> прямо из обычного приглашения PySH:</p>

{code_block(
        "Реальная сессия",
        "└─❯ #py\n"
        "PySH Python Command Execution Layer | GPL-2.0-only\n"
        "Python 3.13.5\n"
        "Type #help for commands, Ctrl+D or #exit to return to PySH.\n\n"
        ">>> 2 + 2\n4\n"
        ">>> print(\"Привет, PySH!\")\nПривет, PySH!\n"
        ">>> #exit",
        lang="text",
    )}

    <h2 id="sravnenie">Bash-скрипт и PySH-подход: один пример</h2>
    <p>Небольшая иллюстрация разницы в стиле — не чтобы объявить один способ «плохим», а чтобы
    показать, откуда берётся Python-first идея.</p>

{classic_vs_modern(
        "Задача: посчитать файлы в текущей папке",
        "Bash",
        "count=$(ls | wc -l)\n"
        'echo "Файлов: $count"',
        "PySH (py-блок)",
        "py {\n"
        "    import os\n"
        "    count = len(os.listdir('.'))\n"
        "    print(f'Файлов: {count}')\n"
        "}",
        "Для короткой разовой команды Bash по-прежнему быстрее набрать. Но как только "
        "автоматизация обрастает условиями, обработкой ошибок и тестами — читаемый Python "
        "начинает выигрывать. PySH даёт этот путь, не заставляя переключаться в отдельный "
        ".py-файл.",
    )}

    <h2 id="lokalnaya-lab">[[icon:code]] Локальная лаборатория: попробуйте PySH (необязательно)</h2>
    <p>Это — необязательное упражнение для вашего собственного компьютера. Оно не проверяется
    автоматически и не является обязательным условием для прохождения курса Python — PySH стоит
    <strong>знать</strong>, а пользоваться им дальше или нет — решать вам.</p>

    <div class="exercise">
      <div class="exercise-stars">[[icon:code]] Необязательно · локально на вашем компьютере</div>
      <div class="exercise-title">Чек-лист: первый запуск PySH</div>
      <ul style="list-style:none;padding-left:0;margin-top:16px">
        <li style="margin-bottom:10px"><label style="display:flex;gap:10px;align-items:flex-start;cursor:pointer"><input type="checkbox" style="margin-top:4px;flex-shrink:0" /><span>Установите PySH: <code class="inline">pip install pysh-shell</code> (или найдите готовую установку через <code class="inline">command -v pysh</code>)</span></label></li>
        <li style="margin-bottom:10px"><label style="display:flex;gap:10px;align-items:flex-start;cursor:pointer"><input type="checkbox" style="margin-top:4px;flex-shrink:0" /><span>Запустите <code class="inline">pysh</code> и посмотрите на настоящий баннер и приглашение</span></label></li>
        <li style="margin-bottom:10px"><label style="display:flex;gap:10px;align-items:flex-start;cursor:pointer"><input type="checkbox" style="margin-top:4px;flex-shrink:0" /><span>Выполните одну простую команду, например <code class="inline">pwd</code> или <code class="inline">ls</code></span></label></li>
        <li style="margin-bottom:10px"><label style="display:flex;gap:10px;align-items:flex-start;cursor:pointer"><input type="checkbox" style="margin-top:4px;flex-shrink:0" /><span>Попробуйте команду <code class="inline">py print("hello")</code> — Python прямо из приглашения PySH</span></label></li>
        <li style="margin-bottom:10px"><label style="display:flex;gap:10px;align-items:flex-start;cursor:pointer"><input type="checkbox" style="margin-top:4px;flex-shrink:0" /><span>Выйдите командой <code class="inline">exit</code> или Ctrl+D</span></label></li>
      </ul>
    </div>

{callout(
        "info",
        "[[icon:note]] Официальные источники",
        "pysh-shell.com — сайт проекта; pypi.org/project/pysh-shell — страница пакета "
        "(<code class=\"inline\">pip install pysh-shell</code>); полная документация — в "
        "репозитории проекта, ссылка указана на PyPI-странице.",
    )}"""

    out = render_page(
        page_title="PySH: Python-first оболочка",
        description="Знакомство с PySH — Python-native альтернативой традиционным shell — на "
        "примере реального локально установленного окружения.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("PySH", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="PySH: Python-first оболочка",
        lede="Ещё один взгляд на командную строку — что если вместо мини-языка команд "
        "использовать прямо настоящий Python?",
        body_html=body,
        sidebar_groups=sidebar("03-08-pysh.html"),
        nav=PageNav(prev_href="03-07-semejstvo-obolochek.html", prev_label="Семейство командных оболочек", next_href="03-02-interaktivny-rezhim.html", next_label="Интерактивный режим (Python REPL)"),
    )
    write("03-08-pysh.html", out)


def build_02_repl() -> None:
    repl_cycle = timeline_diagram(
        [
            ("Read", "Python читает строку, которую вы набрали"),
            ("Eval", "вычисляет её как выражение или выполняет как код"),
            ("Print", "если это выражение — печатает результат"),
            ("Loop", "и снова ждёт следующую строку"),
        ],
        caption="REPL = Read – Eval – Print – Loop",
    )

    body = f"""
    <p>Кроме запуска файлов (раздел 3.1), у Python есть второй режим работы —
    <strong>интерактивный</strong>. В нём вы вводите код по одной строке и сразу видите
    результат, без файла и без явного «запуска» в привычном смысле. Мы уже называли это Python
    REPL или Python Shell в разделе 3.2 — теперь разберём его по-настоящему подробно.</p>

    <h2 id="zapusk-repl">Запуск</h2>
    <p>Откройте терминал (в VS Code, PyCharm или отдельным приложением — раздел 3.2) и наберите:</p>
{code_block("Терминал", "python", lang="text")}
    <p>Вы увидите что-то вроде:</p>
{code_block(
        "Реальный вывод",
        "Python 3.14.7 (main, Aug  5 2026, 00:00:00) [GCC ...] on linux\n"
        'Type "help", "copyright", "credits" or "license" for more information.\n'
        ">>> ",
        lang="text",
    )}
    <p>Приглашение <code class="inline">&gt;&gt;&gt;</code> означает: Python готов и ждёт вашу
    команду.</p>

    <h2 id="chto-takoe-repl">Что означает R-E-P-L</h2>
    <p>REPL — сокращение от <strong>Read–Eval–Print Loop</strong> («прочитать — выполнить —
    напечатать — повторить»). Именно так и работает интерактивный режим:</p>
{repl_cycle}

    <h2 id="primery">Первые примеры</h2>
{code_block(
        "Python REPL",
        '>>> 2 + 2\n4\n>>> "Py" + "thon"\n\'Python\'\n>>> name = "Анна"\n>>> name\n\'Анна\'',
        lang="text",
    )}
    <p>Обратите внимание: строка <code class="inline">name = "Анна"</code> НЕ показала результат
    — присваивание само по себе не является выражением, значение которого нужно печатать. А вот
    следующая строка, где мы просто написали <code class="inline">name</code>, — это уже
    выражение, и REPL сразу же его вычислил и напечатал.</p>

{callout(
        "tip",
        "[[icon:idea]] Почему REPL печатает сам, а файл — нет",
        "REPL автоматически показывает результат <em>последнего вычисленного выражения</em> в "
        "каждой введённой строке — это удобство именно интерактивного режима. Обычный "
        "<code class=\"inline\">.py</code>-файл выполняется целиком и молча — если нигде явно не "
        "вызвать <code class=\"inline\">print()</code>, на экране ничего не появится, даже если "
        "где-то в середине файла встретилось выражение вроде <code class=\"inline\">2 + 2</code>.",
    )}

    <h2 id="schitaet">Ваша оболочка умеет считать</h2>
    <p>Раз REPL сразу показывает результат каждой строки, его удобно использовать как быстрый
    калькулятор — без единого <code class="inline">print()</code>:</p>
{code_block("Python REPL", '>>> 2 + 2\n4\n>>> 10 / 4\n2.5\n>>> 3 * 7\n21', lang="text")}
    <p>Это работает только в самой оболочке: в обычном <code class="inline">.py</code>-файле
    строка <code class="inline">2 + 2</code> сама по себе ничего не выведет.</p>

{practice_card(
        "03-02",
        "Практика: интерактивный режим в ноутбуке",
        "Интерактивный ноутбук прямо в браузере — сравните ячейку Jupyter с Python REPL",
        "../../practice/03-02/index.html",
    )}
{practice_card(
        "03-03",
        "Практика: используйте Python как калькулятор",
        "Интерактивный ноутбук прямо в браузере — сложение, вычитание, умножение, деление",
        "../../practice/03-03/index.html",
    )}

    <h2 id="prompty">Два вида приглашения</h2>
    <ul>
      <li><code class="inline">&gt;&gt;&gt;</code> — <strong>основное</strong> приглашение: Python
        ждёт начало новой команды;</li>
      <li><code class="inline">...</code> — <strong>приглашение продолжения</strong>: Python
        видит, что текущая команда ещё не закончена (например, открыта скобка или начат блок), и
        ждёт остальное.</li>
    </ul>
{code_block(
        "Python REPL — многострочный пример",
        ">>> total = (\n...     2\n...     + 2\n... )\n>>> total\n4",
        lang="text",
    )}

    <h2 id="vyhod">Как выйти</h2>
    <p>Наберите <code class="inline">exit()</code> и нажмите Enter. Также работают клавиатурные
    сочетания: <code class="inline">Ctrl+Z</code> затем Enter на Windows, или
    <code class="inline">Ctrl+D</code> на macOS/Linux.</p>"""

    out = render_page(
        page_title="Интерактивный режим Python (Python REPL)",
        description="Python REPL подробно: цикл Read-Eval-Print-Loop, первые выражения, "
        "приглашения >>> и ..., и выход из режима.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("Интерактивный режим (Python REPL)", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="Интерактивный режим Python (Python REPL)",
        lede="Второй способ работать с Python — вводить код по одной строке и сразу видеть "
        "результат. Разберём, как он устроен на самом деле.",
        body_html=body,
        sidebar_groups=sidebar("03-02-interaktivny-rezhim.html"),
        nav=PageNav(prev_href="03-08-pysh.html", prev_label="PySH", next_href="03-09-repl-kak-instrument.html", next_label="REPL как инструмент исследования"),
    )
    write("03-02-interaktivny-rezhim.html", out)


def build_09_repl_tool() -> None:
    comparison = comparison_table(
        ["", "Script (.py)", "REPL", "Notebook (.ipynb)", "IDE/редактор"],
        [
            ["Что это", "Сохранённый файл с кодом", "Временный интерактивный сеанс", "Ячейки кода + текст + результаты", "Инструмент для редактирования/запуска/отладки"],
            ["Хранится?", "Да, на диске", "Нет — исчезает при выходе", "Да, в файле .ipynb", "—"],
            ["Лучше всего для", "Готовых программ", "Быстрых экспериментов", "Обучения, исследования данных", "Написания и отладки кода"],
            ["Python-язык?", "Да", "Да", "Да", "Нет — это инструмент, использующий Python"],
        ],
    )

    body = f"""
    <p>REPL — это не только способ запуска кода, но и удобный инструмент для того, чтобы задавать
    Python вопросы прямо во время работы. Три встроенные команды особенно полезны для
    исследования.</p>

    <h2 id="type">type() — какого типа это значение?</h2>
{code_block("Python REPL", ">>> type(42)\n<class 'int'>\n>>> type(\"Python\")\n<class 'str'>", lang="text")}

    <h2 id="help">help() — встроенная справка</h2>
{code_block("Python REPL", ">>> help(print)", lang="text")}
    <p>Появится описание функции прямо из официальной документации Python — работает даже без
    интернета, потому что справка встроена в сам интерпретатор.</p>

    <h2 id="dir">dir() — что вообще есть у значения</h2>
{code_block("Python REPL", ">>> dir(42)", lang="text")}

{callout(
        "info",
        "[[icon:idea]] Длинный список — это нормально",
        "<code class=\"inline\">dir()</code> покажет длинный список имён вроде "
        "<code class=\"inline\">__add__</code>, <code class=\"inline\">__class__</code> и "
        "другие — сейчас понимать каждое из них не нужно. Сама привычка «спросить у Python "
        "напрямую» гораздо важнее, чем немедленное понимание каждого имени в ответе.",
    )}

{practice_card(
        "03-05",
        "Практика: предскажите и проверьте",
        "Интерактивный ноутбук прямо в браузере — type(), help(), dir() на практике",
        "../../practice/03-05/index.html",
    )}

    <h2 id="script-vs-repl">Script vs REPL vs Notebook vs IDE</h2>
    <p>Мы уже встречали все четыре понятия по отдельности — соберём их в одну таблицу, чтобы
    видеть общую картину:</p>
{comparison}

    <h2 id="brauzernaya-praktika">А как насчёт браузерной практики этого курса?</h2>
    <p>Интерактивные упражнения, которые вы проходите прямо на этой странице курса, — это ещё
    один, пятый вариант: настоящий Python выполняется у вас в браузере через технологию
    <strong>Pyodide</strong> (подробнее — в разделе 3.16 про notebook и kernel). Это тоже
    полноценный Python — просто с другой средой выполнения, без установки на компьютер.</p>"""

    out = render_page(
        page_title="REPL как инструмент исследования",
        description="type(), help() и dir() как инструменты исследования Python — и сводная "
        "таблица Script vs REPL vs Notebook vs IDE.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("REPL как инструмент", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="REPL как инструмент исследования",
        lede="type(), help(), dir() — как задавать Python вопросы прямо во время работы, и чем "
        "в итоге отличаются script, REPL, notebook и IDE.",
        body_html=body,
        sidebar_groups=sidebar("03-09-repl-kak-instrument.html"),
        nav=PageNav(prev_href="03-02-interaktivny-rezhim.html", prev_label="Интерактивный режим (Python REPL)", next_href="03-03-vyvod-dannyh.html", next_label="Вывод данных с помощью Python"),
    )
    write("03-09-repl-kak-instrument.html", out)


def build_03_print() -> None:
    body = f"""
    <p>В файле <code class="inline">.py</code> ничего не выводится на экран само по себе — нужно
    явно попросить об этом командой <code class="inline">print()</code>. Мы уже пользовались ей в
    главе 1 и в REPL (раздел 3.5), теперь разберём подробнее — это первый настоящий инструмент,
    которым мы будем пользоваться в каждой программе этого курса.</p>

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
    <p>По умолчанию каждый <code class="inline">print()</code> завершается переводом строки
    (<code class="inline">\\n</code>) — поэтому следующий вызов начинается с новой строки.
    Параметр <code class="inline">end</code> позволяет это изменить:</p>
{code_block("print_end.py", 'print("Загрузка", end="")\nprint("...", end="")\nprint("готово!")\n')}
{code_block("вывод программы", 'Загрузка...готово!')}

{callout(
        "tip",
        "[[icon:idea]] Пустая строка",
        "Вызов <code class=\"inline\">print()</code> без аргументов просто выводит пустую строку "
        "— удобно, чтобы отделить блоки текста друг от друга.",
    )}

{callout(
        "info",
        "[[icon:note]] Официальный источник",
        "Полное описание всех параметров <code class=\"inline\">print()</code> — в разделе "
        "«Built-in Functions» на docs.python.org.",
    )}

{practice_card(
        "03-04",
        "Практика: sep, end и форматирование вывода",
        "Интерактивный ноутбук прямо в браузере — параметры print() на практике",
        "../../practice/03-04/index.html",
    )}"""

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
        nav=PageNav(prev_href="03-09-repl-kak-instrument.html", prev_label="REPL как инструмент", next_href="03-10-input-i-dialog.html", next_label="input(): первый диалог"),
    )
    write("03-03-vyvod-dannyh.html", out)


def build_10_input() -> None:
    input_flow = timeline_diagram(
        [
            ("Программа печатает приглашение", 'input("Как вас зовут? ")'),
            ("Программа ждёт", "выполнение приостановлено"),
            ("Пользователь печатает текст", "и нажимает Enter"),
            ("input() возвращает текст", "как строку"),
            ("Имя указывает на этот текст", "name = ..."),
            ("print() использует значение", "print(\"Привет,\", name)"),
        ],
        caption="Что происходит при вызове input()",
    )

    body = f"""
    <p>До сих пор наши программы только говорили — теперь научим их слушать.
    <code class="inline">input()</code> — первая команда, которая делает программу по-настоящему
    интерактивной: она приостанавливает выполнение и ждёт, пока человек что-то напечатает.</p>

    <h2 id="pervyj-dialog">Первый диалог</h2>
{code_block("dialog.py", 'name = input("Как вас зовут? ")\nprint("Привет,", name)\n')}
    <p>При запуске в терминале появится приглашение, программа будет ждать ввода, а затем
    поприветствует вас:</p>
{code_block("Терминал", 'Как вас зовут? Анна\nПривет, Анна', lang="text")}

    <h2 id="chto-proishodit">Что происходит по шагам</h2>
{input_flow}

{callout(
        "warning",
        "[[icon:warning]] input() всегда возвращает текст",
        "Даже если пользователь вводит цифры, <code class=\"inline\">input()</code> возвращает "
        "<strong>строку</strong> (текст), а не число. Чтобы получить настоящее число, текст нужно "
        "явно преобразовать — например, командой <code class=\"inline\">int(...)</code>. Подробно "
        "числа и преобразование типов мы разберём в следующей главе; здесь достаточно запомнить "
        "сам факт: результат <code class=\"inline\">input()</code> — всегда текст.",
    )}

{code_block(
        "Пример преобразования (забегая вперёд)",
        'age_text = input("Сколько вам лет? ")\nprint(int(age_text) + 1)\n',
    )}

{practice_card(
        "03-06",
        "Практика: input() и первый диалог",
        "Интерактивный ноутбук прямо в браузере — настоящее поле ввода",
        "../../practice/03-06/index.html",
    )}"""

    out = render_page(
        page_title="input(): первый диалог",
        description="input() — как программа начинает разговаривать с пользователем, и почему "
        "результат всегда текст.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("input(): первый диалог", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="input(): программа начинает разговаривать с человеком",
        lede="Первая команда, которая делает программу по-настоящему интерактивной.",
        body_html=body,
        sidebar_groups=sidebar("03-10-input-i-dialog.html"),
        nav=PageNav(prev_href="03-03-vyvod-dannyh.html", prev_label="Вывод данных с помощью Python", next_href="03-11-imena-i-znacheniya.html", next_label="Имена и значения"),
    )
    write("03-10-input-i-dialog.html", out)


def build_11_names() -> None:
    diagram = name_value_diagram("city", "'Warsaw'", caption="Имя указывает на значение — а не «содержит» его")

    body = f"""
    <p>Мы уже создавали имена вроде <code class="inline">name</code> в предыдущих разделах —
    настало время разобрать, что это на самом деле означает.</p>

    <h2 id="ne-korobka">Не «коробка с данными»</h2>
    <p>Частая, но не совсем точная метафора: «переменная — это коробка, в которую кладут
    значение». Она сбивает с толку в Python, потому что подразумевает, будто у каждого имени
    своя отдельная ячейка памяти. На самом деле правильнее думать иначе:</p>

{diagram}

    <p>Имя — это, скорее, стрелка, указывающая на значение. Присваивание
    <code class="inline">city = "Warsaw"</code> не «кладёт» строку внутрь <code class="inline">city</code>
    — оно заставляет имя <code class="inline">city</code> указывать на объект-строку
    <code class="inline">"Warsaw"</code>, который существует сам по себе.</p>

    <h2 id="pervoe-imya">Создание и чтение имени</h2>
{code_block("names.py", 'city = "Warsaw"\nprint(city)\n')}
    <p>Части этой строки:</p>
    <ul>
      <li><code class="inline">city</code> — имя (переменная);</li>
      <li><code class="inline">=</code> — оператор присваивания: «пусть имя слева указывает на
        значение справа»;</li>
      <li><code class="inline">"Warsaw"</code> — значение (объект).</li>
    </ul>

    <h2 id="odno-znachenie-neskolko-imen">Несколько имён — один объект</h2>
    <p>Поскольку имя — это просто указатель, у одного и того же объекта может быть несколько
    имён одновременно. Возьмём пример:</p>
{code_block("score.py", 'score = 100\nbest_score = score\nprint(score)\nprint(best_score)\n')}
    <p>Здесь <strong>два имени</strong> — <code class="inline">score</code> и
    <code class="inline">best_score</code> — но <strong>один объект</strong>, на который оба
    указывают:</p>

{converge_diagram(
        ["score", "best_score"],
        "100",
        caption="Две ссылки на один и тот же объект — а не два отдельных числа 100",
    )}

{callout(
        "warning",
        "[[icon:warning]] Частая ошибка мышления",
        "НЕ думайте, что Python «скопировал 100 в две переменные-коробки» — это ровно та модель, "
        "которую мы отвергли выше. На самом деле объект один, а связей (ссылок) с ним — две. "
        "Правильный термин для стрелки на диаграмме — <strong>ссылка</strong> (reference): "
        "«имя связано с объектом», а не «имя содержит значение».",
    )}

    <h2 id="rebinding">Переприсваивание не меняет старое имя</h2>
    <p>Продолжим тот же пример дальше:</p>
{code_block("score2.py", 'score = 100\nbest_score = score\nscore = 120\nprint(score)       # 120\nprint(best_score)  # всё ещё 100\n')}
    <p>Строка <code class="inline">score = 120</code> — это <strong>переприсваивание</strong>
    (rebinding): имя <code class="inline">score</code> начинает указывать на другой объект.
    Существующий объект <code class="inline">100</code> при этом никак не меняется —
    <code class="inline">best_score</code> по-прежнему указывает на него:</p>

{namespace_diagram(
        [("score", "120"), ("best_score", "100")],
        caption="После score = 120: у каждого имени теперь своя, независимая связь",
    )}

    <p>Это важная идея, к которой мы ещё не раз вернёмся — при разговоре о неизменяемости чисел
    и строк (глава 4), о списках и их отличии от чисел, о том, как один и тот же объект может
    быть доступен из нескольких мест, и о том, как значения передаются в функции. Пока
    достаточно запомнить сам принцип: <strong>переприсваивание меняет связь имени, а не
    объект.</strong></p>

    <h2 id="kogda-ischezaet">Когда объект «исчезает»?</h2>
    <p>Логичный вопрос: если <code class="inline">score</code> больше не указывает на
    <code class="inline">100</code>, что происходит с самим объектом <code class="inline">100</code>?
    Продолжим пример ещё на шаг:</p>
{code_block("score3.py", 'best_score = 130\nprint(score)       # 120\nprint(best_score)  # 130\n')}
    <p>Теперь ни <code class="inline">score</code>, ни <code class="inline">best_score</code> не
    указывают на объект <code class="inline">100</code> — у него не осталось ни одной связи:</p>

{namespace_diagram(
        [("score", "120"), ("best_score", "130")],
        unreachable=["100"],
        caption="100 стал недостижим — ни одно имя больше на него не указывает",
    )}

    <p>Объект <code class="inline">100</code> стал <strong>недостижимым</strong> (unreachable) —
    до него нельзя «дотянуться» ни через одно имя в программе. Именно в этот момент, а не раньше,
    Python может освободить память, которую он занимал.</p>

{callout(
        "warning",
        "[[icon:warning]] Так писать неточно",
        "«Как только переменная перестаёт указывать на значение, сборщик мусора немедленно "
        "удаляет это значение» — эта формулировка вводит в заблуждение. Удаление одной связи "
        "НЕ уничтожает объект, если на него по-прежнему указывают другие имена (как "
        "<code class=\"inline\">best_score</code> указывал на <code class=\"inline\">100</code> "
        "даже после того, как <code class=\"inline\">score</code> переприсвоили). Объект "
        "становится кандидатом на удаление только тогда, когда <strong>ни одной</strong> "
        "связи с ним не остаётся.",
    )}

    <h2 id="gc">Сборщик мусора: автоматическое управление памятью</h2>
    <p>Вам, как правило, никогда не придётся вручную «освобождать» память в Python. За этим
    следит <strong>сборщик мусора</strong> (garbage collector, GC) — часть самого Python,
    которая освобождает память недостижимых объектов автоматически.</p>

{callout(
        "tip",
        "[[icon:idea]] Достаточно для повседневной работы",
        "Python сам следит за объектами и освобождает память, когда объект больше нельзя "
        "использовать ни через одно имя в программе. Именно поэтому в Python (в отличие от "
        "языков вроде C) вы почти никогда не пишете код специально для освобождения памяти.",
    )}

    <h2 id="glubzhe-refcounting">[[icon:experiment]] Что происходит глубже: подсчёт ссылок</h2>
    <p>Это необязательный, более глубокий взгляд — можно спокойно пропустить его при первом
    чтении и вернуться позже.</p>
    <p>В CPython (реализация Python, которой мы пользуемся) у каждого объекта есть счётчик:
    сколько ссылок на него сейчас существует. Пройдём наш же пример ещё раз, но уже с этим
    счётчиком:</p>
{code_block(
        "Объект 100 — счётчик ссылок",
        "score = 100          # объект 100: ссылок = 1\n"
        "best_score = score   # объект 100: ссылок = 2\n"
        "score = 120          # объект 100: ссылок = 1  (score теперь указывает на 120)\n"
        "best_score = 130     # объект 100: ссылок = 0  (недостижим)",
        lang="text",
    )}
    <p>Для обычных, не входящих в циклическую ссылку объектов в CPython момент, когда счётчик
    достигает нуля, обычно совпадает с моментом освобождения памяти — почти сразу, без задержки.
    Это удобное, практичное поведение, но не гарантия, зафиксированная языком Python в целом —
    другие реализации Python (например, PyPy) освобождают память по другим правилам.</p>

    <p>У подсчёта ссылок есть одна принципиальная сложность — <strong>циклические
    ссылки</strong>:</p>
{code_block(
        "Циклическая ссылка (концептуально)",
        "A ──→ B\n↑      │\n└──────┘",
        lang="text",
    )}
    <p>Представьте два объекта, каждый из которых ссылается на другой. Даже если ни одно имя в
    программе больше не указывает ни на A, ни на B, они всё ещё ссылаются друг на друга — и
    счётчик ссылок каждого из них не опускается до нуля. Поэтому в CPython, кроме подсчёта
    ссылок, есть отдельный <strong>циклический сборщик мусора</strong>, который периодически
    ищет именно такие недостижимые снаружи циклы и освобождает их.</p>

{callout(
        "info",
        "[[icon:note]] Идём дальше — не сейчас",
        "Мы намеренно останавливаемся здесь. К управлению памятью, времени жизни объектов и "
        "модулю <code class=\"inline\">gc</code> мы ещё вернёмся позже в курсе, когда появятся "
        "структуры данных, которые реально могут образовывать циклы (например, объекты, "
        "ссылающиеся друг на друга). Сейчас достаточно знать, что такая ситуация существует и "
        "у Python есть механизм для неё.",
    )}

    <h2 id="del">Маленькая заметка про del</h2>
    <p>Команда <code class="inline">del</code> удаляет не объект, а конкретную связь
    (имя):</p>
{code_block("del_demo.py", 'x = 100\ny = x\ndel x\nprint(y)  # 100 — объект никуда не делся\n')}
    <p><code class="inline">del x</code> убирает имя <code class="inline">x</code> из
    пространства имён — но НЕ означает «удали объект 100, что бы ни случилось». Поскольку
    <code class="inline">y</code> по-прежнему указывает на <code class="inline">100</code>,
    объект остаётся полностью доступным через <code class="inline">y</code>.</p>

    <h2 id="prostaya-model-pamyati">Пространство имён</h2>
    <p>Пока программа работает, Python хранит список всех созданных имён и того, на что каждое
    из них сейчас указывает, — это называется <strong>пространством имён</strong> (namespace).
    Диаграммы выше как раз и показывают срез такого пространства имён в разные моменты
    выполнения программы.</p>

    <h2 id="nameerror">Обращение к ещё не созданному имени</h2>
    <p>Если обратиться к имени раньше, чем оно было создано присваиванием, Python не может
    догадаться, что вы имеете в виду — и сообщает об ошибке:</p>
{code_block("broken.py", 'print(favourite_city)\nfavourite_city = "Warsaw"\n', )}
{code_block(
        "Ошибка",
        "NameError: name 'favourite_city' is not defined",
        lang="text",
    )}
    <p>Подробно про ошибки и то, как читать такие сообщения, — в разделе 3.13.</p>

{practice_card(
        "03-07",
        "Практика: имена и значения",
        "Интерактивный ноутбук прямо в браузере — присваивание, чтение, NameError",
        "../../practice/03-07/index.html",
    )}"""

    out = render_page(
        page_title="Имена и значения",
        description="Что такое имя (переменная) в Python — не «коробка», а указатель на "
        "значение, — и как читать NameError.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("Имена и значения", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="Первые имена и значения",
        lede="Правильная мысленная модель переменной в Python — не коробка с данными, а имя, "
        "указывающее на значение.",
        body_html=body,
        sidebar_groups=sidebar("03-11-imena-i-znacheniya.html"),
        nav=PageNav(prev_href="03-10-input-i-dialog.html", prev_label="input(): первый диалог", next_href="03-12-kommentarii-i-stil.html", next_label="Комментарии и читаемый код"),
    )
    write("03-11-imena-i-znacheniya.html", out)


def build_12_comments_style() -> None:
    body = f"""
    <h2 id="kommentarii">Комментарии</h2>
    <p>Строка, начинающаяся с <code class="inline">#</code>, — это <strong>комментарий</strong>:
    Python полностью её игнорирует при выполнении. Комментарии существуют не для компьютера, а
    для людей — включая вас самих через полгода.</p>
{code_block(
        "privet.py",
        '# Спрашиваем имя, чтобы персонализировать приветствие\nname = input("Как вас зовут? ")\nprint("Привет,", name)\n',
    )}

{callout(
        "tip",
        "[[icon:idea]] Хороший комментарий объясняет «почему», а не «что»",
        "Комментарий вроде <code class=\"inline\"># складываем a и b</code> над строкой "
        "<code class=\"inline\">c = a + b</code> бесполезен — код и так это показывает. "
        "Полезный комментарий объясняет то, что не видно из самого кода: почему выбрано именно "
        "такое решение, какая бизнес-логика за этим стоит, на что стоит обратить внимание в "
        "будущем.",
    )}

    <p>На этапе обучения совершенно нормально оставлять больше комментариев, чем оставил бы
    опытный разработчик в готовом проекте — они помогают вам самим проговорить, что делает
    каждая строка. Не переживайте, если пока хочется комментировать почти всё.</p>

    <h2 id="imena-fajlov">Имена файлов и переменных</h2>
    <p>Хороший стиль в именах экономит время — и вам, и всем, кто читает код после вас:</p>
    <ul>
      <li>используйте <strong>строчные буквы</strong>: <code class="inline">privet.py</code>, а
        не <code class="inline">Privet.PY</code>;</li>
      <li>используйте <strong>осмысленные имена</strong>: <code class="inline">calculator.py</code>,
        а не <code class="inline">file1.py</code>;</li>
      <li>для нескольких слов используйте <strong>подчёркивание</strong>:
        <code class="inline">my_first_program.py</code>, а не пробелы или регистр;</li>
      <li>избегайте пробелов в именах файлов — они удобны в графическом интерфейсе, но неудобны
        в терминале, где приходится экранировать каждый пробел.</li>
    </ul>
{comparison_table(
        ["Плохо", "Хорошо"],
        [
            ["<code class=\"inline\">New File FINAL 2!!.py</code>", "<code class=\"inline\">calculator.py</code>"],
            ["<code class=\"inline\">a.py</code>", "<code class=\"inline\">temperature_converter.py</code>"],
            ["<code class=\"inline\">MyFirstProgram.py</code>", "<code class=\"inline\">my_first_program.py</code>"],
        ],
    )}

{callout(
        "info",
        "[[icon:note]] PEP 8",
        "Официальный гид по стилю Python-кода — PEP 8 (peps.python.org/pep-0008) — мы уже "
        "упоминали его в главе 1. Он описывает куда больше, чем имена файлов, но сейчас "
        "достаточно знать: он существует, и его рекомендации разделяет практически всё "
        "сообщество Python.",
    )}"""

    out = render_page(
        page_title="Комментарии и читаемый код",
        description="Комментарии в Python, и базовые правила хорошего стиля для имён файлов и "
        "переменных.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("Комментарии и читаемый код", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="Комментарии и читаемый код",
        lede="Небольшие привычки, которые сильно облегчают жизнь — себе будущему и всем, кто "
        "будет читать ваш код.",
        body_html=body,
        sidebar_groups=sidebar("03-12-kommentarii-i-stil.html"),
        nav=PageNav(prev_href="03-11-imena-i-znacheniya.html", prev_label="Имена и значения", next_href="03-04-idle.html", next_label="Режим сценариев IDLE"),
    )
    write("03-12-kommentarii-i-stil.html", out)


def build_04_idle() -> None:
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
        "автодополнения, отладчика и подсветки ошибок на лету. Мы в основном пользуемся VS Code "
        "или PyCharm — но IDLE стоит знать: именно её вы увидите, если попробуете Python на "
        "чужом компьютере без дополнительной настройки.",
    )

    body = f"""
    <p>У Python есть встроенный простой редактор кода, который устанавливается автоматически
    вместе с самим Python, — <strong>IDLE</strong> (Integrated Development and Learning
    Environment). Открыть его можно, найдя «IDLE» в меню Пуск (Windows) или Launchpad (Mac), или
    набрав <code class="inline">idle3</code> в терминале (Linux).</p>

{callout(
        "info",
        "[[icon:idea]] Зачем IDLE вообще существует",
        "IDLE — не «устаревший мусор», который стоит забыть. Его цель — быть простым и всегда "
        "доступным сразу после установки Python, без единого дополнительного шага. Это делает "
        "его удобным для самого первого знакомства с языком и для быстрых экспериментов, когда "
        "открывать полноценный редактор кода — избыточно.",
    )}

    <h2 id="python-shell-idle">Python Shell — окно интерактивной оболочки</h2>
    <p>При запуске IDLE открывается интерактивная оболочка — тот же самый Python REPL, что мы
    разбирали в разделах 3.5–3.6, только в собственном окне с небольшими удобствами вроде
    подсветки синтаксиса.</p>

    <h2 id="rezhim-scenariev">Режим сценариев (Script Mode)</h2>
    <p>Чтобы написать полноценную программу, нужен отдельный файл: <strong>File → New
    File</strong> откроет пустое окно редактора — это и есть «режим сценариев», второй режим
    работы IDLE.</p>
    <ol>
      <li>Наберите код в новом окне редактора.</li>
      <li>Сохраните файл: <strong>File → Save</strong> (расширение <code class="inline">.py</code>
        подставится само).</li>
      <li>Запустите: <strong>Run → Run Module</strong>, либо просто нажмите клавишу
        <code class="inline">F5</code>.</li>
      <li>Результат появится в окне интерактивной оболочки IDLE.</li>
    </ol>

    <h2 id="kogda-idle">Когда стоит использовать IDLE</h2>
{cvm}"""

    out = render_page(
        page_title="Режим сценариев IDLE",
        description="Знакомимся с IDLE — встроенным редактором Python — Python Shell и режим "
        "сценариев, и сравниваем его с VS Code и PyCharm.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("Режим сценариев IDLE", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="IDLE — что это и когда он полезен",
        lede="Python сам приносит с собой простой редактор — IDLE. Разберёмся, как им "
        "пользоваться и когда стоит перейти на более мощный инструмент.",
        body_html=body,
        sidebar_groups=sidebar("03-04-idle.html"),
        nav=PageNav(prev_href="03-12-kommentarii-i-stil.html", prev_label="Комментарии и читаемый код", next_href="03-05-praktika-itogi.html", next_label="Практика: выведите своё имя"),
    )
    write("03-04-idle.html", out)


def build_05_checkpoint() -> None:
    body = f"""
    <p>Небольшой контрольный чек-пойнт: применим файл, REPL, <code class="inline">print()</code>
    и выбор редактора (включая IDLE) в одном упражнении, прежде чем идти дальше — к ошибкам,
    отладке и первому настоящему мини-проекту.</p>

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
    )}"""

    out = render_page(
        page_title="Практика: выведите своё имя",
        description="Контрольное упражнение главы 3: файл, терминал, print и выбор редактора — "
        "в одном небольшом упражнении.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("Практика: выведите своё имя", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="Практика: выведите своё имя (и кое-что ещё)",
        lede="Собираем воедино файл, терминал, print и выбор редактора — в одном небольшом "
        "упражнении, прежде чем двигаться дальше.",
        body_html=body,
        sidebar_groups=sidebar("03-05-praktika-itogi.html"),
        nav=PageNav(prev_href="03-04-idle.html", prev_label="Режим сценариев IDLE", next_href="03-13-oshibki-i-traceback.html", next_label="Ошибки, traceback и как их читать"),
    )
    write("03-05-praktika-itogi.html", out)


def build_13_errors_traceback() -> None:
    anatomy = timeline_diagram(
        [
            ("Traceback (most recent call last):", "заголовок — сообщает, что дальше будет цепочка вызовов"),
            ("File \"privet.py\", line 3", "ГДЕ — какой файл и какая строка"),
            ("print(\"Привет\"", "сама проблемная строка кода"),
            ("SyntaxError: ...", "ЧТО и ПОЧЕМУ — тип ошибки и объяснение"),
        ],
        caption="Анатомия traceback — читаем снизу вверх",
    )

    fix_flow = flow_diagram(
        [
            ("Где?", "строка и файл"),
            ("Что?", "тип ошибки"),
            ("Почему?", "объяснение"),
            ("Чиним", "и запускаем снова"),
        ],
        caption="Порядок работы с любой ошибкой",
    )

    body = f"""
    <p>Красный текст ошибки — это не повод паниковать. Это <strong>данные</strong>: Python
    подробно объясняет, что именно пошло не так и где именно искать проблему. Научиться спокойно
    читать эти сообщения — один из самых полезных навыков для новичка.</p>

    <h2 id="syntaxerror">SyntaxError</h2>
    <p>Python не может даже понять структуру кода — до выполнения дело не дошло вовсе. Чаще
    всего причина — пропущенная скобка, кавычка или двоеточие.</p>
{code_block("broken.py", 'print("Привет"\n', lang="python")}
{code_block(
        "Traceback",
        '  File "broken.py", line 1\n    print("Привет"\n                 ^\nSyntaxError: \'(\' was never closed',
        lang="text",
    )}

    <h2 id="nameerror">NameError</h2>
    <p>Python встретил имя, которого ещё нигде не было создано присваиванием — часто это просто
    опечатка.</p>
{code_block("broken2.py", 'print(usr_name)\n', lang="python")}
{code_block(
        "Traceback",
        'Traceback (most recent call last):\n  File "broken2.py", line 1, in <module>\n    print(usr_name)\n          ^^^^^^^^\nNameError: name \'usr_name\' is not defined',
        lang="text",
    )}

    <h2 id="indentationerror">IndentationError</h2>
    <p>В Python отступы — часть синтаксиса (мы вернёмся к этому подробно в главе про условия и
    циклы). Несогласованный отступ — тоже ошибка:</p>
{code_block("broken3.py", 'name = "Cartesian"\n    print(name)\n', lang="python")}
{code_block(
        "Traceback",
        '  File "broken3.py", line 2\n    print(name)\nIndentationError: unexpected indent',
        lang="text",
    )}

    <h2 id="anatomiya">Анатомия traceback</h2>
    <p>Traceback лучше всего читать <strong>снизу вверх</strong> — самая важная информация внизу:</p>
{anatomy}

{fix_flow}

{callout(
        "tip",
        "[[icon:launch]] Не бойтесь красного текста",
        "Ошибка — это Python, честно объясняющий, что случилось. Профессиональные разработчики "
        "видят traceback-и десятки раз в день — разница лишь в том, что они умеют быстро находить "
        "в нём нужную строку. Теперь и вы умеете.",
    )}

{practice_card(
        "03-08",
        "Практика: прочитайте traceback (NameError)",
        "Интерактивный ноутбук прямо в браузере — найдите и исправьте опечатку",
        "../../practice/03-08/index.html",
    )}"""

    out = render_page(
        page_title="Ошибки, traceback и как их читать",
        description="SyntaxError, NameError, IndentationError — и анатомия traceback: где, что "
        "и почему.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("Ошибки и traceback", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="Ошибки, traceback и как их читать",
        lede="Ошибки — это данные, а не повод для паники. Разберём три самых частых типа и "
        "научимся читать traceback осмысленно.",
        body_html=body,
        sidebar_groups=sidebar("03-13-oshibki-i-traceback.html"),
        nav=PageNav(prev_href="03-05-praktika-itogi.html", prev_label="Практика: выведите своё имя", next_href="03-14-debug-laboratorii.html", next_label="Лаборатории отладки"),
    )
    write("03-13-oshibki-i-traceback.html", out)


def build_14_debug_labs() -> None:
    def lab(num, title, broken_code, symptom, fix_code, explanation):
        return f"""
        <div class="callout callout-debug">
          <div>
            <div class="callout-title">[[icon:debug]] Лаборатория {num}. {title}</div>
            <div class="callout-body">
              <p><strong>1. Предскажите:</strong> прочитайте код ниже — как вы думаете, что произойдёт?</p>
{code_block("сломанный код", broken_code, lang="python")}
              <p><strong>2. Запустите</strong> — вы увидите: <code class="inline">{symptom}</code></p>
              <p><strong>3. Исправление:</strong></p>
{code_block("исправлено", fix_code, lang="python")}
              <p><strong>4. Почему:</strong> {explanation}</p>
            </div>
          </div>
        </div>"""

    labs_html = "".join([
        lab(
            1,
            "Пропущенная кавычка или скобка",
            'print("Привет, мир!\n',
            "SyntaxError: unterminated string literal",
            'print("Привет, мир!")\n',
            "у открывающей кавычки не было пары — Python не понял, где заканчивается текст.",
        ),
        lab(
            2,
            "Неправильное имя переменной",
            'user_name = "Cartesian"\nprint(usr_name)\n',
            "NameError: name 'usr_name' is not defined",
            'user_name = "Cartesian"\nprint(user_name)\n',
            "опечатка в имени — <code class=\"inline\">usr_name</code> вместо <code class=\"inline\">user_name</code>. Python не «догадывается» об опечатках — для него это два разных имени.",
        ),
        lab(
            3,
            "Ошибка отступа",
            'print("Начало")\n  print("Продолжение")\n',
            "IndentationError: unexpected indent",
            'print("Начало")\nprint("Продолжение")\n',
            "у второй строки появился отступ, которого там быть не должно — вне блоков (if/for/def, которые встретятся в следующих главах) все строки должны начинаться с одной и той же позиции.",
        ),
        lab(
            4,
            "Программа работает, но выводит не то",
            'name = "Анна"\ncity = "Москва"\nprint("Привет,", city)\n',
            "Привет, Москва  (а должно быть — имя)",
            'name = "Анна"\ncity = "Москва"\nprint("Привет,", name)\n',
            "программа выполнилась без единой ошибки — но перепутаны переменные. Это самый коварный тип бага: Python не может знать, что вы имели в виду не то, что написали.",
        ),
        lab(
            5,
            "Не тот интерпретатор — привет из главы 2",
            'import requests\nprint("Пакет найден!")\n',
            "ModuleNotFoundError: No module named 'requests' (хотя вы точно его ставили!)",
            "# в VS Code: Ctrl+Shift+P -> \"Python: Select Interpreter\"\n"
            "# выбрать интерпретатор именно из активного .venv проекта",
            "пакет установлен в одно окружение, а код запускается через другое — классическая проблема из главы 2 (раздел 2.16). Проверьте <code class=\"inline\">sys.executable</code> и выбранный интерпретатор в редакторе.",
        ),
    ])

    body = f"""
    <p>Пять коротких лабораторий — специально сломанный код, чтобы потренироваться находить и
    чинить проблему по одному и тому же алгоритму: предсказать → запустить → изучить → исправить
    → объяснить себе, почему это сработало.</p>

{labs_html}

{practice_card(
        "03-09",
        "Практика: прочитайте traceback (SyntaxError)",
        "Интерактивный ноутбук прямо в браузере — найдите пропущенную скобку и кавычку",
        "../../practice/03-09/index.html",
    )}"""

    out = render_page(
        page_title="Лаборатории отладки",
        description="Пять коротких лабораторий отладки: пропущенная кавычка, опечатка в имени, "
        "ошибка отступа, перепутанные переменные и не тот интерпретатор.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("Лаборатории отладки", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="Лаборатории отладки",
        lede="Пять коротких, специально сломанных примеров — потренируем один и тот же навык: "
        "предсказать, запустить, изучить, исправить.",
        body_html=body,
        sidebar_groups=sidebar("03-14-debug-laboratorii.html"),
        nav=PageNav(prev_href="03-13-oshibki-i-traceback.html", prev_label="Ошибки и traceback", next_href="03-15-otladchik-v-ide.html", next_label="Первый отладчик в IDE"),
    )
    write("03-14-debug-laboratorii.html", out)


def build_15_debugger() -> None:
    debug_flow = flow_diagram(
        [
            ("Точка останова", "клик слева от номера строки"),
            ("Run and Debug", "запуск в режиме отладки"),
            ("Пауза", "программа остановилась на этой строке"),
            ("Осмотр", "видим текущие значения имён"),
        ],
        caption="Общая идея отладчика — одинаковая в VS Code и в PyCharm",
    )

    body = f"""
    <p>Отладчик (debugger) — инструмент, который умеет <strong>приостанавливать</strong>
    выполняющуюся программу в конкретной строке и показывать, чему в этот момент равны все
    имена (раздел 3.9). Это гораздо мощнее, чем расставлять
    <code class="inline">print()</code> по всему коду и запускать заново.</p>

{debug_flow}

    <p>Возьмём один и тот же крошечный пример для обеих сред:</p>
{code_block("debug_demo.py", 'name = "Анна"\ncity = "Варшава"\ngreeting = "Привет, " + name\nprint(greeting)\n')}

    <h2 id="vscode-debugger">Отладчик в VS Code</h2>
    <ol>
      <li>Кликните слева от номера строки <code class="inline">greeting = "Привет, " + name</code>
        — появится красная точка (breakpoint, точка останова).</li>
      <li>Откройте вкладку <strong>Run and Debug</strong> на боковой панели (или нажмите
        <code class="inline">F5</code>).</li>
      <li>Программа запустится и остановится ровно на точке останова — строка подсветится.</li>
      <li>В панели <strong>Variables</strong> слева видно текущие значения: <code class="inline">name</code>
        уже существует, а <code class="inline">greeting</code> — ещё нет (мы остановились ДО
        выполнения этой строки).</li>
      <li><strong>Step Over</strong> (значок со стрелкой поверх точки) выполняет ровно одну
        строку и снова останавливается — теперь <code class="inline">greeting</code> тоже
        появится в списке переменных.</li>
      <li><strong>Continue</strong> (▷) отпускает программу до конца или до следующей точки
        останова.</li>
    </ol>

    <h2 id="pycharm-debugger">Отладчик в PyCharm</h2>
    <p>Идея та же самая — отличаются только названия кнопок:</p>
{comparison_table(
        ["Действие", "VS Code", "PyCharm"],
        [
            ["Поставить точку останova", "Клик слева от номера строки", "Клик слева от номера строки"],
            ["Запустить с отладкой", "Run and Debug / F5", "Значок с жуком рядом с Run"],
            ["Выполнить одну строку", "Step Over", "Step Over (F8)"],
            ["Продолжить до конца/следующей точки", "Continue", "Resume Program"],
            ["Посмотреть значения переменных", "Панель Variables", "Панель Variables (внизу)"],
        ],
    )}

{callout(
        "info",
        "[[icon:code]] О скриншотах на этой странице",
        "Эта страница описывает реальный, стандартный интерфейс отладчика VS Code и PyCharm "
        "текстом и диаграммой, а не скриншотом — окружение, в котором собирался этот курс, не "
        "может делать снимки экрана графических приложений. Сама последовательность действий "
        "(точка останова → запуск с отладкой → пауза → осмотр значений → Step Over/Continue) "
        "полностью совпадает с тем, что вы увидите на экране.",
    )}

{callout(
        "tip",
        "[[icon:launch]] Главная идея",
        "Отладчик позволяет ПРИОСТАНОВИТЬ работающую программу и заглянуть внутрь неё — увидеть "
        "реальные значения имён в реальный момент выполнения, а не гадать по коду, что должно "
        "было произойти.",
    )}"""

    out = render_page(
        page_title="Первый отладчик в IDE",
        description="Точки останова, Step Over и Continue — базовая работа с отладчиком в VS "
        "Code и PyCharm на одном простом примере.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("Первый отладчик", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="Первый отладчик в IDE",
        lede="Отладчик умеет то, что не умеет print() — приостановить программу и заглянуть "
        "внутрь неё.",
        body_html=body,
        sidebar_groups=sidebar("03-15-otladchik-v-ide.html"),
        nav=PageNav(prev_href="03-14-debug-laboratorii.html", prev_label="Лаборатории отладки", next_href="03-16-notebook-i-kernel.html", next_label="Notebook и kernel"),
    )
    write("03-15-otladchik-v-ide.html", out)


def build_16_notebook_kernel() -> None:
    nb_flow = flow_diagram(
        [
            ("03-lesson.ipynb", "файл с ячейками"),
            ("Notebook-интерфейс", "показывает ячейки"),
            ("Kernel", "процесс Python"),
            ("Результат", "возвращается в ячейку"),
        ],
        caption="От файла блокнота до результата — через ядро",
    )

    practice_flow = flow_diagram(
        [
            ("Браузер", "интерфейс урока"),
            ("Worker", "фоновый поток вкладки"),
            ("Pyodide", "настоящий Python в браузере"),
            ("Грейдер", "проверяет результат"),
        ],
        caption="Как устроена браузерная практика этого курса",
    )

    body = f"""
    <p>Мы уже проходили практику этого курса в браузере — самое время объяснить, что там на
    самом деле происходит, с точки зрения выполнения кода.</p>

    <h2 id="notebook-vs-kernel">Notebook — это не то же самое, что kernel</h2>
    <ul>
      <li><strong>notebook</strong> (<code class="inline">.ipynb</code>) — сам файл: набор ячеек
        с кодом, текстом и уже сохранёнными результатами прошлого запуска;</li>
      <li><strong>kernel</strong> (ядро) — отдельный работающий процесс Python, который реально
        выполняет код из ячеек, когда вы их запускаете.</li>
    </ul>
{nb_flow}
    <p>Один и тот же файл блокнота можно открыть и подключить к разным ядрам — например, к ядру
    с одним набором установленных пакетов или с другим (мы говорили об этом в главе 2, раздел
    2.15, применительно к VS Code).</p>

    <h2 id="sostoyanie">Важная особенность: состояние сохраняется между ячейками</h2>
    <p>В отличие от обычного скрипта, который каждый раз выполняется <strong>с самого начала</strong>,
    в блокноте переменные, созданные в одной ячейке, остаются доступны в следующих — пока
    работает то же самое ядро.</p>
{code_block("Ячейка 1", 'x = 10')}
{code_block("Ячейка 2 (запущена ПОСЛЕ ячейки 1)", 'print(x)  # 10 — x всё ещё существует')}

{callout(
        "warning",
        "[[icon:warning]] Порядок запуска ячеек — это не порядок ячеек на экране",
        "Если запустить ячейки не по порядку (например, вторую раньше первой) или перезапустить "
        "ядро, не выполнив всё заново, — результат может не совпасть с тем, что вы видите на "
        "экране. Это одна из самых частых причин путаницы у новичков в блокнотах: то, что "
        "показано на экране, — результат ПОСЛЕДНЕГО запуска, а не гарантия того, что получится "
        "при выполнении сверху вниз прямо сейчас.",
    )}

    <h2 id="brauzernaya-praktika">Как устроена браузерная практика этого курса</h2>
    <p>Все интерактивные упражнения курса — настоящий Python, а не имитация. Устроено это так:</p>
{practice_flow}
    <p><strong>Pyodide</strong> — это реальный интерпретатор Python, скомпилированный в
    WebAssembly и запускающийся прямо в вашем браузере, без установки на компьютер. Это ещё одна
    среда выполнения — со своими ограничениями: например, у неё нет доступа к нативным
    графическим окнам операционной системы, поэтому пакеты вроде <code class="inline">tkinter</code>
    в чистом виде там не работают (в курсе такие упражнения честно помечены как «локальные» — вы
    уже видели это в главе 2).</p>

{callout(
        "info",
        "[[icon:note]] Официальный источник",
        "Подробнее о самом Jupyter — jupyter.org; о Pyodide — pyodide.org.",
    )}"""

    out = render_page(
        page_title="Notebook и kernel",
        description="Разница между файлом блокнота (notebook) и ядром (kernel), сохранение "
        "состояния между ячейками, и как устроена браузерная практика курса.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("Notebook и kernel", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="Notebook и kernel",
        lede="Что на самом деле происходит, когда вы запускаете ячейку — в блокноте и в "
        "браузерной практике этого курса.",
        body_html=body,
        sidebar_groups=sidebar("03-16-notebook-i-kernel.html"),
        nav=PageNav(prev_href="03-15-otladchik-v-ide.html", prev_label="Первый отладчик", next_href="03-17-mini-proekt-i-itogi.html", next_label="Мини-проект и итоги главы"),
    )
    write("03-16-notebook-i-kernel.html", out)


def build_17_mini_project() -> None:
    body = f"""
    <p>Пора собрать почти всё, что мы прошли в этой главе, в один небольшой, но настоящий
    проект.</p>

    <h2 id="proekt">Мини-проект: визитная карточка в терминале</h2>
    <p>Программа спрашивает имя, город и то, что вы хотите создать на Python — а затем печатает
    небольшой персонализированный профиль.</p>

{code_block(
        "card.py",
        'name = input("Ваше имя: ")\n'
        'city = input("Ваш город: ")\n'
        'goal = input("Что вы хотите создать на Python? ")\n\n'
        'print("========================")\n'
        'print(" МОЯ PYTHON-КАРТОЧКА")\n'
        'print("========================")\n'
        'print("Имя:", name)\n'
        'print("Город:", city)\n'
        'print("Хочу создать:", goal)\n'
        'print("========================")\n',
    )}

    <p>Пример того, что должно получиться:</p>
{code_block(
        "Пример вывода",
        "========================\n МОЯ PYTHON-КАРТОЧКА\n========================\n"
        "Имя: Анна\nГород: Варшава\nХочу создать: игру\n========================",
        lang="text",
    )}

{callout(
        "tip",
        "[[icon:idea]] Только то, что уже знакомо",
        "Весь проект построен исключительно на инструментах этой главы: "
        "<code class=\"inline\">input()</code>, присваивание, <code class=\"inline\">print()</code>. "
        "Условия и циклы, которые сделали бы код гибче, придут в следующих главах — а пока "
        "достаточно и этого, чтобы получить настоящую, законченную маленькую программу.",
    )}

{exercise(
        3,
        "[[icon:launch]] Challenge: своё оформление",
        "Придумайте собственное оформление визитки — другая рамка (например, из "
        "<code class=\"inline\">*</code>), выравнивание через <code class=\"inline\">sep</code>, "
        "или добавьте четвёртую строку с любимым языком программирования.",
    )}

{practice_card(
        "03-10",
        "Практика: мини-проект «Python-визитка»",
        "Интерактивный ноутбук прямо в браузере — соберите всё вместе",
        "../../practice/03-10/index.html",
    )}

    <h2 id="itogi">Итоги главы</h2>
{summary_box("Что мы теперь умеем", [
        "Понимаем, что программа на Python — обычный текстовый .py-файл, и как CPython "
        "превращает исходный код в байт-код, а затем выполняет его.",
        "Чётко различаем терминал, shell операционной системы и Python REPL — три разные вещи "
        "под похожими именами.",
        "Знаем основные командные оболочки (Bash, Zsh, PowerShell, cmd.exe, Fish) и "
        "познакомились с PySH — Python-first альтернативой на реальном локальном примере.",
        "Уверенно пользуемся Python REPL: R-E-P-L, приглашения >>> и ..., "
        "type()/help()/dir() как инструменты исследования.",
        "Различаем script, REPL, notebook и IDE — и знаем, для чего каждый из них лучше "
        "подходит.",
        "Подробно освоили print() (несколько значений, sep, end) и input() (первый диалог, "
        "текст как результат).",
        "Понимаем имена как указатели на значения, а не как «коробки с данными».",
        "Умеем писать понятные комментарии и выбирать читаемые имена файлов и переменных.",
        "Спокойно читаем SyntaxError, NameError и IndentationError, понимаем анатомию "
        "traceback и прошли пять лабораторий отладки.",
        "Знаем, как поставить точку останова и использовать отладчик в VS Code и PyCharm.",
        "Понимаем разницу между notebook и kernel — и как устроена браузерная практика этого "
        "курса на Pyodide.",
        "Собрали первый настоящий мини-проект — интерактивную визитную карточку.",
    ])}

{callout(
        "tip",
        "[[icon:launch]] Что дальше",
        "В главе 4 мы вплотную займёмся числами — их видами, преобразованием и математикой на "
        "Python.",
    )}"""

    out = render_page(
        page_title="Мини-проект и итоги главы",
        description="Первый мини-проект главы 3 — визитная карточка в терминале — и полное "
        "резюме пройденного материала.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 3", "index.html"), ("Мини-проект и итоги", "")],
        kicker="Глава 3 · Ваша первая программа на Python",
        h1="Мини-проект и итоги главы",
        lede="Собираем всё пройденное в один небольшой, но настоящий проект — и подводим итоги "
        "главы.",
        body_html=body,
        sidebar_groups=sidebar("03-17-mini-proekt-i-itogi.html"),
        nav=PageNav(prev_href="03-16-notebook-i-kernel.html", prev_label="Notebook и kernel", next_href="../glava-04/index.html", next_label="Глава 4: Python любит числа"),
    )
    write("03-17-mini-proekt-i-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01_create_and_run()
    build_06_terminal_shell_repl()
    build_07_shell_family()
    build_08_pysh()
    build_02_repl()
    build_09_repl_tool()
    build_03_print()
    build_10_input()
    build_11_names()
    build_12_comments_style()
    build_04_idle()
    build_05_checkpoint()
    build_13_errors_traceback()
    build_14_debug_labs()
    build_15_debugger()
    build_16_notebook_kernel()
    build_17_mini_project()
    print(f"Готово: {len(PAGES)} страниц Главы 3")
