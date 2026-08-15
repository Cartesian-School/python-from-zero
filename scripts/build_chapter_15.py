#!/usr/bin/env python3
"""Строит Главу 15: «Python и файлы» (site/chapters/glava-15/)."""

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
OUT_DIR = ROOT / "site" / "chapters" / "glava-15"

PAGES = [
    ("index.html", "Обзор главы"),
    ("15-01-zachem-fajly.html", "Зачем нужны файлы? Открытие и чтение"),
    ("15-02-stroka-za-strokoj.html", "Строка за строкой"),
    ("15-03-sozdanie-fajlov.html", "Создание новых файлов"),
    ("15-04-mini-proekt-itogi.html", "Мини-проект: знакомство с файлами и итоги"),
]

LESSON_IDS = ["15-01", "15-02", "15-03", "15-04"]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 15 · Файлы", items),
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
        chapter_num=15,
        baseline_page=323,
        title="Python и файлы",
        description="Чтение и запись файлов на диске — данные, которые переживают завершение программы.",
        meta_items=["⏱ ~1.5 часа", "📁 open() и pathlib", "📓 4 ноутбука практики"],
        sections=[
            ChapterSectionLink("15.1", "Зачем нужны файлы?", "15-01-zachem-fajly.html", "323"),
            ChapterSectionLink("", "Открытие и чтение существующих файлов", "15-01-zachem-fajly.html#otkrytie", "324"),
            ChapterSectionLink("15.2", "Строка за строкой", "15-02-stroka-za-strokoj.html", "328"),
            ChapterSectionLink("15.3", "Создание новых файлов", "15-03-sozdanie-fajlov.html", "330"),
            ChapterSectionLink("", "Работа с файлами", "15-03-sozdanie-fajlov.html#rabota", "330"),
            ChapterSectionLink("15.4", "Мини-проект — знакомство с файлами", "15-04-mini-proekt-itogi.html", "332"),
            ChapterSectionLink("", "Итоги", "15-04-mini-proekt-itogi.html#itogi", "333"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <h2>Зачем нужны файлы?</h2>
    <p>Все переменные вашей программы исчезают, как только программа завершается. Чтобы
    сохранить данные — список результатов игры, текст, настройки — между запусками программы,
    их нужно записать в <strong>файл</strong> на диске.</p>

    <h2 id="otkrytie">Открытие и чтение существующих файлов</h2>
    {code_block(
        "chtenie_fajla.py",
        'file = open("privet.txt", "r")   # "r" — режим чтения (read)\n'
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
        'file = open("privet.txt", "r")\n'
        "content = file.read()\n"
        "print(content)\n"
        "file.close()   # легко забыть!",
        "Современный Python (with)",
        'with open("privet.txt", "r") as file:\n'
        "    content = file.read()\n"
        "    print(content)\n"
        "# файл закроется САМ, даже если внутри блока произойдёт ошибка",
        "<code class=\"inline\">with</code> — он существует в Python с версии 2.5, так что "
        "дело не в новизне, а в надёжности: файл закроется автоматически при выходе из блока "
        "<code class=\"inline\">with</code>, даже если внутри что-то пойдёт не так. Начиная с "
        "этой главы в книге мы используем именно <code class=\"inline\">with</code>.",
    )}

    {practice_card(
        "15-01",
        "Практика: чтение файлов через with",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-01/index.html",
    )}
    """
    out = render_page(
        page_title="Зачем нужны файлы? Открытие и чтение",
        description="Файлы как способ сохранить данные между запусками программы; open(), read(), менеджер контекста with.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 15", "index.html"), ("Зачем файлы?", "")],
        kicker="Глава 15 · Python и файлы",
        h1="Зачем нужны файлы?",
        lede="Переменные исчезают вместе с программой — файлы позволяют сохранить данные "
        "надолго.",
        body_html=body,
        sidebar_groups=sidebar("15-01-zachem-fajly.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="15-02-stroka-za-strokoj.html", next_label="Строка за строкой"),
    )
    write("15-01-zachem-fajly.html", out)


def build_02() -> None:
    body = f"""
    <p>Читать весь файл сразу одним куском не всегда удобно — особенно если файл большой.
    Часто нужнее обработать его <strong>построчно</strong>:</p>
    {code_block(
        "stroka_za_strokoj.py",
        'with open("spisok.txt", "r") as file:\n'
        "    for line in file:\n"
        "        print(line.strip())   # strip() убирает лишний перевод строки\n",
    )}
    {callout(
        "tip",
        "Зачем нужен strip()",
        "Каждая строка файла, кроме, возможно, последней, заканчивается невидимым символом "
        "перевода строки <code class=\"inline\">\\n</code>. <code class=\"inline\">.strip()</code> "
        "(глава 8) убирает его, чтобы не было лишних пустых строк при выводе.",
    )}

    <h2>Все строки сразу — списком</h2>
    {code_block(
        "readlines.py",
        'with open("spisok.txt", "r") as file:\n'
        "    lines = file.readlines()\n\n"
        'print(len(lines), "строк")\n'
        "print(lines[0])   # первая строка\n",
    )}

    {practice_card(
        "15-02",
        "Практика: построчное чтение файлов",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-02/index.html",
    )}
    """
    out = render_page(
        page_title="Строка за строкой",
        description="Построчное чтение файлов в Python: цикл по файлу и readlines().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 15", "index.html"), ("Строка за строкой", "")],
        kicker="Глава 15 · Python и файлы",
        h1="Строка за строкой",
        lede="Часто удобнее обработать файл по одной строке за раз, а не целиком.",
        body_html=body,
        sidebar_groups=sidebar("15-02-stroka-za-strokoj.html"),
        nav=PageNav(prev_href="15-01-zachem-fajly.html", prev_label="Зачем файлы?", next_href="15-03-sozdanie-fajlov.html", next_label="Создание новых файлов"),
    )
    write("15-02-stroka-za-strokoj.html", out)


def build_03() -> None:
    body = f"""
    <h2>Создание новых файлов</h2>
    <p>Чтобы записать что-то в файл, откройте его в режиме записи
    <code class="inline">"w"</code> (write) — если файла не существует, Python создаст его сам;
    если существует — его прежнее содержимое будет стёрто:</p>
    {code_block(
        "zapis_fajla.py",
        'with open("rezultaty.txt", "w") as file:\n'
        '    file.write("Уровень 1: 100 очков\\n")\n'
        '    file.write("Уровень 2: 250 очков\\n")\n',
    )}

    <h2 id="rabota">Работа с файлами</h2>
    <p>Три основных режима открытия файла:</p>
    <ul>
      <li><code class="inline">"r"</code> — чтение (read); ошибка, если файла не существует.</li>
      <li><code class="inline">"w"</code> — запись (write); создаёт новый файл или полностью
        стирает существующий.</li>
      <li><code class="inline">"a"</code> — дозапись (append); добавляет текст в конец файла, не
        стирая то, что уже есть.</li>
    </ul>
    {code_block("dozapis.py", 'with open("rezultaty.txt", "a") as file:\n    file.write("Уровень 3: 400 очков\\n")\n')}

    <h2>Пути к файлам: строка или pathlib</h2>
    {classic_vs_modern(
        "Путь к файлу: обычная строка → pathlib",
        "Классический подход",
        'file_path = "data/rezultaty.txt"\n'
        "with open(file_path, \"r\") as f:\n"
        "    print(f.read())",
        "Современный Python (pathlib)",
        "from pathlib import Path\n\n"
        'file_path = Path("data") / "rezultaty.txt"\n'
        "print(file_path.exists())   # удобные методы прямо у пути\n"
        "with file_path.open(\"r\") as f:\n"
        "    print(f.read())",
        "<code class=\"inline\">pathlib</code> для путей к файлам — он появился в Python 3.4 и "
        "с тех пор считается предпочтительным способом. Строковые пути всё ещё повсеместно "
        "работают и встречаются в старом коде, но <code class=\"inline\">pathlib</code> "
        "избавляет от ручной сборки пути через <code class=\"inline\">+</code> и добавляет "
        "полезные методы вроде <code class=\"inline\">.exists()</code> прямо у самого пути.",
    )}

    {practice_card(
        "15-03",
        "Практика: запись, дозапись и pathlib",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/15-03/index.html",
    )}
    """
    out = render_page(
        page_title="Создание новых файлов",
        description="Режимы работы с файлами (r, w, a) и современный подход к путям через pathlib.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 15", "index.html"), ("Создание файлов", "")],
        kicker="Глава 15 · Python и файлы",
        h1="Создание новых файлов",
        lede="Записываем данные на диск — и знакомимся с современным способом работать с "
        "путями.",
        body_html=body,
        sidebar_groups=sidebar("15-03-sozdanie-fajlov.html"),
        nav=PageNav(prev_href="15-02-stroka-za-strokoj.html", prev_label="Строка за строкой", next_href="15-04-mini-proekt-itogi.html", next_label="Мини-проект и итоги"),
    )
    write("15-03-sozdanie-fajlov.html", out)


def build_04() -> None:
    body = f"""
    <p>Соберём чтение и запись в одном небольшом проекте — дневнике заметок, который
    сохраняется между запусками программы.</p>
    {code_block(
        "dnevnik_zametok.py",
        "from pathlib import Path\n\n"
        'fajl_zametok = Path("zametki.txt")\n\n'
        'novaya_zametka = input("Новая заметка: ")\n\n'
        'with fajl_zametok.open("a") as f:\n'
        '    f.write(novaya_zametka + "\\n")\n\n'
        'print("Все заметки:")\n'
        'with fajl_zametok.open("r") as f:\n'
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

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
        "Файлы сохраняют данные между запусками программы — в отличие от обычных переменных.",
        "<code class=\"inline\">with open(путь, режим) as file:</code> — современный и "
        "безопасный способ работать с файлами, закрывающий их автоматически.",
        "Режимы: <code class=\"inline\">\"r\"</code> — чтение, <code class=\"inline\">\"w\"</code> "
        "— запись с перезаписью, <code class=\"inline\">\"a\"</code> — дозапись в конец.",
        "Файл можно читать целиком (<code class=\"inline\">.read()</code>), построчно (цикл "
        "<code class=\"inline\">for line in file</code>) или списком строк "
        "(<code class=\"inline\">.readlines()</code>).",
        "<code class=\"inline\">pathlib.Path</code> — современный способ работать с путями к "
        "файлам вместо голых строк.",
    ])}
    """
    out = render_page(
        page_title="Мини-проект — знакомство с файлами",
        description="Итоговый мини-проект главы 15: дневник заметок, сохраняющийся между запусками — и краткие итоги.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 15", "index.html"), ("Мини-проект и итоги", "")],
        kicker="Глава 15 · Python и файлы",
        h1="Мини-проект — знакомство с файлами",
        lede="Дневник заметок, сохраняющийся между запусками программы, — и подведение итогов "
        "главы.",
        body_html=body,
        sidebar_groups=sidebar("15-04-mini-proekt-itogi.html"),
        nav=PageNav(prev_href="15-03-sozdanie-fajlov.html", prev_label="Создание файлов", next_href="../glava-16/index.html", next_label="Глава 16: Создаём классные приложения с Tkinter"),
    )
    write("15-04-mini-proekt-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01()
    build_02()
    build_03()
    build_04()
