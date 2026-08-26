#!/usr/bin/env python3
"""Строит Главу 12: «Множество увлекательных мини-проектов!» (site/chapters/glava-12/).

Curriculum v2: первая настоящая проектная лаборатория курса — глава не
вводит новую теорию, а учит СТРОИТЬ программу из идеи: декомпозиция задачи
на шаги, алгоритм/блок-схема до кода, инкрементальная разработка маленькими
проверяемыми шагами, тестовые таблицы и граничные случаи, воркфлоу отладки,
данные отдельно от алгоритма (data-driven programming) и лёгкий рефакторинг
— на 16 проектах, использующих условия, циклы, строки, числа, random,
списки/кортежи/множества/словари и Turtle из глав 1-11 вместе.

Существующие маршруты и практики (12-01..12-06, все шесть исходных
проектов) сохранены на месте и расширены по этому же шаблону; новый
материал — новые страницы и новые ID практик (12-07..12-22), без
переиспользования занятых ID.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from chapter_12_examples import EXAMPLES
from site_lib import (
    ChapterSectionLink,
    NavItem,
    PageNav,
    SidebarGroup,
    branch_diagram,
    callout,
    capability_map,
    classic_vs_modern,
    code_block,
    comparison_table,
    converge_diagram,
    decision_map,
    exercise,
    flowchart,
    flow_diagram,
    for_loop_flowchart,
    local_required_card,
    matrix_diagram,
    namespace_diagram,
    practice_card,
    render_chapter_opener,
    render_page,
    summary_box,
    timeline_diagram,
    tree_diagram,
    while_loop_flowchart,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-12"
IMG = "../../assets/img"

PAGES = [
    ("index.html", "Обзор главы"),
    ("12-07-chto-takoe-proekt.html", "Что такое проект"),
    ("12-08-stroim-proekt-po-shagam.html", "Строим проект по шагам"),
    ("12-01-chetnoe-ili-nechetnoe.html", "Проект: чётное или нечётное"),
    ("12-02-chaevye.html", "Проект: достаточно ли чаевых?"),
    ("12-09-ugadaj-chislo-v3.html", "Проект: угадай число, версия 3"),
    ("12-11-analizator-teksta.html", "Проект: анализатор текста и частота слов"),
    ("12-13-zapisnaya-knizhka.html", "Проект: записная книжка"),
    ("12-14-zhurnal-i-korzina.html", "Проекты: журнал оценок и корзина покупок"),
    ("12-16-viktorina.html", "Проект: викторина"),
    ("12-18-konsol-i-validator.html", "Проекты: консоль команд и проверка пароля"),
    ("12-20-studiya-mnogougolnikov.html", "Проект: студия многоугольников"),
    ("12-03-elka.html", "Проект: рождественская ёлка"),
    ("12-04-spirali.html", "Проект: спирали!"),
    ("12-05-slozhnaya-mandala.html", "Проект: сложная мандала"),
    ("12-22-setka-piksel-art.html", "Проект: пиксельная графика по сетке"),
    ("12-06-gonka-turtle-itogi.html", "Проект: гонка Turtle и итоги главы"),
]

PRACTICE_IDS = [
    "12-07", "12-08", "12-01", "12-02", "12-09", "12-10", "12-11", "12-12",
    "12-13", "12-14", "12-15", "12-16", "12-17", "12-18", "12-19", "12-20",
    "12-21", "12-03", "12-04", "12-05", "12-22", "12-06",
]

LOCAL_REQUIRED_IDS = {"12-03", "12-04", "12-05", "12-06", "12-21", "12-22"}


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 12 · Проекты", items),
        SidebarGroup("Практика", [
            NavItem(f"[[icon:practice]] {lid}: Практика", f"../../practice/{lid}/index.html") for lid in PRACTICE_IDS
        ]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    clean = "\n".join(line.rstrip() for line in html_out.split("\n"))
    path.write_text(clean, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def two_up(left_html: str, right_html: str) -> str:
    return f"""
    <div style="display:flex;gap:20px;flex-wrap:wrap;margin:20px 0;align-items:flex-start">
      <div style="flex:1 1 260px;min-width:220px">{left_html}</div>
      <div style="flex:1 1 260px;min-width:220px">{right_html}</div>
    </div>"""


def turtle_output(name: str, filename: str, *, caption: str, alt: str) -> str:
    """КОД → РЕАЛЬНЫЙ OUTPUT — тот же компонент, что и в главах 6-7-10 (см.
    scripts/build_chapter_10.py:turtle_output). code_block() слева/сверху,
    реально выполненная картинка справа/снизу; код в EXAMPLES не содержит
    exitonclick()/bye() — эта строка дописывается только для читателя."""
    code = EXAMPLES[name] + "\nscreen.exitonclick()\n"
    return f"""
    <div style="display:flex;gap:20px;flex-wrap:wrap;margin:24px 0;align-items:flex-start">
      <div style="flex:1 1 340px;min-width:280px">
{code_block(filename, code)}
      </div>
      <div style="flex:1 1 300px;min-width:260px">
        <div style="font-family:Sora,sans-serif;font-weight:700;font-size:12px;letter-spacing:.05em;
          text-transform:uppercase;color:#5B24F9;margin-bottom:8px">Результат выполнения</div>
        <figure style="margin:0;padding:14px;background:var(--color-bg-surface,#FAFAFC);
          border-radius:var(--radius-lg,20px)">
          <img src="{IMG}/chapter-12/output/{name}.png" alt="{alt}"
            style="width:100%;height:auto;border-radius:12px;display:block;background:#fff" />
          <figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{caption}</figcaption>
        </figure>
      </div>
    </div>"""


def image_gallery(items: list[tuple[str, str]], *, caption: str = "") -> str:
    """Компактная галерея готовых Turtle-картинок без повторения кода —
    для «одна формула, разные данные» (студия многоугольников): код
    показывается один раз, а результат для каждого значения — рядом,
    маленькими карточками."""
    cards = "".join(
        f"""<figure style="margin:0;padding:10px;background:var(--color-bg-surface,#FAFAFC);
          border-radius:var(--radius-lg,16px);flex:1 1 150px;min-width:130px;max-width:180px">
          <img src="{IMG}/chapter-12/output/{name}.png" alt="{label}"
            style="width:100%;height:auto;border-radius:10px;display:block;background:#fff" />
          <figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px;font-weight:700">{label}</figcaption>
        </figure>"""
        for name, label in items
    )
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">{caption}</figcaption>' if caption else ""
    return f"""
    <div style="display:flex;gap:14px;flex-wrap:wrap;justify-content:center;margin:20px 0">{cards}</div>
    {cap}"""


def requirements_card(uses: list[str], level: str, result: str) -> str:
    """Небольшая карточка «Используем / Уровень / Результат» — открывает
    каждый проект главы, чтобы было видно, какие уже знакомые темы
    складываются вместе, и чего ожидать на выходе."""
    uses_html = "".join(f'<code class="inline">{u}</code>' for u in uses)
    return f"""
    <div style="display:flex;gap:24px;flex-wrap:wrap;margin:20px 0;padding:18px 22px;
      background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px)">
      <div style="flex:2 1 260px">
        <div style="font-family:Sora,sans-serif;font-weight:700;font-size:12px;letter-spacing:.05em;
          text-transform:uppercase;color:#5B24F9;margin-bottom:8px">Используем</div>
        <div style="display:flex;gap:8px;flex-wrap:wrap">{uses_html}</div>
      </div>
      <div style="flex:1 1 140px">
        <div style="font-family:Sora,sans-serif;font-weight:700;font-size:12px;letter-spacing:.05em;
          text-transform:uppercase;color:#5B24F9;margin-bottom:8px">Уровень</div>
        <div style="font-size:16px">{level}</div>
      </div>
      <div style="flex:1 1 200px">
        <div style="font-family:Sora,sans-serif;font-weight:700;font-size:12px;letter-spacing:.05em;
          text-transform:uppercase;color:#5B24F9;margin-bottom:8px">Результат</div>
        <div style="font-size:16px">{result}</div>
      </div>
    </div>"""


def terminal_transcript(lines: list[str], *, caption: str = "") -> str:
    """Панель с реалистичной, детерминированной терминальной транскрипцией
    выполнения программы — вместо того, чтобы просить учащегося
    вообразить результат."""
    body = "\n".join(lines)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{caption}</figcaption>' if caption else ""
    return f"""
    <figure style="margin:24px 0">
      <pre style="background:#0D0230;color:#E7DEFF;border-radius:var(--radius-lg,20px);
        padding:18px 22px;overflow-x:auto;font-family:'JetBrains Mono',monospace;font-size:14px;
        line-height:1.7"><code>{body}</code></pre>
      {cap}
    </figure>"""


_HREFS = [h for h, _ in PAGES]
_TITLES = dict(PAGES)


def nav_for(current_href: str) -> PageNav:
    i = _HREFS.index(current_href)
    prev_href, prev_label = (_HREFS[i - 1], _TITLES[_HREFS[i - 1]]) if i > 0 else (None, None)
    if i < len(_HREFS) - 1:
        next_href, next_label = _HREFS[i + 1], _TITLES[_HREFS[i + 1]]
    else:
        next_href, next_label = "../glava-13/index.html", "Глава 13: Автоматизация с помощью функций"
    return PageNav(prev_href=prev_href, prev_label=prev_label, next_href=next_href, next_label=next_label)


def page(href: str, *, page_title: str, description: str, kicker_suffix: str, h1: str, lede: str, body_html: str) -> None:
    out = render_page(
        page_title=page_title,
        description=description,
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 12", "index.html"), (kicker_suffix, "")],
        kicker="Глава 12 · Множество увлекательных мини-проектов!",
        h1=h1,
        lede=lede,
        body_html=body_html,
        sidebar_groups=sidebar(href),
        nav=nav_for(href),
    )
    write(href, out)


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=12,
        description="Первая настоящая проектная лаборатория курса: 16 проектов, которые заставляют "
        "работать вместе всё, что вы изучили в главах 1-11 — условия, циклы, строки, числа, "
        "random, списки/кортежи/множества/словари и Turtle. Не новая теория, а то, как строить "
        "программу из идеи: декомпозиция, алгоритм до кода, разработка маленькими шагами, тесты "
        "и отладка.",
        meta_items=["[[icon:timer]] ~8 часов", "[[icon:architecture]] проектная лаборатория", "[[icon:practice]] 22 практики"],
        sections=[
            ChapterSectionLink("12.1", "Что такое проект", "12-07-chto-takoe-proekt.html"),
            ChapterSectionLink("12.2", "Строим проект по шагам", "12-08-stroim-proekt-po-shagam.html"),
            ChapterSectionLink("12.3", "Проект: чётное или нечётное", "12-01-chetnoe-ili-nechetnoe.html"),
            ChapterSectionLink("12.4", "Проект: достаточно ли чаевых?", "12-02-chaevye.html"),
            ChapterSectionLink("12.5", "Проект: угадай число, версия 3", "12-09-ugadaj-chislo-v3.html"),
            ChapterSectionLink("12.6", "Проект: анализатор текста и частота слов", "12-11-analizator-teksta.html"),
            ChapterSectionLink("12.7", "Проект: записная книжка", "12-13-zapisnaya-knizhka.html"),
            ChapterSectionLink("12.8", "Проекты: журнал оценок и корзина покупок", "12-14-zhurnal-i-korzina.html"),
            ChapterSectionLink("12.9", "Проект: викторина", "12-16-viktorina.html"),
            ChapterSectionLink("", "Данные vs алгоритм, рефакторинг", "12-16-viktorina.html#dannye-vs-algoritm"),
            ChapterSectionLink("12.10", "Проекты: консоль команд и проверка пароля", "12-18-konsol-i-validator.html"),
            ChapterSectionLink("12.11", "Проект: студия многоугольников", "12-20-studiya-mnogougolnikov.html"),
            ChapterSectionLink("12.12", "Проект: рождественская ёлка", "12-03-elka.html"),
            ChapterSectionLink("12.13", "Проект: спирали!", "12-04-spirali.html"),
            ChapterSectionLink("12.14", "Проект: сложная мандала", "12-05-slozhnaya-mandala.html"),
            ChapterSectionLink("12.15", "Проект: пиксельная графика по сетке", "12-22-setka-piksel-art.html"),
            ChapterSectionLink("12.16", "Проект: гонка Turtle", "12-06-gonka-turtle-itogi.html"),
            ChapterSectionLink("", "Итоги главы", "12-06-gonka-turtle-itogi.html#itogi"),
        ],
    )
    write("index.html", out)


# ---------------------------------------------------------------------------
# 12-07 · Что такое проект
# ---------------------------------------------------------------------------

def build_07() -> None:
    body = f"""
    <h2>От инструментов — к программе</h2>
    <p>Главы 1-11 научили вас инструментам по отдельности: строкам, числам, условиям, циклам,
    Turtle, спискам и словарям. Эта глава не добавляет новых инструментов — она учит
    <strong>складывать их вместе</strong>, чтобы получилась настоящая, работающая программа.</p>
    {converge_diagram(
        ["Строки", "Числа", "Условия", "Циклы", "Списки / словари", "Turtle"],
        "ПРОГРАММА",
        caption="Главы 1-11 — отдельные инструменты. Глава 12 — как собрать их в одну программу",
    )}

    <h2>Чем проект отличается от упражнения</h2>
    {comparison_table(
        ["", "Упражнение", "Проект"],
        [
            ["Пример", "Вычислите <code class=\"inline\">7 % 3</code>", "Постройте конвертер секунд в часы/минуты/секунды с проверкой ввода"],
            ["Входные данные", "обычно нет", "есть, и их нужно продумать заранее"],
            ["Шагов", "один", "несколько, связанных друг с другом"],
            ["Результат", "одно значение", "оформленный вывод, реакция на разные случаи"],
            ["Ошибки", "почти невозможны", "нужно продумать, что может пойти не так"],
        ],
    )}
    {callout(
        "info",
        "Проект — это не «код побольше»",
        "Разница не в количестве строк, а в том, что у проекта есть <strong>цель</strong>, "
        "<strong>входные данные</strong>, <strong>правила</strong> и <strong>результат</strong> "
        "— и всё это нужно продумать до того, как написана первая строка кода.",
    )}

    <h2 id="dekompoziciya">Декомпозиция: разбиваем большую задачу на маленькие</h2>
    <p>Задача «Постройте игру-угадайку» слишком большая, чтобы решить её одним куском кода. Разобьём
    на понятные шаги:</p>
    {branch_diagram(
        "Построить игру-угадайку",
        [
            ("1. Выбрать секрет", "случайное число"),
            ("2. Спросить игрока", "input()"),
            ("3. Преобразовать ввод", "int()"),
            ("4. Сравнить", "если/иначе"),
            ("5. Подсказать", "мало/много"),
            ("6. Повторить", "цикл"),
            ("7. Считать попытки", "счётчик"),
            ("8. Завершить", "угадал!"),
        ],
        caption="Декомпозиция: одна большая задача → восемь маленьких, понятных шагов",
    )}
    {callout(
        "tip",
        "Декомпозиция",
        "<strong>Декомпозиция</strong> — разделить большую задачу на маленькие понятные части. "
        "Это один из самых важных навыков в программировании: гораздо проще написать (и "
        "проверить) восемь маленьких шагов, чем один запутанный кусок кода на сто строк.",
    )}

    <h2>Шаблон проекта, который мы будем использовать</h2>
    <p>Каждый крупный проект этой главы устроен по одной и той же схеме — не обязательно с этими
    же самыми заголовками, но в этом же порядке мысли:</p>
    {capability_map([
        ("1 · Что создаём", ["Цель проекта", "Как выглядит готовый результат"]),
        ("2 · Данные", ["Входные данные", "Какая структура их хранит"]),
        ("3 · Алгоритм", ["Порядок действий", "Блок-схема, если это уместно"]),
        ("4 · Реализация", ["По одному этапу за раз", "Проверка после каждого этапа"]),
        ("5 · Проверка", ["Типичные ошибки", "Debug Lab", "Что можно улучшить"]),
    ], title="Повторяющийся ритм каждого проекта главы")}

    <h2>Требования и «что значит „готово“»</h2>
    <p>Прежде чем писать код, полезно явно сформулировать требования — что программа обязана
    делать, чтобы считаться готовой. Пример для будущей игры-угадайки:</p>
    {comparison_table(
        ["Требование", "Проверка"],
        [
            ["компьютер выбирает целое число от 1 до 100", "секрет — int в диапазоне [1, 100]"],
            ["игрок вводит числа-попытки", "input() + int()"],
            ["программа говорит «мало» / «много»", "if/elif/else"],
            ["программа завершается на правильном ответе", "цикл прекращается при guess == secret"],
            ["попытки считаются", "counter увеличивается на каждой попытке"],
        ],
    )}
    {callout(
        "info",
        "Чек-лист приёмки",
        "Такой список называют <strong>чек-листом приёмки</strong> — до кода мы уже знаем, что "
        "именно должно быть верно, чтобы сказать «проект готов». Не обязательно оформлять его "
        "формально каждый раз — но держать в голове стоит всегда.",
    )}

    <h2 id="razminka">Разминка: статистика трёх чисел</h2>
    <p>Прежде чем переходить к крупным проектам, потренируем сам процесс — от задачи до кода —
    на программе из нескольких строк.</p>
    <p><strong>Задача:</strong> получить три числа и вывести минимальное, максимальное, сумму и
    среднее.</p>
    {code_block(
        "statistika_treh_chisel.py",
        'a = float(input("Первое число: "))\n'
        'b = float(input("Второе число: "))\n'
        'c = float(input("Третье число: "))\n\n'
        "chisla = [a, b, c]\n\n"
        'print(f"Минимум: {min(chisla)}")\n'
        'print(f"Максимум: {max(chisla)}")\n'
        'print(f"Сумма: {sum(chisla)}")\n'
        'print(f"Среднее: {sum(chisla) / len(chisla):.2f}")\n',
    )}
    {callout(
        "tip",
        "Даже такая маленькая программа — уже проект",
        "У неё есть входные данные (три числа), структура для их хранения (список — глава 11), "
        "правило обработки (<code class=\"inline\">min/max/sum/len</code> — глава 11) и "
        "оформленный результат (f-строки — глава 8). Дальше в главе — то же самое, но крупнее.",
    )}

    {practice_card(
        "12-07",
        "Практика: статистика трёх чисел — от задачи до кода",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/12-07/index.html",
    )}
    """
    page(
        "12-07-chto-takoe-proekt.html",
        page_title="Что такое проект",
        description="Чем проект отличается от упражнения, декомпозиция задачи на шаги, шаблон проекта и требования/чек-лист приёмки.",
        kicker_suffix="Что такое проект",
        h1="Что такое проект",
        lede="До сих пор мы изучали инструменты по отдельности. Теперь учимся складывать их "
        "в настоящую программу — начиная с того, как вообще подступиться к большой задаче.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 12-08 · Строим проект по шагам
# ---------------------------------------------------------------------------

def build_08() -> None:
    body = f"""
    <h2>Не пишите 80 строк, а потом нажимайте «Запустить»</h2>
    <p>Профессиональная привычка, которую стоит выработать с первого крупного проекта:
    <strong>инкрементальная разработка</strong> — маленькими шагами, каждый из которых сразу
    проверяется.</p>
    {flow_diagram([
        ("Маленькая версия", "5 строк"),
        ("Проверка", "запустили, посмотрели"),
        ("+ новая часть", "ветвление / цикл"),
        ("Проверка", "снова запустили"),
        ("Финальный проект", "по шагам, а не сразу"),
    ], caption="Small version → test → add a feature → test → ... — а не всё и сразу")}
    {callout(
        "tip",
        "Работающая маленькая версия лучше, чем неработающая большая",
        "Если после каждого маленького шага программа запускается и делает то, что ожидалось "
        "— вы всегда точно знаете, где искать причину, если что-то сломалось на следующем шаге.",
    )}

    <h2>Версии: сначала работает, потом — лучше</h2>
    {comparison_table(
        ["Версия", "Что в ней есть"],
        [
            ["V1", "минимальная работающая версия — ядро идеи, без украшений"],
            ["V2", "более надёжная проверка ввода, обработка граничных случаев"],
            ["V3", "дополнительные возможности, улучшенный вывод"],
        ],
    )}
    <p>Такую первую работающую версию иногда называют <strong>MVP</strong> (minimal working
    version) — «сначала добьёмся маленькой, но работающей версии», а уже потом улучшаем.</p>

    <h2>Проверяем проект на примерах</h2>
    <p>Для каждого нетривиального проекта полезно заранее продумать несколько сценариев — что
    подать на вход и что должно получиться на выходе:</p>
    {comparison_table(
        ["Сценарий", "Вход", "Ожидаемый результат"],
        [
            ["секрет 50, попытка меньше", "guess = 20", "«слишком мало»"],
            ["секрет 50, попытка больше", "guess = 70", "«слишком много»"],
            ["секрет 50, попытка верна", "guess = 50", "победа, цикл завершается"],
        ],
    )}
    {callout(
        "info",
        "Граничные случаи",
        "Обычных примеров недостаточно — стоит явно проверить: пустой ввод, ноль, "
        "отрицательное число там, где оно не ожидается, повтор в данных, пустой список, "
        "неизвестная команда, значение точно на границе диапазона. Мы вернёмся к этой идее в "
        "каждом крупном проекте главы.",
    )}

    <h2>Воркфлоу отладки</h2>
    {flow_diagram([
        ("Ожидание", "EXPECTED"),
        ("Реальность", "ACTUAL"),
        ("Первое расхождение", "где именно разошлось"),
        ("Причина", "какая строка виновата"),
        ("Исправление", "меняем одну вещь"),
    ], caption="Ожидание vs реальность → первое расхождение → причина → исправление")}
    <p>Пошагово:</p>
    {capability_map([
        ("1", ["Воспроизвести ошибку", "получить её снова, стабильно"]),
        ("2", ["Осмотреть значения", "print() нужных переменных"]),
        ("3", ["Найти первое неверное состояние", "где ожидание разошлось с фактом"]),
        ("4", ["Изолировать условие/цикл", "какая именно строка виновата"]),
        ("5", ["Исправить одну причину", "не переписывать всё"]),
        ("6", ["Запустить снова", "убедиться, что починилось"]),
    ], title="Шесть шагов отладки — работают для любого проекта этой главы")}

    <h2>print()-отладка</h2>
    {code_block(
        "print_otladka.py",
        "for word in words:\n"
        '    print("DEBUG:", word, counts.get(word))   # временная диагностика\n'
        "    counts[word] = counts.get(word, 0) + 1\n",
    )}
    {callout(
        "tip",
        "Уберите отладочные print() после того, как нашли причину",
        "Временный <code class=\"inline\">print(\"DEBUG:\", ...)</code> внутри цикла — самый "
        "надёжный способ увидеть, что происходит на самом деле. Уберите такие строки, когда "
        "баг найден и исправлен — иначе они засоряют настоящий вывод программы.",
    )}

    <h2>[[icon:debug]] Debug Lab: найдите ошибку</h2>
    <p>В программе ниже счёт должен расти на каждом правильном ответе, но почему-то всегда
    остаётся <code class="inline">1</code>. Прежде чем читать дальше — попробуйте найти причину
    сами.</p>
    {code_block(
        "debug_lab_schet.py",
        'answers = ["python", "git", "sql"]\n'
        'user_answers = ["python", "python", "sql"]\n\n'
        "for correct, given in zip(answers, user_answers):\n"
        "    score = 0\n"
        "    if given == correct:\n"
        "        score += 1\n\n"
        'print("Итоговый счёт:", score)\n',
    )}
    {callout(
        "warning",
        "Причина: счётчик обнуляется внутри цикла",
        "<code class=\"inline\">score = 0</code> стоит ВНУТРИ тела цикла — значит, он "
        "пересоздаётся на каждой итерации, и предыдущий прогресс теряется. Счётчик нужно "
        "инициализировать ОДИН раз, до цикла — та же ошибка, что и «почему cart total "
        "сбрасывается на каждой итерации» из главы 10.",
    )}

    <h2>Чек-лист готовности проекта</h2>
    {summary_box("Прежде чем сказать «проект готов»", [
        "Программа выполняет то, что требовалось (чек-лист приёмки)?",
        "Обычный, «счастливый» ввод работает правильно?",
        "Проверены граничные случаи (пусто, ноль, повтор, неизвестная команда)?",
        "Имена переменных понятны без дополнительных объяснений?",
        "Нет ли повторяющегося куска кода, который можно было бы убрать?",
        "Использована ли подходящая коллекция (список / множество / словарь)?",
        "Цикл действительно останавливается в нужный момент?",
        "Условия проверяют именно то, что нужно?",
        "Вывод понятен — пользователь видит, что произошло?",
        "Сможет ли другой человек прочитать и понять эту программу?",
    ])}

    {practice_card(
        "12-08",
        "Практика: Debug Lab — найдите и исправьте ошибку счётчика",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/12-08/index.html",
    )}
    """
    page(
        "12-08-stroim-proekt-po-shagam.html",
        page_title="Строим проект по шагам",
        description="Инкрементальная разработка, тестовые сценарии, граничные случаи, воркфлоу отладки, print()-отладка и чек-лист готовности проекта.",
        kicker_suffix="Строим проект по шагам",
        h1="Строим проект по шагам",
        lede="Маленькими проверяемыми шагами вместо 80 строк за раз — и системный способ найти "
        "и исправить ошибку, когда что-то пошло не так.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 12-01 · Чётное или нечётное (расширено шаблоном проекта)
# ---------------------------------------------------------------------------

def build_01() -> None:
    body = f"""
    {requirements_card(["input()", "int()", "%", "if/else", "list comprehension"], "★ разминка", "текстовая программа")}

    <h2>Что создаём</h2>
    <p>Первый настоящий проект главы — маленький, но с полным циклом: данные → алгоритм → код →
    результат.</p>

    <h2>Часть 1 — Ваше число чётное или нечётное?</h2>
    {code_block(
        "chetnoe_ili_nechetnoe.py",
        'number = int(input("Введите число: "))\n\n'
        "if number % 2 == 0:\n"
        '    print(f"{number} — чётное.")\n'
        "else:\n"
        '    print(f"{number} — нечётное.")\n',
    )}
    {terminal_transcript([
        "Введите число: 17",
        "17 — нечётное.",
    ], caption="Детерминированный пример выполнения")}

    <h2>Часть 2 — выводим чётные или нечётные числа из диапазона</h2>
    {code_block(
        "chetnye_iz_diapazona.py",
        'nachalo = int(input("Начало диапазона: "))\n'
        'konec = int(input("Конец диапазона: "))\n\n'
        "chetnye = [n for n in range(nachalo, konec + 1) if n % 2 == 0]\n"
        'print("Чётные числа:", chetnye)\n',
    )}
    {callout(
        "info",
        "Какие темы здесь встретились",
        "<code class=\"inline\">input()</code> и <code class=\"inline\">int()</code> — глава 8; "
        "<code class=\"inline\">%</code> — глава 5; <code class=\"inline\">if/else</code> — "
        "глава 9; генератор списков — глава 11.",
    )}

    {practice_card(
        "12-01",
        "Практика: чётное или нечётное",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/12-01/index.html",
    )}
    """
    page(
        "12-01-chetnoe-ili-nechetnoe.html",
        page_title="Проект: чётное или нечётное",
        description="Мини-проект: определяем чётность числа и находим все чётные числа в диапазоне.",
        kicker_suffix="Чётное или нечётное",
        h1="Проект: чётное или нечётное",
        lede="Первый проект главы закрепляет условия и оператор % из ранних глав — маленький, "
        "но с полным циклом «данные → алгоритм → код».",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 12-02 · Достаточно ли чаевых? (расширено шаблоном проекта)
# ---------------------------------------------------------------------------

def build_02() -> None:
    body = f"""
    {requirements_card(["input()", "float()", "арифметика", "if/elif/else", "f-строки"], "★ разминка", "текстовая программа")}

    <h2>Что создаём</h2>
    <p>Стандартные чаевые в ресторане — 15–20% от счёта. Проверим, укладывается ли конкретная
    сумма чаевых в этот диапазон.</p>
    {code_block(
        "chaevye.py",
        'schet = float(input("Сумма счёта: "))\n'
        'chaevye = float(input("Сумма чаевых: "))\n\n'
        "procent = (chaevye / schet) * 100\n\n"
        "if procent < 15:\n"
        '    print(f"Маловато — всего {procent:.1f}%. Обычно оставляют 15-20%.")\n'
        "elif procent <= 20:\n"
        '    print(f"В самый раз — {procent:.1f}%!")\n'
        "else:\n"
        '    print(f"Очень щедро — целых {procent:.1f}%!")\n',
    )}
    {terminal_transcript([
        "Сумма счёта: 40",
        "Сумма чаевых: 8",
        "В самый раз — 20.0%!",
    ], caption="Детерминированный пример выполнения")}

    {exercise(2, "Своя граница щедрости", "Добавьте четвёртую категорию — «сказочно щедро» — для чаевых больше 30%.")}

    {practice_card(
        "12-02",
        "Практика: вычисляем и оцениваем процент чаевых",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/12-02/index.html",
    )}
    """
    page(
        "12-02-chaevye.html",
        page_title="Проект: достаточно ли чаевых оставляет ваша мама?",
        description="Мини-проект: считаем процент чаевых от счёта и оцениваем его через elif.",
        kicker_suffix="Чаевые",
        h1="Проект: достаточно ли чаевых оставляет ваша мама?",
        lede="Считаем процент чаевых от суммы счёта и оцениваем щедрость через цепочку elif.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 12-09 · Угадай число, версия 3
# ---------------------------------------------------------------------------

def build_09() -> None:
    body = f"""
    {requirements_card(["random", "while", "if/elif/else", "input()/int()", "счётчик"], "★★ средний", "текстовая игра")}

    <h2>Что создаём</h2>
    <p>Финальная, отполированная версия игры-угадайки из глав 9-10 — с подсчётом попыток и
    аккуратным выводом.</p>
    {terminal_transcript([
        "Загадано число от 1 до 100. Попробуйте угадать!",
        "Ваша попытка: 50",
        "Слишком много!",
        "Ваша попытка: 25",
        "Слишком мало!",
        "Ваша попытка: 37",
        "Поздравляем! Загадано было 37. Попыток: 3",
    ], caption="Детерминированный пример выполнения")}

    <h2>Требования</h2>
    {comparison_table(
        ["Требование", "Как проверим"],
        [
            ["компьютер выбирает целое число от 1 до 100", "<code class=\"inline\">random.randint(1, 100)</code>"],
            ["игрок вводит попытки, пока не угадает", "<code class=\"inline\">while guess != secret</code>"],
            ["после каждой попытки — подсказка мало/много", "<code class=\"inline\">if/elif/else</code>"],
            ["попытки считаются", "<code class=\"inline\">attempts += 1</code>"],
            ["игра завершается на правильном ответе", "цикл заканчивается, печатается итог"],
        ],
    )}

    <h2>Алгоритм: внешний цикл</h2>
    {while_loop_flowchart(
        "secret = random, attempts = 0",
        "guess != secret",
        "спросить guess, сравнить, дать подсказку",
        "attempts += 1",
        caption="Пока не угадано — спросить попытку, сравнить, подсказать, увеличить счётчик",
    )}

    <h2>Алгоритм: что происходит внутри одной попытки</h2>
    {flowchart([
        {"kind": "input", "label": "guess = int(input(...))"},
        {"kind": "process", "label": "attempts += 1"},
        {
            "kind": "decision",
            "label": "guess == secret?",
            "yes": [{"kind": "output", "label": "Поздравляем! Попыток: attempts"}],
            "no": [
                {
                    "kind": "decision",
                    "label": "guess < secret?",
                    "yes": [{"kind": "output", "label": "Слишком мало!"}],
                    "no": [{"kind": "output", "label": "Слишком много!"}],
                }
            ],
        },
    ], caption="Одна попытка: сравнить и подсказать — весь этот блок повторяется циклом while сверху")}

    <h2>Трасса состояния</h2>
    {comparison_table(
        ["Попытка", "guess", "secret", "Результат"],
        [
            ["1", "50", "37", "слишком много"],
            ["2", "25", "37", "слишком мало"],
            ["3", "37", "37", "угадано, цикл завершается"],
        ],
    )}

    <h2>Финальный код</h2>
    {code_block(
        "ugadaj_chislo_v3.py",
        "import random\n\n"
        "secret = random.randint(1, 100)\n"
        "attempts = 0\n"
        "guess = None\n\n"
        'print("Загадано число от 1 до 100. Попробуйте угадать!")\n\n'
        "while guess != secret:\n"
        '    guess = int(input("Ваша попытка: "))\n'
        "    attempts += 1\n"
        "    if guess < secret:\n"
        '        print("Слишком мало!")\n'
        "    elif guess > secret:\n"
        '        print("Слишком много!")\n'
        "    else:\n"
        '        print(f"Поздравляем! Загадано было {secret}. Попыток: {attempts}")\n',
    )}
    {callout(
        "info",
        "В практике число фиксировано, а не случайно",
        "На странице показан настоящий <code class=\"inline\">random.randint(1, 100)</code> — "
        "именно так должна работать игра. В ноутбуке практики секретное число зафиксировано "
        "заранее, а ввод подставляется автоматически — иначе автоматическая проверка результата "
        "была бы недетерминированной.",
    )}

    <h2>[[icon:debug]] Debug Lab</h2>
    <p>Что произойдёт, если строку <code class="inline">attempts = 0</code> случайно перенести
    внутрь цикла <code class="inline">while</code>? Проверьте предположение, прежде чем читать
    дальше.</p>
    {callout(
        "warning",
        "attempts всегда будет равен 1",
        "Ровно та же ошибка, что и в §12.2 Debug Lab: счётчик, обнуляемый внутри цикла, "
        "никогда не накапливает значение — на каждой итерации он создаётся заново.",
    )}

    <h2>Уровень 3: ограничение попыток</h2>
    <p>Усложним требования: игра заканчивается поражением после 10 неудачных попыток.</p>
    {code_block(
        "ugadaj_chislo_limit.py",
        "max_attempts = 10\n\n"
        "while guess != secret and attempts < max_attempts:\n"
        "    ...\n\n"
        "if guess == secret:\n"
        '    print(f"Победа за {attempts} попыток!")\n'
        "else:\n"
        '    print(f"Числа закончились. Было загадано {secret}.")\n',
    )}

    {practice_card(
        "12-09",
        "Практика: угадай число, версия 3",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/12-09/index.html",
    )}
    {practice_card(
        "12-10",
        "Практика (★★★): ограничение числа попыток",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/12-10/index.html",
    )}
    """
    page(
        "12-09-ugadaj-chislo-v3.html",
        page_title="Проект: угадай число, версия 3",
        description="Финальная версия игры-угадайки: random, while, if/elif/else, счётчик попыток, полный алгоритм с блок-схемами и трассой состояния.",
        kicker_suffix="Угадай число v3",
        h1="Проект: угадай число, версия 3",
        lede="Полный цикл разработки на знакомой игре: требования → алгоритм → блок-схема → "
        "трасса состояния → код.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 12-11 · Анализатор текста и частота слов
# ---------------------------------------------------------------------------

def build_11() -> None:
    body = f"""
    {requirements_card(["strings", "циклы", "list", "set", "dict"], "★★★ интеграционный", "текстовый отчёт")}

    <h2>Что создаём</h2>
    <p>Программу, которая получает предложение и считает про него всё интересное: сколько
    символов, слов, уникальных слов и какое слово встречается чаще всего.</p>
    {terminal_transcript([
        "Введите текст: Python is great and python is fun",
        "Символов: 35",
        "Слов: 7",
        "Уникальных слов: 6",
        "Самое частое слово: 'is' — 2 раз(а)",
    ], caption="Детерминированный пример выполнения")}

    <h2>Конвейер обработки данных</h2>
    {flow_diagram([
        ("Исходный текст", "'Python python code'"),
        ("нормализация", ".lower()"),
        ("split()", "['python','python','code']"),
        ("set(...)", "{'python','code'}"),
    ], caption="Текст → нормализация → список слов → множество уникальных слов")}
    {callout(
        "tip",
        "Почему set()",
        "Множество естественно устраняет повторы (глава 11) — количество уникальных слов "
        "равно просто <code class=\"inline\">len(set(words))</code>, без единой ручной "
        "проверки.",
    )}

    <h2>Этап 1 — базовые подсчёты</h2>
    {code_block(
        "analizator_etap1.py",
        'text = input("Введите текст: ")\n\n'
        "words = text.split()\n\n"
        'print("Символов:", len(text))\n'
        'print("Слов:", len(words))\n',
    )}

    <h2>Этап 2 — уникальные слова</h2>
    {code_block(
        "analizator_etap2.py",
        "normalized = text.lower().split()\n"
        "unikalnye = set(normalized)\n\n"
        'print("Уникальных слов:", len(unikalnye))\n',
    )}
    {callout(
        "warning",
        "Без .lower() 'Python' и 'python' — разные слова",
        "Строки сравниваются посимвольно и с учётом регистра (глава 8) — "
        "<code class=\"inline\">\"Python\" != \"python\"</code>. Если забыть "
        "<code class=\"inline\">.lower()</code> перед подсчётом уникальных слов, они "
        "посчитаются как два разных слова.",
    )}

    <h2>Этап 3 — частота слов</h2>
    <p>Тот же алгоритм, что подробно разбирался в главе 11 (§11.24) — теперь как часть более
    крупной программы:</p>
    {code_block(
        "chastota_slov.py",
        "counts = {}\n"
        "for word in normalized:\n"
        "    counts[word] = counts.get(word, 0) + 1\n",
    )}
    {comparison_table(
        ["word", "старое значение", "новое значение"],
        [
            ["python", "0 (get вернул 0)", "1"],
            ["is", "0", "1"],
            ["great", "0", "1"],
            ["and", "0", "1"],
            ["python", "1", "2"],
            ["is", "1", "2"],
        ],
    )}

    <h2>Находим самое частое слово</h2>
    {code_block(
        "samoe_chastoe.py",
        "samoe_chastoe = max(counts, key=counts.get)\n"
        'print(f"Самое частое слово: {samoe_chastoe!r} — {counts[samoe_chastoe]} раз(а)")\n',
    )}
    {callout(
        "info",
        "max() с key — не только для чисел",
        "<code class=\"inline\">max(counts, key=counts.get)</code> перебирает КЛЮЧИ словаря "
        "(глава 11) и выбирает тот, для которого <code class=\"inline\">counts.get(ключ)</code> "
        "максимален — компактный способ найти «самое частое» без ручного цикла со сравнением.",
    )}

    <h2>Финальный код</h2>
    {code_block(
        "analizator_teksta.py",
        'text = input("Введите текст: ")\n'
        "normalized = text.lower().split()\n\n"
        "unikalnye = set(normalized)\n\n"
        "counts = {}\n"
        "for word in normalized:\n"
        "    counts[word] = counts.get(word, 0) + 1\n"
        "samoe_chastoe = max(counts, key=counts.get)\n\n"
        'print("Символов:", len(text))\n'
        'print("Слов:", len(normalized))\n'
        'print("Уникальных слов:", len(unikalnye))\n'
        'print(f"Самое частое слово: {samoe_chastoe!r} — {counts[samoe_chastoe]} раз(а)")\n',
    )}

    <h2>[[icon:debug]] Debug Lab</h2>
    <p>Если посчитать <code class="inline">len(unikalnye)</code> из слов БЕЗ
    <code class="inline">.lower()</code>, а частоту слов — уже ПОСЛЕ приведения к нижнему
    регистру, эти два числа могут не biться друг с другом. Почему?</p>
    {callout(
        "warning",
        "Используйте один и тот же нормализованный список везде",
        "Если <code class=\"inline\">unikalnye</code> считается из необработанных слов, а "
        "<code class=\"inline\">counts</code> — из <code class=\"inline\">normalized</code>, то "
        "«Python» и «python» попадут в <code class=\"inline\">unikalnye</code> как два разных "
        "слова, а в <code class=\"inline\">counts</code> — как одно. Всегда считайте от одного и "
        "того же, уже нормализованного, списка.",
    )}

    {practice_card(
        "12-11",
        "Практика: анализатор текста — символы, слова, уникальные слова",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/12-11/index.html",
    )}
    {practice_card(
        "12-12",
        "Практика: частота слов и самое частое слово",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/12-12/index.html",
    )}
    """
    page(
        "12-11-analizator-teksta.html",
        page_title="Проект: анализатор текста и частота слов",
        description="Интеграционный проект: строки, циклы, множества и словари вместе — анализ текста, уникальные слова и частота слов.",
        kicker_suffix="Анализатор текста",
        h1="Проект: анализатор текста и частота слов",
        lede="Строки, циклы, множества и словари — впервые вместе, в одной программе, которая "
        "рассказывает о тексте больше, чем видно на первый взгляд.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 12-13 · Записная книжка
# ---------------------------------------------------------------------------

def build_13() -> None:
    body = f"""
    {requirements_card(["dict", "if/elif", "циклы", "f-строки"], "★★ средний", "текстовое меню")}

    <h2>Что создаём</h2>
    <p>Записную книжку контактов в памяти программы: показать все контакты, добавить, найти,
    изменить, удалить.</p>

    <h2>Модель данных</h2>
    {tree_diagram(
        ("contacts (dict)", [
            ("\"Anna\" → \"+48 111 111 111\"", []),
            ("\"Bob\" → \"+48 222 222 222\"", []),
        ]),
        caption="Ключ — имя, значение — телефон. Почему dict? Потому что ищем контакт по имени, а не по позиции",
    )}
    {callout(
        "info",
        "Почему словарь, а не список",
        "Список пришлось бы перебирать целиком в поисках нужного имени. Словарь сразу даёт "
        "доступ по ключу (глава 11) — <code class=\"inline\">contacts[\"Anna\"]</code>, без "
        "перебора.",
    )}

    <h2>Действия</h2>
    {code_block(
        "zapisnaya_knizhka.py",
        "contacts = {\n"
        '    "Anna": "+48 111 111 111",\n'
        '    "Bob": "+48 222 222 222",\n'
        "}\n\n"
        "# показать все контакты\n"
        "for name, phone in contacts.items():\n"
        '    print(f"{name}: {phone}")\n\n'
        "# добавить контакт\n"
        'contacts["Maria"] = "+48 333 333 333"\n\n'
        "# найти контакт\n"
        'zapros = "Anna"\n'
        "if zapros in contacts:\n"
        '    print(f"Найдено: {contacts[zapros]}")\n'
        "else:\n"
        '    print("Контакт не найден")\n\n'
        "# изменить контакт\n"
        'contacts["Anna"] = "+48 111 000 000"\n\n'
        "# удалить контакт\n"
        'del contacts["Bob"]\n\n'
        'print("Контактов осталось:", len(contacts))\n',
    )}

    <h2>Уровень 2: интерактивное меню</h2>
    <p>То же самое, но управляется командами вместо жёстко прописанной последовательности
    действий — предвестник консоли команд из §12.10:</p>
    {code_block(
        "zapisnaya_knizhka_menu.py",
        "contacts = {}\n\n"
        "while True:\n"
        '    command = input("Команда (add/show/exit): ").strip().lower()\n'
        "    if command == \"exit\":\n"
        "        break\n"
        "    elif command == \"add\":\n"
        '        name = input("Имя: ")\n'
        '        phone = input("Телефон: ")\n'
        "        contacts[name] = phone\n"
        "    elif command == \"show\":\n"
        "        for name, phone in contacts.items():\n"
        '            print(f"{name}: {phone}")\n',
    )}
    {callout(
        "warning",
        "Когда программа завершится, contacts исчезнет",
        "<code class=\"inline\">contacts</code> живёт только в памяти, пока работает программа "
        "— это обычная переменная (глава 3). Чтобы данные сохранялись между запусками, "
        "понадобятся файлы — тема одной из следующих глав.",
    )}

    <h2>[[icon:launch]] Чуть глубже — контакт с несколькими полями</h2>
    <p>Если контакту нужно больше одного значения (телефон И email), внешний словарь может
    хранить вложенные словари (глава 11, §11.19):</p>
    {code_block(
        "zapisnaya_knizhka_vlozhennaya.py",
        "contacts = {\n"
        '    "Anna": {"phone": "+48 111 111 111", "email": "anna@example.com"},\n'
        "}\n"
        'print(contacts["Anna"]["email"])\n',
    )}

    <h2>[[icon:debug]] Debug Lab</h2>
    {code_block(
        "debug_lab_contacts.py",
        'contacts = {"Anna": "+48 111 111 111"}\n'
        'print("+48 111 111 111" in contacts)   # False!\n',
    )}
    {callout(
        "warning",
        "in у словаря проверяет ключи, а не значения",
        "Та же ловушка из главы 11 (§11.19): <code class=\"inline\">in</code> ищет среди "
        "КЛЮЧЕЙ. Чтобы проверить, есть ли такой телефон среди значений, нужно "
        "<code class=\"inline\">\"+48 111 111 111\" in contacts.values()</code>.",
    )}

    {practice_card(
        "12-13",
        "Практика: записная книжка — добавить, найти, изменить, удалить",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/12-13/index.html",
    )}
    """
    page(
        "12-13-zapisnaya-knizhka.html",
        page_title="Проект: записная книжка",
        description="Записная книжка контактов на словаре: показать, добавить, найти, изменить, удалить. Почему dict, а не list.",
        kicker_suffix="Записная книжка",
        h1="Проект: записная книжка",
        lede="Словарь как естественное хранилище «имя → телефон» — и первый взгляд на "
        "интерактивное меню, управляемое командами.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 12-14 · Журнал оценок и корзина покупок
# ---------------------------------------------------------------------------

def build_14() -> None:
    body = f"""
    {requirements_card(["list", "dict", "циклы", "накопитель"], "★★★ интеграционный", "отчёт / чек")}

    <p>Два проекта на одной странице специально: у обоих одна и та же модель данных — "
    <strong>список словарей</strong> — и один и тот же приём — <strong>накопитель</strong>
    (глава 10), только применённый по-разному.</p>

    <h2 id="zhurnal-ocenok">Проект: журнал оценок</h2>
    {tree_diagram(
        ("students (список)", [
            ("[0]", [("name → \"Anna\"", []), ("score → 95", [])]),
            ("[1]", [("name → \"Bob\"", []), ("score → 82", [])]),
        ]),
        caption="Список словарей — почему list? Потому что ученики образуют упорядоченную последовательность записей",
    )}
    {code_block(
        "zhurnal_ocenok.py",
        "students = [\n"
        '    {"name": "Anna", "score": 95},\n'
        '    {"name": "Bob", "score": 82},\n'
        '    {"name": "Maria", "score": 91},\n'
        '    {"name": "Leo", "score": 58},\n'
        "]\n\n"
        "for student in students:\n"
        '    print(f"{student[\'name\']}: {student[\'score\']}")\n\n'
        "scores = [student[\"score\"] for student in students]\n"
        "average = sum(scores) / len(scores)\n"
        'print(f"Средний балл: {average:.1f}")\n'
        'print("Максимум:", max(scores))\n'
        'print("Минимум:", min(scores))\n\n'
        "otlichniki = [s for s in students if s[\"score\"] >= 90]\n"
        'print("Отличников:", len(otlichniki))\n',
    )}
    {callout(
        "info",
        "Классификация через if/elif",
        "Если нужна не просто фильтрация, а оценка «отлично/хорошо/пересдача», к каждому "
        "студенту можно применить цепочку <code class=\"inline\">if/elif/else</code> из главы 9 "
        "— это не про реальные школьные критерии, а про тренировку алгоритма классификации.",
    )}

    <h2 id="korzina-pokupok">Проект: корзина покупок</h2>
    {flow_diagram([
        ("товар", "цена × количество"),
        ("сумма по строке", "line total"),
        ("накопитель", "cart total"),
    ], caption="Каждый товар даёт свою сумму, накопитель складывает их все вместе")}
    {code_block(
        "korzina_pokupok.py",
        "cart = [\n"
        '    {"name": "Молоко", "price": 4.50, "qty": 2},\n'
        '    {"name": "Хлеб", "price": 2.20, "qty": 1},\n'
        '    {"name": "Сыр", "price": 9.90, "qty": 1},\n'
        "]\n\n"
        "total = 0\n"
        "for item in cart:\n"
        "    line_total = item[\"price\"] * item[\"qty\"]\n"
        "    total += line_total\n"
        '    print(f"{item[\'name\']:<10} {item[\'qty\']} x {item[\'price\']:.2f} = {line_total:.2f}")\n\n'
        'print(f"Итого: {total:.2f}")\n',
    )}
    {terminal_transcript([
        "Молоко     2 x 4.50 = 9.00",
        "Хлеб       1 x 2.20 = 2.20",
        "Сыр        1 x 9.90 = 9.90",
        "Итого: 21.10",
    ], caption="Чек — детерминированный пример выполнения")}
    {callout(
        "info",
        "Это учебная арифметика, не Decimal",
        "Для настоящих денежных расчётов используют более точные типы (например "
        "<code class=\"inline\">decimal.Decimal</code>), чтобы избежать неточностей float "
        "(глава 5). Здесь используется обычная арифметика — целей главы 12 это не меняет: "
        "фокус на структуре программы, а не на денежной точности.",
    )}

    <h2>[[icon:debug]] Debug Lab</h2>
    <p>Почему в этом коде <code class="inline">total</code> в конце равен сумме только
    ПОСЛЕДНЕГО товара?</p>
    {code_block(
        "debug_lab_korzina.py",
        "for item in cart:\n"
        "    total = 0\n"
        "    total += item[\"price\"] * item[\"qty\"]\n",
    )}
    {callout(
        "warning",
        "Накопитель обнуляется внутри цикла",
        "Та же ошибка, что уже встречалась в §12.5 и §12.6: <code class=\"inline\">total = 0</code> "
        "стоит внутри тела цикла, поэтому пересоздаётся на каждой итерации. Инициализация "
        "накопителя должна быть ОДИН раз, до цикла.",
    )}

    {practice_card(
        "12-14",
        "Практика: журнал оценок — среднее, максимум, минимум, отличники",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/12-14/index.html",
    )}
    {practice_card(
        "12-15",
        "Практика: корзина покупок — чек и итоговая сумма",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/12-15/index.html",
    )}
    """
    page(
        "12-14-zhurnal-i-korzina.html",
        page_title="Проекты: журнал оценок и корзина покупок",
        description="Два проекта на одной модели данных (список словарей): журнал оценок с накопителем среднего/максимума и корзина покупок с расчётом чека.",
        kicker_suffix="Журнал и корзина",
        h1="Проекты: журнал оценок и корзина покупок",
        lede="Одна и та же модель данных — список словарей — и один и тот же приём — "
        "накопитель, применённый в двух разных задачах.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 12-16 · Викторина (данные vs алгоритм, рефакторинг)
# ---------------------------------------------------------------------------

def build_16() -> None:
    body = f"""
    {requirements_card(["list", "dict", "for", "input", "if", "счётчик"], "★★★★ challenge", "текстовая викторина")}

    <h2>Что создаём</h2>
    <p>Викторину из нескольких вопросов: программа задаёт вопрос, принимает ответ, сравнивает
    его с правильным, считает счёт и в конце показывает результат.</p>
    {terminal_transcript([
        "Вопрос 1: Столица Франции?",
        "Ваш ответ: paris",
        "[[icon:success]] Верно!",
        "Вопрос 2: 7 * 8?",
        "Ваш ответ: 54",
        "[[icon:error]] Неверно. Правильный ответ: 56",
        "Счёт: 1 из 2",
    ], caption="Детерминированный пример выполнения")}

    <h2 id="dannye-vs-algoritm">Данные vs алгоритм — главный урок этого проекта</h2>
    <p>Есть соблазн написать викторину так:</p>
    {classic_vs_modern(
        "Три вопроса: захардкоженная логика → данные + цикл",
        "Вопросы «зашиты» в код",
        'question1 = "Столица Франции?"\n'
        'answer1 = "paris"\n'
        'user1 = input(question1 + " ").strip().lower()\n'
        "if user1 == answer1:\n"
        "    score += 1\n\n"
        'question2 = "7 * 8?"\n'
        'answer2 = "56"\n'
        'user2 = input(question2 + " ").strip().lower()\n'
        "if user2 == answer2:\n"
        "    score += 1\n\n"
        "# ...и так для каждого следующего вопроса",
        "Вопросы — данные, алгоритм один",
        "questions = [\n"
        '    {"question": "Столица Франции?", "answer": "paris"},\n'
        '    {"question": "7 * 8?", "answer": "56"},\n'
        "]\n\n"
        "score = 0\n"
        "for q in questions:\n"
        '    user_answer = input(q["question"] + " ").strip().lower()\n'
        "    if user_answer == q[\"answer\"]:\n"
        "        score += 1",
        "хранить вопросы как ДАННЫЕ (список словарей), а не как повторяющийся код. Если "
        "вопросов станет 20 вместо 2, левый вариант пришлось бы переписывать заново, а правый "
        "— просто дополнить список. <strong>Алгоритм не меняется, когда меняются данные</strong> "
        "— в этом суть <em>data-driven programming</em>.",
    )}
    {callout(
        "tip",
        "Рефакторинг",
        "Переход от левого варианта к правому называется <strong>рефакторингом</strong> — мы "
        "улучшаем внутреннюю структуру программы, не меняя то, что она должна делать. Программа "
        "с двумя вопросами ведёт себя одинаково в обеих версиях — правая просто лучше "
        "устроена и легче расширяется.",
    )}

    <h2>Алгоритм</h2>
    {for_loop_flowchart(
        "questions",
        "question",
        "спросить, сравнить, посчитать",
        caption="for question in questions — один и тот же алгоритм для любого числа вопросов",
    )}
    {flowchart([
        {"kind": "output", "label": "показать question['question']"},
        {"kind": "input", "label": "user_answer = input()"},
        {"kind": "process", "label": "нормализовать: .strip().lower()"},
        {
            "kind": "decision",
            "label": "user_answer == question['answer']?",
            "yes": [{"kind": "process", "label": "score += 1"}],
            "no": [{"kind": "output", "label": "показать правильный ответ"}],
        },
    ], caption="Одна итерация цикла — этот блок повторяется for-циклом сверху, для каждого вопроса")}

    <h2>Финальный код</h2>
    {code_block(
        "viktorina.py",
        "questions = [\n"
        '    {"question": "Столица Франции?", "answer": "paris"},\n'
        '    {"question": "7 * 8?", "answer": "56"},\n'
        '    {"question": "Язык, который мы изучаем?", "answer": "python"},\n'
        "]\n\n"
        "score = 0\n"
        "for q in questions:\n"
        '    user_answer = input(q["question"] + " ").strip().lower()\n'
        "    if user_answer == q[\"answer\"]:\n"
        '        print("✅ Верно!")\n'
        "        score += 1\n"
        "    else:\n"
        '        print(f"❌ Неверно. Правильный ответ: {q[\'answer\']}")\n\n'
        'print(f"Счёт: {score} из {len(questions)}")\n',
    )}

    <h2>Уровень 4: процент правильных ответов</h2>
    {code_block(
        "viktorina_procent.py",
        "procent = score / len(questions) * 100\n"
        'print(f"Результат: {procent:.0f}%")\n',
    )}

    <h2>[[icon:debug]] Debug Lab</h2>
    <p>Что произойдёт, если убрать <code class="inline">.strip().lower()</code> при нормализации
    ответа?</p>
    {callout(
        "warning",
        "«Paris» и «paris» — разные строки",
        "Без нормализации регистр и лишние пробелы делают правильный ответ «неверным» — та же "
        "чувствительность строк к регистру и пробелам, что и в главе 8. Всегда нормализуйте "
        "пользовательский ввод перед сравнением.",
    )}

    {practice_card(
        "12-16",
        "Практика: викторина из списка вопросов",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/12-16/index.html",
    )}
    {practice_card(
        "12-17",
        "Практика (★★★★): процент правильных ответов",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/12-17/index.html",
    )}
    """
    page(
        "12-16-viktorina.html",
        page_title="Проект: викторина",
        description="Викторина из списка вопросов: данные vs алгоритм, рефакторинг от захардкоженной логики к данным + циклу, счётчик и процент правильных ответов.",
        kicker_suffix="Викторина",
        h1="Проект: викторина",
        lede="Самый важный архитектурный урок главы: вопросы — это данные, а не код, и "
        "алгоритм не должен меняться, когда меняются данные.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 12-18 · Консоль команд и проверка пароля
# ---------------------------------------------------------------------------

def build_18() -> None:
    body = f"""
    {requirements_card(["while True", "if/elif/else", "break", "strings", "bool"], "★★★ интеграционный", "текстовая консоль / проверка")}

    <h2 id="konsol-komand">Проект: консоль команд</h2>
    <p>Простое текстовое приложение с командами: <code class="inline">help</code>,
    <code class="inline">hello</code>, <code class="inline">status</code>,
    <code class="inline">exit</code>. Этот паттерн — «бесконечный цикл, читающий команды» —
    встречается в меню, консолях, ботах, играх и утилитах командной строки.</p>
    {flowchart([
        {"kind": "output", "label": "показать список команд"},
        {"kind": "input", "label": "command = input()"},
        {"kind": "process", "label": "нормализовать: .strip().lower()"},
        {
            "kind": "decision",
            "label": "command == 'exit'?",
            "yes": [{"kind": "end", "label": "завершить программу"}],
            "no": [
                {
                    "kind": "decision",
                    "label": "известная команда?",
                    "yes": [{"kind": "output", "label": "выполнить help / hello / status"}],
                    "no": [{"kind": "output", "label": "«неизвестная команда»"}],
                }
            ],
        },
    ], caption="Пока не exit — прочитать команду, распознать её, выполнить, повторить")}
    {code_block(
        "konsol_komand.py",
        "history = []\n\n"
        "while True:\n"
        '    command = input("> ").strip().lower()\n'
        "    history.append(command)\n\n"
        '    if command == "exit":\n'
        '        print("До встречи!")\n'
        "        break\n"
        '    elif command == "help":\n'
        '        print("Команды: help, hello, status, exit")\n'
        '    elif command == "hello":\n'
        '        print("Привет!")\n'
        '    elif command == "status":\n'
        '        print(f"Команд выполнено: {len(history)}")\n'
        "    else:\n"
        '        print(f"Неизвестная команда: {command}")\n',
    )}
    {terminal_transcript([
        "> help",
        "Команды: help, hello, status, exit",
        "> hello",
        "Привет!",
        "> exit",
        "До встречи!",
    ], caption="Детерминированный пример выполнения")}
    {callout(
        "tip",
        "history — обычный список",
        "<code class=\"inline\">history</code> копит все введённые команды в порядке "
        "поступления — ровно то, для чего создан список (глава 11): упорядоченная, изменяемая "
        "коллекция.",
    )}

    <h2 id="validator-parolya">Проект: проверка имени пользователя / пароля</h2>
    {callout(
        "warning",
        "Это учебное упражнение по строкам, а не защита данных",
        "Ниже — тренировка работы со строками и булевыми флагами, а НЕ полноценная политика "
        "безопасности паролей. Настоящая защита учётных записей требует значительно большего "
        "(хеширование, соль, менеджеры паролей, лимиты попыток) — тем этого курса пока не "
        "касаемся.",
    )}
    <p>Правила (учебные): минимум 8 символов, есть хотя бы одна цифра, есть хотя бы одна буква,
    нет пробелов.</p>
    {flow_diagram([
        ("символ", "по одному"),
        ("cifra? / bukva? / probel?", "проверка"),
        ("обновить флаги", "has_digit / has_letter / has_space"),
    ], caption="Перебираем строку посимвольно, накапливая три булевых флага")}
    {code_block(
        "validator_parolya.py",
        'password = input("Придумайте пароль: ")\n\n'
        "has_digit = False\n"
        "has_letter = False\n"
        "has_space = False\n\n"
        "for ch in password:\n"
        "    if ch.isdigit():\n"
        "        has_digit = True\n"
        "    elif ch.isalpha():\n"
        "        has_letter = True\n"
        "    elif ch == \" \":\n"
        "        has_space = True\n\n"
        "dlinnyj_dostatochno = len(password) >= 8\n\n"
        "if dlinnyj_dostatochno and has_digit and has_letter and not has_space:\n"
        '    print("Пароль подходит под учебные правила.")\n'
        "else:\n"
        '    print("Пароль не подходит:")\n'
        "    if not dlinnyj_dostatochno:\n"
        '        print("- слишком короткий (нужно 8+ символов)")\n'
        "    if not has_digit:\n"
        '        print("- нет ни одной цифры")\n'
        "    if not has_letter:\n"
        '        print("- нет ни одной буквы")\n'
        "    if has_space:\n"
        '        print("- содержит пробел")\n',
    )}
    {callout(
        "info",
        "Накопление состояния через булевы флаги",
        "<code class=\"inline\">has_digit</code>, <code class=\"inline\">has_letter</code> и "
        "<code class=\"inline\">has_space</code> — это накопители (глава 10), только "
        "булевы: каждый символ может ПЕРЕКЛЮЧИТЬ флаг в <code class=\"inline\">True</code>, "
        "и он остаётся <code class=\"inline\">True</code> до конца перебора.",
    )}

    <h2>[[icon:debug]] Debug Lab</h2>
    <p>Если использовать <code class="inline">elif</code> вместо трёх отдельных
    <code class="inline">if</code> при проверке символа — некоторые символы могут обрабатываться
    неправильно. Например, что если правило было бы «есть спецсимвол»?</p>
    {callout(
        "warning",
        "elif проверяет только одну ветку на символ",
        "Пока правила взаимоисключающие (цифра/буква/пробел — символ не может быть сразу двумя "
        "из них), <code class=\"inline\">elif</code> работает верно. Но если добавить проверку "
        "ещё одного, НЕ взаимоисключающего свойства (например, «является заглавной буквой»), "
        "её нужно проверять отдельным <code class=\"inline\">if</code>, а не веткой в той же "
        "цепочке <code class=\"inline\">elif</code>.",
    )}

    {practice_card(
        "12-18",
        "Практика: консоль команд с историей",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/12-18/index.html",
    )}
    {practice_card(
        "12-19",
        "Практика: проверка пароля по учебным правилам",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/12-19/index.html",
    )}
    """
    page(
        "12-18-konsol-i-validator.html",
        page_title="Проекты: консоль команд и проверка пароля",
        description="Консоль команд (while True + if/elif/else + break) и учебная проверка пароля через накопление булевых флагов посимвольно.",
        kicker_suffix="Консоль и валидатор",
        h1="Проекты: консоль команд и проверка пароля",
        lede="Два способа читать пользовательский ввод в цикле: команда за командой и символ "
        "за символом, накапливая состояние.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 12-20 · Студия многоугольников
# ---------------------------------------------------------------------------

def build_20() -> None:
    body = f"""
    {requirements_card(["Turtle", "input()/int()", "for", "формула"], "★★★ интеграционный", "геометрическая фигура")}

    <h2>Что создаём</h2>
    <p>Программу, которая рисует ЛЮБОЙ правильный многоугольник — не переписывая код, а меняя
    одно число.</p>

    <h2>Формула</h2>
    <p>Правильный многоугольник с <code class="inline">storony</code> сторонами всегда
    поворачивает на один и тот же угол между сторонами:</p>
    {code_block("formula_ugla.py", "ugol = 360 / storony\n")}
    {comparison_table(
        ["storony", "ugol"],
        [["3", "120°"], ["4", "90°"], ["5", "72°"], ["6", "60°"], ["8", "45°"]],
    )}

    <h2>Один алгоритм — пять результатов</h2>
    {turtle_output(
        "12-polygon-5",
        "studiya_mnogougolnikov.py",
        caption="storony = 5 → правильный пятиугольник",
        alt="Правильный пятиугольник, нарисованный Turtle",
    )}
    {code_block(
        "studiya_mnogougolnikov.py",
        'storony = int(input("Сколько сторон? "))\n'
        "dlina = 300 / storony\n"
        "ugol = 360 / storony\n\n"
        "for _ in range(storony):\n"
        "    artist.forward(dlina)\n"
        "    artist.right(ugol)\n",
    )}
    {callout(
        "tip",
        "Данные меняются — алгоритм нет",
        "Та же идея, что и в проекте «Викторина» (§12.9): цикл <code class=\"inline\">for _ in "
        "range(storony)</code> и формула <code class=\"inline\">ugol = 360 / storony</code> "
        "не меняются — меняется только введённое число.",
    )}
    {image_gallery(
        [
            ("12-polygon-3", "storony = 3"),
            ("12-polygon-4", "storony = 4"),
            ("12-polygon-5", "storony = 5"),
            ("12-polygon-6", "storony = 6"),
            ("12-polygon-8", "storony = 8"),
        ],
        caption="Один и тот же код, разное значение storony — реально сгенерированные результаты",
    )}

    <h2>[[icon:debug]] Debug Lab</h2>
    <p>Что произойдёт, если ввести <code class="inline">storony = 1</code> или
    <code class="inline">storony = 2</code>?</p>
    {callout(
        "warning",
        "Формула работает только для storony >= 3",
        "Многоугольника с одной или двумя сторонами не существует геометрически — код не "
        "упадёт с ошибкой (<code class=\"inline\">360 / 1 = 360</code>), но нарисует не то, что "
        "ожидалось. Полноценная защита от такого ввода потребует проверки "
        "<code class=\"inline\">if storony < 3</code> перед рисованием.",
    )}

    {practice_card(
        "12-20",
        "Практика: вычисляем угол поворота для многоугольника",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/12-20/index.html",
    )}
    {local_required_card(
        "12-21",
        "Практика: рисуем многоугольник по введённому числу сторон",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/12-21/index.html",
    )}
    """
    page(
        "12-20-studiya-mnogougolnikov.html",
        page_title="Проект: студия многоугольников",
        description="Параметризованный многоугольник в Turtle: одна формула (360/storony), любое число сторон, реально сгенерированные результаты для 3-8 сторон.",
        kicker_suffix="Студия многоугольников",
        h1="Проект: студия многоугольников",
        lede="Одна и та же формула и один и тот же цикл рисуют треугольник, квадрат, "
        "пятиугольник, шестиугольник или восьмиугольник — в зависимости от одного числа.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 12-03 · Рождественская ёлка (расширено: реальный вывод)
# ---------------------------------------------------------------------------

def build_03() -> None:
    body = f"""
    {requirements_card(["Turtle", "for", "begin_fill/end_fill"], "★★ средний", "графика Turtle")}

    <h2>Что создаём</h2>
    <p>Нарисуем ёлку из треугольных «ярусов» уменьшающегося размера — используя цикл и фигуры
    из главы 6.</p>
    {turtle_output(
        "12-elka",
        "elka.py",
        caption="Четыре яруса уменьшающегося размера + ствол",
        alt="Рождественская ёлка, нарисованная Turtle из уменьшающихся треугольных ярусов",
    )}
    {callout(
        "tip",
        "Каждый ярус — тот же треугольник, что и в главе 6",
        "Формула угла поворота (<code class=\"inline\">360 / 3 = 120</code>) — та же самая, что "
        "и для любого правильного многоугольника из главы 6 (и из проекта «Студия "
        "многоугольников», §12.11). Ёлка — это просто несколько треугольников уменьшающегося "
        "размера, нарисованных друг под другом в цикле.",
    )}

    {local_required_card(
        "12-03",
        "Практика: рисуем ёлку",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/12-03/index.html",
    )}
    """
    page(
        "12-03-elka.html",
        page_title="Проект: рождественская ёлка",
        description="Мини-проект: рисуем ёлку из уменьшающихся треугольных ярусов с помощью Turtle и цикла.",
        kicker_suffix="Ёлка",
        h1="Проект: рождественская ёлка",
        lede="Несколько треугольных ярусов уменьшающегося размера, нарисованных циклом.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 12-04 · Спирали! (расширено: реальный вывод для всех пяти вариаций)
# ---------------------------------------------------------------------------

def build_04() -> None:
    body = f"""
    {requirements_card(["Turtle", "for", "random (одна из версий)"], "★★★ интеграционный", "графика Turtle · генеративное искусство")}

    <h2>Что создаём</h2>
    <p>Пять вариаций одной идеи — фигура, каждый шаг которой немного больше предыдущего. Один
    принцип из главы 10 («шаг + поворот + увеличение переменной»), пять углов поворота.</p>

    <h2>Квадратная спираль</h2>
    {turtle_output("12-spiral-square", "kvadratnaya_spiral.py", caption="right(90) на каждом шаге", alt="Квадратная спираль Turtle")}

    <h2>Случайная спираль</h2>
    {turtle_output("12-spiral-random", "sluchaynaya_spiral.py", caption="Угол «дрожит» случайно в диапазоне 80-100°", alt="Спираль со случайно дрожащим углом поворота")}

    <h2>Треугольная спираль</h2>
    {turtle_output("12-spiral-triangle", "treugolnaya_spiral.py", caption="right(120) на каждом шаге", alt="Треугольная спираль Turtle")}

    <h2>Звёздная спираль</h2>
    {turtle_output("12-spiral-star", "zvezdnaya_spiral.py", caption="right(144) — угол пятиконечной звезды", alt="Звёздная спираль Turtle")}

    <h2>Круговая спираль</h2>
    {turtle_output("12-spiral-circle", "krugovaya_spiral.py", caption="circle(radius, 90) с растущим радиусом", alt="Круговая спираль из дуг Turtle")}

    {callout(
        "info",
        "Один общий принцип",
        "Все пять спиралей — одна и та же идея из главы 10 («шаг + поворот + увеличение "
        "переменной») с разным углом поворота. Освоив один вариант, вы фактически освоили все "
        "пять.",
    )}

    {local_required_card(
        "12-04",
        "Практика: спирали",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/12-04/index.html",
    )}
    """
    page(
        "12-04-spirali.html",
        page_title="Проект: спирали!",
        description="Пять вариаций спирали: квадратная, случайная, треугольная, звёздная и круговая — реально сгенерированные результаты.",
        kicker_suffix="Спирали",
        h1="Проект: спирали!",
        lede="Один и тот же принцип — пять разных узоров, в зависимости от угла поворота.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 12-05 · Сложная мандала (расширено: реальный вывод)
# ---------------------------------------------------------------------------

def build_05() -> None:
    body = f"""
    {requirements_card(["Turtle", "for", "random.choice"], "★★★★ challenge", "графика Turtle · генеративное искусство")}

    <h2>Что создаём</h2>
    <p>Финальная эволюция мандалы из глав 6 и 10 — добавим случайный цвет на каждый луч и
    сделаем полностью автоматической, без единого «магического числа», прописанного вручную.</p>

    <h2>Как строится узор: от одного луча к полной мандале</h2>
    <p>Тот же принцип поэтапного построения, что и в главе 10: сначала один элемент, потом
    несколько, потом полный узор.</p>
    {code_block(
        "odin_luch.py",
        "artist.circle(20)\n"
        "artist.forward(150)\n"
        "artist.forward(-150)\n",
    )}
    {turtle_output(
        "12-mandala-slozhnaya",
        "slozhnaya_mandala.py",
        caption="36 лучей, случайный цвет на каждом (seed зафиксирован для документации)",
        alt="Сложная мандала Turtle из 36 лучей случайных цветов с кругами на концах",
    )}
    {code_block(
        "slozhnaya_mandala.py",
        "import random\n\n"
        "luchi = 36\n"
        "shag_ugla = 360 / luchi\n"
        "cveta = [\"red\", \"orange\", \"purple\", \"blue\", \"green\"]\n\n"
        "for i in range(luchi):\n"
        "    artist.pencolor(random.choice(cveta))\n"
        "    artist.setheading(i * shag_ugla)\n"
        "    artist.forward(150)\n"
        "    artist.circle(20)\n"
        "    artist.forward(-150)\n",
    )}
    {callout(
        "tip",
        "luchi определяет всё остальное",
        "Измените только <code class=\"inline\">luchi</code> — угол шага, число повторов "
        "цикла и даже плотность узора пересчитаются автоматически, ничего больше менять не "
        "нужно. Это и называется «полностью автоматизировано».",
    )}

    {local_required_card(
        "12-05",
        "Практика: сложная мандала со случайными цветами",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/12-05/index.html",
    )}
    """
    page(
        "12-05-slozhnaya-mandala.html",
        page_title="Проект: сложная мандала — полностью автоматизированная",
        description="Финальная версия мандалы: случайные цвета, круги на концах лучей, полностью управляется одной переменной. Реально сгенерированный результат.",
        kicker_suffix="Сложная мандала",
        h1="Проект: сложная мандала — полностью автоматизированная",
        lede="Финальная версия мандалы из глав 6 и 10 — со случайными цветами и кругами на "
        "концах лучей.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 12-22 · Пиксельная графика по сетке
# ---------------------------------------------------------------------------

def build_22() -> None:
    body = f"""
    {requirements_card(["nested list", "nested for", "Turtle"], "★★★★ challenge", "пиксельная графика")}

    <h2>Что создаём</h2>
    <p>Мост между данными и графикой: матрица из нулей и единиц — и программа, которая рисует
    по ней картинку. <code class="inline">0</code> — пусто, <code class="inline">1</code> —
    закрашенный квадрат.</p>
    {matrix_diagram(
        [["0", "1", "0", "1", "0"], ["1", "1", "1", "1", "1"], ["1", "1", "1", "1", "1"], ["0", "1", "1", "1", "0"], ["0", "0", "1", "0", "0"]],
        row_labels=["0", "1", "2", "3", "4"],
        col_labels=["0", "1", "2", "3", "4"],
        caption="picture — вложенный список: 0 = пусто, 1 = закрашенный квадрат",
    )}
    {turtle_output(
        "12-grid-art-heart",
        "setka_piksel_art.py",
        caption="Та же матрица, нарисованная вложенным циклом",
        alt="Сердце из закрашенных квадратов, нарисованное по матрице нулей и единиц",
    )}

    <h2>Алгоритм</h2>
    {code_block(
        "setka_piksel_art.py",
        "picture = [\n"
        "    [0, 1, 0, 1, 0],\n"
        "    [1, 1, 1, 1, 1],\n"
        "    [1, 1, 1, 1, 1],\n"
        "    [0, 1, 1, 1, 0],\n"
        "    [0, 0, 1, 0, 0],\n"
        "]\n\n"
        "razmer = 40\n"
        "for row_index, row in enumerate(picture):\n"
        "    for col_index, value in enumerate(row):\n"
        "        if value == 1:\n"
        "            x = -100 + col_index * razmer\n"
        "            y = 100 - row_index * razmer\n"
        "            artist.goto(x, y)\n"
        "            artist.pendown()\n"
        "            artist.begin_fill()\n"
        "            for _ in range(4):\n"
        "                artist.forward(razmer)\n"
        "                artist.right(90)\n"
        "            artist.end_fill()\n"
        "            artist.penup()\n",
    )}
    {callout(
        "info",
        "Вложенный цикл — строка за строкой, столбец за столбцом",
        "Внешний цикл (глава 10) идёт по строкам матрицы, внутренний — по значениям внутри "
        "строки; та же схема, что и у матрицы из главы 11 (§11.11), только теперь на каждую "
        "единицу рисуется квадрат, а не просто печатается число.",
    )}

    {exercise(3, "Измените ОДНО: своя картинка", "Замените picture на свою собственную матрицу 5×5 (или другого размера) из нулей и единиц — буква, смайлик, любой узор. Алгоритм менять не нужно.")}

    <h2>[[icon:debug]] Debug Lab</h2>
    <p>Что произойдёт, если в формуле координат перепутать местами
    <code class="inline">row_index</code> и <code class="inline">col_index</code>?</p>
    {code_block("debug_lab_grid.py", "x = -100 + row_index * razmer   # было col_index\ny = 100 - col_index * razmer    # было row_index\n")}
    {callout(
        "warning",
        "Картинка окажется зеркально отражённой (транспонированной)",
        "Строки и столбцы поменяются местами — там, где должна быть широкая горизонтальная "
        "часть сердца, получится вытянутая вертикальная. Формулы координат нужно очень "
        "аккуратно сверять с тем, что означает каждый индекс.",
    )}

    {local_required_card(
        "12-22",
        "Практика: пиксельная графика по своей матрице",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/12-22/index.html",
    )}
    """
    page(
        "12-22-setka-piksel-art.html",
        page_title="Проект: пиксельная графика по сетке",
        description="Мост между данными и графикой: матрица нулей и единиц, вложенные циклы, Turtle рисует по данным — реально сгенерированное сердце из квадратов.",
        kicker_suffix="Пиксельная графика",
        h1="Проект: пиксельная графика по сетке",
        lede="Данные → алгоритм → графика: вложенный список решает, что нарисовать, а "
        "вложенный цикл — как.",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# 12-06 · Гонка Turtle и итоги главы (расширено: реальный вывод + полные итоги)
# ---------------------------------------------------------------------------

def build_06() -> None:
    body = f"""
    {requirements_card(["Turtle", "list", "while", "random"], "★★★★ challenge", "графика Turtle")}

    <h2>Что создаём</h2>
    <p>Помните из главы 6, что экран и черепашка — разные объекты, и черепашек может быть
    несколько? Настало время это использовать: гонка из нескольких черепашек со случайным
    шагом.</p>
    {turtle_output(
        "12-gonka-turtle",
        "gonka_turtle.py",
        caption="Четыре черепашки в момент завершения гонки (seed зафиксирован для документации)",
        alt="Четыре цветные черепашки Turtle на разных позициях в конце гонки",
    )}
    {code_block(
        "gonka_turtle.py",
        "import random\n\n"
        "screen = turtle.Screen()\n"
        'screen.setup(500, 400)\n\n'
        'cveta = ["red", "blue", "green", "orange"]\n'
        "uchastniki = []\n\n"
        "for i, cvet in enumerate(cveta):\n"
        "    t = turtle.Turtle()\n"
        '    t.shape("turtle")\n'
        "    t.color(cvet)\n"
        "    t.penup()\n"
        "    t.goto(-200, i * 40 - 60)\n"
        "    uchastniki.append(t)\n\n"
        "finish_line = 200\n"
        "pobeditel = None\n\n"
        "while pobeditel is None:\n"
        "    for t in uchastniki:\n"
        "        t.forward(random.randint(1, 10))\n"
        "        if t.xcor() >= finish_line:\n"
        "            pobeditel = t.pencolor()\n"
        "            break\n\n"
        'print(f"Победила черепашка цвета {pobeditel}!")\n',
    )}
    {callout(
        "info",
        "Список черепашек — тот же список из главы 11",
        "<code class=\"inline\">uchastniki</code> — обычный список Python (глава 11), просто "
        "хранящий не числа, а объекты <code class=\"inline\">turtle.Turtle()</code>. Цикл "
        "<code class=\"inline\">for t in uchastniki</code> перебирает его точно так же, как "
        "перебирал бы список чисел или строк.",
    )}

    {exercise(3, "Финишная лента", "Нарисуйте вертикальную линию на финише (x=200) перед началом гонки, используя отдельную черепашку-«судью».")}
{local_required_card(
        "12-06",
        "Практика: гонка Turtle",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/12-06/index.html",
    )}

    <h2 id="itogi">Итоги главы</h2>

    <h3>Что мы теперь умеем строить</h3>
    {tree_diagram(
        ("Что мы теперь умеем строить", [
            ("Текстовые программы", [
                ("Анализатор текста и частота слов", []),
                ("Викторина", []),
                ("Консоль команд", []),
                ("Записная книжка", []),
                ("Угадай число, версия 3", []),
            ]),
            ("Программы с данными", [
                ("Журнал оценок", []),
                ("Корзина покупок", []),
                ("Проверка пароля", []),
            ]),
            ("Графика", [
                ("Студия многоугольников", []),
                ("Пиксельная графика по сетке", []),
                ("Спирали и сложная мандала", []),
                ("Рождественская ёлка", []),
                ("Гонка Turtle", []),
            ]),
        ]),
        caption="16 проектов — и всё это работает на одних и тех же инструментах глав 1-11",
    )}
    {capability_map([
        ("Строки", ["input(), split(), .lower()", "форматирование f-строками"]),
        ("Числа", ["арифметика, округление", "random"]),
        ("Условия", ["if / elif / else", "булевы флаги"]),
        ("Циклы", ["for, while, break", "счётчики, накопители"]),
        ("Коллекции", ["list, dict, set", "список словарей"]),
        ("Turtle", ["формулы поворота", "вложенные циклы → графика"]),
    ], title="Всё это питается одними и теми же инструментами глав 1-11")}

    <h3>Как далеко мы продвинулись</h3>
    {comparison_table(
        ["Глава 1", "Глава 12"],
        [["<code class=\"inline\">print(\"Hello\")</code>", "интерактивная игра, анализатор текста, викторина, записная книжка, структурированные данные, графический генератор"]],
    )}

    <h3>Чек-лист готовности проекта</h3>
    <p>Полный чек-лист — в §12.2 «Строим проект по шагам». Перед тем как считать любой из 16
    проектов главы законченным, полезно пройтись по нему ещё раз.</p>

    <h3>Что дальше: зачем нужны функции</h3>
    <p>Присмотритесь к проектам этой главы: нормализация ввода
    (<code class="inline">.strip().lower()</code>) повторяется в анализаторе текста, в
    консоли команд и в викторине. Накопитель, который нужно завести до цикла — та же самая
    ошибка чинилась трижды в разных Debug Lab. Формула угла поворота Turtle появляется и в
    ёлке, и в мандале, и в студии многоугольников.</p>
    {callout(
        "info",
        "[[icon:launch]] Скоро мы это упростим",
        "Сейчас, если один и тот же блок кода нужен в нескольких местах, его приходится "
        "копировать. В следующей главе — <strong>«Автоматизация с помощью функций»</strong> — "
        "мы научимся давать группе команд имя и использовать её многократно, не копируя код "
        "заново. Ничего из глав 1-12 при этом не устареет — функции просто дадут более "
        "аккуратный способ организовать то, что мы уже умеем писать.",
    )}

    {summary_box("Что мы закрепили в этой главе", [
        "<strong>Декомпозиция</strong> — разбиение большой задачи на маленькие понятные шаги.",
        "<strong>Инкрементальная разработка</strong> — маленькими шагами, каждый сразу "
        "проверяется, а не 80 строк за раз.",
        "<strong>Данные отдельно от алгоритма</strong> — викторина и студия многоугольников "
        "показали, что одна и та же логика работает для любых входных данных.",
        "<strong>Рефакторинг</strong> — улучшение структуры программы без изменения её "
        "поведения.",
        "Условия, циклы, строки, числа, <code class=\"inline\">random</code>, "
        "списки/множества/словари и Turtle — впервые работали вместе, в одной программе, а не "
        "по отдельности.",
        "Системный воркфлоу отладки: ожидание vs реальность → первое расхождение → причина → "
        "исправление.",
        "Сложные результаты (викторина, анализатор текста, мандала) — всегда комбинация "
        "нескольких простых, уже знакомых приёмов.",
    ])}
    """
    out = render_page(
        page_title="Проект: гонка Turtle с использованием циклов",
        description="Финальный проект главы 12: гонка нескольких черепашек — и полные итоги главы, включая карту всех 16 проектов и мост к функциям.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 12", "index.html"), ("Гонка Turtle", "")],
        kicker="Глава 12 · Множество увлекательных мини-проектов!",
        h1="Проект: гонка Turtle с использованием циклов",
        lede="Несколько черепашек на одном экране одновременно — и подведение итогов всей "
        "проектной лаборатории.",
        body_html=body,
        sidebar_groups=sidebar("12-06-gonka-turtle-itogi.html"),
        nav=nav_for("12-06-gonka-turtle-itogi.html"),
    )
    write("12-06-gonka-turtle-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_07()
    build_08()
    build_01()
    build_02()
    build_09()
    build_11()
    build_13()
    build_14()
    build_16()
    build_18()
    build_20()
    build_03()
    build_04()
    build_05()
    build_22()
    build_06()
