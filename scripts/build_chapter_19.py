#!/usr/bin/env python3
"""Строит Главу 19: «Проект: игра «Змейка» с Turtle» (site/chapters/glava-19/)."""

import html
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
    color_swatch_row,
    comparison_table,
    decision_map,
    exercise,
    flowchart,
    image_figure,
    local_required_card,
    object_diagram,
    pipeline_diagram,
    practice_card,
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-19"
IMG = "../../assets/img/chapter-19/output"

PAGES = [
    ("index.html", "Обзор главы"),
    ("19-01-igra-import.html", "Игра «Змейка» и импорт модулей"),
    ("19-02-ekran-peremennye.html", "Настраиваем экран и переменные"),
    ("19-03-golova-yabloko.html", "Рисуем голову и яблоко"),
    ("19-04-klavishi-dvizhenie.html", "Клавиши и движение головы"),
    ("19-05-tablo-scheta.html", "Табло счёта"),
    ("19-06-eda-telo.html", "Змейка ест! Движение тела"),
    ("19-07-stolknoveniya.html", "Проверка столкновений"),
    ("19-08-polnyj-kod-itogi.html", "Полный код и итоги"),
    ("19-09-mir-kak-setka.html", "Мир игры как сетка"),
    ("19-10-koordinaty-kletki.html", "Координаты клетки и пиксели Turtle"),
    ("19-11-napravlenie-kak-vektor.html", "Направление как вектор"),
    ("19-12-odin-igrovoj-tik.html", "Один игровой тик"),
    ("19-13-nastoyaschij-cikl.html", "Настоящий игровой цикл"),
    ("19-14-vremya-skorost.html", "Время, скорость и задержка"),
    ("19-15-sostoyanie-igry.html", "Состояние игры"),
    ("19-16-model-snake.html", "Голова, тело и модель Snake"),
    ("19-17-pochemu-s-hvosta.html", "Почему тело движется с хвоста"),
    ("19-18-eda-svobodnaya-kletka.html", "Еда и свободная клетка"),
    ("19-19-stolknovenie-so-stenoj.html", "Столкновение со стеной"),
    ("19-20-stolknovenie-s-soboj.html", "Столкновение с собой"),
    ("19-21-game-over.html", "Game Over как состояние"),
    ("19-22-pauza.html", "Pause / Resume"),
    ("19-23-restart.html", "Restart / New Game"),
    ("19-24-skorost-slozhnost.html", "Скорость и рост сложности"),
    ("19-25-high-score.html", "High Score"),
    ("19-26-chistaya-logika.html", "Чистая игровая логика без Turtle"),
    ("19-27-gamestate-dataclass.html", "GameState с dataclass"),
    ("19-28-snakeapp-arhitektura.html", "SnakeApp: отделяем модель от визуализации"),
    ("19-29-render-model.html", "Render: модель → Turtle"),
    ("19-30-testiruem-pravila.html", "Тестируем правила игры"),
    ("19-31-debug-labs.html", "Debug Labs"),
    ("19-32-snake-pro-itogi.html", "Snake Pro — финальная игра"),
    ("19-33-itogi-glavy.html", "Итоги и переход дальше"),
]

NOTEBOOKS = [
    "19-02-ekran.ipynb",
    "19-03-golova-yabloko.ipynb",
    "19-04-dvizhenie.ipynb",
    "19-06-eda-telo.ipynb",
    "19-07-stolknoveniya.ipynb",
    "19-08-polnaya-igra.ipynb",
]

LOCAL_REQUIRED_IDS = ["19-02", "19-03", "19-04", "19-06", "19-07", "19-08", "19-13", "19-28", "19-29", "19-32"]
BROWSER_AUTO_IDS = [
    "19-09", "19-10", "19-11", "19-12", "19-14", "19-15", "19-16", "19-17", "19-18",
    "19-19", "19-20", "19-21", "19-22", "19-23", "19-24", "19-25", "19-26", "19-27",
    "19-30", "19-31",
]
LESSON_IDS = sorted(LOCAL_REQUIRED_IDS + BROWSER_AUTO_IDS)


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 19 · Змейка", items),
        SidebarGroup(
            "Практика",
            [NavItem(f"[[icon:practice]] {lid}: Практика", f"../../practice/{lid}/index.html") for lid in LESSON_IDS],
        ),
        SidebarGroup("Исходный код", [
            NavItem("[[icon:code]] snake_basic.py — первый прототип (19.8)", "../../../projects/turtle/snake/snake_basic.py"),
            NavItem("[[icon:code]] snake.py — финальная версия Pro (19.32)", "../../../projects/turtle/snake/snake.py"),
        ]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    clean = "\n".join(line.rstrip() for line in html_out.split("\n"))
    path.write_text(clean, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# Локальные помощники главы 19
# ---------------------------------------------------------------------------

def grid_lattice_diagram(*, head: tuple[int, int] = (1, 1), food: tuple[int, int] | None = (2, 0),
                          cols: int = 5, rows: int = 4, caption: str = "") -> str:
    """Компактная HTML/CSS-сетка клеток — визуализация того, что легальные
    позиции лежат на решётке с шагом STEP, а не где угодно (раздел 19.9)."""
    cells = []
    for r in range(rows):
        for c in range(cols):
            is_head = (c, r) == head
            is_food = food is not None and (c, r) == food
            bg = "#5B24F9" if is_head else ("#FF5D5D" if is_food else "var(--color-bg-canvas,#fff)")
            border = "1px solid #3A2E63"
            cells.append(
                f'<div style="width:36px;height:36px;background:{bg};border:{border};'
                f'display:flex;align-items:center;justify-content:center;font-size:11px;'
                f'color:{"#fff" if (is_head or is_food) else "var(--ink-soft,#6B6B7D)"}">'
                f'{"●" if is_food else ("■" if is_head else "")}</div>'
            )
    grid_html = (
        f'<div style="display:grid;grid-template-columns:repeat({cols},36px);gap:0;'
        f'width:max-content;margin:0 auto;border:2px solid #5B24F9;border-radius:8px;overflow:hidden">'
        f'{"".join(cells)}</div>'
    )
    cap = (
        f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">'
        f'{html.escape(caption)}</figcaption>' if caption else ""
    )
    return (
        f'<figure style="margin:20px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px)">{grid_html}{cap}</figure>'
    )


def direction_vector_diagram() -> str:
    """Четыре карточки DIRECTION -> (dx, dy) вместо длинной if/elif-цепочки —
    визуальный эквивалент словаря DIRECTION_VECTORS (раздел 19.11)."""
    rows = [
        ("UP", "↑", "(0, +STEP)", "#5B24F9"),
        ("DOWN", "↓", "(0, −STEP)", "#5B24F9"),
        ("LEFT", "←", "(−STEP, 0)", "#DB2777"),
        ("RIGHT", "→", "(+STEP, 0)", "#DB2777"),
    ]
    cards = "".join(
        f'''<div style="background:var(--color-bg-canvas,#fff);border:1.5px solid {color};
          border-radius:14px;padding:14px 10px;text-align:center">
          <div style="font-size:28px;color:{color};line-height:1">{arrow}</div>
          <div style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:13px;margin-top:4px">{name}</div>
          <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:var(--ink-soft,#6B6B7D)">{delta}</div>
        </div>'''
        for name, arrow, delta, color in rows
    )
    return (
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));'
        f'gap:12px;margin:20px 0">{cards}</div>'
    )


def state_machine_diagram() -> str:
    """READY -> RUNNING <-> PAUSED, RUNNING -> GAME_OVER -> (restart) -> READY —
    четыре карточки состояния и подписанные переходы между ними, без диаграммы
    с пересекающимися стрелками (раздел 19.24, тот же стиль, что и раздел 18.12)."""
    def node(label: str, sub: str, accent: str) -> str:
        return f'''<div style="border:1.5px solid {accent};border-radius:14px;background:var(--color-bg-canvas,#fff);
          padding:10px 18px;text-align:center;width:min(220px,100%)">
          <div style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:13px;color:{accent}">{label}</div>
          <div style="font-size:13px;margin-top:2px">{sub}</div>
        </div>'''

    def arrow(text: str) -> str:
        return (
            f'<div style="display:flex;align-items:center;gap:8px;color:var(--ink-soft,#6B6B7D);'
            f'font-size:12px;margin:2px 0"><span style="font-size:18px;line-height:1">↓</span>{html.escape(text)}</div>'
        )

    ready = node("READY", "ждём первое направление", "#5B24F9")
    running = node("RUNNING", "тики идут", "#059669")
    paused = node("PAUSED", "тики остановлены", "#B45309")
    game_over = node("GAME_OVER", "столкновение", "#DB2777")

    pause_pair = f'''<div style="display:flex;flex-direction:column;align-items:center;gap:6px">
      {running}
      <div style="display:flex;align-items:center;gap:10px;color:var(--ink-soft,#6B6B7D);font-size:12px">
        <span>toggle_pause() ⇄ toggle_pause()</span>
      </div>
      {paused}
    </div>'''

    return f'''
    <figure style="margin:24px 0;padding:24px 20px;background:var(--color-bg-surface,#FAFAFC);
      border-radius:var(--radius-lg,20px);display:flex;flex-direction:column;align-items:center">
      {ready}
      {arrow("request_direction() — первое нажатие")}
      {pause_pair}
      {arrow("столкновение со стеной/собой")}
      {game_over}
      {arrow("restart()")}
      {ready}
    </figure>'''


def before_after_grid(before: list[tuple[int, int]], after: list[tuple[int, int]], *,
                       cols: int = 5, rows: int = 2, caption_before: str = "", caption_after: str = "") -> str:
    """Две мини-сетки рядом: было -> стало. cell-координаты в единицах
    клетки (col, row), 0-индексация слева-сверху — используется для body-follow
    и «новая голова + старое тело» (разделы 19.17–19.18)."""
    def grid(cells: list[tuple[int, int]], caption: str) -> str:
        boxes = []
        for r in range(rows):
            for c in range(cols):
                idx = None
                for i, (cx, cy) in enumerate(cells):
                    if (cx, cy) == (c, r):
                        idx = i
                        break
                if idx is None:
                    bg, label = "var(--color-bg-canvas,#fff)", ""
                elif idx == 0:
                    bg, label = "#5B24F9", "H"
                else:
                    bg, label = "#4ECDC4", str(idx)
                boxes.append(
                    f'<div style="width:32px;height:32px;background:{bg};border:1px solid #3A2E63;'
                    f'display:flex;align-items:center;justify-content:center;font-size:11px;'
                    f'color:{"#fff" if idx is not None else "transparent"}">{label}</div>'
                )
        return (
            f'<div><div style="display:grid;grid-template-columns:repeat({cols},32px);'
            f'border:2px solid #5B24F9;border-radius:8px;overflow:hidden">{"".join(boxes)}</div>'
            f'<div style="text-align:center;font-size:12px;color:var(--ink-soft,#6B6B7D);margin-top:6px">{html.escape(caption)}</div></div>'
        )

    return (
        f'<div style="display:flex;gap:24px;align-items:center;justify-content:center;'
        f'flex-wrap:wrap;margin:20px 0">{grid(before, caption_before)}'
        f'<div style="font-size:24px;color:#B9A0FC">→</div>{grid(after, caption_after)}</div>'
    )


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
    """Единый компонент Debug Lab (введён в главе 14, переиспользован в 15–18):
    сломанный код → что происходит на экране → объяснение → исправленный код."""
    return f"""
    <div style="margin:28px 0;padding:4px 4px 20px;border:2px dashed #DB2777;border-radius:var(--radius-lg,20px)">
      <div style="display:flex;align-items:center;gap:12px;padding:16px 20px 6px">
        <div class="cs-icon-emblem cs-icon-emblem--debug">[[icon:debug]]</div>
        <div style="font-family:Sora,sans-serif;font-weight:700;font-size:13px;
        letter-spacing:.05em;text-transform:uppercase;color:#DB2777">Debug Lab {n}: {html.escape(title)}</div>
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


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=19,
        baseline_page=413,
        title="Проект: игра «Змейка» с Turtle",
        description="От первого работающего прототипа до модели игры с игровым тиком, "
        "паузой, рестартом, счётом и проверяемыми правилами — классическая «Змейка» на Turtle "
        "как введение в программирование игр реального времени.",
        meta_items=["[[icon:timer]] ~8 часов", "[[icon:code]] Turtle + игровой цикл", "[[icon:game]] Snake Pro", "[[icon:practice]] 30 практик"],
        sections=[
            ChapterSectionLink("19.1", "Игра «Змейка»", "19-01-igra-import.html", "413"),
            ChapterSectionLink("19.2", "Настраиваем экран Turtle", "19-02-ekran-peremennye.html", "415"),
            ChapterSectionLink("19.3", "Рисуем голову", "19-03-golova-yabloko.html", "417"),
            ChapterSectionLink("19.4", "Клавиши и движение головы", "19-04-klavishi-dvizhenie.html", "421"),
            ChapterSectionLink("19.5", "Запускаем табло счёта", "19-05-tablo-scheta.html", "426"),
            ChapterSectionLink("19.6", "Наша змейка ест!", "19-06-eda-telo.html", "428"),
            ChapterSectionLink("19.7", "Проверка столкновений", "19-07-stolknoveniya.html", "434"),
            ChapterSectionLink("19.8", "Полный код первого прототипа", "19-08-polnyj-kod-itogi.html", "439"),
            ChapterSectionLink("19.9", "Мир игры как сетка", "19-09-mir-kak-setka.html", "442"),
            ChapterSectionLink("19.10", "Координаты клетки и пиксели Turtle", "19-10-koordinaty-kletki.html", "444"),
            ChapterSectionLink("19.11", "Направление как вектор", "19-11-napravlenie-kak-vektor.html", "446"),
            ChapterSectionLink("19.12", "Один игровой тик", "19-12-odin-igrovoj-tik.html", "448"),
            ChapterSectionLink("19.13", "Настоящий игровой цикл", "19-13-nastoyaschij-cikl.html", "450"),
            ChapterSectionLink("19.14", "Время, скорость и задержка", "19-14-vremya-skorost.html", "452"),
            ChapterSectionLink("19.15", "Состояние игры", "19-15-sostoyanie-igry.html", "454"),
            ChapterSectionLink("19.16", "Голова, тело и модель Snake", "19-16-model-snake.html", "456"),
            ChapterSectionLink("19.17", "Почему тело движется с хвоста", "19-17-pochemu-s-hvosta.html", "458"),
            ChapterSectionLink("19.18", "Еда и свободная клетка", "19-18-eda-svobodnaya-kletka.html", "460"),
            ChapterSectionLink("19.19", "Столкновение со стеной", "19-19-stolknovenie-so-stenoj.html", "462"),
            ChapterSectionLink("19.20", "Столкновение с собой", "19-20-stolknovenie-s-soboj.html", "464"),
            ChapterSectionLink("19.21", "Game Over как состояние", "19-21-game-over.html", "466"),
            ChapterSectionLink("19.22", "Pause / Resume", "19-22-pauza.html", "468"),
            ChapterSectionLink("19.23", "Restart / New Game", "19-23-restart.html", "470"),
            ChapterSectionLink("19.24", "Скорость и рост сложности", "19-24-skorost-slozhnost.html", "472"),
            ChapterSectionLink("19.25", "High Score", "19-25-high-score.html", "474"),
            ChapterSectionLink("19.26", "Чистая игровая логика без Turtle", "19-26-chistaya-logika.html", "476"),
            ChapterSectionLink("19.27", "GameState с dataclass", "19-27-gamestate-dataclass.html", "478"),
            ChapterSectionLink("19.28", "SnakeApp: отделяем модель от визуализации", "19-28-snakeapp-arhitektura.html", "480"),
            ChapterSectionLink("19.29", "Render: модель → Turtle", "19-29-render-model.html", "483"),
            ChapterSectionLink("19.30", "Тестируем правила игры", "19-30-testiruem-pravila.html", "485"),
            ChapterSectionLink("19.31", "Debug Labs", "19-31-debug-labs.html", "487"),
            ChapterSectionLink("19.32", "Snake Pro — финальная игра", "19-32-snake-pro-itogi.html", "491"),
            ChapterSectionLink("19.33", "Итоги главы", "19-33-itogi-glavy.html", "494"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    {image_figure(f"{IMG}/snake-final-overview.png", "Реальное окно: змейка из нескольких сегментов, яблоко, счёт и рекорд на тёмном поле", "К концу главы эта игра будет работать на собственной модели состояния, игровом цикле и проверяемых правилах.", width=560)}

    <h2>Игра «Змейка»</h2>
    <p>«Змейка» — одна из самых узнаваемых игр в истории программирования. Змейка непрерывно
    движется по полю, съедает появляющиеся яблоки и растёт с каждым съеденным яблоком; игра
    заканчивается при столкновении со стеной или с собственным хвостом. Соберём её на уже
    знакомом модуле <code class="inline">turtle</code> (главы 6–7, 12) — только на этот раз
    черепашка станет не художником, а персонажем игры.</p>
    <p>Как и в главе 18, план знакомый: сначала честно работающий процедурный прототип
    (разделы 19.1–19.8), потом внимательный разбор того, как устроена игра на самом деле —
    сетка, направление как данные, игровой тик, состояние, архитектура (разделы 19.9–19.33).</p>

    <h2 id="import">Импортируем необходимые модули</h2>
    {code_block(
        "importy.py",
        "import random\n"
        "import turtle\n",
    )}
    <p><code class="inline">random</code> понадобится для случайного положения яблока (глава 5),
    <code class="inline">turtle</code> — для самой графики.</p>

    {local_required_card(
        "19-02",
        "Практика: начинаем собирать игру",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/19-02/index.html",
    )}
    """
    out = render_page(
        page_title="Игра «Змейка» и импорт модулей",
        description="Введение в проект «Змейка» на Turtle и необходимые модули random и turtle.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Игра и импорт", "")],
        kicker="Глава 19 · Проект: «Змейка»",
        h1="Игра «Змейка»",
        lede="Классическая игра — движение, еда и столкновения — на уже знакомом модуле "
        "turtle.",
        body_html=body,
        sidebar_groups=sidebar("19-01-igra-import.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="19-02-ekran-peremennye.html", next_label="Экран и переменные"),
    )
    write("19-01-igra-import.html", out)


def build_02() -> None:
    body = f"""
    <h2>Настраиваем экран Turtle</h2>
    <p>Игре нужен предсказуемый, контролируемый экран — и, что важно, отключённое
    автообновление: обновлять картинку мы будем вручную, ровно раз за игровой шаг, а не при
    каждом мелком движении:</p>
    {code_block(
        "nastrojka_ekrana.py",
        "screen = turtle.Screen()\n"
        'screen.title("Змейка")\n'
        'screen.bgcolor("black")\n'
        "screen.setup(width=600, height=600)\n"
        "screen.tracer(0)   # отключаем автообновление\n",
    )}
    {callout(
        "info",
        "Зачем tracer(0)?",
        "Без <code class=\"inline\">tracer(0)</code> Turtle перерисовывает экран после "
        "<em>каждого</em> отдельного движения — для игры, где нужно двигать голову и "
        "несколько сегментов тела на каждом шаге, это выглядело бы мерцающим и медленным. "
        "<code class=\"inline\">tracer(0)</code> + ручной <code class=\"inline\">screen.update()"
        "</code> в конце каждого шага дают куда более плавную анимацию.",
    )}

    <h2 id="peremennye">Создаём и инициализируем необходимые переменные</h2>
    {code_block(
        "peremennye.py",
        "RAZMER_SHAGA = 20\n"
        "GRANICA = 280\n\n"
        'napravlenie = "stop"\n'
        "schet = 0\n"
        "igra_okonchena = False\n"
        "segmenty = []   # тело змейки\n",
    )}
    {callout(
        "tip",
        "ЗАГЛАВНЫЕ_БУКВЫ — соглашение для констант",
        "<code class=\"inline\">RAZMER_SHAGA</code> и <code class=\"inline\">GRANICA</code> не "
        "меняются в процессе игры — по соглашению такие «постоянные» переменные принято "
        "называть заглавными буквами. Само по себе это ничего не меняет технически, но "
        "сигнализирует читателю: «это значение не должно меняться».",
    )}
    {image_figure(f"{IMG}/snake-basic-empty-field.png", "Реальное окно: чёрный игровой экран 600×600 с надписью «Счёт: 0» и одним красным яблоком", "Реальное окно: экран настроен, переменные заведены — рисовать пока нечего.", width=380)}

    {local_required_card(
        "19-02",
        "Практика: настройка экрана и переменных",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/19-02/index.html",
    )}
    """
    out = render_page(
        page_title="Настраиваем экран Turtle и переменные",
        description="tracer(0) для ручного управления обновлением экрана и переменные состояния игры «Змейка».",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Экран и переменные", "")],
        kicker="Глава 19 · Проект: «Змейка»",
        h1="Настраиваем экран Turtle",
        lede="Отключаем автообновление экрана и заводим переменные, которые будут помнить "
        "состояние игры.",
        body_html=body,
        sidebar_groups=sidebar("19-02-ekran-peremennye.html"),
        nav=PageNav(prev_href="19-01-igra-import.html", prev_label="Игра и импорт", next_href="19-03-golova-yabloko.html", next_label="Голова и яблоко"),
    )
    write("19-02-ekran-peremennye.html", out)


def build_03() -> None:
    body = f"""
    <h2>Рисуем голову</h2>
    <p>Голова змейки — обычный объект <code class="inline">turtle.Turtle()</code>, знакомый
    ещё с главы 6, только с квадратной формой и без рисования линий (перо поднято):</p>
    {code_block(
        "golova.py",
        "golova = turtle.Turtle()\n"
        "golova.speed(0)\n"
        'golova.shape("square")\n'
        'golova.color("white")\n'
        "golova.penup()\n"
        "golova.goto(0, 0)\n",
    )}

    <h2 id="yabloko">Рисуем первое яблоко</h2>
    <p>Яблоко — тоже черепашка, только круглая и красная, и появляется в случайном месте поля,
    выровненном по сетке шага (<code class="inline">random.randrange()</code> с шагом
    <code class="inline">RAZMER_SHAGA</code>, чтобы яблоко всегда оказывалось «в клетке»):</p>
    {code_block(
        "yabloko.py",
        "yabloko = turtle.Turtle()\n"
        "yabloko.speed(0)\n"
        'yabloko.shape("circle")\n'
        'yabloko.color("red")\n'
        "yabloko.penup()\n\n"
        "def novoe_yabloko():\n"
        "    x = random.randrange(-GRANICA, GRANICA, RAZMER_SHAGA)\n"
        "    y = random.randrange(-GRANICA, GRANICA, RAZMER_SHAGA)\n"
        "    yabloko.goto(x, y)\n\n"
        "novoe_yabloko()\n",
    )}
    {image_figure(f"{IMG}/snake-basic-head-food.png", "Реальное окно: белая квадратная голова змейки в центре, красное круглое яблоко рядом", "Реальное окно: голова и яблоко — два независимых объекта Turtle, оба с поднятым пером.", width=380)}

    {local_required_card(
        "19-03",
        "Практика: голова и яблоко",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/19-03/index.html",
    )}
    """
    out = render_page(
        page_title="Рисуем голову и яблоко",
        description="Создаём голову змейки и яблоко как объекты turtle.Turtle() со случайным положением.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Голова и яблоко", "")],
        kicker="Глава 19 · Проект: «Змейка»",
        h1="Рисуем голову",
        lede="Голова и яблоко — обычные объекты Turtle с разной формой и цветом.",
        body_html=body,
        sidebar_groups=sidebar("19-03-golova-yabloko.html"),
        nav=PageNav(prev_href="19-02-ekran-peremennye.html", prev_label="Экран и переменные", next_href="19-04-klavishi-dvizhenie.html", next_label="Клавиши и движение"),
    )
    write("19-03-golova-yabloko.html", out)


def build_04() -> None:
    body = f"""
    <h2>Регистрирует ли экран нажатия клавиш со стрелками?</h2>
    <p>Чтобы Turtle реагировал на клавиатуру, ему нужно явно разрешить «слушать» события
    (<code class="inline">screen.listen()</code>) и связать конкретные клавиши с функциями через
    <code class="inline">onkeypress()</code> — идея та же, что и <code class="inline">.bind()</code>
    у Tkinter в главе 17, только с более простым, специализированным интерфейсом:</p>
    {code_block(
        "klavishi.py",
        "def idti_vverh():\n"
        "    global napravlenie\n"
        '    if napravlenie != "down":   # нельзя развернуться на 180° мгновенно\n'
        '        napravlenie = "up"\n\n'
        "def idti_vniz():\n"
        "    global napravlenie\n"
        '    if napravlenie != "up":\n'
        '        napravlenie = "down"\n\n'
        "# idti_vlevo() и idti_vpravo() устроены аналогично\n\n"
        "screen.listen()\n"
        'screen.onkeypress(idti_vverh, "Up")\n'
        'screen.onkeypress(idti_vniz, "Down")\n'
        'screen.onkeypress(idti_vlevo, "Left")\n'
        'screen.onkeypress(idti_vpravo, "Right")\n',
    )}
    {callout(
        "warning",
        "Почему нельзя просто развернуться на 180°?",
        "Если змейка двигалась вправо, а игрок нажмёт «влево», голова мгновенно «наедет» на "
        "первый сегмент собственного тела — это выглядело бы как мгновенный проигрыш без "
        "видимой причины. Проверка <code class=\"inline\">if napravlenie != \"down\":</code> "
        "запрещает разворот на месте, разрешая только повороты на 90°.",
    )}

    <h2 id="dvizhenie">Заставляем голову змейки двигаться</h2>
    {code_block(
        "dvizhenie_golovy.py",
        "def dvigat_golovu():\n"
        '    if napravlenie == "up":\n'
        "        golova.sety(golova.ycor() + RAZMER_SHAGA)\n"
        '    elif napravlenie == "down":\n'
        "        golova.sety(golova.ycor() - RAZMER_SHAGA)\n"
        '    elif napravlenie == "left":\n'
        "        golova.setx(golova.xcor() - RAZMER_SHAGA)\n"
        '    elif napravlenie == "right":\n'
        "        golova.setx(golova.xcor() + RAZMER_SHAGA)\n",
    )}
    {callout(
        "tip",
        "sety()/setx() — половина от goto()",
        "<code class=\"inline\">sety(y)</code> меняет только координату Y, оставляя X "
        "прежним — удобнее, чем вычислять обе координаты через "
        "<code class=\"inline\">goto()</code> каждый раз.",
    )}
    {image_figure(f"{IMG}/snake-basic-moving.png", "Реальное окно: голова змейки сдвинулась вправо от центра поля на несколько шагов", "Реальное окно: после нескольких вызовов dvigat_golovu() с направлением right.", width=380)}

    {local_required_card(
        "19-04",
        "Практика: клавиши и движение головы",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/19-04/index.html",
    )}
    """
    out = render_page(
        page_title="Клавиши и движение головы",
        description="onkeypress() для управления с клавиатуры и движение головы змейки по сетке.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Клавиши и движение", "")],
        kicker="Глава 19 · Проект: «Змейка»",
        h1="Регистрирует ли экран нажатия клавиш со стрелками?",
        lede="Подключаем клавиатуру и заставляем голову двигаться — с защитой от мгновенного "
        "разворота на 180°.",
        body_html=body,
        sidebar_groups=sidebar("19-04-klavishi-dvizhenie.html"),
        nav=PageNav(prev_href="19-03-golova-yabloko.html", prev_label="Голова и яблоко", next_href="19-05-tablo-scheta.html", next_label="Табло счёта"),
    )
    write("19-04-klavishi-dvizhenie.html", out)


def build_05() -> None:
    body = f"""
    <p>Счёт удобно показывать отдельной черепашкой без формы (<code class="inline">hideturtle()</code>),
    которая ничего не рисует, кроме текста (<code class="inline">write()</code> из главы 7):</p>
    {code_block(
        "tablo_scheta.py",
        "tablo = turtle.Turtle()\n"
        "tablo.speed(0)\n"
        'tablo.color("white")\n'
        "tablo.penup()\n"
        "tablo.hideturtle()\n"
        "tablo.goto(0, 260)\n\n"
        "def obnovit_tablo():\n"
        "    tablo.clear()   # стираем старую надпись перед новой\n"
        '    tablo.write(f"Счёт: {schet}", align="center", font=("Arial", 16, "normal"))\n\n'
        "obnovit_tablo()\n",
    )}
    {callout(
        "warning",
        "clear() перед write() — обязательно",
        "Без <code class=\"inline\">tablo.clear()</code> каждый новый счёт накладывался бы "
        "поверх предыдущего — цифры быстро превратились бы в нечитаемую кашу.",
    )}
    {image_figure(f"{IMG}/snake-basic-full-game.png", "Реальное окно: игровое поле с надписью «Счёт: 30» вверху, змейка из трёх сегментов", "Реальное окно: obnovit_tablo() перерисовывает счёт после каждого съеденного яблока.", width=380)}

    {local_required_card(
        "19-06",
        "Практика: табло и поедание яблок",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/19-06/index.html",
    )}
    """
    out = render_page(
        page_title="Запускаем табло счёта",
        description="Отдельная черепашка для отображения текущего счёта игры «Змейка».",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Табло счёта", "")],
        kicker="Глава 19 · Проект: «Змейка»",
        h1="Запускаем табло счёта",
        lede="Отдельная черепашка без формы, которая только показывает текст текущего счёта.",
        body_html=body,
        sidebar_groups=sidebar("19-05-tablo-scheta.html"),
        nav=PageNav(prev_href="19-04-klavishi-dvizhenie.html", prev_label="Клавиши и движение", next_href="19-06-eda-telo.html", next_label="Змейка ест! Тело"),
    )
    write("19-05-tablo-scheta.html", out)


def build_06() -> None:
    body = f"""
    <h2>Наша змейка ест!</h2>
    <p>Проверяем, достаточно ли близко голова оказалась к яблоку (метод
    <code class="inline">.distance()</code> считает расстояние между двумя черепашками) — если
    да, яблоко «съедено»: появляется новое яблоко, змейка растёт, счёт увеличивается:</p>
    {code_block(
        "eda.py",
        "def proverit_edu():\n"
        "    global schet\n"
        "    if golova.distance(yabloko) < RAZMER_SHAGA:\n"
        "        novoe_yabloko()\n"
        "        dobavit_segment()\n"
        "        schet += 10\n"
        "        obnovit_tablo()\n",
    )}

    <h2 id="telo">Заставляем двигаться всю змейку</h2>
    <p>Каждый сегмент тела должен занять место <em>предыдущего</em> сегмента (а первый — место
    головы) — это создаёт эффект «змейка ползёт целиком», а не «части двигаются независимо»:</p>
    {code_block(
        "dobavit_segment.py",
        "def dobavit_segment():\n"
        "    novyj = turtle.Turtle()\n"
        "    novyj.speed(0)\n"
        '    novyj.shape("square")\n'
        '    novyj.color("grey")\n'
        "    novyj.penup()\n"
        "    segmenty.append(novyj)\n",
    )}
    {code_block(
        "dvigat_telo.py",
        "def dvigat_telo():\n"
        "    # начинаем с хвоста и идём к голове, чтобы не потерять позиции по пути\n"
        "    for indeks in range(len(segmenty) - 1, 0, -1):\n"
        "        x = segmenty[indeks - 1].xcor()\n"
        "        y = segmenty[indeks - 1].ycor()\n"
        "        segmenty[indeks].goto(x, y)\n\n"
        "    if segmenty:\n"
        "        segmenty[0].goto(golova.xcor(), golova.ycor())\n",
    )}
    {callout(
        "warning",
        "Порядок вызовов решает всё",
        "<code class=\"inline\">dvigat_telo()</code> обязательно вызывается <strong>до</strong> "
        "<code class=\"inline\">dvigat_golovu()</code> — иначе первый сегмент «унаследует» уже "
        "<em>новую</em> позицию головы вместо старой, и тело слипнется с головой в одну точку.",
    )}
    {image_figure(f"{IMG}/snake-basic-eaten-strip.png", "Два реальных окна рядом: слева голова рядом с яблоком, справа яблоко исчезло и появился один серый сегмент тела", "Реальное окно до и после proverit_edu(): яблоко съедено, счёт вырос, добавился сегмент.", width=680)}

    {local_required_card(
        "19-06",
        "Практика: поедание яблок и движение тела",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/19-06/index.html",
    )}
    """
    out = render_page(
        page_title="Змейка ест! Движение тела",
        description="Проверка поедания яблока через distance() и движение всех сегментов тела змейки.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Еда и тело", "")],
        kicker="Глава 19 · Проект: «Змейка»",
        h1="Наша змейка ест!",
        lede="Съеденное яблоко добавляет сегмент — и каждый сегмент должен правильно следовать "
        "за предыдущим.",
        body_html=body,
        sidebar_groups=sidebar("19-06-eda-telo.html"),
        nav=PageNav(prev_href="19-05-tablo-scheta.html", prev_label="Табло счёта", next_href="19-07-stolknoveniya.html", next_label="Проверка столкновений"),
    )
    write("19-06-eda-telo.html", out)


def build_07() -> None:
    body = f"""
    <p>Игра заканчивается при одном из двух столкновений: со стеной поля или с собственным
    телом.</p>
    {code_block(
        "stolknoveniya.py",
        "def proverit_stolknoveniya():\n"
        "    global igra_okonchena\n\n"
        "    # столкновение со стеной\n"
        "    if abs(golova.xcor()) > GRANICA or abs(golova.ycor()) > GRANICA:\n"
        "        igra_okonchena = True\n\n"
        "    # столкновение с собственным телом\n"
        "    for segment in segmenty:\n"
        "        if segment.distance(golova) < RAZMER_SHAGA / 2:\n"
        "            igra_okonchena = True\n",
    )}
    {callout(
        "info",
        "abs() снова экономит код",
        "<code class=\"inline\">abs(golova.xcor()) > GRANICA</code> проверяет сразу обе "
        "стены (левую и правую) одним сравнением — вместо "
        "<code class=\"inline\">golova.xcor() &gt; GRANICA or golova.xcor() &lt; -GRANICA</code>. "
        "Тот же приём мы использовали для факториала и других вычислений в главе 5.",
    )}
    {image_figure(f"{IMG}/snake-basic-collision.png", "Реальное окно: голова змейки у самого правого края тёмного поля, счёт остаётся прежним", "Реальное окно: голова вышла за GRANICA — proverit_stolknoveniya() выставила igra_okonchena в True.", width=380)}

    {exercise(2, "Ускорение игры", "Увеличивайте скорость движения (уменьшайте задержку между шагами) на каждые 50 очков — игра станет постепенно сложнее.")}

    {local_required_card(
        "19-07",
        "Практика: столкновения",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/19-07/index.html",
    )}
    """
    out = render_page(
        page_title="Проверка столкновений",
        description="Определяем конец игры: столкновение со стеной поля или с собственным телом змейки.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Столкновения", "")],
        kicker="Глава 19 · Проект: «Змейка»",
        h1="Проверка столкновений",
        lede="Игра заканчивается при столкновении со стеной или с собственным хвостом.",
        body_html=body,
        sidebar_groups=sidebar("19-07-stolknoveniya.html"),
        nav=PageNav(prev_href="19-06-eda-telo.html", prev_label="Еда и тело", next_href="19-08-polnyj-kod-itogi.html", next_label="Полный код и итоги"),
    )
    write("19-07-stolknoveniya.html", out)


def build_08() -> None:
    body = f"""
    <p>Соберём один игровой шаг из всех частей главы — эта функция и есть сердце игры,
    вызываемое снова и снова, пока игра не закончится:</p>
    {code_block(
        "igrovoj_shag.py",
        "def igrovoj_shag():\n"
        "    if igra_okonchena:\n"
        "        return False\n\n"
        "    dvigat_telo()\n"
        "    dvigat_golovu()\n"
        "    proverit_edu()\n"
        "    proverit_stolknoveniya()\n"
        "    screen.update()\n"
        "    return not igra_okonchena\n\n"
        "def glavnyj_cikl():\n"
        '    global napravlenie\n'
        '    napravlenie = "right"\n'
        "    while igrovoj_shag():\n"
        "        screen.update()\n"
        '    tablo.goto(0, 0)\n'
        '    tablo.write(f"Игра окончена! Счёт: {schet}", align="center", font=("Arial", 20, "bold"))\n',
    )}
    {image_figure(f"{IMG}/snake-basic-full-game.png", "Реальное окно: собранная игра — счёт 30, змейка из трёх сегментов, яблоко на поле", "Реальное окно первого прототипа: всё вместе — движение, еда, счёт.", width=380)}
    <p>Полная, уже собранная и проверенная программа первого прототипа доступна отдельным файлом:</p>
    <p>[[icon:file]] <a href="../../../projects/turtle/snake/snake_basic.py">projects/turtle/snake/snake_basic.py</a></p>
    {callout(
        "tip",
        "Запустите игру у себя",
        "<code class=\"inline\">python snake_basic.py</code> в терминале — управление стрелками "
        "клавиатуры.",
    )}
    {callout(
        "info",
        "Честная, но не окончательная версия",
        "Мы построили настоящую работающую игру — с движением, едой, счётом и столкновениями. "
        "Но <code class=\"inline\">while igrovoj_shag(): screen.update()</code> — busy-цикл без "
        "паузы и без изменяемой скорости, а всё состояние живёт в глобальных переменных модуля. "
        "Начиная со следующего раздела глава смотрит на игру внимательнее: что такое сетка и "
        "игровой тик по-настоящему, как устроить паузу и рестарт без второй параллельной "
        "цепочки таймеров, и как вырастить из этого прототипа архитектуру уровня "
        "<code class=\"inline\">SnakeApp</code> (раздел 19.32).",
    )}

    {exercise(3, "Уровни сложности", "Добавьте выбор уровня сложности перед стартом игры (input() из главы 8) — влияющий на начальную скорость через задержку между шагами.")}

{local_required_card(
        "19-08",
        "Практика: полная игра",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/19-08/index.html",
    )}

    <h2 id="itogi">Итоги первого прототипа</h2>
    {summary_box("Что мы узнали в первых восьми разделах", [
        "<code class=\"inline\">screen.tracer(0)</code> + ручной "
        "<code class=\"inline\">screen.update()</code> — стандартный приём для плавной "
        "анимации в играх на Turtle.",
        "<code class=\"inline\">screen.onkeypress()</code> связывает клавиши со стрелками с "
        "функциями изменения направления; запрет разворота на 180° предотвращает мгновенное "
        "самостолкновение.",
        "Тело змейки — список отдельных сегментов, каждый из которых следует за предыдущим; "
        "порядок обновления (сначала тело, потом голова) критически важен.",
        "<code class=\"inline\">.distance()</code> между двумя черепашками — удобный способ "
        "проверить, находятся ли они «достаточно близко» (для еды и столкновений).",
        "Игровой цикл — функция, вызываемая снова и снова, пока не наступит условие конца "
        "игры.",
        "Это только первый прототип — дальше глава разбирает сетку, тик, состояние и "
        "архитектуру куда внимательнее.",
    ])}
    """
    out = render_page(
        page_title="Полный код первого прототипа",
        description="Собираем игровой шаг воедино, ссылка на snake_basic.py и итоги первого прототипа главы 19.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Полный код и итоги", "")],
        kicker="Глава 19 · Проект: «Змейка»",
        h1="Полный код первого прототипа",
        lede="Собираем все части в единый игровой цикл — и переходим от честного прототипа к "
        "внимательному разбору того, как устроена игра на самом деле.",
        body_html=body,
        sidebar_groups=sidebar("19-08-polnyj-kod-itogi.html"),
        nav=PageNav(prev_href="19-07-stolknoveniya.html", prev_label="Столкновения", next_href="19-09-mir-kak-setka.html", next_label="Мир игры как сетка"),
    )
    write("19-08-polnyj-kod-itogi.html", out)


# ---------------------------------------------------------------------------
# 19.9 – 19.17: сетка, координаты, направление, тик, цикл, время, состояние, модель
# ---------------------------------------------------------------------------

def build_09() -> None:
    body = f"""
    <h2>Змейка живёт не в произвольных координатах</h2>
    <p>Первый прототип уже двигает голову шагами по 20 пикселей, но легко не заметить, почему
    именно так: змейка не может оказаться в точке (137, 52) — только в точках, кратных
    <code class="inline">RAZMER_SHAGA</code>. Игровое поле — это не холст, где можно нарисовать
    линию под любым углом (как Canvas в главе 18), а <strong>дискретная сетка</strong>: конечный
    набор клеток, и каждый объект игры — голова, сегмент тела, яблоко — всегда стоит ровно в
    одной из них.</p>
    {grid_lattice_diagram(caption="Легальные позиции — узлы решётки с шагом RAZMER_SHAGA, а не любая точка поля.")}
    <p>При <code class="inline">RAZMER_SHAGA = 20</code> легальные координаты по каждой оси —
    <code class="inline">..., -40, -20, 0, 20, 40, ...</code>. Движение на шаг — это переход к
    соседнему узлу решётки, а не плавное скольжение на произвольное расстояние.</p>
    {callout(
        "info",
        "Та же идея, что и в главе 18 — но без пикселей между клетками",
        "Canvas тоже работал в целых пикселях, но фигуру можно было сдвинуть на 1 пиксель. "
        "У змейки шаг фиксирован: <code class=\"inline\">RAZMER_SHAGA</code> — это не «минимальная "
        "единица экрана», а сама единица игрового мира. Это и определяет всё остальное в главе: "
        "как размещается еда, как обнаруживается столкновение, как выглядит движение тела.",
    )}

    {practice_card(
        "19-09",
        "Практика: легальные позиции сетки",
        "Автоматическая проверка — определяем, кратна ли точка шагу сетки",
        "../../practice/19-09/index.html",
    )}
    """
    out = render_page(
        page_title="Мир игры как сетка",
        description="Змейка живёт на дискретной решётке с шагом RAZMER_SHAGA — легальные позиции кратны шагу, а не произвольны.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Мир как сетка", "")],
        kicker="Глава 19 · Модель игры",
        h1="Мир игры как сетка",
        lede="Голова, тело и яблоко всегда стоят в узле решётки — движение это переход к "
        "соседнему узлу, не скольжение.",
        body_html=body,
        sidebar_groups=sidebar("19-09-mir-kak-setka.html"),
        nav=PageNav(prev_href="19-08-polnyj-kod-itogi.html", prev_label="Полный код первого прототипа", next_href="19-10-koordinaty-kletki.html", next_label="Координаты клетки и пиксели"),
    )
    write("19-09-mir-kak-setka.html", out)


def build_10() -> None:
    body = f"""
    <h2>Клетка сетки против пикселя Turtle</h2>
    <p>У Turtle нет отдельного понятия «клетка» — есть только пиксельные координаты
    <code class="inline">(x, y)</code>, те же самые, что и в главах 6–7. Можно было бы завести
    отдельную систему координат клеток — <code class="inline">col = x // STEP</code>,
    <code class="inline">row = y // STEP</code> — и переводить одно в другое при каждом
    обращении к экрану.</p>
    {code_block(
        "kletka_v_pikseli.py",
        "def kletka_v_pikseli(col, row, step=20):\n"
        "    return col * step, row * step\n\n"
        "def pikseli_v_kletku(x, y, step=20):\n"
        "    return x // step, y // step\n",
    )}
    {callout(
        "warning",
        "Целочисленное деление отрицательных чисел — не то же самое, что округление к нулю",
        "<code class=\"inline\">-10 // 20</code> в Python равно <code class=\"inline\">-1</code>, "
        "а не <code class=\"inline\">0</code> — Python округляет деление вниз (к минус "
        "бесконечности), а не к нулю. Формула перевода пикселей в клетки, написанная без учёта "
        "этого, будет неверна ровно в половине поля — той, что с отрицательными координатами.",
    )}
    <p>Для этой главы выбрано более простое решение: логическая позиция змейки и яблока —
    это сразу пиксельные координаты Turtle, уже кратные <code class="inline">STEP</code>. Отдельной
    системы «клетка (col, row)» нет вообще — <code class="inline">(x, y)</code> одновременно и
    то, что мы храним в модели, и то, что понимает <code class="inline">turtle.goto()</code>.</p>
    {code_block(
        "logicheskaya_poziciya.py",
        "STEP = 20\n"
        "head = (0, 0)          # уже пиксели Turtle — и уже позиция клетки\n"
        "head = (head[0] + STEP, head[1])   # шаг вправо — сразу в пикселях\n",
    )}
    {callout(
        "tip",
        "Меньше кода — меньше мест для ошибки",
        "Перевод «клетка ↔ пиксель» — лишний шаг, который пришлось бы делать в обе стороны на "
        "каждом тике: один раз при движении, второй — при отрисовке. Раз координаты и так всегда "
        "кратны <code class=\"inline\">STEP</code>, этот перевод не добавляет никакой новой "
        "информации — только риск обратной ошибки округления из примера выше.",
    )}

    {practice_card(
        "19-10",
        "Практика: клетка и пиксели",
        "Автоматическая проверка — округление координат в клетки с отрицательными числами",
        "../../practice/19-10/index.html",
    )}
    """
    out = render_page(
        page_title="Координаты клетки и пиксели Turtle",
        description="Почему логические позиции змейки — это сразу пиксельные координаты Turtle, а не отдельная система col/row.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Координаты клетки", "")],
        kicker="Глава 19 · Модель игры",
        h1="Координаты клетки и пиксели Turtle",
        lede="Отдельный перевод «клетка → пиксель» не нужен — координаты и так всегда кратны шагу.",
        body_html=body,
        sidebar_groups=sidebar("19-10-koordinaty-kletki.html"),
        nav=PageNav(prev_href="19-09-mir-kak-setka.html", prev_label="Мир как сетка", next_href="19-11-napravlenie-kak-vektor.html", next_label="Направление как вектор"),
    )
    write("19-10-koordinaty-kletki.html", out)


def build_11() -> None:
    body = f"""
    <h2>От четырёх if/elif к одному словарю</h2>
    <p>Первый прототип определял движение головы четырьмя ветками <code class="inline">if/elif</code>
    (раздел 19.4) — читаемо, но при добавлении новой логики (например, диагонального движения в
    другой игре) пришлось бы дублировать структуру снова. Направление можно представить иначе —
    как <strong>вектор смещения</strong>:</p>
    {direction_vector_diagram()}
    {code_block(
        "direction_vectors.py",
        "DIRECTION_VECTORS = {\n"
        '    Direction.UP: (0, STEP),\n'
        '    Direction.DOWN: (0, -STEP),\n'
        '    Direction.LEFT: (-STEP, 0),\n'
        '    Direction.RIGHT: (STEP, 0),\n'
        "}\n\n"
        "def next_head(head, direction):\n"
        "    dx, dy = DIRECTION_VECTORS[direction]\n"
        "    return (head[0] + dx, head[1] + dy)\n",
    )}
    {classic_vs_modern(
        "if/elif против словаря векторов",
        "Явно, но растёт с числом направлений",
        'if napravlenie == "up":\n'
        "    golova.sety(golova.ycor() + RAZMER_SHAGA)\n"
        'elif napravlenie == "down":\n'
        "    golova.sety(golova.ycor() - RAZMER_SHAGA)\n"
        "# ...и так для left, right",
        "Один словарь, одна формула",
        "dx, dy = DIRECTION_VECTORS[direction]\n"
        "new_x, new_y = x + dx, y + dy",
        "Оба варианта дают одинаковый результат для четырёх направлений. Разница появляется в "
        "том, как код растёт: словарь — это данные, а не ветвление, поэтому тестировать и "
        "расширять его проще, не трогая саму формулу движения.",
    )}

    {practice_card(
        "19-11",
        "Практика: направление как вектор",
        "Автоматическая проверка — next_head() для всех четырёх направлений",
        "../../practice/19-11/index.html",
    )}
    """
    out = render_page(
        page_title="Направление как вектор",
        description="DIRECTION_VECTORS — словарь направление → смещение (dx, dy) вместо цепочки if/elif.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Направление как вектор", "")],
        kicker="Глава 19 · Модель игры",
        h1="Направление как вектор",
        lede="Направление — это не строка, которую сравнивают в if/elif, а данные: пара чисел "
        "(dx, dy).",
        body_html=body,
        sidebar_groups=sidebar("19-11-napravlenie-kak-vektor.html"),
        nav=PageNav(prev_href="19-10-koordinaty-kletki.html", prev_label="Координаты клетки", next_href="19-12-odin-igrovoj-tik.html", next_label="Один игровой тик"),
    )
    write("19-11-napravlenie-kak-vektor.html", out)


def build_12() -> None:
    body = f"""
    <h2>Игровой тик — одно дискретное обновление игры</h2>
    <p>Игровой тик — не «один кадр анимации», а один полный цикл правил: применить направление,
    подвинуть голову, проверить еду, проверить столкновения, обновить модель. Отрисовка —
    отдельный, хоть и обычно смежный шаг:</p>
    {pipeline_diagram([
        {"kind": "plain", "title": "применить направление"},
        {"kind": "plain", "title": "next_head()"},
        {"kind": "object", "title": "проверка еды", "rows": ["съедено? → grow=True"]},
        {"kind": "object", "title": "move_snake()", "rows": ["новая голова + старое тело"]},
        {"kind": "plain", "title": "проверка столкновений"},
        {"kind": "object", "title": "render()"},
    ], caption="Один тик — это вся эта цепочка целиком, а не одно движение головы.")}
    {callout(
        "info",
        "Тик и render — разные понятия, даже если происходят вместе",
        "В этой простой игре каждый тик заканчивается отрисовкой — но это решение, а не "
        "обязательное правило. <code class=\"inline\">game_tick()</code> отвечает за ПРАВИЛА: что "
        "изменилось в модели. <code class=\"inline\">render()</code> отвечает только за то, чтобы "
        "показать текущую модель на экране. Раздел 19.29 разберёт эту границу подробнее — она "
        "станет важна, когда логика будет тестироваться без Turtle вообще (раздел 19.26).",
    )}

    {practice_card(
        "19-12",
        "Практика: порядок шагов одного тика",
        "Автоматическая проверка — что должно произойти раньше: проверка еды или столкновений",
        "../../practice/19-12/index.html",
    )}
    """
    out = render_page(
        page_title="Один игровой тик",
        description="Игровой тик — одно дискретное обновление правил игры: направление, движение, еда, столкновения.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Игровой тик", "")],
        kicker="Глава 19 · Модель игры",
        h1="Один игровой тик",
        lede="Тик — это вся цепочка правил целиком, а не одно движение головы по экрану.",
        body_html=body,
        sidebar_groups=sidebar("19-12-odin-igrovoj-tik.html"),
        nav=PageNav(prev_href="19-11-napravlenie-kak-vektor.html", prev_label="Направление как вектор", next_href="19-13-nastoyaschij-cikl.html", next_label="Настоящий игровой цикл"),
    )
    write("19-12-odin-igrovoj-tik.html", out)


def build_13() -> None:
    body = f"""
    <h2>while — не единственный способ повторять тики</h2>
    <p>Первый прототип запускает игру через <code class="inline">while igrovoj_shag(): screen.update()</code>
    — простой и понятный busy-цикл, который крутится без остановки, пока не наступит конец игры.
    У него есть цена: пока цикл выполняется, программа не может сделать ничего другого — ни
    поставить игру на паузу по нажатию клавиши, ни аккуратно изменить скорость на лету.</p>
    {code_block(
        "ontimer_cikl.py",
        "def game_tick(self):\n"
        "    if self.state.status is not GameStatus.RUNNING:\n"
        "        return\n"
        "    # ...применить направление, подвинуть голову, проверить еду и столкновения...\n"
        "    self.render()\n"
        "    self.screen.ontimer(self.game_tick, self.state.delay_ms)\n",
    )}
    {callout(
        "info",
        "screen.ontimer() планирует следующий тик, а не блокирует программу",
        "<code class=\"inline\">screen.ontimer(callback, delay_ms)</code> просит цикл событий "
        "Tkinter (тот же самый, что и в главе 17) вызвать <code class=\"inline\">callback</code> "
        "примерно через <code class=\"inline\">delay_ms</code> — и сразу возвращает управление. "
        "Между тиками программа полностью свободна: клавиатура, пауза, изменение скорости "
        "обрабатываются как обычные события, а не ждут своей очереди внутри цикла.",
    )}
    {callout(
        "warning",
        "time.sleep() в игровом цикле на Tkinter/Turtle — плохая идея",
        "<code class=\"inline\">time.sleep()</code> останавливает <em>весь</em> процесс, включая "
        "обработку событий — окно перестанет реагировать на клавиатуру и закрытие ровно на время "
        "сна. <code class=\"inline\">screen.ontimer()</code> ничего не блокирует: он передаёт "
        "часы циклу событий, который в это время продолжает обслуживать всё остальное.",
    )}
    <p>Каждый вызов <code class="inline">game_tick()</code> сам планирует следующий через
    <code class="inline">ontimer()</code> — получается цепочка, а не цикл в привычном смысле.
    Если <code class="inline">status</code> не <code class="inline">RUNNING</code>, тик тихо
    ничего не делает — и не планирует следующий: это и есть механизм паузы (раздел 19.22).</p>

    {local_required_card(
        "19-13",
        "Практика: игровой цикл на ontimer()",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/19-13/index.html",
    )}
    """
    out = render_page(
        page_title="Настоящий игровой цикл",
        description="screen.ontimer() вместо busy-цикла while — тики планируются друг за другом, не блокируя цикл событий.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Настоящий игровой цикл", "")],
        kicker="Глава 19 · Модель игры",
        h1="Настоящий игровой цикл",
        lede="screen.ontimer() планирует следующий тик и сразу возвращает управление — вместо "
        "того чтобы блокировать программу в while.",
        body_html=body,
        sidebar_groups=sidebar("19-13-nastoyaschij-cikl.html"),
        nav=PageNav(prev_href="19-12-odin-igrovoj-tik.html", prev_label="Один игровой тик", next_href="19-14-vremya-skorost.html", next_label="Время, скорость и задержка"),
    )
    write("19-13-nastoyaschij-cikl.html", out)


def build_14() -> None:
    body = f"""
    <h2>delay_ms — не гарантия, а просьба</h2>
    <p><code class="inline">screen.ontimer(game_tick, 120)</code> означает «вызови
    <code class="inline">game_tick</code> примерно через 120 миллисекунд, когда цикл событий "
    "сможет это сделать» — не «ровно через 120.000 мс». Если в этот момент цикл событий занят "
    "чем-то ещё (например, перерисовкой), вызов немного задержится. Для игры такого масштаба "
    "разница обычно незаметна, но обещать точное время не стоит.</p>
    {comparison_table(
        ["delay_ms", "Ощущение"],
        [
            ["200", "медленно — удобно для первого знакомства с управлением"],
            ["120", "нормальная скорость — значение по умолчанию"],
            ["70", "быстро — требует точных и быстрых реакций"],
        ],
    )}
    {code_block(
        "calculate_delay.py",
        "def calculate_delay(score, *, base_ms=140, min_ms=60, step_score=50, step_ms=10):\n"
        "    steps = score // step_score\n"
        "    return max(min_ms, base_ms - steps * step_ms)\n",
    )}
    {callout(
        "warning",
        "max() — обязательная защита от нуля и отрицательной задержки",
        "Без <code class=\"inline\">max(min_ms, ...)</code> достаточно высокий счёт рано или "
        "поздно довёл бы задержку до нуля или отрицательного числа. "
        "<code class=\"inline\">screen.ontimer(callback, 0)</code> формально не упадёт, но игра "
        "станет неиграбельно быстрой; отрицательное значение — и вовсе поведение, которое не "
        "стоит проверять на практике. <code class=\"inline\">min_ms</code> — жёсткая нижняя "
        "граница скорости.",
    )}

    {practice_card(
        "19-14",
        "Практика: задержка тика по счёту",
        "Автоматическая проверка — calculate_delay() уменьшается со счётом и не опускается ниже минимума",
        "../../practice/19-14/index.html",
    )}
    """
    out = render_page(
        page_title="Время, скорость и задержка",
        description="calculate_delay() — задержка между тиками уменьшается со счётом, но не опускается ниже минимума.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Время и скорость", "")],
        kicker="Глава 19 · Модель игры",
        h1="Время, скорость и задержка",
        lede="delay_ms — не точное время, а приблизительный интервал между тиками, который "
        "уменьшается по мере роста счёта.",
        body_html=body,
        sidebar_groups=sidebar("19-14-vremya-skorost.html"),
        nav=PageNav(prev_href="19-13-nastoyaschij-cikl.html", prev_label="Настоящий игровой цикл", next_href="19-15-sostoyanie-igry.html", next_label="Состояние игры"),
    )
    write("19-14-vremya-skorost.html", out)


def build_15() -> None:
    body = f"""
    <h2>Игра — это не только «идёт» или «не идёт»</h2>
    <p>Первый прототип знал только <code class="inline">igra_okonchena</code> — булево
    да/нет. Финальная версия различает четыре разных состояния, и переходы между ними —
    это не случайность, а чёткие правила:</p>
    {state_machine_diagram()}
    {comparison_table(
        ["Состояние", "Что происходит"],
        [
            ["READY", "змейка на месте, ждём первое нажатие направления — тики ещё не идут"],
            ["RUNNING", "тики планируются друг за другом через ontimer()"],
            ["PAUSED", "тики остановлены, модель не меняется, экран показывает «ПАУЗА»"],
            ["GAME_OVER", "столкновение произошло; ждём restart()"],
        ],
    )}
    {callout(
        "tip",
        "GameStatus как Enum — та же идея, что и Tool в главе 18",
        "Четыре состояния — конечный известный список, поэтому <code class=\"inline\">Enum</code> "
        "здесь так же оправдан, как <code class=\"inline\">Tool</code> для инструментов рисовалки: "
        "опечатку в имени состояния поймает редактор, а не тихий баг посреди игры.",
    )}

    {practice_card(
        "19-15",
        "Практика: переходы состояния игры",
        "Автоматическая проверка — какие переходы между READY/RUNNING/PAUSED/GAME_OVER легальны",
        "../../practice/19-15/index.html",
    )}
    """
    out = render_page(
        page_title="Состояние игры",
        description="READY, RUNNING, PAUSED, GAME_OVER — четыре состояния игры вместо одного булева флага.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Состояние игры", "")],
        kicker="Глава 19 · Модель игры",
        h1="Состояние игры",
        lede="Не просто «игра идёт или закончилась» — четыре чётких состояния с ясными "
        "переходами между ними.",
        body_html=body,
        sidebar_groups=sidebar("19-15-sostoyanie-igry.html"),
        nav=PageNav(prev_href="19-14-vremya-skorost.html", prev_label="Время и скорость", next_href="19-16-model-snake.html", next_label="Модель Snake"),
    )
    write("19-15-sostoyanie-igry.html", out)


def build_16() -> None:
    body = f"""
    <h2>Змейка как список позиций, а не список черепашек</h2>
    <p>Первый прототип хранит тело как список <em>объектов Turtle</em> — состояние игры и
    графика неразрывно связаны, ту же проблему глава 18 уже разбирала для Canvas (раздел 18.8).
    Финальная модель хранит змейку как обычный список координат:</p>
    {code_block(
        "model_snake.py",
        "snake = [\n"
        "    (0, 0),      # snake[0] — голова\n"
        "    (-20, 0),\n"
        "    (-40, 0),\n"
        "]\n",
    )}
    {class_diagram(
        "GameState (фрагмент)",
        ["snake: list[Position]", "direction: Direction"],
        [],
        caption="snake[0] — голова; snake[1:] — тело. Ни одного объекта Turtle внутри.",
    )}
    {callout(
        "info",
        "Отрисовка превращает позиции в Turtle-сегменты — не наоборот",
        "Модель ничего не знает о том, как выглядит змейка на экране. "
        "<code class=\"inline\">render()</code> (раздел 19.29) читает "
        "<code class=\"inline\">snake</code> и раскладывает координаты по уже существующим "
        "Turtle-сегментам — то же разделение «модель ≠ виджеты», что и "
        "<code class=\"inline\">render_document()</code> в PaintApp главы 18.",
    )}

    {practice_card(
        "19-16",
        "Практика: список позиций как модель Snake",
        "Автоматическая проверка — snake[0] это голова, длина списка равна числу сегментов",
        "../../practice/19-16/index.html",
    )}
    """
    out = render_page(
        page_title="Голова, тело и модель Snake",
        description="Змейка как список логических позиций (Position), а не список объектов Turtle — snake[0] всегда голова.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Модель Snake", "")],
        kicker="Глава 19 · Модель игры",
        h1="Голова, тело и модель Snake",
        lede="Список координат вместо списка Turtle-объектов — snake[0] это голова, остальное "
        "— тело.",
        body_html=body,
        sidebar_groups=sidebar("19-16-model-snake.html"),
        nav=PageNav(prev_href="19-15-sostoyanie-igry.html", prev_label="Состояние игры", next_href="19-17-pochemu-s-hvosta.html", next_label="Почему тело движется с хвоста"),
    )
    write("19-16-model-snake.html", out)


def build_17() -> None:
    body = f"""
    <h2>Порядок обновления сегментов — не деталь, а необходимость</h2>
    <p>Раздел 19.6 уже показал правило: тело обновляется с хвоста, каждый сегмент занимает
    место <em>предыдущего</em>. Разберём, что случится, если поменять порядок на
    противоположный — от головы к хвосту:</p>
    {before_after_grid(
        [(2, 0), (1, 0), (0, 0)], [(3, 0), (2, 0), (1, 0)],
        caption_before="было: H-S1-S2", caption_after="стало (правильно): каждый унаследовал позицию предыдущего",
    )}
    {code_block(
        "ot_hvosta.py",
        "def dvigat_telo():\n"
        "    for indeks in range(len(segmenty) - 1, 0, -1):\n"
        "        # segmenty[indeks] получает СТАРУЮ позицию segmenty[indeks - 1]\n"
        "        x = segmenty[indeks - 1].xcor()\n"
        "        y = segmenty[indeks - 1].ycor()\n"
        "        segmenty[indeks].goto(x, y)\n",
    )}
    {callout(
        "warning",
        "От головы к хвосту — сегменты схлопываются в одну точку",
        "Если пойти в обратном порядке, <code class=\"inline\">segmenty[0]</code> первым "
        "получит позицию головы. На следующей итерации "
        "<code class=\"inline\">segmenty[1]</code> прочитает координаты "
        "<code class=\"inline\">segmenty[0]</code> — но это уже НОВАЯ, только что "
        "перезаписанная позиция, а не старая. Через несколько итераций все сегменты окажутся "
        "в одной и той же точке — змейка визуально схлопнется в квадрат.",
    )}
    <p>Раздел 19.18 покажет более элегантную альтернативу этому циклу — модель «новая голова +
    старое тело», которая вообще не двигает существующие сегменты по отдельности.</p>

    {practice_card(
        "19-17",
        "Практика: правильный порядок обновления тела",
        "Автоматическая проверка — движение от хвоста к голове не теряет позиции",
        "../../practice/19-17/index.html",
    )}
    """
    out = render_page(
        page_title="Почему тело движется с хвоста",
        description="Обновление тела от хвоста к голове — единственный порядок, который не теряет позиции сегментов.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Почему с хвоста", "")],
        kicker="Глава 19 · Модель игры",
        h1="Почему тело движется с хвоста",
        lede="Обновление в обратном порядке схлопывает все сегменты в одну точку — разберём, "
        "почему.",
        body_html=body,
        sidebar_groups=sidebar("19-17-pochemu-s-hvosta.html"),
        nav=PageNav(prev_href="19-16-model-snake.html", prev_label="Модель Snake", next_href="19-18-eda-svobodnaya-kletka.html", next_label="Еда и свободная клетка"),
    )
    write("19-17-pochemu-s-hvosta.html", out)


# ---------------------------------------------------------------------------
# 19.18 – 19.25: еда, столкновения, Game Over, pause, restart, скорость, рекорд
# ---------------------------------------------------------------------------

def build_18() -> None:
    body = f"""
    <h2>Элегантная альтернатива циклу по сегментам</h2>
    <p>Вместо того чтобы двигать каждый существующий сегмент по отдельности (раздел 19.17),
    можно построить новый список целиком — новая голова спереди, старое тело позади, без
    последнего элемента (если змейка не растёт):</p>
    {before_after_grid(
        [(2, 0), (1, 0), (0, 0)], [(3, 0), (2, 0), (1, 0)],
        caption_before="snake до", caption_after="[новая_голова] + snake[:-1]",
    )}
    {code_block(
        "move_snake.py",
        "def move_snake(snake, new_head, *, grow):\n"
        "    if grow:\n"
        "        return [new_head, *snake]\n"
        "    return [new_head, *snake[:-1]]\n",
    )}
    <p>Хвост при этом естественным образом «отваливается» — <code class="inline">snake[:-1]</code>
    отбрасывает последний элемент. Никакого цикла, никакого риска перепутать порядок обновления:
    результат строится за один проход, а не мутирует существующие позиции одну за другой.</p>

    <h2>Еда — случайная свободная клетка</h2>
    <p>Раздел 19.3 выбирала случайную клетку без проверки — при достаточно длинной змейке яблоко
    иногда оказывалось бы прямо внутри тела. Честная версия выбирает только среди по-настоящему
    свободных клеток:</p>
    {code_block(
        "choose_food.py",
        "def choose_food(snake, rng, *, half=280, step=20):\n"
        "    occupied = set(snake)\n"
        "    free = tuple(\n"
        "        cell for cell in all_cells(half=half, step=step) if cell not in occupied\n"
        "    )\n"
        "    return rng.choice(free)\n",
    )}
    {callout(
        "tip",
        "rng как параметр — та же идея пригодится в разделе 19.30",
        "<code class=\"inline\">choose_food()</code> принимает готовый "
        "<code class=\"inline\">random.Random</code>, а не читает глобальный "
        "<code class=\"inline\">random</code> модуль напрямую. В реальной игре передают "
        "<code class=\"inline\">random.Random()</code> — настоящую случайность; в тестах —  "
        "<code class=\"inline\">random.Random(seed)</code> с фиксированным зерном, чтобы "
        "результат был предсказуем и его можно было проверить <code class=\"inline\">assert</code>-ом.",
    )}

    {practice_card(
        "19-18",
        "Практика: еда только на свободной клетке",
        "Автоматическая проверка — choose_food() никогда не совпадает с телом змейки",
        "../../practice/19-18/index.html",
    )}
    """
    out = render_page(
        page_title="Еда и свободная клетка",
        description="move_snake() как новая голова плюс старое тело, и choose_food() — еда только на свободной клетке.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Еда и свободная клетка", "")],
        kicker="Глава 19 · Правила игры",
        h1="Еда и свободная клетка",
        lede="Новая голова плюс старое тело строит движение за один проход — и та же идея "
        "множества свободных клеток решает, куда честно поставить еду.",
        body_html=body,
        sidebar_groups=sidebar("19-18-eda-svobodnaya-kletka.html"),
        nav=PageNav(prev_href="19-17-pochemu-s-hvosta.html", prev_label="Почему с хвоста", next_href="19-19-stolknovenie-so-stenoj.html", next_label="Столкновение со стеной"),
    )
    write("19-18-eda-svobodnaya-kletka.html", out)


def build_19() -> None:
    body = f"""
    <h2>Граница — координата центра сегмента, а не края экрана</h2>
    <p><code class="inline">GRANICA = 280</code> — это не размер окна (600×600), а предел для
    координаты <em>центра</em> головы. При толщине сегмента в 20 пикселей голова с центром
    ровно в 280 всё ещё целиком помещается на видимом поле; на 300 она бы уже выходила за
    край.</p>
    {code_block(
        "is_wall_collision.py",
        "def is_wall_collision(head, *, half=280):\n"
        "    x, y = head\n"
        "    return abs(x) > half or abs(y) > half\n",
    )}
    {comparison_table(
        ["Позиция головы", "is_wall_collision()"],
        [
            ["(280, 0)", "False — легальная граница"],
            ["(-280, -280)", "False — легальная граница, угол поля"],
            ["(300, 0)", "True — уже за пределами"],
        ],
    )}
    {callout(
        "info",
        "Строгое сравнение (>), не (>=) — граница включена",
        "Если бы проверка использовала <code class=\"inline\">&gt;=</code>, легальная позиция "
        "<code class=\"inline\">280</code> уже считалась бы столкновением — змейка не смогла бы "
        "доехать до самого края поля. Раздел 19.51 разбирает эти пограничные случаи как отдельные "
        "тесты, а не только на словах.",
    )}

    {practice_card(
        "19-19",
        "Практика: граница поля",
        "Автоматическая проверка — is_wall_collision() на самой границе и за ней",
        "../../practice/19-19/index.html",
    )}
    """
    out = render_page(
        page_title="Столкновение со стеной",
        description="is_wall_collision() и точная граница поля — координата центра сегмента, а не край окна.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Столкновение со стеной", "")],
        kicker="Глава 19 · Правила игры",
        h1="Столкновение со стеной",
        lede="GRANICA — предел координаты центра головы, а не размер окна; граница включена в "
        "легальную область.",
        body_html=body,
        sidebar_groups=sidebar("19-19-stolknovenie-so-stenoj.html"),
        nav=PageNav(prev_href="19-18-eda-svobodnaya-kletka.html", prev_label="Еда и свободная клетка", next_href="19-20-stolknovenie-s-soboj.html", next_label="Столкновение с собой"),
    )
    write("19-19-stolknovenie-so-stenoj.html", out)


def build_20() -> None:
    body = f"""
    <h2>Заезд в клетку хвоста — не всегда столкновение</h2>
    <p>Классическое правило «Змейки»: если змейка не растёт, хвост в этот же тик освобождает
    свою клетку — заехать туда головой законно. Если растёт — хвост никуда не девается, и та же
    самая клетка уже занята.</p>
    {code_block(
        "is_self_collision.py",
        "def is_self_collision(new_head, body_after_move):\n"
        "    # body_after_move — тело ПОСЛЕ move_snake(), без самой головы\n"
        "    return new_head in body_after_move\n",
    )}
    {callout(
        "warning",
        "Проверять нужно тело ПОСЛЕ движения, а не до",
        "Если проверить <code class=\"inline\">new_head in snake[1:]</code> на СТАРОМ списке "
        "(до <code class=\"inline\">move_snake()</code>), клетка старого хвоста всё ещё будет в "
        "списке — и легальный заезд в неё ошибочно посчитается столкновением. Правильная "
        "проверка идёт против <code class=\"inline\">move_snake(...)[1:]</code> — тела, каким оно "
        "станет ПОСЛЕ хода, а не каким было до него.",
    )}
    {comparison_table(
        ["Ситуация", "is_self_collision()"],
        [
            ["Голова заезжает в клетку старого хвоста, змейка не растёт", "False — хвост уже освободил клетку"],
            ["Голова заезжает в клетку старого хвоста, змейка растёт", "True — хвост никуда не делся"],
            ["Голова заезжает в клетку середины тела", "True — настоящее столкновение"],
        ],
    )}

    {practice_card(
        "19-20",
        "Практика: столкновение с собственным телом",
        "Автоматическая проверка — заезд в клетку хвоста легален, заезд в середину тела — нет",
        "../../practice/19-20/index.html",
    )}
    """
    out = render_page(
        page_title="Столкновение с собой",
        description="is_self_collision() против тела ПОСЛЕ move_snake() — заезд в клетку освободившегося хвоста легален.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Столкновение с собой", "")],
        kicker="Глава 19 · Правила игры",
        h1="Столкновение с собой",
        lede="Проверять нужно тело после хода, а не до — иначе легальный заезд в клетку "
        "освободившегося хвоста ошибочно засчитается столкновением.",
        body_html=body,
        sidebar_groups=sidebar("19-20-stolknovenie-s-soboj.html"),
        nav=PageNav(prev_href="19-19-stolknovenie-so-stenoj.html", prev_label="Столкновение со стеной", next_href="19-21-game-over.html", next_label="Game Over"),
    )
    write("19-20-stolknovenie-s-soboj.html", out)


def build_21() -> None:
    body = f"""
    <h2>Game Over — состояние, а не только надпись на экране</h2>
    {image_figure(f"{IMG}/snake-self-collision.png", "Реальное окно: неподвижная змейка S-образной формы, поверх поля крупная надпись GAME OVER и счёт", "Реальное окно: столкновение с собственным телом переводит игру в GAME_OVER — та же надпись появилась бы и при столкновении со стеной.", width=420)}
    <p>Когда <code class="inline">is_wall_collision()</code> или <code class="inline">is_self_collision()</code>
    возвращают True, тик не просто останавливает движение — он переводит
    <code class="inline">state.status</code> в <code class="inline">GAME_OVER</code> и рисует
    оверлей поверх последнего кадра игры:</p>
    {code_block(
        "game_over.py",
        "if is_wall_collision(head):\n"
        "    state.status = GameStatus.GAME_OVER\n"
        "    self.render()\n"
        '    self._show_overlay("GAME OVER", f"Счёт: {state.score}  |  R — новая игра")\n'
        "    return\n",
    )}
    {callout(
        "info",
        "GAME_OVER не запускает больше тиков",
        "<code class=\"inline\">game_tick()</code> в самом начале проверяет "
        "<code class=\"inline\">if state.status is not RUNNING: return</code> — "
        "<code class=\"inline\">GAME_OVER</code> сюда попадает точно так же, как "
        "<code class=\"inline\">PAUSED</code>. Единственный способ снова сдвинуться с места — "
        "<code class=\"inline\">restart()</code> (раздел 19.23), который явно создаёт новое "
        "состояние.",
    )}

    {practice_card(
        "19-21",
        "Практика: переход в GAME_OVER",
        "Автоматическая проверка — какие столкновения переводят игру в GAME_OVER",
        "../../practice/19-21/index.html",
    )}
    """
    out = render_page(
        page_title="Game Over как состояние",
        description="Столкновение переводит state.status в GAME_OVER — тики останавливаются, экран показывает счёт и подсказку restart.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Game Over", "")],
        kicker="Глава 19 · Правила игры",
        h1="Game Over как состояние",
        lede="Столкновение не просто останавливает движение — оно переводит игру в отдельное "
        "состояние GAME_OVER.",
        body_html=body,
        sidebar_groups=sidebar("19-21-game-over.html"),
        nav=PageNav(prev_href="19-20-stolknovenie-s-soboj.html", prev_label="Столкновение с собой", next_href="19-22-pauza.html", next_label="Pause / Resume"),
    )
    write("19-21-game-over.html", out)


def build_22() -> None:
    body = f"""
    <h2>Пауза останавливает тики, а не рисует поверх бегущей игры</h2>
    {image_figure(f"{IMG}/snake-pause-strip.png", "Два реальных окна рядом: слева игра идёт, справа надпись ПАУЗА и подсказка Space — продолжить поверх того же кадра", "Реальное окно: toggle_pause() не двигает змейку дальше — кадр справа тот же самый, что и слева, только с оверлеем.", width=760)}
    <p>Клавиша <code class="inline">Space</code> переключает игру между <code class="inline">RUNNING</code>
    и <code class="inline">PAUSED</code>:</p>
    {code_block(
        "toggle_pause.py",
        "def toggle_pause(self):\n"
        "    if self.state.status is GameStatus.RUNNING:\n"
        "        self.state.status = GameStatus.PAUSED\n"
        '        self._show_overlay("ПАУЗА", "Space — продолжить")\n'
        "    elif self.state.status is GameStatus.PAUSED:\n"
        "        self.state.status = GameStatus.RUNNING\n"
        "        self._clear_overlay()\n"
        "        self._schedule_next_tick()   # цепочка тиков остановилась — нужно запустить заново\n",
    )}
    {callout(
        "warning",
        "Пауза не пересоздаёт змейку",
        "<code class=\"inline\">toggle_pause()</code> не трогает <code class=\"inline\">state.snake</code>, "
        "<code class=\"inline\">state.score</code> или <code class=\"inline\">state.food</code> — "
        "меняется только <code class=\"inline\">status</code>. Возобновление продолжает ту же "
        "самую игру с того же места, а не начинает новую.",
    )}
    <p>Важная деталь: когда <code class="inline">status</code> становится <code class="inline">PAUSED</code>,
    цепочка запланированных тиков (раздел 19.13) обрывается сама — следующий
    <code class="inline">_on_timer()</code> увидит <code class="inline">status != RUNNING</code>
    внутри <code class="inline">game_tick()</code> и просто ничего не сделает, не планируя
    следующий тик. Поэтому возобновление обязано явно вызвать
    <code class="inline">_schedule_next_tick()</code> заново — иначе игра останется «включена»,
    но без единого тика вперёд.</p>

    {practice_card(
        "19-22",
        "Практика: pause не двигает состояние",
        "Автоматическая проверка — тик во время PAUSED не меняет змейку",
        "../../practice/19-22/index.html",
    )}
    """
    out = render_page(
        page_title="Pause / Resume",
        description="toggle_pause() останавливает цепочку тиков без изменения состояния змейки — возобновление запускает тики заново.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Pause / Resume", "")],
        kicker="Глава 19 · Функции игры",
        h1="Pause / Resume",
        lede="Пауза замораживает модель на месте — возобновление продолжает ту же игру, не "
        "начинает новую.",
        body_html=body,
        sidebar_groups=sidebar("19-22-pauza.html"),
        nav=PageNav(prev_href="19-21-game-over.html", prev_label="Game Over", next_href="19-23-restart.html", next_label="Restart / New Game"),
    )
    write("19-22-pauza.html", out)


def build_23() -> None:
    body = f"""
    <h2>Restart обязан оборвать старую цепочку тиков</h2>
    {image_figure(f"{IMG}/snake-restarted.png", "Реальное окно: свежая игра с одной головой в центре, табло Счёт: 0 Рекорд: 40", "Реальное окно после restart(): свежая змейка, счёт обнулён, рекорд остался.", width=420)}
    <p>Restart не просто возвращает змейку в исходную позицию — раздел 19.27 предупреждал:
    если старая цепочка <code class="inline">ontimer()</code> всё ещё тикает, у игры на
    мгновение оказалось бы два независимых потока обновлений одновременно (глава 16 уже
    разбирала похожую проблему с повторным нажатием кнопки).</p>
    {code_block(
        "restart.py",
        "def restart(self):\n"
        "    self._generation += 1   # обрывает любую ещё тикающую цепочку прошлой игры\n"
        "    high_score = self.state.high_score\n"
        "    self.state = new_game_state(self.rng, high_score=high_score)\n"
        "    self._clear_overlay()\n"
        "    self.render()\n",
    )}
    {code_block(
        "generation_guard.py",
        "def _schedule_next_tick(self):\n"
        "    generation = self._generation\n"
        "    self.screen.ontimer(lambda: self._on_timer(generation), self.state.delay_ms)\n\n"
        "def _on_timer(self, generation):\n"
        "    if generation != self._generation:\n"
        "        return   # просроченная цепочка от игры до restart() — сама себя гасит\n"
        "    self.game_tick()\n"
        "    if self.state.status is GameStatus.RUNNING:\n"
        "        self._schedule_next_tick()\n",
    )}
    {callout(
        "info",
        "Поколение (generation) — простой счётчик, не сложная архитектура",
        "Каждый <code class=\"inline\">restart()</code> увеличивает "
        "<code class=\"inline\">_generation</code> на единицу. Любой уже запланированный "
        "<code class=\"inline\">_on_timer()</code> запомнил СТАРОЕ значение — когда он наконец "
        "сработает, число не совпадёт, и он тихо ничего не сделает вместо того, чтобы двигать "
        "уже несуществующую змейку прошлой игры.",
    )}
    <p><code class="inline">high_score</code> — единственное поле, которое restart переносит из
    старого состояния в новое; всё остальное создаётся заново через
    <code class="inline">new_game_state()</code> (раздел 19.25).</p>

    {practice_card(
        "19-23",
        "Практика: restart и просроченные тики",
        "Автоматическая проверка — старый _on_timer() после restart() не двигает новую игру",
        "../../practice/19-23/index.html",
    )}
    """
    out = render_page(
        page_title="Restart / New Game",
        description="restart() увеличивает поколение (generation), чтобы просроченная цепочка ontimer() от старой игры сама себя остановила.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Restart", "")],
        kicker="Глава 19 · Функции игры",
        h1="Restart / New Game",
        lede="Новая игра обязана оборвать старую цепочку тиков — иначе на мгновение окажется "
        "два параллельных игровых потока.",
        body_html=body,
        sidebar_groups=sidebar("19-23-restart.html"),
        nav=PageNav(prev_href="19-22-pauza.html", prev_label="Pause / Resume", next_href="19-24-skorost-slozhnost.html", next_label="Скорость и сложность"),
    )
    write("19-23-restart.html", out)


def build_24() -> None:
    body = f"""
    <h2>Игра ускоряется вместе со счётом</h2>
    {image_figure(f"{IMG}/snake-fast-speed.png", "Реальное окно: змейка из пяти сегментов, счёт 450, яблоко в верхней части поля", "Реальное окно: при высоком счёте calculate_delay() уже упёрлась в минимум — игра идёт на предельной скорости.", width=420)}
    <p>Раздел 19.14 уже показал формулу — здесь она подключается к самой игре: после каждого
    съеденного яблока пересчитывается не только счёт, но и задержка следующего тика:</p>
    {code_block(
        "speed_progression.py",
        "if grow:\n"
        "    state.score += FOOD_SCORE\n"
        "    state.high_score = max(state.high_score, state.score)\n"
        "    state.food = choose_food(state.snake, self.rng)\n"
        "    state.delay_ms = calculate_delay(state.score)\n",
    )}
    <p>Новое значение <code class="inline">delay_ms</code> вступит в силу на следующем вызове
    <code class="inline">_schedule_next_tick()</code> — предыдущий тик уже был запланирован со
    старой задержкой, и это нормально: скорость меняется плавно, не рывком.</p>
    {callout(
        "tip",
        "min_ms — сознательный предел, а не случайность",
        "Раздел 19.14 уже объяснял <code class=\"inline\">max(min_ms, ...)</code> — здесь видно, "
        "зачем он нужен на практике: без него достаточно долгая игра рано или поздно довела бы "
        "задержку до нуля.",
    )}

    {practice_card(
        "19-24",
        "Практика: скорость растёт со счётом",
        "Автоматическая проверка — задержка тика уменьшается по мере роста счёта и не опускается ниже минимума",
        "../../practice/19-24/index.html",
    )}
    """
    out = render_page(
        page_title="Скорость и рост сложности",
        description="Каждое съеденное яблоко пересчитывает delay_ms через calculate_delay() — игра ускоряется вместе со счётом.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Скорость и сложность", "")],
        kicker="Глава 19 · Функции игры",
        h1="Скорость и рост сложности",
        lede="Каждое яблоко не только увеличивает счёт, но и пересчитывает задержку — игра "
        "постепенно ускоряется.",
        body_html=body,
        sidebar_groups=sidebar("19-24-skorost-slozhnost.html"),
        nav=PageNav(prev_href="19-23-restart.html", prev_label="Restart", next_href="19-25-high-score.html", next_label="High Score"),
    )
    write("19-24-skorost-slozhnost.html", out)


def build_25() -> None:
    body = f"""
    <h2>Рекорд переживает рестарт — счёт нет</h2>
    {image_figure(f"{IMG}/snake-high-score.png", "Реальное окно: одна голова в центре поля, табло сверху показывает Счёт: 0 Рекорд: 40", "Реальное окно: после restart() счёт обнулился, а рекорд остался прежним.", width=420)}
    <p><code class="inline">score</code> и <code class="inline">high_score</code> — два разных
    поля с разным временем жизни. Раздел 19.23 уже показал, что
    <code class="inline">restart()</code> явно передаёт <code class="inline">high_score</code> в
    новое состояние, а не создаёт его заново:</p>
    {code_block(
        "high_score.py",
        "def new_game_state(rng, *, high_score=0):\n"
        "    snake = [(0, 0)]\n"
        "    return GameState(\n"
        "        snake=snake,\n"
        "        # ...\n"
        "        score=0,               # всегда с нуля\n"
        "        high_score=high_score, # передан вызывающим кодом\n"
        "        # ...\n"
        "    )\n",
    )}
    {comparison_table(
        ["Поле", "Что происходит при restart()"],
        [
            ["score", "всегда сбрасывается в 0 — новая игра начинается с чистого счёта"],
            ["high_score", "передаётся из прошлого state.high_score — переживает рестарт"],
        ],
    )}
    {callout(
        "info",
        "high_score обновляется в момент max(), а не в конце игры",
        "<code class=\"inline\">state.high_score = max(state.high_score, state.score)</code> "
        "вызывается сразу при каждом съеденном яблоке (раздел 19.24) — рекорд не нужно "
        "«подводить» отдельно в конце: он уже точен в любой момент игры, включая экран Game "
        "Over.",
    )}

    {practice_card(
        "19-25",
        "Практика: рекорд переживает рестарт",
        "Автоматическая проверка — high_score не обнуляется, а score всегда с нуля",
        "../../practice/19-25/index.html",
    )}
    """
    out = render_page(
        page_title="High Score",
        description="high_score сохраняется между рестартами через явную передачу в new_game_state(), в отличие от score.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("High Score", "")],
        kicker="Глава 19 · Функции игры",
        h1="High Score",
        lede="score и high_score — разные поля с разным временем жизни: одно обнуляется при "
        "рестарте, другое переживает его.",
        body_html=body,
        sidebar_groups=sidebar("19-25-high-score.html"),
        nav=PageNav(prev_href="19-24-skorost-slozhnost.html", prev_label="Скорость и сложность", next_href="19-26-chistaya-logika.html", next_label="Чистая логика без Turtle"),
    )
    write("19-25-high-score.html", out)


# ---------------------------------------------------------------------------
# 19.26 – 19.33: чистая логика, архитектура, тесты, Debug Labs, финал, итоги
# ---------------------------------------------------------------------------

def build_26() -> None:
    body = f"""
    <h2>Ни одна из функций правил не открывает окно</h2>
    <p>Оглянемся на все функции, разобранные с раздела 19.9: <code class="inline">next_head()</code>,
    <code class="inline">move_snake()</code>, <code class="inline">is_wall_collision()</code>,
    <code class="inline">is_self_collision()</code>, <code class="inline">choose_food()</code>,
    <code class="inline">calculate_delay()</code>. Ни одна из них не создаёт
    <code class="inline">turtle.Turtle()</code>, не читает <code class="inline">golova.xcor()</code>
    и вообще ничего не знает про экран:</p>
    {capability_map([
        ("next_head(head, direction)", ["кортеж → кортеж", "raздел 19.11"]),
        ("move_snake(snake, head, grow)", ["список → список", "раздел 19.18"]),
        ("is_wall_collision(head)", ["кортеж → bool", "раздел 19.19"]),
        ("is_self_collision(head, body)", ["кортеж, список → bool", "раздел 19.20"]),
        ("choose_food(snake, rng)", ["список → кортеж", "раздел 19.18"]),
        ("calculate_delay(score)", ["int → int", "раздел 19.14"]),
    ], title="Правила игры — обычные функции над числами и списками")}
    <p>Это не случайность, а сознательное разделение: правила «Змейки» — это математика над
    координатами, а Turtle — только один из способов эту математику <em>показать</em>. Раздел
    19.30 использует ровно это свойство, чтобы протестировать правила напрямую, без единого
    настоящего окна.</p>
    {callout(
        "tip",
        "Тот же принцип, что и в главе 18",
        "<code class=\"inline\">normalize_bounds()</code> и <code class=\"inline\">Shape</code> "
        "в PaintApp (глава 18) были ровно такими же — чистыми функциями и данными без "
        "<code class=\"inline\">tkinter</code> внутри. Пользы от этого две: логику проще "
        "тестировать, и её проще понять — читая функцию, не нужно держать в голове состояние "
        "целого окна.",
    )}

    {practice_card(
        "19-26",
        "Практика: какие функции — чистая логика",
        "Автоматическая проверка — отличаем функции без Turtle от кода, которому нужен экран",
        "../../practice/19-26/index.html",
    )}
    """
    out = render_page(
        page_title="Чистая игровая логика без Turtle",
        description="next_head, move_snake, is_wall_collision, is_self_collision, choose_food, calculate_delay — ни одна не знает про экран.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Чистая логика", "")],
        kicker="Глава 19 · Архитектура",
        h1="Чистая игровая логика без Turtle",
        lede="Правила игры — обычные функции над числами и списками; Turtle нужен только для "
        "того, чтобы их показать.",
        body_html=body,
        sidebar_groups=sidebar("19-26-chistaya-logika.html"),
        nav=PageNav(prev_href="19-25-high-score.html", prev_label="High Score", next_href="19-27-gamestate-dataclass.html", next_label="GameState с dataclass"),
    )
    write("19-26-chistaya-logika.html", out)


def build_27() -> None:
    body = f"""
    <h2>Одна структура вместо восьми отдельных переменных</h2>
    <p>Собираем все поля, разобранные по частям — змейку, направление, еду, счёт, статус,
    скорость — в один <code class="inline">@dataclass</code>, ту же идею, что и
    <code class="inline">DrawingState</code> в главе 18:</p>
    {class_diagram(
        "GameState",
        ["snake: list[Position]", "direction: Direction", "next_direction: Direction",
         "food: Position", "score: int", "high_score: int", "status: GameStatus", "delay_ms: int"],
        [],
        caption="Ни одного объекта Turtle — только данные, которые полностью описывают текущую игру.",
    )}
    {code_block(
        "gamestate.py",
        "@dataclass\n"
        "class GameState:\n"
        "    snake: list[Position] = field(default_factory=lambda: [(0, 0)])\n"
        "    direction: Direction = Direction.RIGHT\n"
        "    next_direction: Direction = Direction.RIGHT\n"
        "    food: Position = (0, 0)\n"
        "    score: int = 0\n"
        "    high_score: int = 0\n"
        "    status: GameStatus = GameStatus.READY\n"
        "    delay_ms: int = BASE_DELAY_MS\n",
    )}
    {callout(
        "warning",
        "Соблазн сохранить сюда Turtle-объект — частая ошибка",
        "Если положить <code class=\"inline\">head_turtle</code> внутрь "
        "<code class=\"inline\">GameState</code>, тесты из раздела 19.30 перестанут работать без "
        "настоящего окна, а «модель» перестанет быть моделью — она снова срастётся с "
        "отображением, как в первом прототипе. Раздел 19.31 разбирает эту ошибку как отдельный "
        "Debug Lab.",
    )}
    <p><code class="inline">next_direction</code> — отдельное от <code class="inline">direction</code>
    поле неспроста: раздел 19.48 объясняет, зачем клавиатура запрашивает направление, а не
    меняет его напрямую.</p>

    {practice_card(
        "19-27",
        "Практика: конструируем и сравниваем GameState",
        "Автоматическая проверка — создание, сравнение и обновление полей GameState",
        "../../practice/19-27/index.html",
    )}
    """
    out = render_page(
        page_title="GameState с dataclass",
        description="Все поля игры — snake, direction, food, score, status, delay_ms — в одном dataclass без объектов Turtle.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("GameState", "")],
        kicker="Глава 19 · Архитектура",
        h1="GameState с dataclass",
        lede="Одна структура данных описывает всю игру целиком — без единого объекта Turtle "
        "внутри.",
        body_html=body,
        sidebar_groups=sidebar("19-27-gamestate-dataclass.html"),
        nav=PageNav(prev_href="19-26-chistaya-logika.html", prev_label="Чистая логика", next_href="19-28-snakeapp-arhitektura.html", next_label="Архитектура SnakeApp"),
    )
    write("19-27-gamestate-dataclass.html", out)


def build_28() -> None:
    body = f"""
    <h2>app HAS-A screen — тот же паттерн, что и в главах 16–18</h2>
    {object_diagram(
        "app", "SnakeApp",
        [("screen", "Screen"), ("state", "GameState"), ("rng", "random.Random"),
         ("head", "Turtle"), ("food_turtle", "Turtle"), ("_segment_pool", "list[Turtle]")],
        caption="app хранит и виджеты Turtle, и модель (state) — но не путает их друг с другом.",
    )}
    {comparison_table(
        ["Группа методов", "За что отвечает"],
        [
            ["<code class=\"inline\">bind_keys</code>", "построение обработчиков клавиатуры — один раз, при запуске"],
            ["<code class=\"inline\">request_direction</code>", "клавиша → запрос направления, без движения прямо сейчас"],
            ["<code class=\"inline\">game_tick</code>", "события мыши... то есть тика → изменения state"],
            ["<code class=\"inline\">render</code>", "state → Turtle (единственное место, которое рисует по-настоящему)"],
            ["<code class=\"inline\">toggle_pause / restart</code>", "управление жизненным циклом игры"],
        ],
    )}
    {callout(
        "info",
        "SnakeApp не наследуется от turtle.Screen",
        "Как и <code class=\"inline\">PaintApp(tk.Tk)</code> в главе 18, наследование здесь "
        "технически возможно, но не выбрано: <code class=\"inline\">self.screen</code> — "
        "отдельный атрибут, а не сам объект <code class=\"inline\">SnakeApp</code>. Композиция "
        "делает границу между «моей логикой» и «внутренностями Turtle» явной.",
    )}

    {local_required_card(
        "19-28",
        "Практика: собираем объектный граф SnakeApp",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/19-28/index.html",
    )}
    """
    out = render_page(
        page_title="SnakeApp: отделяем модель от визуализации",
        description="SnakeApp хранит state (GameState) и Turtle-виджеты отдельно, композицией, а не наследованием от Screen.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Архитектура SnakeApp", "")],
        kicker="Глава 19 · Архитектура",
        h1="SnakeApp: отделяем модель от визуализации",
        lede="app.state — модель игры; app.screen и Turtle-объекты — только то, что видно на "
        "экране.",
        body_html=body,
        sidebar_groups=sidebar("19-28-snakeapp-arhitektura.html"),
        nav=PageNav(prev_href="19-27-gamestate-dataclass.html", prev_label="GameState", next_href="19-29-render-model.html", next_label="Render: модель → Turtle"),
    )
    write("19-28-snakeapp-arhitektura.html", out)


def build_29() -> None:
    body = f"""
    <h2>render() не создаёт новые сегменты на каждом тике</h2>
    {image_figure(f"{IMG}/snake-grid-demo.png", "Реальное окно: тонкая фиолетовая сетка на поле, подписанные клетки head cell и food cell", "Реальное окно: та же сетка из раздела 19.9, но теперь видно, как голова и еда — просто клетки, которые render() превращает в конкретные Turtle-объекты.", width=420)}
    <p>Раздел 18.35 главы 18 уже вводил идею пула сегментов для рисовалки — здесь та же техника
    решает похожую проблему: змейка растёт, но создавать новый <code class="inline">turtle.Turtle()</code>
    на каждое яблоко было бы расточительно, если тело потом может понадобиться отрисовать снова
    в следующем кадре.</p>
    {code_block(
        "render.py",
        "def render(self):\n"
        "    self.head.goto(*self.state.snake[0])\n\n"
        "    body = self.state.snake[1:]\n"
        "    self._ensure_segment_pool(len(body))\n"
        "    for i, segment in enumerate(self._segment_pool):\n"
        "        if i < len(body):\n"
        "            segment.showturtle()\n"
        "            segment.goto(*body[i])\n"
        "        else:\n"
        "            segment.hideturtle()\n\n"
        "    self.food_turtle.goto(*self.state.food)\n"
        "    self._render_scoreboard()\n"
        "    self.screen.update()\n",
    )}
    {callout(
        "info",
        "Пул растёт, но никогда не уменьшается сам по себе",
        "<code class=\"inline\">_ensure_segment_pool()</code> добавляет новые Turtle-сегменты, "
        "только если их не хватает — уже существующие переиспользуются. Когда змейка становится "
        "короче (после <code class=\"inline\">restart()</code>), лишние сегменты не удаляются, а "
        "просто прячутся через <code class=\"inline\">hideturtle()</code> — на следующей долгой "
        "игре они снова понадобятся, и пересоздавать их не придётся.",
    )}

    {local_required_card(
        "19-29",
        "Практика: render() и пул сегментов",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/19-29/index.html",
    )}
    """
    out = render_page(
        page_title="Render: модель → Turtle",
        description="render() переиспользует пул Turtle-сегментов вместо создания новых на каждом тике — прячет лишние через hideturtle().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Render", "")],
        kicker="Глава 19 · Архитектура",
        h1="Render: модель → Turtle",
        lede="Один и тот же пул Turtle-сегментов переиспользуется на каждом тике — новые "
        "создаются, только когда змейка выросла.",
        body_html=body,
        sidebar_groups=sidebar("19-29-render-model.html"),
        nav=PageNav(prev_href="19-28-snakeapp-arhitektura.html", prev_label="Архитектура SnakeApp", next_href="19-30-testiruem-pravila.html", next_label="Тестируем правила игры"),
    )
    write("19-29-render-model.html", out)


def build_30() -> None:
    body = f"""
    <h2>Проверяем правила напрямую, без единого окна</h2>
    <p>Раздел 19.26 показал, что правила игры — чистые функции. Значит, их можно проверить
    обычным <code class="inline">assert</code>, как в главе 3 — без Xvfb, без
    <code class="inline">turtle.Screen()</code>, без ожидания, пока что-то нарисуется:</p>
    {code_block(
        "test_snake_logic.py",
        "def test_move_snake_without_growth_drops_tail():\n"
        "    snake = [(0, 0), (-20, 0), (-40, 0)]\n"
        "    result = move_snake(snake, (20, 0), grow=False)\n"
        "    assert result == [(20, 0), (0, 0), (-20, 0)]\n\n"
        "def test_wall_collision_boundary_is_safe():\n"
        "    assert is_wall_collision((280, 280)) is False\n\n"
        "def test_wall_collision_beyond_boundary():\n"
        "    assert is_wall_collision((300, 0)) is True\n",
    )}
    {callout(
        "tip",
        "Пограничные случаи — отдельные тесты, а не один общий",
        "«Безопасно ровно на границе» и «столкновение чуть дальше границы» — два разных теста, "
        "не один: если объединить их в одну проверку, тест может остаться зелёным даже при "
        "ошибке ровно в этой точке (раздел 19.51 разбирал, почему граница включена).",
    )}
    <p>Тестировать сценарии, для которых важна случайность (выбор еды), помогает
    <code class="inline">random.Random(seed)</code> с зафиксированным зерном — раздел 19.18 уже
    объяснял, зачем <code class="inline">choose_food()</code> принимает готовый генератор, а не
    читает глобальный <code class="inline">random</code> напрямую:</p>
    {code_block(
        "test_food.py",
        "def test_choose_food_never_lands_on_snake():\n"
        "    rng = random.Random(1)\n"
        "    snake = [(0, 0), (-20, 0), (-40, 0)]\n"
        "    for _ in range(50):\n"
        "        food = choose_food(snake, rng)\n"
        "        assert food not in snake\n",
    )}

    {practice_card(
        "19-30",
        "Практика: пишем тест правила игры",
        "Автоматическая проверка — тест ловит намеренно сломанную версию функции",
        "../../practice/19-30/index.html",
    )}
    """
    out = render_page(
        page_title="Тестируем правила игры",
        description="Чистые функции правил проверяются обычным assert без Turtle — включая пограничные случаи и детерминированную случайность.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Тестируем правила", "")],
        kicker="Глава 19 · Архитектура",
        h1="Тестируем правила игры",
        lede="Раз правила — чистые функции, их можно проверить обычным assert, без окна и без "
        "Xvfb.",
        body_html=body,
        sidebar_groups=sidebar("19-30-testiruem-pravila.html"),
        nav=PageNav(prev_href="19-29-render-model.html", prev_label="Render", next_href="19-31-debug-labs.html", next_label="Debug Labs"),
    )
    write("19-30-testiruem-pravila.html", out)


def build_31() -> None:
    body = f"""
    <p>Небольшая коллекция типичных ошибок «Змейки» — каждая с симптомом и исправлением. Часть
    из них вы уже видели раньше в главе; здесь они собраны как справочник.</p>

    {debug_lab(
        1,
        "Забыли screen.tracer(0)",
        "bez_tracer.py",
        "screen = turtle.Screen()\n"
        'screen.title("Змейка")\n'
        "# tracer(0) не вызван\n",
        ["# Игра работает, но каждое движение головы и КАЖДОГО сегмента", "# перерисовывается отдельно — заметное мерцание и заметная задержка."],
        "Без <code class=\"inline\">tracer(0)</code> Turtle обновляет экран после каждого "
        "отдельного вызова <code class=\"inline\">goto()</code> — раздел 19.2 уже объяснял, "
        "зачем нужно отключить автообновление и делать это вручную, ровно раз за тик.",
        "s_tracer.py",
        "screen = turtle.Screen()\n"
        'screen.title("Змейка")\n'
        "screen.tracer(0)\n",
    )}

    {debug_lab(
        2,
        "Забыли screen.update() в конце render()",
        "bez_update.py",
        "def render(self):\n"
        "    self.head.goto(*self.state.snake[0])\n"
        "    # ...остальная отрисовка...\n"
        "    # self.screen.update() не вызван\n",
        ["# Модель меняется на каждом тике (можно проверить print()),", "# но на экране змейка стоит неподвижно."],
        "С <code class=\"inline\">tracer(0)</code> ручной <code class=\"inline\">screen.update()</code> "
        "— единственный момент, когда изменения долетают до экрана. Тот же принцип, что и в "
        "главе 17: изменение модели без вызова отрисовки невидимо пользователю.",
        "s_update.py",
        "def render(self):\n"
        "    self.head.goto(*self.state.snake[0])\n"
        "    # ...остальная отрисовка...\n"
        "    self.screen.update()\n",
    )}

    {debug_lab(
        3,
        "Busy-цикл не даёт добавить паузу",
        "busy_loop.py",
        "while igrovoj_shag():\n"
        "    screen.update()\n"
        "# пока цикл не закончится, программа не может сделать ничего другого\n",
        ["# Нажатие Space во время игры никак не влияет на неё —", "# обработчик паузы просто не успевает выполниться, пока while не закончится."],
        "Раздел 19.13 разбирал это подробно: <code class=\"inline\">while</code> занимает "
        "программу целиком. <code class=\"inline\">screen.ontimer()</code> возвращает управление "
        "между тиками — только тогда события клавиатуры успевают обработаться.",
        "ontimer_vmesto_busy.py",
        "def game_tick(self):\n"
        "    if self.state.status is not GameStatus.RUNNING:\n"
        "        return\n"
        "    # ...\n"
        "    self.screen.ontimer(self.game_tick, self.state.delay_ms)\n",
    )}

    {debug_lab(
        4,
        "time.sleep() внутри игрового цикла",
        "s_sleep.py",
        "def game_tick(self):\n"
        "    # ...\n"
        "    time.sleep(self.state.delay_ms / 1000)\n"
        "    self.game_tick()\n",
        ["# Во время сна окно полностью перестаёт реагировать:", "# ни клавиатура, ни закрытие окна не работают заданное число миллисекунд."],
        "<code class=\"inline\">time.sleep()</code> блокирует ВЕСЬ процесс, включая цикл "
        "событий Tkinter, на котором держится Turtle. <code class=\"inline\">screen.ontimer()</code> "
        "не блокирует ничего — раздел 19.13 объясняет разницу подробно.",
        "bez_sleep.py",
        "def game_tick(self):\n"
        "    # ...\n"
        "    self.screen.ontimer(self.game_tick, self.state.delay_ms)\n",
    )}

    {debug_lab(
        5,
        "Разворот на 180° разрешён",
        "bez_is_reverse.py",
        "def request_direction(self, direction):\n"
        "    self.state.next_direction = direction   # без проверки!\n",
        ["# Змейка едет вправо, игрок нажимает Left —", "# голова немедленно врезается в первый сегмент собственного тела."],
        "Без <code class=\"inline\">is_reverse()</code> ничто не мешает развернуть змейку прямо "
        "в её же тело за один тик — раздел 19.4 (и 19.11) объясняли, почему разворот на 180° "
        "должен быть запрещён на уровне ввода, а не только совпадением по случайности.",
        "s_is_reverse.py",
        "def request_direction(self, direction):\n"
        "    if is_reverse(self.state.direction, direction):\n"
        "        return\n"
        "    self.state.next_direction = direction\n",
    )}

    {debug_lab(
        6,
        "Быстрая пара клавиш проносит разворот мимо проверки",
        "proverka_ne_protiv_togo.py",
        "def request_direction(self, direction):\n"
        "    if is_reverse(self.state.next_direction, direction):   # против next_direction!\n"
        "        return\n"
        "    self.state.next_direction = direction\n",
        ["# Змейка едет вправо. Игрок быстро нажимает Up, потом Left —", "# Left проходит проверку, потому что next_direction уже стало Up, а не Right."],
        "Раздел 19.49 разбирал эту ловушку: проверка обязана идти против "
        "<code class=\"inline\">state.direction</code> — направления, которое СЕЙЧАС "
        "применяется на тике — а не против уже изменённого "
        "<code class=\"inline\">next_direction</code>, иначе вторая клавиша между тиками может "
        "протащить нелегальный разворот.",
        "proverka_protiv_direction.py",
        "def request_direction(self, direction):\n"
        "    if is_reverse(self.state.direction, direction):\n"
        "        return\n"
        "    self.state.next_direction = direction\n",
    )}

    {debug_lab(
        7,
        "Еда не выровнена по сетке",
        "neverno_vyrovnennaya_eda.py",
        "def choose_food(snake, rng, *, half=280):\n"
        "    x = rng.randint(-half, half)   # любое целое, не кратное STEP!\n"
        "    y = rng.randint(-half, half)\n"
        "    return (x, y)\n",
        ["# Яблоко появляется в точке вроде (137, -52) —", "# голова змейки никогда не попадёт туда ровно, съесть его невозможно."],
        "Раздел 19.9 объяснял: легальные позиции — узлы решётки с шагом "
        "<code class=\"inline\">STEP</code>. <code class=\"inline\">choose_food()</code> обязана "
        "выбирать из того же множества клеток, что и <code class=\"inline\">next_head()</code> — "
        "иначе математически невозможно попасть точно в клетку еды.",
        "vyrovnennaya_eda.py",
        "def choose_food(snake, rng, *, half=280, step=20):\n"
        "    free = tuple(c for c in all_cells(half=half, step=step) if c not in set(snake))\n"
        "    return rng.choice(free)\n",
    )}

    {debug_lab(
        8,
        "Еда появляется внутри тела змейки",
        "eda_bez_proverki.py",
        "def choose_food(snake, rng, *, half=280, step=20):\n"
        "    coords = range(-half, half + 1, step)\n"
        "    return (rng.choice(coords), rng.choice(coords))   # не проверяет snake!\n",
        ["# При достаточно длинной змейке яблоко иногда появляется", "# прямо внутри собственного тела — заведомо несъедобное."],
        "Раздел 19.18 разбирал именно эту проблему: без исключения занятых клеток "
        "<code class=\"inline\">choose_food()</code> честно выбирает случайно среди ВСЕХ клеток, "
        "включая занятые телом — что технически случайно, но нечестно по отношению к игроку.",
        "eda_s_proverkoj.py",
        "def choose_food(snake, rng, *, half=280, step=20):\n"
        "    occupied = set(snake)\n"
        "    free = tuple(c for c in all_cells(half=half, step=step) if c not in occupied)\n"
        "    return rng.choice(free)\n",
    )}

    {debug_lab(
        9,
        "Тело обновляется от головы к хвосту",
        "ot_golovy_k_hvostu.py",
        "def dvigat_telo():\n"
        "    for indeks in range(len(segmenty) - 1):   # неверное направление цикла!\n"
        "        segmenty[indeks].goto(segmenty[indeks + 1].xcor(), segmenty[indeks + 1].ycor())\n",
        ["# Через несколько шагов все сегменты тела", "# визуально схлопываются в одну точку."],
        "Раздел 19.17 разбирал это подробно: обновление обязано идти с хвоста к голове, иначе "
        "каждый следующий сегмент читает уже перезаписанную, а не старую позицию соседа.",
        "s_hvosta_k_golove.py",
        "def dvigat_telo():\n"
        "    for indeks in range(len(segmenty) - 1, 0, -1):\n"
        "        segmenty[indeks].goto(segmenty[indeks - 1].xcor(), segmenty[indeks - 1].ycor())\n",
    )}

    {debug_lab(
        10,
        "Табло счёта без clear()",
        "tablo_bez_clear.py",
        "def obnovit_tablo():\n"
        "    tablo.write(f\"Счёт: {{schet}}\", align=\"center\", font=(\"Arial\", 16, \"normal\"))\n"
        "    # tablo.clear() не вызван\n",
        ["# После нескольких съеденных яблок надпись на табло", "# превращается в нечитаемую кашу из наложенных друг на друга цифр."],
        "Раздел 19.5 объяснял: <code class=\"inline\">write()</code> не заменяет предыдущий "
        "текст, а рисует поверх него. <code class=\"inline\">clear()</code> обязателен перед "
        "каждой новой надписью той же черепашки.",
        "tablo_s_clear.py",
        "def obnovit_tablo():\n"
        "    tablo.clear()\n"
        "    tablo.write(f\"Счёт: {{schet}}\", align=\"center\", font=(\"Arial\", 16, \"normal\"))\n",
    )}

    {debug_lab(
        11,
        "Граница проверена нестрого — голова не доезжает до края",
        "granica_s_ravno.py",
        "def is_wall_collision(head, *, half=280):\n"
        "    x, y = head\n"
        "    return abs(x) >= half or abs(y) >= half   # >=, не >\n",
        ["# Игра заканчивается на одну клетку раньше настоящей границы —", "# змейка никогда не может доехать до последнего легального ряда клеток."],
        "Раздел 19.19 объяснял: <code class=\"inline\">GRANICA</code> — координата центра "
        "СЕГМЕНТА, который на ней всё ещё целиком помещается на поле. "
        "<code class=\"inline\">&gt;=</code> ошибочно исключает саму границу из легальной "
        "области.",
        "granica_strogo.py",
        "def is_wall_collision(head, *, half=280):\n"
        "    x, y = head\n"
        "    return abs(x) > half or abs(y) > half\n",
    )}

    {debug_lab(
        12,
        "Самостолкновение проверено по СТАРОМУ телу",
        "stolknovenie_po_staromu.py",
        "grow = head == state.food\n"
        "if is_self_collision(head, state.snake[1:]):   # ещё ДО move_snake()!\n"
        "    state.status = GameStatus.GAME_OVER\n",
        ["# Змейка не растёт, а игрок пытается заехать в клетку, которую", "# хвост как раз освобождает в этом же тике — игра ошибочно завершается."],
        "Раздел 19.20 разбирал именно это: клетка старого хвоста всё ещё в "
        "<code class=\"inline\">state.snake</code> ДО <code class=\"inline\">move_snake()</code>. "
        "Проверять нужно тело ПОСЛЕ хода — <code class=\"inline\">new_snake[1:]</code> — где "
        "хвост уже честно отброшен, если змейка не растёт.",
        "stolknovenie_po_novomu.py",
        "new_snake = move_snake(state.snake, head, grow=grow)\n"
        "if is_self_collision(head, new_snake[1:]):\n"
        "    state.status = GameStatus.GAME_OVER\n",
    )}

    {debug_lab(
        13,
        "Restart оставляет старую цепочку тиков живой",
        "restart_bez_generation.py",
        "def restart(self):\n"
        "    self.state = new_game_state(self.rng)\n"
        "    self.render()\n"
        "    # generation не увеличен — старый _on_timer() всё ещё запланирован!\n",
        ["# Через мгновение после Restart на экране внезапно появляется", "# фигура/движение от уже несуществующей прошлой игры."],
        "Раздел 19.23 разбирал этот случай — классический баг «двух параллельных таймерных "
        "цепочек», знакомый ещё по главе 16. Без счётчика поколений старый "
        "<code class=\"inline\">_on_timer()</code> ничем не отличим от нового — оба тикают "
        "одновременно.",
        "restart_s_generation.py",
        "def restart(self):\n"
        "    self._generation += 1\n"
        "    self.state = new_game_state(self.rng, high_score=self.state.high_score)\n"
        "    self.render()\n",
    )}

    {debug_lab(
        14,
        "Пауза меняет экран, но игра продолжает двигаться",
        "pauza_tolko_vizualno.py",
        "def toggle_pause(self):\n"
        '    self._show_overlay("ПАУЗА", "Space — продолжить")\n'
        "    # state.status не изменён — game_tick() ничего не знает о паузе!\n",
        ["# Оверлей «ПАУЗА» показан, но змейка под ним", "# продолжает двигаться и может врезаться в стену."],
        "Раздел 19.22 объяснял: оверлей — это только то, что ВИДНО. Реальная остановка "
        "происходит из-за проверки <code class=\"inline\">status is not RUNNING</code> в самом "
        "начале <code class=\"inline\">game_tick()</code> — без смены "
        "<code class=\"inline\">state.status</code> эта проверка никогда не сработает.",
        "pauza_po_statusu.py",
        "def toggle_pause(self):\n"
        "    if self.state.status is GameStatus.RUNNING:\n"
        "        self.state.status = GameStatus.PAUSED\n"
        '        self._show_overlay("ПАУЗА", "Space — продолжить")\n',
    )}

    {debug_lab(
        15,
        "Новая игра не сбрасывает направление",
        "restart_bez_napravleniya.py",
        "def restart(self):\n"
        "    self._generation += 1\n"
        "    self.state.snake = [(0, 0)]   # правит поле точечно, а не создаёт state заново\n"
        "    self.state.score = 0\n"
        "    # direction/next_direction остались от прошлой игры!\n",
        ["# Новая змейка стоит в центре, но при первом же движении", "# уезжает в направлении, в котором закончилась ПРОШЛАЯ игра."],
        "Точечные правки существующего <code class=\"inline\">state</code> легко забывают одно "
        "из полей. <code class=\"inline\">new_game_state()</code> (раздел 19.25) создаёт "
        "структуру целиком заново — забыть отдельное поле в новом объекте невозможно, оно либо "
        "есть в конструкторе, либо код не запустится.",
        "restart_novym_state.py",
        "def restart(self):\n"
        "    self._generation += 1\n"
        "    self.state = new_game_state(self.rng, high_score=self.state.high_score)\n",
    )}

    {debug_lab(
        16,
        "Рекорд обнуляется вместе со счётом",
        "restart_teryaet_rekord.py",
        "def restart(self):\n"
        "    self._generation += 1\n"
        "    self.state = new_game_state(self.rng)   # high_score не передан — снова 0!\n",
        ["# Игрок набрал 90 очков, проиграл, нажал R —", "# табло снова показывает «Рекорд: 0», как будто игра только что установлена."],
        "Раздел 19.25 объяснял: <code class=\"inline\">high_score</code> обязан быть явно "
        "передан из старого <code class=\"inline\">state</code> в новый. "
        "<code class=\"inline\">new_game_state()</code> без аргумента "
        "<code class=\"inline\">high_score</code> использует значение по умолчанию — ноль.",
        "restart_s_rekordom.py",
        "def restart(self):\n"
        "    self._generation += 1\n"
        "    self.state = new_game_state(self.rng, high_score=self.state.high_score)\n",
    )}

    {debug_lab(
        17,
        "GameState хранит объект Turtle",
        "gamestate_s_turtle.py",
        "@dataclass\n"
        "class GameState:\n"
        "    snake: list[Position]\n"
        "    head_turtle: turtle.Turtle   # объект Turtle внутри модели!\n",
        ["# Тесты из раздела 19.30 падают с ошибкой создания Turtle,", "# хотя проверяют только математику координат — окно им не нужно."],
        "Раздел 19.27 предупреждал об этом явно: <code class=\"inline\">GameState</code> — "
        "домен данных, а не контейнер для виджетов. Как только внутри появляется "
        "<code class=\"inline\">turtle.Turtle</code>, создать состояние без реального окна "
        "становится невозможно — вся польза чистой логики (раздел 19.26) исчезает.",
        "gamestate_bez_turtle.py",
        "@dataclass\n"
        "class GameState:\n"
        "    snake: list[Position]\n"
        "    # объекты Turtle живут в SnakeApp, не в GameState\n",
    )}

    {debug_lab(
        18,
        "Тик планирует сам себя, даже когда игра уже не RUNNING",
        "tik_planiruet_vsegda.py",
        "def _on_timer(self, generation):\n"
        "    if generation != self._generation:\n"
        "        return\n"
        "    self.game_tick()\n"
        "    self._schedule_next_tick()   # без проверки статуса!\n",
        ["# После Game Over или паузы змейка выглядит остановленной,", "# но цепочка ontimer() продолжает тикать вхолостую в фоне."],
        "<code class=\"inline\">game_tick()</code> сама по себе безопасна — она просто ничего не "
        "делает при <code class=\"inline\">status != RUNNING</code>. Но если следующий тик "
        "планируется БЕЗУСЛОВНО, цепочка никогда не остановится сама, продолжая впустую "
        "расходовать таймер даже после конца игры.",
        "tik_planiruet_esli_running.py",
        "def _on_timer(self, generation):\n"
        "    if generation != self._generation:\n"
        "        return\n"
        "    self.game_tick()\n"
        "    if self.state.status is GameStatus.RUNNING:\n"
        "        self._schedule_next_tick()\n",
    )}

    {practice_card(
        "19-31",
        "Практика: находим баг «Змейки» по симптому",
        "Автоматическая проверка — для набора описанных симптомов выбираем правильную причину/исправление",
        "../../practice/19-31/index.html",
    )}
    """
    out = render_page(
        page_title="Debug Labs — типичные ошибки «Змейки»",
        description="Восемнадцать разобранных багов игры «Змейка»: тик, таймеры, направление, столкновения, restart, состояние.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Debug Labs", "")],
        kicker="Глава 19 · Тестирование",
        h1="Debug Labs — типичные ошибки «Змейки»",
        lede="Каждая ошибка здесь встречается в реальных студенческих проектах — научитесь "
        "узнавать симптом раньше, чем откроете отладчик.",
        body_html=body,
        sidebar_groups=sidebar("19-31-debug-labs.html"),
        nav=PageNav(prev_href="19-30-testiruem-pravila.html", prev_label="Тестируем правила", next_href="19-32-snake-pro-itogi.html", next_label="Snake Pro — итоги"),
    )
    write("19-31-debug-labs.html", out)


def build_32() -> None:
    checklist_model = "".join(f"<li>{x}</li>" for x in [
        "GameState — snake, direction, food, score, status, delay_ms, без Turtle внутри",
        "чистые функции правил — next_head, move_snake, is_wall_collision, is_self_collision, choose_food, calculate_delay",
        "новая голова + старое тело вместо цикла по сегментам",
    ])
    checklist_loop = "".join(f"<li>{x}</li>" for x in [
        "тик через screen.ontimer(), без busy-цикла и time.sleep()",
        "клавиатура запрашивает направление, тик его применяет",
        "поколение (generation) защищает от параллельных цепочек тиков",
    ])
    checklist_features = "".join(f"<li>{x}</li>" for x in [
        "pause/resume без пересоздания змейки",
        "restart с сохранением рекорда",
        "скорость растёт вместе со счётом, не опускаясь ниже минимума",
    ])
    checklist_testing = "".join(f"<li>{x}</li>" for x in [
        "правила протестированы без единого настоящего окна",
        "детерминированная еда через random.Random(seed)",
        "render() переиспользует пул Turtle-сегментов",
    ])
    body = f"""
    <h2>Итоговая программа</h2>
    {image_figure(f"{IMG}/snake-final-pro.png", "Финальное окно Snake Pro: несколько сегментов тела, яблоко, счёт и рекорд на тёмном поле", "Реальное окно финальной версии — та же самая идея, что открывала главу в разделе 19.1, но теперь мы знаем, из чего она построена.", width=560)}
    <p>Файл целиком, самодостаточный и без невидимых зависимостей от других уроков:</p>
    <p>[[icon:file]] <a href="../../../projects/turtle/snake/snake.py">projects/turtle/snake/snake.py</a></p>
    {code_block(
        "snake.py — структура",
        "class Direction(Enum): ...\n"
        "class GameStatus(Enum): ...\n\n"
        "@dataclass\n"
        "class GameState: ...\n\n"
        "def next_head(head, direction): ...\n"
        "def move_snake(snake, new_head, *, grow): ...\n"
        "def is_wall_collision(head): ...\n"
        "def is_self_collision(new_head, body_after_move): ...\n"
        "def choose_food(snake, rng): ...\n"
        "def calculate_delay(score): ...\n"
        "def new_game_state(rng, *, high_score=0): ...\n\n"
        "class SnakeApp:\n"
        "    def __init__(self, *, rng=None): ...\n"
        "    def bind_keys(self): ...\n"
        "    def request_direction(self, direction): ...\n"
        "    def game_tick(self): ...\n"
        "    def toggle_pause(self): ...\n"
        "    def restart(self): ...\n"
        "    def render(self): ...\n"
        "    def run(self): ...\n\n"
        "def main():\n"
        "    app = SnakeApp()\n"
        "    app.run()\n\n"
        'if __name__ == "__main__":\n'
        "    main()\n",
    )}
    {callout(
        "tip",
        "Запустите игру у себя",
        "<code class=\"inline\">python snake.py</code> в терминале. Стрелки или WASD — движение, "
        "<code class=\"inline\">Space</code> — пауза, <code class=\"inline\">R</code> — новая "
        "игра. Сравните с <code class=\"inline\">snake_basic.py</code> (раздел 19.8) — та же "
        "идея игры, но совершенно другая внутренняя архитектура.",
    )}

    <h2>Чек-лист готового приложения</h2>
    <div class="capability-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin:24px 0">
      <div style="background:var(--color-bg-canvas,#fff);border:1.5px solid var(--color-border-default,#E4E1F5);border-radius:16px;padding:16px 18px">
        <div style="font-family:Sora,sans-serif;font-weight:700;color:#5B24F9;margin-bottom:8px">МОДЕЛЬ</div>
        <ul style="margin:0;padding-left:18px;font-size:14px;line-height:1.6">{checklist_model}</ul>
      </div>
      <div style="background:var(--color-bg-canvas,#fff);border:1.5px solid var(--color-border-default,#E4E1F5);border-radius:16px;padding:16px 18px">
        <div style="font-family:Sora,sans-serif;font-weight:700;color:#5B24F9;margin-bottom:8px">ЦИКЛ</div>
        <ul style="margin:0;padding-left:18px;font-size:14px;line-height:1.6">{checklist_loop}</ul>
      </div>
      <div style="background:var(--color-bg-canvas,#fff);border:1.5px solid var(--color-border-default,#E4E1F5);border-radius:16px;padding:16px 18px">
        <div style="font-family:Sora,sans-serif;font-weight:700;color:#5B24F9;margin-bottom:8px">ФУНКЦИИ ИГРЫ</div>
        <ul style="margin:0;padding-left:18px;font-size:14px;line-height:1.6">{checklist_features}</ul>
      </div>
      <div style="background:var(--color-bg-canvas,#fff);border:1.5px solid var(--color-border-default,#E4E1F5);border-radius:16px;padding:16px 18px">
        <div style="font-family:Sora,sans-serif;font-weight:700;color:#5B24F9;margin-bottom:8px">ТЕСТИРОВАНИЕ</div>
        <ul style="margin:0;padding-left:18px;font-size:14px;line-height:1.6">{checklist_testing}</ul>
      </div>
    </div>

    <h2>Небольшая визуальная палитра</h2>
    <p>Финальная игра использует всего пять цветов — не для того, чтобы выглядеть скромно, а
    потому что различать голову, тело и еду проще по контрасту, а не по количеству оттенков:</p>
    {color_swatch_row([
        ("#000000", "Фон", "#000000"),
        ("#FFFFFF", "Голова", "#FFFFFF"),
        ("#4ECDC4", "Тело", "#4ECDC4"),
        ("#FF5D5D", "Еда", "#FF5D5D"),
        ("#FFFFFF", "Текст", "#FFFFFF"),
    ])}

    {local_required_card(
        "19-32",
        "Практика: Snake Pro целиком",
        "Модуль turtle открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/19-32/index.html",
    )}
    """
    out = render_page(
        page_title="Snake Pro — финальная игра",
        description="Финальная архитектура игры целиком: GameState, чистая логика, SnakeApp, screen.ontimer(), pause/restart/score.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Snake Pro", "")],
        kicker="Глава 19 · Финал",
        h1="Snake Pro — финальная игра",
        lede="Тот же самый прототип из раздела 19.1 — но теперь с моделью состояния, игровым "
        "тиком и архитектурой, которая выдержит рост проекта.",
        body_html=body,
        sidebar_groups=sidebar("19-32-snake-pro-itogi.html"),
        nav=PageNav(prev_href="19-31-debug-labs.html", prev_label="Debug Labs", next_href="19-33-itogi-glavy.html", next_label="Итоги главы"),
    )
    write("19-32-snake-pro-itogi.html", out)


def build_33() -> None:
    body = f"""
    <h2 id="itogi-glavy">Итоги главы 19</h2>
    {summary_box("Что мы построили и чему научились", [
        "Игровой мир — дискретная решётка с шагом STEP; легальные позиции всегда кратны шагу, "
        "а не произвольны.",
        "Направление — не строка для сравнения в if/elif, а вектор смещения "
        "(DIRECTION_VECTORS), и запрет разворота на 180° проверяется против ТЕКУЩЕГО "
        "направления, а не уже запрошенного следующего.",
        "Игровой тик — вся цепочка правил целиком (направление → движение → еда → "
        "столкновения → рендер), а отрисовка — концептуально отдельный шаг.",
        "screen.ontimer() планирует следующий тик и сразу возвращает управление — вместо "
        "того чтобы блокировать программу в busy-цикле или time.sleep().",
        "Модель змейки — список логических позиций; новая голова плюс старое тело строит "
        "движение за один проход, без цикла с риском перепутать порядок.",
        "Столкновение с собой проверяется против тела ПОСЛЕ хода — иначе легальный заезд в "
        "клетку освободившегося хвоста ошибочно считается проигрышем.",
        "Явные состояния READY/RUNNING/PAUSED/GAME_OVER — пауза и рестарт не просто меняют "
        "картинку, а переключают состояние, от которого зависит, тикает ли игра вообще.",
        "Поколение (generation) защищает restart() от параллельных цепочек ontimer() — тот же "
        "класс проблемы, что и повторное нажатие кнопки в главе 16.",
        "GameState не хранит ни одного объекта Turtle — правила игры протестированы обычным "
        "assert, без единого настоящего окна.",
    ])}

    <h2 id="most-k-glave-20">Мост к главе 20</h2>
    {callout(
        "info",
        "Дальше: полноценный игровой движок вместо Turtle",
        "«Змейка» построена на том же Tkinter-цикле событий, что и рисовалка из главы 18 — "
        "удобно для учебных целей, но Turtle никогда не проектировался как игровой движок. В "
        "следующей главе — Pygame — появятся настоящие спрайты, обработка коллизий на уровне "
        "библиотеки и цикл кадров, спроектированный именно для игр реального времени.",
    )}
    """
    out = render_page(
        page_title="Итоги главы",
        description="Итоги главы 19: сетка, направление как вектор, игровой тик, состояние игры, чистая логика и мост к главе 20.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 19", "index.html"), ("Итоги главы", "")],
        kicker="Глава 19 · Финал",
        h1="Итоги главы",
        lede="От busy-цикла с глобальными переменными до модели состояния с игровым тиком, "
        "паузой, рестартом и проверяемыми правилами.",
        body_html=body,
        sidebar_groups=sidebar("19-33-itogi-glavy.html"),
        nav=PageNav(prev_href="19-32-snake-pro-itogi.html", prev_label="Snake Pro", next_href="../glava-20/index.html", next_label="Глава 20: Станьте разработчиком игр с Pygame"),
    )
    write("19-33-itogi-glavy.html", out)


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
    build_33()
