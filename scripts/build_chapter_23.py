#!/usr/bin/env python3
"""Строит Главу 23: «Первый проект на GitHub: SafeSort» (site/chapters/glava-23/).

Основной путь главы — один проект SafeSort, доведённый от идеи до релиза
(22-01..23-32 — исторический номер главы 23 сохранён, но нумерация страниц
здесь своя, с 01 по 32). Шесть исторических мини-проектов, ранее бывших
основным содержанием главы, перенесены в приложение — «Дополнительная
практика: шесть мини-проектов для GitHub» — и сохраняют свои прежние
идентификаторы практики (23-01..23-06). Старые URL этих мини-проектов
сохранены как страницы-указатели на новое место (см. build_legacy_redirect).
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
    code_block,
    comparison_table,
    decision_map,
    exercise,
    flow_diagram,
    image_figure,
    local_required_card,
    practice_card,
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-23"
IMG = "../../assets/img/chapter-23/output"

# --- Основной путь главы: SafeSort, от идеи до релиза -----------------------
PAGES = [
    ("index.html", "Обзор главы"),
    ("23-01-ideya-trebovaniya.html", "От идеи к требованиям проекта"),
    ("23-02-repozitorij.html", "Создаём репозиторий проекта"),
    ("23-03-readme.html", "Первый README проекта"),
    ("23-04-struktura-paketa.html", "Планируем структуру Python-пакета"),
    ("23-05-pyproject-toml.html", "pyproject.toml и установка проекта"),
    ("23-06-komandnaya-stroka.html", "Командная строка SafeSort"),
    ("23-07-pathlib.html", "pathlib: работаем с путями и каталогами"),
    ("23-08-skaniruem-katalog.html", "Сканируем каталог"),
    ("23-09-isklyucheniya.html", "Какие каталоги не нужно сканировать"),
    ("23-10-klassifikaciya.html", "Определяем категорию файла"),
    ("23-11-plan-dejstvij.html", "От анализа к плану действий"),
    ("23-12-predvaritelnyj-prosmotr.html", "Режим предварительного просмотра"),
    ("23-13-peremeshaem-fajly.html", "Безопасно перемещаем файлы"),
    ("23-14-imya-zanyato.html", "Что делать, если имя уже занято"),
    ("23-15-zhurnal-operacij.html", "Журнал выполненных операций"),
    ("23-16-otmena-operacii.html", "Отмена последней операции"),
    ("23-17-poisk-dublikatov.html", "Поиск одинаковых файлов"),
    ("23-18-sha256.html", "SHA-256 и хеш содержимого файла"),
    ("23-19-gruppy-dublikatov.html", "Находим группы дубликатов"),
    ("23-20-oshibki-fajlovoj-sistemy.html", "Обрабатываем ошибки файловой системы"),
    ("23-21-logging.html", "Добавляем журнал работы программы"),
    ("23-22-nastrojki-proekta.html", "Настройки проекта"),
    ("23-23-pervye-testy.html", "Пишем первые автоматические тесты"),
    ("23-24-testy-skanirovaniya.html", "Проверяем сканирование и классификацию"),
    ("23-25-testy-peremeshheniya.html", "Проверяем перемещение и отмену"),
    ("23-26-testy-dublikatov.html", "Проверяем поиск дубликатов"),
    ("23-27-testy-cli.html", "Проверяем интерфейс командной строки"),
    ("23-28-git-kommit.html", "Git: от рабочего изменения к коммиту"),
    ("23-29-github-pr.html", "GitHub: Issue, ветка и Pull Request"),
    ("23-30-github-actions.html", "GitHub Actions: автоматически запускаем тесты"),
    ("23-31-versiya-reliz.html", "Документация, версия и первый релиз"),
    ("23-32-itogi-reliz.html", "Итоги: полный путь проекта от идеи до релиза"),
]

# --- Приложение: шесть мини-проектов для домашней практики -------------------
HOMEWORK_PAGES = [
    ("23-hw-index.html", "Дополнительная практика: шесть мини-проектов для GitHub"),
    ("23-hw-01-kalkulyator.html", "Домашний проект A: калькулятор с Tkinter"),
    ("23-hw-02-generator-istorij.html", "Домашний проект B: генератор случайных историй"),
    ("23-hw-03-kamen-nozhnicy-bumaga.html", "Домашний проект C: «Камень, ножницы, бумага»"),
    ("23-hw-04-otskakivayushie-myachi.html", "Домашний проект D: отскакивающие мячи с Pygame"),
    ("23-hw-05-temperatura.html", "Домашний проект E: преобразование температуры"),
    ("23-hw-06-zametki.html", "Домашний проект F: приложение «Заметки»"),
]

# Старые URL шести мини-проектов (существовали до этой перестройки главы) —
# сохраняются как отдельные, короткие страницы-указатели на новое место.
# Не входят в PAGES: это не часть основного содержания, а только
# совместимость со старыми ссылками, поэтому книжные EPUB/PDF (которые
# читают PAGES) их не увидят.
LEGACY_REDIRECTS = [
    ("23-01-kalkulyator.html", "23-hw-01-kalkulyator.html", "Домашний проект A: калькулятор с Tkinter"),
    ("23-02-generator-istorij.html", "23-hw-02-generator-istorij.html", "Домашний проект B: генератор случайных историй"),
    ("23-03-kamen-nozhnicy-bumaga.html", "23-hw-03-kamen-nozhnicy-bumaga.html", "Домашний проект C: «Камень, ножницы, бумага»"),
    ("23-04-otskakivayushij-myach.html", "23-hw-04-otskakivayushie-myachi.html", "Домашний проект D: отскакивающие мячи с Pygame"),
    ("23-05-temperatura.html", "23-hw-05-temperatura.html", "Домашний проект E: преобразование температуры"),
    ("23-06-fajly-tkinter-itogi.html", "23-hw-06-zametki.html", "Домашний проект F: приложение «Заметки»"),
]

# lesson_id -> имя ноутбука для практик SafeSort (browser-pyodide и
# local-required вперемешку — см. manifest/practice_manifest.json).
SAFESORT_LESSON_IDS = [f"23-{n:02d}" for n in range(7, 25)]  # 23-07..23-24
HOMEWORK_LESSON_IDS = [f"23-{n:02d}" for n in range(1, 7)]  # 23-01..23-06 (сохранены)


def sidebar(active_href: str) -> list[SidebarGroup]:
    main_items = [NavItem(title, href) for href, title in PAGES]
    hw_items = [NavItem(title, href) for href, title in HOMEWORK_PAGES]
    for it in main_items + hw_items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 23 · SafeSort", main_items),
        SidebarGroup("Приложение · Домашняя практика", hw_items),
        SidebarGroup(
            "Практика: SafeSort",
            [NavItem(f"[[icon:practice]] {lid}: Практика", f"../../practice/{lid}/index.html") for lid in SAFESORT_LESSON_IDS],
        ),
        SidebarGroup(
            "Практика: домашние проекты",
            [NavItem(f"[[icon:practice]] {lid}: Практика", f"../../practice/{lid}/index.html") for lid in HOMEWORK_LESSON_IDS],
        ),
        SidebarGroup(
            "Исходный код",
            [
                NavItem("[[icon:code]] projects/python/safesort/", "../../../projects/python/safesort/README.md"),
                NavItem("[[icon:code]] python-mini-projects", "https://github.com/Cartesian-School/python-mini-projects"),
            ],
        ),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text("\n".join(line.rstrip() for line in html_out.split("\n")), encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=23,
        baseline_page=511,
        title="Первый проект на GitHub: SafeSort",
        description="От идеи и структуры репозитория до работающей программы, автоматических тестов, GitHub Actions и первого релиза.",
        meta_items=["[[icon:timer]] ~10-14 часов", "[[icon:architecture]] один проект от идеи до релиза", "[[icon:practice]] 20 практик + приложение"],
        sections=[
            ChapterSectionLink("23.1", "От идеи к требованиям проекта", "23-01-ideya-trebovaniya.html"),
            ChapterSectionLink("23.2", "Создаём репозиторий проекта", "23-02-repozitorij.html"),
            ChapterSectionLink("23.3", "Первый README проекта", "23-03-readme.html"),
            ChapterSectionLink("23.4", "Планируем структуру Python-пакета", "23-04-struktura-paketa.html"),
            ChapterSectionLink("23.5", "pyproject.toml и установка проекта", "23-05-pyproject-toml.html"),
            ChapterSectionLink("23.6", "Командная строка SafeSort", "23-06-komandnaya-stroka.html"),
            ChapterSectionLink("23.7", "pathlib: работаем с путями и каталогами", "23-07-pathlib.html"),
            ChapterSectionLink("23.8", "Сканируем каталог", "23-08-skaniruem-katalog.html"),
            ChapterSectionLink("23.9", "Какие каталоги не нужно сканировать", "23-09-isklyucheniya.html"),
            ChapterSectionLink("23.10", "Определяем категорию файла", "23-10-klassifikaciya.html"),
            ChapterSectionLink("23.11", "От анализа к плану действий", "23-11-plan-dejstvij.html"),
            ChapterSectionLink("23.12", "Режим предварительного просмотра", "23-12-predvaritelnyj-prosmotr.html"),
            ChapterSectionLink("23.13", "Безопасно перемещаем файлы", "23-13-peremeshaem-fajly.html"),
            ChapterSectionLink("23.14", "Что делать, если имя уже занято", "23-14-imya-zanyato.html"),
            ChapterSectionLink("23.15", "Журнал выполненных операций", "23-15-zhurnal-operacij.html"),
            ChapterSectionLink("23.16", "Отмена последней операции", "23-16-otmena-operacii.html"),
            ChapterSectionLink("23.17", "Поиск одинаковых файлов", "23-17-poisk-dublikatov.html"),
            ChapterSectionLink("23.18", "SHA-256 и хеш содержимого файла", "23-18-sha256.html"),
            ChapterSectionLink("23.19", "Находим группы дубликатов", "23-19-gruppy-dublikatov.html"),
            ChapterSectionLink("23.20", "Обрабатываем ошибки файловой системы", "23-20-oshibki-fajlovoj-sistemy.html"),
            ChapterSectionLink("23.21", "Добавляем журнал работы программы", "23-21-logging.html"),
            ChapterSectionLink("23.22", "Настройки проекта", "23-22-nastrojki-proekta.html"),
            ChapterSectionLink("23.23", "Пишем первые автоматические тесты", "23-23-pervye-testy.html"),
            ChapterSectionLink("23.24", "Проверяем сканирование и классификацию", "23-24-testy-skanirovaniya.html"),
            ChapterSectionLink("23.25", "Проверяем перемещение и отмену", "23-25-testy-peremeshheniya.html"),
            ChapterSectionLink("23.26", "Проверяем поиск дубликатов", "23-26-testy-dublikatov.html"),
            ChapterSectionLink("23.27", "Проверяем интерфейс командной строки", "23-27-testy-cli.html"),
            ChapterSectionLink("23.28", "Git: от рабочего изменения к коммиту", "23-28-git-kommit.html"),
            ChapterSectionLink("23.29", "GitHub: Issue, ветка и Pull Request", "23-29-github-pr.html"),
            ChapterSectionLink("23.30", "GitHub Actions: автоматически запускаем тесты", "23-30-github-actions.html"),
            ChapterSectionLink("23.31", "Документация, версия и первый релиз", "23-31-versiya-reliz.html"),
            ChapterSectionLink("23.32", "Итоги: полный путь проекта от идеи до релиза", "23-32-itogi-reliz.html"),
            ChapterSectionLink("", "Приложение: шесть мини-проектов для GitHub", "23-hw-index.html"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <p>Проекты предыдущих глав решали учебную задачу и заканчивались, когда работали
    правильно. SafeSort устроен иначе: это первый проект главы, который доводится до
    состояния, в котором его можно опубликовать на GitHub, установить командой
    <code class="inline">pip install</code> и показать другим людям как часть портфолио.
    Прежде чем писать код, нужно точно сформулировать, что программа обязана делать —
    и, не менее важно, чего она делать не должна.</p>

    <p><strong>SafeSort</strong> — локальная программа командной строки, которая наводит
    порядок в каталоге с файлами: раскладывает их по категориям (документы, изображения,
    архивы и так далее) и находит файлы с одинаковым содержимым. У задачи есть особенность,
    которая определяет всю архитектуру программы: SafeSort работает с настоящими файлами
    пользователя, а значит, ошибка в программе может стоить кому-то реальных данных.</p>

    <h2>Функциональные требования</h2>
    <p>Функциональные требования описывают, что программа должна уметь:</p>
    <ul>
      <li>сканировать каталог и находить в нём файлы;</li>
      <li>классифицировать каждый файл по расширению;</li>
      <li>строить план перемещений, не трогая диск;</li>
      <li>выполнять перемещения только по явной команде;</li>
      <li>находить файлы с одинаковым содержимым;</li>
      <li>отменять последнюю выполненную операцию.</li>
    </ul>

    <h2>Нефункциональные требования</h2>
    <p>Нефункциональные требования описывают не «что», а «как» — свойства, которым должна
    отвечать программа независимо от конкретной команды:</p>
    <ul>
      <li>поведение по умолчанию не должно изменять файлы пользователя;</li>
      <li>программа никогда не перезаписывает существующий файл молча;</li>
      <li>результат работы предсказуем: одинаковый ввод даёт одинаковый план действий;</li>
      <li>вся обработка происходит локально, без сети;</li>
      <li>логику можно проверить автоматическими тестами без реальных файлов пользователя.</li>
    </ul>

    {callout(
        "warning",
        "Программа по умолчанию ничего не меняет",
        "Это не пожелание, а главное архитектурное решение проекта. Команды "
        "<code class=\"inline\">scan</code>, <code class=\"inline\">plan</code> и "
        "<code class=\"inline\">duplicates</code> только читают файловую систему. Переместить "
        "файлы может исключительно команда <code class=\"inline\">apply</code> — и никакая "
        "другая команда не должна перемещать или удалять файлы неожиданно для пользователя.",
    )}

    <h2>Что сознательно остаётся за рамками версии 0.1.0</h2>
    <p>Формулировка границ проекта так же важна, как список того, что он делает — иначе
    проект разрастается быстрее, чем его успевают довести до рабочего состояния:</p>
    {comparison_table(
        ["Не входит в версию 0.1.0", "Почему"],
        [
            ["Автоматическое удаление дубликатов", "Удаление данных без явного подтверждения — риск, а не удобство"],
            ["Графический интерфейс", "Командная строка проще реализовать, протестировать и объяснить"],
            ["Загрузка файлов в облако", "Программа работает только с локальной файловой системой"],
            ["Классификация по содержимому файла", "Классификация по расширению уже решает основную задачу"],
            ["Сетевой сервис", "SafeSort — инструмент для одного пользователя на одной машине"],
        ],
    )}

    <h2>От требований к плану работы</h2>
    <p>Требования выше определяют пять команд SafeSort — <code class="inline">scan</code>,
    <code class="inline">plan</code>, <code class="inline">apply</code>,
    <code class="inline">duplicates</code>, <code class="inline">undo</code> — и то, в каком
    порядке имеет смысл их реализовывать: сначала то, что только читает файловую систему,
    затем то, что её меняет, и только потом — поиск дубликатов и отмену операций. Разделы
    23.7-23.16 следуют именно этому порядку.</p>

    {summary_box("Коротко", [
        "Функциональные требования описывают, что программа делает; нефункциональные — какими "
        "свойствами обладает её поведение.",
        "Явная граница «что не входит в версию» защищает проект от бесконечного разрастания.",
        "Главное нефункциональное требование SafeSort: команды чтения (scan, plan, duplicates) "
        "никогда не меняют файлы, перемещение делает только явная команда apply.",
    ])}
    """
    out = render_page(
        page_title="От идеи к требованиям проекта",
        description="Функциональные и нефункциональные требования SafeSort, явные границы версии 0.1.0.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Требования", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="От идеи к требованиям проекта",
        lede="Прежде чем писать код, нужно точно решить, что программа обязана делать — и чего делать не должна.",
        body_html=body,
        sidebar_groups=sidebar("23-01-ideya-trebovaniya.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="23-02-repozitorij.html", next_label="Создаём репозиторий проекта"),
    )
    write("23-01-ideya-trebovaniya.html", out)


def build_02() -> None:
    body = f"""
    <p><strong>Репозиторий</strong> — каталог, в котором Git хранит историю изменений
    проекта: все версии файлов, кто и когда их менял, и метаданные для восстановления любой
    прошлой версии. Каталог проекта и репозиторий — не одно и то же понятие, хотя на практике
    репозиторий обычно и есть каталог проекта: сами файлы проекта называют
    <strong>рабочим деревом</strong> (working tree), а служебные данные Git хранятся отдельно,
    в подкаталоге <code class="inline">.git</code>, который создаёт команда
    <code class="inline">git init</code>.</p>

    {code_block(
        "Терминал",
        "mkdir safesort\n"
        "cd safesort\n"
        "git init\n",
        lang="text",
    )}

    <p>После <code class="inline">git init</code> каталог уже репозиторий, но в нём пока нет
    ни одного файла и ни одного коммита. Проверить состояние репозитория можно командой
    <code class="inline">git status</code> — она показывает, какие файлы Git видит, но ещё не
    отслеживает, какие изменены с последнего коммита, и какие уже подготовлены к коммиту:</p>

    {code_block("Терминал", "git status", lang="text")}

    {callout(
        "info",
        "Локальный репозиторий и репозиторий на GitHub — разные вещи",
        "Команда <code class=\"inline\">git init</code> создаёт только локальный репозиторий "
        "на компьютере. GitHub хранит отдельную копию той же истории — "
        "<strong>удалённый репозиторий</strong> (remote). Раздел 23.29 подключит удалённый "
        "репозиторий к локальному через <code class=\"inline\">git push</code>: до этого "
        "момента вся история существует только на компьютере.",
    )}

    <h2>Что войдёт в репозиторий, а что нет</h2>
    <p>Не все файлы, которые появляются в каталоге проекта, стоит хранить в Git: например,
    служебные файлы виртуального окружения или кеш сборки создаются заново на любой машине и
    только засоряют историю. Список того, что Git должен игнорировать, задаёт файл
    <code class="inline">.gitignore</code>:</p>
    {code_block(
        ".gitignore",
        "__pycache__/\n"
        "*.pyc\n"
        ".venv/\n"
        "dist/\n"
        "*.egg-info/\n",
    )}

    {summary_box("Коротко", [
        "git init создаёт локальный репозиторий — каталог .git с историей изменений — внутри "
        "рабочего дерева проекта.",
        "git status показывает текущее состояние: какие файлы изменены, какие ещё не отслеживаются Git.",
        "Локальный репозиторий и репозиторий на GitHub — разные копии одной истории; они "
        "связываются позже, через git push.",
        ".gitignore перечисляет то, что Git не должен отслеживать: временные и сгенерированные файлы.",
    ])}
    """
    out = render_page(
        page_title="Создаём репозиторий проекта",
        description="git init, рабочее дерево, git status и .gitignore — начало репозитория SafeSort.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Репозиторий", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Создаём репозиторий проекта",
        lede="git init превращает обычный каталог в репозиторий — но каталог проекта и репозиторий не одно и то же понятие.",
        body_html=body,
        sidebar_groups=sidebar("23-02-repozitorij.html"),
        nav=PageNav(prev_href="23-01-ideya-trebovaniya.html", prev_label="От идеи к требованиям", next_href="23-03-readme.html", next_label="Первый README проекта"),
    )
    write("23-02-repozitorij.html", out)


def build_03() -> None:
    body = f"""
    <p><strong>README</strong> — первый файл, который видит любой человек, открывший
    репозиторий: GitHub автоматически показывает его содержимое на главной странице проекта.
    Хороший README отвечает на вопросы «что это?», «зачем?» и «как запустить?» ещё до того,
    как человек откроет исходный код.</p>

    <h2>Структура README SafeSort</h2>
    {code_block(
        "README.md",
        "# SafeSort\n\n"
        "Локальная программа командной строки для безопасной сортировки файлов "
        "и поиска дубликатов.\n\n"
        "## Features\n\n"
        "- сканирование каталога и классификация файлов по расширению\n"
        "- план перемещений без изменения файлов\n"
        "- перемещение файлов только по явной команде\n"
        "- поиск файлов с одинаковым содержимым\n"
        "- отмена последней выполненной операции\n\n"
        "## Safety\n\n"
        "scan, plan и duplicates только читают файловую систему. Перемещает файлы "
        "исключительно apply.\n\n"
        "## Installation\n\n"
        "## Usage\n\n"
        "## Examples\n\n"
        "## Development\n\n"
        "## Tests\n\n"
        "## License\n",
    )}

    {callout(
        "warning",
        "Без придуманных значков и статусов",
        "На странице проекта на GitHub иногда встречаются цветные значки (badge) вида "
        "«tests: passing» или «coverage: 98%». Такой значок честен только тогда, когда его "
        "действительно обслуживает настроенный сервис — например, GitHub Actions из раздела "
        "23.30. Вставлять его раньше, чем он подключён к реальной проверке, значит показывать "
        "то, чего на самом деле нет.",
    )}

    <p>Полный, уже заполненный README настоящего проекта — здесь: [[icon:file]]
    <a href="../../../projects/python/safesort/README.md">projects/python/safesort/README.md</a>.</p>

    {summary_box("Коротко", [
        "README.md — первое, что видит человек, открывший репозиторий на GitHub.",
        "Разделы Features, Safety, Installation, Usage, Development, Tests и License покрывают "
        "вопросы «что», «зачем» и «как запустить», которые обычно задают в первую очередь.",
        "Значок статуса на README честен только тогда, когда его действительно обслуживает "
        "настроенная проверка, а не просто вставлен для вида.",
    ])}
    """
    out = render_page(
        page_title="Первый README проекта",
        description="Структура README.md: назначение проекта, безопасность, установка, использование, тесты.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("README", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Первый README проекта",
        lede="README отвечает на вопросы «что это?» и «как запустить?» ещё до того, как человек откроет код.",
        body_html=body,
        sidebar_groups=sidebar("23-03-readme.html"),
        nav=PageNav(prev_href="23-02-repozitorij.html", prev_label="Репозиторий проекта", next_href="23-04-struktura-paketa.html", next_label="Структура Python-пакета"),
    )
    write("23-03-readme.html", out)


def build_04() -> None:
    body = f"""
    <p>Прежде чем писать код SafeSort, стоит решить, как разложить его по файлам. Хаотичная
    структура каталогов не мешает программе работать, но мешает её понимать, тестировать и
    устанавливать как пакет. SafeSort использует так называемую <strong>src-раскладку</strong>
    (src layout) — пакет лежит внутри каталога <code class="inline">src/</code>, а не прямо в
    корне репозитория:</p>

    {code_block(
        "Структура каталогов",
        "safesort/\n"
        "├── pyproject.toml\n"
        "├── README.md\n"
        "├── CHANGELOG.md\n"
        "├── LICENSE\n"
        "├── src/\n"
        "│   └── safesort/\n"
        "│       ├── __init__.py\n"
        "│       ├── __main__.py\n"
        "│       ├── cli.py\n"
        "│       ├── models.py\n"
        "│       ├── scanner.py\n"
        "│       ├── classifier.py\n"
        "│       ├── planner.py\n"
        "│       ├── executor.py\n"
        "│       ├── duplicates.py\n"
        "│       ├── manifest.py\n"
        "│       └── config.py\n"
        "└── tests/\n"
        "    ├── test_scanner.py\n"
        "    ├── test_classifier.py\n"
        "    ├── test_planner.py\n"
        "    ├── test_executor.py\n"
        "    ├── test_duplicates.py\n"
        "    ├── test_manifest.py\n"
        "    ├── test_config.py\n"
        "    └── test_cli.py\n",
        lang="text",
    )}

    {callout(
        "info",
        "Зачем нужен лишний уровень src/",
        "Без каталога <code class=\"inline\">src/</code> установленный пакет и каталог "
        "исходников совпадали бы, и легко было бы по ошибке протестировать не тот код, что "
        "реально установлен — например, если забыть переустановить пакет после правки файла. "
        "src-раскладка заставляет тесты обращаться к <em>установленному</em> пакету "
        "<code class=\"inline\">safesort</code>, а не к соседнему каталогу с исходниками. Это "
        "не единственный правильный способ организовать пакет — есть проекты и без "
        "<code class=\"inline\">src/</code> — но для SafeSort он выбран сознательно, а не "
        "потому что так «принято».",
    )}

    <p>Каждый файл в <code class="inline">src/safesort/</code> отвечает за одну часть
    программы: <code class="inline">scanner.py</code> только читает каталог,
    <code class="inline">planner.py</code> только строит план, <code class="inline">
    executor.py</code> — единственный файл, которому разрешено перемещать файлы на диске.
    Разделы 23.8-23.19 разбирают эти модули по очереди.</p>

    {summary_box("Коротко", [
        "src-раскладка кладёт исходный пакет в src/safesort/, а не в корень репозитория.",
        "Такая раскладка не даёт тестам случайно обратиться к неустановленному коду вместо "
        "установленного пакета.",
        "Каждый модуль SafeSort отвечает за одну часть программы — от чтения каталога до "
        "перемещения файлов.",
    ])}
    """
    out = render_page(
        page_title="Планируем структуру Python-пакета",
        description="src-раскладка пакета SafeSort: зачем нужен каталог src/ и как модули разделены по ответственности.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Структура пакета", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Планируем структуру Python-пакета",
        lede="src-раскладка: пакет лежит в src/safesort/, а не в корне репозитория — и почему это осознанный выбор, а не догма.",
        body_html=body,
        sidebar_groups=sidebar("23-04-struktura-paketa.html"),
        nav=PageNav(prev_href="23-03-readme.html", prev_label="README проекта", next_href="23-05-pyproject-toml.html", next_label="pyproject.toml и установка"),
    )
    write("23-04-struktura-paketa.html", out)


def build_05() -> None:
    body = f"""
    <p><code class="inline">pyproject.toml</code> — файл, который описывает пакет для
    инструментов установки: как называется проект, какая у него версия, какой Python ему
    нужен, какие у него зависимости и какая команда запускается после установки. SafeSort
    использует ровно те поля, которые ему нужны — этого достаточно, чтобы пакет
    устанавливался и работал:</p>

    {code_block(
        "pyproject.toml",
        '[build-system]\n'
        'requires = ["hatchling"]\n'
        'build-backend = "hatchling.build"\n\n'
        '[project]\n'
        'name = "safesort"\n'
        'version = "0.1.0"\n'
        'description = "A safe, non-destructive command-line file organizer."\n'
        'readme = "README.md"\n'
        'requires-python = ">=3.14"\n'
        'license = "MIT"\n'
        'dependencies = []\n\n'
        '[project.optional-dependencies]\n'
        'dev = ["pytest>=8"]\n\n'
        '[project.scripts]\n'
        'safesort = "safesort.cli:main"\n',
    )}

    {callout(
        "info",
        "dependencies = [] — не пропуск, а факт",
        "У SafeSort нет ни одной обязательной сторонней зависимости: <code class=\"inline\">"
        "pathlib</code>, <code class=\"inline\">argparse</code>, <code class=\"inline\">"
        "hashlib</code>, <code class=\"inline\">shutil</code>, <code class=\"inline\">json</code>"
        " и <code class=\"inline\">tomllib</code> — часть стандартной библиотеки Python. "
        "<code class=\"inline\">pytest</code> нужен только для разработки и тестов, поэтому он "
        "перечислен отдельно, в <code class=\"inline\">[project.optional-dependencies]</code>, "
        "а не в <code class=\"inline\">dependencies</code>.",
    )}

    <h2>[project.scripts] — команда после установки</h2>
    <p>Строка <code class="inline">safesort = "safesort.cli:main"</code> говорит инструменту
    установки: после установки пакета создай в окружении исполняемую команду
    <code class="inline">safesort</code>, которая вызывает функцию
    <code class="inline">main()</code> из модуля <code class="inline">safesort.cli</code>.
    Без этой строки пакет всё равно можно было бы использовать через
    <code class="inline">python -m safesort</code>, но отдельной команды
    <code class="inline">safesort</code> в терминале не появилось бы.</p>

    <h2>Устанавливаем пакет в редактируемом режиме</h2>
    <p><strong>Редактируемая установка</strong> (editable install) связывает окружение
    Python с исходным кодом пакета напрямую: изменения в файлах <code class="inline">
    src/safesort/</code> становятся видны сразу, без повторной установки.</p>
    {code_block("Терминал (окружение активировано)", "pip install -e .[dev]", lang="text")}
    <p>После этого команда <code class="inline">safesort --help</code> должна работать прямо
    в терминале:</p>
    {code_block(
        "Терминал",
        "$ safesort --help\n"
        "usage: safesort [-h] {scan,plan,apply,duplicates,undo} ...\n\n"
        "SafeSort: a safe, non-destructive file organizer. scan/plan/duplicates never\n"
        "modify anything; only 'apply' moves files.\n",
        lang="text",
    )}

    {practice_card(
        "23-07",
        "Практика: разбор аргументов командной строки",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/23-07/index.html",
    )}
    """
    out = render_page(
        page_title="pyproject.toml и установка проекта",
        description="Минимальный pyproject.toml SafeSort: метаданные, точка входа, редактируемая установка pip install -e.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("pyproject.toml", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="pyproject.toml и установка проекта",
        lede="Один файл описывает пакет для инструментов установки — и после pip install -e команда safesort появляется в терминале.",
        body_html=body,
        sidebar_groups=sidebar("23-05-pyproject-toml.html"),
        nav=PageNav(prev_href="23-04-struktura-paketa.html", prev_label="Структура пакета", next_href="23-06-komandnaya-stroka.html", next_label="Командная строка SafeSort"),
    )
    write("23-05-pyproject-toml.html", out)


def build_06() -> None:
    body = f"""
    <p>SafeSort управляется пятью подкомандами: <code class="inline">scan</code>,
    <code class="inline">plan</code>, <code class="inline">apply</code>,
    <code class="inline">duplicates</code> и <code class="inline">undo</code>. За разбор
    аргументов командной строки отвечает модуль <code class="inline">argparse</code> из
    стандартной библиотеки — он же формирует текст <code class="inline">--help</code>,
    который вы уже видели в предыдущем разделе.</p>

    {code_block(
        "src/safesort/cli.py",
        'def build_parser() -> argparse.ArgumentParser:\n'
        '    parser = argparse.ArgumentParser(\n'
        '        prog="safesort",\n'
        '        description=(\n'
        '            "SafeSort: a safe, non-destructive file organizer. "\n'
        '            "scan/plan/duplicates never modify anything; only \'apply\' moves files."\n'
        '        ),\n'
        '    )\n'
        '    subparsers = parser.add_subparsers(dest="command", required=True)\n\n'
        '    scan_parser = subparsers.add_parser("scan", help="...")\n'
        '    scan_parser.add_argument("root", type=Path, help="Directory to scan.")\n'
        "    # ...аналогично для plan, apply, duplicates, undo\n"
        "    return parser\n",
    )}

    {callout(
        "tip",
        "add_subparsers(dest=\"command\", required=True)",
        "<code class=\"inline\">dest=\"command\"</code> кладёт название вызванной подкоманды в "
        "<code class=\"inline\">args.command</code>. <code class=\"inline\">required=True</code>"
        " заставляет argparse самостоятельно вывести понятную ошибку, если пользователь "
        "запустит <code class=\"inline\">safesort</code> вообще без подкоманды, — писать эту "
        "проверку вручную не нужно.",
    )}

    <h2>От разобранных аргументов к результату</h2>
    <p>Каждой подкоманде соответствует одна функция-обработчик, и словарь связывает имя
    команды с нужной функцией:</p>
    {code_block(
        "src/safesort/cli.py",
        '_HANDLERS = {\n'
        '    "scan": cmd_scan,\n'
        '    "plan": cmd_plan,\n'
        '    "apply": cmd_apply,\n'
        '    "duplicates": cmd_duplicates,\n'
        '    "undo": cmd_undo,\n'
        "}\n\n"
        "def main(argv: list[str] | None = None) -> int:\n"
        "    parser = build_parser()\n"
        "    args = parser.parse_args(argv)\n"
        "    handler = _HANDLERS[args.command]\n"
        "    return handler(args)\n",
    )}
    <p>Такой словарь — тот же приём, что и в игре «Камень, ножницы, бумага» из приложения к
    этой главе: вместо цепочки <code class="inline">if args.command == "scan": ... elif ...
    </code> нужную функцию просто ищут по ключу.</p>

    <p>Каждая обработчик-функция возвращает целое число: <code class="inline">0</code> при
    успехе, отличное от нуля значение при ошибке — это и есть код возврата программы, который
    видит операционная система и любой сценарий, вызывающий <code class="inline">safesort</code>
    из другого места.</p>

    {summary_box("Коротко", [
        "argparse.ArgumentParser с add_subparsers() разбирает пять подкоманд SafeSort и сам "
        "формирует текст --help.",
        "dest=\"command\" кладёт имя вызванной подкоманды в args.command; словарь _HANDLERS "
        "связывает это имя с нужной функцией.",
        "Каждый обработчик возвращает 0 при успехе и ненулевое значение при ошибке — это код "
        "возврата всей программы.",
    ])}
    """
    out = render_page(
        page_title="Командная строка SafeSort",
        description="argparse, add_subparsers() и пять подкоманд SafeSort: scan, plan, apply, duplicates, undo.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Командная строка", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Командная строка SafeSort",
        lede="argparse разбирает пять подкоманд SafeSort и связывает каждую с отдельной функцией-обработчиком.",
        body_html=body,
        sidebar_groups=sidebar("23-06-komandnaya-stroka.html"),
        nav=PageNav(prev_href="23-05-pyproject-toml.html", prev_label="pyproject.toml", next_href="23-07-pathlib.html", next_label="pathlib: пути и каталоги"),
    )
    write("23-06-komandnaya-stroka.html", out)


def build_07() -> None:
    body = f"""
    <p>Всё, что SafeSort делает с файлами, начинается с путей — а модуль
    <code class="inline">pathlib</code> из стандартной библиотеки описывает путь не строкой, а
    объектом <code class="inline">Path</code> с собственными операциями: сложение частей пути,
    проверка существования, получение расширения файла.</p>

    {code_block(
        "pathlib_osnovy.py",
        'from pathlib import Path\n\n'
        'koren = Path("~/Downloads").expanduser()\n'
        'fajl = koren / "otchet.pdf"\n\n'
        'print(fajl.name)        # otchet.pdf\n'
        'print(fajl.suffix)      # .pdf\n'
        'print(fajl.parent)      # /home/anna/Downloads\n'
        'print(fajl.exists())    # True, если файл действительно есть\n',
    )}

    {callout(
        "tip",
        "koren / \"otchet.pdf\" — оператор / для путей",
        "У класса <code class=\"inline\">Path</code> переопределён оператор "
        "<code class=\"inline\">/</code>: он не делит числа, а склеивает часть пути с новым "
        "именем, автоматически подставляя правильный разделитель для текущей операционной "
        "системы. Собирать пути строковой конкатенацией "
        "(<code class=\"inline\">koren + \"/\" + \"otchet.pdf\"</code>) не нужно.",
    )}

    <h2>Модель данных SafeSort: FileInfo</h2>
    <p>Сканер SafeSort не хранит просто список путей — он описывает каждый найденный файл
    небольшим неизменяемым объектом:</p>
    {code_block(
        "src/safesort/models.py",
        '@dataclass(frozen=True)\n'
        'class FileInfo:\n'
        '    path: Path\n'
        '    size: int\n'
        '    extension: str\n',
    )}
    <p><code class="inline">frozen=True</code> запрещает менять поля объекта после создания —
    для SafeSort это не случайная деталь: программа сознательно разделяет
    <em>планирование</em> (ничего не меняет на диске) и <em>выполнение</em> (единственный
    этап, которому разрешено трогать файлы), и неизменяемые объекты не дают коду планирования
    случайно превратиться в код, который что-то меняет.</p>

    {practice_card(
        "23-08",
        "Практика: операции с Path",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/23-08/index.html",
    )}
    """
    out = render_page(
        page_title="pathlib: работаем с путями и каталогами",
        description="Path, оператор / для путей и неизменяемая модель FileInfo — основа для сканера SafeSort.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("pathlib", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="pathlib: работаем с путями и каталогами",
        lede="Path описывает путь объектом со своими операциями — и на нём строится вся модель данных SafeSort.",
        body_html=body,
        sidebar_groups=sidebar("23-07-pathlib.html"),
        nav=PageNav(prev_href="23-06-komandnaya-stroka.html", prev_label="Командная строка", next_href="23-08-skaniruem-katalog.html", next_label="Сканируем каталог"),
    )
    write("23-07-pathlib.html", out)


def build_08() -> None:
    body = f"""
    <p>Первый настоящий шаг SafeSort — обойти каталог и составить список файлов. Функция
    <code class="inline">scan()</code> — одна из трёх строго нечитающих команд SafeSort: она
    только вызывает <code class="inline">iterdir()</code> и <code class="inline">stat()</code>,
    ни разу не создавая, не перемещая и не удаляя ничего на диске.</p>

    {code_block(
        "src/safesort/scanner.py",
        'def scan(root: Path, config: Config) -> list[FileInfo]:\n'
        '    root = Path(root)\n'
        '    excluded = config.excluded_names()\n'
        '    results: list[FileInfo] = []\n'
        '    _scan_dir(root, excluded, results)\n'
        '    return results\n',
    )}

    <p>Сам обход рекурсивный: функция <code class="inline">_scan_dir()</code> заходит в
    каждый подкаталог и вызывает себя снова:</p>
    {code_block(
        "src/safesort/scanner.py",
        "for entry in entries:\n"
        "    if entry.is_symlink():\n"
        "        continue  # символические ссылки пропускаются — раздел 23.9\n"
        "    if entry.is_dir():\n"
        "        if entry.name in excluded:\n"
        "            continue  # исключённые каталоги пропускаются — раздел 23.9\n"
        "        _scan_dir(entry, excluded, results)\n"
        "    elif entry.is_file():\n"
        "        size = entry.stat().st_size\n"
        "        results.append(FileInfo(path=entry, size=size, extension=entry.suffix.lower()))\n",
    )}

    {callout(
        "warning",
        "Каталог, который нельзя прочитать, не должен остановить всё сканирование",
        "Если для какого-то подкаталога недостаточно прав доступа, "
        "<code class=\"inline\">iterdir()</code> вызывает "
        "<code class=\"inline\">PermissionError</code>. Настоящая реализация "
        "<code class=\"inline\">_scan_dir()</code> перехватывает эту ошибку для каждого "
        "подкаталога отдельно, записывает предупреждение в журнал (раздел 23.21) и продолжает "
        "сканировать остальные каталоги — так один недоступный подкаталог не обрывает весь "
        "просмотр целиком. Подробнее об этом — раздел 23.20.",
    )}

    <p>Проверить сканер можно прямо сейчас — реальный вывод:</p>
    {code_block(
        "Терминал",
        "$ safesort scan ~/Downloads\n"
        "Files scanned: 48\n"
        "Documents: 12\n"
        "Images: 18\n"
        "Archives: 5\n"
        "Other: 13\n",
        lang="text",
    )}

    {local_required_card(
        "23-09",
        "Практика: сканируем настоящий каталог",
        "Нужен доступ к настоящей файловой системе — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/23-09/index.html",
    )}
    """
    out = render_page(
        page_title="Сканируем каталог",
        description="scan() рекурсивно обходит каталог через iterdir() и stat(), не изменяя файловую систему.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Сканирование", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Сканируем каталог",
        lede="scan() строго читает файловую систему — обходит каталог рекурсивно и не меняет ни одного файла.",
        body_html=body,
        sidebar_groups=sidebar("23-08-skaniruem-katalog.html"),
        nav=PageNav(prev_href="23-07-pathlib.html", prev_label="pathlib", next_href="23-09-isklyucheniya.html", next_label="Какие каталоги не сканировать"),
    )
    write("23-08-skaniruem-katalog.html", out)


def build_09() -> None:
    body = f"""
    <p>Сканер SafeSort пропускает не только неважные файлы, но и целые каталоги — по двум
    разным причинам. Первая: некоторые каталоги заведомо не относятся к пользовательским
    файлам — например, <code class="inline">.git</code> или <code class="inline">.venv</code>.
    Вторая, более тонкая: собственный каталог результата, <code class="inline">Sorted/</code>,
    и служебный каталог самого SafeSort, <code class="inline">.safesort/</code>, должны быть
    исключены <em>всегда</em> — иначе повторный запуск начал бы сортировать уже
    отсортированные файлы и собственные журналы операций.</p>

    {code_block(
        "src/safesort/config.py",
        'def excluded_names(self) -> frozenset[str]:\n'
        '    return frozenset({*self.exclude, self.destination, STATE_DIRNAME})\n',
    )}

    {callout(
        "info",
        "Настраиваемые исключения и обязательные исключения — разные множества",
        "<code class=\"inline\">self.exclude</code> — список, который пользователь может "
        "изменить через файл настроек (раздел 23.22). Каталог результата "
        "(<code class=\"inline\">self.destination</code>, по умолчанию "
        "<code class=\"inline\">Sorted</code>) и служебный каталог "
        "<code class=\"inline\">.safesort</code> добавляются в исключения динамически, при "
        "каждом вызове — их нельзя случайно убрать из списка исключений через настройки.",
    )}

    <h2>Символические ссылки: осознанно пропускаются</h2>
    <p>Символическая ссылка — файл или каталог, который на самом деле указывает на другое
    место в файловой системе. SafeSort не переходит по символическим ссылкам вообще, ни на
    файлы, ни на каталоги:</p>
    {comparison_table(
        ["Почему ссылки пропускаются", "Что произошло бы иначе"],
        [
            ["Ссылка может указывать за пределы просканированного каталога", "SafeSort мог бы переместить файл, не принадлежащий выбранному каталогу"],
            ["Ссылка на каталог может создать цикл обхода", "Рекурсивное сканирование могло бы никогда не завершиться"],
            ["Поведение с симлинками не всегда очевидно даже опытным пользователям", "Первая версия программы выбирает предсказуемое поведение вместо более сложного"],
        ],
    )}

    <p>Это решение легко проверить: сканер использует <code class="inline">entry.is_symlink()
    </code> раньше любой другой проверки и, если это символическая ссылка, сразу переходит к
    следующему элементу каталога — раздел 23.8 уже показывал эту строку в
    <code class="inline">_scan_dir()</code>.</p>

    {practice_card(
        "23-10",
        "Практика: проверка исключённых каталогов",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/23-10/index.html",
    )}
    """
    out = render_page(
        page_title="Какие каталоги не нужно сканировать",
        description="Настраиваемые исключения, обязательное исключение каталога результата и .safesort, политика в отношении символических ссылок.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Исключения", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Какие каталоги не нужно сканировать",
        lede="Каталог результата и служебный каталог SafeSort исключены всегда — а символические ссылки не отслеживаются вовсе.",
        body_html=body,
        sidebar_groups=sidebar("23-09-isklyucheniya.html"),
        nav=PageNav(prev_href="23-08-skaniruem-katalog.html", prev_label="Сканируем каталог", next_href="23-10-klassifikaciya.html", next_label="Определяем категорию файла"),
    )
    write("23-09-isklyucheniya.html", out)


def build_10() -> None:
    body = f"""
    <p>Каждому найденному файлу нужно назначить категорию — документы, изображения, видео и
    так далее. SafeSort определяет категорию по расширению файла: простое и предсказуемое
    правило, которое покрывает подавляющее большинство практических случаев.</p>

    {code_block(
        "src/safesort/config.py",
        'DEFAULT_EXTENSIONS: dict[str, list[str]] = {\n'
        '    "documents": [".pdf", ".docx", ".txt", ".odt"],\n'
        '    "images": [".jpg", ".jpeg", ".png", ".webp"],\n'
        '    "video": [".mp4", ".mkv", ".mov"],\n'
        '    "audio": [".mp3", ".wav", ".flac"],\n'
        '    "archives": [".zip", ".tar", ".gz", ".7z"],\n'
        '    "code": [".py", ".js", ".ts", ".rs", ".java"],\n'
        '    "data": [".json", ".csv", ".xml"],\n'
        "}\n",
    )}

    {code_block(
        "src/safesort/classifier.py",
        'OTHER_CATEGORY = "other"\n\n'
        'def classify(extension: str, mapping: dict[str, list[str]]) -> str:\n'
        '    normalized = extension.lower()\n'
        '    for category, extensions in mapping.items():\n'
        '        lowered = {ext.lower() for ext in extensions}\n'
        '        if normalized in lowered:\n'
        '            return category\n'
        '    return OTHER_CATEGORY\n',
    )}

    {callout(
        "warning",
        "Классификация по расширению — эвристика, а не доказательство содержимого",
        "Расширение <code class=\"inline\">.pdf</code> означает лишь то, что имя файла "
        "заканчивается на <code class=\"inline\">.pdf</code> — ничто не мешает переименовать "
        "любой файл так, чтобы его расширение не соответствовало реальному формату. SafeSort "
        "сознательно не заглядывает внутрь файла: это было бы медленнее, менее предсказуемо и "
        "выходит за рамки задачи «разложить файлы по тому, чем они себя называют».",
    )}

    <p>Файл с расширением, которого нет ни в одной категории, попадает в
    <code class="inline">"other"</code> — так классификация остаётся полной: у любого файла
    всегда есть категория, даже если это самая широкая из них.</p>

    {practice_card(
        "23-11",
        "Практика: classify() и собственные категории",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/23-11/index.html",
    )}
    """
    out = render_page(
        page_title="Определяем категорию файла",
        description="classify() сопоставляет расширение файла категории по словарю DEFAULT_EXTENSIONS, с явным запасным вариантом other.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Классификация", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Определяем категорию файла",
        lede="Классификация по расширению — практичная эвристика, не доказательство того, что действительно лежит внутри файла.",
        body_html=body,
        sidebar_groups=sidebar("23-10-klassifikaciya.html"),
        nav=PageNav(prev_href="23-09-isklyucheniya.html", prev_label="Исключения", next_href="23-11-plan-dejstvij.html", next_label="От анализа к плану действий"),
    )
    write("23-10-klassifikaciya.html", out)


def build_11() -> None:
    body = f"""
    <p>У SafeSort есть список найденных файлов и правило классификации — но само по себе это
    ещё не план действий. <strong>План</strong> — список конкретных перемещений: откуда и
    куда переместится каждый файл, если пользователь подтвердит выполнение.</p>

    {code_block(
        "src/safesort/models.py",
        '@dataclass(frozen=True)\n'
        'class MoveOperation:\n'
        '    source: Path\n'
        '    destination: Path\n\n'
        '@dataclass(frozen=True)\n'
        'class SortPlan:\n'
        '    root: Path\n'
        '    operations: tuple[MoveOperation, ...]\n',
    )}

    {callout(
        "tip",
        "План — это данные, а не действие",
        "<code class=\"inline\">SortPlan</code> не содержит ни одного вызова, который "
        "перемещает файлы, — только описание того, что <em>можно было бы</em> сделать. Эта "
        "мысль — ключевая для всей архитектуры SafeSort: пока объект остаётся данными, его "
        "можно вывести на экран, проверить тестами, сохранить или просто отбросить, не "
        "рискуя ни одним файлом пользователя.",
    )}

    <p>Функция <code class="inline">build_plan()</code> строит план по списку файлов от
    сканера, не трогая диск ни разу, кроме одной read-only проверки — существует ли уже файл
    с таким именем в месте назначения (об этом раздел 23.14):</p>
    {code_block(
        "src/safesort/planner.py",
        'def build_plan(files: list[FileInfo], root: Path, config: Config) -> SortPlan:\n'
        '    dest_root = Path(root) / config.destination\n'
        '    operations = []\n'
        '    for file in files:\n'
        '        category = classify(file.extension, config.extensions)\n'
        '        dest_dir = dest_root / category\n'
        '        candidate = dest_dir / file.path.name\n'
        '        destination = _resolve_collision(candidate, reserved)\n'
        '        operations.append(MoveOperation(source=file.path, destination=destination))\n'
        '    return SortPlan(root=root, operations=tuple(operations))\n',
    )}

    {practice_card(
        "23-12",
        "Практика: строим план из списка файлов",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/23-12/index.html",
    )}
    """
    out = render_page(
        page_title="От анализа к плану действий",
        description="MoveOperation, SortPlan и build_plan() — план перемещений как данные, без единого изменения файловой системы.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("План действий", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="От анализа к плану действий",
        lede="План перемещений — обычные данные: его можно вывести на экран, проверить или отбросить, не тронув ни одного файла.",
        body_html=body,
        sidebar_groups=sidebar("23-11-plan-dejstvij.html"),
        nav=PageNav(prev_href="23-10-klassifikaciya.html", prev_label="Классификация файла", next_href="23-12-predvaritelnyj-prosmotr.html", next_label="Режим предварительного просмотра"),
    )
    write("23-11-plan-dejstvij.html", out)


def build_12() -> None:
    body = f"""
    <p>Команда <code class="inline">plan</code> — единственное, что нужно сделать с готовым
    объектом <code class="inline">SortPlan</code>, чтобы получить полноценный
    <strong>предварительный просмотр</strong> (dry run): она собирает план и выводит его
    размер на экран, ни разу не вызывая ничего, что меняет диск.</p>

    {code_block(
        "src/safesort/cli.py",
        'def cmd_plan(args: argparse.Namespace) -> int:\n'
        '    root = args.root\n'
        '    config, code = _load_config(root)\n'
        '    files = scan(root, config)\n'
        '    plan = build_plan(files, root, config)\n'
        '    print(f"{len(plan.operations)} move operations planned.")\n'
        '    print("No files have been changed.")\n'
        '    return 0\n',
    )}

    {code_block(
        "Терминал",
        "$ safesort plan ~/Downloads\n"
        "12 move operations planned.\n"
        "No files have been changed.\n",
        lang="text",
    )}

    {callout(
        "info",
        "scan, plan и duplicates используют один и тот же список файлов",
        "Три read-only команды SafeSort — <code class=\"inline\">scan</code>, "
        "<code class=\"inline\">plan</code> и <code class=\"inline\">duplicates</code> — "
        "начинаются одинаково: вызывают <code class=\"inline\">scan()</code>, чтобы получить "
        "список файлов. Дальше их пути расходятся: <code class=\"inline\">plan</code> строит "
        "план, <code class=\"inline\">duplicates</code> ищет совпадения по содержимому "
        "(раздел 23.17), а <code class=\"inline\">scan</code> просто считает файлы по "
        "категориям.",
    )}

    <p>Вторая строка вывода — <code class="inline">"No files have been changed."</code> — не
    формальность. Это утверждение, которое действительно проверяется: раздел 23.24 напишет
    тест, который убедится, что после вызова <code class="inline">plan</code> содержимое
    каталога не изменилось ни на один байт.</p>

    {summary_box("Коротко", [
        "plan строит тот же SortPlan, что и apply, но только выводит его размер на экран.",
        "scan, plan и duplicates начинаются одинаково — с вызова scan() — и расходятся дальше.",
        "Утверждение «файлы не изменены» после plan — не текст для красоты, а поведение, "
        "которое проверяется автоматическим тестом.",
    ])}
    """
    out = render_page(
        page_title="Режим предварительного просмотра",
        description="Команда plan показывает размер плана перемещений, не трогая файловую систему — настоящий dry run.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Предпросмотр", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Режим предварительного просмотра",
        lede="Команда plan — предварительный просмотр без побочных эффектов: тот же план, что и у apply, но без единого изменения диска.",
        body_html=body,
        sidebar_groups=sidebar("23-12-predvaritelnyj-prosmotr.html"),
        nav=PageNav(prev_href="23-11-plan-dejstvij.html", prev_label="План действий", next_href="23-13-peremeshaem-fajly.html", next_label="Безопасно перемещаем файлы"),
    )
    write("23-12-predvaritelnyj-prosmotr.html", out)


def build_13() -> None:
    body = f"""
    <p>До сих пор ни одна строка кода SafeSort не трогала файловую систему на запись. Модуль
    <code class="inline">executor.py</code> — единственное место во всей программе, где это
    происходит: функция <code class="inline">apply_plan()</code> выполняет уже готовый план и
    только его.</p>

    {code_block(
        "src/safesort/executor.py",
        'def apply_plan(plan: SortPlan) -> list[CompletedMove]:\n'
        '    results = []\n'
        '    for operation in plan.operations:\n'
        '        source, destination = operation.source, operation.destination\n'
        '        destination.parent.mkdir(parents=True, exist_ok=True)\n\n'
        '        if destination.exists() or destination.is_symlink():\n'
        '            results.append(CompletedMove(source, destination, completed=False,\n'
        '                                          error="destination already exists"))\n'
        '            continue\n\n'
        '        shutil.move(str(source), str(destination))\n'
        '        results.append(CompletedMove(source, destination, completed=True))\n'
        '    return results\n',
    )}

    {callout(
        "warning",
        "Партия перемещений — не транзакция базы данных",
        "Если один файл в середине партии не удаётся переместить (например, права доступа "
        "изменились между сканированием и выполнением), это не должно остановить обработку "
        "остальных файлов и не должно откатывать уже выполненные перемещения — файловая "
        "система не умеет так же атомарно откатывать группу операций, как это делает база "
        "данных. Поэтому <code class=\"inline\">apply_plan()</code> обрабатывает каждое "
        "перемещение независимо и в конце возвращает честный отчёт о том, что реально "
        "произошло с каждым файлом.",
    )}

    <p>Обратите внимание на проверку <code class="inline">destination.exists()</code> прямо
    перед перемещением, хотя планировщик уже избегал этого конфликта на этапе построения плана
    (раздел 23.14). Между построением плана и его выполнением на диске мог появиться новый
    файл — например, если пользователь сам что-то туда положил в этот момент. Без повторной
    проверки <code class="inline">shutil.move()</code> в системах на основе POSIX молча
    перезаписал бы такой файл — а SafeSort не перезаписывает файлы молча ни при каких
    обстоятельствах.</p>

    {code_block(
        "Терминал",
        "$ safesort apply ~/Downloads\n"
        "Applied 12 moves.\n"
        "Manifest written to:\n"
        ".safesort/history/20260824T011640800152.json\n",
        lang="text",
    )}

    {local_required_card(
        "23-13",
        "Практика: перемещаем файлы во временном каталоге",
        "Нужен доступ к настоящей файловой системе — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/23-13/index.html",
    )}
    """
    out = render_page(
        page_title="Безопасно перемещаем файлы",
        description="apply_plan() — единственная функция SafeSort, которая перемещает файлы, с повторной проверкой перед каждым перемещением.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Перемещение файлов", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Безопасно перемещаем файлы",
        lede="Одна функция во всей программе имеет право перемещать файлы — и делает это только после повторной проверки на конфликт.",
        body_html=body,
        sidebar_groups=sidebar("23-13-peremeshaem-fajly.html"),
        nav=PageNav(prev_href="23-12-predvaritelnyj-prosmotr.html", prev_label="Предварительный просмотр", next_href="23-14-imya-zanyato.html", next_label="Если имя уже занято"),
    )
    write("23-13-peremeshaem-fajly.html", out)


def build_14() -> None:
    body = f"""
    <p>Два файла с одинаковым именем могут попасть в одну и ту же категорию — например, два
    разных <code class="inline">otchet.pdf</code> из разных подкаталогов исходного каталога.
    SafeSort никогда не решает эту ситуацию перезаписью: вместо этого он находит свободное
    имя по понятной схеме.</p>

    {code_block(
        "src/safesort/planner.py",
        'def _resolve_collision(candidate: Path, reserved: set[Path]) -> Path:\n'
        '    if candidate not in reserved and not candidate.exists():\n'
        '        return candidate\n\n'
        '    stem, suffix, parent = candidate.stem, candidate.suffix, candidate.parent\n'
        '    counter = 1\n'
        '    while True:\n'
        '        alternative = parent / f"{stem} ({counter}){suffix}"\n'
        '        if alternative not in reserved and not alternative.exists():\n'
        '            return alternative\n'
        '        counter += 1\n',
    )}

    {code_block(
        "Пример",
        "otchet.pdf уже существует в Sorted/documents/\n"
        "→ следующий otchet.pdf получит имя otchet (1).pdf\n"
        "→ если и оно занято — otchet (2).pdf, и так далее\n",
        lang="text",
    )}

    {callout(
        "info",
        "reserved — конфликты внутри одного плана, не только на диске",
        "Проверки <code class=\"inline\">not candidate.exists()</code> достаточно для "
        "конфликта с уже существующим файлом на диске — но не для случая, когда <em>два "
        "файла из одного и того же плана</em> претендуют на одинаковое имя одновременно, пока "
        "ни один из них ещё не перемещён. Множество <code class=\"inline\">reserved</code> "
        "запоминает уже занятые в этом плане имена, поэтому второй файл получит "
        "<code class=\"inline\">otchet (1).pdf</code>, даже если на диске пока нет ни "
        "одного <code class=\"inline\">otchet.pdf</code>.",
    )}

    {practice_card(
        "23-14",
        "Практика: безопасное имя при конфликте",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/23-14/index.html",
    )}
    """
    out = render_page(
        page_title="Что делать, если имя уже занято",
        description="_resolve_collision() находит свободное имя по схеме name (1).ext, никогда не перезаписывая существующий файл.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Конфликт имён", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Что делать, если имя уже занято",
        lede="Ни на диске, ни внутри одного плана два файла никогда не получат одинаковое имя назначения.",
        body_html=body,
        sidebar_groups=sidebar("23-14-imya-zanyato.html"),
        nav=PageNav(prev_href="23-13-peremeshaem-fajly.html", prev_label="Перемещение файлов", next_href="23-15-zhurnal-operacij.html", next_label="Журнал выполненных операций"),
    )
    write("23-14-imya-zanyato.html", out)


def build_15() -> None:
    body = f"""
    <p>Каждый успешный вызов <code class="inline">apply</code> оставляет след — файл-манифест
    в формате JSON, который описывает, что именно было сделано. Без этого журнала команда
    <code class="inline">undo</code> (раздел 23.16) не знала бы, что именно нужно отменить.</p>

    {code_block(
        ".safesort/history/20260824T011640800152.json",
        '{\n'
        '  "operation_id": "20260824T011640800152",\n'
        '  "root": "/home/anna/Downloads",\n'
        '  "timestamp": "2026-08-24T01:16:40",\n'
        '  "moves": [\n'
        '    {\n'
        '      "source": "/home/anna/Downloads/otchet.pdf",\n'
        '      "destination": "/home/anna/Downloads/Sorted/documents/otchet.pdf",\n'
        '      "completed": true,\n'
        '      "error": null\n'
        '    }\n'
        '  ]\n'
        "}\n",
        lang="json",
    )}

    <p>Путь до манифеста — не случайный: он предсказуемо строится из корня и идентификатора
    операции, а сам идентификатор — временна́я метка, отформатированная так, чтобы
    лексикографический порядок совпадал с хронологическим:</p>
    {code_block(
        "src/safesort/manifest.py",
        'def new_operation_id() -> str:\n'
        '    return datetime.now().strftime("%Y%m%dT%H%M%S%f")\n\n'
        'def history_dir(root: Path) -> Path:\n'
        '    return Path(root) / STATE_DIRNAME / "history"\n',
    )}

    {callout(
        "tip",
        "Почему именно такой формат идентификатора",
        "Строка вида <code class=\"inline\">20260824T011640800152</code> сортируется как "
        "текст точно в том же порядке, в каком операции происходили по времени. Это позволяет "
        "функции <code class=\"inline\">find_latest_manifest()</code> находить последнюю "
        "операцию простой сортировкой имён файлов, не читая содержимое каждого манифеста.",
    )}

    <p>Модели <code class="inline">Path</code> внутри программы нужно превратить в обычные
    строки, чтобы записать их в JSON — формат, у которого нет типа «путь». Это единственное
    место в SafeSort, где происходит такое преобразование в обе стороны.</p>

    {practice_card(
        "23-15",
        "Практика: манифест как обычный JSON",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/23-15/index.html",
    )}
    """
    out = render_page(
        page_title="Журнал выполненных операций",
        description="JSON-манифест каждого apply: operation_id, список перемещений и их статус — основа для undo.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Журнал операций", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Журнал выполненных операций",
        lede="Каждый apply записывает JSON-манифест того, что действительно произошло — это единственный источник данных для отмены.",
        body_html=body,
        sidebar_groups=sidebar("23-15-zhurnal-operacij.html"),
        nav=PageNav(prev_href="23-14-imya-zanyato.html", prev_label="Конфликт имён", next_href="23-16-otmena-operacii.html", next_label="Отмена последней операции"),
    )
    write("23-15-zhurnal-operacij.html", out)


def build_16() -> None:
    body = f"""
    <p>Команда <code class="inline">undo</code> находит последний манифест, читает список
    выполненных перемещений и возвращает файлы туда, откуда они были взяты. Здесь действует
    то же правило, что и во всей программе: <strong>ничего не перезаписывать молча</strong>.</p>

    {code_block(
        "src/safesort/manifest.py",
        'def undo(manifest: OperationManifest) -> UndoResult:\n'
        '    restored, conflicts = [], []\n'
        '    for move in manifest.moves:\n'
        '        if not move.completed:\n'
        '            continue\n'
        '        source, destination = move.source, move.destination\n\n'
        '        if source.exists() or source.is_symlink():\n'
        '            conflicts.append(UndoConflict(source, destination,\n'
        '                "a file already exists at the original location"))\n'
        '            continue\n\n'
        '        shutil.move(str(destination), str(source))\n'
        '        restored.append(CompletedMove(destination, source, completed=True))\n'
        '    return UndoResult(restored=tuple(restored), conflicts=tuple(conflicts))\n',
    )}

    {callout(
        "warning",
        "Отмена не восстанавливает то, чего не было выполнено",
        "Цикл проверяет <code class=\"inline\">if not move.completed: continue</code> — "
        "перемещения, которые не удались во время <code class=\"inline\">apply</code> "
        "(раздел 23.13), никогда не касались диска, и отменять для них нечего.",
    )}

    <h2>Конфликт при отмене — реальный сценарий</h2>
    <p>Представьте: SafeSort переместил <code class="inline">otchet.pdf</code> в
    <code class="inline">Sorted/documents/</code>, а затем пользователь вручную создал новый
    файл с тем же именем <code class="inline">otchet.pdf</code> на исходном месте. Если
    теперь вызвать <code class="inline">undo</code>, простое перемещение назад стёрло бы этот
    новый файл. Вместо этого SafeSort проверяет исходное место <em>перед</em> восстановлением
    и, если там уже что-то есть, отказывается восстанавливать именно этот файл — но
    продолжает отменять остальные, не затронутые конфликтом:</p>
    {code_block(
        "Терминал",
        "$ safesort undo\n"
        "Restored 4 moves.\n"
        "1 moves could not be restored:\n"
        "  Sorted/documents/otchet.pdf -> otchet.pdf: a file already exists at the original location\n",
        lang="text",
    )}

    {local_required_card(
        "23-16",
        "Практика: отмена и конфликт при восстановлении",
        "Нужен доступ к настоящей файловой системе — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/23-16/index.html",
    )}
    """
    out = render_page(
        page_title="Отмена последней операции",
        description="undo() восстанавливает файлы из последнего манифеста и отказывается перезаписывать, если на исходном месте что-то появилось.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Отмена операции", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Отмена последней операции",
        lede="undo восстанавливает файлы из журнала — и отказывается затирать то, что успело появиться на исходном месте.",
        body_html=body,
        sidebar_groups=sidebar("23-16-otmena-operacii.html"),
        nav=PageNav(prev_href="23-15-zhurnal-operacij.html", prev_label="Журнал операций", next_href="23-17-poisk-dublikatov.html", next_label="Поиск одинаковых файлов"),
    )
    write("23-16-otmena-operacii.html", out)


def build_17() -> None:
    body = f"""
    <p>Второй настоящий инструмент SafeSort — поиск файлов с одинаковым содержимым. Задача
    выглядит просто: если у двух файлов одинаковые байты, они дубликаты. Наивное решение —
    сравнить содержимое каждого файла с содержимым каждого другого — работает, но для тысяч
    файлов означает чтение каждого файла снова и снова.</p>

    {flow_diagram(
        [
            ("Все файлы", "список FileInfo от сканера"),
            ("Группировка по size", "файлы с уникальным размером сразу отбрасываются"),
            ("Хеш SHA-256", "только для файлов внутри одной группы размера"),
            ("Группировка по (size, digest)", "совпадение — кандидат в дубликаты"),
        ],
        caption="Поэтапный поиск дубликатов: дорогое хеширование делается только там, где оно может изменить ответ",
    )}

    {callout(
        "tip",
        "Файл с уникальным размером не может быть дубликатом",
        "Если размер файла не совпадает ни с одним другим файлом в просканированном каталоге, "
        "у него точно нет дубликата — и вычислять его хеш незачем. Эта проверка почти "
        "бесплатна (размер уже известен из <code class=\"inline\">FileInfo</code>), а "
        "экономит она ровно то, что дороже всего — чтение и хеширование содержимого файлов.",
    )}

    <p>Раздел 23.18 разбирает саму функцию хеширования, а раздел 23.19 — то, как результаты
    хеширования группируются в готовые группы дубликатов.</p>

    {summary_box("Коротко", [
        "Поиск дубликатов идёт в три этапа: сначала по размеру, потом по хешу, потом по паре (размер, хеш).",
        "Хеш вычисляется только для файлов, у которых уже нашёлся хотя бы один файл того же размера.",
        "duplicates() — read-only команда: она только сообщает о найденных группах, ничего не удаляя.",
    ])}
    """
    out = render_page(
        page_title="Поиск одинаковых файлов",
        description="Поэтапный поиск дубликатов: сначала по размеру, затем хеширование только внутри групп совпадающего размера.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Поиск дубликатов", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Поиск одинаковых файлов",
        lede="Дорогое хеширование содержимого делается только там, где оно действительно может изменить ответ — после отбора по размеру.",
        body_html=body,
        sidebar_groups=sidebar("23-17-poisk-dublikatov.html"),
        nav=PageNav(prev_href="23-16-otmena-operacii.html", prev_label="Отмена операции", next_href="23-18-sha256.html", next_label="SHA-256 и хеш файла"),
    )
    write("23-17-poisk-dublikatov.html", out)


def build_18() -> None:
    body = f"""
    <p><strong>Хеш-функция</strong> превращает содержимое файла произвольного размера в
    строку фиксированной длины — <strong>дайджест</strong>. SafeSort использует
    <strong>SHA-256</strong> из модуля <code class="inline">hashlib</code>: два файла с
    одинаковым содержимым всегда дают одинаковый дайджест SHA-256, а изменение хотя бы одного
    байта меняет его полностью и непредсказуемо.</p>

    {code_block(
        "src/safesort/duplicates.py",
        'def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:\n'
        '    digest = hashlib.sha256()\n'
        '    with path.open("rb") as file:\n'
        '        while chunk := file.read(chunk_size):\n'
        '            digest.update(chunk)\n'
        '    return digest.hexdigest()\n',
    )}

    {callout(
        "warning",
        "Хеширование — не шифрование",
        "SHA-256 нельзя обратить: из дайджеста невозможно восстановить исходное содержимое "
        "файла, и это не его задача. Хеш-функция отвечает на вопрос «одинаковое ли это "
        "содержимое», а не скрывает его — SafeSort использует SHA-256 исключительно для "
        "сравнения файлов, а не для защиты данных.",
    )}

    <h2>Зачем читать файл частями</h2>
    <p>Цикл <code class="inline">while chunk := file.read(chunk_size)</code> читает файл не
    целиком, а блоками по мегабайту, и каждый блок сразу добавляет к дайджесту через
    <code class="inline">digest.update()</code>. Если бы функция читала файл одним вызовом
    <code class="inline">file.read()</code>, для файла в несколько гигабайт программе
    пришлось бы держать в оперативной памяти всё его содержимое разом — при поэтапном чтении
    в памяти в любой момент находится только один блок, независимо от размера файла целиком.</p>

    {code_block(
        "Проверка вручную",
        ">>> from pathlib import Path\n"
        ">>> from safesort.duplicates import sha256_file\n"
        ">>> sha256_file(Path(\"otchet.pdf\"))\n"
        "'784cc58b2286b83f67f58ffb1968ca4b80d1d0615863ad9b1ce9c3d05666f4e'\n",
        lang="pycon",
    )}

    {practice_card(
        "23-17",
        "Практика: хеш содержимого по частям",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/23-17/index.html",
    )}
    """
    out = render_page(
        page_title="SHA-256 и хеш содержимого файла",
        description="sha256_file() читает файл блоками, а не целиком, вычисляя дайджест SHA-256 без загрузки всего файла в память.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("SHA-256", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="SHA-256 и хеш содержимого файла",
        lede="Одинаковое содержимое всегда даёт одинаковый дайджест SHA-256 — а поблочное чтение не требует держать в памяти весь файл разом.",
        body_html=body,
        sidebar_groups=sidebar("23-18-sha256.html"),
        nav=PageNav(prev_href="23-17-poisk-dublikatov.html", prev_label="Поиск дубликатов", next_href="23-19-gruppy-dublikatov.html", next_label="Находим группы дубликатов"),
    )
    write("23-18-sha256.html", out)


def build_19() -> None:
    body = f"""
    <p>С хеш-функцией из раздела 23.18 полный поиск дубликатов укладывается в одну функцию:
    сгруппировать файлы по размеру, внутри каждой группы посчитать хеш и снова сгруппировать —
    теперь уже по паре (размер, дайджест).</p>

    {code_block(
        "src/safesort/duplicates.py",
        'def find_duplicates(files: list[FileInfo]) -> list[DuplicateGroup]:\n'
        '    by_size = defaultdict(list)\n'
        '    for file in files:\n'
        '        by_size[file.size].append(file)\n\n'
        '    groups = []\n'
        '    for size, candidates in by_size.items():\n'
        '        if len(candidates) < 2:\n'
        '            continue\n'
        '        by_digest = defaultdict(list)\n'
        '        for candidate in candidates:\n'
        '            digest = sha256_file(candidate.path)\n'
        '            by_digest[digest].append(candidate)\n'
        '        for digest, matched in by_digest.items():\n'
        '            if len(matched) >= 2:\n'
        '                groups.append(DuplicateGroup(size=size, digest=digest, files=tuple(matched)))\n'
        '    return groups\n',
    )}

    {callout(
        "info",
        "Пустые файлы — тоже дубликаты друг друга",
        "Два файла нулевого размера побайтово идентичны: у обоих попросту нет байтов. "
        "<code class=\"inline\">find_duplicates()</code> не делает для этого случая никакого "
        "исключения — они естественно попадают в одну группу по размеру "
        "(<code class=\"inline\">0</code>) и в одну группу по дайджесту пустого содержимого. "
        "Раздел 23.26 проверяет это отдельным тестом.",
    )}

    <p>Реальный вывод команды <code class="inline">duplicates</code> для каталога с двумя
    одинаковыми файлами:</p>
    {code_block(
        "Терминал",
        "$ safesort duplicates ~/Downloads\n"
        "Found 1 duplicate group(s):\n"
        "Group 1: 2 files, 23 bytes each, sha256=784cc58b2286b83f67f58ffb1968ca4b80d1d0615863ad9b1ce9c3d05666f4e\n"
        "  /home/anna/Downloads/notes.txt\n"
        "  /home/anna/Downloads/copy_of_notes.txt\n",
        lang="text",
    )}

    {callout(
        "warning",
        "duplicates только сообщает — не удаляет",
        "Версия 0.1.0 не удаляет ни один файл из найденной группы, и в коде "
        "<code class=\"inline\">find_duplicates()</code> нет ни одного вызова, который "
        "удаляет файлы — даже отключённого или закомментированного. Автоматическое удаление "
        "дубликатов сознательно вынесено за рамки версии (раздел 23.1): решение о том, какой "
        "из одинаковых файлов оставить, требует контекста, которого у программы нет.",
    )}

    {practice_card(
        "23-18",
        "Практика: группируем файлы в дубликаты",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/23-18/index.html",
    )}
    """
    out = render_page(
        page_title="Находим группы дубликатов",
        description="find_duplicates() группирует файлы сначала по размеру, затем по дайджесту — с зеркальным правилом для пустых файлов.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Группы дубликатов", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Находим группы дубликатов",
        lede="Одна функция превращает список файлов в группы дубликатов — и никогда не удаляет ни одного файла сама.",
        body_html=body,
        sidebar_groups=sidebar("23-19-gruppy-dublikatov.html"),
        nav=PageNav(prev_href="23-18-sha256.html", prev_label="SHA-256", next_href="23-20-oshibki-fajlovoj-sistemy.html", next_label="Ошибки файловой системы"),
    )
    write("23-19-gruppy-dublikatov.html", out)


def build_20() -> None:
    body = f"""
    <p>Реальная файловая система непредсказуема: файл может исчезнуть между сканированием и
    чтением, доступ к каталогу может быть запрещён, диск может оказаться неисправен. Python
    сообщает о таких ситуациях через конкретные классы исключений, и SafeSort ловит именно
    их — не всё подряд.</p>

    {comparison_table(
        ["Исключение", "Когда возникает", "Как реагирует SafeSort"],
        [
            ["FileNotFoundError", "Файл или каталог исчез между шагами", "Пропускает эту запись, продолжает остальные"],
            ["PermissionError", "Недостаточно прав для чтения или записи", "Пропускает эту запись, пишет предупреждение в журнал"],
            ["OSError", "Общая ошибка файловой системы (например, диск переполнен)", "Пропускает эту запись, продолжает остальные"],
        ],
    )}

    {callout(
        "warning",
        "except Exception — не решение",
        "Перехват <code class=\"inline\">except Exception: pass</code> проглотил бы не только "
        "ожидаемые ошибки файловой системы, но и настоящие ошибки в самой программе — "
        "например, опечатку в имени переменной, — и программа продолжила бы работать, как ни "
        "в чём не бывало, скрывая реальную проблему. SafeSort перехватывает только те "
        "исключения, которые действительно ожидает в конкретном месте: "
        "<code class=\"inline\">FileNotFoundError</code>, <code class=\"inline\">"
        "PermissionError</code>, <code class=\"inline\">OSError</code> — и ни разу не "
        "перехватывает исключения без указания типа.",
    )}

    <p>Пример из <code class="inline">scanner.py</code> — чтение каталога, для которого может
    не быть прав доступа:</p>
    {code_block(
        "src/safesort/scanner.py",
        "try:\n"
        "    entries = list(directory.iterdir())\n"
        "except PermissionError:\n"
        '    logger.warning("Permission denied, skipping directory: %s", directory)\n'
        "    return\n"
        "except FileNotFoundError:\n"
        '    logger.warning("Directory vanished during scan, skipping: %s", directory)\n'
        "    return\n"
        "except OSError as exc:\n"
        '    logger.warning("Could not read directory %s: %s", directory, exc)\n'
        "    return\n",
    )}

    <p>Каждая ветка перехватывает свой конкретный случай, пишет понятное сообщение в журнал
    (раздел 23.21 объясняет, что такое этот журнал) и возвращает управление — сканирование
    остальных каталогов продолжается как ни в чём не бывало.</p>

    {summary_box("Коротко", [
        "SafeSort перехватывает конкретные ожидаемые исключения — FileNotFoundError, "
        "PermissionError, OSError — а не всё подряд.",
        "Каждый перехват сопровождается сообщением в журнал, а не молчаливым игнорированием.",
        "Ошибка на одном файле или каталоге не должна останавливать обработку остальных.",
    ])}
    """
    out = render_page(
        page_title="Обрабатываем ошибки файловой системы",
        description="SafeSort перехватывает конкретные исключения — FileNotFoundError, PermissionError, OSError — а не всё подряд.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Ошибки файловой системы", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Обрабатываем ошибки файловой системы",
        lede="Конкретные исключения вместо except Exception: программа не скрывает реальные ошибки, а обрабатывает только ожидаемые.",
        body_html=body,
        sidebar_groups=sidebar("23-20-oshibki-fajlovoj-sistemy.html"),
        nav=PageNav(prev_href="23-19-gruppy-dublikatov.html", prev_label="Группы дубликатов", next_href="23-21-logging.html", next_label="Журнал работы программы"),
    )
    write("23-20-oshibki-fajlovoj-sistemy.html", out)


def build_21() -> None:
    body = f"""
    <p>В коде SafeSort уже несколько раз встречался вызов <code class="inline">logger.warning
    (...)</code>. Это не то же самое, что вывод на экран через <code class="inline">print()
    </code>: у программы есть два разных канала сообщений с разным назначением.</p>

    {comparison_table(
        ["", "Пользовательский вывод (print)", "Журнал (logging)"],
        [
            ["Кому адресован", "Человеку, который вызвал команду", "Тому, кто разбирается, что произошло внутри"],
            ["Что показывает", "Итог команды — сколько файлов, сколько перемещений", "Диагностику: пропущенные файлы, ошибки доступа"],
            ["Формат", "Короткий, фиксированный", "Уровень важности + подробности"],
        ],
    )}

    {code_block(
        "src/safesort/cli.py",
        'def _configure_logging() -> None:\n'
        '    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")\n',
    )}

    <p>SafeSort использует три уровня важности, каждый для своей ситуации:</p>
    {comparison_table(
        ["Уровень", "Когда используется в SafeSort"],
        [
            ["INFO", "Обычные события: файл перемещён, символическая ссылка пропущена"],
            ["WARNING", "Что-то пропущено, но программа продолжает работать: каталог недоступен"],
            ["ERROR", "Операция не удалась: перемещение или восстановление не выполнено"],
        ],
    )}

    {callout(
        "tip",
        "Модуль получает logger по своему имени",
        "Каждый файл начинается со строки <code class=\"inline\">logger = logging.getLogger("
        "__name__)</code> — так сообщения журнала автоматически помечены тем модулем, откуда "
        "они пришли (<code class=\"inline\">safesort.scanner</code>, "
        "<code class=\"inline\">safesort.executor</code> и так далее), и не нужно вручную "
        "добавлять эту информацию в каждое сообщение.",
    )}

    {summary_box("Коротко", [
        "Пользовательский вывод (print) и диагностический журнал (logging) — два разных канала "
        "с разным назначением, их не стоит смешивать.",
        "Три уровня важности — INFO, WARNING, ERROR — покрывают всё, что нужно SafeSort, без "
        "избыточной настройки.",
        "logging.getLogger(__name__) в каждом модуле помечает сообщения тем модулем, откуда они пришли.",
    ])}
    """
    out = render_page(
        page_title="Добавляем журнал работы программы",
        description="logging отдельно от пользовательского вывода: три уровня важности — INFO, WARNING, ERROR.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Журнал программы", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Добавляем журнал работы программы",
        lede="Итог для пользователя печатается напрямую; диагностика идёт отдельным каналом — через модуль logging.",
        body_html=body,
        sidebar_groups=sidebar("23-21-logging.html"),
        nav=PageNav(prev_href="23-20-oshibki-fajlovoj-sistemy.html", prev_label="Ошибки файловой системы", next_href="23-22-nastrojki-proekta.html", next_label="Настройки проекта"),
    )
    write("23-21-logging.html", out)


def build_22() -> None:
    body = f"""
    <p>Категории по умолчанию и каталог результата подходят для большинства случаев, но
    иногда их стоит настроить — например, добавить свою категорию или изменить имя каталога
    результата. SafeSort ищет необязательный файл <code class="inline">safesort.toml</code>
    прямо в корне сканируемого каталога:</p>

    {code_block(
        "safesort.toml",
        'destination = "Sorted"\n'
        'exclude = [".git", ".venv"]\n\n'
        '[extensions]\n'
        'documents = [".pdf", ".docx", ".txt"]\n'
        'images = [".jpg", ".jpeg", ".png", ".webp"]\n',
    )}

    {callout(
        "info",
        "Ни одна команда SafeSort не требует файла настроек",
        "Если <code class=\"inline\">safesort.toml</code> не найден, в дело идут встроенные "
        "значения по умолчанию — программа работает предсказуемо и без единой строчки "
        "настроек. Файл конфигурации — это возможность что-то переопределить, а не "
        "обязательное условие для запуска.",
    )}

    <p>Чтение файла использует <code class="inline">tomllib</code> — модуль стандартной
    библиотеки Python для разбора TOML, доступный только на чтение:</p>
    {code_block(
        "src/safesort/config.py",
        'def load_config(root: Path) -> Config:\n'
        '    config_path = root / "safesort.toml"\n'
        '    if not config_path.is_file():\n'
        '        return Config()\n\n'
        '    try:\n'
        '        with config_path.open("rb") as handle:\n'
        '            raw = tomllib.load(handle)\n'
        '    except tomllib.TOMLDecodeError as exc:\n'
        '        raise ConfigError(f"Could not parse config file {config_path}: {exc}") from exc\n'
        "    # ...\n",
    )}

    {callout(
        "warning",
        "tomllib.load() принимает открытый файл в бинарном режиме",
        "Обратите внимание на <code class=\"inline\">open(\"rb\")</code>, а не "
        "<code class=\"inline\">open(\"r\")</code>: <code class=\"inline\">tomllib</code> "
        "сам решает, как декодировать байты файла в текст согласно спецификации TOML, "
        "поэтому ожидает на входе именно бинарный поток, а не уже прочитанную строку.",
    )}

    <p>Если файл настроек существует, но содержит некорректный TOML, SafeSort не пытается
    угадать намерение пользователя — он поднимает понятную ошибку <code class="inline">
    ConfigError</code> с указанием файла и причины, вместо того чтобы либо упасть с
    трудночитаемой трассировкой, либо молча продолжить с настройками по умолчанию.</p>

    {practice_card(
        "23-19",
        "Практика: читаем и проверяем TOML-настройки",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/23-19/index.html",
    )}
    """
    out = render_page(
        page_title="Настройки проекта",
        description="Необязательный файл safesort.toml переопределяет каталог результата, исключения и категории через tomllib.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Настройки проекта", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Настройки проекта",
        lede="Файл настроек необязателен: без него в силу вступают встроенные значения по умолчанию, а с ним можно переопределить часть поведения.",
        body_html=body,
        sidebar_groups=sidebar("23-22-nastrojki-proekta.html"),
        nav=PageNav(prev_href="23-21-logging.html", prev_label="Журнал программы", next_href="23-23-pervye-testy.html", next_label="Первые автоматические тесты"),
    )
    write("23-22-nastrojki-proekta.html", out)


def build_23() -> None:
    body = f"""
    <p>Код SafeSort уже написан, но откуда известно, что он работает правильно — не только
    сейчас, но и после следующей правки? Ответ — автоматические тесты: код, который проверяет
    другой код и сообщает, если поведение изменилось незаметно для человека.</p>

    {code_block(
        "Терминал (окружение активировано)", "pip install -e .[dev]\npytest tests/ -v", lang="text",
    )}

    {callout(
        "warning",
        "Тесты файловой системы никогда не используют настоящие пользовательские каталоги",
        "Тест, который вызывает <code class=\"inline\">apply</code> прямо на "
        "<code class=\"inline\">~/Downloads</code>, при первом же неудачном запуске способен "
        "испортить реальные файлы. Все тесты SafeSort работают внутри временного каталога, "
        "который pytest создаёт и удаляет сам, через встроенную функцию "
        "<code class=\"inline\">tmp_path</code> — она передаётся тестовой функции как обычный "
        "параметр:",
    )}

    {code_block(
        "tests/test_classifier.py",
        'from safesort.classifier import classify\n'
        'from safesort.config import DEFAULT_EXTENSIONS\n\n'
        'def test_classify_known_extension():\n'
        '    assert classify(".pdf", DEFAULT_EXTENSIONS) == "documents"\n\n'
        'def test_classify_unknown_extension_is_other():\n'
        '    assert classify(".xyz", DEFAULT_EXTENSIONS) == "other"\n',
    )}

    <p>Функция <code class="inline">classify()</code> — хороший первый тест не случайно: она
    чистая, не трогает файловую систему и не зависит ни от чего внешнего. Раздел 23.24 берётся
    за более сложные тесты — те, что действительно создают файлы во временном каталоге.</p>

    {summary_box("Коротко", [
        "Тест — код, который проверяет код: запускает функцию и сравнивает результат с ожидаемым.",
        "tmp_path — временный каталог, который pytest создаёт и удаляет для каждого теста сам.",
        "Ни один тест SafeSort не обращается к настоящему пользовательскому каталогу вроде ~/Downloads.",
    ])}
    """
    out = render_page(
        page_title="Пишем первые автоматические тесты",
        description="pytest и tmp_path: первые тесты SafeSort проверяют классификатор, не трогая файловую систему.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Первые тесты", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Пишем первые автоматические тесты",
        lede="Тесты SafeSort работают только во временном каталоге pytest — ни один из них не трогает настоящие пользовательские файлы.",
        body_html=body,
        sidebar_groups=sidebar("23-23-pervye-testy.html"),
        nav=PageNav(prev_href="23-22-nastrojki-proekta.html", prev_label="Настройки проекта", next_href="23-24-testy-skanirovaniya.html", next_label="Тесты сканирования"),
    )
    write("23-23-pervye-testy.html", out)


def build_24() -> None:
    body = f"""
    <p>Тесты для <code class="inline">scan()</code> и <code class="inline">classify()</code>
    вместе создают маленькую, полностью контролируемую файловую структуру во временном
    каталоге, а затем проверяют, что сканер нашёл именно те файлы, которые туда положили —
    ни больше, ни меньше.</p>

    {code_block(
        "tests/test_scanner.py",
        'def test_scan_finds_nested_files(tmp_path):\n'
        '    (tmp_path / "a").mkdir()\n'
        '    (tmp_path / "a" / "otchet.pdf").write_text("...")\n'
        '    (tmp_path / "photo.jpg").write_text("...")\n\n'
        '    files = scan(tmp_path, Config())\n'
        '    names = {f.path.name for f in files}\n'
        '    assert names == {"otchet.pdf", "photo.jpg"}\n\n'
        'def test_scan_skips_destination_directory(tmp_path):\n'
        '    (tmp_path / "Sorted" / "documents").mkdir(parents=True)\n'
        '    (tmp_path / "Sorted" / "documents" / "staryj.pdf").write_text("...")\n\n'
        '    files = scan(tmp_path, Config())\n'
        '    assert files == []\n',
    )}

    {callout(
        "tip",
        "Пустой каталог — тоже проверяемый случай",
        "Тест на пустом временном каталоге (без единого файла) кажется тривиальным, но именно "
        "такие крайние случаи чаще всего ломаются при рефакторинге: убедиться, что "
        "<code class=\"inline\">scan()</code> возвращает пустой список, а не падает с "
        "ошибкой, — простой, но реальный тест.",
    )}

    <p>Второй тест выше — прямая проверка требования из раздела 23.9: каталог результата
    никогда не сканируется повторно. Без такого теста регресс (случайный возврат старой,
    неправильной логики) остался бы незамеченным до тех пор, пока кто-то не запустил бы
    SafeSort дважды подряд на одном каталоге и не увидел странный результат вручную.</p>

    {local_required_card(
        "23-21",
        "Практика: тестируем сканер и классификатор",
        "Нужен доступ к настоящей файловой системе — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/23-21/index.html",
    )}
    """
    out = render_page(
        page_title="Проверяем сканирование и классификацию",
        description="Тесты для scan() создают контролируемую структуру во временном каталоге и проверяют её результат, включая исключение каталога результата.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Тесты сканирования", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Проверяем сканирование и классификацию",
        lede="Тест на пустом каталоге и тест на повторное сканирование Sorted/ — простые случаи, которые чаще всего ломаются незаметно.",
        body_html=body,
        sidebar_groups=sidebar("23-24-testy-skanirovaniya.html"),
        nav=PageNav(prev_href="23-23-pervye-testy.html", prev_label="Первые тесты", next_href="23-25-testy-peremeshheniya.html", next_label="Тесты перемещения и отмены"),
    )
    write("23-24-testy-skanirovaniya.html", out)


def build_25() -> None:
    body = f"""
    <p>Проверить перемещение файлов сложнее, чем проверить чистую функцию: нужно создать
    файлы, применить план, убедиться, что они оказались в новом месте, и только потом
    проверить отмену. Каждый шаг проверяется отдельным тестом, а не одним большим сценарием —
    так гораздо понятнее, что именно сломалось, если тест не проходит.</p>

    {code_block(
        "tests/test_executor.py",
        'def test_apply_plan_moves_file_to_destination(tmp_path):\n'
        '    source = tmp_path / "otchet.pdf"\n'
        '    source.write_text("...")\n'
        '    destination = tmp_path / "Sorted" / "documents" / "otchet.pdf"\n'
        '    plan = SortPlan(root=tmp_path, operations=(MoveOperation(source, destination),))\n\n'
        '    results = apply_plan(plan)\n\n'
        '    assert results[0].completed is True\n'
        '    assert not source.exists()\n'
        '    assert destination.exists()\n',
    )}

    <p>Тест отмены строит план, применяет его, затем вызывает <code class="inline">undo()</code>
    и проверяет, что файл оказался в точности там, откуда был взят:</p>
    {code_block(
        "tests/test_manifest.py",
        'def test_undo_restores_original_location(tmp_path):\n'
        '    source = tmp_path / "otchet.pdf"\n'
        '    source.write_text("...")\n'
        '    plan = build_plan(scan(tmp_path, Config()), tmp_path, Config())\n'
        '    moves = apply_plan(plan)\n'
        '    manifest_obj, _ = write_manifest(tmp_path, moves)\n\n'
        '    result = undo(manifest_obj)\n\n'
        '    assert source.exists()\n'
        '    assert result.conflicts == ()\n',
    )}

    {callout(
        "warning",
        "Тест конфликта отмены — не менее важен, чем тест успешной отмены",
        "Одного теста «отмена работает» недостаточно: нужен ещё тест, который специально "
        "создаёт конфликт — кладёт новый файл на исходное место перед вызовом "
        "<code class=\"inline\">undo()</code> — и проверяет, что SafeSort отказался его "
        "перезаписать, а не проверяет только «счастливый путь».",
    )}

    {local_required_card(
        "23-20",
        "Практика: тестируем перемещение и отмену",
        "Нужен доступ к настоящей файловой системе — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/23-20/index.html",
    )}
    """
    out = render_page(
        page_title="Проверяем перемещение и отмену",
        description="Тесты apply_plan() и undo(): успешное перемещение, полная отмена и отдельный тест на конфликт при восстановлении.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Тесты перемещения", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Проверяем перемещение и отмену",
        lede="Каждый шаг — перемещение, отмену, конфликт при отмене — проверяет отдельный тест, а не один общий сценарий.",
        body_html=body,
        sidebar_groups=sidebar("23-25-testy-peremeshheniya.html"),
        nav=PageNav(prev_href="23-24-testy-skanirovaniya.html", prev_label="Тесты сканирования", next_href="23-26-testy-dublikatov.html", next_label="Тесты поиска дубликатов"),
    )
    write("23-25-testy-peremeshheniya.html", out)


def build_26() -> None:
    body = f"""
    <p>Тесты для <code class="inline">find_duplicates()</code> проверяют не только «типичный»
    случай двух одинаковых файлов, но и два крайних случая, которые легко упустить: файлы
    нулевого размера и по-настоящему большой файл.</p>

    {code_block(
        "tests/test_duplicates.py",
        'def test_identical_content_files_are_grouped(tmp_path):\n'
        '    a = tmp_path / "notes.txt"\n'
        '    b = tmp_path / "copy_of_notes.txt"\n'
        '    a.write_text("тот же текст")\n'
        '    b.write_text("тот же текст")\n\n'
        '    groups = find_duplicates(scan(tmp_path, Config()))\n\n'
        '    assert len(groups) == 1\n'
        '    assert len(groups[0].files) == 2\n\n'
        'def test_empty_files_are_duplicates_of_each_other(tmp_path):\n'
        '    (tmp_path / "a.txt").write_text("")\n'
        '    (tmp_path / "b.txt").write_text("")\n\n'
        '    groups = find_duplicates(scan(tmp_path, Config()))\n\n'
        '    assert len(groups) == 1\n'
        '    assert groups[0].size == 0\n',
    )}

    {callout(
        "tip",
        "Большой файл в тесте — несколько мегабайт, а не гигабайты",
        "Проверить, что <code class=\"inline\">sha256_file()</code> действительно читает файл "
        "по частям, а не целиком, можно файлом всего в несколько мегабайт — заметно больше "
        "одного блока чтения, но при этом тест выполняется за доли секунды. Гигабайтные файлы "
        "в тестах замедлили бы весь набор тестов без дополнительной пользы.",
    )}

    {code_block(
        "tests/test_duplicates.py",
        'def test_sha256_hashes_large_file_incrementally(tmp_path):\n'
        '    data = b"x" * (5 * 1024 * 1024)  # 5 МБ — больше одного блока чтения\n'
        '    path = tmp_path / "bolshoj_fajl.bin"\n'
        '    path.write_bytes(data)\n\n'
        '    assert sha256_file(path) == hashlib.sha256(data).hexdigest()\n',
    )}

    {practice_card(
        "23-22",
        "Практика: тесты дубликатов и пустых файлов",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/23-22/index.html",
    )}
    """
    out = render_page(
        page_title="Проверяем поиск дубликатов",
        description="Тесты find_duplicates(): одинаковое содержимое, пустые файлы как дубликаты друг друга, инкрементальное хеширование большого файла.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Тесты дубликатов", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Проверяем поиск дубликатов",
        lede="Два крайних случая — пустые файлы и по-настоящему большой файл — проверяют то, что типичный тест на паре файлов не заметит.",
        body_html=body,
        sidebar_groups=sidebar("23-26-testy-dublikatov.html"),
        nav=PageNav(prev_href="23-25-testy-peremeshheniya.html", prev_label="Тесты перемещения", next_href="23-27-testy-cli.html", next_label="Тесты интерфейса командной строки"),
    )
    write("23-26-testy-dublikatov.html", out)


def build_27() -> None:
    body = f"""
    <p>Последний слой SafeSort, который стоит проверить тестами, — сама командная строка:
    правильно ли <code class="inline">argparse</code> разбирает аргументы, и правильный ли код
    возврата получает вызывающая сторона.</p>

    {code_block(
        "tests/test_cli.py",
        'def test_scan_subcommand_returns_zero_on_success(tmp_path, capsys):\n'
        '    (tmp_path / "otchet.pdf").write_text("...")\n\n'
        '    code = main(["scan", str(tmp_path)])\n\n'
        '    assert code == 0\n'
        '    assert "Files scanned: 1" in capsys.readouterr().out\n\n'
        'def test_missing_path_returns_nonzero(tmp_path):\n'
        '    code = main(["scan", str(tmp_path / "net-takogo-kataloga")])\n\n'
        '    assert code != 0\n',
    )}

    {callout(
        "info",
        "capsys — встроенная перехватка вывода pytest",
        "Функция <code class=\"inline\">main()</code> печатает результат через "
        "<code class=\"inline\">print()</code>, а не возвращает текст напрямую — фикстура "
        "<code class=\"inline\">capsys</code> перехватывает всё, что попало на стандартный "
        "вывод и поток ошибок во время теста, и позволяет проверить это как обычную строку.",
    )}

    <p>Проверка <code class="inline">--help</code> тоже заслуживает отдельного теста: она
    ловит ситуацию, когда кто-то случайно удаляет описание подкоманды или ломает сам разбор
    аргументов — <code class="inline">argparse</code> в этом случае завершает программу с
    ошибкой ещё до того, как выполнится хоть одна строка логики SafeSort.</p>

    {practice_card(
        "23-23",
        "Практика: тесты аргументов командной строки",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/23-23/index.html",
    )}
    """
    out = render_page(
        page_title="Проверяем интерфейс командной строки",
        description="Тесты cli.main(): код возврата, разбор аргументов и перехват вывода через capsys.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Тесты интерфейса", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Проверяем интерфейс командной строки",
        lede="capsys перехватывает то, что программа напечатала, — и тесты проверяют это как обычную строку, без реального терминала.",
        body_html=body,
        sidebar_groups=sidebar("23-27-testy-cli.html"),
        nav=PageNav(prev_href="23-26-testy-dublikatov.html", prev_label="Тесты дубликатов", next_href="23-28-git-kommit.html", next_label="Git: от изменения к коммиту"),
    )
    write("23-27-testy-cli.html", out)


def build_28() -> None:
    body = f"""
    <p>Код SafeSort готов и проверен тестами — самое время сохранить его в истории Git.
    Между «файл изменён на диске» и «изменение сохранено в истории» есть два промежуточных
    шага, и понимание разницы между ними экономит немало недоумения в будущем.</p>

    {flow_diagram(
        [
            ("Рабочее дерево", "файлы на диске — то, что видит текстовый редактор"),
            ("Индекс", "изменения, отмеченные командой git add — «черновик» будущего коммита"),
            ("Коммит", "сохранённый снимок индекса — постоянная запись в истории"),
        ],
        caption="git add переносит изменение из рабочего дерева в индекс; git commit фиксирует содержимое индекса в истории",
    )}

    {code_block(
        "Терминал",
        "git status\n"
        "git diff\n"
        "git add src/safesort/duplicates.py tests/test_duplicates.py\n"
        "git commit -m \"feat: add duplicate-file detection\"\n",
        lang="text",
    )}

    {callout(
        "tip",
        "git diff — что именно изменилось, а не только какие файлы",
        "<code class=\"inline\">git status</code> перечисляет изменённые файлы, но не "
        "показывает содержимое изменений. <code class=\"inline\">git diff</code> показывает "
        "построчно, что именно добавлено и что удалено — стоит прочитать его перед каждым "
        "коммитом, чтобы случайно не закоммитить что-то лишнее: отладочный "
        "<code class=\"inline\">print()</code>, забытый файл с личными данными, временный код.",
    )}

    <h2>Логические коммиты</h2>
    <p>Один коммит должен описывать одно законченное, осмысленное изменение — а не «конец
    рабочего дня» или случайный набор всего, что накопилось. Сравните:</p>
    {comparison_table(
        ["Хорошо", "Плохо"],
        [
            ["feat: add directory scanner", "update"],
            ["feat: add dry-run sort planning", "fix"],
            ["test: cover undo conflicts", "stuff"],
            ["docs: document SafeSort 0.1.0", "final-final"],
        ],
    )}

    {callout(
        "info",
        "git add . — не единственный и не всегда лучший способ",
        "<code class=\"inline\">git add .</code> добавляет в индекс вообще все изменения в "
        "текущем каталоге разом — удобно, когда коммит действительно должен включать всё, но "
        "легко случайно затянуть в коммит что-то не относящееся к делу. "
        "<code class=\"inline\">git add путь/к/файлу</code> добавляет только нужные файлы и "
        "делает коммиты более осмысленными.",
    )}

    {local_required_card(
        "23-24",
        "Практика: читаем git diff и группируем изменения",
        "Нужен настоящий Git-репозиторий — выполните локально в VS Code, PyCharm или терминале",
        "../../practice/23-24/index.html",
    )}
    """
    out = render_page(
        page_title="Git: от рабочего изменения к коммиту",
        description="Рабочее дерево, индекс и коммит; git diff перед коммитом; логические коммиты вместо «update» и «fix».",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Git и коммит", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Git: от рабочего изменения к коммиту",
        lede="git add переносит изменение в индекс, git commit фиксирует его в истории — а хороший коммит описывает одно законченное изменение.",
        body_html=body,
        sidebar_groups=sidebar("23-28-git-kommit.html"),
        nav=PageNav(prev_href="23-27-testy-cli.html", prev_label="Тесты интерфейса", next_href="23-29-github-pr.html", next_label="GitHub: Issue, ветка и Pull Request"),
    )
    write("23-28-git-kommit.html", out)


def build_29() -> None:
    body = f"""
    <p>История коммитов в разделе 23.28 пока существует только в локальном репозитории — на
    одном компьютере. GitHub хранит удалённую копию этой истории и добавляет вокруг неё
    рабочий процесс, рассчитанный на совместную разработку: Issue, ветки и Pull Request.</p>

    {flow_diagram(
        [
            ("Issue", "описание задачи или найденной проблемы"),
            ("Ветка", "изолированное место для изменений по этой задаче"),
            ("Коммиты", "сохранённые шаги работы в этой ветке"),
            ("Pull Request", "предложение перенести изменения ветки в main"),
            ("Проверка и слияние", "код проверен, затем объединён с основной веткой"),
        ],
        caption="От постановки задачи до слияния кода: путь одного изменения на GitHub",
    )}

    <h2>Issue — формулировка задачи</h2>
    <p><strong>Issue</strong> — запись на GitHub, описывающая задачу, найденную проблему или
    предложение. Прежде чем писать код для новой возможности, полезно кратко сформулировать,
    что именно нужно сделать и как проверить, что это сделано:</p>
    {code_block(
        "Issue: Add duplicate-file detection",
        "## Problem\n\n"
        "SafeSort не умеет находить файлы с одинаковым содержимым.\n\n"
        "## Expected behavior\n\n"
        "Команда `safesort duplicates ROOT` должна вывести группы файлов с "
        "одинаковым содержимым, не изменяя ни одного файла.\n\n"
        "## Acceptance criteria\n\n"
        "- [ ] Файлы группируются по (размер, SHA-256)\n"
        "- [ ] Хеш вычисляется только для файлов с совпадающим размером\n"
        "- [ ] Команда ничего не удаляет\n"
        "- [ ] Есть тесты на пустые файлы и на настоящие дубликаты\n",
        lang="markdown",
    )}

    <h2>Ветка — изолированное место для изменений</h2>
    <p><strong>Ветка</strong> (branch) — независимая линия истории, отходящая от
    <code class="inline">main</code>. Пока изменения делаются в отдельной ветке, основная
    ветка репозитория остаётся нетронутой и всегда содержит последнюю рабочую версию:</p>
    {code_block(
        "Терминал",
        "git switch -c feat/duplicate-detection\n"
        "# ...пишем код и тесты, коммитим изменения...\n"
        "git push -u origin feat/duplicate-detection\n",
        lang="text",
    )}

    <h2>Pull Request — предложение изменений</h2>
    <p><strong>Pull Request</strong> (PR) — предложение перенести изменения из одной ветки в
    другую, обычно из рабочей ветки в <code class="inline">main</code>. PR не «сливает» код
    автоматически: он открывает изменения для просмотра, автоматических проверок (раздел
    23.30) и обсуждения, прежде чем код попадёт в основную ветку.</p>

    {image_figure(
        f"{IMG}/29-pr-checks.png",
        "Открытый Pull Request на GitHub с зелёной галочкой пройденной проверки и вкладкой Files changed",
        "Реальный Pull Request с прошедшей автоматической проверкой — тот же рабочий процесс, что описан в этом разделе: ветка, изменения, проверка, слияние.",
        size="wide",
    )}

    {callout(
        "info",
        "PR можно открыть раньше, чем код готов полностью",
        "Pull Request не обязан представлять уже законченную работу — его можно открыть "
        "раньше, чтобы обсудить подход или получить промежуточный отзыв, и явно пометить как "
        "черновик. Ожидание «пока всё не будет идеально» не единственный способ работать с "
        "Pull Request.",
    )}

    {summary_box("Коротко", [
        "Issue формулирует задачу до того, как написан код — так проще понять, что именно "
        "нужно сделать и как проверить результат.",
        "Ветка изолирует работу над одной задачей, оставляя main нетронутой до готовности.",
        "Pull Request открывает изменения для проверки и обсуждения перед слиянием в main — "
        "он не сливает код автоматически сам по себе.",
    ])}
    """
    out = render_page(
        page_title="GitHub: Issue, ветка и Pull Request",
        description="Issue формулирует задачу, ветка изолирует изменения, Pull Request открывает их для проверки перед слиянием в main.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Issue, ветка, PR", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="GitHub: Issue, ветка и Pull Request",
        lede="От формулировки задачи в Issue до предложения изменений через Pull Request — путь одного изменения на GitHub.",
        body_html=body,
        sidebar_groups=sidebar("23-29-github-pr.html"),
        nav=PageNav(prev_href="23-28-git-kommit.html", prev_label="Git и коммит", next_href="23-30-github-actions.html", next_label="GitHub Actions"),
    )
    write("23-29-github-pr.html", out)


def build_30() -> None:
    body = f"""
    <p>Проверять тесты вручную перед каждым Pull Request легко забыть. <strong>GitHub
    Actions</strong> — сервис, который автоматически выполняет заданные действия при
    определённых событиях в репозитории, например при каждом пуше или открытии Pull Request.
    Для SafeSort такое действие — запуск тестов.</p>

    {code_block(
        ".github/workflows/safesort-tests.yml",
        "name: SafeSort tests\n\n"
        "on:\n"
        "  push:\n"
        "    paths:\n"
        '      - "projects/python/safesort/**"\n'
        "  pull_request:\n"
        "    paths:\n"
        '      - "projects/python/safesort/**"\n\n'
        "jobs:\n"
        "  test:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - name: Check out repository\n"
        "        uses: actions/checkout@v7\n\n"
        "      - name: Set up Python\n"
        "        uses: actions/setup-python@v7\n"
        "        with:\n"
        '          python-version: "3.14"\n\n'
        "      - name: Install SafeSort with dev dependencies\n"
        '        run: pip install -e "projects/python/safesort/[dev]"\n\n'
        "      - name: Run tests\n"
        "        run: pytest projects/python/safesort/tests/\n",
        lang="yaml",
    )}

    {callout(
        "tip",
        "paths — не запускать проверку по любому поводу",
        "Ключ <code class=\"inline\">paths</code> ограничивает запуск: воркфлоу срабатывает "
        "только тогда, когда изменились файлы внутри "
        "<code class=\"inline\">projects/python/safesort/</code>. Без этого ограничения любое "
        "изменение в совершенно другой части репозитория запускало бы тесты SafeSort "
        "впустую.",
    )}

    <h2>Управляемая проверка: специально сломанный тест</h2>
    <p>Полезно один раз увидеть, как выглядит красная (неудачная) проверка — и как её
    исправить, — прежде чем столкнуться с этим впервые в реальной ситуации:</p>
    {flow_diagram(
        [
            ("Ломаем тест", "намеренно меняем ожидаемое значение на неверное"),
            ("Пушим ветку", "GitHub Actions запускается автоматически"),
            ("Красная проверка", "открываем журнал и видим точную причину падения"),
            ("Исправляем", "возвращаем правильное значение, коммитим"),
            ("Зелёная проверка", "тот же воркфлоу запускается снова и проходит"),
        ],
        caption="Один раз специально сломать тест — самый быстрый способ научиться читать журнал GitHub Actions",
    )}

    {callout(
        "warning",
        "Основная ветка не должна оставаться красной",
        "Смысл этого упражнения — увидеть неудачную проверку в управляемых условиях и сразу "
        "её исправить, а не оставить <code class=\"inline\">main</code> в сломанном "
        "состоянии. Реальная красная проверка на основной ветке означает, что кто-то другой, "
        "кто скачает код прямо сейчас, получит нерабочую версию.",
    )}

    {summary_box("Коротко", [
        "GitHub Actions запускает заданные действия автоматически — при пуше или открытии Pull Request.",
        "paths ограничивает запуск воркфлоу только теми изменениями, к которым он относится.",
        "Специально сломанный и затем исправленный тест — быстрый способ научиться читать журнал проверки.",
    ])}
    """
    out = render_page(
        page_title="GitHub Actions: автоматически запускаем тесты",
        description="Воркфлоу GitHub Actions с ограничением по paths и упражнение на намеренно сломанном тесте.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("GitHub Actions", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="GitHub Actions: автоматически запускаем тесты",
        lede="Один файл воркфлоу запускает тесты SafeSort автоматически при каждом изменении — без ручной проверки перед Pull Request.",
        body_html=body,
        sidebar_groups=sidebar("23-30-github-actions.html"),
        nav=PageNav(prev_href="23-29-github-pr.html", prev_label="Issue, ветка, PR", next_href="23-31-versiya-reliz.html", next_label="Версия и первый релиз"),
    )
    write("23-30-github-actions.html", out)


def build_31() -> None:
    body = f"""
    <p>Проект готов, проверен тестами и подключён к автоматической проверке. Последний шаг —
    зафиксировать версию и оформить релиз, чтобы у проекта появилась точка, к которой можно
    вернуться и на которую можно ссылаться.</p>

    <h2>Семантическое версионирование</h2>
    <p>SafeSort использует <strong>семантическое версионирование</strong> — соглашение о
    записи номера версии как <code class="inline">MAJOR.MINOR.PATCH</code>:</p>
    {comparison_table(
        ["Часть номера", "Меняется, когда"],
        [
            ["MAJOR", "несовместимые изменения — старый способ использования перестаёт работать"],
            ["MINOR", "добавлена новая возможность, старое поведение сохранено"],
            ["PATCH", "исправлена ошибка, поведение по сути не изменилось"],
        ],
    )}
    {callout(
        "info",
        "Соглашение, а не закон физики",
        "Семантическое версионирование — общепринятая договорённость, а не встроенное в "
        "инструменты правило: ничто технически не мешает нарушить его смысл. Пользы от него "
        "ровно столько, сколько сам проект последовательно ему следует — это ориентир для "
        "тех, кто устанавливает пакет и хочет понимать, чего ждать от новой версии.",
    )}

    <p>Первая версия SafeSort — <code class="inline">0.1.0</code>: минорная версия ниже 1
    традиционно означает «интерфейс ещё может измениться без отдельного согласования».</p>

    <h2>CHANGELOG — что изменилось в этой версии</h2>
    {code_block(
        "CHANGELOG.md",
        "## [0.1.0]\n\n"
        "### Added\n\n"
        "- scan, plan, apply, duplicates, undo commands\n\n"
        "### Safety\n\n"
        "- dry-run by default (scan/plan/duplicates never modify files)\n"
        "- no automatic duplicate deletion\n"
        "- no silent overwrite of existing files\n",
    )}
    {callout(
        "warning",
        "CHANGELOG описывает только реальные версии",
        "Придумывать историю более ранних версий, которых не существовало, — не задача "
        "CHANGELOG: он честно описывает то, что действительно вышло, начиная с первой "
        "настоящей версии проекта.",
    )}

    <h2>Тег и релиз</h2>
    <p><strong>Тег</strong> (tag) — постоянная метка на конкретном коммите, обычно
    соответствующая номеру версии. <strong>Релиз</strong> на GitHub строится поверх тега и
    добавляет к нему описание изменений — то же содержание, что и в CHANGELOG, но в формате,
    который видно прямо на странице репозитория:</p>
    {code_block(
        "Терминал",
        "git tag v0.1.0\n"
        "git push origin v0.1.0\n",
        lang="text",
    )}

    {callout(
        "tip",
        "Публикация в PyPI — осознанно за рамками версии 0.1.0",
        "Установка через <code class=\"inline\">pip install -e .</code> достаточна для "
        "разработки и личного использования. Публикация пакета в PyPI, чтобы его можно было "
        "установить командой <code class=\"inline\">pip install safesort</code> без ссылки на "
        "репозиторий, — отдельная тема с собственными требованиями к учётной записи и "
        "публикации, и версия 0.1.0 сознательно её не касается.",
    )}

    {summary_box("Коротко", [
        "MAJOR.MINOR.PATCH — соглашение о номере версии, а не встроенное в инструменты правило.",
        "CHANGELOG.md описывает только версии, которые действительно вышли.",
        "Тег фиксирует версию на конкретном коммите; релиз на GitHub добавляет к тегу описание "
        "изменений.",
    ])}
    """
    out = render_page(
        page_title="Документация, версия и первый релиз",
        description="Семантическое версионирование, CHANGELOG.md и тег версии — от 0.1.0 к первому релизу проекта.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Версия и релиз", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Документация, версия и первый релиз",
        lede="MAJOR.MINOR.PATCH, CHANGELOG.md и тег версии — проект получает точку, к которой можно вернуться и на которую можно ссылаться.",
        body_html=body,
        sidebar_groups=sidebar("23-31-versiya-reliz.html"),
        nav=PageNav(prev_href="23-30-github-actions.html", prev_label="GitHub Actions", next_href="23-32-itogi-reliz.html", next_label="Итоги главы"),
    )
    write("23-31-versiya-reliz.html", out)


def build_32() -> None:
    body = f"""
    <h2 id="itogi">Полный путь проекта</h2>
    <p>Тридцать один раздел назад SafeSort был только идеей. Теперь это установленный пакет с
    рабочей командной строкой, автоматическими тестами и настроенной проверкой на GitHub:</p>

    {flow_diagram(
        [
            ("Идея", "требования: что программа делает и чего не делает"),
            ("Репозиторий", "git init, README, структура пакета"),
            ("Реализация", "scanner → classifier → planner → executor"),
            ("Тесты", "pytest, временные каталоги, крайние случаи"),
            ("Git и GitHub", "коммиты, Issue, ветка, Pull Request"),
            ("CI и релиз", "GitHub Actions, версия, тег"),
        ],
        caption="От идеи до релиза — путь, который теперь пройден целиком один раз",
    )}

    <h2>Что уже умеет SafeSort</h2>
    {comparison_table(
        ["Команда", "Что делает", "Меняет файлы?"],
        [
            ["scan", "находит и подсчитывает файлы по категориям", "нет"],
            ["plan", "показывает план перемещений", "нет"],
            ["duplicates", "находит файлы с одинаковым содержимым", "нет"],
            ["apply", "выполняет перемещения из плана", "да, только по явной команде"],
            ["undo", "отменяет последнюю выполненную операцию", "да, только восстановление"],
        ],
    )}

    <h2>Что дальше</h2>
    <p>Версия 0.1.0 сознательно не покрывает всё, что в принципе возможно: раздел 23.1 заранее
    очертил границы. Дальнейшее развитие SafeSort — за рамками этой главы, но некоторые
    направления естественно продолжают уже сделанное: публикация пакета в PyPI, классификация
    не только по расширению, а с осторожной проверкой содержимого файла, интерфейс для
    настройки, отличный от редактирования TOML-файла вручную.</p>

    <p>Приложение к этой главе повторяет тот же самый путь — от задачи до Pull Request — ещё
    шесть раз, уже самостоятельно, на шести небольших проектах:
    <a href="23-hw-index.html">Дополнительная практика: шесть мини-проектов для GitHub</a>.</p>

    {summary_box("Что мы узнали в этой главе", [
        "Прежде чем писать код, требования проекта описывают не только то, что программа делает, "
        "но и то, что она сознательно не делает.",
        "Разделение на планирование (данные, ничего не меняющие) и выполнение (единственный "
        "код, который трогает диск) защищает от случайных изменений файлов пользователя.",
        "Поиск дубликатов дорогую операцию — хеширование — делает только там, где она "
        "действительно может изменить ответ: после отбора файлов по размеру.",
        "Автоматические тесты работают только во временных каталогах — ни один тест не должен "
        "касаться настоящих файлов пользователя.",
        "Git и GitHub — часть разработки с самого начала, а не финальный шаг: Issue формулирует "
        "задачу, ветка изолирует работу, Pull Request открывает её для проверки, GitHub Actions "
        "проверяет тесты автоматически.",
    ])}
    """
    out = render_page(
        page_title="Итоги: полный путь проекта от идеи до релиза",
        description="От требований и репозитория до тестов, GitHub Actions и версии 0.1.0 — итоги главы 23.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Итоги главы", "")],
        kicker="Глава 23 · Первый проект на GitHub",
        h1="Итоги: полный путь проекта от идеи до релиза",
        lede="От идеи до первого релиза — весь путь пройден один раз целиком, на настоящем проекте.",
        body_html=body,
        sidebar_groups=sidebar("23-32-itogi-reliz.html"),
        nav=PageNav(prev_href="23-31-versiya-reliz.html", prev_label="Версия и релиз", next_href="23-hw-index.html", next_label="Приложение: шесть мини-проектов"),
    )
    write("23-32-itogi-reliz.html", out)


# ---------------------------------------------------------------------------
# Приложение: шесть мини-проектов для домашней практики
# ---------------------------------------------------------------------------


def build_hw_index() -> None:
    body = f"""
    <p>Основной проект главы — SafeSort — показывает полный цикл разработки один раз
    подробно. В дополнительной практике этот же цикл нужно повторить самостоятельно на шести
    небольших проектах.</p>

    <p>Цель здесь не только написать работающий код. Каждый проект необходимо оформить как
    часть GitHub-портфолио: определить задачу, привести код в порядок, добавить тесты и
    документацию, выполнить работу в отдельной ветке и завершить её через Pull Request.</p>

    <h2>Шесть проектов</h2>
    {comparison_table(
        ["Проект", "Что практикует"],
        [
            ["A. Калькулятор с Tkinter", "безопасный разбор выражений без eval(), разделение логики и интерфейса"],
            ["B. Генератор случайных историй", "детерминированный генератор случайных чисел, тестируемая случайность"],
            ["C. «Камень, ножницы, бумага»", "таблица правил вместо цепочки условий, проверка всех девяти комбинаций"],
            ["D. Отскакивающие мячи с Pygame", "движение по времени кадра, независимость от FPS"],
            ["E. Преобразование температуры", "чистые функции конвертации, проверка ниже абсолютного нуля"],
            ["F. Приложение «Заметки»", "файловые операции отдельно от интерфейса, обработка ошибок чтения"],
        ],
    )}

    <h2>Один репозиторий для всех шести проектов</h2>
    <p>Канонический репозиторий курса для этой практики — <a
    href="https://github.com/Cartesian-School/python-mini-projects">python-mini-projects</a>,
    один репозиторий на все шесть проектов, а не шесть отдельных:</p>
    {comparison_table(
        ["Один репозиторий", "Шесть репозиториев"],
        [
            ["Один и тот же рабочий процесс с Issue, веткой и Pull Request повторяется шесть раз в одном месте", "Тот же процесс нужно настраивать заново для каждого репозитория"],
            ["Прогресс по всем проектам виден сразу в одном списке коммитов и PR", "Прогресс разбросан по шести отдельным историям"],
            ["Профиль на GitHub не засорён шестью крошечными репозиториями", "Шесть репозиториев ради шести небольших упражнений"],
        ],
    )}
    <p>Если один из проектов вырастет во что-то самостоятельное и заслуживающее отдельного
    внимания, его можно позже вынести в собственный репозиторий — но это решение для будущего,
    не отправная точка.</p>

    <h2>Рабочий процесс для каждого проекта</h2>
    {flow_diagram(
        [
            ("Issue", "краткое описание задачи и критериев готовности"),
            ("Ветка", "feat/название-проекта"),
            ("Код и тесты", "реализация плюс хотя бы один автоматический тест"),
            ("Коммит", "git diff проверен, изменение осмысленное"),
            ("Pull Request", "открыт, просмотрен, проверки пройдены"),
        ],
        caption="Один и тот же процесс повторяется для каждого из шести проектов",
    )}

    {callout(
        "warning",
        "Портфолио измеряется не количеством репозиториев",
        "Понятный README, работающий код, разумная структура, тесты и читаемая история "
        "коммитов производят куда лучшее впечатление, чем десяток пустых репозиториев с одним "
        "файлом в каждом. Шесть проектов в одном аккуратном репозитории — сильнее, чем "
        "шесть заброшенных отдельных.",
    )}

    <h2>Итоговый список</h2>
    <ul>
      <li>[ ] SafeSort завершён</li>
      <li>[ ] Репозиторий python-mini-projects создан</li>
      <li>[ ] A. Калькулятор — Pull Request слит</li>
      <li>[ ] B. Генератор историй — Pull Request слит</li>
      <li>[ ] C. Камень, ножницы, бумага — Pull Request слит</li>
      <li>[ ] D. Отскакивающие мячи — Pull Request слит</li>
      <li>[ ] E. Преобразование температуры — Pull Request слит</li>
      <li>[ ] F. Заметки — Pull Request слит</li>
      <li>[ ] Автоматическая проверка настроена и проходит</li>
      <li>[ ] README репозитория обновлён</li>
    </ul>
    """
    out = render_page(
        page_title="Дополнительная практика: шесть мини-проектов для GitHub",
        description="Приложение к главе 23: шесть небольших проектов, каждый — через полный цикл Issue, ветка, тесты, Pull Request.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Дополнительная практика", "")],
        kicker="Глава 23 · Приложение",
        h1="Дополнительная практика: шесть мини-проектов для GitHub",
        lede="Повторите полный путь разработки самостоятельно: от постановки задачи и кода до тестов, коммита и Pull Request.",
        body_html=body,
        sidebar_groups=sidebar("23-hw-index.html"),
        nav=PageNav(prev_href="23-32-itogi-reliz.html", prev_label="Итоги главы", next_href="23-hw-01-kalkulyator.html", next_label="Домашний проект A: калькулятор"),
    )
    write("23-hw-index.html", out)


def build_hw_01() -> None:
    body = f"""
    <p>Классический калькулятор на Tkinter: экран сверху, сетка кнопок с цифрами и знаками
    снизу — тот же приём, что и в тренажёре «Крестики-нолики» из главы 19, одна функция на все
    кнопки:</p>

    {code_block(
        "calculator.py",
        'KNOPKI = [\n'
        '    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),\n'
        '    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),\n'
        "    # ...\n"
        "]\n\n"
        "for podpis, stroka, stolbec in KNOPKI:\n"
        "    knopka = tk.Button(root, text=podpis,\n"
        "                        command=lambda s=podpis: na_cifru_ili_znak_nazhali(s))\n"
        "    knopka.grid(row=stroka, column=stolbec, sticky=\"we\")\n",
    )}

    <h2>Вычисление выражения без eval()</h2>
    <p>Обычный <code class="inline">eval()</code> выполняет любой переданный ему код Python —
    даже если строка формально похожа на арифметику, ограничить его до безопасного набора
    операций сложнее, чем кажется. Калькулятор разбирает выражение через модуль
    <code class="inline">ast</code> и вычисляет только то, что действительно разрешено:
    числа, <code class="inline">+ - * /</code> и скобки:</p>
    {code_block(
        "calculator.py",
        'def vychislit_uzel(uzel: ast.AST) -> float:\n'
        '    if isinstance(uzel, ast.Constant) and isinstance(uzel.value, int | float):\n'
        '        return uzel.value\n'
        '    if isinstance(uzel, ast.BinOp) and type(uzel.op) in DOPUSTIMYE_OPERATORY:\n'
        '        return DOPUSTIMYE_OPERATORY[type(uzel.op)](\n'
        '            vychislit_uzel(uzel.left), vychislit_uzel(uzel.right)\n'
        '        )\n'
        '    if isinstance(uzel, ast.UnaryOp) and isinstance(uzel.op, ast.USub):\n'
        '        return -vychislit_uzel(uzel.operand)\n'
        '    raise ValueError(f"недопустимый узел выражения: {ast.dump(uzel)}")\n\n'
        'def vychislit_vyrazhenie(vyrazhenie: str) -> str:\n'
        '    derevo = ast.parse(vyrazhenie, mode="eval")\n'
        '    return str(vychislit_uzel(derevo.body))\n',
    )}

    {callout(
        "info",
        "Почему это безопаснее eval(), даже ограниченного",
        "Строка вроде <code class=\"inline\">\"import os\"</code> не является допустимым "
        "арифметическим выражением, поэтому <code class=\"inline\">ast.parse(..., "
        "mode=\"eval\")</code> сразу вызывает <code class=\"inline\">SyntaxError</code> — "
        "разбору просто негде появиться. Дерево <code class=\"inline\">vychislit_uzel()</code> "
        "понимает только числа и четыре арифметических оператора: вызвать функцию, "
        "обратиться к переменной или выполнить любой другой код через него в принципе "
        "невозможно, а не запрещено проверкой символов.",
    )}

    <h2>Логика отдельно от интерфейса</h2>
    <p>Состояние калькулятора — текущее введённое выражение — обычная строка внутри
    маленького класса без единого упоминания Tkinter. Импорт файла <code class="inline">
    calculator.py</code> не открывает окно: <code class="inline">tk.Tk()</code> создаётся
    только внутри <code class="inline">main()</code>, поэтому логику можно проверять тестами
    без графического интерфейса вовсе.</p>

    <p>Полный код: [[icon:file]] <a href="../../../projects/tkinter/calculator/calculator.py">projects/tkinter/calculator/calculator.py</a></p>

    <h2>Задание</h2>
    {exercise(2, "Кнопка «±»", "Добавьте кнопку, меняющую знак текущего результата, не трогая функцию vychislit_vyrazhenie().")}

    <h2>GitHub-практика</h2>
    <p>Заведите Issue «Add calculator project» с критериями готовности (интерфейс
    открывается, арифметика работает, деление на ноль обрабатывается, тесты проходят),
    создайте ветку <code class="inline">feat/calculator</code>, добавьте проект в
    <code class="inline">python-mini-projects</code> и завершите работу через Pull Request.</p>

    {local_required_card(
        "23-01",
        "Практика: вычисления и последовательности нажатий",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/23-01/index.html",
    )}
    """
    out = render_page(
        page_title="Домашний проект A: калькулятор с Tkinter",
        description="Сетка кнопок и безопасное вычисление выражений через ast — без eval(). Логика отдельно от интерфейса.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Калькулятор", "")],
        kicker="Глава 23 · Приложение",
        h1="Домашний проект A: калькулятор с Tkinter",
        lede="Экран, сетка кнопок и безопасный разбор выражения через ast — без единого вызова eval().",
        body_html=body,
        sidebar_groups=sidebar("23-hw-01-kalkulyator.html"),
        nav=PageNav(prev_href="23-hw-index.html", prev_label="Дополнительная практика", next_href="23-hw-02-generator-istorij.html", next_label="Домашний проект B: генератор историй"),
    )
    write("23-hw-01-kalkulyator.html", out)


def build_hw_02() -> None:
    body = f"""
    <p>Генератор заполняет шаблон предложения случайно выбранными словами из нескольких
    списков. Все существительные в списке — мужского рода, поэтому согласование с
    прилагательными не нарушается ни при каком сочетании:</p>

    {code_block(
        "story_generator.py",
        'PRILAGATELNYE = ["храбрый", "любопытный", "рассеянный", "весёлый", "загадочный"]\n'
        'SUSHESTVITELNYE = ["дракон", "программист", "кот", "путешественник", "робот"]\n'
        'MESTA = ["в тёмном лесу", "на далёкой планете", "в старой библиотеке", "в подвале дома"]\n'
        'GLAGOLY = ["нашёл", "потерял", "починил", "изобрёл", "испугался"]\n'
        'PREDMETY = ["волшебный ноутбук", "древний свиток", "сломанный компас", "банку варенья"]\n\n'
        'SHABLON = (\n'
        '    "Однажды {prilagatelnoe} {sushestvitelnoe} {mesto} {glagol} {predmet}. "\n'
        '    "С тех пор жизнь его больше не была прежней."\n'
        ")\n",
    )}

    <h2>Проверяемая случайность</h2>
    <p>Если <code class="inline">sluchajnaya_istoriya()</code> всегда обращается напрямую к
    глобальному состоянию модуля <code class="inline">random</code>, тест может проверить
    результат, только предварительно засеяв это глобальное состояние — хрупкий способ, легко
    ломающийся, если где-то ещё в программе тоже вызывается <code class="inline">random
    </code>. Вместо этого функция принимает необязательный генератор случайных чисел:</p>
    {code_block(
        "story_generator.py",
        'def sluchajnaya_istoriya(rng: random.Random | None = None) -> str:\n'
        '    generator = rng if rng is not None else random\n'
        '    return SHABLON.format(\n'
        '        prilagatelnoe=generator.choice(PRILAGATELNYE),\n'
        '        sushestvitelnoe=generator.choice(SUSHESTVITELNYE),\n'
        '        mesto=generator.choice(MESTA),\n'
        '        glagol=generator.choice(GLAGOLY),\n'
        '        predmet=generator.choice(PREDMETY),\n'
        "    )\n",
    )}

    {callout(
        "tip",
        "random.Random(seed) — независимый источник случайности",
        "<code class=\"inline\">random.Random(1)</code> создаёт отдельный генератор "
        "случайных чисел, не связанный с глобальным состоянием модуля "
        "<code class=\"inline\">random</code>. Два экземпляра "
        "<code class=\"inline\">random.Random(7)</code>, созданные независимо, всегда выдают "
        "одну и ту же последовательность — на этом и строится детерминированный тест: "
        "<code class=\"inline\">sluchajnaya_istoriya(random.Random(7))</code>, вызванная "
        "дважды с новым генератором на то же зерно, оба раза вернёт одну и ту же историю.",
    )}

    <p>Полный код: [[icon:file]] <a href="../../../projects/console/story-generator/story_generator.py">projects/console/story-generator/story_generator.py</a></p>

    <h2>Задание</h2>
    {exercise(2, "Ещё один список", "Добавьте список НАРЕЧИЯ (например, «внезапно», «случайно», «незаметно») и вставьте {narechie} в шаблон, сохранив согласование по роду.")}

    <h2>GitHub-практика</h2>
    <p>Issue «Add random story generator», ветка <code class="inline">feat/story-generator</code>,
    тест на детерминированный результат с фиксированным <code class="inline">random.Random
    </code>, Pull Request.</p>

    {practice_card(
        "23-02",
        "Практика: случайные истории и random.Random()",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/23-02/index.html",
    )}
    """
    out = render_page(
        page_title="Домашний проект B: генератор случайных историй",
        description="Шаблон предложения заполняется случайными словами; sluchajnaya_istoriya() принимает генератор random.Random для тестируемости.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Генератор историй", "")],
        kicker="Глава 23 · Приложение",
        h1="Домашний проект B: генератор случайных историй",
        lede="Пять независимых случайных выборов заполняют шаблон — а необязательный random.Random делает результат воспроизводимым в тестах.",
        body_html=body,
        sidebar_groups=sidebar("23-hw-02-generator-istorij.html"),
        nav=PageNav(prev_href="23-hw-01-kalkulyator.html", prev_label="Калькулятор", next_href="23-hw-03-kamen-nozhnicy-bumaga.html", next_label="Домашний проект C: Камень, ножницы, бумага"),
    )
    write("23-hw-02-generator-istorij.html", out)


def build_hw_03() -> None:
    body = f"""
    <p>Логика победителя в игре «Камень, ножницы, бумага» умещается в одном словаре — кто
    кого побеждает:</p>
    {code_block(
        "rps.py",
        'POBEZHDAET = {\n'
        '    "камень": "ножницы",\n'
        '    "ножницы": "бумага",\n'
        '    "бумага": "камень",\n'
        "}\n\n"
        "def opredelit_pobeditelya(hod_igroka: str, hod_kompyutera: str) -> str:\n"
        "    if hod_igroka == hod_kompyutera:\n"
        '        return "ничья"\n'
        "    if POBEZHDAET[hod_igroka] == hod_kompyutera:\n"
        '        return "игрок"\n'
        '    return "компьютер"\n',
    )}
    {callout(
        "tip",
        "Словарь вместо девяти условий",
        "Можно было бы написать девять веток <code class=\"inline\">if hod_igroka == "
        "\"камень\" and hod_kompyutera == \"ножницы\": ...</code> — словарь "
        "<code class=\"inline\">POBEZHDAET</code> делает то же самое в трёх строках и "
        "читается как обычное предложение: «камень побеждает ножницы».",
    )}

    <h2>Ход компьютера с проверяемой случайностью</h2>
    <p>Как и в генераторе историй, ход компьютера принимает необязательный генератор случайных
    чисел — это позволяет тесту проверить конкретный, воспроизводимый ход:</p>
    {code_block(
        "rps.py",
        'def hod_kompyutera(rng: random.Random | None = None) -> str:\n'
        '    generator = rng if rng is not None else random\n'
        '    return generator.choice(VARIANTY)\n',
    )}

    <h2>Матч до трёх побед</h2>
    <p>Игра теперь заканчивается не только по слову «выход», но и когда одна из сторон
    набирает три победы — ясно определённое условие окончания, а не бесконечный цикл:</p>
    {code_block(
        "rps.py",
        'POBED_DLYA_POBEDY_V_MATCHE = 3\n\n'
        "while schet_igroka < POBED_DLYA_POBEDY_V_MATCHE and schet_kompyutera < POBED_DLYA_POBEDY_V_MATCHE:\n"
        "    # ...раунд игры...\n",
    )}

    <p>Полный код: [[icon:file]] <a href="../../../projects/console/rock-paper-scissors/rps.py">projects/console/rock-paper-scissors/rps.py</a></p>

    <h2>Задание</h2>
    {exercise(3, "Добавляем ящерицу и Спока", "Реализуйте расширенную версию игры «Камень, ножницы, бумага, ящерица, Спок» — понадобится словарь POBEZHDAET с пятью ключами, каждый побеждает по два варианта.")}

    <h2>GitHub-практика</h2>
    <p>Issue «Add rock paper scissors game», ветка <code class="inline">feat/rock-paper-scissors
    </code>, тесты на все девять комбинаций ходов, Pull Request.</p>

    {practice_card(
        "23-03",
        "Практика: все 9 комбинаций и симуляция раундов",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/23-03/index.html",
    )}
    """
    out = render_page(
        page_title="Домашний проект C: «Камень, ножницы, бумага»",
        description="Словарь правил вместо цепочки условий, проверяемый ход компьютера через random.Random, матч до трёх побед.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Камень, ножницы, бумага", "")],
        kicker="Глава 23 · Приложение",
        h1="Домашний проект C: «Камень, ножницы, бумага»",
        lede="Вся логика игры — один словарь: кто кого побеждает. Матч теперь заканчивается по ясному условию — до трёх побед.",
        body_html=body,
        sidebar_groups=sidebar("23-hw-03-kamen-nozhnicy-bumaga.html"),
        nav=PageNav(prev_href="23-hw-02-generator-istorij.html", prev_label="Генератор историй", next_href="23-hw-04-otskakivayushie-myachi.html", next_label="Домашний проект D: отскакивающие мячи"),
    )
    write("23-hw-03-kamen-nozhnicy-bumaga.html", out)


def build_hw_04() -> None:
    body = f"""
    <p>Мяч описан классом <code class="inline">Myach</code> — позиция и скорость хранятся как
    <code class="inline">pygame.Vector2</code>, а скорость измеряется в пикселях <strong>в
    секунду</strong>, а не в пикселях за кадр:</p>

    {code_block(
        "bouncing_balls.py",
        "class Myach:\n"
        "    def __init__(self, x, y, vx, vy, radius, cvet):\n"
        "        self.pos = Vector2(x, y)\n"
        "        self.velocity = Vector2(vx, vy)  # пикселей в секунду\n"
        "        self.radius = radius\n"
        "        self.cvet = cvet\n"
        "        self.otskokov = 0\n\n"
        "    def shag(self, dt: float) -> None:\n"
        "        self.pos += self.velocity * dt\n"
        "        if self.pos.x - self.radius < 0 or self.pos.x + self.radius > SHIRINA:\n"
        "            self.velocity.x = -self.velocity.x\n"
        "            self.otskokov += 1\n"
        "        # ...то же самое для self.pos.y и VYSOTA\n",
    )}

    {callout(
        "warning",
        "self.pos += self.velocity * dt — не self.pos += self.velocity",
        "Глава 20 уже показывала эту ошибку: если прибавлять скорость к позиции на каждый "
        "кадр без учёта <code class=\"inline\">dt</code> (реального времени, прошедшего с "
        "прошлого кадра), мяч на экране с частотой 120 кадров в секунду улетит вчетверо "
        "дальше за одну и ту же секунду, чем на 30 кадрах в секунду. Умножение на "
        "<code class=\"inline\">dt</code> делает движение независимым от частоты кадров: за "
        "одну реальную секунду мяч проходит одно и то же расстояние независимо от FPS.",
    )}

    <p>Окно и цикл отрисовки создаются только внутри <code class="inline">main()</code> —
    импорт файла <code class="inline">bouncing_balls.py</code> не открывает окно pygame, а
    значит, <code class="inline">Myach.shag()</code> можно проверить тестом без дисплея:</p>
    {code_block(
        "bouncing_balls.py",
        "def main() -> None:\n"
        "    pygame.init()\n"
        "    screen = pygame.display.set_mode((SHIRINA, VYSOTA))\n"
        "    clock = pygame.time.Clock()\n"
        "    myachi = sozdat_myachi()\n"
        "    while rabotaet:\n"
        "        dt = clock.tick(FPS) / 1000\n"
        "        for myach in myachi:\n"
        "            myach.shag(dt)\n"
        "        narisovat_kadr(screen, myachi)\n",
    )}

    <p>Полный код: [[icon:file]] <a href="../../../projects/pygame/bouncing-balls-oop/bouncing_balls.py">projects/pygame/bouncing-balls-oop/bouncing_balls.py</a></p>

    <h2>Задание</h2>
    {exercise(2, "Столкновение мячей друг с другом", "Добавьте проверку расстояния между каждой парой мячей — если они соприкоснулись, поменяйте местами их velocity.")}

    <h2>GitHub-практика</h2>
    <p>Issue «Add bouncing balls project», ветка <code class="inline">feat/bouncing-balls</code>,
    тест на независимость движения от FPS (30/60/120 кадров дают одинаковый результат за одну и
    ту же секунду), Pull Request.</p>

    {local_required_card(
        "23-04",
        "Практика: класс Myach и несколько мячей сразу",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/23-04/index.html",
    )}
    """
    out = render_page(
        page_title="Домашний проект D: отскакивающие мячи с Pygame",
        description="Vector2 и скорость в пикселях в секунду, движение по delta time — независимо от частоты кадров.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Отскакивающие мячи", "")],
        kicker="Глава 23 · Приложение",
        h1="Домашний проект D: отскакивающие мячи с Pygame",
        lede="Позиция и скорость через Vector2, движение через dt — за одну реальную секунду мяч проходит одно и то же расстояние на любой частоте кадров.",
        body_html=body,
        sidebar_groups=sidebar("23-hw-04-otskakivayushie-myachi.html"),
        nav=PageNav(prev_href="23-hw-03-kamen-nozhnicy-bumaga.html", prev_label="Камень, ножницы, бумага", next_href="23-hw-05-temperatura.html", next_label="Домашний проект E: температура"),
    )
    write("23-hw-04-otskakivayushie-myachi.html", out)


def build_hw_05() -> None:
    body = f"""
    <p>Небольшое, но по-настоящему полезное приложение: вводим температуру, выбираем единицу
    через переключатели и сразу видим значение во всех трёх шкалах — Цельсий, Фаренгейт,
    Кельвин:</p>
    {code_block(
        "temperature_converter.py",
        "ABSOLYUTNYJ_NOL_C = -273.15\n\n"
        "def preobrazovat(znachenie: float, iz_edinicy: str) -> dict[str, float]:\n"
        '    if iz_edinicy == "C":\n'
        "        c = znachenie\n"
        '    elif iz_edinicy == "F":\n'
        "        c = farengejt_v_celsij(znachenie)\n"
        "    else:\n"
        "        c = kelvin_v_celsij(znachenie)\n\n"
        "    if c < ABSOLYUTNYJ_NOL_C:\n"
        '        raise ValueError("температура ниже абсолютного нуля")\n\n'
        '    return {"C": c, "F": celsij_v_farengejt(c), "K": celsij_v_kelvin(c)}\n',
    )}

    {callout(
        "warning",
        "-300°C не существует",
        "Абсолютный ноль — минимально возможная температура: -273.15°C, 0 K, -459.67°F. Любое "
        "значение ниже этой границы физически невозможно, и приложение отклоняет его явной "
        "ошибкой <code class=\"inline\">ValueError</code>, а не молча выдаёт формально "
        "посчитанный, но бессмысленный результат.",
    )}

    {callout(
        "tip",
        "K, а не °K",
        "У шкалы Кельвина нет знака градуса: правильная запись — <code class=\"inline\">"
        "273.15 K</code>, а не <code class=\"inline\">273.15°K</code>. Это не орфографическая "
        "мелочь: у Цельсия и Фаренгейта отсчёт идёт от условно выбранной точки, поэтому у них "
        "и есть «градус» в названии единицы, а кельвин отсчитывается от абсолютного нуля и "
        "исторически определён без такого смещения.",
    )}

    <p>Формулы перевода остаются чистыми функциями без Tkinter, а окно создаётся только
    внутри <code class="inline">main()</code> — как и во всех остальных домашних проектах.</p>

    <p>Полный код: [[icon:file]] <a href="../../../projects/tkinter/temperature-converter/temperature_converter.py">projects/tkinter/temperature-converter/temperature_converter.py</a></p>

    <h2>Задание</h2>
    {exercise(2, "Шкала Ранкина", "Добавьте перевод в шкалу Ранкина (R = (C + 273.15) × 9 / 5) и обратно, с той же проверкой на физически невозможные значения.")}

    <h2>GitHub-практика</h2>
    <p>Issue «Add temperature converter», ветка <code class="inline">feat/temperature-converter
    </code>, тесты на 0°C = 32°F, 100°C = 212°F, 0°C = 273.15 K, -273.15°C = 0 K и на отказ
    принять значение ниже абсолютного нуля, Pull Request.</p>

    {local_required_card(
        "23-05",
        "Практика: формулы и проверка абсолютного нуля",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/23-05/index.html",
    )}
    """
    out = render_page(
        page_title="Домашний проект E: преобразование температуры",
        description="Чистые функции перевода между Цельсием, Фаренгейтом и Кельвином, с явным отказом принимать значения ниже абсолютного нуля.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Температура", "")],
        kicker="Глава 23 · Приложение",
        h1="Домашний проект E: преобразование температуры",
        lede="Одна функция перевода в Цельсий и обратно — и явная проверка, что такой температуры вообще может существовать.",
        body_html=body,
        sidebar_groups=sidebar("23-hw-05-temperatura.html"),
        nav=PageNav(prev_href="23-hw-04-otskakivayushie-myachi.html", prev_label="Отскакивающие мячи", next_href="23-hw-06-zametki.html", next_label="Домашний проект F: заметки"),
    )
    write("23-hw-05-temperatura.html", out)


def build_hw_06() -> None:
    body = f"""
    <p>Последний домашний проект объединяет файлы (глава 14) и Tkinter: приложение «Заметки»
    с текстовым полем и кнопками сохранить, загрузить, очистить. Работа с файлом вынесена в
    отдельные функции, не знающие о существовании Tkinter вовсе:</p>

    {code_block(
        "notes_app.py",
        "def sohranit_v_fajl(put: Path, tekst: str) -> None:\n"
        '    put.write_text(tekst, encoding="utf-8")\n\n'
        "def zagruzit_iz_fajla(put: Path) -> str:\n"
        "    if not put.exists():\n"
        "        raise FileNotFoundError(put)\n"
        '    return put.read_text(encoding="utf-8")\n',
    )}

    {callout(
        "tip",
        "Файловые функции без Tkinter — легко проверить тестом",
        "<code class=\"inline\">sohranit_v_fajl()</code> и <code class=\"inline\">"
        "zagruzit_iz_fajla()</code> принимают обычный <code class=\"inline\">Path</code> и не "
        "обращаются ни к одному виджету — тест может вызвать их во временном каталоге "
        "pytest, без единого окна на экране.",
    )}

    <h2>Обработка ошибок и несохранённые изменения</h2>
    <p>Интерфейсный слой ловит конкретные исключения, а не пытается угадать, что пошло не
    так, — и предупреждает, если попытаться загрузить файл поверх ещё не сохранённого текста:</p>
    {code_block(
        "notes_app.py",
        "def zagruzit_zametku() -> None:\n"
        "    if est_nesohranennye_izmeneniya.get():\n"
        '        status_text.set("Есть несохранённые изменения — сначала сохраните или очистите поле")\n'
        "        return\n"
        "    try:\n"
        "        tekst = zagruzit_iz_fajla(fajl_zametok)\n"
        "    except FileNotFoundError:\n"
        '        status_text.set("Файл заметки ещё не создан — сначала сохраните.")\n'
        "        return\n"
        "    except (PermissionError, OSError) as oshibka:\n"
        '        status_text.set(f"Не удалось загрузить: {oshibka}")\n'
        "        return\n",
    )}

    <p>Полный код: [[icon:file]] <a href="../../../projects/tkinter/notes-app/notes_app.py">projects/tkinter/notes-app/notes_app.py</a></p>

    <h2>Задание</h2>
    {exercise(2, "Сохранение под другим именем", "Добавьте кнопку «Сохранить как», открывающую filedialog.asksaveasfilename() и сохраняющую текст в выбранный пользователем файл.")}

    <h2>GitHub-практика</h2>
    <p>Issue «Add notes app project», ветка <code class="inline">feat/notes</code>, тест на
    сохранение и загрузку через временный файл (round-trip в UTF-8) и на
    <code class="inline">FileNotFoundError</code> при отсутствующем файле, Pull Request.</p>

    {local_required_card(
        "23-06",
        "Практика: сохранение, загрузка и отсутствующий файл",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/23-06/index.html",
    )}

    <h2 id="itogi">Итоги приложения</h2>
    {summary_box("Что мы повторили на шести проектах", [
        "Безопасный разбор арифметики через ast — вместо eval(), даже ограниченного.",
        "Проверяемая случайность: генератор random.Random передаётся явно, а не берётся из "
        "глобального состояния модуля random.",
        "Таблица правил вместо цепочки условий — и полная проверка всех возможных комбинаций.",
        "Движение по delta time: скорость в пикселях в секунду, а не в пикселях за кадр.",
        "Проверка физических ограничений (температура не бывает ниже абсолютного нуля) — не "
        "только формальный ввод-вывод чисел.",
        "Файловые операции отдельно от интерфейса — с конкретной обработкой FileNotFoundError, "
        "PermissionError и OSError, а не общим except Exception.",
        "Каждый проект — тот же рабочий процесс, что и у SafeSort: Issue, ветка, тесты, "
        "коммит, Pull Request.",
    ])}
    """
    out = render_page(
        page_title="Домашний проект F: приложение «Заметки»",
        description="Файловые операции отдельно от интерфейса, обработка FileNotFoundError и PermissionError, UTF-8.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Заметки", "")],
        kicker="Глава 23 · Приложение",
        h1="Домашний проект F: приложение «Заметки»",
        lede="Файлы и Tkinter вместе — но чтение и запись вынесены в функции, которые ничего не знают об интерфейсе.",
        body_html=body,
        sidebar_groups=sidebar("23-hw-06-zametki.html"),
        nav=PageNav(prev_href="23-hw-05-temperatura.html", prev_label="Температура", next_href="../glava-24/index.html", next_label="Глава 24: Что дальше?"),
    )
    write("23-hw-06-zametki.html", out)


# ---------------------------------------------------------------------------
# Совместимость со старыми адресами шести мини-проектов
# ---------------------------------------------------------------------------


def build_legacy_redirects() -> None:
    """Старые адреса шести мини-проектов (существовавшие до переработки главы)
    сохраняются как короткие страницы-указатели на новое место в приложении —
    без них внешние и внутренние ссылки на старые URL превратились бы в 404.
    Не входят в PAGES (см. комментарий у LEGACY_REDIRECTS) — это не часть
    основного содержания главы, а только совместимость."""
    for old_href, new_href, new_title in LEGACY_REDIRECTS:
        body = f"""
        {callout(
            "info",
            "Материал перенесён в дополнительную практику Главы 23",
            "Этот мини-проект больше не часть основного содержания главы 23 — основной путь "
            "главы теперь один проект, доведённый от идеи до релиза, SafeSort. Материал, который был "
            f"на этой странице, перенесён в приложение и обновлён: <a href=\"{new_href}\">{new_title}</a>.",
        )}
        <p><a href="{new_href}">Перейти к разделу «{new_title}» →</a></p>
        """
        out = render_page(
            page_title=f"{new_title} — перенесено",
            description=f"Страница перенесена: {new_title} теперь находится в дополнительной практике главы 23.",
            depth=2,
            breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Материал перенесён", "")],
            kicker="Глава 23 · Материал перенесён",
            h1="Материал перенесён",
            lede=f"Эта страница переехала в приложение к главе 23: {new_title}.",
            body_html=body,
            sidebar_groups=sidebar(new_href),
            nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href=new_href, next_label=new_title),
        )
        write(old_href, out)


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
    build_32()
    build_hw_index()
    build_hw_01()
    build_hw_02()
    build_hw_03()
    build_hw_04()
    build_hw_05()
    build_hw_06()
    build_legacy_redirects()
