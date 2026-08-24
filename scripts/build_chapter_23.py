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
    before_after_trees,
    callout,
    code_block,
    comparison_table,
    decision_map,
    dir_tree,
    exercise,
    flow_diagram,
    github_lockup,
    github_mark,
    image_figure,
    local_required_card,
    official_sources,
    practice_card,
    project_state_card,
    render_chapter_opener,
    render_page,
    safety_boundary,
    stage_tracker,
    summary_box,
    terminal_capture,
    timeline_diagram,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-23"
IMG = "../../assets/img/chapter-23/output"

# --- Основной путь главы: SafeSort, от идеи до релиза -----------------------
# Каждая запись — (href, title, часть); "часть" — номер ЧАСТИ 1..6, тот же,
# что передаётся в stage_tracker() на самой странице (см. SAFESORT_STAGES в
# site_lib.py). Группировка сайдбара строится по этому полю явно (см.
# sidebar() ниже), а не угадывается по числу в имени файла — так новые
# страницы Части I/II можно свободно добавлять с любыми именами.
PAGES = [
    ("index.html", "Обзор главы", 1),
    ("23-01-ideya-trebovaniya.html", "Что мы будем создавать: SafeSort", 1),
    ("23-git-01-chto-takoe-git-github.html", "Что такое Git и что такое GitHub", 1),
    ("23-git-02-ustanavlivaem-git.html", "Устанавливаем Git", 1),
    ("23-git-03-pervaya-nastrojka.html", "Первая настройка Git", 1),
    ("23-git-04-github-account.html", "Создаём и защищаем учётную запись GitHub", 1),
    ("23-git-05-autentifikaciya.html", "HTTPS, SSH и аутентификация", 1),
    ("23-git-06-ssh.html", "Настраиваем SSH", 1),
    ("23-git-07-sozdaem-repozitorij.html", "Создаём репозиторий SafeSort на GitHub", 1),
    ("23-git-08-kloniruem.html", "Клонируем репозиторий", 1),
    ("23-git-09-lokalnyj-i-udalennyj.html", "Локальный и удалённый репозиторий", 1),
    ("23-git-10-working-tree-staging-commit.html", "Working tree, staging и commit", 1),
    ("23-proj-01-repo-vs-project.html", "Repository и GitHub Project — в чём разница", 2),
    ("23-proj-02-luchshie-praktiki.html", "Как спланировать Project: лучшие практики", 2),
    ("23-proj-03-sozdaem-project.html", "Создаём GitHub Project", 2),
    ("23-proj-04-kopiruem-project.html", "Копируем существующий Project", 2),
    ("23-proj-05-board-table-roadmap.html", "Board, Table и Roadmap", 2),
    ("23-proj-06-polya.html", "Поля Project: встроенные и пользовательские", 2),
    ("23-proj-07-chernoviki.html", "Черновики: задача без Issue", 2),
    ("23-proj-08-chernovik-v-issue.html", "Превращаем черновик в Issue", 2),
    ("23-proj-09-issues.html", "Создаём Issues и добавляем в Project", 2),
    ("23-proj-10-redaktiruem-elementy.html", "Редактируем элементы Project", 2),
    ("23-proj-11-filtr-sort-grupp.html", "Фильтруем, сортируем и группируем", 2),
    ("23-proj-12-upravlyaem-predstavleniyami.html", "Управляем представлениями", 2),
    ("23-proj-13-avtomatizaciya.html", "Встроенная автоматизация и auto-add", 2),
    ("23-proj-14-arhiviruem.html", "Архивируем и восстанавливаем элементы", 2),
    ("23-proj-15-shablony.html", "Шаблоны Project", 2),
    ("23-proj-16-insights.html", "Insights и графики Project", 2),
    ("23-proj-17-issue-branch-pr.html", "Первый цикл: Issue → Branch → Pull Request", 2),
    ("23-02-repozitorij.html", "Первый коммит в клонированном репозитории", 3),
    ("23-03-readme.html", "Первый README проекта", 3),
    ("23-04-struktura-paketa.html", "Планируем структуру Python-пакета", 3),
    ("23-05-pyproject-toml.html", "pyproject.toml и установка проекта", 3),
    ("23-06-komandnaya-stroka.html", "Командная строка SafeSort", 3),
    ("23-07-pathlib.html", "pathlib: работаем с путями и каталогами", 4),
    ("23-08-skaniruem-katalog.html", "Сканируем каталог", 4),
    ("23-09-isklyucheniya.html", "Какие каталоги не нужно сканировать", 4),
    ("23-10-klassifikaciya.html", "Определяем категорию файла", 4),
    ("23-11-plan-dejstvij.html", "От анализа к плану действий", 4),
    ("23-12-predvaritelnyj-prosmotr.html", "Режим предварительного просмотра", 4),
    ("23-13-peremeshaem-fajly.html", "Безопасно перемещаем файлы", 4),
    ("23-14-imya-zanyato.html", "Что делать, если имя уже занято", 4),
    ("23-15-zhurnal-operacij.html", "Журнал выполненных операций", 4),
    ("23-16-otmena-operacii.html", "Отмена последней операции", 4),
    ("23-17-poisk-dublikatov.html", "Поиск одинаковых файлов", 4),
    ("23-18-sha256.html", "SHA-256 и хеш содержимого файла", 4),
    ("23-19-gruppy-dublikatov.html", "Находим группы дубликатов", 4),
    ("23-20-oshibki-fajlovoj-sistemy.html", "Обрабатываем ошибки файловой системы", 4),
    ("23-21-logging.html", "Добавляем журнал работы программы", 4),
    ("23-22-nastrojki-proekta.html", "Настройки проекта", 4),
    ("23-23-pervye-testy.html", "Пишем первые автоматические тесты", 5),
    ("23-24-testy-skanirovaniya.html", "Проверяем сканирование и классификацию", 5),
    ("23-25-testy-peremeshheniya.html", "Проверяем перемещение и отмену", 5),
    ("23-26-testy-dublikatov.html", "Проверяем поиск дубликатов", 5),
    ("23-27-testy-cli.html", "Проверяем интерфейс командной строки", 5),
    ("23-28-git-kommit.html", "Git: от рабочего изменения к коммиту", 5),
    ("23-29-github-pr.html", "GitHub: Issue, ветка и Pull Request", 5),
    ("23-30-github-actions.html", "GitHub Actions: автоматически запускаем тесты", 5),
    ("23-31-versiya-reliz.html", "Документация, версия и первый релиз", 6),
    ("23-32-itogi-reliz.html", "Итоги: полный путь проекта от идеи до релиза", 6),
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


# Шесть частей главы — те же названия, что и SAFESORT_STAGES в site_lib.py
# (индекс совпадает с полем "часть" в PAGES и с аргументом stage_tracker()).
SAFESORT_PART_TITLES: list[str] = [
    "Часть I · Git и GitHub с нуля",
    "Часть II · Планируем SafeSort на GitHub",
    "Часть III · Создаём Python-проект",
    "Часть IV · Реализуем SafeSort",
    "Часть V · Проверяем и автоматизируем",
    "Часть VI · Выпускаем первую версию",
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    hw_items = [NavItem(title, href) for href, title in HOMEWORK_PAGES]
    phase_groups = []
    for part_num, part_title in enumerate(SAFESORT_PART_TITLES, start=1):
        items = [NavItem(title, href) for href, title, part in PAGES if part == part_num and href != "index.html"]
        phase_groups.append(SidebarGroup(part_title, items))
    overview_item = NavItem("Обзор главы", "index.html")
    phase_groups[0].items.insert(0, overview_item)
    all_main_items = [it for g in phase_groups for it in g.items]
    for it in all_main_items + hw_items:
        it.active = it.href == active_href
    return [
        *phase_groups,
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
    intro = f"""
    <div style="display:flex;align-items:center;gap:8px;font-family:Sora,sans-serif;font-weight:700;
      font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:#5B24F9;margin:0 0 16px">
      {github_mark()}<span>Первый проект, доведённый до Pull Request на GitHub</span>
    </div>

    <p>В этой главе мы построим программу, которая наводит порядок в захламлённой папке —
    и доведём её до состояния, в котором её можно показать на GitHub: с тестами, историей
    коммитов и Pull Request.</p>

    {before_after_trees(
        ("Downloads", "dir", [
            ("report.pdf", "file", []),
            ("IMG_4912.jpg", "file", []),
            ("archive.zip", "file", []),
            ("notes.txt", "file", []),
            ("photo-copy.jpg", "file", []),
        ]),
        ("Downloads", "dir", [
            ("Sorted", "dir", [
                ("documents", "dir", [("report.pdf", "file", [])]),
                ("images", "dir", [("IMG_4912.jpg", "file", []), ("photo-copy.jpg", "file", [])]),
                ("archives", "dir", [("archive.zip", "file", [])]),
                ("other", "dir", [("notes.txt", "file", [])]),
            ]),
        ]),
        caption="SafeSort раскладывает файлы по категориям и находит одинаковые (photo-copy.jpg — не «пропавший» файл, а его копия).",
    )}

    {flow_diagram([
        ("Пользователь", "запускает команду"),
        ("SafeSort", "scan / plan / apply / duplicates / undo"),
        ("Файловая система", "читается или меняется"),
    ], caption="Программа не делает ничего без явной команды пользователя.")}

    {safety_boundary(
        ["scan — показывает файлы", "plan — показывает план перемещений", "duplicates — показывает совпадения"],
        ["apply — перемещает файлы", "undo — возвращает файлы на место"],
    )}

    {terminal_capture([
        "$ safesort plan ~/Downloads",
        "9 move operations planned.",
        "No files have been changed.",
    ], caption="plan только показывает, что произойдёт — apply понадобится отдельно.")}
    """
    out = render_chapter_opener(
        chapter_num=23,
        baseline_page=511,
        title="Первый проект на GitHub: SafeSort",
        description="Пишем программу, которая наводит порядок в файлах, — и доводим её до состояния, готового для GitHub: тесты, история коммитов, Pull Request.",
        meta_items=["[[icon:timer]] ~16-20 часов", "[[icon:architecture]] один проект, 6 частей", "[[icon:practice]] 20 практик + приложение"],
        intro_html=intro,
        sections=[
            ChapterSectionLink("23.1", "Что мы будем создавать: SafeSort", "23-01-ideya-trebovaniya.html"),
            ChapterSectionLink("", "Что такое Git и что такое GitHub", "23-git-01-chto-takoe-git-github.html"),
            ChapterSectionLink("", "Устанавливаем Git", "23-git-02-ustanavlivaem-git.html"),
            ChapterSectionLink("", "Первая настройка Git", "23-git-03-pervaya-nastrojka.html"),
            ChapterSectionLink("", "Учётная запись GitHub", "23-git-04-github-account.html"),
            ChapterSectionLink("", "HTTPS, SSH и аутентификация", "23-git-05-autentifikaciya.html"),
            ChapterSectionLink("", "Настраиваем SSH", "23-git-06-ssh.html"),
            ChapterSectionLink("", "Создаём репозиторий SafeSort", "23-git-07-sozdaem-repozitorij.html"),
            ChapterSectionLink("", "Клонируем репозиторий", "23-git-08-kloniruem.html"),
            ChapterSectionLink("", "Локальный и удалённый репозиторий", "23-git-09-lokalnyj-i-udalennyj.html"),
            ChapterSectionLink("", "Working tree, staging и commit", "23-git-10-working-tree-staging-commit.html"),
            ChapterSectionLink("", "Repository и GitHub Project", "23-proj-01-repo-vs-project.html"),
            ChapterSectionLink("", "Лучшие практики Project", "23-proj-02-luchshie-praktiki.html"),
            ChapterSectionLink("", "Создаём GitHub Project", "23-proj-03-sozdaem-project.html"),
            ChapterSectionLink("", "Копируем существующий Project", "23-proj-04-kopiruem-project.html"),
            ChapterSectionLink("", "Board, Table и Roadmap", "23-proj-05-board-table-roadmap.html"),
            ChapterSectionLink("", "Поля Project", "23-proj-06-polya.html"),
            ChapterSectionLink("", "Черновики: задача без Issue", "23-proj-07-chernoviki.html"),
            ChapterSectionLink("", "Превращаем черновик в Issue", "23-proj-08-chernovik-v-issue.html"),
            ChapterSectionLink("", "Создаём Issues", "23-proj-09-issues.html"),
            ChapterSectionLink("", "Редактируем элементы Project", "23-proj-10-redaktiruem-elementy.html"),
            ChapterSectionLink("", "Фильтруем, сортируем, группируем", "23-proj-11-filtr-sort-grupp.html"),
            ChapterSectionLink("", "Управляем представлениями", "23-proj-12-upravlyaem-predstavleniyami.html"),
            ChapterSectionLink("", "Автоматизация и auto-add", "23-proj-13-avtomatizaciya.html"),
            ChapterSectionLink("", "Архивируем элементы", "23-proj-14-arhiviruem.html"),
            ChapterSectionLink("", "Шаблоны Project", "23-proj-15-shablony.html"),
            ChapterSectionLink("", "Insights и графики", "23-proj-16-insights.html"),
            ChapterSectionLink("", "Первый цикл: Issue → Branch → PR", "23-proj-17-issue-branch-pr.html"),
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
    {stage_tracker(1)}

    <p>До сих пор мы писали программы по частям: функции, игры, интерфейсы. Теперь
    соберём один проект целиком и доведём его до состояния, которое можно разместить на
    GitHub. Программа называется <strong>SafeSort</strong>, и вот что она делает.</p>

    {before_after_trees(
        ("Downloads", "dir", [
            ("report.pdf", "file", []),
            ("photo.jpg", "file", []),
            ("archive.zip", "file", []),
            ("notes.txt", "file", []),
            ("copy_of_notes.txt", "file", []),
        ]),
        ("Downloads", "dir", [
            ("Sorted", "dir", [
                ("documents", "dir", [("report.pdf", "file", []), ("notes.txt", "file", []), ("copy_of_notes.txt", "file", [])]),
                ("images", "dir", [("photo.jpg", "file", [])]),
                ("archives", "dir", [("archive.zip", "file", [])]),
            ]),
        ]),
        caption="notes.txt и copy_of_notes.txt — одинаковое содержимое; SafeSort сообщит об этом отдельно, а не удалит файл сам.",
    )}

    <p>Сначала программа только показывает, что собирается сделать. Переместить файлы
    может исключительно отдельная, явно вызванная команда:</p>

    {flow_diagram([
        ("Пользователь", "запускает команду"),
        ("SafeSort", "scan / plan / apply / duplicates / undo"),
        ("Файловая система", "читается или меняется"),
    ])}

    {safety_boundary(
        ["scan — показывает найденные файлы", "plan — показывает план перемещений", "duplicates — показывает совпадения"],
        ["apply — перемещает файлы", "undo — возвращает файлы на место"],
    )}

    {terminal_capture([
        "$ safesort plan ~/Downloads",
        "5 move operations planned.",
        "No files have been changed.",
    ])}

    <p>Файловая система после этой команды осталась прежней — <code class="inline">plan</code>
    только описывает будущие перемещения. Это различие между «показать» и «сделать» —
    главная идея всего проекта, и мы будем возвращаться к ней ещё не раз.</p>

    <h2>Что должна уметь первая версия</h2>
    <p>Программа должна уметь:</p>
    <ul>
      <li>показать найденные файлы, разложенные по категориям;</li>
      <li>показать план будущих перемещений, ничего не меняя;</li>
      <li>выполнить перемещения только по явной команде;</li>
      <li>найти файлы с одинаковым содержимым;</li>
      <li>отменить последнюю выполненную операцию.</li>
    </ul>

    <p>Как программа должна себя вести:</p>
    <ul>
      <li>не изменять файлы без явной команды;</li>
      <li>не перезаписывать существующий файл молча;</li>
      <li>одинаковый ввод даёт одинаковый план — никакой случайности;</li>
      <li>вся обработка происходит локально, без сети;</li>
      <li>логику можно проверить автоматическими тестами, не трогая настоящие файлы.</li>
    </ul>

    <p>Первый список в разработке принято называть <strong>функциональными
    требованиями</strong> — что программа делает. Второй — <strong>нефункциональными</strong>:
    не «что», а «как», какими свойствами обладает поведение программы независимо от команды.</p>

    <h2>Что не будем делать в первой версии</h2>
    <p>Чтобы закончить проект, а не растягивать его бесконечно, сразу ограничим задачу:</p>
    {comparison_table(
        ["Не входит в первую версию", "Почему"],
        [
            ["Автоматическое удаление дубликатов", "Удаление данных без явного подтверждения — риск, а не удобство"],
            ["Графический интерфейс", "Командную строку проще реализовать, протестировать и объяснить"],
            ["Загрузка файлов в облако", "Программа работает только с локальной файловой системой"],
            ["Классификация по содержимому файла", "Классификация по расширению уже решает основную задачу"],
        ],
    )}

    {summary_box("Коротко", [
        "scan, plan и duplicates только читают файловую систему; перемещает файлы исключительно apply.",
        "«Показать план» и «выполнить план» — разные шаги, и это различие определяет всю архитектуру программы.",
        "Функциональные требования — что программа делает; нефункциональные — какими свойствами обладает её поведение.",
    ])}
    """
    out = render_page(
        page_title="Что мы будем создавать: SafeSort",
        description="Знакомимся с SafeSort, видим будущий результат и определяем, что должна уметь первая версия проекта.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("SafeSort", "")],
        kicker="Глава 23 · Часть I · Git и GitHub с нуля",
        h1="Что мы будем создавать: SafeSort",
        lede="Программа, которая наводит порядок в файлах, — сначала показывает, что сделает, и только потом делает это по команде.",
        body_html=body,
        sidebar_groups=sidebar("23-01-ideya-trebovaniya.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="23-git-01-chto-takoe-git-github.html", next_label="Что такое Git и что такое GitHub"),
    )
    write("23-01-ideya-trebovaniya.html", out)


def build_git_01() -> None:
    body = f"""
    {stage_tracker(1)}

    <div style="margin:8px 0 20px">{github_lockup(150)}</div>

    <p>Предыдущий раздел показал, что будет делать SafeSort. Прежде чем писать код, разберёмся с
    инструментами, вокруг которых построена вся оставшаяся часть главы, — и с четырьмя
    похожими словами, которые легко перепутать.</p>

    {comparison_table(
        ["Понятие", "Что это"],
        [
            ["Python-проект", "исходный код и файлы SafeSort на диске — то, что мы пишем"],
            ["Git-репозиторий", "история изменений этих файлов, хранящаяся в скрытом каталоге .git"],
            ["GitHub-репозиторий", "тот же Git-репозиторий, размещённый на сервере GitHub — плюс веб-интерфейс"],
            ["GitHub Project", "отдельный инструмент планирования поверх репозитория — Issues, доска, представления"],
        ],
    )}

    <p><strong>Git</strong> — программа, которая работает локально, на вашем компьютере: она
    следит за историей изменений файлов. <strong>GitHub</strong> — сервис в интернете,
    построенный вокруг Git: он хранит удалённую копию репозитория и добавляет то, чего у
    голого Git нет, — Issues, Pull Request, Projects, Actions, Releases.</p>

    {flow_diagram([
        ("Ваш компьютер", "Git-репозиторий — работает без интернета"),
        ("git push / git pull", "синхронизация истории"),
        ("GitHub", "удалённая копия + Issues, Projects, PR, Actions, Releases"),
    ], caption="Git — локальный инструмент истории; GitHub — сервис вокруг него. Одно не работает без другого, но это два разных слоя.")}

    {callout(
        "info",
        "Репозиторий на GitHub — не то же самое, что GitHub Project",
        "Это одна из самых частых путаниц у начинающих. Репозиторий хранит код и его историю. "
        "GitHub Project — отдельный, необязательный инструмент планирования: можно иметь "
        "репозиторий вообще без Project, и можно завести Project, объединяющий Issues сразу "
        "из нескольких репозиториев. Часть II этой главы разберёт эту разницу подробно.",
    )}

    {official_sources([
        ("Git", "https://git-scm.com/"),
        ("Start your journey: What is GitHub?", "https://docs.github.com/en/get-started/start-your-journey/what-is-github"),
    ])}

    {summary_box("Коротко", [
        "Git работает локально и следит за историей файлов; ему не нужен интернет.",
        "GitHub — сервис вокруг Git: удалённая копия репозитория плюс Issues, Pull Request, Projects, Actions, Releases.",
        "Репозиторий (код и история) и GitHub Project (планирование) — разные, независимые понятия.",
    ])}
    """
    out = render_page(
        page_title="Что такое Git и что такое GitHub",
        description="Git — локальный инструмент истории изменений; GitHub — сервис вокруг него с Issues, Pull Request, Projects и Actions.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Git и GitHub", "")],
        kicker="Глава 23 · Часть I · Git и GitHub с нуля",
        h1="Что такое Git и что такое GitHub",
        lede="Git и GitHub — не синонимы: один работает локально, другой — сервис вокруг него.",
        body_html=body,
        sidebar_groups=sidebar("23-git-01-chto-takoe-git-github.html"),
        nav=PageNav(prev_href="23-01-ideya-trebovaniya.html", prev_label="Что мы будем создавать", next_href="23-git-02-ustanavlivaem-git.html", next_label="Устанавливаем Git"),
    )
    write("23-git-01-chto-takoe-git-github.html", out)


def build_git_02() -> None:
    body = f"""
    {stage_tracker(1)}

    <p>Git — не встроенная часть Python: его нужно установить отдельно, один раз для всей
    системы. Способ установки зависит от операционной системы.</p>

    {terminal_capture([
        "$ git --version",
        "git version 2.47.3",
    ], caption="Так выглядит успешная проверка — программа сообщает свою версию и ничего больше.")}

    <h2>Linux (Debian/Ubuntu)</h2>
    {code_block(
        "Документированная команда — см. git-scm.com/download/linux",
        "sudo apt update\nsudo apt install git\n",
        lang="text",
    )}
    {callout(
        "info",
        "git, а не git-all",
        "Пакет <code class=\"inline\">git</code> уже включает всё нужное для этого курса. Пакет "
        "<code class=\"inline\">git-all</code> — метапакет, добавляющий дополнительные "
        "интеграции (например, с Emacs), которые здесь не понадобятся.",
    )}
    <p>Для дистрибутивов на основе Fedora/RHEL:</p>
    {code_block("Документированная команда", "sudo dnf install git\n", lang="text")}

    <h2>Windows</h2>
    <p>Официальный установщик — <strong>Git for Windows</strong>: он ставит саму программу
    <code class="inline">git</code> и терминал <strong>Git Bash</strong>, в котором работают
    все команды этой главы без изменений.</p>
    {official_sources([("Git for Windows", "https://git-scm.com/download/win")])}

    <h2>macOS</h2>
    <p>Простейший путь — Xcode Command Line Tools (<code class="inline">xcode-select
    --install</code>), которые включают Git. Официальный установщик с git-scm.com —
    альтернатива, если нужна конкретная версия Git.</p>
    {official_sources([("Git for macOS", "https://git-scm.com/download/mac")])}

    <h2>Проверяем установку</h2>
    <p>Независимо от системы, результат один и тот же: команда <code class="inline">git
    --version</code> в терминале печатает номер версии. Если вместо этого терминал отвечает
    «command not found» (или похожим сообщением на Windows) — Git не установлен или его нет
    в PATH; переустановка обычно решает проблему.</p>

    {official_sources([("Git — Downloads", "https://git-scm.com/downloads")], adapted=False)}

    {summary_box("Коротко", [
        "Git ставится один раз для системы — отдельно от Python.",
        "Linux: sudo apt install git (или dnf install git). Windows: Git for Windows + Git Bash. macOS: Xcode Command Line Tools.",
        "git --version — единственная проверка, что всё получилось.",
    ])}
    """
    out = render_page(
        page_title="Устанавливаем Git",
        description="Установка Git на Linux, Windows и macOS — и проверка через git --version.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Установка Git", "")],
        kicker="Глава 23 · Часть I · Git и GitHub с нуля",
        h1="Устанавливаем Git",
        lede="Git ставится отдельно от Python, один раз для всей системы — способ зависит от операционной системы.",
        body_html=body,
        sidebar_groups=sidebar("23-git-02-ustanavlivaem-git.html"),
        nav=PageNav(prev_href="23-git-01-chto-takoe-git-github.html", prev_label="Что такое Git и GitHub", next_href="23-git-03-pervaya-nastrojka.html", next_label="Первая настройка Git"),
    )
    write("23-git-02-ustanavlivaem-git.html", out)


def build_git_03() -> None:
    body = f"""
    {stage_tracker(1)}

    <p>Прежде чем сделать первый коммит, Git нужно один раз сказать, кто вы, — эта информация
    записывается в каждый коммит и остаётся в истории навсегда.</p>

    {terminal_capture([
        "$ git init",
        "Initialized empty Git repository in .../git_demo/.git/",
        "$ git config user.name \"Ваше Имя\"",
        "$ git config user.email \"you@example.com\"",
        "$ git config --local --list",
        "core.repositoryformatversion=0",
        "core.filemode=true",
        "core.bare=false",
        "core.logallrefupdates=true",
        "user.name=Ваше Имя",
        "user.email=you@example.com",
    ], cwd="~/git_demo")}

    {callout(
        "warning",
        "Это имя пишется в коммиты — а не только в профиль GitHub",
        "<code class=\"inline\">user.name</code>/<code class=\"inline\">user.email</code> — "
        "не логин GitHub и не то же самое, что имя в профиле. Это данные, которые буквально "
        "попадают в каждый коммит как автор изменения, и их видно всем, кто посмотрит "
        "историю — в том числе после публикации на GitHub.",
    )}

    <p>Флаг <code class="inline">--local</code> относится только к этому одному репозиторию.
    Чтобы не повторять настройку для каждого нового проекта, обычно используют
    <code class="inline">--global</code> — тогда имя и почта применяются ко всем репозиториям
    на этом компьютере:</p>

    {code_block(
        "Терминал",
        "git config --global user.name \"Ваше Имя\"\n"
        "git config --global user.email \"you@example.com\"\n",
        lang="text",
    )}

    <h2>Имя ветки по умолчанию</h2>
    <p>Здесь легко ошибиться: сам Git до сих пор называет самую первую ветку нового репозитория
    <code class="inline">master</code>, если её имя никак не настроено, — это встроенное
    поведение не изменилось. В версии 2.28 у Git появилась только сама
    <em>настройка</em> <code class="inline">init.defaultBranch</code>, позволяющая задать другое
    имя по умолчанию, — а не новое поведение "из коробки". Имя <code class="inline">main</code>
    стало привычным, потому что GitHub, GitLab и многие редакторы настраивают эту опцию сами при
    установке, но сам Git её не устанавливает. Поэтому Cartesian School задаёт её явно, а не
    полагается на то, что окажется настроено на конкретном компьютере:</p>
    {code_block("Терминал", "git config --global init.defaultBranch main\n", lang="text")}

    {callout(
        "warning",
        "Git 2.28 добавил настройку, а не новое поведение",
        "Легко перепутать эти две вещи. Git 2.28 (выпущен в 2020 году) добавил опцию "
        "<code class=\"inline\">init.defaultBranch</code> — раньше такой настройки не "
        "существовало вообще, и переименовать первую ветку можно было только вручную после "
        "создания репозитория. Но сама опция ничего не меняет, пока её не задать: без неё Git "
        "по-прежнему создаёт ветку <code class=\"inline\">master</code>, в любой версии, вплоть "
        "до самой новой. Проверить это можно на чистом окружении без "
        "<code class=\"inline\">~/.gitconfig</code> — там <code class=\"inline\">git init</code> "
        "создаёт именно <code class=\"inline\">master</code>.",
    )}

    {official_sources([("Set up Git", "https://docs.github.com/en/get-started/git-basics/set-up-git")])}

    {summary_box("Коротко", [
        "user.name/user.email записываются в каждый коммит — это данные автора, а не логин GitHub.",
        "--global применяет настройку сразу ко всем репозиториям на компьютере.",
        "Git 2.28 добавил настройку init.defaultBranch, но встроенное имя первой ветки по-прежнему master — main нужно задать явно.",
    ])}
    """
    out = render_page(
        page_title="Первая настройка Git",
        description="user.name и user.email записываются в каждый коммит; --global применяет настройку ко всем репозиториям.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Настройка Git", "")],
        kicker="Глава 23 · Часть I · Git и GitHub с нуля",
        h1="Первая настройка Git",
        lede="Прежде чем сделать первый коммит, Git нужно один раз сказать, кто вы, — это записывается в каждый коммит.",
        body_html=body,
        sidebar_groups=sidebar("23-git-03-pervaya-nastrojka.html"),
        nav=PageNav(prev_href="23-git-02-ustanavlivaem-git.html", prev_label="Устанавливаем Git", next_href="23-git-04-github-account.html", next_label="Учётная запись GitHub"),
    )
    write("23-git-03-pervaya-nastrojka.html", out)


def build_git_04() -> None:
    body = f"""
    {stage_tracker(1)}

    <p>Работа с GitHub требует учётной записи. Завести её просто, но пара решений на этом шаге
    стоит того, чтобы принять их осознанно.</p>

    <h2>Имя пользователя</h2>
    <p>Имя пользователя GitHub становится частью адреса каждого вашего репозитория
    (<code class="inline">github.com/имя/репозиторий</code>) и видно всем — стоит выбрать
    что-то, что не жалко будет использовать в резюме или портфолио, а не сиюминутный
    никнейм.</p>

    <h2>Email</h2>
    <p>GitHub требует подтверждённый email. Если не хочется, чтобы личный адрес попадал в
    историю коммитов при публикации репозитория, GitHub предоставляет приватный
    <code class="inline">@users.noreply.github.com</code>-адрес — специально для этого
    случая.</p>

    <h2>Пароль и двухфакторная аутентификация</h2>
    <p>GitHub поддерживает вход по паролю с двухфакторной аутентификацией (2FA) и по
    passkey. Включить 2FA стоит сразу: учётная запись на GitHub — это не просто набор файлов,
    а доступ к публикации кода от вашего имени.</p>

    {decision_map([
        ("Личный email в коммитах нежелателен", "используйте noreply-адрес GitHub"),
        ("Нужен резервный способ входа", "сохраните коды восстановления при включении 2FA"),
        ("Забыт пароль", "используйте официальное восстановление доступа, не сторонние сервисы"),
    ], title="Частые решения при создании аккаунта")}

    {official_sources([
        ("Signing up for a new GitHub account", "https://docs.github.com/en/get-started/onboarding/getting-started-with-your-github-account"),
        ("About two-factor authentication", "https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/about-two-factor-authentication"),
    ])}

    {summary_box("Коротко", [
        "Имя пользователя становится частью адреса каждого репозитория — выбирайте осознанно.",
        "Приватный noreply-адрес GitHub скрывает личный email из истории коммитов.",
        "Двухфакторная аутентификация стоит того, чтобы включить её сразу, а не откладывать.",
    ])}
    """
    out = render_page(
        page_title="Создаём и защищаем учётную запись GitHub",
        description="Имя пользователя, email (в том числе приватный noreply-адрес) и двухфакторная аутентификация.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Аккаунт GitHub", "")],
        kicker="Глава 23 · Часть I · Git и GitHub с нуля",
        h1="Создаём и защищаем учётную запись GitHub",
        lede="Имя пользователя, email и двухфакторная аутентификация — несколько решений стоит принять осознанно с самого начала.",
        body_html=body,
        sidebar_groups=sidebar("23-git-04-github-account.html"),
        nav=PageNav(prev_href="23-git-03-pervaya-nastrojka.html", prev_label="Настройка Git", next_href="23-git-05-autentifikaciya.html", next_label="HTTPS, SSH и аутентификация"),
    )
    write("23-git-04-github-account.html", out)


def build_git_05() -> None:
    body = f"""
    {stage_tracker(1)}

    <p>Открыть github.com в браузере и работать с Git из терминала — два разных способа
    подтвердить, что это действительно вы, и у них разные механизмы.</p>

    {flow_diagram([
        ("Браузер", "вход в аккаунт — пароль/passkey + 2FA"),
        ("Git по HTTPS", "credential helper или GitHub CLI, не пароль напрямую"),
        ("Git по SSH", "пара ключей — приватный остаётся на компьютере"),
    ], caption="Три разных способа подтвердить, что это вы — у каждого свой механизм")}

    {callout(
        "warning",
        "Пароль напрямую для git push больше не работает",
        "Раньше можно было использовать пароль аккаунта прямо при git push по HTTPS — GitHub "
        "отключил этот способ. Сейчас HTTPS требует personal access token через credential "
        "helper или вход через GitHub CLI (<code class=\"inline\">gh auth login</code>), а не "
        "пароль напрямую.",
    )}

    {comparison_table(
        ["HTTPS", "SSH"],
        [
            ["URL вида https://github.com/OWNER/REPO.git", "URL вида git@github.com:OWNER/REPO.git"],
            ["Работает почти везде, включая сети со строгим firewall", "Может требовать открытый порт 22"],
            ["Аутентификация через credential helper / GitHub CLI", "Аутентификация через пару SSH-ключей"],
        ],
    )}

    <p>Курс использует <strong>SSH</strong> как основной путь: один раз настроенная пара
    ключей работает для любого числа репозиториев без повторного ввода токена — а следующая
    страница проведёт через настройку целиком. Это не значит, что SSH объективно лучше во
    всех случаях: в сети с жёстким firewall, блокирующим порт 22, HTTPS может быть
    единственным рабочим вариантом.</p>

    {official_sources([("About authentication to GitHub", "https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github")])}

    {summary_box("Коротко", [
        "Вход в браузере, Git по HTTPS и Git по SSH — три разных механизма аутентификации.",
        "Пароль аккаунта напрямую для git push больше не работает — только token или SSH-ключ.",
        "Курс использует SSH как основной путь; HTTPS остаётся рабочей альтернативой.",
    ])}
    """
    out = render_page(
        page_title="HTTPS, SSH и аутентификация",
        description="Вход в браузере, Git по HTTPS (credential helper) и Git по SSH (пара ключей) — три разных механизма.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Аутентификация", "")],
        kicker="Глава 23 · Часть I · Git и GitHub с нуля",
        h1="HTTPS, SSH и аутентификация",
        lede="Браузер, Git по HTTPS и Git по SSH подтверждают личность тремя разными способами — курс использует SSH.",
        body_html=body,
        sidebar_groups=sidebar("23-git-05-autentifikaciya.html"),
        nav=PageNav(prev_href="23-git-04-github-account.html", prev_label="Аккаунт GitHub", next_href="23-git-06-ssh.html", next_label="Настраиваем SSH"),
    )
    write("23-git-05-autentifikaciya.html", out)


def build_git_06() -> None:
    body = f"""
    {stage_tracker(1)}

    {flow_diagram([
        ("Ваш компьютер", "приватный ключ — никогда его не покидает"),
        ("ssh-agent", "хранит расшифрованный ключ в памяти на время сессии"),
        ("GitHub", "публичный ключ — подтверждает подлинность, не даёт доступа сам по себе"),
    ], caption="Приватный ключ доказывает личность, не покидая компьютер; на GitHub попадает только публичный")}

    <p>SSH-аутентификация строится на паре ключей: приватный остаётся на вашем компьютере и
    никогда никому не передаётся, публичный — загружается в настройки GitHub. GitHub
    проверяет, что у вас есть приватная половина пары, не видя её саму.</p>

    <h2>Создаём ключ</h2>
    {code_block(
        "Документированная команда — см. официальную инструкцию GitHub",
        'ssh-keygen -t ed25519 -C "you@example.com"\n',
        lang="text",
    )}
    <p>На вопрос о файле для сохранения обычно достаточно нажать Enter (путь по умолчанию),
    а парольную фразу (passphrase) стоит задать — это дополнительная защита ключа на диске.</p>

    <h2>Добавляем ключ в ssh-agent</h2>
    {code_block(
        "Документированная команда",
        "eval \"$(ssh-agent -s)\"\n"
        "ssh-add ~/.ssh/id_ed25519\n",
        lang="text",
    )}

    <h2>Добавляем публичный ключ в GitHub</h2>
    <p>Содержимое файла <code class="inline">~/.ssh/id_ed25519.pub</code> копируется в
    Settings → SSH and GPG keys → New SSH key.</p>

    <h2>Проверяем соединение</h2>
    {code_block(
        "Документированная команда",
        "ssh -T git@github.com\n"
        "# Hi USERNAME! You've successfully authenticated, but GitHub does not provide shell access.\n",
        lang="text",
    )}
    {callout(
        "info",
        "Это сообщение — не ошибка",
        "GitHub не предоставляет интерактивную оболочку по SSH — фраза «does not provide shell "
        "access» означает ровно то, что она говорит: соединение и аутентификация прошли "
        "успешно, именно это и было целью проверки.",
    )}

    {official_sources([
        ("About SSH", "https://docs.github.com/en/authentication/connecting-to-github-with-ssh/about-ssh"),
        ("Generating a new SSH key and adding it to the ssh-agent", "https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent"),
        ("Adding a new SSH key to your GitHub account", "https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account"),
    ])}

    {summary_box("Коротко", [
        "Приватный ключ никогда не покидает компьютер; на GitHub загружается только публичный.",
        "ssh-keygen создаёт пару, ssh-add добавляет её в ssh-agent на время сессии.",
        "ssh -T git@github.com проверяет соединение — сообщение об отсутствии shell-доступа означает успех.",
    ])}
    """
    out = render_page(
        page_title="Настраиваем SSH",
        description="Пара SSH-ключей: приватный остаётся на компьютере, публичный загружается в настройки GitHub.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("SSH", "")],
        kicker="Глава 23 · Часть I · Git и GitHub с нуля",
        h1="Настраиваем SSH",
        lede="Приватный ключ остаётся на компьютере и доказывает личность, не покидая его; публичный ключ уходит на GitHub.",
        body_html=body,
        sidebar_groups=sidebar("23-git-06-ssh.html"),
        nav=PageNav(prev_href="23-git-05-autentifikaciya.html", prev_label="Аутентификация", next_href="23-git-07-sozdaem-repozitorij.html", next_label="Создаём репозиторий SafeSort"),
    )
    write("23-git-06-ssh.html", out)


def build_git_07() -> None:
    body = f"""
    {stage_tracker(1)}

    <div style="display:flex;align-items:center;gap:8px;font-family:Sora,sans-serif;font-weight:700;
      font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:#5B24F9;margin:8px 0 16px">
      {github_mark()}<span>Настоящий репозиторий этой главы</span>
    </div>

    <p>Учётная запись готова, аутентификация настроена — пора создать настоящий репозиторий
    для SafeSort. Именно этот репозиторий, <code class="inline">Cartesian-School/safesort</code>,
    используется на всех оставшихся страницах главы: каждый Issue, каждая ветка, каждый
    Pull Request и финальный релиз, которые здесь показаны, — реальные.</p>

    {image_figure(
        f"{IMG}/safesort-repo-home.jpg",
        "Главная страница реального репозитория Cartesian-School/safesort на GitHub: файлы, README, история коммитов, вкладки Issues/Pull requests/Actions/Projects",
        "Реальный репозиторий SafeSort — тот, что используется во всей оставшейся части главы.",
        size="wide",
    )}

    <h2>Поля формы создания репозитория</h2>
    {comparison_table(
        ["Поле", "Что оно значит"],
        [
            ["Owner", "аккаунт или организация, которой принадлежит репозиторий"],
            ["Repository name", "часть адреса github.com/OWNER/ИМЯ — короткое, без пробелов"],
            ["Description", "одна строка, видна в списке репозиториев и в поиске"],
            ["Public / Private", "виден ли репозиторий всем или только тем, кого вы пригласили"],
            ["Add a README", "создать ли стартовый README.md сразу при создании"],
            [".gitignore template", "готовый шаблон исключений для конкретного языка"],
            ["License", "лицензия, под которой распространяется код — например, MIT"],
        ],
    )}

    <h2>Пустой репозиторий или сразу с README?</h2>
    <p>Есть два пути: создать репозиторий с README/.gitignore/лицензией сразу на GitHub — или
    создать его пустым и запушить туда уже готовый локальный проект. Эта глава идёт вторым
    путём: пустой репозиторий на GitHub, а первый коммит (README, LICENSE, .gitignore,
    pyproject.toml) приходит с локальной машины — так с самого начала понятно, что именно
    легло в историю первым коммитом, а не появилось «само» через веб-интерфейс.</p>

    {official_sources([("Creating a new repository", "https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository")])}

    {summary_box("Коротко", [
        "Cartesian-School/safesort — настоящий репозиторий, используемый во всей оставшейся части главы.",
        "Repository name становится частью адреса; Public/Private определяет видимость.",
        "Курс создаёт пустой репозиторий на GitHub и пушит в него готовый локальный первый коммит.",
    ])}
    """
    out = render_page(
        page_title="Создаём репозиторий SafeSort на GitHub",
        description="Настоящий репозиторий Cartesian-School/safesort — используется во всей оставшейся части главы.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Репозиторий SafeSort", "")],
        kicker="Глава 23 · Часть I · Git и GitHub с нуля",
        h1="Создаём репозиторий SafeSort на GitHub",
        lede="Настоящий репозиторий Cartesian-School/safesort — тот, что используется во всей оставшейся части главы.",
        body_html=body,
        sidebar_groups=sidebar("23-git-07-sozdaem-repozitorij.html"),
        nav=PageNav(prev_href="23-git-06-ssh.html", prev_label="Настраиваем SSH", next_href="23-git-08-kloniruem.html", next_label="Клонируем репозиторий"),
    )
    write("23-git-07-sozdaem-repozitorij.html", out)


def build_git_08() -> None:
    body = f"""
    {stage_tracker(1)}

    <p>Репозиторий существует на GitHub — но, чтобы писать код, его нужно получить на свой
    компьютер. <code class="inline">git clone</code> скачивает репозиторий целиком, вместе со
    всей его историей коммитов, и сразу настраивает связь с GitHub как <code class="inline">
    origin</code> (следующая страница разберёт это подробнее).</p>

    {flow_diagram([
        ("GitHub", "Cartesian-School/safesort"),
        ("git clone", "скачивает файлы и всю историю"),
        ("Ваш компьютер", "локальная копия, готовая к работе"),
    ], caption="git clone — единственная команда, разом создающая полную локальную копию")}

    {terminal_capture([
        "$ git clone https://github.com/Cartesian-School/safesort.git",
        "Cloning into 'safesort'...",
        "$ cd safesort",
        "$ git status",
        "On branch main",
        "Your branch is up to date with 'origin/main'.",
        "",
        "nothing to commit, working tree clean",
        "$ git log --oneline -5",
        "fe610cf docs: fill in CHANGELOG for 0.1.0 (#23)",
        "c376fba feat: add command-line interface (#21)",
        "01989e0 feat: add duplicate detection with byte-level confirmation (#20)",
        "29c6328 feat: record operation manifest and add undo (#19)",
        "c5e34d5 feat: add explicit apply operation (#18)",
    ], caption="Как эталонный репозиторий Cartesian-School/safesort выглядит сейчас — с уже завершённой историей")}

    {callout(
        "info",
        "Эталонный репозиторий подготовлен для курса заранее",
        "git log --oneline сразу после клонирования показывает не пустую историю, а все "
        "коммиты, которые уже есть в репозитории на GitHub, — клонирование скачивает полную "
        "историю, а не только последнее состояние файлов. И это не пустой репозиторий: "
        "Cartesian-School/safesort подготовлен для курса заранее, со всеми Issue, ветками, "
        "Pull Request и релизом v0.1.0 уже сделанными. Учебные шаги этой главы показывают, "
        "как такой проект строится с нуля, но настоящая история эталонного репозитория — не "
        "покадровая запись этих шагов, а её собственная, отдельная и полностью честная "
        "последовательность реальных коммитов. Ниже по главе явные пометки различают "
        "«РЕАЛЬНОЕ СВИДЕТЕЛЬСТВО РЕПОЗИТОРИЯ» (то, что действительно есть в этой истории) и "
        "«УЧЕБНЫЙ ПРИМЕР» (иллюстрация приёма на отдельном тренировочном материале).",
    )}

    {official_sources([("Cloning a repository", "https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository")])}

    {summary_box("Коротко", [
        "git clone скачивает репозиторий целиком — файлы и всю историю коммитов, не только последнее состояние.",
        "После клонирования git status сразу показывает связь с origin — GitHub уже настроен как удалённый репозиторий.",
        "git log --oneline после клонирования сразу показывает настоящую историю проекта.",
    ])}
    """
    out = render_page(
        page_title="Клонируем репозиторий",
        description="git clone скачивает репозиторий целиком — файлы и всю историю коммитов — и сразу настраивает origin.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Клонирование", "")],
        kicker="Глава 23 · Часть I · Git и GitHub с нуля",
        h1="Клонируем репозиторий",
        lede="git clone создаёт полную локальную копию репозитория разом — файлы, всю историю и связь с GitHub.",
        body_html=body,
        sidebar_groups=sidebar("23-git-08-kloniruem.html"),
        nav=PageNav(prev_href="23-git-07-sozdaem-repozitorij.html", prev_label="Репозиторий SafeSort", next_href="23-git-09-lokalnyj-i-udalennyj.html", next_label="Локальный и удалённый репозиторий"),
    )
    write("23-git-08-kloniruem.html", out)


def build_git_09() -> None:
    body = f"""
    {stage_tracker(1)}

    <p><code class="inline">origin</code> — не специальный сервер и не зарезервированное
    слово Git, а просто имя, которое <code class="inline">git clone</code> дал одному
    конкретному удалённому репозиторию по умолчанию. Ничто не мешает называть удалённые
    репозитории иначе — но <code class="inline">origin</code> для «того, откуда всё началось»
    настолько общепринято, что почти никто не выбирает другое имя без веской причины.</p>

    {terminal_capture([
        "$ git remote -v",
        "origin\thttps://github.com/Cartesian-School/safesort.git (fetch)",
        "origin\thttps://github.com/Cartesian-School/safesort.git (push)",
    ])}

    {flow_diagram([
        ("Локальный репозиторий", "ветка main на вашем компьютере"),
        ("origin", "имя удалённого репозитория — просто ссылка на URL"),
        ("GitHub", "Cartesian-School/safesort"),
    ], caption="origin — имя, а не адрес; сам адрес хранится отдельно и виден через git remote -v")}

    <p>Один локальный репозиторий может иметь несколько удалённых — например, «origin» для
    основного репозитория и «upstream» для оригинала, из которого сделан fork (этот сценарий
    встретится в домашней практике, где студенты работают в собственном fork
    <code class="inline">python-mini-projects</code>).</p>

    {official_sources([
        ("About remote repositories", "https://docs.github.com/en/get-started/git-basics/about-remote-repositories"),
        ("Managing remote repositories", "https://docs.github.com/en/get-started/git-basics/managing-remote-repositories"),
    ])}

    {summary_box("Коротко", [
        "origin — имя удалённого репозитория, которое git clone назначает по умолчанию, а не специальное слово Git.",
        "git remote -v показывает настоящий URL, стоящий за именем origin.",
        "У одного локального репозитория может быть несколько удалённых — например, origin и upstream при работе с fork.",
    ])}
    """
    out = render_page(
        page_title="Локальный и удалённый репозиторий",
        description="origin — имя удалённого репозитория, назначенное git clone по умолчанию, а не специальное слово Git.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Remotes", "")],
        kicker="Глава 23 · Часть I · Git и GitHub с нуля",
        h1="Локальный и удалённый репозиторий",
        lede="origin — просто имя для удалённого репозитория, которое git clone назначает по умолчанию.",
        body_html=body,
        sidebar_groups=sidebar("23-git-09-lokalnyj-i-udalennyj.html"),
        nav=PageNav(prev_href="23-git-08-kloniruem.html", prev_label="Клонируем репозиторий", next_href="23-git-10-working-tree-staging-commit.html", next_label="Working tree, staging и commit"),
    )
    write("23-git-09-lokalnyj-i-udalennyj.html", out)


def build_git_10() -> None:
    body = f"""
    {stage_tracker(1)}

    <p>Прежде чем что-то менять в SafeSort, стоит один раз чётко понять три состояния, через
    которые проходит любое изменение файла в Git.</p>

    {flow_diagram([
        ("Working tree", "файлы на диске — то, что видит текстовый редактор"),
        ("git add", "Staging area / индекс — что попадёт в следующий коммит"),
        ("git commit", "Локальный репозиторий — постоянная запись в истории"),
        ("git push", "GitHub — та же история, опубликованная удалённо"),
    ], caption="Четыре состояния одного изменения — от файла на диске до истории на GitHub")}

    {comparison_table(
        ["Команда", "Что показывает"],
        [
            ["git status", "какие файлы изменены, какие уже в staging, какие Git вообще не отслеживает"],
            ["git diff", "построчные изменения в рабочем дереве, ещё не добавленные в staging"],
            ["git diff --staged", "построчные изменения, уже добавленные в staging — то, что попадёт в коммит"],
            ["git log", "история коммитов — что уже стало постоянной записью"],
        ],
    )}

    <p>Ниже — <strong>учебный пример</strong> на отдельном, специально созданном для
    демонстрации каталоге (не в самом SafeSort — в клонированном репозитории README.md уже
    закоммичен, это было видно в части III), чтобы показать, как эти четыре команды выглядят
    на практике при самом первом коммите нового файла:</p>

    {terminal_capture([
        "$ git status",
        "?? notes.md",
        "$ git add notes.md",
        "$ git status",
        "A  notes.md",
        "$ git commit -m \"Add notes\"",
        "[main (root-commit) a1c2e9f] Add notes",
        " 1 file changed, 1 insertion(+)",
        " create mode 100644 notes.md",
        "$ git log --oneline",
        "a1c2e9f Add notes",
    ], cwd="~/demo-project", caption="УЧЕБНЫЙ ПРИМЕР — отдельный тренировочный каталог, не репозиторий SafeSort")}

    <p>Разница между <code class="inline">git diff</code> и <code class="inline">git diff
    --staged</code> — источник частой путаницы: первая команда сравнивает рабочее дерево с
    staging, вторая — staging с последним коммитом. Если файл добавлен через
    <code class="inline">git add</code>, а потом ещё раз изменён, <code class="inline">git
    diff</code> покажет только это последнее, ещё не добавленное изменение.</p>

    {summary_box("Коротко", [
        "Working tree → staging (git add) → локальный репозиторий (git commit) → GitHub (git push) — четыре состояния одного изменения.",
        "git diff сравнивает рабочее дерево со staging; git diff --staged — staging с последним коммитом.",
        "git log показывает историю уже сделанных коммитов — постоянных записей.",
    ])}
    """
    out = render_page(
        page_title="Working tree, staging и commit",
        description="Working tree, staging area, локальный репозиторий и GitHub — четыре состояния одного изменения.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Working tree", "")],
        kicker="Глава 23 · Часть I · Git и GitHub с нуля",
        h1="Working tree, staging и commit",
        lede="Working tree, staging, локальный репозиторий и GitHub — четыре состояния, через которые проходит любое изменение.",
        body_html=body,
        sidebar_groups=sidebar("23-git-10-working-tree-staging-commit.html"),
        nav=PageNav(prev_href="23-git-09-lokalnyj-i-udalennyj.html", prev_label="Локальный и удалённый репозиторий", next_href="23-proj-01-repo-vs-project.html", next_label="Repository и GitHub Project"),
    )
    write("23-git-10-working-tree-staging-commit.html", out)


def build_proj_01() -> None:
    body = f"""
    {stage_tracker(2)}

    <p>Часть I уже разделила Git и GitHub. Здесь — вторая частая путаница: репозиторий
    и <strong>GitHub Project</strong> — тоже разные, независимые понятия, и легко решить, что
    раз оба слова начинаются с «проект», это одно и то же.</p>

    {comparison_table(
        ["Repository", "GitHub Project"],
        [
            ["код, файлы, история коммитов", "задачи, их статус, представления (доска/таблица)"],
            ["ветки, теги, Pull Request", "может объединять Issues сразу из нескольких репозиториев"],
            ["отвечает на вопрос «что уже сделано»", "отвечает на вопрос «что нужно сделать и в каком порядке»"],
            ["обязателен — без него нет кода", "необязателен — можно работать вообще без Project"],
        ],
    )}

    {flow_diagram([
        ("Issue", "формулировка задачи"),
        ("GitHub Project", "статус, приоритет, представление"),
        ("Ветка / Pull Request", "работа над задачей и её результат"),
    ], caption="Project не хранит код — он отслеживает статус задач, которые ссылаются на репозиторий")}

    {callout(
        "info",
        "Один Project может охватывать несколько репозиториев",
        "GitHub Project — не часть репозитория и не находится «внутри» него: это отдельный "
        "объект, который может показывать Issues и Pull Request сразу из нескольких "
        "репозиториев одной организации. Для SafeSort в этой главе используется один Project "
        "на один репозиторий — но так бывает не всегда.",
    )}

    {official_sources([("About Projects", "https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects")])}

    {summary_box("Коротко", [
        "Repository хранит код и историю; GitHub Project отслеживает статус задач — это разные объекты.",
        "Project не обязателен: можно вести репозиторий вообще без него.",
        "Один Project может объединять Issues из нескольких репозиториев организации.",
    ])}
    """
    out = render_page(
        page_title="Repository и GitHub Project — в чём разница",
        description="Repository хранит код и историю; GitHub Project отслеживает статус задач — разные, независимые объекты.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Repository vs Project", "")],
        kicker="Глава 23 · Часть II · Планируем SafeSort на GitHub",
        h1="Repository и GitHub Project — в чём разница",
        lede="Repository хранит код; GitHub Project отслеживает статус задач — два разных, независимых объекта.",
        body_html=body,
        sidebar_groups=sidebar("23-proj-01-repo-vs-project.html"),
        nav=PageNav(prev_href="23-git-10-working-tree-staging-commit.html", prev_label="Working tree, staging, commit", next_href="23-proj-02-luchshie-praktiki.html", next_label="Лучшие практики Project"),
    )
    write("23-proj-01-repo-vs-project.html", out)


def build_proj_02() -> None:
    body = f"""
    {stage_tracker(2)}

    <p>Создать Project — секундное дело; ошибка, которую совершает почти каждый новичок, —
    сразу добавить десяток полей и три представления «на будущее», а через месяц забросить
    большинство из них. Прежде чем нажать «New project», стоит принять несколько решений
    осознанно.</p>

    <h2>Решить область действия заранее</h2>
    <p>Project можно привязать к одному репозиторию или объединить в нём несколько.
    Для SafeSort ответ простой — один Project на один репозиторий, потому что вся работа
    этой главы происходит в <code class="inline">Cartesian-School/safesort</code> и нет
    смысла тянуть в один список задачи из других репозиториев курса.</p>

    <h2>Меньше полей — лучше</h2>
    {comparison_table(
        ["Вместо", "Лучше"],
        [
            ["поле «на всякий случай», которое никто не заполняет", "поле, отвечающее на конкретный вопрос (кто важнее, что за часть кода)"],
            ["свободный текст там, где вариантов на самом деле немного", "Single select с заранее известным списком значений"],
            ["новое представление для каждой идеи «а вдруг пригодится»", "одно-два представления, которые реально открывают каждый день"],
        ],
    )}

    {callout(
        "info",
        "Статус — почти всегда достаточно одного поля для отслеживания прогресса",
        "У GitHub Project уже есть встроенное поле Status. Прежде чем добавлять что-то ещё, "
        "стоит спросить: отвечает ли новое поле на вопрос, которого Status не покрывает? Для "
        "SafeSort это Priority (что делать в первую очередь) и Area (к какой части кода "
        "относится задача) — оба поля появятся дальше в этой части главы.",
    )}

    <h2>Поля и представления можно менять позже</h2>
    <p>Ничего из решённого на этом шаге не высечено в камне: GitHub позволяет добавить,
    переименовать или удалить поле и представление в любой момент, не теряя уже собранные
    данные. Ошибка новичка — не «выбрать неправильное поле», а решить всё сразу и никогда
    не пересматривать.</p>

    {official_sources([("Best practices for Projects", "https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects")])}

    {summary_box("Коротко", [
        "Перед созданием Project стоит решить его область действия — один репозиторий или несколько.",
        "Меньше полей и представлений, каждое из которых реально используется, лучше десятка «на будущее».",
        "Status — встроенное поле; собственные поля стоит добавлять только когда Status не отвечает на нужный вопрос.",
    ])}
    """
    out = render_page(
        page_title="Как спланировать Project: лучшие практики",
        description="Прежде чем создавать GitHub Project: область действия, минимум полей, встроенный Status вместо самодельных полей.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Лучшие практики", "")],
        kicker="Глава 23 · Часть II · Планируем SafeSort на GitHub",
        h1="Как спланировать Project: лучшие практики",
        lede="Project легко создать за секунду и так же легко захламить десятком неиспользуемых полей — несколько решений стоит принять заранее.",
        body_html=body,
        sidebar_groups=sidebar("23-proj-02-luchshie-praktiki.html"),
        nav=PageNav(prev_href="23-proj-01-repo-vs-project.html", prev_label="Repository vs Project", next_href="23-proj-03-sozdaem-project.html", next_label="Создаём GitHub Project"),
    )
    write("23-proj-02-luchshie-praktiki.html", out)


def build_proj_03() -> None:
    body = f"""
    {stage_tracker(2)}

    <p>Прежде чем писать код SafeSort, полезно составить список того, что нужно сделать, —
    GitHub Project даёт для этого готовое место, связанное с реальными Issues репозитория.</p>

    <h2>Что заполняется при создании</h2>
    {comparison_table(
        ["Поле", "Значение"],
        [
            ["Owner", "организация или аккаунт — здесь Cartesian-School"],
            ["Title", "например, «SafeSort — первый релиз»"],
            ["Template", "пустой Project или один из готовых шаблонов (Board, Roadmap...)"],
            ["Visibility", "виден ли Project всем или только участникам организации"],
        ],
    )}

    {callout(
        "warning",
        "На момент подготовки этой страницы live-доступ к Projects ещё не был предоставлен",
        "Создание GitHub Project требует отдельного разрешения (\"project\" scope) для "
        "инструмента, которым собирается этот курс, — предоставляется отдельно от доступа к "
        "самому репозиторию. Реальные скриншоты доски Project (созданный Project, Board, "
        "Table, перемещение элементов между статусами) появятся на этой и следующих страницах "
        "после того, как доступ будет подтверждён; текстовое и диаграммное описание работы "
        "Project точное и основано на официальной документации независимо от этого.",
    )}

    <h2>Название без номера версии</h2>
    <p>Название Project для этой главы — <strong>«SafeSort — первый релиз»</strong>, без
    номера <code class="inline">0.1.0</code>: часть VI введёт версии только тогда, когда
    первая версия действительно будет готова, и называть Project по номеру раньше времени —
    забегать вперёд без необходимости.</p>

    {official_sources([("Creating a project", "https://docs.github.com/en/issues/planning-and-tracking-with-projects/creating-projects/creating-a-project")])}

    {summary_box("Коротко", [
        "GitHub Project создаётся для конкретного владельца (организации или аккаунта) с названием и уровнем видимости.",
        "Название Project для SafeSort не включает номер версии — версия появляется позже.",
        "Project изначально пуст: следующие разделы показывают его представления, поля, а затем — как в него попадают задачи.",
    ])}
    """
    out = render_page(
        page_title="Создаём GitHub Project",
        description="GitHub Project для SafeSort: владелец, название без номера версии, уровень видимости.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Создаём Project", "")],
        kicker="Глава 23 · Часть II · Планируем SafeSort на GitHub",
        h1="Создаём GitHub Project",
        lede="Прежде чем писать код, GitHub Project даёт место для списка задач, связанного с реальными Issues репозитория.",
        body_html=body,
        sidebar_groups=sidebar("23-proj-03-sozdaem-project.html"),
        nav=PageNav(prev_href="23-proj-02-luchshie-praktiki.html", prev_label="Лучшие практики", next_href="23-proj-04-kopiruem-project.html", next_label="Копируем существующий Project"),
    )
    write("23-proj-03-sozdaem-project.html", out)


def build_proj_04() -> None:
    body = f"""
    {stage_tracker(2)}

    <p>Создать Project с нуля — не единственный способ начать. Если в организации уже есть
    Project с нужным набором статусов, полей и представлений, GitHub позволяет
    <strong>скопировать</strong> его: новый Project получает ту же структуру, но пустой список
    задач — прошлые Issues, Pull Request и история статусов не переносятся.</p>

    {flow_diagram([
        ("Существующий Project", "поля, статусы, представления уже настроены"),
        ("Copy", "новый Project с той же структурой"),
        ("Пустой список задач", "старые элементы не копируются — только структура"),
    ], caption="Копирование переносит структуру Project, а не его содержимое")}

    {callout(
        "info",
        "SafeSort создаётся с нуля — копировать пока нечего",
        "У Cartesian-School на момент подготовки этой главы ещё не было готового Project с "
        "нужной структурой, поэтому Project «SafeSort — первый релиз» создаётся заново "
        "(предыдущий раздел), а не копированием. Но у копирования есть реальное применение "
        "для курса: после того как этот Project будет готов, он сам может стать заготовкой "
        "для планирования следующих больших проектных глав — не нужно будет заново придумывать "
        "статусы Backlog / Ready / In Progress / In Review / Done и поля Priority / Area.",
    )}

    <h2>Когда копирование окупается</h2>
    <p>Копирование полезно, когда команда уже выработала удобный набор статусов и полей и
    не хочет каждый раз собирать его заново, — типичный случай: несколько похожих релизов
    подряд или несколько похожих учебных проектов один за другим. Для первого Project в
    организации копировать попросту не с чего, и создание с нуля — не компромисс, а
    единственный доступный путь.</p>

    {official_sources([("Copying an existing project", "https://docs.github.com/en/issues/planning-and-tracking-with-projects/creating-projects/copying-an-existing-project")])}

    {summary_box("Коротко", [
        "Копирование Project переносит его структуру — поля, статусы, представления — но не сами задачи.",
        "SafeSort создан с нуля, потому что подходящего Project для копирования ещё не существовало.",
        "Копирование окупается, когда одна и та же структура нужна для нескольких похожих проектов подряд.",
    ])}
    """
    out = render_page(
        page_title="Копируем существующий Project",
        description="Copy Project переносит структуру — поля, статусы, представления — но не задачи; SafeSort создан с нуля.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Копируем Project", "")],
        kicker="Глава 23 · Часть II · Планируем SafeSort на GitHub",
        h1="Копируем существующий Project",
        lede="Copy Project переносит структуру — поля, статусы, представления, — но не переносит сами задачи.",
        body_html=body,
        sidebar_groups=sidebar("23-proj-04-kopiruem-project.html"),
        nav=PageNav(prev_href="23-proj-03-sozdaem-project.html", prev_label="Создаём Project", next_href="23-proj-05-board-table-roadmap.html", next_label="Board, Table и Roadmap"),
    )
    write("23-proj-04-kopiruem-project.html", out)


def build_proj_05() -> None:
    body = f"""
    {stage_tracker(2)}

    <p>Один и тот же набор задач можно смотреть по-разному — GitHub Project называет это
    <strong>представлениями</strong> (views): один набор элементов, несколько способов на
    него посмотреть.</p>

    {comparison_table(
        ["Представление", "Когда полезно"],
        [
            ["Board", "видеть прогресс по колонкам-статусам: Backlog / Ready / In Progress / In Review / Done"],
            ["Table", "видеть все задачи и их поля сразу — сортировать, фильтровать, группировать"],
            ["Roadmap", "видеть задачи на временной шкале — полезно при датах и дедлайнах"],
        ],
    )}

    {callout(
        "info",
        "Не каждому проекту нужны все представления",
        "Для SafeSort в этой главе хватает Board (видно, что происходит прямо сейчас) и Table "
        "(видно все задачи целиком). Roadmap имеет смысл, когда у задач есть даты начала и "
        "окончания, — здесь этого нет, и добавлять его не нужно только потому, что "
        "GitHub его предлагает.",
    )}

    <h2>Статусы для SafeSort</h2>
    {flow_diagram([
        ("Backlog", "задача сформулирована, но пока не начата"),
        ("Ready", "готова к работе — можно начинать в любой момент"),
        ("In Progress", "ветка создана, идёт разработка"),
        ("In Review", "Pull Request открыт, ждёт проверки"),
        ("Done", "изменения слиты в main"),
    ], caption="Пять статусов, через которые проходит каждая задача SafeSort")}

    {official_sources([("Changing the layout of a view", "https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/changing-the-layout-of-a-view")])}

    {summary_box("Коротко", [
        "Board, Table и Roadmap — представления одного и того же набора задач, а не отдельные наборы данных.",
        "SafeSort использует пять статусов: Backlog, Ready, In Progress, In Review, Done.",
        "Представление стоит добавлять только тогда, когда им реально будут пользоваться.",
    ])}
    """
    out = render_page(
        page_title="Board, Table и Roadmap",
        description="Board, Table и Roadmap — представления одного набора задач; пять статусов SafeSort.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Board и Table", "")],
        kicker="Глава 23 · Часть II · Планируем SafeSort на GitHub",
        h1="Board, Table и Roadmap",
        lede="Board, Table и Roadmap — разные способы посмотреть на один и тот же набор задач, а не отдельные наборы данных.",
        body_html=body,
        sidebar_groups=sidebar("23-proj-05-board-table-roadmap.html"),
        nav=PageNav(prev_href="23-proj-04-kopiruem-project.html", prev_label="Копируем Project", next_href="23-proj-06-polya.html", next_label="Поля Project"),
    )
    write("23-proj-05-board-table-roadmap.html", out)


def build_proj_06() -> None:
    body = f"""
    {stage_tracker(2)}

    <p>Каждый элемент Project — это набор полей: часть из них встроена в GitHub и есть
    у любого Project, часть можно добавить самим под конкретную задачу.</p>

    <h2>Встроенные поля</h2>
    {comparison_table(
        ["Поле", "Откуда берётся"],
        [
            ["Title", "заголовок Issue или Pull Request"],
            ["Assignees", "кому назначена задача в самом Issue"],
            ["Status", "колонка Board — управляется Project, не репозиторием"],
            ["Labels", "метки Issue/PR из репозитория"],
            ["Repository", "какой репозиторий, если Project объединяет несколько"],
            ["Linked pull requests", "PR, связанные с Issue через «Closes #N»"],
        ],
    )}
    <p>Эти поля Project не придумывает сам — он либо читает их из репозитория (Title,
    Assignees, Labels), либо управляет ими только внутри себя (Status).</p>

    <h2>Типы пользовательских полей</h2>
    {comparison_table(
        ["Тип поля", "Когда использовать"],
        [
            ["Text", "короткая произвольная заметка — например, ссылка на обсуждение"],
            ["Number", "числовое значение — например, оценка сложности в часах"],
            ["Date", "конкретная дата — например, дедлайн, если он есть"],
            ["Single select", "фиксированный список значений — то, что выбирают из выпадающего списка"],
            ["Iteration", "повторяющиеся отрезки времени — спринты, недели"],
        ],
    )}

    <h2>Два пользовательских поля SafeSort</h2>
    {comparison_table(
        ["Поле", "Тип", "Значения"],
        [
            ["Priority", "Single select", "High / Medium / Low"],
            ["Area", "Single select", "Packaging / CLI / Filesystem / Safety / Duplicates / Testing / Documentation / CI"],
        ],
    )}
    <p>Оба поля — Single select, а не Text: список значений заранее известен и конечен,
    а Single select ещё и позволяет группировать и фильтровать Table по значению, чего
    свободный текст не даёт. <code class="inline">Iteration</code> здесь не нужен — SafeSort
    не ведётся спринтами, у задач нет повторяющихся временных отрезков.</p>

    {official_sources([("Understanding fields", "https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields")])}

    {summary_box("Коротко", [
        "Встроенные поля (Title, Assignees, Status, Labels) есть у любого Project без настройки.",
        "Пользовательские поля бывают текстом, числом, датой, Single select или Iteration.",
        "SafeSort использует два поля Single select — Priority и Area — потому что список их значений заранее известен и конечен.",
    ])}
    """
    out = render_page(
        page_title="Поля Project: встроенные и пользовательские",
        description="Встроенные поля Title/Status/Labels и пользовательские типы Text/Number/Date/Single select/Iteration.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Поля Project", "")],
        kicker="Глава 23 · Часть II · Планируем SafeSort на GitHub",
        h1="Поля Project: встроенные и пользовательские",
        lede="Часть полей Project встроена в GitHub, часть можно добавить самим — под конкретный вопрос, который они должны решать.",
        body_html=body,
        sidebar_groups=sidebar("23-proj-06-polya.html"),
        nav=PageNav(prev_href="23-proj-05-board-table-roadmap.html", prev_label="Board, Table, Roadmap", next_href="23-proj-07-chernoviki.html", next_label="Черновики: задача без Issue"),
    )
    write("23-proj-06-polya.html", out)


def build_proj_07() -> None:
    body = f"""
    {stage_tracker(2)}

    <p>Не каждая мысль о будущей задаче сразу дозревает до полноценного Issue с Problem,
    Expected outcome и чек-листом Acceptance criteria. Для таких промежуточных заметок
    у Project есть <strong>черновик</strong> (draft issue) — элемент с заголовком и текстом,
    который существует только внутри Project и пока не связан ни с одним репозиторием.</p>

    {comparison_table(
        ["Issue", "Черновик (draft issue)"],
        [
            ["живёт в конкретном репозитории", "живёт только внутри Project"],
            ["у него есть номер (#14 и т.д.)", "номера нет — это ещё не запись репозитория"],
            ["виден в списке Issues репозитория", "виден только тем, у кого есть доступ к Project"],
            ["можно связать Pull Request через «Closes #N»", "связать Pull Request нельзя, пока не станет Issue"],
        ],
    )}

    {flow_diagram([
        ("Идея", "коротко записана прямо в Project"),
        ("Черновик", "заголовок и текст, статус можно менять как у любого элемента"),
        ("Дозрел до задачи", "следующий раздел — превращение в настоящий Issue"),
    ], caption="Черновик — способ зафиксировать мысль в Project раньше, чем она станет формальным Issue")}

    {callout(
        "info",
        "У SafeSort черновиков не было — но приём стоит знать",
        "Все 14 задач SafeSort с самого начала были сформулированы достаточно чётко, чтобы "
        "сразу стать полноценными Issues (следующие разделы), — черновики в их истории не "
        "использовались. Но приём полезен в проектах, где работа идёт не заранее спланированным "
        "списком, а по ходу дела: увидели проблему во время разработки — сразу записали "
        "черновиком в Project, не отвлекаясь на формулировку полноценного Issue.",
    )}

    {official_sources([("Adding items to your project", "https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-items-in-your-project/adding-items-to-your-project")])}

    {summary_box("Коротко", [
        "Черновик (draft issue) — элемент Project без репозитория и без номера, для мыслей, которые ещё не дозрели до Issue.",
        "У черновика есть заголовок, текст и статус, но нет связи с Pull Request.",
        "SafeSort обошёлся без черновиков, потому что все 14 задач были сформулированы сразу как Issues.",
    ])}
    """
    out = render_page(
        page_title="Черновики: задача без Issue",
        description="Draft issue — элемент Project без репозитория и номера, для мыслей, которые ещё не дозрели до полноценного Issue.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Черновики", "")],
        kicker="Глава 23 · Часть II · Планируем SafeSort на GitHub",
        h1="Черновики: задача без Issue",
        lede="Черновик (draft issue) фиксирует мысль внутри Project раньше, чем она станет формальным Issue репозитория.",
        body_html=body,
        sidebar_groups=sidebar("23-proj-07-chernoviki.html"),
        nav=PageNav(prev_href="23-proj-06-polya.html", prev_label="Поля Project", next_href="23-proj-08-chernovik-v-issue.html", next_label="Превращаем черновик в Issue"),
    )
    write("23-proj-07-chernoviki.html", out)


def build_proj_08() -> None:
    body = f"""
    {stage_tracker(2)}

    <p>Когда черновик дозрел до понятной задачи, его можно превратить в настоящий Issue —
    одним действием прямо из Project, без копирования текста вручную.</p>

    {flow_diagram([
        ("Черновик в Project", "заголовок и текст, репозитория ещё нет"),
        ("Convert to issue", "выбирается репозиторий-получатель"),
        ("Настоящий Issue", "появляется номер, запись видна в репозитории"),
        ("Элемент Project", "тот же элемент, поля Status/Priority/Area сохраняются"),
    ], caption="Конвертация меняет тип элемента, но не создаёт новый — это тот же элемент Project")}

    {callout(
        "info",
        "Поля не сбрасываются при конвертации",
        "Если у черновика уже был выставлен статус или заполнено поле Priority, после "
        "конвертации в Issue эти значения остаются как есть — конвертация меняет только "
        "тип элемента (черновик → Issue) и добавляет связь с репозиторием, а не пересоздаёт "
        "элемент с нуля.",
    )}

    <h2>Репозиторий выбирается в момент конвертации</h2>
    <p>У черновика изначально нет репозитория — GitHub спрашивает, в какой репозиторий
    добавить будущий Issue, только когда происходит конвертация. Для Project с несколькими
    репозиториями это осознанный выбор; для SafeSort, где Project привязан к одному
    репозиторию, ответ всегда один и тот же — <code class="inline">Cartesian-School/safesort</code>.</p>

    {official_sources([("Converting draft issues to issues", "https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-items-in-your-project/converting-draft-issues-to-issues")])}

    {summary_box("Коротко", [
        "Convert to issue превращает черновик в настоящий Issue одним действием, без ручного копирования текста.",
        "Уже заполненные поля элемента (Status, Priority и другие) сохраняются после конвертации.",
        "Репозиторий-получатель выбирается в момент конвертации — у черновика его до этого не было.",
    ])}
    """
    out = render_page(
        page_title="Превращаем черновик в Issue",
        description="Convert to issue превращает черновик Project в настоящий Issue репозитория, сохраняя уже заполненные поля.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Черновик → Issue", "")],
        kicker="Глава 23 · Часть II · Планируем SafeSort на GitHub",
        h1="Превращаем черновик в Issue",
        lede="Convert to issue превращает черновик в настоящий Issue репозитория одним действием — без ручного копирования текста.",
        body_html=body,
        sidebar_groups=sidebar("23-proj-08-chernovik-v-issue.html"),
        nav=PageNav(prev_href="23-proj-07-chernoviki.html", prev_label="Черновики", next_href="23-proj-09-issues.html", next_label="Создаём Issues"),
    )
    write("23-proj-08-chernovik-v-issue.html", out)


def build_proj_09() -> None:
    body = f"""
    {stage_tracker(2)}

    <p>Прежде чем писать код, каждая часть SafeSort формулируется как <strong>Issue</strong> —
    запись, описывающая задачу, до того как появилась хоть одна строка кода.</p>

    {comparison_table(
        ["Часть Issue", "Пример для SafeSort"],
        [
            ["Title", "«Add directory scanner»"],
            ["Problem", "SafeSort не умеет находить файлы в каталоге"],
            ["Expected outcome", "scan() обходит каталог и возвращает список FileInfo"],
            ["Acceptance criteria", "чек-лист: принимает Path, исключает .git/.venv, не следует по символическим ссылкам, покрыт тестами"],
        ],
    )}

    <p>Все 14 задач SafeSort действительно оформлены так в реальном репозитории — не
    отредактированы задним числом, а созданы как формулировка задачи до начала работы над
    ней:</p>

    {image_figure(
        f"{IMG}/safesort-issues-list.jpg",
        "Список Issues репозитория Cartesian-School/safesort: 14 закрытых задач, каждая — от scanner до релиза",
        "Настоящие 14 Issues репозитория SafeSort.",
        size="wide",
    )}

    {callout(
        "info",
        "Один Issue — не всегда один Pull Request",
        "В репозитории SafeSort 9 из 14 Issues закрыты Pull Request — но не «каждый своим»: "
        "коллизии имён (Issue №6) оказались достаточно тесно связаны с планом перемещений "
        "(Issue №3), чтобы попасть в один PR №17; то же с манифестом и undo (Issues №7 и №8 — "
        "один PR №19). Остальные пять Issues (обработка ошибок файловой системы, настройки и "
        "логирование, тестовый набор, CI, подготовка релиза) не имеют собственного "
        "выделенного PR: эта работа вошла в код по мере реализации соответствующих модулей "
        "и была закрыта записью, объясняющей, где именно она оказалась — реальная история "
        "проекта, а не выдуманная ради красивой таблицы «14 Issues → 14 PR».",
    )}

    <h2>Issue добавляется в Project</h2>
    {flow_diagram([
        ("Issue создан", "в репозитории"),
        ("Добавлен в Project", "статус по умолчанию — Backlog"),
        ("Готов к работе", "статус меняется на Ready"),
    ], caption="Issue существует в репозитории независимо от Project; добавление в Project — отдельное, необязательное действие")}

    {official_sources([
        ("About issues", "https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues"),
        ("Creating an issue", "https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue"),
        ("Adding items to your project", "https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-items-in-your-project/adding-items-to-your-project"),
    ])}

    {summary_box("Коротко", [
        "Issue формулирует задачу — что нужно сделать и как проверить результат — до того, как написан код.",
        "У каждого Issue SafeSort есть Title, Problem, Expected outcome и чек-лист Acceptance criteria.",
        "Issue существует в репозитории независимо от Project; добавление в Project — отдельный шаг.",
    ])}
    """
    out = render_page(
        page_title="Создаём Issues и добавляем в Project",
        description="Issue формулирует задачу до написания кода: Title, Problem, Expected outcome, Acceptance criteria.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Issues", "")],
        kicker="Глава 23 · Часть II · Планируем SafeSort на GitHub",
        h1="Создаём Issues и добавляем в Project",
        lede="Каждая часть SafeSort формулируется как Issue до того, как написана хоть одна строка кода.",
        body_html=body,
        sidebar_groups=sidebar("23-proj-09-issues.html"),
        nav=PageNav(prev_href="23-proj-08-chernovik-v-issue.html", prev_label="Черновик → Issue", next_href="23-proj-10-redaktiruem-elementy.html", next_label="Редактируем элементы Project"),
    )
    write("23-proj-09-issues.html", out)


def build_proj_10() -> None:
    body = f"""
    {stage_tracker(2)}

    <p>Задача редко остаётся неизменной от Backlog до Done — статус, приоритет, а иногда и
    заголовок меняются по ходу работы. У Project для этого есть три способа, разной степени
    массовости.</p>

    {comparison_table(
        ["Способ", "Когда удобен"],
        [
            ["Перетащить карточку на Board", "поменять только статус одного элемента — самый быстрый способ"],
            ["Открыть панель элемента", "изменить сразу несколько полей одного элемента — Priority, Area, Assignees"],
            ["Массовое изменение в Table", "выделить несколько строк и применить одно значение поля сразу ко всем"],
        ],
    )}

    {flow_diagram([
        ("Issue №1 создан", "статус Backlog"),
        ("Ветка feat/directory-scanner создана", "статус меняется на In Progress"),
        ("Как: перетащить карточку", "из колонки Backlog в колонку In Progress на Board"),
    ], caption="Смена статуса — самое частое редактирование элемента Project")}

    {callout(
        "info",
        "Массовое редактирование экономит время на однотипных задачах",
        "Если несколько Issues одновременно переходят в одну и ту же фазу — например, все "
        "задачи тестирования (Issues №20–23 по нумерации ноутбуков практики) готовы к работе "
        "разом, — выделение нескольких строк в Table и разовое изменение поля Status для всех "
        "выделенных быстрее, чем открывать каждый элемент по отдельности.",
    )}

    {official_sources([("Editing items in your project", "https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-items-in-your-project/editing-items-in-your-project")])}

    {summary_box("Коротко", [
        "Перетаскивание карточки на Board — самый быстрый способ изменить статус одного элемента.",
        "Панель элемента позволяет менять сразу несколько полей одного элемента за раз.",
        "Массовое редактирование в Table применяет одно значение поля сразу ко всем выделенным элементам.",
    ])}
    """
    out = render_page(
        page_title="Редактируем элементы Project",
        description="Три способа редактировать элемент Project: перетащить карточку, открыть панель, массово изменить в Table.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Редактируем элементы", "")],
        kicker="Глава 23 · Часть II · Планируем SafeSort на GitHub",
        h1="Редактируем элементы Project",
        lede="Статус, приоритет и другие поля элемента можно менять по одному, через панель или сразу массово в Table.",
        body_html=body,
        sidebar_groups=sidebar("23-proj-10-redaktiruem-elementy.html"),
        nav=PageNav(prev_href="23-proj-09-issues.html", prev_label="Создаём Issues", next_href="23-proj-11-filtr-sort-grupp.html", next_label="Фильтруем, сортируем, группируем"),
    )
    write("23-proj-10-redaktiruem-elementy.html", out)


def build_proj_11() -> None:
    body = f"""
    {stage_tracker(2)}

    <p>Table и Board показывают все элементы Project сразу, но по мере роста списка задач
    нужен способ увидеть только нужную часть — для этого у представлений есть фильтрация,
    сортировка и группировка.</p>

    {comparison_table(
        ["Операция", "Что делает", "Пример для SafeSort"],
        [
            ["Фильтр", "оставляет только элементы, подходящие под условие", "показать только Priority: High"],
            ["Сортировка", "меняет порядок строк по значению поля", "отсортировать Table по Priority"],
            ["Группировка", "разбивает элементы на секции по значению поля", "сгруппировать по Area — все задачи Filesystem вместе"],
        ],
    )}

    {callout(
        "info",
        "Фильтр и группировка решают разные задачи",
        "Фильтр убирает лишнее и оставляет подмножество — удобно, когда интересна только "
        "часть списка (например, только задачи со статусом In Progress прямо сейчас). "
        "Группировка не убирает ничего — она organiзует весь список по разделам, так что "
        "видно сразу все задачи, но разложенные по Area или по Priority.",
    )}

    <h2>Фильтр — это строка запроса</h2>
    <p>Фильтр в Project записывается как текстовый запрос вида
    <code class="inline">status:"In Review" area:CLI</code> — его можно ввести вручную в
    строке фильтра или собрать через выпадающие подсказки. Тот же синтаксис используется
    и в поиске по Issues репозитория, так что навык переносится.</p>

    {official_sources([("Filtering projects", "https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/filtering-projects")])}

    {summary_box("Коротко", [
        "Фильтр оставляет только элементы, подходящие под условие — остальные временно скрываются из представления.",
        "Сортировка меняет порядок строк; группировка раскладывает весь список по значению поля, не убирая элементы.",
        "Фильтр записывается как текстовый запрос вида status:\"In Review\" — тот же синтаксис, что и в поиске по Issues.",
    ])}
    """
    out = render_page(
        page_title="Фильтруем, сортируем и группируем",
        description="Фильтр оставляет подмножество элементов, сортировка меняет порядок строк, группировка раскладывает список по секциям.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Фильтр и группировка", "")],
        kicker="Глава 23 · Часть II · Планируем SafeSort на GitHub",
        h1="Фильтруем, сортируем и группируем",
        lede="Фильтр оставляет подмножество элементов, сортировка меняет порядок строк, группировка раскладывает весь список по секциям.",
        body_html=body,
        sidebar_groups=sidebar("23-proj-11-filtr-sort-grupp.html"),
        nav=PageNav(prev_href="23-proj-10-redaktiruem-elementy.html", prev_label="Редактируем элементы", next_href="23-proj-12-upravlyaem-predstavleniyami.html", next_label="Управляем представлениями"),
    )
    write("23-proj-11-filtr-sort-grupp.html", out)


def build_proj_12() -> None:
    body = f"""
    {stage_tracker(2)}

    <p>Настроенные фильтр, сортировку и группировку не нужно собирать заново каждый раз —
    их можно сохранить как отдельное представление (view) со своей вкладкой и именем.</p>

    {flow_diagram([
        ("Table + фильтр area:CLI", "настроено вручную один раз"),
        ("Сохранить как представление", "получает своё имя и вкладку"),
        ("«CLI-задачи»", "открывается одним кликом, без повторной настройки фильтра"),
    ], caption="Сохранённое представление — это настройка, а не копия данных")}

    {comparison_table(
        ["Действие", "Результат"],
        [
            ["Создать представление", "новая вкладка со своим макетом, фильтром и группировкой"],
            ["Дублировать представление", "копия существующей вкладки — удобно как отправная точка для похожей настройки"],
            ["Переименовать представление", "меняет только подпись вкладки"],
            ["Изменить порядок вкладок", "перетаскивание вкладок местами"],
        ],
    )}

    {callout(
        "info",
        "Board и Table для SafeSort — это два сохранённых представления одного Project",
        "Board (статусы по колонкам) и Table (все поля сразу) не дублируют данные — это два "
        "разных способа посмотреть на один и тот же список из 14 задач. Изменение элемента "
        "в одном представлении сразу видно в другом.",
    )}

    {official_sources([("Managing your views", "https://docs.github.com/en/issues/planning-and-tracking-with-projects/customizing-views-in-your-project/managing-your-views")])}

    {summary_box("Коротко", [
        "Представление можно сохранить с именем и своей вкладкой — фильтр и группировка не нужно настраивать заново.",
        "Board и Table — два сохранённых представления одного и того же списка задач, а не отдельные копии данных.",
        "Представления можно дублировать, переименовывать и переставлять местами.",
    ])}
    """
    out = render_page(
        page_title="Управляем представлениями",
        description="Сохранённые представления (views) хранят фильтр, сортировку и группировку под своим именем и вкладкой.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Управление представлениями", "")],
        kicker="Глава 23 · Часть II · Планируем SafeSort на GitHub",
        h1="Управляем представлениями",
        lede="Настроенные фильтр, сортировку и группировку можно сохранить как именованное представление со своей вкладкой.",
        body_html=body,
        sidebar_groups=sidebar("23-proj-12-upravlyaem-predstavleniyami.html"),
        nav=PageNav(prev_href="23-proj-11-filtr-sort-grupp.html", prev_label="Фильтр и группировка", next_href="23-proj-13-avtomatizaciya.html", next_label="Автоматизация и auto-add"),
    )
    write("23-proj-12-upravlyaem-predstavleniyami.html", out)


def build_proj_13() -> None:
    body = f"""
    {stage_tracker(2)}

    <p>Часть переходов между статусами не нужно делать руками — у Project есть встроенные
    автоматизации (built-in workflows), которые реагируют на события в репозитории.</p>

    {comparison_table(
        ["Встроенный workflow", "Что делает"],
        [
            ["Item added to project", "выставляет статус по умолчанию новому элементу"],
            ["Item reopened", "возвращает элемент в заданный статус, если Issue переоткрыт"],
            ["Item closed", "переводит элемент в статус Done, когда Issue или PR закрыт"],
            ["Pull request merged", "переводит элемент в статус Done при слиянии Pull Request"],
            ["Auto-add to project", "автоматически добавляет в Project новые Issues и PR, подходящие под фильтр"],
            ["Auto-archive items", "архивирует элементы, подходящие под фильтр — например, всё в статусе Done"],
        ],
    )}

    {flow_diagram([
        ("Pull Request смержен", "событие в репозитории"),
        ("Workflow \"Pull request merged\"", "встроенная автоматизация Project реагирует"),
        ("Статус элемента → Done", "без ручного перетаскивания карточки"),
    ], caption="Встроенные workflow реагируют на события репозитория и сами меняют статус")}

    <h2>Auto-add — чтобы не добавлять Issues вручную</h2>
    <p>Workflow <strong>Auto-add to project</strong> настраивается фильтром — например,
    «любой новый Issue в репозитории <code class="inline">Cartesian-School/safesort</code>».
    С таким правилом каждый новый Issue сам попадает в Project со статусом по умолчанию,
    и не нужно помнить о ручном шаге «добавить в Project» из более раннего раздела главы.</p>

    {callout(
        "warning",
        "Автоматизация не заменяет решения — она освобождает от рутины",
        "Auto-add избавляет только от механического действия «перетащить Issue в Project». "
        "Решение о том, в каком статусе должна оказаться задача дальше — Ready она уже или "
        "ещё Backlog, — по-прежнему принимает человек.",
    )}

    {official_sources([
        ("Using the built-in automations", "https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations"),
        ("Adding items automatically", "https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/adding-items-automatically"),
    ])}

    {summary_box("Коротко", [
        "Встроенные workflow меняют статус элемента в ответ на событие репозитория — например, слияние Pull Request.",
        "Auto-add to project автоматически добавляет в Project новые Issues и PR, подходящие под настроенный фильтр.",
        "Автоматизация убирает рутинные действия, но не решения о том, в каком статусе должна быть задача.",
    ])}
    """
    out = render_page(
        page_title="Встроенная автоматизация и auto-add",
        description="Built-in workflows меняют статус элемента по событиям репозитория; auto-add сам добавляет новые Issues в Project.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Автоматизация", "")],
        kicker="Глава 23 · Часть II · Планируем SafeSort на GitHub",
        h1="Встроенная автоматизация и auto-add",
        lede="Встроенные workflow сами меняют статус элемента по событиям репозитория и сами добавляют новые Issues в Project.",
        body_html=body,
        sidebar_groups=sidebar("23-proj-13-avtomatizaciya.html"),
        nav=PageNav(prev_href="23-proj-12-upravlyaem-predstavleniyami.html", prev_label="Управление представлениями", next_href="23-proj-14-arhiviruem.html", next_label="Архивируем элементы"),
    )
    write("23-proj-13-avtomatizaciya.html", out)


def build_proj_14() -> None:
    body = f"""
    {stage_tracker(2)}

    <p>Когда задача закрыта и попала в статус Done, оставлять её карточку на Board навсегда
    не обязательно — но и удалять запись из Project тоже не стоит. Для этого есть
    промежуточный шаг: <strong>архивирование</strong>.</p>

    {comparison_table(
        ["Действие", "Что происходит"],
        [
            ["Архивировать", "элемент исчезает из активных представлений, но данные сохраняются и его можно восстановить"],
            ["Восстановить", "элемент возвращается во все представления с теми же полями, что были до архивации"],
            ["Удалить", "элемент удаляется из Project безвозвратно — сам Issue в репозитории при этом не затрагивается"],
        ],
    )}

    {flow_diagram([
        ("14 задач в статусе Done", "Board и Table переполнены завершёнными карточками"),
        ("Архивировать выполненные", "убирает их из активного вида"),
        ("История не теряется", "при необходимости — Restore возвращает элемент как был"),
    ], caption="Архивирование расчищает активное представление, не стирая историю")}

    {callout(
        "info",
        "Архивирование можно автоматизировать",
        "Workflow <strong>Auto-archive items</strong> из предыдущего раздела делает то же "
        "самое по фильтру автоматически — например, архивирует любой элемент, как только его "
        "статус становится Done, чтобы Board оставался читаемым без ручной уборки.",
    )}

    {official_sources([("Archiving items from your project", "https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-items-in-your-project/archiving-items-from-your-project")])}

    {summary_box("Коротко", [
        "Архивирование убирает элемент из активных представлений, но сохраняет его данные и позволяет восстановить.",
        "Удаление, в отличие от архивирования, стирает элемент из Project безвозвратно — сам Issue в репозитории не затрагивается.",
        "Auto-archive items автоматизирует архивирование завершённых задач по фильтру.",
    ])}
    """
    out = render_page(
        page_title="Архивируем и восстанавливаем элементы",
        description="Архивирование убирает завершённые задачи из активного вида, сохраняя данные и возможность восстановить.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Архивирование", "")],
        kicker="Глава 23 · Часть II · Планируем SafeSort на GitHub",
        h1="Архивируем и восстанавливаем элементы",
        lede="Архивирование расчищает активное представление от завершённых задач, не стирая их данные и историю.",
        body_html=body,
        sidebar_groups=sidebar("23-proj-14-arhiviruem.html"),
        nav=PageNav(prev_href="23-proj-13-avtomatizaciya.html", prev_label="Автоматизация", next_href="23-proj-15-shablony.html", next_label="Шаблоны Project"),
    )
    write("23-proj-14-arhiviruem.html", out)


def build_proj_15() -> None:
    body = f"""
    {stage_tracker(2)}

    <p>Организация может пометить готовый Project как <strong>шаблон</strong> — тогда его
    структура (поля, статусы, представления, но не сами задачи, как и при копировании из
    более раннего раздела) появляется в списке заготовок, доступных при создании нового
    Project любому участнику организации.</p>

    {comparison_table(
        ["Copy существующего Project", "Project-шаблон"],
        [
            ["копируется один раз, вручную выбранный Project", "виден в галерее шаблонов при создании любого нового Project"],
            ["нужно знать, какой именно Project копировать", "не нужно искать — шаблон предлагается сразу в интерфейсе"],
            ["доступно для любого Project, на который есть права", "требует, чтобы владелец явно включил флаг «сделать шаблоном»"],
        ],
    )}

    {callout(
        "info",
        "Потенциальный следующий шаг для Cartesian-School, не часть текущей главы",
        "Project «SafeSort — первый релиз» решает конкретную задачу этой главы и сам по себе "
        "шаблоном пока не помечен. Но его структура — статусы Backlog/Ready/In Progress/In "
        "Review/Done и поля Priority/Area — подошла бы и другим проектным главам курса; "
        "пометить его шаблоном для организации Cartesian-School — разумный будущий шаг, "
        "а не то, что нужно SafeSort прямо сейчас.",
    )}

    {official_sources([("Managing project templates in your organization", "https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-your-project/managing-project-templates-in-your-organization")])}

    {summary_box("Коротко", [
        "Project-шаблон появляется в галерее заготовок при создании нового Project — не нужно искать, что копировать.",
        "Шаблоном становится Project, для которого владелец организации явно включил эту настройку.",
        "SafeSort пока не помечен шаблоном — это не нужно для текущей главы, но подходит как будущий шаг курса.",
    ])}
    """
    out = render_page(
        page_title="Шаблоны Project",
        description="Project-шаблон появляется в галерее заготовок организации при создании нового Project.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Шаблоны Project", "")],
        kicker="Глава 23 · Часть II · Планируем SafeSort на GitHub",
        h1="Шаблоны Project",
        lede="Project, помеченный шаблоном, появляется в галерее заготовок организации при создании нового Project.",
        body_html=body,
        sidebar_groups=sidebar("23-proj-15-shablony.html"),
        nav=PageNav(prev_href="23-proj-14-arhiviruem.html", prev_label="Архивирование", next_href="23-proj-16-insights.html", next_label="Insights и графики"),
    )
    write("23-proj-15-shablony.html", out)


def build_proj_16() -> None:
    body = f"""
    {stage_tracker(2)}

    <p>Последний раздел про механику Project — необязательный и более продвинутый:
    <strong>Insights</strong> строит графики прямо из данных Project, без экспорта в
    сторонний инструмент.</p>

    {flow_diagram([
        ("Данные Project", "статус, приоритет, область каждого элемента"),
        ("Insights", "выбирается тип графика и группировка"),
        ("График сохраняется", "остаётся частью Project, обновляется вместе с данными"),
    ], caption="График строится из тех же полей, что уже есть у элементов Project")}

    {comparison_table(
        ["Настройка графика", "Пример для SafeSort"],
        [
            ["Группировка", "по Status — сколько задач в каждой колонке прямо сейчас"],
            ["Фильтр", "например, только Area: CI — сколько задач относится к настройке CI"],
            ["Тип графика", "столбчатая диаграмма, круговая диаграмма и другие — зависит от вопроса"],
        ],
    )}

    {callout(
        "info",
        "Полезно для больших списков задач, необязательно для четырнадцати",
        "Insights раскрывает свою пользу, когда элементов в Project много и вручную посчитать "
        "распределение по статусам или областям неудобно. При 14 задачах SafeSort это "
        "распределение видно и просто посмотрев на Board — Insights здесь скорее демонстрация "
        "возможности, чем необходимость.",
    )}

    {official_sources([
        ("About insights for Projects", "https://docs.github.com/en/issues/planning-and-tracking-with-projects/viewing-insights-from-your-project/about-insights-for-projects"),
        ("Creating charts", "https://docs.github.com/en/issues/planning-and-tracking-with-projects/viewing-insights-from-your-project/creating-charts"),
    ])}

    {summary_box("Коротко", [
        "Insights строит графики прямо из полей Project — без экспорта данных в сторонний инструмент.",
        "График настраивается группировкой, фильтром и типом визуализации.",
        "Польза Insights растёт вместе с количеством задач — на 14 элементах распределение видно и на глаз.",
    ])}
    """
    out = render_page(
        page_title="Insights и графики Project",
        description="Insights строит графики прямо из полей Project — группировка, фильтр, тип визуализации, без экспорта данных.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Insights", "")],
        kicker="Глава 23 · Часть II · Планируем SafeSort на GitHub",
        h1="Insights и графики Project",
        lede="Insights строит графики прямо из полей Project — необязательная, более продвинутая возможность.",
        body_html=body,
        sidebar_groups=sidebar("23-proj-16-insights.html"),
        nav=PageNav(prev_href="23-proj-15-shablony.html", prev_label="Шаблоны Project", next_href="23-proj-17-issue-branch-pr.html", next_label="Первый цикл: Issue → Branch → PR"),
    )
    write("23-proj-16-insights.html", out)


def build_proj_17() -> None:
    body = f"""
    {stage_tracker(2)}

    <p>Issue сформулирован — теперь разберём полный цикл его жизни, от постановки задачи до
    закрытия. Этот цикл повторяется для большинства задач SafeSort, начиная со следующей
    части главы — но не по жёсткому правилу «один Issue — один Pull Request», а так, как
    реально удобно ложится работа.</p>

    {flow_diagram([
        ("Issue", "задача сформулирована, статус Ready"),
        ("Ветка", "статус меняется на In Progress"),
        ("Код и тесты", "работа в изолированной ветке"),
        ("Pull Request", "статус меняется на In Review"),
        ("CI и проверка", "автоматические тесты + самопроверка Files changed"),
        ("Слияние", "Issue закрывается, статус — Done"),
    ], caption="Полный цикл одной задачи — от Issue до Done")}

    {code_block(
        "Терминал",
        "git switch -c feat/directory-scanner\n"
        "# ...пишем код и тесты, коммитим изменения...\n"
        "git push -u origin feat/directory-scanner\n"
        "gh pr create --title \"feat: add directory scanner\" --body \"Closes #1.\"\n",
        lang="text",
    )}

    {callout(
        "tip",
        "Closes #N закрывает Issue автоматически — а один PR может закрыть сразу несколько",
        "Если тело Pull Request содержит фразу вида <code class=\"inline\">Closes #1</code>, "
        "GitHub автоматически закрывает Issue №1 в момент слияния этого PR — вручную закрывать "
        "Issue не нужно. Ничто не мешает написать "
        "<code class=\"inline\">Closes #3, Closes #6</code>, если один PR решает сразу две "
        "тесно связанные задачи — именно так и произошло в репозитории SafeSort с планом "
        "перемещений и обработкой конфликтов имён.",
    )}

    {callout(
        "warning",
        "Не каждый Issue закрывается через PR",
        "Формулировка задачи через Issue не обязывает закрывать её именно Pull Request'ом. "
        "Если работа была сделана попутно, в рамках другой задачи, или не требовала кода "
        "вовсе, Issue можно закрыть вручную — с комментарием, объясняющим, что произошло. "
        "Реальная история проекта важнее искусственно ровной таблицы «N задач — N PR».",
    )}

    <p>Следующая часть главы проходит этот цикл по-настоящему, шаг за шагом, для первой
    реальной задачи — сканера каталогов.</p>

    {official_sources([("About pull requests", "https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests")])}

    {summary_box("Коротко", [
        "Issue → ветка → код и тесты → Pull Request → CI и проверка → слияние — полный цикл одной задачи.",
        "«Closes #N» в описании Pull Request закрывает Issue автоматически при слиянии.",
        "Этот цикл описывает большинство задач SafeSort, но не жёсткое правило — один PR иногда закрывает несколько тесно связанных Issues, а часть задач закрывается без отдельного PR.",
    ])}
    """
    out = render_page(
        page_title="Первый цикл: Issue → Branch → Pull Request",
        description="Полный цикл одной задачи SafeSort — от Issue до слияния Pull Request и автоматического закрытия.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Issue → Branch → PR", "")],
        kicker="Глава 23 · Часть II · Планируем SafeSort на GitHub",
        h1="Первый цикл: Issue → Branch → Pull Request",
        lede="Issue → ветка → код и тесты → Pull Request → CI → слияние — цикл, который повторяется для большинства задач SafeSort, но не по жёсткому правилу «один Issue — один PR».",
        body_html=body,
        sidebar_groups=sidebar("23-proj-17-issue-branch-pr.html"),
        nav=PageNav(prev_href="23-proj-16-insights.html", prev_label="Insights", next_href="23-02-repozitorij.html", next_label="Первый коммит в клонированном репозитории"),
    )
    write("23-proj-17-issue-branch-pr.html", out)


def build_02() -> None:
    body = f"""
    {stage_tracker(3)}

    <p>Репозиторий склонирован (часть I), Issues и GitHub Project разобраны (часть II) — самое
    время заглянуть внутрь каталога, который появился после <code class="inline">git
    clone</code>, и понять, что в нём уже есть.</p>

    {terminal_capture([
        "$ ls -la",
        "CHANGELOG.md",
        ".git/",
        ".github/",
        ".gitignore",
        "LICENSE",
        "pyproject.toml",
        "README.md",
        "src/",
        "tests/",
        "$ cat .gitignore",
        "__pycache__/",
        "*.pyc",
        ".venv/",
        "dist/",
        "build/",
        "*.egg-info/",
        ".pytest_cache/",
        ".safesort/",
    ])}

    {dir_tree(("safesort", "dir", [
        (".git", "dir", []),
        (".github", "dir", []),
        (".gitignore", "file", []),
        ("README.md", "file", []),
        ("LICENSE", "file", []),
        ("CHANGELOG.md", "file", []),
        ("pyproject.toml", "file", []),
        ("src", "dir", []),
        ("tests", "dir", []),
    ]), caption="Настоящий стартовый набор репозитория SafeSort — уже в вашем каталоге после клонирования.")}

    <p>Всё это — первый коммит репозитория, <code class="inline">chore: initial project
    scaffold</code>: рабочее дерево (файлы на диске) плюс <code class="inline">.git</code>
    (история изменений) — вместе их и называют <strong>репозиторием</strong>. Каждый следующий
    раздел этой части добавляет к этому набору содержание — README дополняется, появляется
    Python-пакет внутри <code class="inline">src/</code>, а <code class="inline">
    .gitignore</code> уже сейчас исключает служебные файлы (кеш байткода, виртуальное
    окружение, сборочные каталоги), чтобы они не засоряли историю.</p>

    {summary_box("Коротко", [
        "git clone сразу приносит рабочее дерево — файлы на диске — и .git — историю изменений; вместе это и есть репозиторий.",
        "У SafeSort уже есть стартовый набор: README, LICENSE, CHANGELOG, pyproject.toml, .gitignore — первый коммит репозитория.",
        ".gitignore перечисляет то, что Git не должен отслеживать: временные и сгенерированные файлы.",
    ])}
    """
    out = render_page(
        page_title="Первый коммит в клонированном репозитории",
        description="После git clone в рабочем дереве уже есть README, LICENSE, CHANGELOG, pyproject.toml и .gitignore — стартовый набор репозитория SafeSort.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Репозиторий", "")],
        kicker="Глава 23 · Часть III · Создаём Python-проект",
        h1="Первый коммит в клонированном репозитории",
        lede="После клонирования в рабочем дереве уже есть стартовый набор файлов — первый коммит репозитория SafeSort.",
        body_html=body,
        sidebar_groups=sidebar("23-02-repozitorij.html"),
        nav=PageNav(prev_href="23-proj-17-issue-branch-pr.html", prev_label="Issue → Branch → PR", next_href="23-03-readme.html", next_label="Первый README проекта"),
    )
    write("23-02-repozitorij.html", out)


def build_03() -> None:
    body = f"""
    {stage_tracker(3)}

    {dir_tree(("safesort", "dir", [(".git", "dir", []), ("README.md", "file", [])]), highlight=frozenset({"README.md"}), caption="README.md — один из файлов стартового коммита, увиденного в предыдущем разделе.")}

    <p><strong>README</strong> — первый файл, который видит человек, открывший репозиторий:
    GitHub автоматически показывает его содержимое на главной странице проекта. В клонированном
    репозитории README.md уже существует и уже закоммичен — это часть стартового коммита
    <code class="inline">chore: initial project scaffold</code>, который был показан в предыдущем
    разделе. Сейчас он совсем короткий:</p>

    {code_block(
        "README.md",
        "# SafeSort\n\n"
        "SafeSort — программа для безопасной сортировки файлов по папкам.\n",
    )}

    <p>Раз файл уже отслеживается Git, <code class="inline">git status</code> в чистом рабочем
    дереве ничего не покажет — нечего добавлять и нечего коммитить. Интересное начнётся, когда
    в файл внесут изменения: именно так README и растёт по ходу главы — дополняется разделами,
    а не переписывается с нуля. Добавим первый такой раздел:</p>

    {code_block(
        "README.md",
        "# SafeSort\n\n"
        "SafeSort — программа для безопасной сортировки файлов по папкам.\n\n"
        "## Установка\n\n"
        "pip install -e .\n",
    )}

    {terminal_capture([
        "$ git diff",
        "diff --git a/README.md b/README.md",
        "index f5a2610..d60da39 100644",
        "--- a/README.md",
        "+++ b/README.md",
        "@@ -1,3 +1,7 @@",
        " # SafeSort",
        " ",
        " SafeSort — программа для безопасной сортировки файлов по папкам.",
        "+",
        "+## Установка",
        "+",
        "+pip install -e .",
        "$ git status",
        " M README.md",
    ])}

    <p>git diff показывает построчную разницу перед коммитом, git status — что именно
    изменилось с последнего коммита. По мере того как в проекте появляются установка,
    команды и тесты, в README добавятся такие же короткие разделы Usage и Tests. Полный
    README проекта, уже дополненный: [[icon:file]]
    <a href="../../../projects/python/safesort/README.md">projects/python/safesort/README.md</a>.</p>

    {callout(
        "warning",
        "Без придуманных значков",
        "На странице проекта на GitHub иногда встречаются цветные значки (badge) вида "
        "«tests: passing». Такой значок честен только тогда, когда его действительно "
        "обслуживает настроенная проверка — мы вернёмся к этому, когда подключим GitHub "
        "Actions. Вставлять его раньше значит показывать то, чего на самом деле ещё нет.",
    )}

    {summary_box("Коротко", [
        "README.md — первое, что видит человек, открывший репозиторий на GitHub.",
        "README можно дополнять по мере роста проекта, а не писать целиком с первого раза.",
        "git diff показывает построчные изменения, git status — какие файлы затронуты.",
    ])}
    """
    out = render_page(
        page_title="Первый README проекта",
        description="Пишем README.md постепенно — сначала заголовок и описание, потом раздел за разделом — и коммитим каждый шаг.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("README", "")],
        kicker="Глава 23 · Часть III · Создаём Python-проект",
        h1="Первый README проекта",
        lede="README отвечает на вопросы «что это?» и «как запустить?» ещё до того, как человек откроет код.",
        body_html=body,
        sidebar_groups=sidebar("23-03-readme.html"),
        nav=PageNav(prev_href="23-02-repozitorij.html", prev_label="Репозиторий проекта", next_href="23-04-struktura-paketa.html", next_label="Структура Python-пакета"),
    )
    write("23-03-readme.html", out)


def build_04() -> None:
    body = f"""
    {stage_tracker(3)}

    <p>Хаотичная структура каталогов не мешает программе работать, но мешает её понимать,
    тестировать и устанавливать как пакет. Пока код не написан, зафиксируем только каркас —
    и добавим в него по одному файлу за раз, когда для него появится задача.</p>

    {dir_tree(
        ("safesort", "dir", [
            ("README.md", "file", []),
            ("pyproject.toml", "file", []),
            ("src", "dir", [("safesort", "dir", [("__init__.py", "file", [])])]),
            ("tests", "dir", []),
        ]),
        highlight=frozenset({"pyproject.toml", "src", "safesort", "__init__.py", "tests"}),
        caption="Каркас пакета: pyproject.toml описывает пакет, src/safesort/ — сам код, tests/ — проверки.",
    )}

    <p>Исходный код лежит внутри <code class="inline">src/</code>, а не прямо в корне
    репозитория — это называют <strong>src-раскладкой</strong> (src layout). Без этого
    уровня установленный пакет и каталог исходников совпадали бы, и было бы легко по ошибке
    протестировать не тот код, что реально установлен — например, если забыть переустановить
    пакет после правки файла.</p>

    {dir_tree(
        ("src/safesort", "dir", [
            ("__init__.py", "file", []),
            ("scanner.py", "file", []),
            ("classifier.py", "file", []),
            ("planner.py", "file", []),
            ("executor.py", "file", []),
            ("cli.py", "file", []),
            ("duplicates.py", "file", []),
            ("manifest.py", "file", []),
            ("config.py", "file", []),
        ]),
        faded=frozenset({"scanner.py", "classifier.py", "planner.py", "executor.py", "cli.py", "duplicates.py", "manifest.py", "config.py"}),
        caption="Эти файлы появятся позже, когда для них появится задача — запоминать их сейчас не нужно.",
    )}

    {summary_box("Коротко", [
        "Пакет пока состоит только из README.md, pyproject.toml, src/safesort/__init__.py и tests/.",
        "src-раскладка кладёт исходный код в src/safesort/, а не в корень репозитория, — так тесты "
        "не могут случайно обратиться к неустановленному коду.",
        "Остальные модули появятся по одному, каждый — когда для него будет конкретная задача.",
    ])}
    """
    out = render_page(
        page_title="Планируем структуру Python-пакета",
        description="Строим каркас пакета шаг за шагом: README, pyproject.toml, src/safesort/ — а остальные модули появятся позже, по одному.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Структура пакета", "")],
        kicker="Глава 23 · Часть III · Создаём Python-проект",
        h1="Планируем структуру Python-пакета",
        lede="src-раскладка: пакет лежит в src/safesort/, а не в корне репозитория — и почему это осознанный выбор, а не догма.",
        body_html=body,
        sidebar_groups=sidebar("23-04-struktura-paketa.html"),
        nav=PageNav(prev_href="23-03-readme.html", prev_label="README проекта", next_href="23-05-pyproject-toml.html", next_label="pyproject.toml и установка"),
    )
    write("23-04-struktura-paketa.html", out)


def build_05() -> None:
    body = f"""
    {stage_tracker(3)}

    <p>Python пока видит в <code class="inline">src/safesort/</code> просто папку с кодом —
    не пакет, который можно установить. <code class="inline">pyproject.toml</code> это
    меняет: он описывает пакет для инструментов установки.</p>

    {flow_diagram([
        ("pip / uv", "инструмент установки"),
        ("читает pyproject.toml", "имя, версия, команда"),
        ("устанавливает safesort", "в окружение Python"),
        ("команда safesort", "доступна в терминале"),
    ])}

    {code_block(
        "pyproject.toml",
        '[project]\n'
        'name = "safesort"\n'
        'version = "0.1.0"\n'
        'description = "A safe, non-destructive command-line file organizer."\n'
        'dependencies = []\n\n'
        '[project.scripts]\n'
        'safesort = "safesort.cli:main"\n',
    )}

    <p>Поле <code class="inline">version</code> обязательно идентифицирует текущую версию
    пакета. Пока просто запишем <code class="inline">0.1.0</code> как номер первой учебной
    версии. Как устроены номера версий и почему здесь три числа, разберём ближе к завершению
    проекта.</p>

    <p>Строка <code class="inline">safesort = "safesort.cli:main"</code> говорит инструменту
    установки: после установки создай в окружении команду <code class="inline">safesort</code>,
    которая вызывает функцию <code class="inline">main()</code> из модуля
    <code class="inline">safesort.cli</code> — этого модуля пока не существует, мы напишем его
    на следующей странице.</p>

    {callout(
        "info",
        "dependencies = [] — не пропуск, а факт",
        "У SafeSort нет ни одной обязательной сторонней зависимости: "
        "<code class=\"inline\">pathlib</code>, <code class=\"inline\">argparse</code>, "
        "<code class=\"inline\">hashlib</code>, <code class=\"inline\">shutil</code> и "
        "<code class=\"inline\">json</code> — часть стандартной библиотеки Python.",
    )}

    <h2>Устанавливаем пакет в редактируемом режиме</h2>
    <p><strong>Редактируемая установка</strong> (editable install) связывает окружение
    Python с исходным кодом пакета напрямую: изменения в файлах <code class="inline">
    src/safesort/</code> становятся видны сразу, без повторной установки.</p>
    {code_block("Терминал (окружение активировано)", "pip install -e .[dev]", lang="text")}

    {practice_card(
        "23-07",
        "Практика: разбор аргументов командной строки",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/23-07/index.html",
    )}
    """
    out = render_page(
        page_title="pyproject.toml и установка проекта",
        description="pyproject.toml превращает папку с кодом в устанавливаемый пакет: имя, версия, команда safesort после pip install -e.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("pyproject.toml", "")],
        kicker="Глава 23 · Часть III · Создаём Python-проект",
        h1="pyproject.toml и установка проекта",
        lede="Один файл описывает пакет для инструментов установки — и после pip install -e команда safesort появляется в терминале.",
        body_html=body,
        sidebar_groups=sidebar("23-05-pyproject-toml.html"),
        nav=PageNav(prev_href="23-04-struktura-paketa.html", prev_label="Структура пакета", next_href="23-06-komandnaya-stroka.html", next_label="Командная строка SafeSort"),
    )
    write("23-05-pyproject-toml.html", out)


def build_06() -> None:
    body = f"""
    {stage_tracker(3)}

    {dir_tree(("src/safesort", "dir", [("__init__.py", "file", []), ("cli.py", "file", [])]), highlight=frozenset({"cli.py"}), caption="Первый файл с настоящей логикой: cli.py.")}

    <p>SafeSort будет управляться пятью подкомандами: <code class="inline">scan</code>,
    <code class="inline">plan</code>, <code class="inline">apply</code>,
    <code class="inline">duplicates</code> и <code class="inline">undo</code>. За разбор
    аргументов командной строки отвечает модуль <code class="inline">argparse</code> из
    стандартной библиотеки — он же формирует текст <code class="inline">--help</code>.</p>

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

    <p>Установим пакет и запустим команду — argparse уже формирует текст помощи сам, без
    единой написанной вручную строки:</p>

    {terminal_capture([
        "$ safesort --help",
        "usage: safesort [-h] {scan,plan,apply,duplicates,undo} ...",
        "",
        "SafeSort: a safe, non-destructive file organizer. scan/plan/duplicates never",
        "modify anything; only 'apply' moves files.",
        "",
        "positional arguments:",
        "  {scan,plan,apply,duplicates,undo}",
        "    scan                List files found under ROOT, grouped by category",
        "    plan                Show the moves that would be made under ROOT",
        "    apply               Move files under ROOT into Sorted/<category>/",
        "    duplicates          Report groups of files with identical content",
        "    undo                Undo the most recent 'apply' run",
        "",
        "options:",
        "  -h, --help            show this help message and exit",
    ])}

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
        kicker="Глава 23 · Часть III · Создаём Python-проект",
        h1="Командная строка SafeSort",
        lede="argparse разбирает пять подкоманд SafeSort и связывает каждую с отдельной функцией-обработчиком.",
        body_html=body,
        sidebar_groups=sidebar("23-06-komandnaya-stroka.html"),
        nav=PageNav(prev_href="23-05-pyproject-toml.html", prev_label="pyproject.toml", next_href="23-07-pathlib.html", next_label="pathlib: пути и каталоги"),
    )
    write("23-06-komandnaya-stroka.html", out)


def build_07() -> None:
    body = f"""
    {stage_tracker(4)}

    <p>Всё, что SafeSort делает с файлами, начинается с путей — а модуль
    <code class="inline">pathlib</code> из стандартной библиотеки описывает путь не строкой, а
    объектом <code class="inline">Path</code> с собственными операциями.</p>

    {comparison_table(
        ["Строка", "Path"],
        [
            ['"/home/anna/Downloads/report.pdf"', 'Path("/home/anna/Downloads/report.pdf")'],
            ["ручной разбор через .split('/')", "fajl.parent, fajl.name, fajl.suffix, fajl.stem — готовые атрибуты"],
            ["конкатенация строк для соединения путей", "koren / 'report.pdf' — оператор / собирает путь сам"],
        ],
    )}

    {code_block(
        "pathlib_osnovy.py",
        'from pathlib import Path\n\n'
        'koren = Path("~/Downloads").expanduser()\n'
        'fajl = koren / "otchet.pdf"\n',
    )}

    {terminal_capture([
        ">>> fajl.name",
        "'otchet.pdf'",
        ">>> fajl.suffix",
        "'.pdf'",
        ">>> fajl.stem",
        "'otchet'",
        ">>> fajl.parent",
        "PosixPath('/home/anna/Downloads')",
    ])}

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
        kicker="Глава 23 · Часть IV · Реализуем SafeSort",
        h1="pathlib: работаем с путями и каталогами",
        lede="Path описывает путь объектом со своими операциями — и на нём строится вся модель данных SafeSort.",
        body_html=body,
        sidebar_groups=sidebar("23-07-pathlib.html"),
        nav=PageNav(prev_href="23-06-komandnaya-stroka.html", prev_label="Командная строка", next_href="23-08-skaniruem-katalog.html", next_label="Сканируем каталог"),
    )
    write("23-07-pathlib.html", out)


def build_08() -> None:
    body = f"""
    {stage_tracker(4)}

    <p>Первый шаг SafeSort — обойти каталог и составить список файлов. Функция
    <code class="inline">scan()</code> — одна из трёх строго читающих команд SafeSort: она
    только вызывает <code class="inline">iterdir()</code> и <code class="inline">stat()</code>,
    ни разу не создавая, не перемещая и не удаляя ничего на диске.</p>

    {dir_tree(("Downloads", "dir", [("report.pdf", "file", []), ("cat.jpg", "file", []), ("archive.zip", "file", [])]))}

    {flow_diagram([
        ("Файловая система", "каталог с файлами"),
        ("Сканер", "scan()"),
        ("FileInfo", "путь, размер, расширение"),
    ], caption="Эта цепочка будет расти: следующие страницы добавят в неё новые звенья.")}

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
        "        continue  # символические ссылки пропускаются — см. следующую страницу\n"
        "    if entry.is_dir():\n"
        "        if entry.name in excluded:\n"
        "            continue  # исключённые каталоги пропускаются — см. следующую страницу\n"
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
        "<code class=\"inline\">PermissionError</code>. Реализация "
        "<code class=\"inline\">_scan_dir()</code> перехватывает эту ошибку для каждого "
        "подкаталога отдельно, записывает предупреждение в журнал и продолжает сканировать "
        "остальные каталоги — так один недоступный подкаталог не обрывает весь просмотр "
        "целиком. Позже мы рассмотрим это подробнее вместе с остальными ошибками файловой "
        "системы.",
    )}

    <p>Проверить сканер можно прямо сейчас — реальный вывод:</p>
    {terminal_capture([
        "$ safesort scan ~/Downloads",
        "Files scanned: 9",
        "Documents: 3",
        "Images: 1",
        "Archives: 1",
        "Other: 4",
    ])}

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
        kicker="Глава 23 · Часть IV · Реализуем SafeSort",
        h1="Сканируем каталог",
        lede="scan() строго читает файловую систему — обходит каталог рекурсивно и не меняет ни одного файла.",
        body_html=body,
        sidebar_groups=sidebar("23-08-skaniruem-katalog.html"),
        nav=PageNav(prev_href="23-07-pathlib.html", prev_label="pathlib", next_href="23-09-isklyucheniya.html", next_label="Какие каталоги не сканировать"),
    )
    write("23-08-skaniruem-katalog.html", out)


def build_09() -> None:
    body = f"""
    {stage_tracker(4)}

    {dir_tree(("Downloads", "dir", [
        ("report.pdf — ✓ сканировать", "file", []),
        ("images — ✓ сканировать", "dir", []),
        ("Sorted — ✕ пропустить", "dir", []),
        (".git — ✕ пропустить", "dir", []),
        (".venv — ✕ пропустить", "dir", []),
    ]))}

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
        "изменить через файл настроек, который мы рассмотрим позже. Каталог результата "
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
    следующему элементу каталога — эта строка уже встречалась в <code class="inline">
    _scan_dir()</code> на предыдущей странице.</p>

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
        kicker="Глава 23 · Часть IV · Реализуем SafeSort",
        h1="Какие каталоги не нужно сканировать",
        lede="Каталог результата и служебный каталог SafeSort исключены всегда — а символические ссылки не отслеживаются вовсе.",
        body_html=body,
        sidebar_groups=sidebar("23-09-isklyucheniya.html"),
        nav=PageNav(prev_href="23-08-skaniruem-katalog.html", prev_label="Сканируем каталог", next_href="23-10-klassifikaciya.html", next_label="Определяем категорию файла"),
    )
    write("23-09-isklyucheniya.html", out)


def build_10() -> None:
    body = f"""
    {stage_tracker(4)}

    <p>Каждому найденному файлу нужно назначить категорию — документы, изображения, видео и
    так далее. SafeSort определяет категорию по расширению файла: простое и предсказуемое
    правило, которое покрывает подавляющее большинство практических случаев.</p>

    {flow_diagram([
        ("Файловая система", "каталог с файлами"),
        ("Сканер", "scan()"),
        ("Классификатор", "classify()"),
    ], caption="К цепочке присоединяется новое звено — классификатор.")}

    {comparison_table(
        ["Файл", "Категория"],
        [
            ["report.pdf", "documents"],
            ["photo.jpg", "images"],
            ["backup.zip", "archives"],
            ["unknown.xyz", "other"],
        ],
    )}

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
        kicker="Глава 23 · Часть IV · Реализуем SafeSort",
        h1="Определяем категорию файла",
        lede="Классификация по расширению — практичная эвристика, не доказательство того, что действительно лежит внутри файла.",
        body_html=body,
        sidebar_groups=sidebar("23-10-klassifikaciya.html"),
        nav=PageNav(prev_href="23-09-isklyucheniya.html", prev_label="Исключения", next_href="23-11-plan-dejstvij.html", next_label="От анализа к плану действий"),
    )
    write("23-10-klassifikaciya.html", out)


def build_11() -> None:
    body = f"""
    {stage_tracker(4)}

    <p>У SafeSort есть список найденных файлов и правило классификации — но само по себе это
    ещё не план действий. <strong>План</strong> — список конкретных перемещений: откуда и
    куда переместится каждый файл, если пользователь подтвердит выполнение.</p>

    {flow_diagram([
        ("Файловая система (сейчас)", "не тронута"),
        ("build_plan()", "только читает"),
        ("PLAN", "только описание"),
    ])}

    {safety_boundary(["PLAN — только описание, файловая система не меняется"], ["APPLY — единственная команда, которая меняет диск"])}

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
    с таким именем в месте назначения. Что делать, если да, — тема следующего этапа.</p>
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
        kicker="Глава 23 · Часть IV · Реализуем SafeSort",
        h1="От анализа к плану действий",
        lede="План перемещений — обычные данные: его можно вывести на экран, проверить или отбросить, не тронув ни одного файла.",
        body_html=body,
        sidebar_groups=sidebar("23-11-plan-dejstvij.html"),
        nav=PageNav(prev_href="23-10-klassifikaciya.html", prev_label="Классификация файла", next_href="23-12-predvaritelnyj-prosmotr.html", next_label="Режим предварительного просмотра"),
    )
    write("23-11-plan-dejstvij.html", out)


def build_12() -> None:
    body = f"""
    {stage_tracker(4)}

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

    {terminal_capture([
        "$ safesort plan ~/Downloads",
        "9 move operations planned.",
        "No files have been changed.",
    ])}

    <p>Вторая строка вывода — <code class="inline">"No files have been changed."</code> — не
    формальность. Проверим её честно: посчитаем контрольные суммы файлов до и после
    <code class="inline">plan</code> и сравним.</p>

    {terminal_capture([
        "$ sha256sum Downloads/* > before.txt",
        "$ safesort plan ~/Downloads",
        "9 move operations planned.",
        "No files have been changed.",
        "$ sha256sum Downloads/* > after.txt",
        "$ diff before.txt after.txt",
        "",
    ], cwd="~")}

    <p><code class="inline">diff</code> не вывел ни строки — файлы действительно не
    изменились. Позже такую же проверку сделает автоматический тест, а не ручное сравнение.</p>

    {callout(
        "info",
        "scan, plan и duplicates используют один и тот же список файлов",
        "Три read-only команды SafeSort — <code class=\"inline\">scan</code>, "
        "<code class=\"inline\">plan</code> и <code class=\"inline\">duplicates</code> — "
        "начинаются одинаково: вызывают <code class=\"inline\">scan()</code>, чтобы получить "
        "список файлов. Дальше их пути расходятся: <code class=\"inline\">plan</code> строит "
        "план, <code class=\"inline\">duplicates</code> ищет совпадения по содержимому, а "
        "<code class=\"inline\">scan</code> просто считает файлы по категориям.",
    )}

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
        kicker="Глава 23 · Часть IV · Реализуем SafeSort",
        h1="Режим предварительного просмотра",
        lede="Команда plan — предварительный просмотр без побочных эффектов: тот же план, что и у apply, но без единого изменения диска.",
        body_html=body,
        sidebar_groups=sidebar("23-12-predvaritelnyj-prosmotr.html"),
        nav=PageNav(prev_href="23-11-plan-dejstvij.html", prev_label="План действий", next_href="23-13-peremeshaem-fajly.html", next_label="Безопасно перемещаем файлы"),
    )
    write("23-12-predvaritelnyj-prosmotr.html", out)


def build_13() -> None:
    body = f"""
    {stage_tracker(4)}

    <p>До сих пор ни одна строка кода SafeSort не трогала файловую систему на запись. Модуль
    <code class="inline">executor.py</code> — единственное место во всей программе, где это
    происходит: функция <code class="inline">apply_plan()</code> выполняет уже готовый план и
    только его.</p>

    {flow_diagram([
        ("Файловая система", "каталог с файлами"),
        ("Сканер", "scan()"),
        ("Классификатор", "classify()"),
        ("Executor", "apply_plan()"),
    ], caption="Последнее звено цепочки — единственное, которому разрешено писать на диск.")}

    {before_after_trees(
        ("Downloads", "dir", [("report.pdf", "file", []), ("photo.jpg", "file", []), ("archive.zip", "file", [])]),
        ("Downloads", "dir", [("Sorted", "dir", [
            ("documents", "dir", [("report.pdf", "file", [])]),
            ("images", "dir", [("photo.jpg", "file", [])]),
            ("archives", "dir", [("archive.zip", "file", [])]),
        ])]),
        caption="apply — единственная команда, после которой файлы физически меняют место.",
    )}

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
    перед перемещением, хотя планировщик уже избегал этого конфликта на этапе построения плана.
    Между построением плана и его выполнением на диске мог появиться новый файл — например,
    если пользователь сам что-то туда положил в этот момент. Без повторной проверки
    <code class="inline">shutil.move()</code> в системах на основе POSIX молча перезаписал бы
    такой файл — а SafeSort не перезаписывает файлы молча ни при каких обстоятельствах.</p>

    {terminal_capture([
        "$ safesort apply ~/Downloads",
        "Applied 9 moves.",
        "Manifest written to:",
        ".safesort/history/20260824T085400685280.json",
    ])}

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
        kicker="Глава 23 · Часть IV · Реализуем SafeSort",
        h1="Безопасно перемещаем файлы",
        lede="Одна функция во всей программе имеет право перемещать файлы — и делает это только после повторной проверки на конфликт.",
        body_html=body,
        sidebar_groups=sidebar("23-13-peremeshaem-fajly.html"),
        nav=PageNav(prev_href="23-12-predvaritelnyj-prosmotr.html", prev_label="Предварительный просмотр", next_href="23-14-imya-zanyato.html", next_label="Если имя уже занято"),
    )
    write("23-13-peremeshaem-fajly.html", out)


def build_14() -> None:
    body = f"""
    {stage_tracker(4)}

    <p>Два файла с одинаковым именем могут попасть в одну и ту же категорию — например, два
    разных <code class="inline">notes.txt</code> из разных подкаталогов исходного каталога.
    Если бы SafeSort просто перемещал файл поверх существующего, второй файл исчез бы молча —
    в каталоге назначения осталось бы одно и то же имя <code class="inline">notes.txt</code>,
    но с содержимым только одного из двух файлов, без единого предупреждения об этом.</p>

    {terminal_capture([
        "$ safesort apply ~/Downloads",
        "Applied 1 moves.",
    ])}

    {dir_tree(("Sorted/documents", "dir", [("notes.txt", "file", []), ("notes (1).txt", "file", [])]), highlight=frozenset({"notes (1).txt"}), caption="Файл, который уже был в Sorted/documents/, остался нетронутым; новый получил свободное имя.")}

    <p>SafeSort никогда не решает конфликт имён перезаписью: вместо этого он находит свободное
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
        kicker="Глава 23 · Часть IV · Реализуем SafeSort",
        h1="Что делать, если имя уже занято",
        lede="Ни на диске, ни внутри одного плана два файла никогда не получат одинаковое имя назначения.",
        body_html=body,
        sidebar_groups=sidebar("23-14-imya-zanyato.html"),
        nav=PageNav(prev_href="23-13-peremeshaem-fajly.html", prev_label="Перемещение файлов", next_href="23-15-zhurnal-operacij.html", next_label="Журнал выполненных операций"),
    )
    write("23-14-imya-zanyato.html", out)


def build_15() -> None:
    body = f"""
    {stage_tracker(4)}

    <p>Каждый успешный вызов <code class="inline">apply</code> оставляет след — файл-манифест
    в формате JSON, который описывает, что именно было сделано. Без этого журнала команда
    <code class="inline">undo</code>, о которой пойдёт речь на следующей странице, не знала бы,
    что именно нужно отменить.</p>

    {flow_diagram([
        ("apply", "перемещает файлы"),
        ("список перемещений", "source → destination"),
        ("manifest.json", "записан на диск"),
    ], caption="apply не только двигает файлы — он записывает, что именно сделал.")}

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
        kicker="Глава 23 · Часть IV · Реализуем SafeSort",
        h1="Журнал выполненных операций",
        lede="Каждый apply записывает JSON-манифест того, что действительно произошло — это единственный источник данных для отмены.",
        body_html=body,
        sidebar_groups=sidebar("23-15-zhurnal-operacij.html"),
        nav=PageNav(prev_href="23-14-imya-zanyato.html", prev_label="Конфликт имён", next_href="23-16-otmena-operacii.html", next_label="Отмена последней операции"),
    )
    write("23-15-zhurnal-operacij.html", out)


def build_16() -> None:
    body = f"""
    {stage_tracker(4)}

    <p>Команда <code class="inline">undo</code> находит последний манифест, читает список
    выполненных перемещений и возвращает файлы туда, откуда они были взяты. Здесь действует
    то же правило, что и во всей программе: <strong>ничего не перезаписывать молча</strong>.</p>

    {flow_diagram([
        ("manifest.json", "последняя запись"),
        ("список перемещений", "destination → source"),
        ("undo", "восстанавливает файлы"),
    ], caption="Тот же путь, что и у apply, но в обратную сторону.")}

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
        "перемещения, которые не удались во время <code class=\"inline\">apply</code>, "
        "никогда не касались диска, и отменять для них нечего.",
    )}

    <p>Сначала — обычный успешный откат:</p>
    {terminal_capture([
        "$ safesort undo ~/Downloads",
        "Restored 9 moves.",
    ])}

    <h2>Конфликт при отмене — реальный сценарий</h2>
    <p>Что произойдёт, если запустить <code class="inline">undo</code> ещё раз, когда файлы
    уже на исходных местах? Простое перемещение назад стёрло бы то, что там уже есть. Вместо
    этого SafeSort проверяет исходное место <em>перед</em> восстановлением каждого файла и,
    если там уже что-то есть, отказывается восстанавливать именно этот файл:</p>
    {terminal_capture([
        "$ safesort undo ~/Downloads",
        "ERROR: Refusing to undo Sorted/other/bigfile_b.dat -> bigfile_b.dat:",
        "  a file already exists at the original location: bigfile_b.dat",
        "ERROR: Refusing to undo Sorted/documents/notes.txt -> notes.txt:",
        "  a file already exists at the original location: notes.txt",
        "… (ещё 7 таких строк)",
        "Restored 0 moves.",
        "9 moves could not be restored:",
        "  Sorted/other/bigfile_b.dat -> bigfile_b.dat: a file already exists at the original location",
        "  … (ещё 8 строк)",
    ])}

    <p>Отказ — а не тихая перезапись. Каждый конфликт обрабатывается независимо: файлы без
    конфликта восстановились бы, даже если часть списка отказала.</p>

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
        kicker="Глава 23 · Часть IV · Реализуем SafeSort",
        h1="Отмена последней операции",
        lede="undo восстанавливает файлы из журнала — и отказывается затирать то, что успело появиться на исходном месте.",
        body_html=body,
        sidebar_groups=sidebar("23-16-otmena-operacii.html"),
        nav=PageNav(prev_href="23-15-zhurnal-operacij.html", prev_label="Журнал операций", next_href="23-17-poisk-dublikatov.html", next_label="Поиск одинаковых файлов"),
    )
    write("23-16-otmena-operacii.html", out)


def build_17() -> None:
    body = f"""
    {stage_tracker(4)}

    <p>Второй крупный компонент SafeSort — поиск файлов с одинаковым содержимым. Задача
    выглядит просто: если у двух файлов одинаковые байты, они дубликаты. Наивное решение —
    сравнить содержимое каждого файла с содержимым каждого другого — работает, но для тысяч
    файлов означает чтение каждого файла снова и снова.</p>

    {comparison_table(
        ["Размер", "Файлы"],
        [
            ["100 KB", "a.jpg, b.jpg"],
            ["240 KB", "report.pdf (один файл — дальше не идёт)"],
            ["3 MB", "video.mp4, video-copy.mp4"],
        ],
    )}

    <p>Дальше в проверку идут только группы из двух и более файлов — одиночный размер сразу
    отбрасывается, дублировать ему нечего.</p>

    {flow_diagram(
        [
            ("Все файлы", "список FileInfo от сканера"),
            ("Группировка по size", "файлы с уникальным размером сразу отбрасываются"),
            ("Хеш SHA-256", "только для файлов внутри одной группы размера"),
            ("Группировка по (size, digest)", "совпадение — кандидат в дубликаты"),
            ("Байтовое подтверждение", "кандидат становится подтверждённым дубликатом"),
        ],
        caption="Поэтапный поиск дубликатов: каждый следующий, более дорогой шаг применяется только к тому, что прошло предыдущий",
    )}

    {callout(
        "tip",
        "Файл с уникальным размером не может быть дубликатом",
        "Если размер файла не совпадает ни с одним другим файлом в просканированном каталоге, "
        "у него точно нет дубликата — и вычислять его хеш незачем. Эта проверка почти "
        "бесплатна (размер уже известен из <code class=\"inline\">FileInfo</code>), а "
        "экономит она ровно то, что дороже всего — чтение и хеширование содержимого файлов.",
    )}

    <p>Дальше — сама функция хеширования, а затем то, как результаты хеширования
    группируются в готовые группы дубликатов и проходят последнее, байтовое подтверждение.</p>

    {summary_box("Коротко", [
        "Поиск дубликатов идёт в четыре этапа: по размеру, по хешу, по паре (размер, хеш), затем байтовое подтверждение.",
        "Хеш вычисляется только для файлов, у которых уже нашёлся хотя бы один файл того же размера.",
        "duplicates() — read-only команда: она только сообщает о найденных группах, ничего не удаляя.",
    ])}
    """
    out = render_page(
        page_title="Поиск одинаковых файлов",
        description="Поэтапный поиск дубликатов: сначала по размеру, затем хеширование только внутри групп совпадающего размера.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Поиск дубликатов", "")],
        kicker="Глава 23 · Часть IV · Реализуем SafeSort",
        h1="Поиск одинаковых файлов",
        lede="Дорогое хеширование содержимого делается только там, где оно действительно может изменить ответ — после отбора по размеру.",
        body_html=body,
        sidebar_groups=sidebar("23-17-poisk-dublikatov.html"),
        nav=PageNav(prev_href="23-16-otmena-operacii.html", prev_label="Отмена операции", next_href="23-18-sha256.html", next_label="SHA-256 и хеш файла"),
    )
    write("23-17-poisk-dublikatov.html", out)


def build_18() -> None:
    body = f"""
    {stage_tracker(4)}

    {flow_diagram([
        ("Байты файла", "содержимое целиком"),
        ("SHA-256", "hashlib.sha256()"),
        ("64 hex-символа", "дайджест"),
    ])}

    <p><strong>Хеш-функция</strong> превращает содержимое файла произвольного размера в
    строку фиксированной длины — <strong>дайджест</strong>. SafeSort использует
    <strong>SHA-256</strong> из модуля <code class="inline">hashlib</code>: одинаковые байты
    всегда дают одинаковый дайджест, а разные дайджесты гарантированно значат разное
    содержимое. Совпадающий дайджест — сильный сигнал, но не абсолютное доказательство:
    у SHA-256 в принципе есть коллизии, астрономически маловероятные, но не равные нулю.
    Поскольку SafeSort перемещает настоящие файлы пользователя, он не останавливается на
    совпадении дайджеста — следующая страница показывает последний шаг, который превращает
    совпадение хеша в подтверждённый дубликат.</p>

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
        kicker="Глава 23 · Часть IV · Реализуем SafeSort",
        h1="SHA-256 и хеш содержимого файла",
        lede="Одинаковое содержимое всегда даёт одинаковый дайджест SHA-256 — а поблочное чтение не требует держать в памяти весь файл разом.",
        body_html=body,
        sidebar_groups=sidebar("23-18-sha256.html"),
        nav=PageNav(prev_href="23-17-poisk-dublikatov.html", prev_label="Поиск дубликатов", next_href="23-19-gruppy-dublikatov.html", next_label="Находим группы дубликатов"),
    )
    write("23-18-sha256.html", out)


def build_19() -> None:
    body = f"""
    {stage_tracker(4)}

    <p>С хеш-функцией с предыдущей страницы поиск дубликатов группирует файлы сначала по
    размеру, затем по дайджесту SHA-256 — и на этом почти любая реализация бы остановилась.
    SafeSort делает ещё один шаг: прежде чем считать группу подтверждённой, он сравнивает
    файлы внутри неё побайтово.</p>

    {code_block(
        "src/safesort/duplicates.py",
        'def files_equal(path_a: Path, path_b: Path, chunk_size: int = DEFAULT_CHUNK_SIZE) -> bool:\n'
        '    """Финальное подтверждение — совпадающий дайджест не гарантия."""\n'
        '    with path_a.open("rb") as file_a, path_b.open("rb") as file_b:\n'
        '        while True:\n'
        '            chunk_a = file_a.read(chunk_size)\n'
        '            chunk_b = file_b.read(chunk_size)\n'
        '            if chunk_a != chunk_b:\n'
        '                return False\n'
        '            if not chunk_a:\n'
        '                return True\n\n'
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
        '            if len(matched) < 2:\n'
        '                continue\n'
        '            confirmed = [matched[0]]\n'
        '            for candidate in matched[1:]:\n'
        '                if files_equal(matched[0].path, candidate.path):\n'
        '                    confirmed.append(candidate)\n'
        '            if len(confirmed) >= 2:\n'
        '                groups.append(DuplicateGroup(size=size, digest=digest, files=tuple(confirmed)))\n'
        '    return groups\n',
    )}

    {callout(
        "info",
        "files_equal() — та же идея, что и sha256_file(): читать блоками",
        "Побайтовая сверка читает оба файла кусками по мегабайту и сравнивает кусок с куском, "
        "а не загружает файлы в память целиком — то же соображение, что и на предыдущей "
        "странице про <code class=\"inline\">sha256_file()</code>. Как только один из кусков "
        "не совпал, сравнение сразу останавливается: незачем дочитывать оставшуюся часть "
        "заведомо разных файлов.",
    )}

    {callout(
        "info",
        "Пустые файлы — тоже дубликаты друг друга",
        "Два файла нулевого размера побайтово идентичны: у обоих попросту нет байтов. "
        "<code class=\"inline\">find_duplicates()</code> не делает для этого случая никакого "
        "исключения — они естественно попадают в одну группу по размеру "
        "(<code class=\"inline\">0</code>) и в одну группу по дайджесту пустого содержимого. "
        "Позже мы проверим это отдельным тестом.",
    )}

    <p>Реальный вывод команды <code class="inline">duplicates</code> для каталога с тремя
    парами совпадений:</p>
    {terminal_capture([
        "$ safesort duplicates ~/Downloads",
        "Found 3 duplicate group(s):",
        "Group 1: 2 files, 2097289 bytes each, sha256=5e5aab7a...",
        "  Downloads/bigfile_b.dat",
        "  Downloads/bigfile_a.dat",
        "Group 2: 2 files, 0 bytes each, sha256=e3b0c442...",
        "  Downloads/empty_b.bin",
        "  Downloads/empty_a.bin",
        "Group 3: 2 files, 28 bytes each, sha256=0833b7c4...",
        "  Downloads/copy_of_notes.txt",
        "  Downloads/notes.txt",
    ])}

    {callout(
        "warning",
        "duplicates только сообщает — не удаляет",
        "Первая версия программы не удаляет ни один файл из найденной группы, и в коде "
        "<code class=\"inline\">find_duplicates()</code> нет ни одного вызова, который "
        "удаляет файлы — даже отключённого или закомментированного. Автоматическое удаление "
        "дубликатов сознательно вынесено за рамки первой версии: решение о том, какой из "
        "одинаковых файлов оставить, требует контекста, которого у программы нет.",
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
        kicker="Глава 23 · Часть IV · Реализуем SafeSort",
        h1="Находим группы дубликатов",
        lede="Одна функция превращает список файлов в группы дубликатов — и никогда не удаляет ни одного файла сама.",
        body_html=body,
        sidebar_groups=sidebar("23-19-gruppy-dublikatov.html"),
        nav=PageNav(prev_href="23-18-sha256.html", prev_label="SHA-256", next_href="23-20-oshibki-fajlovoj-sistemy.html", next_label="Ошибки файловой системы"),
    )
    write("23-19-gruppy-dublikatov.html", out)


def build_20() -> None:
    body = f"""
    {stage_tracker(4)}

    <p>Реальная файловая система непредсказуема: файл может исчезнуть между сканированием и
    чтением, доступ к каталогу может быть запрещён, диск может оказаться неисправен. Python
    сообщает о таких ситуациях через конкретные классы исключений, и SafeSort ловит именно
    их — не всё подряд.</p>

    {decision_map([
        ("Файл пропал между шагами", "FileNotFoundError"),
        ("Недостаточно прав доступа", "PermissionError"),
        ("Другая ошибка файловой системы", "OSError"),
    ], title="Что произошло → какое исключение")}

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
    (что это за журнал — на следующей странице) и возвращает управление — сканирование
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
        kicker="Глава 23 · Часть IV · Реализуем SafeSort",
        h1="Обрабатываем ошибки файловой системы",
        lede="Конкретные исключения вместо except Exception: программа не скрывает реальные ошибки, а обрабатывает только ожидаемые.",
        body_html=body,
        sidebar_groups=sidebar("23-20-oshibki-fajlovoj-sistemy.html"),
        nav=PageNav(prev_href="23-19-gruppy-dublikatov.html", prev_label="Группы дубликатов", next_href="23-21-logging.html", next_label="Журнал работы программы"),
    )
    write("23-20-oshibki-fajlovoj-sistemy.html", out)


def build_21() -> None:
    body = f"""
    {stage_tracker(4)}

    <p>В коде SafeSort уже несколько раз встречался вызов <code class="inline">logger.warning
    (...)</code>. Это не то же самое, что вывод на экран через <code class="inline">print()
    </code>: у программы есть два разных канала сообщений с разным назначением.</p>

    {flow_diagram([
        ("Программа", "выполняет команду"),
        ("Вывод для пользователя", "print() — итог команды"),
    ])}
    {flow_diagram([
        ("Программа", "выполняет команду"),
        ("Журнал (logging)", "диагностика: что пропущено, что не удалось"),
    ])}

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
        kicker="Глава 23 · Часть IV · Реализуем SafeSort",
        h1="Добавляем журнал работы программы",
        lede="Итог для пользователя печатается напрямую; диагностика идёт отдельным каналом — через модуль logging.",
        body_html=body,
        sidebar_groups=sidebar("23-21-logging.html"),
        nav=PageNav(prev_href="23-20-oshibki-fajlovoj-sistemy.html", prev_label="Ошибки файловой системы", next_href="23-22-nastrojki-proekta.html", next_label="Настройки проекта"),
    )
    write("23-21-logging.html", out)


def build_22() -> None:
    body = f"""
    {stage_tracker(4)}

    <p>Категории по умолчанию и каталог результата подходят для большинства случаев, но
    иногда их стоит настроить — например, разложенные файлы должны попадать не в
    <code class="inline">Sorted/</code>, а в каталог с другим именем. Без файла настроек
    SafeSort использует встроенные значения:</p>

    {code_block(
        "Встроенные значения по умолчанию (нигде в файле не записаны — это поведение программы)",
        'destination = "Sorted"\n'
        'exclude = [".git", ".venv"]\n',
        lang="toml",
    )}

    <p>Чтобы изменить их, SafeSort ищет необязательный файл
    <code class="inline">safesort.toml</code> прямо в корне сканируемого каталога:</p>

    {decision_map([
        ("safesort.toml есть в корне каталога", "читаем и применяем настройки"),
        ("safesort.toml отсутствует", "используем встроенные значения по умолчанию"),
    ], title="Что произойдёт при запуске")}

    {code_block(
        "safesort.toml — переопределяет имя каталога результата и добавляет категорию",
        'destination = "Organized"\n'
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
        kicker="Глава 23 · Часть IV · Реализуем SafeSort",
        h1="Настройки проекта",
        lede="Файл настроек необязателен: без него в силу вступают встроенные значения по умолчанию, а с ним можно переопределить часть поведения.",
        body_html=body,
        sidebar_groups=sidebar("23-22-nastrojki-proekta.html"),
        nav=PageNav(prev_href="23-21-logging.html", prev_label="Журнал программы", next_href="23-23-pervye-testy.html", next_label="Первые автоматические тесты"),
    )
    write("23-22-nastrojki-proekta.html", out)


def build_23() -> None:
    body = f"""
    {stage_tracker(5)}

    <p>Представим: кто-то случайно сломал классификатор — расширение <code class="inline">
    .PDF</code> в верхнем регистре перестало определяться как документ. Как об этом узнать, не
    проверяя вручную каждый раз?</p>

    {terminal_capture([
        "$ pytest tests/test_classifier.py -q",
        "........F.",
        "=================================== FAILURES ===================================",
        "______________________ test_classify_is_case_insensitive _______________________",
        "",
        '    assert classify(".PDF", DEFAULT_EXTENSIONS) == "documents"',
        "E   AssertionError: assert 'other' == 'documents'",
        "",
        "1 failed, 9 passed in 0.04s",
    ], caption="RED — тест обнаружил поломку раньше человека.")}

    <p>Возвращаем нормализацию регистра на место — и тот же тест подтверждает исправление:</p>

    {terminal_capture([
        "$ pytest tests/test_classifier.py -q",
        "..........",
        "10 passed in 0.02s",
    ], caption="GREEN — поведение снова соответствует ожиданию.")}

    <p>Код, который сам проверяет другой код и сообщает, если поведение изменилось незаметно
    для человека, называют <strong>автоматическим тестом</strong>. В Python для этого чаще
    всего используют <code class="inline">pytest</code>.</p>

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

    {safety_boundary(
        ["ВРЕМЕННЫЙ КАТАЛОГ /tmp/pytest-.../ — создаём, перемещаем, удаляем — удаляется автоматически"],
        ["РЕАЛЬНЫЕ ФАЙЛЫ ПОЛЬЗОВАТЕЛЯ ~/Downloads — здесь тесты не выполняются никогда"],
    )}

    {code_block(
        "tests/test_classifier.py",
        'from safesort.classifier import classify\n'
        'from safesort.config import DEFAULT_EXTENSIONS\n\n'
        'def test_classify_known_extension():\n'
        '    # Arrange: расширение и правило классификации уже готовы, ничего создавать не нужно\n'
        '    # Act\n'
        '    rezultat = classify(".pdf", DEFAULT_EXTENSIONS)\n'
        '    # Assert\n'
        '    assert rezultat == "documents"\n',
    )}

    <p>Три части — <strong>Arrange</strong> (подготовить), <strong>Act</strong> (вызвать),
    <strong>Assert</strong> (проверить) — повторяются почти в каждом тесте SafeSort. Функция
    <code class="inline">classify()</code> — хороший первый тест не случайно: она чистая, не
    трогает файловую систему и не зависит ни от чего внешнего. Следующая страница берётся за
    более сложные тесты — те, что действительно создают файлы во временном каталоге.</p>

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
        kicker="Глава 23 · Часть V · Проверяем и автоматизируем",
        h1="Пишем первые автоматические тесты",
        lede="Тесты SafeSort работают только во временном каталоге pytest — ни один из них не трогает настоящие пользовательские файлы.",
        body_html=body,
        sidebar_groups=sidebar("23-23-pervye-testy.html"),
        nav=PageNav(prev_href="23-22-nastrojki-proekta.html", prev_label="Настройки проекта", next_href="23-24-testy-skanirovaniya.html", next_label="Тесты сканирования"),
    )
    write("23-23-pervye-testy.html", out)


def build_24() -> None:
    body = f"""
    {stage_tracker(5)}

    {flow_diagram([("Arrange", "подготовить файлы"), ("Act", "вызвать scan()"), ("Assert", "проверить результат")])}

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

    <p>Второй тест выше — прямая проверка требования, которое мы обсуждали раньше: каталог
    результата никогда не сканируется повторно. Без такого теста регресс (случайный возврат старой,
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
        kicker="Глава 23 · Часть V · Проверяем и автоматизируем",
        h1="Проверяем сканирование и классификацию",
        lede="Тест на пустом каталоге и тест на повторное сканирование Sorted/ — простые случаи, которые чаще всего ломаются незаметно.",
        body_html=body,
        sidebar_groups=sidebar("23-24-testy-skanirovaniya.html"),
        nav=PageNav(prev_href="23-23-pervye-testy.html", prev_label="Первые тесты", next_href="23-25-testy-peremeshheniya.html", next_label="Тесты перемещения и отмены"),
    )
    write("23-24-testy-skanirovaniya.html", out)


def build_25() -> None:
    body = f"""
    {stage_tracker(5)}

    {flow_diagram([("Arrange", "создать файл во временном каталоге"), ("Act", "apply_plan() / undo()"), ("Assert", "файл на новом или исходном месте")])}

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
        kicker="Глава 23 · Часть V · Проверяем и автоматизируем",
        h1="Проверяем перемещение и отмену",
        lede="Каждый шаг — перемещение, отмену, конфликт при отмене — проверяет отдельный тест, а не один общий сценарий.",
        body_html=body,
        sidebar_groups=sidebar("23-25-testy-peremeshheniya.html"),
        nav=PageNav(prev_href="23-24-testy-skanirovaniya.html", prev_label="Тесты сканирования", next_href="23-26-testy-dublikatov.html", next_label="Тесты поиска дубликатов"),
    )
    write("23-25-testy-peremeshheniya.html", out)


def build_26() -> None:
    body = f"""
    {stage_tracker(5)}

    {flow_diagram([("Arrange", "два файла с одинаковым содержимым"), ("Act", "find_duplicates()"), ("Assert", "одна группа из двух файлов")])}

    <p>Тесты для <code class="inline">find_duplicates()</code> проверяют не только «типичный»
    случай двух одинаковых файлов, но и два крайних случая, которые легко упустить: файлы
    нулевого размера и файл заметно больше одного блока чтения.</p>

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
        kicker="Глава 23 · Часть V · Проверяем и автоматизируем",
        h1="Проверяем поиск дубликатов",
        lede="Два крайних случая — пустые файлы и файл в несколько мегабайт — проверяют то, что типичный тест на паре файлов не заметит.",
        body_html=body,
        sidebar_groups=sidebar("23-26-testy-dublikatov.html"),
        nav=PageNav(prev_href="23-25-testy-peremeshheniya.html", prev_label="Тесты перемещения", next_href="23-27-testy-cli.html", next_label="Тесты интерфейса командной строки"),
    )
    write("23-26-testy-dublikatov.html", out)


def build_27() -> None:
    body = f"""
    {stage_tracker(5)}

    {flow_diagram([("Arrange", "файл во временном каталоге"), ("Act", 'main(["scan", ...])'), ("Assert", "код возврата и вывод capsys")])}

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
        kicker="Глава 23 · Часть V · Проверяем и автоматизируем",
        h1="Проверяем интерфейс командной строки",
        lede="capsys перехватывает то, что программа напечатала, — и тесты проверяют это как обычную строку, без реального терминала.",
        body_html=body,
        sidebar_groups=sidebar("23-27-testy-cli.html"),
        nav=PageNav(prev_href="23-26-testy-dublikatov.html", prev_label="Тесты дубликатов", next_href="23-28-git-kommit.html", next_label="Git: от изменения к коммиту"),
    )
    write("23-27-testy-cli.html", out)


def build_28() -> None:
    body = f"""
    {stage_tracker(5)}

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
            ["docs: document safesort.toml options", "final-final"],
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
        kicker="Глава 23 · Часть V · Проверяем и автоматизируем",
        h1="Git: от рабочего изменения к коммиту",
        lede="git add переносит изменение в индекс, git commit фиксирует его в истории — а хороший коммит описывает одно законченное изменение.",
        body_html=body,
        sidebar_groups=sidebar("23-28-git-kommit.html"),
        nav=PageNav(prev_href="23-27-testy-cli.html", prev_label="Тесты интерфейса", next_href="23-29-github-pr.html", next_label="GitHub: Issue, ветка и Pull Request"),
    )
    write("23-28-git-kommit.html", out)


GITHUB_WORKFLOW_STEPS = [
    ("Issue", "описание задачи или найденной проблемы"),
    ("Ветка", "изолированное место для изменений по этой задаче"),
    ("Коммиты", "сохранённые шаги работы в этой ветке"),
    ("Push", "ветка публикуется на GitHub"),
    ("Pull Request", "предложение перенести изменения ветки в main"),
    ("Проверка (CI)", "автоматические тесты запускаются на GitHub"),
    ("Слияние", "код объединён с основной веткой"),
]


def build_29() -> None:
    body = f"""
    {stage_tracker(5)}

    <p>История коммитов, сделанных до этого момента, пока существует только в локальном репозитории — на
    одном компьютере. <code class="inline">git push</code> публикует её на GitHub — там вокруг
    этой истории есть рабочий процесс для совместной разработки: Issue, ветка, Pull Request.</p>

    <div style="display:flex;align-items:center;gap:8px;font-family:Sora,sans-serif;font-weight:700;
      font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:#5B24F9;margin:8px 0 16px">
      {github_mark()}<span>Этот этап целиком происходит на GitHub</span>
    </div>

    {flow_diagram(
        GITHUB_WORKFLOW_STEPS,
        caption="Путь одного изменения на GitHub — на этой странице первые три шага и Pull Request, дальше про проверку и слияние отдельно",
    )}

    <h2>Issue — формулировка задачи до кода</h2>
    <p><strong>Issue</strong> — запись на GitHub, описывающая задачу, найденную
    проблему или предложение. Прежде чем писать код, полезно кратко сформулировать, что именно
    нужно сделать и как проверить, что это сделано — так выглядит настоящая форма создания
    Issue (ничего не отправлено, это просто интерфейс формы):</p>

    {image_figure(
        f"{IMG}/github-new-issue.jpg",
        "Форма создания нового Issue на GitHub: поле заголовка, поле описания, боковая панель Assignees/Labels/Type",
        "Реальная форма Issue на GitHub — заголовок и описание задачи, до того как написана хоть одна строка кода.",
        size="wide",
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
    автоматически: он открывает изменения для просмотра, автоматических проверок (о них —
    на следующей странице) и обсуждения, прежде чем код попадёт в основную ветку.</p>

    {image_figure(
        f"{IMG}/safesort-pr-files-changed.jpg",
        "Вкладка Files changed настоящего Pull Request репозитория Cartesian-School/safesort: добавленный файл duplicates.py, статус Merged",
        "Настоящий Pull Request репозитория SafeSort — «Add duplicate detection with byte-level confirmation», закрывший Issue №9.",
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
        kicker="Глава 23 · Часть V · Проверяем и автоматизируем",
        h1="GitHub: Issue, ветка и Pull Request",
        lede="От формулировки задачи в Issue до предложения изменений через Pull Request — путь одного изменения на GitHub.",
        body_html=body,
        sidebar_groups=sidebar("23-29-github-pr.html"),
        nav=PageNav(prev_href="23-28-git-kommit.html", prev_label="Git и коммит", next_href="23-30-github-actions.html", next_label="GitHub Actions"),
    )
    write("23-29-github-pr.html", out)


def build_30() -> None:
    body = f"""
    {stage_tracker(5)}

    <div style="display:flex;align-items:center;gap:8px;font-family:Sora,sans-serif;font-weight:700;
      font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:#5B24F9;margin:8px 0 16px">
      {github_mark()}<span>Проверка (CI) — четвёртый шаг из диаграммы на прошлой странице</span>
    </div>

    <p>Проверять тесты вручную перед каждым Pull Request легко забыть. <strong>GitHub
    Actions</strong> — сервис, который автоматически выполняет заданные действия при
    определённых событиях в репозитории, например при каждом пуше или открытии Pull Request.
    Для SafeSort такое действие — запуск тестов.</p>

    {flow_diagram(
        [
            ("push / pull_request", "событие в репозитории"),
            ("workflow YAML", "GitHub читает файл-инструкцию"),
            ("Раннер GitHub", "виртуальная машина поднимается и получает код"),
            ("pytest", "тесты запускаются внутри раннера"),
            ("✓ / ✗", "результат виден в Pull Request"),
        ],
        caption="От события в репозитории до зелёной или красной галочки в Pull Request",
    )}

    {image_figure(
        f"{IMG}/safesort-actions-runs.jpg",
        "Список запусков GitHub Actions репозитория Cartesian-School/safesort: 19 реальных запусков, включая один красный (намеренно сломанный тест) и следующий за ним зелёный",
        "Настоящая история запусков CI репозитория SafeSort — 19 запусков, вплоть до одного специально сломанного и тут же исправленного (раздел ниже).",
        size="wide",
    )}

    <p>Вот тот самый файл-инструкция, который GitHub читает перед каждым запуском:</p>
    {code_block(
        ".github/workflows/tests.yml",
        "name: tests\n\n"
        "on:\n"
        "  push:\n"
        '    branches: ["main"]\n'
        "  pull_request:\n\n"
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
        '        run: pip install -e ".[dev]"\n\n'
        "      - name: Run tests\n"
        "        run: pytest tests/\n",
        lang="yaml",
    )}

    {callout(
        "tip",
        "on: без ограничений — потому что весь репозиторий и есть SafeSort",
        "Здесь нет ключа <code class=\"inline\">paths</code>, ограничивающего запуск по "
        "изменённым файлам: в отдельном репозитории <code class=\"inline\">safesort</code> "
        "любой пуш или Pull Request так или иначе касается самого пакета. Такое ограничение "
        "нужно только в общем репозитории курса, где SafeSort — лишь один из многих "
        "подкаталогов и незачем перезапускать его тесты из-за изменений где-то ещё.",
    )}

    <h2>Управляемая проверка: специально сломанный тест</h2>
    <p>Полезно один раз увидеть, как выглядит красная (неудачная) проверка — и как её
    исправить, — прежде чем столкнуться с этим впервые в реальной ситуации. В истории запусков
    выше это тот самый красный кружок: временный коммит намеренно вернул регистрозависимое
    сравнение расширений в классификаторе (тот же дефект, что показан в разделе 23-23 как
    RED/GREEN пример), затем был отменён следующим же коммитом — main ни на секунду не
    оставался в сломанном состоянии.</p>
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
        "В отдельном репозитории воркфлоу запускается без ограничения по paths — любое изменение здесь так или иначе касается SafeSort.",
        "Специально сломанный и затем исправленный тест — быстрый способ научиться читать журнал проверки.",
    ])}
    """
    out = render_page(
        page_title="GitHub Actions: автоматически запускаем тесты",
        description="Воркфлоу GitHub Actions с ограничением по paths и упражнение на намеренно сломанном тесте.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("GitHub Actions", "")],
        kicker="Глава 23 · Часть V · Проверяем и автоматизируем",
        h1="GitHub Actions: автоматически запускаем тесты",
        lede="Один файл воркфлоу запускает тесты SafeSort автоматически при каждом изменении — без ручной проверки перед Pull Request.",
        body_html=body,
        sidebar_groups=sidebar("23-30-github-actions.html"),
        nav=PageNav(prev_href="23-29-github-pr.html", prev_label="Issue, ветка, PR", next_href="23-31-versiya-reliz.html", next_label="Версия и первый релиз"),
    )
    write("23-30-github-actions.html", out)


def build_31() -> None:
    body = f"""
    {stage_tracker(6)}

    <p>Проект готов, проверен тестами и подключён к автоматической проверке. Мы закончили
    первую пригодную для использования версию SafeSort. Теперь ей нужен номер, чтобы отличать
    её от будущих изменений — тот самый номер, который мы уже записали в
    <code class="inline">pyproject.toml</code> ещё в части III, где он был просто техническим
    полем. Сейчас разберём, что он означает.</p>

    {flow_diagram(
        [
            ("0", "MAJOR — несовместимые изменения"),
            ("1", "MINOR — новая возможность, старое поведение сохранено"),
            ("0", "PATCH — исправление ошибки"),
        ],
        caption="0.1.0 — три числа, разделённые точкой, каждое отвечает за свой тип изменений",
    )}

    <h2>Семантическое версионирование</h2>
    <p>Эта схема называется <strong>семантическим версионированием</strong> (Semantic
    Versioning, SemVer) — соглашение о записи номера версии как
    <code class="inline">MAJOR.MINOR.PATCH</code>:</p>
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

    <div style="display:flex;align-items:center;gap:8px;font-family:Sora,sans-serif;font-weight:700;
      font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:#5B24F9;margin:24px 0 16px">
      {github_mark()}<span>GitHub Release строится поверх тега</span>
    </div>

    <h2>Тег и релиз</h2>
    <p><strong>Тег</strong> (tag) — постоянная метка на конкретном коммите, обычно
    соответствующая номеру версии. <strong>Релиз</strong> на GitHub строится поверх тега и
    добавляет к нему описание изменений — то же содержание, что и в CHANGELOG, но в формате,
    который видно прямо на странице репозитория. Тег версии относится ко всему репозиторию
    целиком, а не к одной его части — именно поэтому SafeSort живёт в собственном репозитории
    <code class="inline">Cartesian-School/safesort</code>, а не только в подкаталоге курса:
    <code class="inline">git tag v0.1.0</code> здесь однозначно означает «версия 0.1.0
    SafeSort», без двусмысленности.</p>

    {terminal_capture([
        "$ git tag -a v0.1.0 -m \"SafeSort 0.1.0 — first release\"",
        "$ git push origin v0.1.0",
        "To https://github.com/Cartesian-School/safesort.git",
        " * [new tag]         v0.1.0 -> v0.1.0",
    ], cwd="~/safesort")}

    {image_figure(
        f"{IMG}/safesort-release.jpg",
        "Страница релиза SafeSort 0.1.0 на GitHub: заголовок, метка Latest, описание, команда pip install, прикреплённые файлы wheel и sdist",
        "Настоящий релиз SafeSort 0.1.0 — тег, описание изменений и собранные пакеты (wheel и sdist) как файлы релиза.",
        size="wide",
    )}

    {callout(
        "info",
        "Релиз создан только после того, как всё остальное было готово",
        "Тег и релиз — последний шаг, не первый: он появился только когда CI был зелёным, "
        "CHANGELOG.md описывал реальные изменения, а editable install, сборка wheel/sdist и "
        "команда <code class=\"inline\">safesort --help</code> были заново проверены на чистом "
        "окружении. Релиз без этих проверок — только цифра в номере, ничего не гарантирующая.",
    )}

    {callout(
        "tip",
        "Публикация в PyPI — осознанно за рамками версии 0.1.0",
        "Установка через <code class=\"inline\">pip install git+https://github.com/Cartesian-"
        "School/safesort.git@v0.1.0</code> достаточна для разработки и личного использования. "
        "Публикация пакета в PyPI, чтобы его можно было установить командой "
        "<code class=\"inline\">pip install safesort</code> без ссылки на репозиторий, — "
        "отдельная тема с собственными требованиями к учётной записи и публикации, и версия "
        "0.1.0 сознательно её не касается.",
    )}

    {summary_box("Коротко", [
        "MAJOR.MINOR.PATCH — соглашение о номере версии, а не встроенное в инструменты правило.",
        "CHANGELOG.md описывает только версии, которые действительно вышли.",
        "Тег версии относится ко всему репозиторию — SafeSort живёт в собственном репозитории, "
        "поэтому v0.1.0 однозначно означает «версия SafeSort», а не «версия курса».",
    ])}
    """
    out = render_page(
        page_title="Документация, версия и первый релиз",
        description="Семантическое версионирование, CHANGELOG.md, реальный тег и GitHub Release SafeSort 0.1.0.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Версия и релиз", "")],
        kicker="Глава 23 · Часть VI · Выпускаем первую версию",
        h1="Документация, версия и первый релиз",
        lede="MAJOR.MINOR.PATCH, CHANGELOG.md, настоящий тег и GitHub Release — проект получает точку, к которой можно вернуться и на которую можно ссылаться.",
        body_html=body,
        sidebar_groups=sidebar("23-31-versiya-reliz.html"),
        nav=PageNav(prev_href="23-30-github-actions.html", prev_label="GitHub Actions", next_href="23-32-itogi-reliz.html", next_label="Итоги главы"),
    )
    write("23-31-versiya-reliz.html", out)


def build_32() -> None:
    body = f"""
    {stage_tracker(6)}

    <h2 id="itogi">Полный путь проекта</h2>
    <p>В начале этой главы SafeSort был только идеей. Теперь это настоящий репозиторий на
    GitHub — <a href="https://github.com/Cartesian-School/safesort">Cartesian-School/safesort</a>
    — с 14 закрытыми Issues, реальными Pull Request, зелёной проверкой CI и опубликованным
    релизом 0.1.0. Вот весь путь целиком, с тем, что появилось на каждом шаге:</p>

    {timeline_diagram([
        ("Идея", "требования: что программа делает и чего не делает"),
        ("Git и GitHub", "установка, аутентификация, настоящий репозиторий SafeSort"),
        ("GitHub Project", "14 Issues — задача сформулирована для каждой части"),
        ("README.md, pyproject.toml", "первый коммит репозитория — команда safesort становится доступной"),
        ("Сканер", "scanner.py — Issue №1, PR №15"),
        ("Классификатор", "classifier.py — Issue №2, PR №16"),
        ("План и коллизии", "planner.py — Issues №3 и №6 вместе, PR №17"),
        ("Apply", "executor.py — Issue №5, PR №18"),
        ("Manifest и undo", "manifest.py — Issues №7 и №8 вместе, PR №19"),
        ("Дубликаты", "duplicates.py — размер → SHA-256 → байтовое подтверждение, Issue №9, PR №20"),
        ("Командная строка", "argparse, пять подкоманд — Issue №4, PR №21 (последней, когда всё остальное уже было)"),
        ("Ошибки, config, тесты, CI", "Issues №10–13 — часть реализации соответствующих модулей, без отдельного PR"),
        ("Версия 0.1.0", "CHANGELOG.md, editable install, wheel и sdist проверены заново — Issue №14"),
        ("Релиз", "настоящий тег v0.1.0 и GitHub Release"),
    ], caption="От идеи до опубликованного релиза — точная история: 9 из 14 Issues закрыты через 7 Pull Request (два PR закрыли по два Issue), остальные пять — без отдельного PR")}

    {project_state_card(
        [
            "Git и GitHub настроены", "Настоящий репозиторий SafeSort", "GitHub Project и 14 Issues",
            "Установленный пакет", "Работающая командная строка", "Безопасные перемещения с отменой",
            "Поиск дубликатов", "Автоматические тесты", "GitHub Actions (CI)",
        ],
        "Версия 0.1.0 — тег и GitHub Release опубликованы",
        ["Публикация в PyPI", "Классификация по содержимому файла"],
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
    <p>Версия 0.1.0 сознательно не покрывает всё, что в принципе возможно: самый первый раздел этой главы заранее
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
        kicker="Глава 23 · Часть VI · Выпускаем первую версию",
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
    <div style="display:flex;align-items:center;gap:8px;font-family:Sora,sans-serif;font-weight:700;
      font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:#5B24F9;margin:8px 0 16px">
      {github_mark()}<span>GitHub-практика — тот же рабочий процесс, что и в SafeSort, самостоятельно</span>
    </div>

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
    <p><a href="https://github.com/Cartesian-School/python-mini-projects">python-mini-projects</a>
    — эталонный репозиторий курса: он показывает ожидаемую структуру и рабочий процесс, но
    учебная работа выполняется не прямо в нём. Практика — в собственной копии:</p>

    {flow_diagram(
        [
            ("Cartesian School", "эталонный репозиторий — структура и пример"),
            ("Ваш аккаунт", "собственный репозиторий или fork этого же имени"),
            ("Шесть проектов", "Issue → ветка → код → тесты → PR — в вашем репозитории"),
        ],
        caption="Практика выполняется в собственном репозитории или fork, не прямо в репозитории школы",
    )}

    <p>Один репозиторий на все шесть проектов, а не шесть отдельных:</p>
    {comparison_table(
        ["Один репозиторий", "Шесть репозиториев"],
        [
            ["Один и тот же рабочий процесс с Issue, веткой и Pull Request повторяется шесть раз в одном месте", "Тот же процесс нужно настраивать заново для каждого репозитория"],
            ["Прогресс по всем проектам виден сразу в одном списке коммитов и PR", "Прогресс разбросан по шести отдельным историям"],
            ["На странице профиля — один репозиторий с шестью проектами внутри", "На странице профиля — шесть отдельных репозиториев, каждый на одну небольшую задачу"],
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

    <div style="display:flex;align-items:center;gap:8px;font-family:Sora,sans-serif;font-weight:700;
      font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:#5B24F9;margin:24px 0 4px">
      {github_mark()}<span>GitHub-практика</span>
    </div>
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
        'GLAGOLY = ["нашёл", "потерял", "починил", "изобрёл", "спрятал"]\n'
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

    <div style="display:flex;align-items:center;gap:8px;font-family:Sora,sans-serif;font-weight:700;
      font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:#5B24F9;margin:24px 0 4px">
      {github_mark()}<span>GitHub-практика</span>
    </div>
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
    <p>Определение победителя раунда — только один из кусков логики игры (наряду со случайным
    ходом компьютера и подсчётом счёта матча ниже), но именно он умещается в одном словаре —
    кто кого побеждает:</p>
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

    <div style="display:flex;align-items:center;gap:8px;font-family:Sora,sans-serif;font-weight:700;
      font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:#5B24F9;margin:24px 0 4px">
      {github_mark()}<span>GitHub-практика</span>
    </div>
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
        lede="Победителя раунда решает один словарь — кто кого побеждает; матч теперь заканчивается по ясному условию — до трёх побед.",
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

    <div style="display:flex;align-items:center;gap:8px;font-family:Sora,sans-serif;font-weight:700;
      font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:#5B24F9;margin:24px 0 4px">
      {github_mark()}<span>GitHub-практика</span>
    </div>
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

    <div style="display:flex;align-items:center;gap:8px;font-family:Sora,sans-serif;font-weight:700;
      font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:#5B24F9;margin:24px 0 4px">
      {github_mark()}<span>GitHub-практика</span>
    </div>
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

    <div style="display:flex;align-items:center;gap:8px;font-family:Sora,sans-serif;font-weight:700;
      font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:#5B24F9;margin:24px 0 4px">
      {github_mark()}<span>GitHub-практика</span>
    </div>
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
    build_git_01()
    build_git_02()
    build_git_03()
    build_git_04()
    build_git_05()
    build_git_06()
    build_git_07()
    build_git_08()
    build_git_09()
    build_git_10()
    build_proj_01()
    build_proj_02()
    build_proj_03()
    build_proj_04()
    build_proj_05()
    build_proj_06()
    build_proj_07()
    build_proj_08()
    build_proj_09()
    build_proj_10()
    build_proj_11()
    build_proj_12()
    build_proj_13()
    build_proj_14()
    build_proj_15()
    build_proj_16()
    build_proj_17()
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
