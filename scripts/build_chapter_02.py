#!/usr/bin/env python3
"""Строит Главу 2: «Давайте установим Python!» (site/chapters/glava-02/)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_lib import (
    ChapterSectionLink,
    NavItem,
    PageNav,
    SidebarGroup,
    callout,
    flow_diagram,
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-02"

PAGES = [
    ("index.html", "Приступаем"),
    ("02-01-govorim-na-yazyke-kompyutera.html", "Говорим на языке компьютера"),
    ("02-02-windows.html", "Установка на Windows"),
    ("02-03-mac.html", "Установка на Mac"),
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


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=2,
        baseline_page=13,
        title="Давайте установим Python!",
        description="Устанавливаем настоящий Python 3.14 на Windows или Mac — шаг за шагом, с проверкой в терминале.",
        meta_items=["⏱ ~20 минут", "💻 Windows или macOS", "🔧 без ноутбука практики — тут мы готовим инструменты"],
        sections=[
            ChapterSectionLink("2.1", "Говорим на языке компьютера", "02-01-govorim-na-yazyke-kompyutera.html", "13"),
            ChapterSectionLink("2.2", "Установка Python на компьютере с Windows", "02-02-windows.html", "14"),
            ChapterSectionLink("2.3", "Установка Python на устройстве Mac", "02-03-mac.html", "18"),
            ChapterSectionLink("", "Итоги", "02-03-mac.html#itogi", "25"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    diagram = flow_diagram(
        [
            ("Скачать", "python.org"),
            ("Установить", "запустить мастер установки"),
            ("Проверить", "python --version в терминале"),
        ],
        caption="Общая схема установки — детали различаются для Windows и Mac",
    )

    body = f"""
    <h2>Начало работы — устанавливаем Python</h2>
    <p>Когда вы устанавливаете Python, вы устанавливаете <strong>интерпретатор</strong> — программу,
    которая умеет читать и выполнять код на Python (напомним: об этом шла речь в главе 1). После
    установки ваш компьютер начинает «понимать» файлы с расширением <code class="inline">.py</code>
    и команду <code class="inline">python</code> в терминале.</p>

    {diagram}

    <p>Шаги отличаются в зависимости от операционной системы — выберите свою:</p>
    <ul>
      <li><a href="02-02-windows.html">Установка на Windows →</a></li>
      <li><a href="02-03-mac.html">Установка на Mac →</a></li>
    </ul>

    {callout(
        "security",
        "Скачивайте только с python.org",
        "Официальный установщик — единственный источник, которому стоит доверять. Сайты-двойники "
        "и «ускоренные» установщики с других сайтов иногда добавляют в систему нежелательные "
        "программы. В этой книге мы всегда используем только "
        "<a href=\"https://www.python.org/downloads/\" target=\"_blank\" rel=\"noopener\">python.org/downloads</a>.",
    )}

    {callout(
        "info",
        "Зачем именно 3.14?",
        "Python постоянно развивается. Версия 3.14 — самая новая стабильная версия на момент "
        "написания этой книги, и весь код в ней рассчитан именно на неё. Более старая версия "
        "(например, 3.9 или 3.10) в большинстве случаев тоже подойдёт для базовых глав, но "
        "несколько современных примеров в книге её потребуют.",
    )}
    """

    out = render_page(
        page_title="Говорим на языке компьютера",
        description="Что происходит при установке Python и откуда его безопасно скачать.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("Говорим на языке компьютера", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="Говорим на языке компьютера",
        lede="Прежде чем писать код, компьютеру нужно «выучить» Python — то есть получить "
        "интерпретатор, который умеет его понимать.",
        body_html=body,
        sidebar_groups=sidebar("02-01-govorim-na-yazyke-kompyutera.html"),
        nav=PageNav(prev_href="index.html", prev_label="Приступаем", next_href="02-02-windows.html", next_label="Установка на Windows"),
    )
    write("02-01-govorim-na-yazyke-kompyutera.html", out)


def build_02_windows() -> None:
    body = f"""
    <h2>Скачивание Python</h2>
    <ol>
      <li>Откройте в браузере <a href="https://www.python.org/downloads/windows/" target="_blank" rel="noopener">python.org/downloads/windows</a>.</li>
      <li>Найдите самую свежую версию 3.14.x и нажмите на ссылку
        <strong>«Windows installer (64-bit)»</strong>. Почти все современные компьютеры на Windows
        — 64-битные; если сомневаетесь, эта версия почти наверняка подойдёт.</li>
      <li>Дождитесь, пока файл вида <code class="inline">python-3.14.x-amd64.exe</code> загрузится
        в папку «Загрузки».</li>
    </ol>

    <h2>Установка Python</h2>
    <ol>
      <li>Запустите скачанный файл двойным щелчком.</li>
      <li>На первом экране мастера установки обязательно поставьте галочку
        <strong>«Add python.exe to PATH»</strong> внизу окна. Это самый важный шаг: PATH — список
        папок, где Windows ищет программы по имени. Без этой галочки команда
        <code class="inline">python</code> в терминале не будет найдена.</li>
      <li>Нажмите <strong>«Install Now»</strong> и дождитесь завершения установки.</li>
      <li>На последнем экране нажмите <strong>«Close»</strong>.</li>
    </ol>

    {callout(
        "warning",
        "Забыли галочку PATH?",
        "Не страшно — запустите установщик заново, выберите «Modify», затем на шаге "
        "«Advanced Options» включите «Add Python to environment variables» и завершите установку "
        "повторно.",
    )}

    <h2>Проверка установки</h2>
    <p>Откройте приложение <strong>«Командная строка»</strong> (наберите <em>cmd</em> в поиске
    Windows) и введите:</p>
    <div class="code-block"><div class="code-label"><span>командная строка</span></div>
    <pre><code>python --version</code></pre></div>
    <p>Если вы видите строку вида <code class="inline">Python 3.14.x</code> — Python установлен и
    готов к работе. Переходите к главе 3.</p>
    """

    out = render_page(
        page_title="Установка Python на Windows",
        description="Пошаговая установка Python 3.14 на Windows: скачивание, PATH, проверка через python --version.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("Установка на Windows", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="Установка Python на компьютере с Windows",
        lede="Три коротких шага: скачать официальный установщик, поставить галочку PATH и "
        "проверить результат в командной строке.",
        body_html=body,
        sidebar_groups=sidebar("02-02-windows.html"),
        nav=PageNav(prev_href="02-01-govorim-na-yazyke-kompyutera.html", prev_label="Говорим на языке компьютера", next_href="02-03-mac.html", next_label="Установка на Mac"),
    )
    write("02-02-windows.html", out)


def build_03_mac() -> None:
    body = f"""
    <h2>Скачивание Python</h2>
    <ol>
      <li>Откройте в браузере <a href="https://www.python.org/downloads/macos/" target="_blank" rel="noopener">python.org/downloads/macos</a>.</li>
      <li>Найдите самую свежую версию 3.14.x и нажмите на ссылку
        <strong>«macOS 64-bit universal2 installer»</strong> — этот установщик подходит и для
        Mac с процессором Apple Silicon (M1/M2/M3/M4), и для Mac с процессором Intel.</li>
      <li>Дождитесь, пока файл вида <code class="inline">python-3.14.x-macos11.pkg</code>
        загрузится в папку «Загрузки».</li>
    </ol>

    <h2>Установка Python</h2>
    <ol>
      <li>Откройте скачанный файл <code class="inline">.pkg</code> двойным щелчком.</li>
      <li>Пройдите шаги мастера установки — «Введение», «Лицензия», «Место установки» — нажимая
        «Продолжить». Настройки по умолчанию подходят для этой книги, менять их не нужно.</li>
      <li>На шаге «Тип установки» нажмите «Установить» и введите пароль своей учётной записи
        Mac, когда система попросит подтверждение.</li>
      <li>Дождитесь надписи «Установка прошла успешно» и закройте окно.</li>
    </ol>

    {callout(
        "info",
        "На Mac уже есть Python — но не тот",
        "На некоторых Mac предустановлена очень старая версия Python 2 для внутренних нужд "
        "системы. Не используйте её — после установки с python.org в системе появится отдельная,"
        " современная команда <code class=\"inline\">python3</code>, именно её мы и будем "
        "использовать.",
    )}

    <h2>Проверка установки</h2>
    <p>Откройте приложение <strong>«Терминал»</strong> (Programs → Utilities → Terminal, либо
    через поиск Spotlight) и введите:</p>
    <div class="code-block"><div class="code-label"><span>терминал</span></div>
    <pre><code>python3 --version</code></pre></div>
    <p>Если вы видите строку вида <code class="inline">Python 3.14.x</code> — всё готово.</p>

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
        "Установка Python — это установка <strong>интерпретатора</strong>, который умеет "
        "выполнять код на Python.",
        "Официальный и безопасный источник — только <strong>python.org</strong>.",
        "На Windows критически важно включить галочку <strong>«Add python.exe to PATH»</strong>.",
        "На Mac команда для запуска — <strong>python3</strong>, а не <code class=\"inline\">"
        "python</code>.",
        "Проверить установку можно одной командой: <code class=\"inline\">python --version</code> "
        "(Windows) или <code class=\"inline\">python3 --version</code> (Mac).",
    ])}
    """

    out = render_page(
        page_title="Установка Python на Mac",
        description="Пошаговая установка Python 3.14 на macOS: скачивание universal2-установщика, установка, проверка через python3 --version.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 2", "index.html"), ("Установка на Mac", "")],
        kicker="Глава 2 · Давайте установим Python!",
        h1="Установка Python на устройстве Mac",
        lede="Тот же принцип, что и на Windows, но с учётом особенностей macOS — и краткие итоги "
        "главы.",
        body_html=body,
        sidebar_groups=sidebar("02-03-mac.html"),
        nav=PageNav(prev_href="02-02-windows.html", prev_label="Установка на Windows", next_href="../glava-03/index.html", next_label="Глава 3: Ваша первая программа на Python"),
    )
    write("02-03-mac.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01()
    build_02_windows()
    build_03_mac()
