#!/usr/bin/env python3
"""Строит Главу 15: «Python и файлы» (site/chapters/glava-15/).

Curriculum v2: файлы, пути, файловая система, текстовые кодировки,
персистентность и структурированные данные (JSON/CSV). Путь: ПАМЯТЬ
ПРОГРАММЫ → ПЕРСИСТЕНТНОСТЬ → ФАЙЛОВАЯ СИСТЕМА → ПУТИ → CWD → pathlib.Path →
ОБЪЕКТ ФАЙЛА → РЕЖИМ ОТКРЫТИЯ → with → ЧТЕНИЕ/ЗАПИСЬ → КУРСОР → TEXT vs BYTES
→ ENCODING/UTF-8 → ПАПКИ → ОШИБКИ → JSON → CSV → БЕЗОПАСНАЯ ПЕРСИСТЕНТНОСТЬ →
РЕАЛЬНЫЕ ПРОЕКТЫ. Отправная точка — не open("file.txt"), а вопрос «куда
пропадают переменные, когда программа завершается».

Существующие маршруты и практики (15-01..15-04, включая дневник заметок)
сохранены на месте и расширены по тому же шаблону, что и в главах 12-14;
новый материал — новые страницы и новые ID практик (15-05..15-30), без
переиспользования занятых ID. Итоги главы переехали на новую страницу 15-31
(как «итоги» переехали из 14-04 в 14-27) — 15-04 остаётся дневником заметок.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_lib import (
    ChapterSectionLink,
    NavItem,
    PageNav,
    SidebarGroup,
    callout,
    capability_map,
    class_diagram,
    classic_vs_modern,
    code_block,
    comparison_table,
    decision_map,
    exercise,
    file_cursor_diagram,
    file_state_diagram,
    local_required_card,
    object_diagram,
    path_anatomy_diagram,
    pipeline_diagram,
    practice_card,
    relationship_diagram,
    render_chapter_opener,
    render_page,
    summary_box,
    tree_diagram,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-15"

PAGES = [
    ("index.html", "Обзор главы"),
    ("15-01-zachem-fajly.html", "Зачем нужны файлы? Открытие и чтение"),
    ("15-02-stroka-za-strokoj.html", "Строка за строкой"),
    ("15-03-sozdanie-fajlov.html", "Создание новых файлов"),
    ("15-04-mini-proekt-itogi.html", "Мини-проект: дневник заметок"),
    ("15-05-fajl-i-papka.html", "Файл, папка и файловая система"),
    ("15-06-puti-absolyutnye-i-otnositelnye.html", "Пути: абсолютные и относительные"),
    ("15-07-tekushaya-rabochaya-directoriya.html", "Текущая рабочая директория (CWD)"),
    ("15-08-pochemu-pathlib.html", "pathlib.Path: пути как объекты"),
    ("15-09-razbiraem-put.html", "Разбираем путь: name, stem, suffix, parent"),
    ("15-10-praktika-puti-i-cwd.html", "Практика: пути и CWD"),
    ("15-11-file-object.html", "open() возвращает объект файла"),
    ("15-12-zhiznenny-cikl-i-with.html", "Жизненный цикл файла и with"),
    ("15-13-kursor-fajla.html", "Курсор файла: tell() и seek()"),
    ("15-14-chitaem-fajly.html", "Читаем файлы: read(), readline(), readlines()"),
    ("15-15-pishem-i-rezhimy.html", "Пишем в файлы: write() и режимы r/w/a/x"),
    ("15-16-text-bytes-encoding.html", "Текст, bytes и кодировка UTF-8"),
    ("15-17-binarnye-fajly-i-perevody-strok.html", "Бинарные файлы и переносы строк"),
    ("15-18-pathlib-udobnye-metody.html", "pathlib: read_text, write_text, read_bytes, write_bytes"),
    ("15-19-papki-exists-mkdir.html", "Папки: exists(), is_file(), mkdir()"),
    ("15-20-poisk-fajlov-glob.html", "Поиск файлов: iterdir() и glob()"),
    ("15-21-pereimenovanie-kopirovanie-udalenie.html", "Переименование, копирование, удаление"),
    ("15-22-oshibki-fajlovoj-sistemy.html", "Ошибки файловой системы"),
    ("15-23-bolshie-fajly-i-potoki.html", "Большие файлы и потоковая обработка"),
    ("15-24-kak-vybrat-format.html", "Как выбрать формат хранения данных"),
    ("15-25-json-serializatsiya.html", "JSON: сохраняем структуры данных"),
    ("15-26-mini-proekt-save-player.html", "Мини-проект: сохраняем Player"),
    ("15-27-csv-tablitsy.html", "CSV: таблицы в текстовом виде"),
    ("15-28-bezopasnaya-rabota-s-fajlami.html", "Безопасная работа с файлами"),
    ("15-29-mini-proekt-rekordy-i-nastrojki.html", "Мини-проект: таблица рекордов"),
    ("15-30-brauzer-vs-lokalny-disk.html", "Браузер и локальный диск: две файловые системы"),
    ("15-31-itogi-glavy.html", "Итоги главы: инструментарий работы с файлами"),
]

PRACTICE_IDS = [
    "15-01", "15-02", "15-03", "15-04", "15-05", "15-06", "15-07", "15-08",
    "15-09", "15-10", "15-11", "15-12", "15-13", "15-14", "15-15", "15-16",
    "15-17", "15-18", "15-19", "15-20", "15-21", "15-22", "15-23", "15-24",
    "15-25", "15-26", "15-27", "15-28", "15-29", "15-30",
]

LOCAL_REQUIRED_IDS = {"15-07", "15-30"}


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 15 · Файлы", items),
        SidebarGroup("Практика", [
            NavItem(f"[[icon:practice]] {lid}: Практика", f"../../practice/{lid}/index.html") for lid in PRACTICE_IDS
        ]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    clean = "\n".join(line.rstrip() for line in html_out.split("\n"))
    path.write_text(clean, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def terminal_transcript(lines: list[str], *, caption: str = "") -> str:
    body = "\n".join(lines)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{caption}</figcaption>' if caption else ""
    return f"""
    <figure style="margin:24px 0">
      <pre style="background:#0D0230;color:#E7DEFF;border-radius:var(--radius-lg,20px);
        padding:18px 22px;overflow-x:auto;font-family:'JetBrains Mono',monospace;font-size:14px;
        line-height:1.7"><code>{body}</code></pre>
      {cap}
    </figure>"""


def debug_lab(n: int, title: str, broken_code_filename: str, broken_code: str, symptom_lines: list[str], explanation_html: str, fixed_code_filename: str, fixed_code: str) -> str:
    """Единый компонент Debug Lab (введён в главе 14): сломанный код → что
    происходит на экране → объяснение → исправленный код. Используется во
    всех 14 обязательных debug-лабораториях этой главы."""
    return f"""
    <div style="margin:28px 0;padding:4px 4px 20px;border:2px dashed #DB2777;border-radius:var(--radius-lg,20px)">
      <div style="display:flex;align-items:center;gap:12px;padding:16px 20px 6px">
        <div class="cs-icon-emblem cs-icon-emblem--debug">[[icon:debug]]</div>
        <div style="font-family:Sora,sans-serif;font-weight:700;font-size:13px;
        letter-spacing:.05em;text-transform:uppercase;color:#DB2777">Debug Lab {n}: {title}</div>
      </div>
      <div style="padding:0 20px">
{code_block(broken_code_filename, broken_code)}
{terminal_transcript(symptom_lines, caption="Что видно на экране")}
        <p>{explanation_html}</p>
        <div style="font-family:Sora,sans-serif;font-weight:700;font-size:12px;letter-spacing:.05em;
          text-transform:uppercase;color:#059669;margin:16px 0 8px">Исправленный код</div>
{code_block(fixed_code_filename, fixed_code)}
      </div>
    </div>"""


_HREFS = [h for h, _ in PAGES]
_TITLES = dict(PAGES)


def nav_for(current_href: str) -> PageNav:
    i = _HREFS.index(current_href)
    prev_href, prev_label = (_HREFS[i - 1], _TITLES[_HREFS[i - 1]]) if i > 0 else (None, None)
    if i < len(_HREFS) - 1:
        next_href, next_label = _HREFS[i + 1], _TITLES[_HREFS[i + 1]]
    else:
        next_href, next_label = "../glava-16/index.html", "Глава 16: Создаём классные приложения с Tkinter"
    return PageNav(prev_href=prev_href, prev_label=prev_label, next_href=next_href, next_label=next_label)


def page(href: str, *, page_title: str, description: str, kicker_suffix: str, h1: str, lede: str, body_html: str) -> None:
    out = render_page(
        page_title=page_title,
        description=description,
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 15", "index.html"), (kicker_suffix, "")],
        kicker="Глава 15 · Python и файлы",
        h1=h1,
        lede=lede,
        body_html=body_html,
        sidebar_groups=sidebar(href),
        nav=nav_for(href),
    )
    write(href, out)


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=15,
        baseline_page=323,
        title="Python и файлы",
        description="Путь данных от объекта Python до файла на диске — и обратно. Файловая "
        "система, переносимые пути через pathlib, безопасное чтение и запись текста и байтов в "
        "UTF-8, JSON и CSV — и как сохранить состояние программы между запусками, а не только на "
        "время одного сеанса.",
        meta_items=["[[icon:timer]] ~9 часов", "[[icon:folder]] pathlib, JSON, CSV", "[[icon:practice]] 30 практик"],
        sections=[
            ChapterSectionLink("15.1", "Зачем нужны файлы? Открытие и чтение", "15-01-zachem-fajly.html", "323"),
            ChapterSectionLink("15.2", "Строка за строкой", "15-02-stroka-za-strokoj.html", "326"),
            ChapterSectionLink("15.3", "Создание новых файлов", "15-03-sozdanie-fajlov.html", "328"),
            ChapterSectionLink("15.4", "Мини-проект: дневник заметок", "15-04-mini-proekt-itogi.html", "330"),
            ChapterSectionLink("15.5", "Файл, папка и файловая система", "15-05-fajl-i-papka.html", "332"),
            ChapterSectionLink("15.6", "Пути: абсолютные и относительные", "15-06-puti-absolyutnye-i-otnositelnye.html", "334"),
            ChapterSectionLink("15.7", "Текущая рабочая директория (CWD)", "15-07-tekushaya-rabochaya-directoriya.html", "336"),
            ChapterSectionLink("15.8", "pathlib.Path: пути как объекты", "15-08-pochemu-pathlib.html", "339"),
            ChapterSectionLink("15.9", "Разбираем путь: name, stem, suffix, parent", "15-09-razbiraem-put.html", "341"),
            ChapterSectionLink("15.10", "Практика: пути и CWD", "15-10-praktika-puti-i-cwd.html", "343"),
            ChapterSectionLink("15.11", "open() возвращает объект файла", "15-11-file-object.html", "345"),
            ChapterSectionLink("15.12", "Жизненный цикл файла и with", "15-12-zhiznenny-cikl-i-with.html", "347"),
            ChapterSectionLink("15.13", "Курсор файла: tell() и seek()", "15-13-kursor-fajla.html", "349"),
            ChapterSectionLink("15.14", "Читаем файлы: read(), readline(), readlines()", "15-14-chitaem-fajly.html", "351"),
            ChapterSectionLink("15.15", "Пишем в файлы: write() и режимы r/w/a/x", "15-15-pishem-i-rezhimy.html", "354"),
            ChapterSectionLink("15.16", "Текст, bytes и кодировка UTF-8", "15-16-text-bytes-encoding.html", "357"),
            ChapterSectionLink("15.17", "Бинарные файлы и переносы строк", "15-17-binarnye-fajly-i-perevody-strok.html", "360"),
            ChapterSectionLink("15.18", "pathlib: read_text/write_text/read_bytes/write_bytes", "15-18-pathlib-udobnye-metody.html", "362"),
            ChapterSectionLink("15.19", "Папки: exists(), is_file(), mkdir()", "15-19-papki-exists-mkdir.html", "364"),
            ChapterSectionLink("15.20", "Поиск файлов: iterdir() и glob()", "15-20-poisk-fajlov-glob.html", "366"),
            ChapterSectionLink("15.21", "Переименование, копирование, удаление", "15-21-pereimenovanie-kopirovanie-udalenie.html", "368"),
            ChapterSectionLink("15.22", "Ошибки файловой системы", "15-22-oshibki-fajlovoj-sistemy.html", "370"),
            ChapterSectionLink("15.23", "Большие файлы и потоковая обработка", "15-23-bolshie-fajly-i-potoki.html", "373"),
            ChapterSectionLink("15.24", "Как выбрать формат хранения данных", "15-24-kak-vybrat-format.html", "375"),
            ChapterSectionLink("15.25", "JSON: сохраняем структуры данных", "15-25-json-serializatsiya.html", "377"),
            ChapterSectionLink("15.26", "Мини-проект: сохраняем Player", "15-26-mini-proekt-save-player.html", "380"),
            ChapterSectionLink("15.27", "CSV: таблицы в текстовом виде", "15-27-csv-tablitsy.html", "382"),
            ChapterSectionLink("15.28", "Безопасная работа с файлами", "15-28-bezopasnaya-rabota-s-fajlami.html", "385"),
            ChapterSectionLink("15.29", "Мини-проект: таблица рекордов", "15-29-mini-proekt-rekordy-i-nastrojki.html", "387"),
            ChapterSectionLink("15.30", "Браузер и локальный диск", "15-30-brauzer-vs-lokalny-disk.html", "389"),
            ChapterSectionLink("15.31", "Итоги главы: инструментарий работы с файлами", "15-31-itogi-glavy.html", "391"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <h2>Куда пропадают переменные?</h2>
    <p>Небольшая программа:</p>
    {code_block(
        "schet_igry.py",
        'score = 1200\n'
        'player = "Anna"\n\n'
        "print(score)\n",
    )}
    <p>Программа заканчивается. Где теперь <code class="inline">score</code> и
    <code class="inline">player</code>? Запустите программу ещё раз — она снова начнёт со
    значения <code class="inline">score = 1200</code>, как будто предыдущего запуска не было.</p>
    {callout(
        "info",
        "Точная формулировка",
        "Не «всё в памяти мгновенно стирается» — а точнее: <strong>следующий запуск программы "
        "не наследует автоматически объекты Python из предыдущего процесса</strong>. Пока "
        "программа выполняется, её объекты живут в памяти запущенного процесса; когда процесс "
        "завершается, эта память освобождается операционной системой.",
    )}
    {pipeline_diagram([
        {"kind": "memory", "title": "RAM · память процесса", "rows": ["score = 1200", 'player = "Anna"']},
        {"kind": "file", "title": "файловая система", "rows": ["без сохранения — ничего"], "note": "программа завершается"},
    ], caption="Без сохранения в файл состояние программы не переживает её завершение.")}
    <p>Чтобы данные <strong>пережили завершение программы</strong> — список результатов игры,
    текст, настройки — их нужно записать в <strong>файл</strong> на диске (или другом
    постоянном хранилище) и прочитать обратно при следующем запуске.</p>

    <h2>Что такое файл?</h2>
    <p>Файл — это <strong>именованный набор данных</strong>, который хранится в файловой системе.</p>
    <p>Чтобы программа могла открыть нужный файл, ей нужно указать, где этот файл находится. Для
    этого используется <strong>путь к файлу</strong> — запись, которая показывает его
    расположение среди папок и файлов. Например:</p>
    {code_block("primer_puti.py", "# data/results.txt\n", lang="text")}
    <p>Здесь <code class="inline">data</code> — это папка, а <code class="inline">results.txt</code>
    — файл внутри неё.</p>
    {callout(
        "tip",
        "Путь — это адрес файла",
        "Для первого знакомства путь можно представить как адрес файла в файловой системе — так "
        "же, как адрес дома помогает найти его среди улиц и номеров. Это лишь сравнение для "
        "интуиции: путь — это текстовая запись, а не физический адрес в памяти компьютера. "
        "Абсолютные и относительные пути подробно разберём в разделе 15.6.",
    )}
    <p>В конечном счёте содержимое файла представлено байтами. Если файл содержит текст, Python
    должен знать, как преобразовать эти байты в символы и обратно. Правило такого преобразования
    называется <strong>кодировкой</strong> — подробно поговорим об этом в разделе 15.16, вместе
    с различием <code class="inline">str</code> и <code class="inline">bytes</code>.</p>

    <h2 id="otkrytie">Открытие и чтение существующих файлов</h2>
    {code_block(
        "chtenie_fajla.py",
        'file = open("privet.txt", "r", encoding="utf-8")   # "r" — режим чтения (read)\n'
        "content = file.read()\n"
        "print(content)\n"
        "file.close()   # обязательно закрыть файл после работы\n",
    )}

    {callout(
        "warning",
        "Не забывайте file.close()",
        "Незакрытый файл может не сохранить изменения на диск или заблокировать доступ к нему "
        "для других программ. Забыть <code class=\"inline\">close()</code> — очень частая "
        "ошибка новичков.",
    )}

    <h2>Современный способ: <code class="inline">with</code></h2>
    {classic_vs_modern(
        "Ручное закрытие → менеджер контекста with",
        "Классический подход",
        'file = open("privet.txt", "r", encoding="utf-8")\n'
        "content = file.read()\n"
        "print(content)\n"
        "file.close()   # легко забыть!",
        "Современный Python (with)",
        'with open("privet.txt", "r", encoding="utf-8") as file:\n'
        "    content = file.read()\n"
        "    print(content)\n"
        "# файл закроется САМ, даже если внутри блока произойдёт ошибка",
        "<code class=\"inline\">with</code> — он существует в Python с версии 2.5, так что "
        "дело не в новизне, а в надёжности: файл закроется автоматически при выходе из блока "
        "<code class=\"inline\">with</code>, даже если внутри что-то пойдёт не так. Начиная с "
        "этой главы в книге мы используем именно <code class=\"inline\">with</code> и всегда "
        "указываем <code class=\"inline\">encoding=\"utf-8\"</code> явно (подробнее — в 15.16).",
    )}

    {practice_card(
        "15-01",
        "Практика: чтение файлов через with",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-01/index.html",
    )}
    """
    page(
        "15-01-zachem-fajly.html",
        page_title="Зачем нужны файлы? Открытие и чтение",
        description="Почему переменные не переживают завершение программы, что такое файл на самом деле, и как открыть и прочитать файл через with.",
        kicker_suffix="Зачем файлы?",
        h1="Зачем нужны файлы?",
        lede="Переменные исчезают вместе с программой — файлы позволяют сохранить данные надолго.",
        body_html=body,
    )


def build_02() -> None:
    body = f"""
    <p>Читать весь файл сразу одним куском не всегда удобно — особенно если файл большой.
    Часто нужнее обработать его <strong>построчно</strong>:</p>
    {code_block(
        "stroka_za_strokoj.py",
        'with open("spisok.txt", "r", encoding="utf-8") as file:\n'
        "    for line in file:\n"
        "        print(line.strip())\n",
    )}
    {callout(
        "tip",
        "Что именно убирает strip()",
        "Каждая строка файла, кроме, возможно, последней, заканчивается невидимым символом "
        "перевода строки <code class=\"inline\">\\n</code>. Но <code class=\"inline\">.strip()</code> "
        "(глава 8) убирает <strong>все</strong> пробельные символы по обеим сторонам строки — "
        "пробелы, табуляции и переносы строк, — а не только этот один перевод строки. Если данные "
        "в файле могут осмысленно начинаться или заканчиваться пробелом, слепой "
        "<code class=\"inline\">.strip()</code> может незаметно испортить их. Если цель — убрать "
        "именно завершающий перевод строки и ничего больше, используйте "
        "<code class=\"inline\">line.rstrip(\"\\\\n\")</code>.",
    )}

    {debug_lab(
        1,
        "strip() убирает больше, чем кажется",
        "citaty.py",
        'with open("citaty.txt", "w", encoding="utf-8") as file:\n'
        '    file.write("  важная цитата с пробелами по краям  \\n")\n\n'
        'with open("citaty.txt", "r", encoding="utf-8") as file:\n'
        "    for line in file:\n"
        '        print(f"[{line.strip()}]")\n',
        ['[важная цитата с пробелами по краям]'],
        "Программа вывела цитату без ведущих и завершающих пробелов — хотя автор специально их "
        "поставил. <code class=\"inline\">.strip()</code> убирает пробелы по краям вместе с "
        "переводом строки, и не различает «случайный мусор» и «намеренный пробел»: она просто "
        "убирает всё пробельное по обоим концам строки.",
        "citaty_fixed.py",
        'with open("citaty.txt", "r", encoding="utf-8") as file:\n'
        "    for line in file:\n"
        '        print(f"[{line.rstrip(chr(10))}]")   # убираем только перевод строки\n',
    )}

    <h2>Все строки сразу — списком</h2>
    {code_block(
        "readlines.py",
        'with open("spisok.txt", "r", encoding="utf-8") as file:\n'
        "    lines = file.readlines()\n\n"
        'print(len(lines), "строк")\n'
        "print(lines[0])   # первая строка — вместе со своим \\n\n",
    )}
    {callout(
        "info",
        "Символы переноса строки — не только \\n",
        "В Python текстовые файлы читаются в режиме универсальных переносов строк: даже если на "
        "диске строки разделены последовательностью <code class=\"inline\">\\r\\n</code> (так "
        "исторически принято в Windows), при чтении в текстовом режиме Python отдаёт вам "
        "<code class=\"inline\">\\n</code>. Подробно про текстовый и бинарный режимы — в 15.17.",
    )}

    {practice_card(
        "15-02",
        "Практика: построчное чтение файлов",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-02/index.html",
    )}
    """
    page(
        "15-02-stroka-za-strokoj.html",
        page_title="Строка за строкой",
        description="Построчное чтение файлов в Python: цикл по файлу, readlines() и что на самом деле делает strip().",
        kicker_suffix="Строка за строкой",
        h1="Строка за строкой",
        lede="Часто удобнее обработать файл по одной строке за раз, а не целиком.",
        body_html=body,
    )


def build_03() -> None:
    body = f"""
    <h2>Создание новых файлов</h2>
    <p>Чтобы записать что-то в файл, откройте его в режиме записи
    <code class="inline">"w"</code> (write) — если файла не существует, Python создаст его сам;
    если существует — его прежнее содержимое стирается <strong>уже в момент открытия</strong>,
    ещё до первого <code class="inline">write()</code>:</p>
    {code_block(
        "zapis_fajla.py",
        'with open("rezultaty.txt", "w", encoding="utf-8") as file:\n'
        '    file.write("Уровень 1: 100 очков\\n")\n'
        '    file.write("Уровень 2: 250 очков\\n")\n',
    )}
    {file_state_diagram(
        "До", ["Уровень 1: 50 очков (старая игра)"],
        "После открытия \"w\"", [],
        action_label='open(..., "w")',
        caption="Режим \"w\" стирает старое содержимое сразу при открытии файла — до первой записи.",
    )}

    <h2 id="rabota">Работа с файлами</h2>
    <p>Три основных режима открытия файла:</p>
    <ul>
      <li><code class="inline">"r"</code> — чтение (read); ошибка, если файла не существует.</li>
      <li><code class="inline">"w"</code> — запись (write); создаёт новый файл или полностью
        стирает существующий сразу при открытии.</li>
      <li><code class="inline">"a"</code> — дозапись (append); добавляет текст в конец файла, не
        стирая то, что уже есть.</li>
    </ul>
    {code_block("dozapis.py", 'with open("rezultaty.txt", "a", encoding="utf-8") as file:\n    file.write("Уровень 3: 400 очков\\n")\n')}
    {callout(
        "warning",
        "\"a\" — это не «вставить куда захочу»",
        "Дозапись всегда добавляет текст в конец файла. Она не умеет вставлять текст в середину "
        "или начало существующего содержимого.",
    )}

    <h2>Пути к файлам: строка или pathlib</h2>
    {classic_vs_modern(
        "Путь к файлу: обычная строка → pathlib",
        "Классический подход",
        'file_path = "data/rezultaty.txt"\n'
        "with open(file_path, \"r\", encoding=\"utf-8\") as f:\n"
        "    print(f.read())",
        "Современный Python (pathlib)",
        "from pathlib import Path\n\n"
        'file_path = Path("data") / "rezultaty.txt"\n'
        "print(file_path.exists())   # удобные методы прямо у пути\n"
        "with file_path.open(\"r\", encoding=\"utf-8\") as f:\n"
        "    print(f.read())",
        "<code class=\"inline\">pathlib</code> для путей к файлам — он появился в Python 3.4 и "
        "с тех пор считается предпочтительным способом. Строковые пути всё ещё повсеместно "
        "работают и встречаются в старом коде, но <code class=\"inline\">pathlib</code> "
        "избавляет от ручной сборки пути через <code class=\"inline\">+</code> и добавляет "
        "полезные методы вроде <code class=\"inline\">.exists()</code> прямо у самого пути. "
        "Подробно разберём его в разделе 15.8.",
    )}

    {practice_card(
        "15-03",
        "Практика: запись, дозапись и pathlib",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-03/index.html",
    )}
    """
    page(
        "15-03-sozdanie-fajlov.html",
        page_title="Создание новых файлов",
        description="Режимы работы с файлами (r, w, a), опасность режима w и первое знакомство с pathlib.",
        kicker_suffix="Создание файлов",
        h1="Создание новых файлов",
        lede="Записываем данные на диск — и знакомимся с современным способом работать с путями.",
        body_html=body,
    )


def build_04() -> None:
    body = f"""
    <p>Соберём чтение и запись в одном небольшом проекте — дневнике заметок, который
    сохраняется между запусками программы.</p>
    {code_block(
        "dnevnik_zametok.py",
        "from pathlib import Path\n\n"
        'fajl_zametok = Path("zametki.txt")\n\n'
        'novaya_zametka = input("Новая заметка: ")\n\n'
        'with fajl_zametok.open("a", encoding="utf-8") as f:\n'
        '    f.write(novaya_zametka + "\\n")\n\n'
        'print("Все заметки:")\n'
        'with fajl_zametok.open("r", encoding="utf-8") as f:\n'
        "    for line in f:\n"
        "        print(\"-\", line.strip())\n",
    )}
    {callout(
        "info",
        "Почему дозапись, а не перезапись",
        "Режим <code class=\"inline\">\"a\"</code> добавляет заметку, не стирая предыдущие — "
        "именно так и должен вести себя настоящий дневник: каждый запуск программы добавляет "
        "новую запись, а не начинает всё заново.",
    )}
    {exercise(2, "Нумерация заметок", "Добавьте номер к каждой заметке при чтении — например, «1. Первая заметка», «2. Вторая заметка».")}
    {practice_card(
        "15-04",
        "Практика: дневник заметок",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-04/index.html",
    )}
    """
    page(
        "15-04-mini-proekt-itogi.html",
        page_title="Мини-проект: дневник заметок",
        description="Мини-проект главы 15: дневник заметок, сохраняющийся между запусками программы.",
        kicker_suffix="Дневник заметок",
        h1="Мини-проект: дневник заметок",
        lede="Дневник заметок, сохраняющийся между запусками программы — первая настоящая персистентность.",
        body_html=body,
    )


def build_05() -> None:
    body = f"""
    <h2>Файл и папка</h2>
    <p>Файловая система различает два основных вида элементов:</p>
    <ul>
      <li><strong>Файл</strong> — хранит данные (текст, код, картинку, что угодно).</li>
      <li><strong>Папка</strong> (директория) — не хранит данные сама, а организует другие файлы
        и папки, вложенные в неё.</li>
    </ul>
    <p><strong>Путь</strong> говорит, где именно в этой организации находится конкретный
    элемент — подробно про пути поговорим в следующем разделе.</p>

    {tree_diagram(
        ("[[icon:folder]] project/", [
            ("[[icon:file]] main.py", []),
            ("[[icon:file]] README.md", []),
            ("[[icon:folder]] data/", [
                ("[[icon:file]] players.json", []),
                ("[[icon:file]] scores.csv", []),
                ("[[icon:file]] notes.txt", []),
            ]),
            ("[[icon:folder]] assets/", [
                ("[[icon:file]] logo.png", []),
            ]),
        ]),
        caption="Файлы и папки образуют иерархию — файловое дерево.",
    )}

    <h2>Файловая система — иерархия от корня</h2>
    <p>На Linux/macOS всё дерево файлов растёт из одного корня — <code class="inline">/</code>:</p>
    {tree_diagram(
        ("/", [
            ("home", [
                ("astra", [
                    ("Projects", [
                        ("Python_001", []),
                    ]),
                ]),
            ]),
        ]),
        caption="POSIX: единый корень / — путь к этому проекту.",
    )}
    <p>На Windows у каждого диска свой корень, например <code class="inline">C:\\</code>:</p>
    {tree_diagram(
        ("C:\\\\", [
            ("Users", [
                ("Anna", [
                    ("project", []),
                ]),
            ]),
        ]),
        caption="Windows: диск как корень (например, C:\\).",
    )}
    {callout(
        "info",
        "POSIX и Windows — не соперники",
        "Не нужно спорить, какой вариант «правильный» — они устроены по-разному, и реальным "
        "кодом с обоими вариантами вам поможет работать не запоминание конкретных разделителей, "
        "а <code class=\"inline\">pathlib</code> (раздел 15.8), который сам собирает переносимый "
        "путь для той системы, где выполняется программа.",
    )}

    {practice_card(
        "15-05",
        "Практика: файлы, папки и дерево путей",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-05/index.html",
    )}
    """
    page(
        "15-05-fajl-i-papka.html",
        page_title="Файл, папка и файловая система",
        description="Различие между файлом и папкой, и файловая система как иерархическое дерево — от корня до конкретного файла.",
        kicker_suffix="Файл и папка",
        h1="Файл, папка и файловая система",
        lede="Файлы хранят данные, папки организуют файловую систему в дерево.",
        body_html=body,
    )


def build_06() -> None:
    body = f"""
    <h2>Анатомия пути</h2>
    <p>Путь — это адрес элемента файловой системы, записанный как последовательность имён папок,
    разделённых слешем, и (для файла) имени файла в конце:</p>
    {path_anatomy_diagram(
        "/home/anna/project/data/scores.txt",
        [("родительская папка", "/home/anna/project/data"), ("имя файла", "scores.txt")],
        caption="Путь состоит из цепочки папок и имени файла — подробный разбор имени файла в 15.9.",
    )}

    <h2>Абсолютный путь</h2>
    <p>Абсолютный путь называет местоположение файла, начиная от <strong>корня</strong>
    файловой системы (или буквы диска на Windows) — он однозначен независимо от того, откуда
    его читают:</p>
    {code_block(
        "absolyutnye_puti.py",
        "# POSIX (Linux/macOS)\n"
        "# /home/anna/project/data.txt\n\n"
        "# Windows\n"
        "# C:\\\\Users\\\\Anna\\\\project\\\\data.txt\n",
        lang="text",
    )}
    {callout(
        "warning",
        "Не зашивайте абсолютные пути в реальный код",
        "Такие пути показаны здесь только как иллюстрация устройства пути. В настоящем коде "
        "курса (и в ваших будущих программах) абсолютный путь конкретного компьютера почти "
        "никогда не подходит — он не будет существовать на другом компьютере.",
    )}

    <h2>Относительный путь — относительно чего?</h2>
    <p>Путь вида:</p>
    {code_block("otnositelny_put.py", '# data/scores.txt\n', lang="text")}
    <p>не называет место в файловой системе однозначно, пока не ответить на главный вопрос:
    <strong>относительно чего?</strong> Ответ — раздел 15.7: относительный путь разрешается
    относительно <strong>текущей рабочей директории</strong> программы, если API или документация
    не говорят иного.</p>

    {practice_card(
        "15-06",
        "Практика: абсолютные и относительные пути",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-06/index.html",
    )}
    """
    page(
        "15-06-puti-absolyutnye-i-otnositelnye.html",
        page_title="Пути: абсолютные и относительные",
        description="Из чего состоит путь к файлу, чем абсолютный путь отличается от относительного и почему относительный путь нельзя понять без ответа на вопрос «относительно чего».",
        kicker_suffix="Абсолютные и относительные пути",
        h1="Пути: абсолютные и относительные",
        lede="Абсолютный путь однозначен всегда. Относительный — только относительно чего-то.",
        body_html=body,
    )


def build_07() -> None:
    body = f"""
    <h2>Текущая рабочая директория (CWD)</h2>
    <p>Узнать текущую рабочую директорию программы:</p>
    {code_block("cwd.py", "from pathlib import Path\n\nprint(Path.cwd())\n")}
    <p><strong>Текущая рабочая директория (CWD)</strong> — это папка, относительно которой
    интерпретируются обычные относительные пути в программе.</p>
    {callout(
        "warning",
        "CWD — это НЕ «папка со скриптом»",
        "Это одна из самых частых ошибок с путями в реальном коде. CWD и папка, где лежит файл "
        "<code class=\"inline\">.py</code>, могут совпадать — а могут и не совпадать. CWD "
        "определяется тем, <strong>откуда была запущена программа</strong>, а не тем, где физически "
        "лежит её исходный файл.",
    )}

    {tree_diagram(
        ("[[icon:folder]] project/  ← CWD (запуск python src/app.py отсюда)", [
            ("[[icon:folder]] src/", [
                ("[[icon:file]] app.py", []),
            ]),
            ("[[icon:folder]] data/", [
                ("[[icon:file]] config.json", []),
            ]),
        ]),
        caption="Скрипт лежит в src/app.py, но CWD — это project/, если запустить программу отсюда.",
    )}
    {code_block(
        "app_py_fragment.py",
        '# внутри src/app.py, если программа запущена из project/:\n'
        'from pathlib import Path\n\n'
        'путь = Path("data/config.json")\n'
        '# указывает на project/data/config.json — НЕ на project/src/data/config.json\n',
    )}

    {debug_lab(
        2,
        "CWD — это не папка со скриптом",
        "app_wrong.py",
        '# файл лежит в project/src/app.py\n'
        'from pathlib import Path\n\n'
        'config = Path("config.json")   # предполагаем: "рядом со скриптом"\n'
        'print(config.read_text(encoding="utf-8"))\n',
        [
            "$ cd project",
            "$ python src/app.py",
            "Traceback (most recent call last):",
            "FileNotFoundError: [Errno 2] No such file or directory: 'config.json'",
        ],
        "Файл <code class=\"inline\">config.json</code> лежит в <code class=\"inline\">project/src/</code>, "
        "рядом со скриптом. Но программа запущена из <code class=\"inline\">project/</code> — значит, CWD "
        "равен <code class=\"inline\">project/</code>, и относительный путь <code class=\"inline\">"
        "\"config.json\"</code> ищется в <code class=\"inline\">project/config.json</code>, которого нет.",
        "app_fixed.py",
        '# надёжный способ — путь относительно самого файла, а не относительно CWD\n'
        'from pathlib import Path\n\n'
        'BASE_DIR = Path(__file__).resolve().parent\n'
        'config = BASE_DIR / "config.json"\n'
        'print(config.read_text(encoding="utf-8"))\n',
    )}

    <h2>Папка скрипта: <code class="inline">__file__</code></h2>
    <p>Для обычных <code class="inline">.py</code>-файлов узнать папку, где лежит сам исходный
    файл, можно так:</p>
    {code_block("script_dir.py", "from pathlib import Path\n\nBASE_DIR = Path(__file__).resolve().parent\n")}
    {callout(
        "warning",
        "__file__ не гарантирован всегда",
        "<code class=\"inline\">__file__</code> обычно определён в обычных скриптах и модулях, "
        "но интерактивная оболочка Python и некоторые окружения ноутбуков могут не задавать эту "
        "переменную. Не считайте её универсально доступной в любом контексте выполнения кода.",
    )}

    {local_required_card(
        "15-07",
        "Практика: CWD и папка скрипта на вашем компьютере",
        "Локальная практика — запустите настоящий .py-файл из разных папок и понаблюдайте, что меняется",
        "../../practice/15-07/index.html",
    )}
    """
    page(
        "15-07-tekushaya-rabochaya-directoriya.html",
        page_title="Текущая рабочая директория (CWD)",
        description="Что такое текущая рабочая директория, почему это не папка со скриптом, и как надёжно находить файлы рядом с исходным кодом через __file__.",
        kicker_suffix="CWD",
        h1="Текущая рабочая директория — CWD",
        lede="Один из самых частых источников файловых ошибок: относительный путь ведёт не туда, куда вы думали.",
        body_html=body,
    )


def build_08() -> None:
    body = f"""
    <h2>Почему pathlib</h2>
    <p>Путь — это не просто строка, это <strong>предметная область со своими правилами</strong>:
    у него есть родитель, имя, расширение, он может существовать или не существовать. Вместо
    ручной сборки строки через <code class="inline">+</code>:</p>
    {classic_vs_modern(
        "Путь как строка → путь как объект",
        "Классический подход",
        'file_path = "data" + "/" + "players" + "/" + "anna.json"\n'
        "# на Windows придётся использовать \"\\\\\", легко ошибиться",
        "Современный Python (pathlib)",
        'from pathlib import Path\n\n'
        'file_path = Path("data") / "players" / "anna.json"\n'
        "# сам подставит правильный разделитель для текущей ОС",
        "<code class=\"inline\">pathlib</code> появился в Python 3.4 и с тех пор считается "
        "предпочтительным способом работы с путями: он избавляет от ручной сборки строк, ошибок "
        "с разделителями и добавляет удобные методы прямо у самого пути.",
    )}

    <h2>Путь — не содержимое файла</h2>
    {callout(
        "warning",
        "Path(...) не читает файл",
        "<code class=\"inline\">Path(\"notes.txt\")</code> создаёт объект-путь — ссылку на "
        "место в файловой системе. Он ничего не читает и не открывает сам по себе, пока вы не "
        "вызовете у него метод вроде <code class=\"inline\">.open()</code> или "
        "<code class=\"inline\">.read_text()</code>.",
    )}

    <h2>Path как объект: атрибуты и методы</h2>
    <p>Это прямая связь с главой 14: <code class="inline">Path</code> — обычный Python-объект со
    своими атрибутами и методами.</p>
    {class_diagram(
        "Path",
        ["name", "stem", "suffix", "parent", "parts"],
        ["exists()", "is_file()", "is_dir()", "open()", "read_text()", "write_text()"],
        caption="pathlib.Path — объект с методами, а не просто текст пути (полный разбор атрибутов — в 15.9).",
    )}

    <h2>Path.home()</h2>
    {code_block("path_home.py", "from pathlib import Path\n\nprint(Path.home())   # только для справки\n")}
    {callout(
        "info",
        "Не пишите практические файлы в домашнюю папку",
        "<code class=\"inline\">Path.home()</code> полезен для справки, но все практики этого "
        "курса записывают файлы только в собственную рабочую директорию — никогда напрямую в "
        "домашнюю папку пользователя.",
    )}

    {practice_card(
        "15-08",
        "Практика: собираем пути через pathlib",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-08/index.html",
    )}
    """
    page(
        "15-08-pochemu-pathlib.html",
        page_title="pathlib.Path: пути как объекты",
        description="Почему путь как объект удобнее пути как строки: сборка пути через /, связь с ООП главы 14, Path.home().",
        kicker_suffix="pathlib.Path",
        h1="pathlib.Path: пути как объекты",
        lede="Путь — не просто текст. Это объект со своими атрибутами и методами.",
        body_html=body,
    )


def build_09() -> None:
    body = f"""
    <h2>Разбираем путь на части</h2>
    {code_block(
        "razbor_puti.py",
        'from pathlib import Path\n\n'
        'path = Path("/home/anna/project/data/scores.txt")\n\n'
        "print(path.name)     # scores.txt\n"
        "print(path.stem)     # scores\n"
        "print(path.suffix)   # .txt\n"
        "print(path.parent)   # /home/anna/project/data\n",
    )}
    {path_anatomy_diagram(
        "/home/anna/project/data/scores.txt",
        [
            ("parent", "/home/anna/project/data"),
            ("name", "scores.txt"),
            ("stem", "scores"),
            ("suffix", ".txt"),
        ],
        caption="name = stem + suffix; parent — родительская папка.",
    )}

    <h2>Точка и две точки</h2>
    <ul>
      <li><code class="inline">.</code> — текущая папка.</li>
      <li><code class="inline">..</code> — родительская папка.</li>
    </ul>
    {code_block("dot_dotdot.py", 'from pathlib import Path\n\nprint(Path("."))\nprint(Path(".."))\n')}
    {callout(
        "tip",
        "Не увлекайтесь ../../../..",
        "Длинные цепочки <code class=\"inline\">..</code> сложно читать и легко сломать при "
        "переносе кода в другое место. Там, где это практично, предпочитайте явную базовую "
        "папку (как <code class=\"inline\">BASE_DIR</code> из раздела 15.7) вместо нескольких "
        "<code class=\"inline\">..</code> подряд.",
    )}

    <h2>Расширение — это соглашение, а не гарантия</h2>
    {callout(
        "warning",
        "Суффикс не гарантирует формат содержимого",
        "<code class=\"inline\">.txt</code>, <code class=\"inline\">.json</code>, "
        "<code class=\"inline\">.jpg</code> — это соглашения об имени файла, а не магическая "
        "проверка того, что внутри. Файл <code class=\"inline\">report.txt</code> технически "
        "может содержать что угодно. Не проверяйте формат содержимого только по расширению имени "
        "файла.",
    )}

    {practice_card(
        "15-09",
        "Практика: name, stem, suffix, parent",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-09/index.html",
    )}
    """
    page(
        "15-09-razbiraem-put.html",
        page_title="Разбираем путь: name, stem, suffix, parent",
        description="Атрибуты pathlib.Path — name, stem, suffix, parent — и почему расширение файла — это лишь соглашение об имени.",
        kicker_suffix="Разбираем путь",
        h1="Разбираем путь: name, stem, suffix, parent",
        lede="У пути, как у любого объекта, есть свои атрибуты — и они отвечают на конкретные вопросы о файле.",
        body_html=body,
    )


def build_10() -> None:
    body = f"""
    <p>Соберём вместе всё, что мы теперь знаем о путях: абсолютные и относительные пути, CWD,
    <code class="inline">pathlib.Path</code> и разбор пути на части.</p>
    {code_block(
        "puteshestvie_po_putyam.py",
        'from pathlib import Path\n\n'
        'BASE_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()\n'
        'data_dir = BASE_DIR / "data"\n'
        'data_dir.mkdir(exist_ok=True)\n\n'
        'file_path = data_dir / "otchet.txt"\n'
        'print("Абсолютный путь:", file_path.resolve())\n'
        'print("Имя:", file_path.name, "| Расширение:", file_path.suffix)\n'
        'print("Существует?", file_path.exists())\n',
    )}
    {callout(
        "info",
        "Path.resolve()",
        "<code class=\"inline\">path.resolve()</code> строит абсолютный, разрешённый вариант "
        "пути — удобно для отладки, чтобы увидеть, куда путь указывает на самом деле. Это не "
        "инструмент безопасности — не полагайтесь на него как на «санитайзер» пользовательского "
        "ввода (вернёмся к этому в разделе 15.28).",
    )}
    {exercise(1, "Путь к самому себе", "Выведите BASE_DIR, .parent от BASE_DIR и .parent.parent от BASE_DIR — понаблюдайте, как подниматься по дереву папок.")}
    {exercise(2, "Проверка перед чтением", "Постройте путь к несуществующему файлу в data/ и, используя .exists(), выведите одно из двух сообщений: «файл найден» или «файла нет — сначала создайте его».")}

    {practice_card(
        "15-10",
        "Практика: пути и CWD — итоговая тренировка",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-10/index.html",
    )}
    """
    page(
        "15-10-praktika-puti-i-cwd.html",
        page_title="Практика: пути и CWD",
        description="Закрепляем пути, CWD и pathlib.Path на одном небольшом упражнении перед переходом к самому файлу.",
        kicker_suffix="Практика: пути и CWD",
        h1="Практика: пути и CWD",
        lede="Прежде чем двигаться к самому файлу — закрепим уверенное владение путями.",
        body_html=body,
    )


def build_11() -> None:
    body = f"""
    <h2>open() возвращает объект</h2>
    <p>Это ещё одна прямая связь с главой 14. Результат <code class="inline">open(...)</code> —
    не «магический канал», а обычный Python-объект — объект файла:</p>
    {code_block("file_object.py", 'with open("privet.txt", "r", encoding="utf-8") as file:\n    print(type(file))\n')}
    {class_diagram(
        "TextIOWrapper (объект файла)",
        ["name", "mode", "closed"],
        ["read()", "readline()", "readlines()", "write(text)", "close()"],
        caption="file — экземпляр класса, отвечающего за чтение/запись текста конкретного открытого файла.",
    )}
    <p>Переменная <code class="inline">file</code> в наших примерах — это имя, которое мы сами
    выбираем; важно то, что оно ссылается на объект со своим состоянием (<code
    class="inline">.closed</code>, <code class="inline">.mode</code>, <code
    class="inline">.name</code>) и методами (<code class="inline">.read()</code>, <code
    class="inline">.write()</code> и другими).</p>
    {callout(
        "info",
        "Точную иерархию классов не запоминаем",
        "У Python есть отдельные внутренние классы для текстовых и бинарных файлов, но для "
        "повседневной работы достаточно знать: <code class=\"inline\">open()</code> возвращает "
        "объект файла с предсказуемым набором методов — точную иерархию классов ввода-вывода "
        "запоминать не нужно.",
    )}

    {practice_card(
        "15-11",
        "Практика: объект файла и его атрибуты",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-11/index.html",
    )}
    """
    page(
        "15-11-file-object.html",
        page_title="open() возвращает объект файла",
        description="open() создаёт обычный Python-объект со своими атрибутами (name, mode, closed) и методами (read, write, readline) — прямая связь с главой 14.",
        kicker_suffix="Объект файла",
        h1="open() возвращает объект файла",
        lede="Файл в Python — не магия, а объект со своим состоянием и методами.",
        body_html=body,
    )


def build_12() -> None:
    body = f"""
    <h2>Жизненный цикл файла</h2>
    {pipeline_diagram([
        {"kind": "plain", "title": "ЗАКРЫТ"},
        {"kind": "object", "title": "ОТКРЫТ", "note": "open()"},
        {"kind": "object", "title": "ОТКРЫТ", "rows": ["чтение / запись"], "note": ""},
        {"kind": "plain", "title": "ЗАКРЫТ", "note": "close()"},
    ], caption="Ручной жизненный цикл: открыть → работать → не забыть закрыть.")}

    <h2>С менеджером контекста</h2>
    {pipeline_diagram([
        {"kind": "plain", "title": "вход в with"},
        {"kind": "object", "title": "ОТКРЫТ", "rows": ["работа внутри блока"], "note": ""},
        {"kind": "plain", "title": "ЗАКРЫТ", "note": "выход из with — автоматически"},
    ], caption="with гарантирует закрытие даже при ошибке внутри блока.")}
    {code_block(
        "with_protokol.py",
        'with open("privet.txt", "r", encoding="utf-8") as file:\n'
        "    print(file.closed)   # False — файл открыт внутри блока\n"
        "print(file.closed)       # True — закрылся сам при выходе из блока\n",
    )}
    {callout(
        "tip",
        "with — это не просто «модный синтаксис»",
        "<code class=\"inline\">with</code> появился в Python 2.5 — дело не в новизне, а в "
        "надёжном управлении ресурсом: даже если внутри блока произойдёт исключение, протокол "
        "менеджера контекста всё равно выполнит корректное закрытие файла.",
    )}

    <h2 id="protokol">Что происходит под капотом</h2>
    <p>Это часть объектной модели Python: объекты, участвующие в <code class="inline">with</code>,
    поддерживают специальное поведение при входе и выходе из блока — методы <code
    class="inline">__enter__</code> и <code class="inline">__exit__</code>. Пока не нужно уметь
    писать свои такие объекты — достаточно знать, что файлы — лишь одно из применений этого
    протокола, а не какая-то функциональность, придуманная специально для файлов.</p>

    <h2>Ручное закрытие — исторический вариант</h2>
    {code_block(
        "ruchnoe_zakrytie.py",
        'file = open("privet.txt", "r", encoding="utf-8")\n'
        "content = file.read()\n"
        "file.close()   # нужно не забыть — и выполнить даже при ошибке выше\n",
    )}
    {callout(
        "warning",
        "with — не просто новее, а надёжнее",
        "Ручное открытие/закрытие всё ещё работает и встречается в старом коде, но <code "
        "class=\"inline\">with</code> рекомендуется не потому, что он новее, а потому, что "
        "закрытие происходит гарантированно, даже при ошибке.",
    )}

    {practice_card(
        "15-12",
        "Практика: жизненный цикл файла",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-12/index.html",
    )}
    """
    page(
        "15-12-zhiznenny-cikl-i-with.html",
        page_title="Жизненный цикл файла и with",
        description="Файл проходит путь закрыт → открыт → закрыт; менеджер контекста with гарантирует закрытие даже при ошибке — и это часть объектной модели Python (__enter__/__exit__).",
        kicker_suffix="Жизненный цикл и with",
        h1="Жизненный цикл файла и with",
        lede="with — не просто удобный синтаксис, а гарантия корректного закрытия ресурса.",
        body_html=body,
    )


def build_13() -> None:
    body = f"""
    <h2>Курсор файла</h2>
    <p>У открытого файла есть текущая <strong>позиция чтения/записи</strong> — курсор. Он
    двигается вперёд по мере чтения или записи:</p>
    {code_block(
        "kursor.py",
        'with open("alfavit.txt", "w", encoding="utf-8") as f:\n'
        '    f.write("ABCDE")\n\n'
        'with open("alfavit.txt", "r", encoding="utf-8") as f:\n'
        "    print(f.read(2))   # AB — курсор передвинулся на 2\n"
        "    print(f.read(2))   # CD — курсор передвинулся ещё на 2\n"
        "    print(f.read())    # E  — до конца файла\n"
        "    print(repr(f.read()))   # '' — курсор уже в конце\n",
    )}
    {file_cursor_diagram("ABCDE", 0, caption="Курсор перед первым read(2): позиция 0.")}
    {file_cursor_diagram("ABCDE", 2, caption="После read(2): курсор на позиции 2, прочитано «AB».")}
    {file_cursor_diagram("ABCDE", 4, caption="После второго read(2): курсор на позиции 4, прочитано «ABCD».")}
    {file_cursor_diagram("ABCDE", 5, caption="После read(): курсор в конце файла (EOF), позиция 5.")}

    {debug_lab(
        3,
        "Курсор уже в конце файла",
        "posle_eof.py",
        'with open("alfavit.txt", "r", encoding="utf-8") as f:\n'
        "    print(f.read())\n"
        "    print(f.read())   # ожидаем увидеть то же самое ещё раз?\n",
        ["ABCDE", "(пустая строка)"],
        "Второй <code class=\"inline\">f.read()</code> вернул пустую строку, а не «ABCDE» "
        "снова. Курсор не возвращается в начало сам — после первого <code "
        "class=\"inline\">read()</code> он остался в конце файла (EOF), и там больше нечего "
        "читать.",
        "vozvrat_v_nachalo.py",
        'with open("alfavit.txt", "r", encoding="utf-8") as f:\n'
        "    print(f.read())\n"
        "    f.seek(0)          # вручную возвращаем курсор в начало\n"
        "    print(f.read())    # теперь снова ABCDE\n",
    )}

    <h2>tell() и seek()</h2>
    {code_block(
        "tell_seek.py",
        'with open("alfavit.txt", "r", encoding="utf-8") as f:\n'
        "    f.read(2)\n"
        "    print(f.tell())   # 2 — текущая позиция курсора\n"
        "    f.seek(0)         # вернуться в начало\n"
        "    print(f.read())   # ABCDE — читаем заново\n",
    )}
    {callout(
        "warning",
        "seek() в текстовом режиме — не «номер символа»",
        "Для простых примеров с ASCII-текстом смещение, которое возвращает "
        "<code class=\"inline\">tell()</code>, интуитивно совпадает с числом прочитанных "
        "символов. Но в общем случае для текста в UTF-8 это неверно: один символ (особенно "
        "кириллица или эмодзи) может занимать несколько байт (раздел 15.16), и произвольные "
        "смещения не соответствуют напрямую индексам символов. Для произвольных байтовых "
        "смещений понятнее и безопаснее работать в бинарном режиме (раздел 15.17). Безопасное "
        "использование <code class=\"inline\">seek()</code> в текстовом режиме — "
        "<code class=\"inline\">seek(0)</code>, чтобы начать чтение сначала.",
    )}

    {practice_card(
        "15-13",
        "Практика: курсор файла, tell() и seek()",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-13/index.html",
    )}
    """
    page(
        "15-13-kursor-fajla.html",
        page_title="Курсор файла: tell() и seek()",
        description="Модель курсора файла: как read() двигает позицию, что происходит на EOF, и как tell()/seek(0) работают с этой позицией.",
        kicker_suffix="Курсор файла",
        h1="Курсор файла: tell() и seek()",
        lede="У открытого файла есть текущая позиция — она двигается вперёд, но сама назад не возвращается.",
        body_html=body,
    )


def build_14() -> None:
    body = f"""
    <h2>read() — весь файл целиком</h2>
    {code_block("read_ves.py", 'with open("spisok.txt", "r", encoding="utf-8") as f:\n    content = f.read()\n')}
    {callout(
        "info",
        "read() — не всегда плохо",
        "Для небольших файлов читать всё сразу — просто и удобно. Для очень больших файлов "
        "(гигабайты логов) это может занять много памяти — тогда лучше читать построчно или "
        "порциями (раздел 15.23). Не одно решение всегда правильное — важно выбирать под задачу.",
    )}

    <h2>readline() — по одной строке</h2>
    {code_block(
        "readline.py",
        'with open("spisok.txt", "r", encoding="utf-8") as f:\n'
        "    print(f.readline())   # первая строка\n"
        "    print(f.readline())   # вторая строка\n"
        "    # ...\n"
        "    print(repr(f.readline()))   # '' — когда строк больше нет\n",
    )}

    {debug_lab(
        4,
        "read() вместо readline()",
        "odna_stroka.py",
        'with open("spisok.txt", "r", encoding="utf-8") as f:\n'
        "    first_line = f.read()   # хотели одну строку\n"
        "    second_line = f.read()\n"
        '    print("Первая:", first_line)\n'
        '    print("Вторая:", repr(second_line))\n',
        ["Первая: яблоки\\nхлеб\\nмолоко\\nсыр\\n", "Вторая: ''"],
        "Ожидалось, что каждый вызов вернёт одну строку — но <code class=\"inline\">read()</code> "
        "без аргумента читает <strong>весь оставшийся файл</strong>, а не одну строку. Курсор "
        "сразу оказался в конце, и второй вызов вернул пустую строку.",
        "odna_stroka_fixed.py",
        'with open("spisok.txt", "r", encoding="utf-8") as f:\n'
        "    first_line = f.readline()\n"
        "    second_line = f.readline()\n"
        '    print("Первая:", first_line.strip())\n'
        '    print("Вторая:", second_line.strip())\n',
    )}

    <h2>Цикл по файлу — предпочтительный способ</h2>
    {code_block(
        "cikl_po_fajlu.py",
        'with open("spisok.txt", "r", encoding="utf-8") as f:\n'
        "    for line in f:\n"
        "        print(line.strip())\n",
    )}
    {callout(
        "tip",
        "Объект файла — итерируемый",
        "Как и список или строка (глава 10), объект файла можно обходить циклом "
        "<code class=\"inline\">for</code> напрямую — Python сам читает по одной строке за раз, "
        "не загружая весь файл в память.",
    )}

    <h2>readlines() — все строки списком</h2>
    {code_block(
        "readlines_spisok.py",
        'with open("spisok.txt", "r", encoding="utf-8") as f:\n'
        "    lines = f.readlines()\n\n"
        'print(len(lines), "строк")\n',
    )}
    {comparison_table(
        ["Способ", "Что возвращает", "Память"],
        [
            ["<code class=\"inline\">for line in file</code>", "по одной строке за раз", "экономно — подходит для больших файлов"],
            ["<code class=\"inline\">file.readlines()</code>", "список всех строк сразу", "весь список строк в памяти одновременно"],
        ],
    )}

    {practice_card(
        "15-14",
        "Практика: read(), readline(), readlines()",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-14/index.html",
    )}
    """
    page(
        "15-14-chitaem-fajly.html",
        page_title="Читаем файлы: read(), readline(), readlines()",
        description="Четыре способа прочитать содержимое файла: read() целиком, readline() по одной строке, цикл for по файлу и readlines() списком — с честным сравнением по памяти.",
        kicker_suffix="Читаем файлы",
        h1="Читаем файлы: read(), readline(), readlines()",
        lede="Один и тот же файл можно прочитать по-разному — и выбор способа — это выбор, а не формальность.",
        body_html=body,
    )


def build_15() -> None:
    body = f"""
    <h2>write() не добавляет перевод строки сам</h2>
    {code_block(
        "write_bez_n.py",
        'with open("log.txt", "w", encoding="utf-8") as f:\n'
        '    f.write("Hello")\n'
        '    f.write("World")\n',
    )}
    {file_state_diagram(
        "Записали", ["f.write(\"Hello\")", "f.write(\"World\")"],
        "На диске", ["HelloWorld"],
        action_label="→",
        caption="write() не вставляет \\n сам — если нужен перевод строки, пишите его явно: f.write(\"Hello\\n\").",
    )}

    <h2>Режимы открытия — обзор</h2>
    {capability_map(
        [
            ("open(путь, \"r\")", ["Чтение.", "Ошибка, если файл не существует."]),
            ("open(путь, \"w\")", ["Запись.", "Создаёт новый файл или очищает существующий", "УЖЕ ПРИ ОТКРЫТИИ."]),
            ("open(путь, \"a\")", ["Дозапись в конец.", "Создаёт файл, если его нет."]),
            ("open(путь, \"x\")", ["Создаёт новый файл.", "FileExistsError, если файл уже существует."]),
        ],
        title="Четыре базовых режима",
        caption="Дальше добавляются модификаторы t/b/+ (раздел 15.17 и далее).",
    )}

    {debug_lab(
        5,
        "\"w\" стирает файл ещё до записи",
        "perezapis.py",
        '# rezultaty.txt уже содержит важные результаты предыдущей игры\n'
        'with open("rezultaty.txt", "w", encoding="utf-8") as f:\n'
        "    pass   # ничего даже не записали\n",
        ["(файл rezultaty.txt теперь пуст)"],
        "Файл стал пустым, хотя мы ничего и не записали внутри блока. Открытие в режиме "
        "<code class=\"inline\">\"w\"</code> стирает прежнее содержимое <strong>в момент "
        "открытия</strong>, а не в момент первого <code class=\"inline\">write()</code>.",
        "dozapis_vmesto_w.py",
        '# если цель — добавить, а не заменить, нужен режим "a", а не "w"\n'
        'with open("rezultaty.txt", "a", encoding="utf-8") as f:\n'
        '    f.write("Новый результат\\n")\n',
    )}

    <h2>Режим "x" — создать, но не заменить</h2>
    {code_block(
        "rezhim_x.py",
        'try:\n'
        '    with open("save.json", "x", encoding="utf-8") as f:\n'
        '        f.write("{}")\n'
        'except FileExistsError:\n'
        '    print("Файл сохранения уже существует — не перезаписываем его случайно")\n',
    )}
    {callout(
        "tip",
        "x — защита от случайной перезаписи",
        "Если важно не перезаписать существующий файл по ошибке — режим "
        "<code class=\"inline\">\"x\"</code> явно сообщит об этом через "
        "<code class=\"inline\">FileExistsError</code>, вместо тихой перезаписи, которую сделал "
        "бы режим <code class=\"inline\">\"w\"</code>.",
    )}

    {debug_lab(
        6,
        "writelines() не добавляет переносы строк",
        "writelines_lovushka.py",
        'stroki = ["Anna", "Bob", "Carlos"]\n'
        'with open("igroki.txt", "w", encoding="utf-8") as f:\n'
        "    f.writelines(stroki)\n",
        ["(файл igroki.txt содержит одну строку: AnnaBobCarlos)"],
        "Ожидались три строки, а получилась одна слитая строка. "
        "<code class=\"inline\">writelines()</code> — несмотря на название — "
        "<strong>не добавляет переносы строк сама</strong>, она просто записывает элементы "
        "один за другим. Если нужны отдельные строки, перевод строки нужно включить в каждый "
        "элемент заранее.",
        "writelines_fixed.py",
        'stroki = ["Anna", "Bob", "Carlos"]\n'
        'with open("igroki.txt", "w", encoding="utf-8") as f:\n'
        '    f.writelines(s + "\\n" for s in stroki)\n',
    )}

    <h2 id="plus">[[icon:experiment]] Чуть глубже: модификаторы +</h2>
    <p><code class="inline">r+</code>, <code class="inline">w+</code>, <code
    class="inline">a+</code> открывают файл сразу для чтения и записи — но базовая семантика
    усечения/дозаписи каждого режима (<code class="inline">w</code> стирает, <code
    class="inline">a</code> добавляет в конец) продолжает действовать и здесь. Это необязательный
    материал — базовых <code class="inline">r</code>/<code class="inline">w</code>/<code
    class="inline">a</code>/<code class="inline">x</code> достаточно для большинства программ.</p>

    {practice_card(
        "15-15",
        "Практика: write() и режимы r/w/a/x",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-15/index.html",
    )}
    """
    page(
        "15-15-pishem-i-rezhimy.html",
        page_title="Пишем в файлы: write() и режимы r/w/a/x",
        description="write() не добавляет перевод строки сам, writelines() не добавляет переносы строк, режим w стирает файл при открытии, а x защищает от случайной перезаписи.",
        kicker_suffix="write() и режимы",
        h1="Пишем в файлы: write() и режимы r/w/a/x",
        lede="Каждый режим открытия — это осознанный выбор, а не деталь синтаксиса.",
        body_html=body,
    )


def build_16() -> None:
    body = f"""
    <h2>Текст и bytes — разные типы</h2>
    {code_block(
        "str_vs_bytes.py",
        "print(type(\"Python\"))     # <class 'str'>\n"
        "print(type(b\"Python\"))   # <class 'bytes'>\n",
    )}
    {callout(
        "info",
        "bytes — не «строка без Unicode»",
        "<code class=\"inline\">bytes</code> — это последовательность целых чисел от 0 до 255 "
        "(двоичные данные), а не урезанная версия строки. Текстовая строка "
        "(<code class=\"inline\">str</code>) и бинарные данные (<code class=\"inline\">bytes</code>) "
        "— два разных типа с разным назначением.",
    )}

    <h2>Кодирование и декодирование</h2>
    <p>Чтобы записать текст в файл, его строковое представление превращают в байты — это
    называется <strong>кодированием (encode)</strong>. При чтении происходит обратное —
    <strong>декодирование (decode)</strong>:</p>
    {code_block(
        "encode_decode.py",
        'text = "Привет"\n'
        'b = text.encode("utf-8")\n'
        "print(b)              # b'\\\\xd0\\\\x9f\\\\xd1\\\\x80\\\\xd0\\\\xb8\\\\xd0\\\\xb2\\\\xd0\\\\xb5\\\\xd1\\\\x82'\n"
        "print(len(text))      # 6  — шесть символов\n"
        "print(len(b))         # 12 — двенадцать байт!\n\n"
        'obratno = b.decode("utf-8")\n'
        "print(obratno)        # Привет\n",
    )}
    {pipeline_diagram([
        {"kind": "object", "title": 'str: "Привет"', "rows": ["6 символов"]},
        {"kind": "file", "title": "bytes", "rows": ["12 байт"], "note": 'encode("utf-8")'},
        {"kind": "object", "title": 'str: "Привет"', "rows": ["6 символов"], "note": 'decode("utf-8")'},
    ], caption="Кириллица в UTF-8 занимает больше байт, чем символов — реально выполненный пример.")}
    {callout(
        "warning",
        "Unicode ≠ UTF-8",
        "Unicode — это система, сопоставляющая символам числовые коды (какой символ значит "
        "какое число). UTF-8 — лишь один из способов записать эти числа байтами; есть и другие "
        "кодировки. В этом курсе мы всегда явно выбираем UTF-8 как стандарт для текстовых "
        "файлов — но это выбор, а не единственно возможный вариант.",
    )}
    <p>Когда формат текста заранее известен как UTF-8 (а в этом курсе это так почти всегда),
    явное указание <code class="inline">encoding="utf-8"</code> делает поведение программы
    предсказуемым и переносимым — вместо того, чтобы зависеть от кодировки по умолчанию,
    которая определяется платформой и настройками окружения выполнения.</p>

    <h2>Почему кодировка важна</h2>
    {debug_lab(
        7,
        "Файл открыт без указания encoding",
        "bez_encoding.py",
        'with open("privet.txt", "w") as f:   # без encoding!\n'
        '    f.write("Привет!")\n',
        [
            "# Работает по-разному на разных компьютерах и системах —",
            "# кодировка по умолчанию НЕ гарантированно UTF-8 везде.",
        ],
        "Без явного <code class=\"inline\">encoding=\"utf-8\"</code> Python использует кодировку "
        "по умолчанию, зависящую от платформы и настроек окружения — а не гарантированно UTF-8. "
        "Файл, записанный на одном компьютере, может быть неправильно прочитан на другом, если "
        "их кодировки по умолчанию различаются.",
        "s_encoding.py",
        'with open("privet.txt", "w", encoding="utf-8") as f:\n'
        '    f.write("Привет!")   # кодировка указана явно и предсказуема всегда\n',
    )}

    {debug_lab(
        8,
        "UnicodeDecodeError: неверная кодировка при чтении",
        "nevernaya_kodirovka.py",
        'data = "Привет".encode("utf-8")\n'
        'with open("soobshenie.bin", "wb") as f:\n'
        "    f.write(data)\n\n"
        '# читаем как текст в ДРУГОЙ кодировке\n'
        'with open("soobshenie.bin", "r", encoding="ascii") as f:\n'
        "    print(f.read())\n",
        [
            "Traceback (most recent call last):",
            "UnicodeDecodeError: 'ascii' codec can't decode byte 0xd0 in position 0: ordinal not in range(128)",
        ],
        "Байты были закодированы в UTF-8, а прочитаны как будто в ASCII — кодировки не совпали, "
        "и Python не смог превратить эти байты обратно в корректные символы. Решение — читать "
        "файл в той же кодировке, в которой он был записан.",
        "pravilnaya_kodirovka.py",
        'with open("soobshenie.bin", "r", encoding="utf-8") as f:\n'
        "    print(f.read())   # Привет\n",
    )}

    <h2 id="errors">[[icon:experiment]] Чуть глубже: параметр errors=</h2>
    <p>У <code class="inline">open()</code> есть параметр <code class="inline">errors</code>
    (<code class="inline">"strict"</code> по умолчанию, также <code class="inline">"replace"</code>,
    <code class="inline">"ignore"</code>) для случаев несовпадения кодировки.</p>
    {callout(
        "warning",
        "errors=\"ignore\" не универсальное решение",
        "<code class=\"inline\">errors=\"ignore\"</code> молча выбрасывает нераспознанные байты "
        "— это может незаметно потерять часть данных. Не используйте его как способ «просто "
        "убрать ошибку» без понимания, что именно теряется.",
    )}

    {practice_card(
        "15-16",
        "Практика: текст, bytes и UTF-8",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-16/index.html",
    )}
    """
    page(
        "15-16-text-bytes-encoding.html",
        page_title="Текст, bytes и кодировка UTF-8",
        description="str и bytes — разные типы; encode/decode превращают одно в другое; почему явный encoding=\"utf-8\" делает поведение программы предсказуемым, и что происходит при несовпадении кодировок.",
        kicker_suffix="Текст, bytes, UTF-8",
        h1="Текст, bytes и кодировка UTF-8",
        lede="Файлы хранят байты. То, как байты превращаются в текст, — это кодировка, и она не универсальна по умолчанию.",
        body_html=body,
    )


def build_17() -> None:
    body = f"""
    <h2>Бинарный режим</h2>
    <p>Добавьте <code class="inline">b</code> к режиму, чтобы работать с файлом как с чистыми
    байтами, без какой-либо текстовой кодировки:</p>
    {code_block(
        "binarny_fajl.py",
        'data = bytes([0, 1, 2, 3, 255])\n\n'
        'with open("signal.bin", "wb") as f:\n'
        "    f.write(data)\n\n"
        'with open("signal.bin", "rb") as f:\n'
        "    print(f.read())   # b'\\\\x00\\\\x01\\\\x02\\\\x03\\\\xff'\n",
    )}
    {comparison_table(
        ["Режим", "Что получаем в Python", "Пример"],
        [
            ["<code class=\"inline\">\"rt\" / \"r\"</code>", "str (текст)", '"Python"'],
            ["<code class=\"inline\">\"rb\"</code>", "bytes (двоичные данные)", "b'Python'"],
        ],
    )}
    {callout(
        "warning",
        "Не декодируйте произвольные бинарные данные как текст",
        "PNG, JPEG или PDF не станут читаемыми от <code class=\"inline\">open(..., "
        "encoding=\"utf-8\")</code> — это не текстовые данные, и попытка прочитать их как текст "
        "приведёт к ошибке или мусору. Для таких форматов используйте бинарный режим "
        "(<code class=\"inline\">\"rb\"</code>) или специализированную библиотеку для этого "
        "формата.",
    )}

    {debug_lab(
        9,
        "Бинарные данные, прочитанные как текст",
        "bin_kak_text.py",
        'data = bytes([0, 1, 2, 3, 255])\n'
        'with open("signal.bin", "wb") as f:\n'
        "    f.write(data)\n\n"
        'with open("signal.bin", "r", encoding="utf-8") as f:\n'
        "    print(f.read())\n",
        [
            "Traceback (most recent call last):",
            "UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 4: invalid start byte",
        ],
        "Байт <code class=\"inline\">0xff</code> не образует корректный символ в UTF-8 — эти "
        "данные никогда и не были текстом. Файл нужно открывать в бинарном режиме "
        "(<code class=\"inline\">\"rb\"</code>), а не текстовом.",
        "bin_pravilno.py",
        'with open("signal.bin", "rb") as f:\n'
        "    print(f.read())   # b'\\\\x00\\\\x01\\\\x02\\\\x03\\\\xff'\n",
    )}

    <h2>Переносы строк и текстовый режим</h2>
    {callout(
        "info",
        "\\n внутри Python — универсальный перевод строки",
        "На разных операционных системах исторически применяются разные последовательности для "
        "перевода строки на диске (например, <code class=\"inline\">\\r\\n</code> в файлах, "
        "созданных на Windows). Текстовый режим Python читает такие файлы в режиме универсальных "
        "переносов строк и отдаёт вам во всех случаях <code class=\"inline\">\\n</code> — вам не "
        "нужно обрабатывать оба варианта вручную в обычном текстовом коде.",
    )}

    <h2>Символы против байтов — реальный пример</h2>
    {code_block(
        "simvoly_vs_bajty.py",
        'text = "Питон🐍"\n'
        "print(len(text))                  # 6 — количество символов\n"
        'print(len(text.encode("utf-8")))  # 14 — количество байт в UTF-8\n',
    )}
    {callout(
        "tip",
        "Длина текста ≠ размер файла в байтах",
        "Кириллица и эмодзи занимают в UTF-8 несколько байт на один символ. "
        "<code class=\"inline\">len(text)</code> считает символы, а не байты — размер файла на "
        "диске может быть заметно больше, чем количество символов в строке.",
    )}

    {practice_card(
        "15-17",
        "Практика: бинарные файлы и переносы строк",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-17/index.html",
    )}
    """
    page(
        "15-17-binarnye-fajly-i-perevody-strok.html",
        page_title="Бинарные файлы и переносы строк",
        description="Бинарный режим (rb/wb), почему нельзя декодировать произвольные бинарные данные как текст, универсальные переносы строк и разница между длиной текста и размером файла в байтах.",
        kicker_suffix="Бинарные файлы",
        h1="Бинарные файлы и переносы строк",
        lede="Не всё, что лежит в файле, — текст. И даже текст занимает на диске больше, чем кажется.",
        body_html=body,
    )


def build_18() -> None:
    body = f"""
    <h2>Удобные методы pathlib для целого файла</h2>
    {code_block(
        "read_write_text.py",
        'from pathlib import Path\n\n'
        'path = Path("nastroyki.txt")\n'
        'path.write_text("Привет!", encoding="utf-8")\n'
        'print(path.read_text(encoding="utf-8"))   # Привет!\n',
    )}
    {code_block(
        "read_write_bytes.py",
        'from pathlib import Path\n\n'
        'path = Path("signal.bin")\n'
        'path.write_bytes(bytes([0, 1, 2]))\n'
        "print(path.read_bytes())   # b'\\\\x00\\\\x01\\\\x02'\n",
    )}
    {callout(
        "warning",
        "write_text()/write_bytes() заменяют содержимое целиком",
        "Как и режим <code class=\"inline\">\"w\"</code>, эти методы полностью заменяют "
        "содержимое файла — они не подходят, когда нужна дозапись.",
    )}

    <h2>open() vs удобные методы pathlib — когда что</h2>
    {decision_map(
        [
            ("Небольшой файл целиком, без потоковой обработки", "path.read_text() / write_text()"),
            ("Нужна построчная обработка или большой файл", "with path.open(...) как в разделах 15.11-15.14"),
            ("Целиком бинарные данные без потока", "path.read_bytes() / write_bytes()"),
            ("Нужен особый режим, например дозапись", "open(путь, \"a\", ...)"),
        ],
        title="Что выбрать для конкретной задачи",
    )}
    {callout(
        "info",
        "pathlib не заменяет open() полностью",
        "<code class=\"inline\">Path</code> добавляет удобные методы для частых случаев целиком "
        "прочитать/записать файл — но потоковая построчная обработка и специальные режимы всё "
        "ещё держатся на <code class=\"inline\">open()</code>/<code class=\"inline\">path.open()</code>. "
        "pathlib не «заменяет open() и делает его ненужным» — они решают разные задачи.",
    )}

    {practice_card(
        "15-18",
        "Практика: read_text, write_text, read_bytes, write_bytes",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-18/index.html",
    )}
    """
    page(
        "15-18-pathlib-udobnye-metody.html",
        page_title="pathlib: read_text, write_text, read_bytes, write_bytes",
        description="Короткие методы pathlib.Path для работы с файлом целиком — и honest-карта решений, когда они подходят, а когда нужен именно open().",
        kicker_suffix="pathlib: удобные методы",
        h1="pathlib: read_text, write_text, read_bytes, write_bytes",
        lede="Для «прочитать всё» и «записать всё» pathlib даёт короткую запись — но не отменяет open().",
        body_html=body,
    )


def build_19() -> None:
    body = f"""
    <h2>Проверяем, что перед нами</h2>
    {code_block(
        "exists_is_file_is_dir.py",
        'from pathlib import Path\n\n'
        'p = Path("data")\n'
        "print(p.exists())    # существует ли путь вообще\n"
        "print(p.is_file())   # это обычный файл?\n"
        "print(p.is_dir())    # это папка?\n",
    )}
    {decision_map(
        [
            ("exists() → False", "путь не существует"),
            ("exists() → True, is_file() → True", "обычный файл"),
            ("exists() → True, is_dir() → True", "папка"),
        ],
        title="Три исхода проверки пути",
    )}
    {callout(
        "warning",
        "exists() — это не гарантия на будущее",
        "Между проверкой <code class=\"inline\">if path.exists():</code> и следующей операцией "
        "файловая система может измениться — файл может быть удалён другим процессом, права "
        "доступа могут отличаться. Проверка существования полезна для логики программы, но не "
        "доказывает, что следующая операция обязательно пройдёт без ошибок (вернёмся к этому в "
        "разделе 15.22).",
    )}

    <h2>Создание папок</h2>
    {code_block("mkdir_prostoj.py", 'from pathlib import Path\n\nPath("data").mkdir()\n')}
    {code_block(
        "mkdir_nadezhny.py",
        'from pathlib import Path\n\n'
        'Path("data/users").mkdir(parents=True, exist_ok=True)\n'
        '# parents=True  — создать все промежуточные папки, если их ещё нет\n'
        '# exist_ok=True — не считать ошибкой, если папка уже существует\n',
    )}
    {tree_diagram(
        ("[[icon:folder]] project/  (до)", []),
        caption="До: project/ — пустой проект.",
    )}
    {tree_diagram(
        ("[[icon:folder]] project/  (после)", [
            ("[[icon:folder]] data/", [
                ("[[icon:folder]] users/", []),
            ]),
        ]),
        caption='После Path("data/users").mkdir(parents=True, exist_ok=True): обе папки созданы за один вызов.',
    )}

    {debug_lab(
        10,
        "Запись в несуществующую папку",
        "propushena_papka.py",
        'from pathlib import Path\n\n'
        'path = Path("data/users/anna.json")\n'
        'path.write_text("{}", encoding="utf-8")   # папки data/users ещё нет!\n',
        [
            "Traceback (most recent call last):",
            "FileNotFoundError: [Errno 2] No such file or directory: 'data/users/anna.json'",
        ],
        "Файл можно создать только внутри папки, которая уже существует. "
        "<code class=\"inline\">write_text()</code>/<code class=\"inline\">open(..., \"w\")</code> "
        "создают файл, но не создают недостающие родительские папки автоматически.",
        "papka_zagotovlena.py",
        'from pathlib import Path\n\n'
        'path = Path("data/users/anna.json")\n'
        'path.parent.mkdir(parents=True, exist_ok=True)   # сначала — папки\n'
        'path.write_text("{}", encoding="utf-8")            # потом — файл\n',
    )}

    {practice_card(
        "15-19",
        "Практика: exists(), is_file(), mkdir()",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-19/index.html",
    )}
    """
    page(
        "15-19-papki-exists-mkdir.html",
        page_title="Папки: exists(), is_file(), mkdir()",
        description="Проверка существования пути и его вида (файл/папка), создание папок с parents=True и exist_ok=True, и почему exists() не гарантирует, что следующая операция пройдёт без ошибок.",
        kicker_suffix="Папки: exists, mkdir",
        h1="Папки: exists(), is_file(), mkdir()",
        lede="Прежде чем работать с путём, часто нужно понять, что перед нами — и создать недостающие папки.",
        body_html=body,
    )


def build_20() -> None:
    body = f"""
    <h2>Список содержимого папки</h2>
    {code_block(
        "iterdir.py",
        'from pathlib import Path\n\n'
        'for item in sorted(Path("data").iterdir()):\n'
        "    print(item.name, \"—\", \"папка\" if item.is_dir() else \"файл\")\n",
    )}
    {callout(
        "tip",
        "Порядок не гарантирован",
        "<code class=\"inline\">iterdir()</code> не обещает какой-либо конкретный порядок "
        "элементов. Если порядок важен для вывода или для теста — оборачивайте в "
        "<code class=\"inline\">sorted(...)</code>, как в примере выше.",
    )}

    <h2>Поиск файлов по шаблону: glob()</h2>
    {code_block(
        "glob_prosty.py",
        'from pathlib import Path\n\n'
        'for f in sorted(Path("data").glob("*.txt")):\n'
        "    print(f.name)\n",
    )}
    {comparison_table(
        ["Файл в data/", "Подходит под \"*.txt\"?"],
        [
            ["a.txt", "да"],
            ["b.csv", "нет"],
            ["c.txt", "да"],
            ["notes.md", "нет"],
        ],
    )}
    {callout(
        "info",
        "glob() — один уровень, rglob() — рекурсивно",
        "<code class=\"inline\">Path(\"data\").glob(\"*.txt\")</code> ищет только в самой папке "
        "<code class=\"inline\">data</code>. Чтобы искать также во всех вложенных папках, "
        "используйте <code class=\"inline\">Path(\"data\").rglob(\"*.txt\")</code>. Не "
        "запускайте рекурсивный поиск на больших системных папках — это не игрушка для "
        "«просканировать весь диск».",
    )}

    <h2>Мини-проект: отчёт по папке</h2>
    <p>Соберите список содержимого учебной папки: имя, тип (файл/папка), расширение и размер (для
    файлов) — используя только <code class="inline">iterdir()</code> и атрибуты
    <code class="inline">Path</code>, без рекурсивного удаления или изменения содержимого.</p>
    {code_block(
        "otchet_po_papke.py",
        'from pathlib import Path\n\n'
        'def otchet(papka: Path) -> list[str]:\n'
        "    stroki = []\n"
        "    for item in sorted(papka.iterdir()):\n"
        '        vid = "папка" if item.is_dir() else "файл"\n'
        '        razmer = f", {item.stat().st_size} байт" if item.is_file() else ""\n'
        '        stroki.append(f"{item.name} — {vid}{razmer}")\n'
        "    return stroki\n\n"
        'for stroka in otchet(Path("data")):\n'
        "    print(stroka)\n",
    )}
    {exercise(2, "Только .json", "Измените отчёт так, чтобы он показывал только файлы с расширением .json, используя glob(\"*.json\") вместо iterdir().")}

    {practice_card(
        "15-20",
        "Практика: iterdir(), glob() и отчёт по папке",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-20/index.html",
    )}
    """
    page(
        "15-20-poisk-fajlov-glob.html",
        page_title="Поиск файлов: iterdir() и glob()",
        description="Список содержимого папки через iterdir(), поиск по шаблону через glob()/rglob() — и мини-проект: отчёт по учебной папке.",
        kicker_suffix="iterdir() и glob()",
        h1="Поиск файлов: iterdir() и glob()",
        lede="Часто нужно не открыть конкретный файл, а сначала понять, что вообще лежит в папке.",
        body_html=body,
    )


def build_21() -> None:
    body = f"""
    <h2>Переименование</h2>
    {code_block(
        "rename.py",
        'from pathlib import Path\n\n'
        'old_path = Path("chernovik.txt")\n'
        'old_path.rename("gotovo.txt")\n',
    )}
    {callout(
        "warning",
        "Файловые операции могут завершиться ошибкой",
        "Переименование, копирование и удаление — это обращения к операционной системе, а не "
        "гарантированно успешные действия Python. Они могут завершиться ошибкой по многим "
        "причинам файловой системы или прав доступа (раздел 15.22) — не считайте их "
        "непременно безотказными.",
    )}

    <h2>replace() — для «заменить целевой файл»</h2>
    {code_block(
        "replace.py",
        'from pathlib import Path\n\n'
        'novy_fajl = Path("save_new.json")\n'
        'tselevoy_fajl = Path("save.json")\n'
        'novy_fajl.replace(tselevoy_fajl)   # заменяет целевой файл, если он уже существует\n',
    )}
    <p>Мы вернёмся к этому в разделе 15.28 — он лежит в основе безопасного паттерна сохранения
    «сначала во временный файл, потом заменить основной».</p>

    <h2>Копирование — shutil</h2>
    {code_block(
        "shutil_copy.py",
        'import shutil\n\n'
        'shutil.copy("save.json", "save_backup.json")\n',
    )}
    {callout(
        "info",
        "pathlib и shutil дополняют друг друга",
        "<code class=\"inline\">pathlib</code> отлично работает с самими путями, а высокоуровневое "
        "копирование файлов обычно берёт на себя модуль стандартной библиотеки "
        "<code class=\"inline\">shutil</code> (<code class=\"inline\">shutil.copy</code>, "
        "<code class=\"inline\">shutil.copy2</code>, <code class=\"inline\">shutil.move</code>).",
    )}

    <h2 id="udalenie">Удаление — с максимальной осторожностью</h2>
    {callout(
        "warning",
        "[[icon:warning]] Удаление — разрушительная операция",
        "<code class=\"inline\">path.unlink()</code> удаляет файл <strong>без возможности "
        "отмены</strong> средствами самой программы. <code class=\"inline\">path.rmdir()</code> "
        "удаляет только <strong>пустую</strong> папку. В этом курсе мы никогда не используем "
        "рекурсивное удаление (<code class=\"inline\">shutil.rmtree</code>) как учебное "
        "упражнение — и все примеры удаления в практике работают только с файлами, созданными "
        "самой практикой в её собственной рабочей папке, никогда с произвольными путями "
        "пользователя.",
    )}
    {code_block(
        "unlink_bezopasno.py",
        'from pathlib import Path\n\n'
        'vremenny_fajl = Path("chernovik_kopiya.txt")\n'
        'if vremenny_fajl.exists():\n'
        "    vremenny_fajl.unlink()\n",
    )}

    {practice_card(
        "15-21",
        "Практика: переименование, копирование, удаление",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-21/index.html",
    )}
    """
    page(
        "15-21-pereimenovanie-kopirovanie-udalenie.html",
        page_title="Переименование, копирование, удаление",
        description="rename() и replace(), копирование через shutil, и почему удаление файла/папки — операция, к которой нужно относиться с максимальной осторожностью.",
        kicker_suffix="Переименование и удаление",
        h1="Переименование, копирование, удаление",
        lede="Эти операции по-настоящему меняют файловую систему — и не всегда обратимы.",
        body_html=body,
    )


def build_22() -> None:
    body = f"""
    <h2>Частые ошибки файловой системы</h2>
    {comparison_table(
        ["Исключение", "Когда возникает"],
        [
            ["<code class=\"inline\">FileNotFoundError</code>", "путь не существует, а операция ожидала существующий файл"],
            ["<code class=\"inline\">FileExistsError</code>", "режим \"x\" (или похожая операция) — а файл уже есть"],
            ["<code class=\"inline\">PermissionError</code>", "нет прав на чтение/запись этого пути"],
            ["<code class=\"inline\">IsADirectoryError</code>", "путь — папка, а операция ожидала файл"],
            ["<code class=\"inline\">NotADirectoryError</code>", "путь — файл, а операция ожидала папку"],
            ["<code class=\"inline\">UnicodeDecodeError</code>", "байты не удаётся декодировать выбранной кодировкой (15.16)"],
        ],
    )}
    {callout(
        "info",
        "Общий предок — OSError",
        "Большинство файловых исключений — это разновидности <code class=\"inline\">OSError</code>. "
        "Знать всю иерархию классов исключений не обязательно — достаточно уверенно "
        "распознавать перечисленные выше по имени и понимать, когда каждое из них возникает.",
    )}

    <h2>Чек-лист: файл не найден</h2>
    <ol>
      <li>Что сейчас является CWD? (<code class="inline">Path.cwd()</code>, раздел 15.7)</li>
      <li>Какой именно путь был построен в коде?</li>
      <li>Существует ли родительская папка этого пути?</li>
      <li>Нет ли опечатки в имени?</li>
      <li>Путь абсолютный или относительный — и относительно чего?</li>
      <li>Совпадает ли регистр букв в имени файла?</li>
    </ol>
    {callout(
        "warning",
        "Регистр имени файла — не мелочь",
        "Поведение по чувствительности к регистру различается между файловыми системами. Не "
        "считайте, что <code class=\"inline\">Data.txt</code> и <code class=\"inline\">data.txt</code> "
        "— обязательно один и тот же файл: пишите код так, чтобы имя совпадало точно.",
    )}

    {debug_lab(
        11,
        "Открыли папку как файл",
        "papka_kak_fajl.py",
        'from pathlib import Path\n\n'
        'Path("arhiv").mkdir(exist_ok=True)\n'
        'with open("arhiv", "r", encoding="utf-8") as f:   # "arhiv" — это папка!\n'
        "    print(f.read())\n",
        ["Traceback (most recent call last):", "IsADirectoryError: [Errno 21] Is a directory: 'arhiv'"],
        "<code class=\"inline\">\"arhiv\"</code> — папка, а не файл, и её нельзя открыть как файл "
        "для чтения текста. Перед открытием стоило проверить <code class=\"inline\">.is_file()</code>.",
        "proverka_pered_otkrytiem.py",
        'from pathlib import Path\n\n'
        'path = Path("arhiv")\n'
        'if path.is_file():\n'
        '    with path.open("r", encoding="utf-8") as f:\n'
        "        print(f.read())\n"
        "else:\n"
        '    print(f"{path} — не обычный файл")\n',
    )}

    <h2>Обрабатываем именно ту ошибку, которую ожидаем</h2>
    {code_block(
        "targeted_except.py",
        'from pathlib import Path\n\n'
        'path = Path("nastroyki.json")\n'
        "try:\n"
        '    text = path.read_text(encoding="utf-8")\n'
        "except FileNotFoundError:\n"
        '    print("Файл настроек не найден — используем значения по умолчанию")\n'
        '    text = "{}"\n',
    )}
    {callout(
        "warning",
        "Никогда except: pass",
        "Пустой перехват всех исключений подряд молча прячет реальные проблемы программы. "
        "Ловите конкретное ожидаемое исключение — как <code class=\"inline\">FileNotFoundError</code> "
        "выше — а не всё подряд.",
    )}

    <h2 id="eafp">[[icon:experiment]] Чуть глубже: EAFP и LBYL</h2>
    <p>Два стиля: <strong>проверить заранее</strong> (<code class="inline">if path.exists():</code>)
    или <strong>попробовать и обработать ошибку</strong> (<code class="inline">try/except</code>).
    В Python операции с файлами часто пишут вторым способом — именно потому, что состояние
    файловой системы может измениться между проверкой и самой операцией (раздел 15.19). Запоминать
    сами английские сокращения не обязательно — важна идея.</p>

    {practice_card(
        "15-22",
        "Практика: ошибки файловой системы",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-22/index.html",
    )}
    """
    page(
        "15-22-oshibki-fajlovoj-sistemy.html",
        page_title="Ошибки файловой системы",
        description="Каталог частых файловых исключений, чек-лист диагностики «файл не найден», и почему обрабатывать нужно именно то исключение, которое ожидается — а не всё подряд.",
        kicker_suffix="Ошибки файловой системы",
        h1="Ошибки файловой системы",
        lede="Файловые операции обращаются к внешнему миру — и внешний мир не всегда отвечает так, как хочется.",
        body_html=body,
    )


def build_23() -> None:
    body = f"""
    <h2>Размер файла</h2>
    {code_block(
        "razmer_fajla.py",
        'from pathlib import Path\n\n'
        'path = Path("spisok.txt")\n'
        "print(path.stat().st_size, \"байт\")\n",
    )}
    {callout(
        "tip",
        "Размер в байтах — не длина текста",
        "<code class=\"inline\">.stat().st_size</code> — это размер в байтах на диске, а не "
        "количество символов. Для текста в UTF-8 с кириллицей или эмодзи эти числа, как мы "
        "видели в разделе 15.17, обычно не совпадают.",
    )}

    <h2>Маленький файл vs большой файл</h2>
    {decision_map(
        [
            ("Файл заведомо небольшой (настройки, короткая заметка)", "read_text() / read() целиком — просто и понятно"),
            ("Файл может быть очень большим (журнал, лог за год)", "построчная обработка — цикл for line in file"),
        ],
        title="Выбор способа чтения по размеру файла",
    )}
    {callout(
        "warning",
        "readlines() на действительно большом файле",
        "Файл в 1 гигабайт логов — плохой повод для <code class=\"inline\">readlines()</code>: "
        "весь список строк придётся держать в памяти одновременно. Построчный цикл <code "
        "class=\"inline\">for line in file</code> обрабатывает файл по одной строке, не "
        "накапливая их все сразу.",
    )}

    <h2 id="chunked">[[icon:experiment]] Чуть глубже: чтение бинарных данных порциями</h2>
    <p>Для очень больших бинарных файлов иногда читают не всё сразу, а порциями (<em>chunks</em>)
    фиксированного размера:</p>
    {code_block(
        "chunked_read.py",
        'with open("bolshoy_fajl.bin", "rb") as f:\n'
        "    while True:\n"
        "        chunk = f.read(8192)   # порция по 8192 байта\n"
        "        if not chunk:\n"
        "            break\n"
        "        # обработать chunk здесь\n",
    )}
    <p>Это необязательный, более глубокий материал — для большинства учебных и небольших
    прикладных задач построчного чтения текста достаточно.</p>

    <h2>Мини-проект: анализатор текстового файла</h2>
    <p>Посчитаем строки, слова и символы файла потоково — без загрузки всего файла в память
    сразу как единой строки:</p>
    {code_block(
        "analizator_fajla.py",
        'from pathlib import Path\n\n'
        'def analiz_fajla(path: Path) -> dict[str, int]:\n'
        "    stroki = 0\n"
        "    slova = 0\n"
        "    simvoly = 0\n"
        '    with path.open("r", encoding="utf-8") as f:\n'
        "        for line in f:\n"
        "            stroki += 1\n"
        "            slova += len(line.split())\n"
        "            simvoly += len(line)\n"
        '    return {"строки": stroki, "слова": slova, "символы": simvoly}\n\n'
        'print(analiz_fajla(Path("spisok.txt")))\n',
    )}
    {exercise(2, "Байты отдельно", "Добавьте в отчёт четвёртое число — размер файла в байтах через .stat().st_size — и сравните его с количеством символов.")}

    {practice_card(
        "15-23",
        "Практика: большие файлы и анализатор текста",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-23/index.html",
    )}
    """
    page(
        "15-23-bolshie-fajly-i-potoki.html",
        page_title="Большие файлы и потоковая обработка",
        description="Как выбрать между чтением целиком и построчной обработкой по размеру файла, размер файла в байтах — и мини-проект: потоковый анализатор текстового файла.",
        kicker_suffix="Большие файлы",
        h1="Большие файлы и потоковая обработка",
        lede="Способ чтения файла — это решение, которое должно учитывать его размер.",
        body_html=body,
    )


def build_24() -> None:
    body = f"""
    <h2>Один и тот же вопрос, разные форматы</h2>
    <p>Как из главы 11 знаком словарь:</p>
    {code_block(
        "igrok_slovar.py",
        'igrok = {\n'
        '    "name": "Anna",\n'
        '    "score": 1200,\n'
        '    "skills": ["Python", "Git"],\n'
        "}\n",
    )}
    <p>Как сохранить такую структуру в файл? <code class="inline">str(igrok)</code> технически
    сработает, но это не настоящий формат для обмена данными — его неудобно и небезопасно
    разбирать обратно. Нужен <strong>формат хранения</strong>, у которого есть чёткие правила
    записи и чтения.</p>

    <h2>Сериализация</h2>
    {callout(
        "info",
        "Сериализация и десериализация",
        "<strong>Сериализация</strong> — превращение структуры Python (словаря, списка, объекта) "
        "в представление, которое можно сохранить или передать (текст или байты). "
        "<strong>Десериализация</strong> — восстановление структуры данных обратно из этого "
        "представления.",
    )}
    {pipeline_diagram([
        {"kind": "object", "title": "dict / list", "rows": ['{"name": "Anna", ...}']},
        {"kind": "file", "title": "JSON-текст", "rows": ["сериализовано"], "note": "сериализация"},
        {"kind": "file", "title": "файл на диске"},
    ], caption="Сериализация превращает объекты Python в сохраняемый текст.")}

    <h2>Как выбрать формат</h2>
    {decision_map(
        [
            ("Простой человекочитаемый текст — заметки, лог", "обычный текстовый файл (главы 15.1-15.4)"),
            ("Таблица со строками и столбцами", "CSV (раздел 15.27)"),
            ("Вложенная структура — словари, списки, настройки, сохранение игры", "JSON (раздел 15.25)"),
            ("Картинка, звук, произвольные не-текстовые данные", "бинарный формат (раздел 15.17)"),
        ],
        title="Какой формат хранения выбрать",
    )}
    {callout(
        "tip",
        "Ни один формат не «лучший всегда»",
        "Выбор формата — это решение под конкретную задачу, а не вопрос моды. Плоский текст "
        "подходит для заметок, но плохо подходит для вложенных структур; JSON отлично сохраняет "
        "структуру, но плохо подходит для таблиц с тысячами одинаковых строк, где куда удобнее "
        "CSV.",
    )}

    {practice_card(
        "15-24",
        "Практика: выбираем формат хранения",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-24/index.html",
    )}
    """
    page(
        "15-24-kak-vybrat-format.html",
        page_title="Как выбрать формат хранения данных",
        description="Сериализация и десериализация как общая идея, и практическая карта решений: когда подходит обычный текст, когда CSV, когда JSON, а когда — бинарный формат.",
        kicker_suffix="Выбор формата",
        h1="Как выбрать формат хранения данных",
        lede="Прежде чем сохранять данные, стоит спросить: а в каком виде их сохранить?",
        body_html=body,
    )


def build_25() -> None:
    body = f"""
    <h2>Модуль json</h2>
    {code_block(
        "json_dump.py",
        'import json\n\n'
        'data = {"name": "Anna", "score": 1200}\n\n'
        'with open("igrok.json", "w", encoding="utf-8") as f:\n'
        "    json.dump(data, f, ensure_ascii=False, indent=2)\n",
    )}
    {terminal_transcript(
        ["$ cat igrok.json", "{", '  "name": "Anna",', '  "score": 1200', "}"],
        caption="Реально сохранённый файл — самый обычный текст, его можно открыть в любом редакторе.",
    )}
    {code_block(
        "json_load.py",
        'import json\n\n'
        'with open("igrok.json", "r", encoding="utf-8") as f:\n'
        "    data = json.load(f)\n\n"
        "print(type(data))   # <class 'dict'>\n"
        "print(data[\"name\"])   # Anna\n",
    )}

    <h2>dump/load vs dumps/loads</h2>
    {comparison_table(
        ["Функция", "Что делает"],
        [
            ["<code class=\"inline\">json.dump(data, file)</code>", "пишет JSON прямо в открытый файловый объект"],
            ["<code class=\"inline\">json.dumps(data)</code>", "возвращает JSON как обычную строку str"],
            ["<code class=\"inline\">json.load(file)</code>", "читает JSON из открытого файлового объекта"],
            ["<code class=\"inline\">json.loads(text)</code>", "разбирает JSON из готовой строки str"],
        ],
    )}

    <h2>Соответствие типов JSON ↔ Python</h2>
    {comparison_table(
        ["JSON", "Python"],
        [
            ["object", "dict"],
            ["array", "list"],
            ["string", "str"],
            ["number", "int / float"],
            ["true / false", "True / False"],
            ["null", "None"],
        ],
    )}

    <h2>Что JSON не умеет напрямую</h2>
    {callout(
        "warning",
        "JSON не сохраняет произвольный объект Python сам",
        "<code class=\"inline\">set</code>, экземпляр собственного класса, <code "
        "class=\"inline\">bytes</code>, <code class=\"inline\">complex</code> — все они не "
        "имеют прямого представления в JSON. <code class=\"inline\">json.dump()</code> не умеет "
        "«магически» сохранить произвольный объект Python — сначала нужно самостоятельно "
        "привести данные к словарям/спискам/строкам/числам.",
    )}
    {callout(
        "info",
        "Кортеж при чтении вернётся списком",
        "Если сохранить <code class=\"inline\">tuple</code> как JSON-массив, при загрузке "
        "обратно вы получите обычный <code class=\"inline\">list</code>, а не "
        "<code class=\"inline\">tuple</code> — JSON не различает эти два типа Python, у него "
        "есть только один вид «массив».",
    )}

    {debug_lab(
        12,
        "Некорректный JSON в файле",
        "slomanny_json.py",
        'with open("nastroyki.json", "w", encoding="utf-8") as f:\n'
        '    f.write(\'{"theme": "dark",}\')   # лишняя запятая перед }\n\n'
        'import json\n'
        'with open("nastroyki.json", "r", encoding="utf-8") as f:\n'
        "    data = json.load(f)\n",
        ["Traceback (most recent call last):", "json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes"],
        "Наличие файла не означает, что его содержимое — корректный JSON: файл мог быть "
        "повреждён, отредактирован вручную или записан с ошибкой в другом месте программы. "
        "<code class=\"inline\">json.JSONDecodeError</code> — сигнал именно об этом, а не о "
        "проблеме с путём или правами доступа.",
        "json_bez_zapyatoj.py",
        'with open("nastroyki.json", "w", encoding="utf-8") as f:\n'
        '    f.write(\'{"theme": "dark"}\')\n',
    )}

    <h2>Мини-проект: менеджер настроек</h2>
    <p>Настройки приложения, которые нужно будет использовать в графическом приложении главы
    16 — с понятными значениями по умолчанию, если файла ещё нет:</p>
    {code_block(
        "nastroyki_menedzher.py",
        'import json\n'
        'from pathlib import Path\n\n'
        'DEFAULT_SETTINGS = {"theme": "light", "language": "ru", "window_width": 900}\n\n'
        'def load_settings(path: Path) -> dict:\n'
        "    if not path.exists():\n"
        "        return dict(DEFAULT_SETTINGS)\n"
        '    with path.open("r", encoding="utf-8") as f:\n'
        "        return json.load(f)\n\n"
        'def save_settings(path: Path, settings: dict) -> None:\n'
        '    with path.open("w", encoding="utf-8") as f:\n'
        "        json.dump(settings, f, ensure_ascii=False, indent=2)\n\n"
        'settings_path = Path("nastroyki.json")\n'
        "settings = load_settings(settings_path)\n"
        'settings["theme"] = "dark"\n'
        "save_settings(settings_path, settings)\n",
    )}
    {callout(
        "info",
        "Готовим почву для главы 16",
        "Именно так графическое приложение на Tkinter (глава 16) сможет запоминать настройки "
        "пользователя между запусками — загружать их при старте и сохранять при изменении, без "
        "единой строчки кода интерфейса в этой функции.",
    )}

    {practice_card(
        "15-25",
        "Практика: JSON и менеджер настроек",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-25/index.html",
    )}
    """
    page(
        "15-25-json-serializatsiya.html",
        page_title="JSON: сохраняем структуры данных",
        description="json.dump/load и dumps/loads, соответствие типов JSON и Python, ограничения JSON, и мини-проект: менеджер настроек со значениями по умолчанию.",
        kicker_suffix="JSON",
        h1="JSON: сохраняем структуры данных",
        lede="Словари и списки из главы 11 наконец получают надёжный способ пережить перезапуск программы.",
        body_html=body,
    )


def build_26() -> None:
    body = f"""
    <p>Соберём вместе главу 14 (dataclasses, объекты) и главу 15 (JSON, файлы): сохраним и
    загрузим настоящего игрового персонажа.</p>
    {code_block(
        "player_dataclass.py",
        'from dataclasses import dataclass, asdict\n\n'
        "@dataclass\n"
        "class Player:\n"
        "    name: str\n"
        "    score: int\n"
        "    inventory: list[str]\n",
    )}

    <h2>Сохранение</h2>
    {code_block(
        "save_player.py",
        'import json\n'
        'from dataclasses import asdict\n'
        'from pathlib import Path\n\n'
        'player = Player(name="Anna", score=1200, inventory=["меч", "щит"])\n\n'
        'with Path("save.json").open("w", encoding="utf-8") as f:\n'
        "    json.dump(asdict(player), f, ensure_ascii=False, indent=2)\n",
    )}
    {callout(
        "tip",
        "asdict() — короткий путь от dataclass к словарю",
        "<code class=\"inline\">dataclasses.asdict()</code> (глава 14) превращает экземпляр "
        "dataclass в обычный словарь — если все значения внутри уже JSON-совместимы (строки, "
        "числа, списки, словари), результат можно передать прямо в <code "
        "class=\"inline\">json.dump()</code>.",
    )}

    <h2>Загрузка</h2>
    {code_block(
        "load_player.py",
        'import json\n'
        'from pathlib import Path\n\n'
        'with Path("save.json").open("r", encoding="utf-8") as f:\n'
        "    data = json.load(f)\n\n"
        "loaded_player = Player(**data)\n"
        "print(loaded_player)\n",
    )}

    {pipeline_diagram([
        {"kind": "object", "title": "player : Player", "rows": ['name = "Anna"', "score = 1200"]},
        {"kind": "file", "title": "save.json", "rows": ["JSON-текст на диске"], "note": "asdict() + json.dump()"},
        {"kind": "plain", "title": "программа завершается"},
        {"kind": "object", "title": "loaded_player : Player", "rows": ['name = "Anna"', "score = 1200"], "note": "json.load() + Player(**data)"},
    ], caption="loaded_player — НЕ тот же объект, что player: это новый экземпляр, восстановленный из файла.")}
    {callout(
        "warning",
        "Это не «тот же самый» объект",
        "После перезапуска программы <code class=\"inline\">loaded_player</code> — это "
        "<strong>новый</strong> экземпляр <code class=\"inline\">Player</code>, построенный из "
        "данных файла, а не тот объект, что существовал в предыдущем запуске программы. Он "
        "просто имеет такое же состояние — и в этом и есть смысл персистентности: не сохранить "
        "сам объект Python, а сохранить достаточно данных, чтобы восстановить эквивалентное "
        "состояние.",
    )}

    {exercise(3, "Дальше самостоятельно: книга контактов на JSON", "Возьмите контактную книгу главы 12 (словарь имя → телефон) и добавьте ей сохранение/загрузку через JSON, по образцу этого раздела — теперь контакты будут переживать перезапуск программы.")}

    {practice_card(
        "15-26",
        "Практика: сохраняем и загружаем Player",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-26/index.html",
    )}
    """
    page(
        "15-26-mini-proekt-save-player.html",
        page_title="Мини-проект: сохраняем Player",
        description="Мини-проект: dataclass Player из главы 14 сохраняется в JSON и восстанавливается новым экземпляром — persistence как реконструкция состояния, а не выживание объекта.",
        kicker_suffix="Мини-проект: Player",
        h1="Мини-проект: сохраняем Player",
        lede="Объект из главы 14 наконец умеет переживать перезапуск программы.",
        body_html=body,
    )


def build_27() -> None:
    body = f"""
    <h2>Таблица в текстовом виде</h2>
    {code_block(
        "rekordy.csv",
        "name,score,level\n"
        "Anna,1200,5\n"
        "Bob,900,4\n",
        lang="text",
    )}
    <p>CSV (comma-separated values) — простой текстовый формат для таблиц: строки — записи,
    значения в строке разделены запятыми. Подходит для экспорта в таблицы, отчётов, наборов
    данных.</p>

    <h2>Почему НЕ split(",")</h2>
    {debug_lab(
        13,
        "CSV, разобранный через split(\",\")",
        "csv_split_lovushka.py",
        'stroka = \'Anna,\"Отлично, продолжай!\"\'\n'
        'chasti = stroka.split(",")\n'
        "print(chasti)\n",
        ["['Anna', '\"Отлично', ' продолжай!\"']"],
        "Поле в кавычках само содержало запятую — как и полноценно допускает формат CSV. "
        "<code class=\"inline\">split(\",\")</code> ничего не знает про кавычки в CSV и слепо "
        "режет по каждой запятой, разрывая одно поле на два. Разбирать CSV нужно модулем "
        "<code class=\"inline\">csv</code>, который правильно обрабатывает кавычки и "
        "запятые внутри полей.",
        "csv_modul_pravilno.py",
        'import csv\n'
        'import io\n\n'
        'stroka = \'Anna,\"Отлично, продолжай!\"\'\n'
        "reader = csv.reader(io.StringIO(stroka))\n"
        "print(next(reader))   # ['Anna', 'Отлично, продолжай!']\n",
    )}

    <h2>csv.reader и csv.DictReader</h2>
    {code_block(
        "csv_reader.py",
        'import csv\n\n'
        'with open("rekordy.csv", "r", encoding="utf-8", newline="") as f:\n'
        "    reader = csv.reader(f)\n"
        "    for row in reader:\n"
        "        print(row)\n",
    )}
    {callout(
        "info",
        "Зачем newline=\"\"",
        "Документация модуля <code class=\"inline\">csv</code> рекомендует открывать файл с "
        "<code class=\"inline\">newline=\"\"</code>, чтобы сам модуль полностью управлял "
        "переносами строк внутри полей — без этого возможна двойная обработка переносов на "
        "некоторых платформах.",
    )}
    {code_block(
        "csv_dictreader.py",
        'import csv\n\n'
        'with open("rekordy.csv", "r", encoding="utf-8", newline="") as f:\n'
        "    reader = csv.DictReader(f)\n"
        "    for row in reader:\n"
        '        print(row["name"], int(row["score"]))\n',
    )}
    {callout(
        "warning",
        "Значения CSV — всегда строки, пока вы их не преобразуете",
        "<code class=\"inline\">row[\"score\"]</code> — это строка <code "
        "class=\"inline\">\"1200\"</code>, а не число <code class=\"inline\">1200</code>, даже "
        "если оно похоже на число визуально. CSV не хранит информацию о типе — приведение "
        "(<code class=\"inline\">int(...)</code>, <code class=\"inline\">float(...)</code>) "
        "нужно делать самостоятельно.",
    )}

    <h2>Запись CSV</h2>
    {code_block(
        "csv_writer.py",
        'import csv\n\n'
        'rows = [\n'
        '    {"name": "Anna", "score": 1200},\n'
        '    {"name": "Bob", "score": 900},\n'
        "]\n\n"
        'with open("novye_rekordy.csv", "w", encoding="utf-8", newline="") as f:\n'
        '    writer = csv.DictWriter(f, fieldnames=["name", "score"])\n'
        "    writer.writeheader()\n"
        "    writer.writerows(rows)\n",
    )}

    <h2>CSV vs JSON — и CSV — не Excel</h2>
    {comparison_table(
        ["", "CSV", "JSON"],
        [
            ["Лучше подходит для", "однородных таблиц (строки/столбцы)", "вложенных структур"],
            ["Типы данных", "всё — строки текста", "строки, числа, булевы, вложенность"],
        ],
    )}
    {callout(
        "info",
        "CSV — это не файл Excel",
        "<code class=\"inline\">.csv</code> — обычный текстовый формат, а не формат-книга "
        "<code class=\"inline\">.xlsx</code> с листами, формулами и форматированием — тем "
        "занимаются другие, специализированные библиотеки.",
    )}

    {practice_card(
        "15-27",
        "Практика: CSV — csv.reader, DictReader, writer",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-27/index.html",
    )}
    """
    page(
        "15-27-csv-tablitsy.html",
        page_title="CSV: таблицы в текстовом виде",
        description="Формат CSV, почему split(\",\") ненадёжен, csv.reader/DictReader/writer, и честное сравнение CSV с JSON.",
        kicker_suffix="CSV",
        h1="CSV: таблицы в текстовом виде",
        lede="Табличные данные заслуживают формат, который понимает, что такое поле — а не просто разделитель.",
        body_html=body,
    )


def build_28() -> None:
    body = f"""
    <h2>Перед записью — спросите себя</h2>
    <ol>
      <li>Я хочу заменить содержимое или дозаписать?</li>
      <li>Или создать только если файла ещё нет?</li>
      <li>Нужна ли резервная копия перед изменением?</li>
      <li>Это точно тот путь, который я имею в виду?</li>
    </ol>
    {callout(
        "warning",
        "Режим — осознанный выбор, не заготовка из примера",
        "<code class=\"inline\">\"r\"</code>, <code class=\"inline\">\"w\"</code>, <code "
        "class=\"inline\">\"a\"</code>, <code class=\"inline\">\"x\"</code> — каждый несёт "
        "разные последствия для существующего содержимого (раздел 15.15). Копировать режим из "
        "примера без вопроса «а что именно мне сейчас нужно?» — источник потери данных.",
    )}

    <h2>Практики этого курса — только в песочнице</h2>
    {callout(
        "warning",
        "[[icon:warning]] Обязательное правило безопасности практик",
        "Все файловые практики этого курса читают, создают, изменяют и удаляют файлы "
        "<strong>только внутри собственной рабочей папки практики</strong>. Никогда — файлы "
        "репозитория курса, документы, которые вы уже сохранили, домашнюю папку пользователя "
        "или произвольные абсолютные пути. Это касается и ваших собственных программ: не "
        "выполняйте разрушительные операции над путём, который пришёл откуда-то извне, не "
        "проверив его.",
    )}

    <h2>Путь наружу из своей папки — path traversal</h2>
    {code_block(
        "put_naruzhu.py",
        'imya_fajla = input("Имя файла для сохранения: ")\n'
        '# если пользователь введёт "../../important.txt" — куда это укажет?\n'
        'path = Path("data") / imya_fajla\n',
    )}
    {callout(
        "warning",
        "Наивное объединение пути — риск выйти за пределы папки",
        "Если имя файла приходит от пользователя и содержит <code class=\"inline\">..</code>, "
        "простое объединение с базовой папкой может увести путь за её пределы, в совершенно "
        "другое место файловой системы. Мы не строим здесь полноценный фильтр безопасности — "
        "важно просто знать о самом риске и не доверять пользовательскому имени файла как "
        "безопасному само по себе.",
    )}

    <h2 id="safe-save">[[icon:launch]] Профессиональнее: безопасное сохранение</h2>
    <p>Идея, снижающая риск оставить основной файл в повреждённом промежуточном состоянии:
    сначала записать во <strong>временный</strong> файл в той же папке, а затем заменить
    основной файл целиком:</p>
    {code_block(
        "bezopasnoe_sohranenie.py",
        'import json\n'
        'from pathlib import Path\n\n'
        'def bezopasno_sohranit(path: Path, data: dict) -> None:\n'
        '    vremenny = path.with_suffix(path.suffix + ".tmp")\n'
        '    with vremenny.open("w", encoding="utf-8") as f:\n'
        "        json.dump(data, f, ensure_ascii=False, indent=2)\n"
        "    vremenny.replace(path)   # заменяем основной файл только когда всё уже записано\n",
    )}
    {callout(
        "info",
        "Не абсолютная гарантия — а сниженный риск",
        "Это снижает риск оставить <code class=\"inline\">path</code> в частично записанном "
        "состоянии при обрыве записи, но не является абсолютной гарантией сохранности данных "
        "на любом оборудовании и любой файловой системе.",
    )}

    <h2>Резервная копия перед заменой</h2>
    {code_block(
        "backup_pered_zamenoj.py",
        'import shutil\n'
        'from pathlib import Path\n\n'
        'path = Path("save.json")\n'
        "if path.exists():\n"
        '    shutil.copy(path, path.with_suffix(".json.bak"))\n',
    )}
    {callout(
        "tip",
        "Одна резервная копия, не бесконечная цепочка",
        "Одной актуальной резервной копии перед заменой обычно достаточно для учебных и "
        "небольших прикладных задач — не нужно плодить бесконечно растущую цепочку файлов "
        "<code class=\"inline\">.bak.bak.bak</code>.",
    )}

    {practice_card(
        "15-28",
        "Практика: безопасная запись и резервная копия",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-28/index.html",
    )}
    """
    page(
        "15-28-bezopasnaya-rabota-s-fajlami.html",
        page_title="Безопасная работа с файлами",
        description="Обязательное правило песочницы для файловых практик, риск path traversal, и паттерн «сначала во временный файл, потом заменить» для более надёжного сохранения.",
        kicker_suffix="Безопасная работа с файлами",
        h1="Безопасная работа с файлами",
        lede="Запись в файл — действие с последствиями. Разумная осторожность стоит нескольких лишних строк кода.",
        body_html=body,
    )


def build_29() -> None:
    body = f"""
    <p>Соберём файлы, списки, словари, функции (глава 13) и сортировку (глава 11) в одном
    практическом проекте — таблице рекордов.</p>
    {pipeline_diagram([
        {"kind": "file", "title": "rekordy.csv", "rows": ["записи с предыдущих игр"]},
        {"kind": "object", "title": "список записей", "rows": ['[{"name": "Anna", ...}, ...]'], "note": "загрузка"},
        {"kind": "object", "title": "список + новая запись", "note": "добавление результата"},
        {"kind": "object", "title": "отсортированный список", "note": "sort по score"},
        {"kind": "file", "title": "rekordy.csv", "rows": ["обновлённый файл"], "note": "сохранение"},
    ], caption="Загрузить → добавить → отсортировать → сохранить — типичный конвейер персистентных данных.")}
    {code_block(
        "tablitsa_rekordov.py",
        'import csv\n'
        'from pathlib import Path\n\n'
        'def load_rekordy(path: Path) -> list[dict]:\n'
        "    if not path.exists():\n"
        "        return []\n"
        '    with path.open("r", encoding="utf-8", newline="") as f:\n'
        "        reader = csv.DictReader(f)\n"
        '        return [{"name": row["name"], "score": int(row["score"])} for row in reader]\n\n'
        'def save_rekordy(path: Path, rekordy: list[dict]) -> None:\n'
        '    with path.open("w", encoding="utf-8", newline="") as f:\n'
        '        writer = csv.DictWriter(f, fieldnames=["name", "score"])\n'
        "        writer.writeheader()\n"
        "        writer.writerows(rekordy)\n\n"
        'def top_n(rekordy: list[dict], n: int) -> list[dict]:\n'
        '    return sorted(rekordy, key=lambda r: r["score"], reverse=True)[:n]\n\n'
        'path = Path("rekordy.csv")\n'
        "rekordy = load_rekordy(path)\n"
        'rekordy.append({"name": "Carlos", "score": 1500})\n'
        "save_rekordy(path, rekordy)\n\n"
        "for zapis in top_n(rekordy, 3):\n"
        '    print(zapis["name"], zapis["score"])\n',
    )}
    {exercise(2, "Без повторов имени", "Измените load_rekordy/добавление так, чтобы при повторном сохранении результата уже существующего игрока обновлялся его рекорд, а не добавлялась вторая строка с тем же именем.")}
    {exercise(3, "На JSON вместо CSV", "Перепишите тот же проект так, чтобы rekordy.csv стал rekordy.json — сравните, что изменилось в load/save, а что осталось прежним (сортировка, top_n).")}

    {practice_card(
        "15-29",
        "Практика: таблица рекордов",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-29/index.html",
    )}
    """
    page(
        "15-29-mini-proekt-rekordy-i-nastrojki.html",
        page_title="Мини-проект: таблица рекордов",
        description="Полный конвейер персистентных данных на CSV — загрузить, добавить запись, отсортировать, сохранить, — собирающий вместе файлы, списки, словари и функции.",
        kicker_suffix="Мини-проект: рекорды",
        h1="Мини-проект: таблица рекордов",
        lede="Загрузить → изменить → сохранить — рабочий цикл почти любой персистентной программы.",
        body_html=body,
    )


def build_30() -> None:
    body = f"""
    <h2>Две разные файловые системы</h2>
    <p>Практики этого курса выполняются в браузере через Pyodide — настоящий Python, но
    работающий внутри веб-страницы, а не как обычная программа на вашем компьютере.</p>
    {callout(
        "warning",
        "[[icon:warning]] Файлы в браузерной практике — не файлы на вашем компьютере",
        "Когда практика этого курса выполняет <code class=\"inline\">Path(\"hello.txt\")."
        "write_text(...)</code>, поведение <code class=\"inline\">open</code>/<code "
        "class=\"inline\">pathlib</code> настоящее — запись, чтение и дозапись работают по "
        "реальным правилам. Но сам файл существует только во <strong>временной файловой "
        "системе Python внутри этой вкладки браузера</strong>. Он не появляется в <code "
        "class=\"inline\">~/Downloads</code>, не виден в проводнике/Finder и исчезает при "
        "нажатии «Сбросить среду» или закрытии вкладки.",
    )}

    {pipeline_diagram([
        {"kind": "object", "title": "код практики", "rows": ["Path(\"hello.txt\").write_text(...)"]},
        {"kind": "file", "title": "виртуальная ФС Pyodide", "rows": ["существует внутри вкладки браузера"], "note": "запись"},
        {"kind": "plain", "title": "НЕ ваш реальный диск"},
    ], caption="Браузерная практика пишет в виртуальную файловую систему — не на настоящий диск компьютера.")}

    {debug_lab(
        14,
        "Файл создан в Pyodide, но его нет на диске",
        "putanitsa_fs.py",
        '# выполнено ВНУТРИ браузерной практики курса\n'
        'from pathlib import Path\n\n'
        'Path("moy_fajl.txt").write_text("привет", encoding="utf-8")\n'
        '# ожидание: "теперь этот файл лежит у меня на компьютере"\n',
        [
            "# Файл действительно создан и читаем внутри этой вкладки браузера —",
            "# но его нет ни в проводнике/Finder, ни в реальной домашней папке.",
        ],
        "Виртуальная файловая система Pyodide полностью реальна для самой программы внутри "
        "вкладки — но она изолирована от настоящего диска компьютера. Путать «файл создан "
        "программой» с «файл появился на моём компьютере» — источник путаницы именно в браузерных "
        "средах выполнения Python.",
        "kak-poluchit-nastoyaschiy-fajl.py",
        '# для файла на настоящем диске — запустите тот же код ЛОКАЛЬНО\n'
        '# (VS Code / PyCharm / Jupyter на вашем компьютере, раздел 15.30)\n'
        'from pathlib import Path\n\n'
        'Path("moy_fajl.txt").write_text("привет", encoding="utf-8")\n',
    )}

    <h2>Когда важна настоящая персистентность на диске</h2>
    <p>Для этого раздела — практика, требующая локального запуска: настоящего файла на настоящем
    диске, который переживёт даже закрытие редактора.</p>
    {local_required_card(
        "15-30",
        "Практика: настоящая персистентность на вашем компьютере",
        "Локальная практика — скачайте .ipynb и выполните его в VS Code/PyCharm/Jupyter",
        "../../practice/15-30/index.html",
    )}
    <ol>
      <li>Скачайте ноутбук этого раздела и откройте его локально (VS Code, PyCharm или Jupyter).</li>
      <li>Выполните ячейку, создающую папку <code class="inline">data/</code> и записывающую в
        неё UTF-8-файл.</li>
      <li>Остановите выполнение (или закройте редактор).</li>
      <li>Откройте файл в проводнике/Finder или в самом редакторе — убедитесь, что он на месте.</li>
      <li>Запустите ноутбук ещё раз и прочитайте тот же файл — данные из первого запуска на
        месте, потому что это настоящий файл на настоящем диске.</li>
    </ol>
    """
    page(
        "15-30-brauzer-vs-lokalny-disk.html",
        page_title="Браузер и локальный диск: две файловые системы",
        description="Файлы, созданные браузерной практикой на Pyodide, живут в виртуальной файловой системе внутри вкладки — а не на настоящем диске компьютера; локальная практика показывает разницу на деле.",
        kicker_suffix="Браузер vs локальный диск",
        h1="Браузер и локальный диск: две файловые системы",
        lede="\"Файл создан\" и \"файл появился на моём компьютере\" — не всегда одно и то же.",
        body_html=body,
    )


def build_31() -> None:
    body = f"""
    <h2>Инструментарий работы с файлами</h2>
    {decision_map(
        [
            ("Нужен путь", "pathlib.Path"),
            ("Нужна текущая рабочая директория", "Path.cwd()"),
            ("Нужна папка рядом со своим .py-файлом", "Path(__file__).resolve().parent"),
            ("Небольшой UTF-8-текстовый файл целиком", "path.read_text() / write_text()"),
            ("Построчная обработка или особый режим", "with path.open(режим, encoding=\"utf-8\")"),
            ("Дозапись без потери старого содержимого", "open(путь, \"a\", ...)"),
            ("Создать, но не заменить существующий файл", "open(путь, \"x\", ...)"),
            ("Бинарные данные целиком", "path.read_bytes() / write_bytes()"),
            ("Список содержимого папки", "path.iterdir()"),
            ("Поиск файлов по шаблону", "path.glob(\"*.txt\")"),
            ("Вложенная структура данных", "модуль json"),
            ("Таблица со строками и столбцами", "модуль csv"),
            ("Много пользователей / транзакции", "вероятно, база данных — не простой файл"),
        ],
        title="Что выбрать для конкретной задачи",
    )}

    {capability_map([
        ("Персистентность", ["память процесса — временна", "устойчивое хранилище переживает завершение процесса", "загрузка ≠ тот же объект"]),
        ("Файловая система", ["файл vs папка", "абсолютный vs относительный путь", "CWD ≠ папка со скриптом"]),
        ("pathlib.Path", ["путь как объект", "name / stem / suffix / parent", "read_text/write_text/read_bytes/write_bytes"]),
        ("Файл и with", ["open() → объект файла", "with гарантирует закрытие", "курсор двигается вперёд, tell()/seek()"]),
        ("Текст и байты", ["str кодируется в bytes", "UTF-8 — явный выбор курса", "символы ≠ байты"]),
        ("Структурированные данные", ["JSON — вложенные структуры", "CSV — таблицы, не split(\",\")", "безопасное сохранение — temp → replace"]),
    ], title="Глава 15 целиком")}

    {tree_diagram(
        ("Работа с файлами", [
            ("Персистентность", [("память временна", []), ("хранилище переживает завершение процесса", [])]),
            ("Пути", [("абсолютные и относительные", []), ("CWD", []), ("pathlib.Path", [])]),
            ("Файл", [("open/with", []), ("курсор, tell/seek", []), ("режимы r/w/a/x", [])]),
            ("Текст и байты", [("str/bytes", []), ("UTF-8", [])]),
            ("Структурированные данные", [("JSON", []), ("CSV", [])]),
        ]),
        caption="Карта главы 15 целиком.",
    )}

    <h2>Что дальше</h2>
    {pipeline_diagram([
        {"kind": "plain", "title": "Глава 16: Tkinter-приложение"},
        {"kind": "object", "title": "load_settings() / save_settings()", "note": "использует то, что мы уже умеем"},
        {"kind": "file", "title": "settings.json"},
    ], caption="Персистентность, освоенная в этой главе, становится памятью будущего графического приложения.")}
    <p>В главе 16 («Создаём классные приложения с Tkinter») мы построим первое настоящее
    графическое приложение — и оно сможет запоминать настройки пользователя между запусками
    именно через <code class="inline">load_settings()</code>/<code
    class="inline">save_settings()</code> из раздела 15.25, без единой новой строчки про файлы.</p>

    {summary_box("Что мы узнали в этой главе", [
        "Объекты Python живут в памяти процесса и не переживают его завершение — данные в устойчивом файловом хранилище могут пережить завершение процесса.",
        "Путь — не содержимое файла: <code class=\"inline\">Path(...)</code> лишь ссылается на место в файловой системе.",
        "Относительный путь разрешается относительно текущей рабочей директории (CWD) — а не папки со скриптом.",
        "<code class=\"inline\">pathlib.Path</code> — путь как объект: name/stem/suffix/parent и удобные методы вместо ручной сборки строк.",
        "<code class=\"inline\">open()</code> возвращает объект файла; <code class=\"inline\">with</code> гарантирует его закрытие даже при ошибке.",
        "У файла есть курсор — позиция чтения/записи, которая двигается вперёд и не возвращается сама; для этого есть <code class=\"inline\">seek()</code>.",
        "Режимы <code class=\"inline\">r/w/a/x</code> — разный риск для существующего содержимого; <code class=\"inline\">\"w\"</code> стирает файл уже при открытии.",
        "Текст кодируется в байты — всегда явно указывайте <code class=\"inline\">encoding=\"utf-8\"</code>, не полагайтесь на кодировку по умолчанию.",
        "JSON сохраняет вложенные структуры Python; CSV — таблицы; ни split(\",\"), ни str(словарь) не заменяют настоящий формат сериализации.",
        "Файлы браузерной практики (Pyodide) — не файлы на вашем реальном компьютере.",
    ])}
    """
    out = render_page(
        page_title="Итоги главы: инструментарий работы с файлами",
        description="Итоги главы 15: инструментарий работы с файлами, картой решений и мостиком к персистентным настройкам главы 16.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 15", "index.html"), ("Итоги главы", "")],
        kicker="Глава 15 · Python и файлы",
        h1="Итоги главы: инструментарий работы с файлами",
        lede="От «куда пропадают переменные» до JSON, CSV и настоящей персистентности — полная карта главы.",
        body_html=body,
        sidebar_groups=sidebar("15-31-itogi-glavy.html"),
        nav=nav_for("15-31-itogi-glavy.html"),
    )
    write("15-31-itogi-glavy.html", out)


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
    build_11()
    build_12()
    build_13()
    build_14()
    build_15()
    build_16()
    build_17()
    build_18()
    build_19()
    build_20()
    build_21()
    build_22()
    build_23()
    build_24()
    build_25()
    build_26()
    build_27()
    build_28()
    build_29()
    build_30()
    build_31()
