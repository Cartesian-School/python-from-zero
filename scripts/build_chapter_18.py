#!/usr/bin/env python3
"""Строит Главу 18: «Проект: приложение для рисования с Tkinter» (site/chapters/glava-18/)."""

import html
import itertools
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
    converge_diagram,
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
OUT_DIR = ROOT / "site" / "chapters" / "glava-18"
IMG = "../../assets/img/chapter-18/output"

PAGES = [
    ("index.html", "Обзор главы"),
    ("18-01-obyasnenie-nachalo.html", "Что мы строим? Начало работы"),
    ("18-02-ekran-holst.html", "Экран и холст (Canvas)"),
    ("18-03-menu-parametry.html", "Панель инструментов и параметры"),
    ("18-04-mysh-linii.html", "Позиция мыши и рисуем линии"),
    ("18-05-figury.html", "Квадраты, прямоугольники, круги и овалы"),
    ("18-06-razmer-cveta.html", "Выбираем размер и цвет"),
    ("18-07-polnaya-programma-itogi.html", "Первая полная программа"),
    ("18-08-mentalnaya-model.html", "Canvas хранит объекты, а не пиксели"),
    ("18-09-sistema-koordinat.html", "Система координат Canvas"),
    ("18-10-item-id.html", "Item ID: что возвращает create_*"),
    ("18-11-tegi.html", "Теги: группируем и выбираем элементы"),
    ("18-12-zhest-myshi.html", "Жизненный цикл жеста мыши"),
    ("18-13-sostoyanie-risovaniya.html", "Состояние рисования"),
    ("18-14-karandash.html", "Карандаш: непрерывный штрих"),
    ("18-15-instrument-liniya.html", "Инструмент «Линия»"),
    ("18-16-geometriya-pryamougolnika.html", "Геометрия прямоугольника"),
    ("18-17-geometriya-ovala.html", "Геометрия овала"),
    ("18-18-zhivoe-prevyu.html", "Живое превью: coords()"),
    ("18-19-redaktirovanie-elementov.html", "itemconfig, move, delete"),
    ("18-20-poryadok-sloev.html", "Порядок наложения"),
    ("18-21-sistema-cveta.html", "Система цвета"),
    ("18-22-tolschina-kisti.html", "Толщина кисти"),
    ("18-23-lastik.html", "Ластик"),
    ("18-24-otmena-deystviy.html", "Отмена действий (Undo)"),
    ("18-25-povtor-deystviy.html", "Повтор действий (Redo)"),
    ("18-26-ochistka-holsta.html", "Очистка холста"),
    ("18-27-goryachie-klavishi.html", "Горячие клавиши"),
    ("18-28-stroka-sostoyaniya.html", "Строка состояния"),
    ("18-29-arhitektura-paintapp.html", "Архитектура PaintApp"),
    ("18-30-sohranenie-json.html", "Сохранение и загрузка JSON"),
    ("18-31-debug-labs.html", "Debug Labs"),
    ("18-32-paint-pro-itogi.html", "Paint Pro — итоги главы"),
]

LESSON_IDS = [
    "18-02", "18-03", "18-04", "18-05", "18-06", "18-07",
    "18-09", "18-10", "18-11", "18-12", "18-13", "18-14", "18-15", "18-16",
    "18-17", "18-18", "18-19", "18-20", "18-21", "18-22", "18-23", "18-24",
    "18-25", "18-26", "18-27", "18-28", "18-29", "18-30", "18-31", "18-32",
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 18 · Рисовалка", items),
        SidebarGroup("Практика", [
            NavItem(f"[[icon:practice]] {lid}: Практика", f"../../practice/{lid}/index.html") for lid in LESSON_IDS
        ]),
        SidebarGroup("Исходный код", [
            NavItem("[[icon:code]] paint_app_basic.py — первый прототип (18.7)", "../../../projects/tkinter/paint-app/paint_app_basic.py"),
            NavItem("[[icon:code]] paint_app.py — финальная версия Pro (18.32)", "../../../projects/tkinter/paint-app/paint_app.py"),
        ]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    clean = "\n".join(line.rstrip() for line in html_out.split("\n"))
    path.write_text(clean, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# Локальные помощники главы 18
# ---------------------------------------------------------------------------

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
    """Единый компонент Debug Lab (введён в главе 14, переиспользован в 15/16/17):
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


_coord_diagram_counter = itertools.count()


def coordinate_diagram(*, points: list[tuple[float, float, str, str]] | None = None, rect: tuple[float, float, float, float] | None = None, caption: str = "", width: int = 360, height: int = 260) -> str:
    """Схема системы координат Canvas: начало координат в левом верхнем углу,
    X вправо, Y вниз. points — список (x, y, label, color); rect — необязательный
    прямоугольник (x1, y1, x2, y2), показанный по двум противоположным углам."""
    pad = 40
    ox, oy = pad, pad
    # Страницы вроде 18-16 вызывают coordinate_diagram() несколько раз — id
    # маркеров должны быть уникальны на всю страницу, иначе получится
    # несколько элементов с одним и тем же id (невалидный HTML).
    mid = f"cd{next(_coord_diagram_counter)}"
    parts = [
        f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="{html.escape(caption)}" style="display:block;width:100%;height:auto">'
    ]
    # оси
    parts.append(f'<line x1="{ox}" y1="{oy}" x2="{width - 20}" y2="{oy}" stroke="#5B24F9" stroke-width="2.5" marker-end="url(#{mid}-arrow-x)"/>')
    parts.append(f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{height - 20}" stroke="#5B24F9" stroke-width="2.5" marker-end="url(#{mid}-arrow-y)"/>')
    parts.append(
        "<defs>"
        f'<marker id="{mid}-arrow-x" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#5B24F9"/></marker>'
        f'<marker id="{mid}-arrow-y" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#5B24F9"/></marker>'
        "</defs>"
    )
    parts.append(f'<text x="{width - 16}" y="{oy - 8}" text-anchor="end" font-family="\'JetBrains Mono\',monospace" font-size="13" fill="#5B24F9" font-weight="700">X →</text>')
    parts.append(f'<text x="{ox + 8}" y="{height - 8}" font-family="\'JetBrains Mono\',monospace" font-size="13" fill="#5B24F9" font-weight="700">Y ↓</text>')
    parts.append(f'<circle cx="{ox}" cy="{oy}" r="3.5" fill="#0D0230"/>')
    parts.append(f'<text x="{ox - 6}" y="{oy - 8}" text-anchor="end" font-family="\'JetBrains Mono\',monospace" font-size="12" fill="#0D0230">(0, 0)</text>')

    def to_px(x, y):
        return ox + x, oy + y

    if rect:
        x1, y1, x2, y2 = rect
        rx1, ry1 = to_px(min(x1, x2), min(y1, y2))
        rx2, ry2 = to_px(max(x1, x2), max(y1, y2))
        parts.append(f'<rect x="{rx1}" y="{ry1}" width="{rx2 - rx1}" height="{ry2 - ry1}" fill="rgba(91,36,249,.08)" stroke="#5B24F9" stroke-width="1.5" stroke-dasharray="5,4"/>')

    for x, y, label, color in points or []:
        px, py = to_px(x, y)
        parts.append(f'<circle cx="{px}" cy="{py}" r="5" fill="{color}"/>')
        parts.append(f'<text x="{px + 9}" y="{py - 8}" font-family="\'JetBrains Mono\',monospace" font-size="12" fill="{color}" font-weight="700">{html.escape(label)}</text>')

    parts.append("</svg>")
    svg = "".join(parts)
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:20px 0;padding:16px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px)"><div style="width:min(100%, {width}px);margin:0 auto">{svg}</div>{cap}</figure>'
    )


def color_dialog_schematic(current_hex: str, caption: str = "") -> str:
    """Явно подписанная схема нативного диалога colorchooser — сам диалог не
    рендерится предсказуемо под headless Xvfb без реального клика пользователя,
    поэтому здесь показана его СХЕМА, а не настоящий скриншот (см. правило
    честных подписей, глава 17). Результат выбора цвета показан отдельным
    настоящим скриншотом приложения."""
    swatches = "".join(
        f'<div style="width:22px;height:22px;border-radius:4px;background:{c};border:1px solid rgba(0,0,0,.15)"></div>'
        for c in ["#111827", "#dc2626", "#2563eb", "#16a34a", "#f59e0b", "#7c3aed", "#ec4899", "#0891b2",
                  "#78716c", "#ef4444", "#3b82f6", "#22c55e"]
    )
    return f"""
    <figure style="margin:24px 0;padding:20px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px)">
      <div style="font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;
        color:#B45309;margin-bottom:8px;text-align:center">[[icon:note]] Схема диалога (не настоящий скриншот)</div>
      <div style="max-width:280px;margin:0 auto;border-radius:8px;border:1px solid #9a97a8;overflow:hidden;
        box-shadow:0 6px 16px rgba(0,0,0,.15);font-family:sans-serif">
        <div style="background:#e2e2e2;padding:6px 10px;font-size:12px;color:#333;border-bottom:1px solid #b8b8b8">Выберите цвет</div>
        <div style="background:#ececec;padding:14px">
          <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin-bottom:10px">{swatches}</div>
          <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:#333">
            <span>Текущий:</span>
            <span style="width:20px;height:20px;border-radius:4px;background:{current_hex};border:1px solid rgba(0,0,0,.2)"></span>
            <span style="font-family:'JetBrains Mono',monospace">{current_hex}</span>
          </div>
        </div>
        <div style="background:#ececec;padding:8px 12px;display:flex;gap:8px;justify-content:flex-end;border-top:1px solid #d5d5d5">
          <div style="padding:5px 16px;border:1px solid #9a97a8;border-radius:4px;font-size:12.5px;background:#ececec;color:#222">Отмена</div>
          <div style="padding:5px 16px;border:1px solid #9a97a8;border-radius:4px;font-size:12.5px;background:#ececec;color:#222">OK</div>
        </div>
      </div>
      {f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{html.escape(caption)}</figcaption>' if caption else ''}
    </figure>"""


def turtle_vs_canvas_diagram() -> str:
    """Side-by-side origin/axis comparison — Canvas (top-left origin, Y down)
    vs Turtle (center origin, Y up), reusing the same simple axes-SVG shape
    so the difference is a direct visual contrast, not two unrelated pictures."""

    def axes_svg(origin_x: float, origin_y: float, *, y_down: bool) -> str:
        y2 = origin_y + 60 if y_down else origin_y - 60
        # Уникальный id маркера на каждый вызов — как и в coordinate_diagram(),
        # чтобы несколько экземпляров на одной странице не дублировали id.
        mid = f"tvc{next(_coord_diagram_counter)}-{'yd' if y_down else 'yu'}"
        return (
            f'<svg viewBox="0 0 170 170" xmlns="http://www.w3.org/2000/svg" style="display:block;width:100%;height:auto">'
            f'<defs><marker id="tc-{mid}-x" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#5B24F9"/></marker>'
            f'<marker id="tc-{mid}-y" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#DB2777"/></marker></defs>'
            f'<line x1="{origin_x}" y1="{origin_y}" x2="{origin_x + 70}" y2="{origin_y}" stroke="#5B24F9" '
            f'stroke-width="2.5" marker-end="url(#tc-{mid}-x)"/>'
            f'<line x1="{origin_x}" y1="{origin_y}" x2="{origin_x}" y2="{y2}" stroke="#DB2777" '
            f'stroke-width="2.5" marker-end="url(#tc-{mid}-y)"/>'
            f'<circle cx="{origin_x}" cy="{origin_y}" r="4" fill="#0D0230"/>'
            f'<text x="{origin_x + 76}" y="{origin_y + 5}" font-family="\'JetBrains Mono\',monospace" '
            f'font-size="12" fill="#5B24F9" font-weight="700">X</text>'
            f'<text x="{origin_x - 6}" y="{y2 + (14 if y_down else -8)}" text-anchor="end" '
            f'font-family="\'JetBrains Mono\',monospace" font-size="12" fill="#DB2777" font-weight="700">Y</text>'
            f'</svg>'
        )

    canvas_svg = axes_svg(20, 20, y_down=True)
    turtle_svg = axes_svg(85, 85, y_down=False)
    return f"""
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px;margin:20px 0">
      <figure style="margin:0;padding:16px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);text-align:center">
        <div style="font-weight:700;margin-bottom:8px">Canvas (Tkinter)</div>
        {canvas_svg}
        <figcaption style="font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">Начало координат — левый верхний угол, Y растёт ВНИЗ</figcaption>
      </figure>
      <figure style="margin:0;padding:16px;background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);text-align:center">
        <div style="font-weight:700;margin-bottom:8px">Turtle (главы 6–7)</div>
        {turtle_svg}
        <figcaption style="font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:8px">Начало координат — центр экрана, Y растёт ВВЕРХ</figcaption>
      </figure>
    </div>"""


def mouse_gesture_diagram(*, caption: str = "") -> str:
    """Вертикальная последовательность press → drag* → release для раздела
    18.12 — сознательно НЕ диаграмма принятия решений: жест мыши линеен,
    а <B1-Motion> может произойти ноль, один или много раз подряд. Вместо
    диаграммы с веткой ДА/НЕТ и кривой стрелкой назад это показано рамкой
    вокруг повторяющегося шага с явной подписью — без пересекающихся
    стрелок и без отдельного SVG viewBox, который на узком экране сжимал
    бы текст вместе с диаграммой (HTML/CSS верстка вместо этого просто
    переносит строки на мобильном экране)."""

    def node(top: str, bottom: str, *, accent: str) -> str:
        return f"""
        <div style="box-sizing:border-box;width:min(320px,100%);border:1.5px solid {accent};
          border-radius:14px;background:var(--color-bg-canvas,#fff);padding:10px 18px;
          text-align:center">
          <div style="font-family:'JetBrains Mono',monospace;font-weight:700;font-size:13px;
            color:{accent}">{html.escape(top)}</div>
          <div style="font-size:14px;margin-top:2px">{html.escape(bottom)}</div>
        </div>"""

    def arrow() -> str:
        return '<div style="font-size:20px;line-height:1;color:#9a97a8;margin:2px 0" aria-hidden="true">↓</div>'

    press = node("<Button-1>", "Нажали левую кнопку мыши", accent="#5B24F9")
    remember = node("start_x, start_y", "Запоминаем точку начала", accent="#5B24F9")
    drag_event = node("<B1-Motion>", "Мышь движется с зажатой кнопкой", accent="#5B24F9")
    drag_update = node("coords() / create_line()", "Обновляем превью или штрих", accent="#5B24F9")
    release = node("<ButtonRelease-1>", "Кнопку отпустили", accent="#DB2777")
    finalize = node("render_document()", "Фиксируем фигуру или действие", accent="#059669")

    repeat_group = f"""
    <div style="box-sizing:border-box;width:min(340px,100%);border:2px dashed #DB2777;
      border-radius:18px;padding:16px 16px 12px;display:flex;flex-direction:column;
      align-items:center;gap:6px;position:relative;margin:6px 0">
      <div style="position:absolute;top:-13px;left:50%;transform:translateX(-50%);
        background:#DB2777;color:#fff;font-family:Sora,sans-serif;font-weight:700;font-size:11px;
        letter-spacing:.04em;text-transform:uppercase;border-radius:999px;padding:3px 12px;
        white-space:nowrap">↻ 0, 1 или много раз</div>
      {drag_event}
      {arrow()}
      {drag_update}
    </div>"""

    cap = (
        f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);'
        f'margin-top:12px;max-width:420px">{html.escape(caption)}</figcaption>'
        if caption else ""
    )
    return f"""
    <figure style="margin:24px 0;padding:24px 20px;background:var(--color-bg-surface,#FAFAFC);
      border-radius:var(--radius-lg,20px);display:flex;flex-direction:column;align-items:center">
      {press}
      {arrow()}
      {remember}
      {arrow()}
      {repeat_group}
      {arrow()}
      {release}
      {arrow()}
      {finalize}
      {cap}
    </figure>"""


# ---------------------------------------------------------------------------
# Опener
# ---------------------------------------------------------------------------

def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=18,
        description="Полноценный редактор рисования на Canvas: карандаш, фигуры, цвет, отмена действий, "
        "сохранение и загрузка — от первого прототипа до архитектуры уровня приложения.",
        meta_items=["[[icon:timer]] ~7 часов", "[[icon:palette]] Canvas + интерактивное рисование", "[[icon:practice]] ~30 практик", "[[icon:palette]] полноценный Paint-проект"],
        sections=[
            ChapterSectionLink("18.1", "Что мы строим? Начало работы", "18-01-obyasnenie-nachalo.html"),
            ChapterSectionLink("18.2", "Экран и холст (Canvas)", "18-02-ekran-holst.html"),
            ChapterSectionLink("18.3", "Панель инструментов и параметры", "18-03-menu-parametry.html"),
            ChapterSectionLink("18.4", "Позиция мыши и рисуем линии", "18-04-mysh-linii.html"),
            ChapterSectionLink("18.5", "Квадраты, прямоугольники, круги и овалы", "18-05-figury.html"),
            ChapterSectionLink("18.6", "Выбираем размер и цвет", "18-06-razmer-cveta.html"),
            ChapterSectionLink("18.7", "Первая полная программа", "18-07-polnaya-programma-itogi.html"),
            ChapterSectionLink("18.8", "Canvas хранит объекты, а не пиксели", "18-08-mentalnaya-model.html"),
            ChapterSectionLink("18.9", "Система координат Canvas", "18-09-sistema-koordinat.html"),
            ChapterSectionLink("18.10", "Item ID: что возвращает create_*", "18-10-item-id.html"),
            ChapterSectionLink("18.11", "Теги: группируем и выбираем элементы", "18-11-tegi.html"),
            ChapterSectionLink("18.12", "Жизненный цикл жеста мыши", "18-12-zhest-myshi.html"),
            ChapterSectionLink("18.13", "Состояние рисования", "18-13-sostoyanie-risovaniya.html"),
            ChapterSectionLink("18.14", "Карандаш: непрерывный штрих", "18-14-karandash.html"),
            ChapterSectionLink("18.15", "Инструмент «Линия»", "18-15-instrument-liniya.html"),
            ChapterSectionLink("18.16", "Геометрия прямоугольника", "18-16-geometriya-pryamougolnika.html"),
            ChapterSectionLink("18.17", "Геометрия овала", "18-17-geometriya-ovala.html"),
            ChapterSectionLink("18.18", "Живое превью: coords()", "18-18-zhivoe-prevyu.html"),
            ChapterSectionLink("18.19", "itemconfig, move, delete", "18-19-redaktirovanie-elementov.html"),
            ChapterSectionLink("18.20", "Порядок наложения", "18-20-poryadok-sloev.html"),
            ChapterSectionLink("18.21", "Система цвета", "18-21-sistema-cveta.html"),
            ChapterSectionLink("18.22", "Толщина кисти", "18-22-tolschina-kisti.html"),
            ChapterSectionLink("18.23", "Ластик", "18-23-lastik.html"),
            ChapterSectionLink("18.24", "Отмена действий (Undo)", "18-24-otmena-deystviy.html"),
            ChapterSectionLink("18.25", "Повтор действий (Redo)", "18-25-povtor-deystviy.html"),
            ChapterSectionLink("18.26", "Очистка холста", "18-26-ochistka-holsta.html"),
            ChapterSectionLink("18.27", "Горячие клавиши", "18-27-goryachie-klavishi.html"),
            ChapterSectionLink("18.28", "Строка состояния", "18-28-stroka-sostoyaniya.html"),
            ChapterSectionLink("18.29", "Архитектура PaintApp", "18-29-arhitektura-paintapp.html"),
            ChapterSectionLink("18.30", "Сохранение и загрузка JSON", "18-30-sohranenie-json.html"),
            ChapterSectionLink("18.31", "Debug Labs", "18-31-debug-labs.html"),
            ChapterSectionLink("18.32", "Paint Pro — итоги главы", "18-32-paint-pro-itogi.html"),
        ],
    )
    write("index.html", out)


# ---------------------------------------------------------------------------
# 18.1 – 18.7: первый прототип (существующие страницы/практики сохранены)
# ---------------------------------------------------------------------------

def build_01() -> None:
    body = f"""
    {image_figure(f"{IMG}/paint-pro-final.png", "Готовое приложение: холст с несколькими фигурами, панель инструментов с выбранным инструментом, палитра цветов, ползунок толщины и строка состояния", "К концу главы мы соберём это приложение шаг за шагом.", width=760)}

    <h2>Приложение для рисования — объяснение</h2>
    <p>Соберём собственный маленький «Paint»: холст, на котором можно рисовать линии,
    прямоугольники, овалы и произвольные каракули мышью, с выбором цвета и толщины. Начнём с
    того же плана, что и в главе 17 — сначала работающий прототип, потом более внимательный
    взгляд на то, как он устроен изнутри:</p>
    <ol>
      <li>Холст для рисования (виджет <code class="inline">Canvas</code>);</li>
      <li>Панель инструментов — кнопки выбора фигуры;</li>
      <li>Реакция на движение и клики мыши;</li>
      <li>Собственно рисование линий, прямоугольников, овалов;</li>
      <li>Выбор толщины и цвета;</li>
      <li>Кнопка очистки холста и свободное рисование.</li>
    </ol>
    <p>Это даст честно работающую программу уже через несколько разделов — раздел 18.7. А
    дальше глава возвращается назад и разбирает Canvas куда внимательнее: что на самом деле
    хранит холст, как устроены координаты, что значит «отменить действие» и как из кучи
    глобальных переменных вырастает архитектура целого приложения.</p>

    <h2 id="nachalo">Начинаем работу</h2>
    {code_block(
        "nachalo.py",
        "import tkinter as tk\n\n"
        "root = tk.Tk()\n"
        'root.title("Рисовалка")\n',
    )}

    {local_required_card(
        "18-02",
        "Практика: начинаем собирать рисовалку",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-02/index.html",
    )}
    """
    out = render_page(
        page_title="Приложение для рисования — объяснение",
        description="План сборки приложения-рисовалки на Tkinter и превью готового результата главы 18.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Объяснение", "")],
        kicker="Глава 18 · Проект: приложение для рисования",
        h1="Приложение для рисования — объяснение",
        lede="Так будет выглядеть готовый проект. Разберём путь к нему по шагам — от пустого "
        "холста до архитектуры уровня приложения.",
        body_html=body,
        sidebar_groups=sidebar("18-01-obyasnenie-nachalo.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="18-02-ekran-holst.html", next_label="Экран и холст"),
    )
    write("18-01-obyasnenie-nachalo.html", out)


def build_02() -> None:
    coord_diag = coordinate_diagram(
        points=[(60, 40, "(60, 40)", "#5B24F9")],
        caption="Точка (60, 40): 60 пикселей ВПРАВО и 40 пикселей ВНИЗ от левого верхнего угла холста.",
    )
    body = f"""
    <h2>Настраиваем экран</h2>
    {code_block("nastrojka_ekrana.py", 'root.title("Рисовалка")\n')}

    <h2>Создаём холст</h2>
    <p>Виджет <code class="inline">Canvas</code> — прямоугольная область, на которой можно
    рисовать линии, фигуры и текст по координатам, как в Turtle (главы 6–7), только внутри окна
    Tkinter:</p>
    {code_block(
        "sozdaem_holst.py",
        'canvas = tk.Canvas(root, width=600, height=400, bg="white")\n'
        "canvas.pack()\n",
    )}
    {image_figure(f"{IMG}/empty-canvas.png", "Реальное окно: пустой белый холст 600×400 внутри окна Tkinter", "Реальное окно: пустой холст сразу после запуска — рисовать пока нечем, но область уже есть.", width=420)}

    {callout(
        "info",
        "Координаты Canvas — как у экрана, не как у Turtle",
        "У <code class=\"inline\">Canvas</code> точка (0, 0) — левый верхний угол, а не центр, "
        "как у экрана Turtle, и ось Y растёт <strong>вниз</strong>, а не вверх. Раздел 18.9 "
        "разберёт это подробнее и сравнит обе системы координат в лоб.",
    )}
    {coord_diag}

    {local_required_card(
        "18-02",
        "Практика: создаём Canvas",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-02/index.html",
    )}
    """
    out = render_page(
        page_title="Настраиваем экран. Создаём холст",
        description="Виджет Canvas в Tkinter — координаты, размер и цвет фона холста для рисования.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Экран и холст", "")],
        kicker="Глава 18 · Проект: приложение для рисования",
        h1="Настраиваем экран. Создаём холст",
        lede="Виджет Canvas — прямоугольная область для рисования внутри окна Tkinter.",
        body_html=body,
        sidebar_groups=sidebar("18-02-ekran-holst.html"),
        nav=PageNav(prev_href="18-01-obyasnenie-nachalo.html", prev_label="Объяснение", next_href="18-03-menu-parametry.html", next_label="Панель инструментов"),
    )
    write("18-02-ekran-holst.html", out)


def build_03() -> None:
    body = f"""
    <h2>Создаём первое меню (фигуры)</h2>
    <p>Панель инструментов — обычный <code class="inline">Frame</code> (глава 16) с кнопками,
    каждая из которых выбирает свою фигуру:</p>
    {code_block(
        "menu_figur.py",
        "toolbar = tk.Frame(root)\n"
        'toolbar.pack(side="top", fill="x")\n\n'
        "def vybrat_figuru(figura):\n"
        "    global tekuschaya_figura\n"
        "    tekuschaya_figura = figura\n\n"
        'tk.Button(toolbar, text="Линия", command=lambda: vybrat_figuru("linia")).pack(side="left")\n'
        'tk.Button(toolbar, text="Прямоугольник", command=lambda: vybrat_figuru("pryamougolnik")).pack(side="left")\n'
        'tk.Button(toolbar, text="Овал", command=lambda: vybrat_figuru("oval")).pack(side="left")\n',
    )}
    {image_figure(f"{IMG}/toolbar-tools.png", "Реальное окно: панель инструментов с кнопками Линия, Прямоугольник, Овал над пустым холстом", "Реальное окно: панель инструментов уже видна, хотя рисовать фигуры мы пока не умеем.", width=420)}

    <h2 id="parametry">Заставляем параметры рисования работать!</h2>
    <p>Заведём глобальные переменные для текущей фигуры, цвета и толщины линии — их будут
    менять кнопки панели инструментов и читать функции рисования:</p>
    {code_block(
        "parametry.py",
        'tekuschaya_figura = "linia"\n'
        'tekuschij_cvet = "black"\n'
        "tolschina = 3\n",
    )}
    {callout(
        "warning",
        "Прототип: глобальные переменные — не финал архитектуры",
        "Три глобальные переменные легко читать и объяснить, пока приложение маленькое — тот же "
        "выбор мы уже видели в первом прототипе крестиков-ноликов (глава 17). Раздел 18.13 "
        "покажет, во что это вырастает, когда инструментов, действий и истории становится "
        "больше.",
    )}

    {local_required_card(
        "18-03",
        "Практика: панель инструментов и параметры рисования",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-03/index.html",
    )}
    """
    out = render_page(
        page_title="Создаём первое меню (фигуры). Параметры рисования",
        description="Панель инструментов с кнопками выбора фигуры и глобальные переменные текущих параметров рисования.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Меню и параметры", "")],
        kicker="Глава 18 · Проект: приложение для рисования",
        h1="Создаём первое меню (фигуры)",
        lede="Панель инструментов с кнопками выбора фигуры — и переменные, хранящие текущее "
        "состояние.",
        body_html=body,
        sidebar_groups=sidebar("18-03-menu-parametry.html"),
        nav=PageNav(prev_href="18-02-ekran-holst.html", prev_label="Экран и холст", next_href="18-04-mysh-linii.html", next_label="Позиция мыши и линии"),
    )
    write("18-03-menu-parametry.html", out)


def build_04() -> None:
    gesture = flowchart([
        {"kind": "start", "label": "<Button-1>: нажали кнопку мыши"},
        {"kind": "process", "label": "запомнить start_x, start_y"},
        {"kind": "process", "label": "<B1-Motion>: двигаем с зажатой кнопкой"},
        {"kind": "process", "label": "рисуем/обновляем линию до текущей точки"},
        {"kind": "end", "label": "<ButtonRelease-1>: отпустили — фигура готова"},
    ], caption="Три события вместе создают жест «нарисовать одним движением» — раздел 18.12 разберёт его подробнее.")
    body = f"""
    <h2>Получаем позицию мыши</h2>
    <p>Как и в главе 17, реагировать на мышь помогает <code class="inline">.bind()</code> —
    только вместо клавиатурных событий здесь события мыши: <code class="inline">&lt;Button-1&gt;</code>
    (нажатие левой кнопки), <code class="inline">&lt;B1-Motion&gt;</code> (движение с зажатой
    левой кнопкой), <code class="inline">&lt;ButtonRelease-1&gt;</code> (кнопку отпустили).</p>
    {code_block(
        "poziciya_myshi.py",
        "def pokazat_poziciyu(event):\n"
        '    pozicia_label.config(text=f"x={event.x}, y={event.y}")\n\n'
        'canvas.bind("<Motion>", pokazat_poziciyu)\n',
    )}
    <p><code class="inline">event.x</code> и <code class="inline">event.y</code> — координаты
    курсора относительно холста, в тех же единицах, что и у самого <code class="inline">Canvas</code>.</p>

    <h2 id="linii">Рисуем линии</h2>
    <p>Три события вместе создают эффект «рисования от точки до точки»: запоминаем начало на
    <code class="inline">&lt;Button-1&gt;</code>, рисуем линию к текущей позиции на каждом
    <code class="inline">&lt;B1-Motion&gt;</code>:</p>
    {code_block(
        "risuem_linii.py",
        "start_x, start_y = None, None\n\n"
        "def nachalo_risovaniya(event):\n"
        "    global start_x, start_y\n"
        "    start_x, start_y = event.x, event.y\n\n"
        "def vo_vremya_risovaniya(event):\n"
        "    canvas.create_line(start_x, start_y, event.x, event.y, fill=tekuschij_cvet, width=tolschina)\n\n"
        'canvas.bind("<Button-1>", nachalo_risovaniya)\n'
        'canvas.bind("<B1-Motion>", vo_vremya_risovaniya)\n',
    )}
    {gesture}
    {image_figure(f"{IMG}/mouse-press-start.png", "Реальное окно: курсор нажат в точке начала линии, отметка на холсте ещё не появилась", "Реальное окно: момент нажатия — start_x/start_y запомнены.", width=420)}
    {image_figure(f"{IMG}/line-final.png", "Реальное окно: готовая прямая линия между точкой нажатия и точкой отпускания", "Реальное окно: кнопку отпустили — линия нарисована.", width=420)}
    {callout(
        "tip",
        "create_line — как forward() у Turtle, только по координатам",
        "<code class=\"inline\">canvas.create_line(x1, y1, x2, y2)</code> рисует прямую между "
        "двумя точками — концептуально то же самое, что <code class=\"inline\">goto()</code> "
        "у Turtle из главы 6, только без «черепашки», которая сама туда едет.",
    )}

    {local_required_card(
        "18-04",
        "Практика: позиция мыши и рисование линий",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-04/index.html",
    )}
    """
    out = render_page(
        page_title="Получаем позицию мыши. Рисуем линии",
        description="События мыши в Tkinter (Button-1, B1-Motion) и рисование линий на Canvas.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Мышь и линии", "")],
        kicker="Глава 18 · Проект: приложение для рисования",
        h1="Получаем позицию мыши",
        lede="События мыши позволяют превратить движение курсора в настоящую линию на холсте.",
        body_html=body,
        sidebar_groups=sidebar("18-04-mysh-linii.html"),
        nav=PageNav(prev_href="18-03-menu-parametry.html", prev_label="Меню и параметры", next_href="18-05-figury.html", next_label="Фигуры: прямоугольники, овалы"),
    )
    write("18-04-mysh-linii.html", out)


def build_05() -> None:
    body = f"""
    <p>Прямоугольники и овалы рисуются похожим образом — Canvas умеет строить их сразу по двум
    противоположным углам, без ручного вычисления сторон:</p>
    {code_block(
        "pryamougolniki_ovaly.py",
        "def vo_vremya_risovaniya(event):\n"
        '    if tekuschaya_figura == "pryamougolnik":\n'
        "        canvas.create_rectangle(\n"
        "            start_x, start_y, event.x, event.y,\n"
        "            outline=tekuschij_cvet, width=tolschina,\n"
        "        )\n"
        '    elif tekuschaya_figura == "oval":\n'
        "        canvas.create_oval(\n"
        "            start_x, start_y, event.x, event.y,\n"
        "            outline=tekuschij_cvet, width=tolschina,\n"
        "        )\n",
    )}
    {image_figure(f"{IMG}/rectangle-final.png", "Реальное окно: прямоугольник, нарисованный между точкой нажатия и точкой отпускания", "Реальное окно: create_rectangle() по двум противоположным углам.", width=380)}
    {image_figure(f"{IMG}/oval-final.png", "Реальное окно: овал, вписанный в область между точкой нажатия и точкой отпускания", "Реальное окно: create_oval() по тем же двум углам — подробнее об этом в разделе 18.17.", width=380)}
    {callout(
        "warning",
        "Промежуточные фигуры множатся",
        "Если рисовать так, как показано выше, при каждом движении мыши будет создаваться "
        "<strong>новая</strong> фигура поверх предыдущей — а не одна, растущая вместе с "
        "движением. В полной программе (раздел 18.7) эта проблема решена: предыдущая "
        "«черновая» фигура удаляется перед тем, как нарисовать новую. Раздел 18.18 показывает "
        "более аккуратный способ — обновлять один и тот же элемент через "
        "<code class=\"inline\">coords()</code>, вместо того чтобы пересоздавать его заново.",
    )}

    {local_required_card(
        "18-05",
        "Практика: прямоугольники и овалы",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-05/index.html",
    )}
    """
    out = render_page(
        page_title="Квадраты и прямоугольники! Круги и овалы!",
        description="Рисование прямоугольников (create_rectangle) и овалов (create_oval) на Canvas.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Фигуры", "")],
        kicker="Глава 18 · Проект: приложение для рисования",
        h1="Квадраты и прямоугольники! Круги и овалы!",
        lede="Canvas умеет рисовать готовые фигуры по двум углам — не только линии.",
        body_html=body,
        sidebar_groups=sidebar("18-05-figury.html"),
        nav=PageNav(prev_href="18-04-mysh-linii.html", prev_label="Мышь и линии", next_href="18-06-razmer-cveta.html", next_label="Размер и цвет"),
    )
    write("18-05-figury.html", out)


def build_06() -> None:
    body = f"""
    <h2>Выбираем размер!</h2>
    <p>Виджет <code class="inline">Scale</code> — ползунок для выбора числа в диапазоне,
    отлично подходит для толщины линии:</p>
    {code_block(
        "vybor_razmera.py",
        "def vybrat_tolschinu(znachenie):\n"
        "    global tolschina\n"
        "    tolschina = int(znachenie)\n\n"
        'tolschina_scale = tk.Scale(toolbar, from_=1, to=10, orient="horizontal", command=vybrat_tolschinu)\n'
        "tolschina_scale.set(3)\n"
        "tolschina_scale.pack(side=\"left\")\n",
    )}
    {callout(
        "info",
        "command у Scale получает значение, а не событие",
        "В отличие от <code class=\"inline\">.bind()</code>, обработчик <code class=\"inline\">"
        "Scale</code> получает готовое строковое значение ползунка напрямую — поэтому "
        "<code class=\"inline\">vybrat_tolschinu(znachenie)</code> сразу превращает его в "
        "число через <code class=\"inline\">int()</code> (глава 4).",
    )}
    {image_figure(f"{IMG}/width-comparison.png", "Реальный холст: четыре линии одного цвета толщиной 1, 3, 8 и 16 пикселей, подписанные числами", "Реальный холст: одна и та же линия при разной толщине — числа в коде превращаются в конкретную разницу на экране.", width=460)}

    <h2>Очень много цветов!</h2>
    <p>Палитру цветов легко построить циклом (глава 10) по списку названий (глава 11) — вместо
    того, чтобы создавать каждую кнопку вручную:</p>
    {code_block(
        "vybor_cveta.py",
        'cveta = ["black", "red", "blue", "green", "orange", "purple"]\n'
        "for cvet in cveta:\n"
        '    tk.Button(toolbar, bg=cvet, width=2, command=lambda c=cvet: vybrat_cvet(c)).pack(side="left")\n',
    )}
    {image_figure(f"{IMG}/color-palette.png", "Реальное окно: панель инструментов с рядом цветных квадратных кнопок палитры", "Реальное окно: шесть кнопок-квадратов, каждая цвета кнопки bg=cvet — палитра видна раньше, чем результат рисования ею.", width=420)}
    {callout(
        "tip",
        "lambda c=cvet — та же тонкость, что и в главе 17",
        "Без <code class=\"inline\">c=cvet</code> все кнопки палитры выбирали бы <strong>"
        "последний</strong> цвет из списка — та же самая ловушка с лямбдами внутри цикла, что "
        "мы уже разбирали в проекте «Крестики-нолики».",
    )}

    {local_required_card(
        "18-06",
        "Практика: Scale и палитра цветов",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-06/index.html",
    )}
    """
    out = render_page(
        page_title="Выбираем размер! Очень много цветов!",
        description="Виджет Scale для выбора толщины линии и палитра цветов, построенная циклом.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Размер и цвет", "")],
        kicker="Глава 18 · Проект: приложение для рисования",
        h1="Выбираем размер! Очень много цветов!",
        lede="Ползунок толщины и палитра цветов, построенная циклом по списку.",
        body_html=body,
        sidebar_groups=sidebar("18-06-razmer-cveta.html"),
        nav=PageNav(prev_href="18-05-figury.html", prev_label="Фигуры", next_href="18-07-polnaya-programma-itogi.html", next_label="Первая полная программа"),
    )
    write("18-06-razmer-cveta.html", out)


def build_07() -> None:
    body = f"""
    <h2>Я закончил рисовать!</h2>
    <p>Осталось добавить кнопку очистки холста и режим «свободного рисования» (карандаш) — для
    него точки рисуются на каждое движение мыши без привязки к начальной точке:</p>
    {code_block(
        "ochistka_i_svobodno.py",
        "def ochistit_holst():\n"
        '    canvas.delete("all")\n\n'
        "def vo_vremya_risovaniya(event):\n"
        '    if tekuschaya_figura == "svobodno":\n'
        "        canvas.create_oval(\n"
        "            event.x - tolschina, event.y - tolschina,\n"
        "            event.x + tolschina, event.y + tolschina,\n"
        "            fill=tekuschij_cvet, outline=tekuschij_cvet,\n"
        "        )\n"
        "        return\n"
        "    # ... остальные фигуры, как в разделе 18.5\n",
    )}
    {image_figure(f"{IMG}/freehand-naive-dots.png", "Реальный холст: штрих из отдельных кружков с заметными промежутками между ними", "Реальный холст: кружок на каждое движение мыши — при резком жесте между ними видны разрывы.", width=420)}
    {callout(
        "warning",
        "Отдельные кружки — не одна линия",
        "Такой штрих рисует не непрерывную линию, а россыпь маленьких кружков-точек, которые "
        "иногда даже не соприкасаются друг с другом, если мышь двигалась быстро между двумя "
        "событиями <code class=\"inline\">&lt;B1-Motion&gt;</code>. Раздел 18.14 показывает, как "
        "получить настоящий непрерывный штрих — соединяя каждую новую точку с предыдущей.",
    )}

    <h2 id="polnaya-programma">Первая полная программа</h2>
    <p>Полная версия первого прототипа, включая исправленную отрисовку «черновых» фигур во время
    перетаскивания мыши, доступна отдельным файлом:</p>
    <p>[[icon:file]] <a href="../../../projects/tkinter/paint-app/paint_app_basic.py">projects/tkinter/paint-app/paint_app_basic.py</a></p>
    {image_figure(f"{IMG}/multiple-shapes.png", "Реальное окно: холст с несколькими линиями, прямоугольником и овалом разных цветов — первый прототип рисовалки", "Реальное окно первого прототипа: несколько фигур разных цветов на одном холсте.", width=460)}
    {callout(
        "info",
        "Честная, но не окончательная версия",
        "Мы построили настоящую работающую программу — с холстом, фигурами, цветом и толщиной. "
        "Но состояние здесь по-прежнему живёт в глобальных переменных, «отменить» ничего "
        "нельзя, а «черновая» фигура во время перетаскивания просто удаляется и создаётся "
        "заново. Начиная со следующего раздела глава смотрит на Canvas куда внимательнее: что "
        "он на самом деле хранит, как отменить действие по-настоящему и как вырастить из этого "
        "прототипа приложение уровня <code class=\"inline\">PaintApp</code> (раздел 18.32).",
    )}

    {exercise(2, "Кнопка «Отменить»", "Сохраняйте id каждой нарисованной фигуры (canvas.create_* возвращает id) в список — и добавьте кнопку, удаляющую последнюю через canvas.delete(id). Раздел 18.24 разберёт эту идею как настоящую архитектуру.")}
    {exercise(3, "Сохранение рисунка", "Изучите модуль tkinter.filedialog и попробуйте добавить кнопку «Сохранить» — как минимум сохраняющую список нарисованных фигур в текстовый файл (глава 15). Раздел 18.30 покажет полное решение через JSON.")}
{local_required_card(
        "18-07",
        "Практика: первая полная программа",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-07/index.html",
    )}

    <h2 id="itogi">Итоги раздела</h2>
    {summary_box("Что мы узнали", [
        "<code class=\"inline\">Canvas</code> — виджет Tkinter для рисования линий и фигур по "
        "координатам; координаты растут вправо и вниз от левого верхнего угла.",
        "<code class=\"inline\">canvas.create_line/rectangle/oval(...)</code> рисуют готовые "
        "фигуры по координатам.",
        "События мыши (<code class=\"inline\">&lt;Button-1&gt;</code>, "
        "<code class=\"inline\">&lt;B1-Motion&gt;</code>, "
        "<code class=\"inline\">&lt;ButtonRelease-1&gt;</code>) отслеживают клик, "
        "перетаскивание и отпускание кнопки мыши.",
        "<code class=\"inline\">Scale</code> — ползунок для выбора числа в диапазоне.",
        "Палитра из нескольких похожих кнопок эффективнее строится циклом, чем вручную одна за "
        "другой.",
        "Это только первый прототип — дальше глава разбирает Canvas и архитектуру приложения "
        "куда внимательнее.",
    ])}
    """
    out = render_page(
        page_title="Первая полная программа",
        description="Очистка холста, режим свободного рисования, ссылка на первый прототип и итоги первой части главы 18.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Первая полная программа", "")],
        kicker="Глава 18 · Проект: приложение для рисования",
        h1="Я закончил рисовать! Первая полная программа",
        lede="Последние штрихи первого прототипа — очистка холста и свободное рисование — и "
        "работающая программа целиком.",
        body_html=body,
        sidebar_groups=sidebar("18-07-polnaya-programma-itogi.html"),
        nav=PageNav(prev_href="18-06-razmer-cveta.html", prev_label="Размер и цвет", next_href="18-08-mentalnaya-model.html", next_label="Canvas хранит объекты, а не пиксели"),
    )
    write("18-07-polnaya-programma-itogi.html", out)


# ---------------------------------------------------------------------------
# 18.8 – 18.20: Canvas по-настоящему — модель, координаты, жесты, редактирование
# ---------------------------------------------------------------------------

def build_08() -> None:
    body = f"""
    <h2>Canvas не «красит пиксели» — он хранит объекты</h2>
    <p>Первый прототип уже рисует, но легко представить его неправильно: будто
    <code class="inline">create_line()</code> просто закрашивает пиксели на картинке, как кисть
    в графическом редакторе. На самом деле Canvas устроен иначе — и от этого зависит почти всё
    остальное в этой главе: отмена действий, редактирование фигур, порядок наложения.</p>
    {pipeline_diagram([
        {"kind": "plain", "title": "canvas.create_rectangle(...)"},
        {"kind": "object", "title": "Canvas", "rows": ["сохраняет фигуру как элемент"]},
        {"kind": "plain", "title": "item_id = 3"},
        {"kind": "object", "title": "экран"},
    ], caption="create_* не просто рисует — он добавляет ЭЛЕМЕНТ в список, который Canvas хранит сам.")}
    <p>Возвращённое число — <strong>item ID</strong>, идентификатор именно этого элемента внутри
    Canvas (раздел 18.10). Пока фигура не удалена явно, Canvas помнит о ней и может её
    перерисовать, переместить или изменить — даже если ваш код давно закончил с ней работать.</p>

    {object_diagram(
        "canvas", "Canvas",
        [("item #1", "line (0, 0, 100, 60)"), ("item #2", "rectangle (10, 80, 120, 140)"),
         ("item #3", "oval (30, 20, 90, 70)")],
        caption="Canvas хранит СПИСОК элементов — примерно так, если бы у него были свои внутренние «объекты».",
    )}
    {image_figure(f"{IMG}/multiple-shapes.png", "Реальное окно: холст с тремя нарисованными фигурами — линией, прямоугольником и овалом", "То же самое реальное окно из раздела 18.7: три видимых фигуры — три хранимых элемента.", width=420)}

    <h2>Три разных слоя — не путайте их</h2>
    {comparison_table(
        ["Слой", "Что это"],
        [
            ["Модель приложения (Python)", "Ваши переменные и структуры данных — то, что вы сами придумали"],
            ["Элемент Canvas (item)", "Запись внутри Canvas с типом, координатами и параметрами — создаётся через create_*"],
            ["Пиксели на экране", "Итоговая картинка, которую видит пользователь — результат отрисовки элемента"],
        ],
    )}
    {callout(
        "warning",
        "item ID — это НЕ идентификатор Python-объекта",
        "<code class=\"inline\">item_id = canvas.create_rectangle(...)</code> возвращает обычное "
        "целое число — внутренний номер записи внутри Canvas, а не <code class=\"inline\">"
        "id()</code> какого-то Python-объекта и не индекс в списке, который ведёте вы сами. Canvas "
        "выдаёт номера по своим правилам (обычно по возрастанию) — полагаться на конкретные "
        "значения не стоит, только на то, что каждый <code class=\"inline\">item_id</code> "
        "уникален для одного элемента.",
    )}
    """
    out = render_page(
        page_title="Canvas хранит объекты, а не пиксели",
        description="Ментальная модель Canvas: create_* добавляет элемент в список, который хранит сам виджет, а не закрашивает пиксели напрямую.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Ментальная модель Canvas", "")],
        kicker="Глава 18 · Canvas по-настоящему",
        h1="Canvas хранит объекты, а не пиксели",
        lede="create_line() не просто рисует — он добавляет элемент в список, который Canvas "
        "помнит сам.",
        body_html=body,
        sidebar_groups=sidebar("18-08-mentalnaya-model.html"),
        nav=PageNav(prev_href="18-07-polnaya-programma-itogi.html", prev_label="Первая полная программа", next_href="18-09-sistema-koordinat.html", next_label="Система координат Canvas"),
    )
    write("18-08-mentalnaya-model.html", out)


def build_09() -> None:
    body = f"""
    <h2>Координаты растут вправо и вниз</h2>
    <p>У Canvas точка <code class="inline">(0, 0)</code> — левый верхний угол. Первая координата
    (X) растёт вправо, вторая (Y) — вниз. Любая фигура задаётся через точки в этой системе:</p>
    {coordinate_diagram(
        points=[(40, 30, "P1 (40, 30)", "#5B24F9"), (160, 120, "P2 (160, 120)", "#DB2777")],
        rect=(40, 30, 160, 120),
        caption="Прямоугольник по двум противоположным углам P1 и P2 — ровно то, что делает create_rectangle(P1x, P1y, P2x, P2y).",
        width=380, height=280,
    )}
    {image_figure(f"{IMG}/canvas-coordinate-demo.png", "Реальное окно: холст с подписанными точками и линией между ними, показывающими рост координат вправо и вниз", "Реальное окно: две точки и линия между ними — движение мыши вправо увеличивает x, движение вниз увеличивает y.", width=420)}

    <h2>Turtle vs Canvas — сравним в лоб</h2>
    <p>Если до этой главы вы рисовали Turtle (главы 6–7), интуиция может подвести: там начало
    координат — центр экрана, а Y растёт вверх, как в математике на бумаге. У Canvas — иначе, и
    это не «более правильная» или «менее правильная» система, а просто другое соглашение,
    которое Tkinter унаследовал от оконных систем, где строки экрана нумеруются сверху вниз.</p>
    {turtle_vs_canvas_diagram()}
    {callout(
        "info",
        "event.x / event.y — те же координаты, что и у самого Canvas",
        "Координаты события мыши (глава 17 — <code class=\"inline\">event.x</code>, "
        "<code class=\"inline\">event.y</code>) и координаты, которые принимает "
        "<code class=\"inline\">create_*</code>, — одна и та же система: пиксели относительно "
        "левого верхнего угла холста. Именно поэтому <code class=\"inline\">canvas.create_line(start_x, "
        "start_y, event.x, event.y)</code> работает без какого-либо пересчёта.",
    )}

    {practice_card(
        "18-09",
        "Практика: координаты Canvas",
        "Автоматическая проверка — определяем координаты точек и границы фигур по описанию жеста",
        "../../practice/18-09/index.html",
    )}
    """
    out = render_page(
        page_title="Система координат Canvas",
        description="Начало координат, направление осей X/Y у Canvas и сравнение с системой координат Turtle.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Координаты Canvas", "")],
        kicker="Глава 18 · Canvas по-настоящему",
        h1="Система координат Canvas",
        lede="Левый верхний угол — начало координат. X растёт вправо, Y — вниз. Не как у Turtle.",
        body_html=body,
        sidebar_groups=sidebar("18-09-sistema-koordinat.html"),
        nav=PageNav(prev_href="18-08-mentalnaya-model.html", prev_label="Ментальная модель Canvas", next_href="18-10-item-id.html", next_label="Item ID"),
    )
    write("18-09-sistema-koordinat.html", out)


def build_10() -> None:
    body = f"""
    <h2>create_* возвращает идентификатор</h2>
    <p>Каждый вызов <code class="inline">canvas.create_line/rectangle/oval(...)</code> возвращает
    целое число — <strong>item ID</strong> только что созданного элемента. Если его не сохранить,
    фигура всё равно нарисуется, но обратиться к ней позже будет нечем:</p>
    {code_block(
        "item_id.py",
        "item_id = canvas.create_rectangle(10, 10, 100, 60, outline=\"blue\")\n"
        "print(item_id)   # например, 1 — конкретное число зависит от того, сколько элементов уже создано\n",
    )}
    <p>Этот номер пригождается для трёх вещей, которые мы разберём дальше в главе:</p>
    {capability_map([
        ("coords(item_id, ...)", ["изменить координаты существующего элемента", "раздел 18.18–18.19"]),
        ("itemconfig(item_id, ...)", ["изменить цвет/толщину без пересоздания", "раздел 18.19"]),
        ("delete(item_id)", ["убрать именно этот элемент, не все остальные", "разделы 18.19, 18.24"]),
    ], title="Зачем помнить item_id")}
    {callout(
        "warning",
        "item_id — не индекс списка и не id() объекта Python",
        "Соблазн считать, что <code class=\"inline\">item_id</code> — это позиция в списке "
        "(«первая фигура — id 0», «вторая — id 1») ошибочен: Canvas выдаёт номера по своим "
        "правилам и не обязан начинать с нуля или идти без пропусков после удаления элементов. "
        "Не полагайтесь на конкретные значения — только на то, что каждый "
        "<code class=\"inline\">item_id</code> уникально ссылается на один элемент.",
    )}

    {practice_card(
        "18-10",
        "Практика: item ID",
        "Автоматическая проверка — какие операции требуют item_id, а какие можно делать иначе",
        "../../practice/18-10/index.html",
    )}
    """
    out = render_page(
        page_title="Item ID: что возвращает create_*",
        description="create_* возвращает целочисленный идентификатор элемента Canvas, нужный для coords/itemconfig/delete.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Item ID", "")],
        kicker="Глава 18 · Canvas по-настоящему",
        h1="Item ID: что возвращает create_*",
        lede="Число, которое create_* возвращает — не пустая формальность: это способ вернуться к "
        "фигуре позже.",
        body_html=body,
        sidebar_groups=sidebar("18-10-item-id.html"),
        nav=PageNav(prev_href="18-09-sistema-koordinat.html", prev_label="Координаты Canvas", next_href="18-11-tegi.html", next_label="Теги"),
    )
    write("18-10-item-id.html", out)


def build_11() -> None:
    body = f"""
    <h2>Тег — это имя, а не число</h2>
    <p><code class="inline">item_id</code> указывает на ОДИН конкретный элемент. Но часто нужно
    обратиться сразу к нескольким — например, ко всем нарисованным фигурам сразу, не трогая
    временную «черновую» фигуру превью. Для этого у Canvas есть теги:</p>
    {code_block(
        "tegi.py",
        'canvas.create_line(\n'
        "    0, 0, 100, 60,\n"
        '    fill="black", tags=("shape", "stroke"),\n'
        ")\n",
    )}
    <p>Один элемент может носить сразу несколько тегов. Дальше к тегу можно обращаться вместо
    <code class="inline">item_id</code> почти везде, где Canvas ожидает адрес элемента:</p>
    {code_block(
        "operacii_s_tegami.py",
        'canvas.delete("preview")           # убрать все элементы с тегом "preview"\n'
        'canvas.itemconfig("shape", width=2) # изменить толщину у ВСЕХ элементов с тегом "shape"\n',
    )}
    {capability_map([
        ("item_id", ["указывает на ОДИН конкретный элемент", "число, которое возвращает create_*"]),
        ("тег", ["может стоять сразу на многих элементах", "строка, которую придумываете вы"]),
    ], title="item_id против тега")}
    <div style="display:flex;gap:32px;flex-wrap:wrap;margin:20px 0">
      <div style="background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);padding:16px 20px">
        <div style="font-weight:700;color:#5B24F9;margin-bottom:8px">тег "shape"</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:13px;line-height:1.9">
          ├─ item 12<br>├─ item 13<br>└─ item 14
        </div>
      </div>
      <div style="background:var(--color-bg-surface,#FAFAFC);border-radius:var(--radius-lg,20px);padding:16px 20px">
        <div style="font-weight:700;color:#DB2777;margin-bottom:8px">тег "preview"</div>
        <div style="font-family:'JetBrains Mono',monospace;font-size:13px;line-height:1.9">
          └─ item 15
        </div>
      </div>
    </div>
    {callout(
        "tip",
        "В финальном приложении теги пригодятся дважды",
        "Раздел 18.20 использует теги, чтобы показать порядок наложения фигур друг на друга. А "
        "черновой элемент превью (раздел 18.18) получает собственный тег "
        "<code class=\"inline\">\"preview\"</code>, чтобы его можно было убрать одной командой, "
        "не перебирая все остальные фигуры.",
    )}

    {practice_card(
        "18-11",
        "Практика: теги Canvas",
        "Автоматическая проверка — какой тег/id подойдёт для конкретной операции над элементами",
        "../../practice/18-11/index.html",
    )}
    """
    out = render_page(
        page_title="Теги: группируем и выбираем элементы",
        description="Теги Canvas — именованные группы элементов, к которым можно обращаться вместо отдельных item_id.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Теги", "")],
        kicker="Глава 18 · Canvas по-настоящему",
        h1="Теги: группируем и выбираем элементы",
        lede="item_id указывает на один элемент. Тег может стоять сразу на многих — и работать "
        "с группой одной командой.",
        body_html=body,
        sidebar_groups=sidebar("18-11-tegi.html"),
        nav=PageNav(prev_href="18-10-item-id.html", prev_label="Item ID", next_href="18-12-zhest-myshi.html", next_label="Жизненный цикл жеста мыши"),
    )
    write("18-11-tegi.html", out)


def build_12() -> None:
    lifecycle = mouse_gesture_diagram(
        caption="press → drag (0, 1 или много раз) → release — один и тот же жест для карандаша, "
        "линии, прямоугольника и овала.",
    )
    body = f"""
    <h2>Один жест, три события</h2>
    <p>Рисование одной фигуры мышью — это не одно событие, а последовательность из трёх разных
    типов, которые вместе образуют жест «нарисовать»:</p>
    {lifecycle}
    {comparison_table(
        ["Событие", "Когда срабатывает"],
        [
            ["<code class=\"inline\">&lt;Button-1&gt;</code>", "ровно один раз — в момент нажатия левой кнопки"],
            ["<code class=\"inline\">&lt;B1-Motion&gt;</code>", "много раз подряд, пока кнопка зажата и мышь движется"],
            ["<code class=\"inline\">&lt;ButtonRelease-1&gt;</code>", "ровно один раз — в момент отпускания кнопки"],
        ],
    )}
    {callout(
        "warning",
        "&lt;Motion&gt; — это НЕ &lt;B1-Motion&gt;",
        "<code class=\"inline\">&lt;Motion&gt;</code> срабатывает при ЛЮБОМ движении мыши над "
        "холстом — даже если ни одна кнопка не нажата. <code class=\"inline\">&lt;B1-Motion&gt;</code> "
        "— только при движении с зажатой ЛЕВОЙ кнопкой. Перепутать их — частая причина, по "
        "которой рисование начинается без клика (раздел 18.31, Debug Lab).",
    )}
    <p>Все нужные координаты приходят через тот же объект <code class="inline">Event</code>, что
    и в главе 17 — <code class="inline">event.x</code>, <code class="inline">event.y</code>.
    <code class="inline">event.widget</code> тоже доступен, хотя для одного холста он обычно и
    так очевиден.</p>

    <h2>Клик без перетаскивания — не забыть про этот случай</h2>
    <p>Что если пользователь нажал и сразу отпустил кнопку в одной точке, не подвинув мышь?
    <code class="inline">&lt;B1-Motion&gt;</code> в этом случае не произойдёт ни разу — событие
    сработает, только если мышь действительно сдвинулась. Финальное приложение (раздел 18.32)
    явно проверяет это: если точка начала и точка отпускания почти совпадают, прямоугольник или
    овал попросту не создаётся — вместо невидимой фигуры нулевого размера.</p>

    {local_required_card(
        "18-12",
        "Практика: жест мыши press → drag → release",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-12/index.html",
    )}
    """
    out = render_page(
        page_title="Жизненный цикл жеста мыши",
        description="press → drag → release: три события Tkinter, из которых складывается любое рисование мышью.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Жест мыши", "")],
        kicker="Глава 18 · Canvas по-настоящему",
        h1="Жизненный цикл жеста мыши",
        lede="Рисование одной фигуры — это последовательность из трёх разных событий, а не одно.",
        body_html=body,
        sidebar_groups=sidebar("18-12-zhest-myshi.html"),
        nav=PageNav(prev_href="18-11-tegi.html", prev_label="Теги", next_href="18-13-sostoyanie-risovaniya.html", next_label="Состояние рисования"),
    )
    write("18-12-zhest-myshi.html", out)


def build_13() -> None:
    body = f"""
    <h2>Что должна помнить программа между событиями</h2>
    <p>Три переменные из раздела 18.3 (<code class="inline">tekuschaya_figura</code>,
    <code class="inline">tekuschij_cvet</code>, <code class="inline">tolschina</code>) —
    честный прототип, но по мере роста приложения к ним добавляются точка начала жеста,
    последняя точка карандаша, id черновой фигуры превью — и глобальных переменных становится
    слишком много, чтобы держать их связь в голове.</p>
    {class_diagram(
        "DrawingState",
        ["tool: Tool", "color: str", "width: int", "start_x: float | None", "start_y: float | None",
         "last_x: float | None", "last_y: float | None", "preview_id: int | None"],
        [],
        caption="Один объект вместо семи отдельных переменных — те же данные, но с понятной границей.",
    )}
    {code_block(
        "drawing_state.py",
        "from dataclasses import dataclass\n"
        "from enum import Enum\n\n"
        "class Tool(Enum):\n"
        '    PENCIL = "pencil"\n'
        '    LINE = "line"\n'
        '    RECTANGLE = "rectangle"\n'
        '    OVAL = "oval"\n'
        '    ERASER = "eraser"\n\n'
        "@dataclass\n"
        "class DrawingState:\n"
        "    tool: Tool = Tool.PENCIL\n"
        '    color: str = "#111827"\n'
        "    width: int = 4\n"
        "    start_x: float | None = None\n"
        "    start_y: float | None = None\n",
    )}
    {callout(
        "tip",
        "Enum вместо строк — когда это того стоит",
        "<code class=\"inline\">tekuschaya_figura = \"pryamougolnik\"</code> работает, но опечатку "
        "в строке Python не заметит, пока код не выполнится и фигура тихо не окажется "
        "«неизвестной». <code class=\"inline\">Tool.RECTANGLE</code> — то же самое по смыслу, "
        "но опечатку поймает уже редактор или <code class=\"inline\">python -c \"import module\"</code>. "
        "Enum здесь оправдан ровно потому, что вариантов инструмента конечное известное число "
        "(глава 12 показывала эту идею на других примерах).",
    )}
    {image_figure(f"{IMG}/tool-pencil-selected.png", "Реальное окно: кнопка «Карандаш» на панели инструментов выглядит нажатой (утоплена), остальные — обычные", "Реальное окно: выбран Карандаш — кнопка визуально «утоплена», а не просто где-то в памяти хранится строка.", width=420)}
    {image_figure(f"{IMG}/tool-line-selected.png", "Реальное окно: кнопка «Линия» выглядит нажатой (утоплена), кнопка «Карандаш» вернулась в обычное состояние", "Реальное окно: переключились на Линию — прежняя кнопка вернулась в обычный вид, новая «утоплена».", width=420)}
    {callout(
        "info",
        "Выбранный инструмент виден, а не только хранится в переменной",
        "Состояние — не только то, что помнит Python. Пользователь должен ВИДЕТЬ, какой "
        "инструмент выбран сейчас, не глядя в код. В финальном приложении "
        "<code class=\"inline\">set_tool()</code> одновременно меняет "
        "<code class=\"inline\">self.state.tool</code> И <code class=\"inline\">relief</code> "
        "нужной кнопки — та же связка «модель → отражение на экране», что и "
        "<code class=\"inline\">render()</code> в главе 17.",
    )}

    <h2>Путь этой главы</h2>
    {capability_map([
        ("V1 — глобальные (18.3)", ["3 отдельные переменные", "просто, но растёт бесконтрольно"]),
        ("V2 — DrawingState", ["@dataclass", "параметры инструмента в одном месте"]),
        ("V3 — PaintApp (18.29)", ["DrawingState + документ фигур", "полная архитектура приложения"]),
    ], title="От глобальных переменных к PaintApp")}

    {practice_card(
        "18-13",
        "Практика: моделируем состояние рисования",
        "Автоматическая проверка — выбор инструмента и параметров без Tkinter",
        "../../practice/18-13/index.html",
    )}
    """
    out = render_page(
        page_title="Состояние рисования",
        description="DrawingState как dataclass вместо отдельных глобальных переменных инструмента, цвета и толщины.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Состояние рисования", "")],
        kicker="Глава 18 · Canvas по-настоящему",
        h1="Состояние рисования",
        lede="Инструмент, цвет, толщина и точка начала жеста — параметры, а не сами фигуры.",
        body_html=body,
        sidebar_groups=sidebar("18-13-sostoyanie-risovaniya.html"),
        nav=PageNav(prev_href="18-12-zhest-myshi.html", prev_label="Жест мыши", next_href="18-14-karandash.html", next_label="Карандаш"),
    )
    write("18-13-sostoyanie-risovaniya.html", out)


def build_14() -> None:
    body = f"""
    <h2>Почему кружки на каждое движение — плохая идея</h2>
    <p>Раздел 18.7 рисовал свободный штрих кружками — по одному на каждое событие
    <code class="inline">&lt;B1-Motion&gt;</code>. Работает, но у этого подхода есть три
    проблемы:</p>
    <ul>
      <li>между кружками остаются разрывы, если мышь двигалась быстрее, чем приходили события;</li>
      <li>сама линия выглядит «бугристой», а не гладкой;</li>
      <li>на длинный штрих уходит гораздо больше элементов Canvas, чем нужно.</li>
    </ul>
    {image_figure(f"{IMG}/freehand-naive-dots.png", "Реальный холст: штрих из отдельных кружков с заметными промежутками между ними", "То же самое реальное окно из раздела 18.7: россыпь кружков вместо линии.", width=420)}

    <h2>Лучшая модель: помнить предыдущую точку</h2>
    <p>Вместо кружка на каждое событие — соединяем каждую новую точку с предыдущей отрезком
    прямой. Отрезков много, но вместе они образуют одну непрерывную линию:</p>
    {code_block(
        "karandash.py",
        "def on_drag(self, event):\n"
        "    self.canvas.create_line(\n"
        "        self.state.last_x, self.state.last_y, event.x, event.y,\n"
        "        fill=self.state.color, width=self.state.width,\n"
        "        capstyle=tk.ROUND, smooth=True,\n"
        "    )\n"
        "    self.state.last_x, self.state.last_y = event.x, event.y\n",
    )}
    {image_figure(f"{IMG}/freehand-connected-stroke.png", "Реальный холст: непрерывная плавная линия без разрывов, повторяющая движение мыши", "Реальное окно финальной версии: та же самая рука, но линия без разрывов — потому что рисуются отрезки, а не отдельные точки.", width=420)}
    {comparison_table(
        ["Параметр", "Зачем"],
        [
            ["<code class=\"inline\">capstyle=tk.ROUND</code>", "скругляет концы каждого отрезка — стыки между ними не выглядят «зубчатыми»"],
            ["<code class=\"inline\">smooth=True</code>", "Tk слегка сглаживает саму линию — не творит чудес, но убирает часть угловатости на резких поворотах"],
        ],
    )}
    {callout(
        "warning",
        "smooth=True не делает штрих идеально гладким",
        "Это лёгкое визуальное сглаживание средствами Tk, а не полноценная интерполяция кривой. "
        "На частых, мелких движениях эффект малозаметен — не стоит обещать пользователю "
        "«художественную» гладкость, которую этот параметр не даёт.",
    )}

    {local_required_card(
        "18-14",
        "Практика: непрерывный штрих карандаша",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-14/index.html",
    )}
    """
    out = render_page(
        page_title="Карандаш: непрерывный штрих",
        description="Почему рисование кружками на каждое движение мыши создаёт разрывы, и как получить непрерывный штрих через last_x/last_y.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Карандаш", "")],
        kicker="Глава 18 · Инструменты рисования",
        h1="Карандаш: непрерывный штрих",
        lede="Отдельные кружки создают разрывы. Соединяем каждую точку с предыдущей — и штрих "
        "становится одной линией.",
        body_html=body,
        sidebar_groups=sidebar("18-14-karandash.html"),
        nav=PageNav(prev_href="18-13-sostoyanie-risovaniya.html", prev_label="Состояние рисования", next_href="18-15-instrument-liniya.html", next_label="Инструмент «Линия»"),
    )
    write("18-14-karandash.html", out)


def build_15() -> None:
    body = f"""
    <h2>Линия — не то же самое, что карандаш</h2>
    <p>У карандаша нет заранее известного конца: штрих завершается там, где пользователь отпустит
    кнопку, и линия строится из множества маленьких отрезков «на лету». У инструмента «Линия» всё
    иначе — есть ровно ОДНА прямая от точки нажатия до точки отпускания, и до самого конца жеста
    она — только черновик, который может ещё много раз поменяться.</p>
    {code_block(
        "instrument_liniya.py",
        "def on_press(self, event):\n"
        "    self.state.start_x, self.state.start_y = event.x, event.y\n"
        "    self.state.preview_id = self.canvas.create_line(\n"
        "        event.x, event.y, event.x, event.y,\n"
        "        fill=self.state.color, width=self.state.width, dash=(4, 2),\n"
        "    )\n\n"
        "def on_drag(self, event):\n"
        "    self.canvas.coords(\n"
        "        self.state.preview_id,\n"
        "        self.state.start_x, self.state.start_y, event.x, event.y,\n"
        "    )\n\n"
        "def on_release(self, event):\n"
        "    self.canvas.delete(self.state.preview_id)\n"
        "    self.canvas.create_line(\n"
        "        self.state.start_x, self.state.start_y, event.x, event.y,\n"
        "        fill=self.state.color, width=self.state.width,\n"
        "    )\n",
    )}
    {image_figure(f"{IMG}/mouse-drag-preview-line.png", "Реальное окно: пунктирная линия-превью тянется от точки нажатия к текущей позиции курсора", "Реальное окно: во время перетаскивания — пунктирная черновая линия, ещё не финальная.", width=420)}
    {image_figure(f"{IMG}/line-final.png", "Реальное окно: сплошная финальная линия на месте бывшего пунктирного превью", "Реальное окно: кнопку отпустили — сплошная линия заменила пунктирный черновик.", width=420)}
    {callout(
        "info",
        "dash=(4, 2) — визуальный сигнал «это ещё не финал»",
        "Пунктир у превью — не техническое требование Canvas, а сознательный выбор: пользователь "
        "должен на глаз отличать черновую фигуру от готовой. Раздел 18.18 обобщает этот приём "
        "«создать превью → обновлять coords() → зафиксировать на release» для прямоугольника и "
        "овала — с линией он работает точно так же.",
    )}

    {local_required_card(
        "18-15",
        "Практика: инструмент «Линия» с превью",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-15/index.html",
    )}
    """
    out = render_page(
        page_title="Инструмент «Линия»",
        description="Точка нажатия, пунктирное превью через coords() и финальная линия на отпускании кнопки мыши.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Инструмент «Линия»", "")],
        kicker="Глава 18 · Инструменты рисования",
        h1="Инструмент «Линия»",
        lede="Точка → пунктирный черновик, который обновляется на лету → финальная сплошная линия.",
        body_html=body,
        sidebar_groups=sidebar("18-15-instrument-liniya.html"),
        nav=PageNav(prev_href="18-14-karandash.html", prev_label="Карандаш", next_href="18-16-geometriya-pryamougolnika.html", next_label="Геометрия прямоугольника"),
    )
    write("18-15-instrument-liniya.html", out)


def build_16() -> None:
    dirs = [
        coordinate_diagram(points=[(30, 30, "старт", "#5B24F9"), (140, 110, "сейчас", "#DB2777")], rect=(30, 30, 140, 110), caption="вниз-вправо", width=200, height=160),
        coordinate_diagram(points=[(140, 30, "старт", "#5B24F9"), (30, 110, "сейчас", "#DB2777")], rect=(30, 30, 140, 110), caption="вниз-влево", width=200, height=160),
        coordinate_diagram(points=[(30, 110, "старт", "#5B24F9"), (140, 30, "сейчас", "#DB2777")], rect=(30, 30, 140, 110), caption="вверх-вправо", width=200, height=160),
        coordinate_diagram(points=[(140, 110, "старт", "#5B24F9"), (30, 30, "сейчас", "#DB2777")], rect=(30, 30, 140, 110), caption="вверх-влево", width=200, height=160),
    ]
    body = f"""
    <h2>Два угла — четыре возможных направления</h2>
    <p><code class="inline">canvas.create_rectangle(x1, y1, x2, y2)</code> рисует прямоугольник
    между двумя точками — но пользователь может тянуть мышь в любую сторону от точки старта:
    вниз-вправо, вниз-влево, вверх-вправо, вверх-влево. Прямоугольник получается один и тот же —
    Tk сам разбирается, какая координата больше:</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;margin:20px 0">
      {"".join(dirs)}
    </div>
    <p>Но если координаты нужны и вашему коду — например, чтобы сохранить фигуру в документе
    (раздел 18.13) с предсказуемым порядком точек, — стоит явно привести их к одному виду:</p>
    {code_block(
        "normalize_bounds.py",
        "def normalize_bounds(x1, y1, x2, y2):\n"
        '    """Приводит две произвольные противоположные точки к (left, top, right, bottom)."""\n'
        "    return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)\n",
    )}
    {callout(
        "tip",
        "Canvas это уже делает сам, а normalize_bounds() — для вашего кода",
        "<code class=\"inline\">create_rectangle()</code> прекрасно рисует прямоугольник, даже "
        "если <code class=\"inline\">x1 &gt; x2</code> — сам Tk не путается в направлении. "
        "<code class=\"inline\">normalize_bounds()</code> нужна не Canvas, а вашей модели "
        "документа: чтобы одна и та же фигура, нарисованная в любую сторону, сохранялась в JSON "
        "(раздел 18.30) в одном и том же предсказуемом виде.",
    )}

    {practice_card(
        "18-16",
        "Практика: normalize_bounds() для всех направлений перетаскивания",
        "Автоматическая проверка — приводим координаты к (left, top, right, bottom) без Tkinter",
        "../../practice/18-16/index.html",
    )}
    """
    out = render_page(
        page_title="Геометрия прямоугольника",
        description="Четыре направления перетаскивания мыши и нормализация координат прямоугольника к (left, top, right, bottom).",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Геометрия прямоугольника", "")],
        kicker="Глава 18 · Инструменты рисования",
        h1="Геометрия прямоугольника",
        lede="Мышь можно тянуть в любую из четырёх сторон — прямоугольник должен получиться "
        "одинаковым.",
        body_html=body,
        sidebar_groups=sidebar("18-16-geometriya-pryamougolnika.html"),
        nav=PageNav(prev_href="18-15-instrument-liniya.html", prev_label="Инструмент «Линия»", next_href="18-17-geometriya-ovala.html", next_label="Геометрия овала"),
    )
    write("18-16-geometriya-pryamougolnika.html", out)


def build_17() -> None:
    body = f"""
    <h2>Овал — это прямоугольник с закруглёнными углами до предела</h2>
    <p><code class="inline">canvas.create_oval(x1, y1, x2, y2)</code> принимает ровно те же четыре
    числа, что и <code class="inline">create_rectangle()</code> — но рисует не прямоугольник, а
    эллипс, <strong>вписанный</strong> в него. Прямоугольник при этом не рисуется — он просто
    определяет границы, внутри которых строится овал.</p>
    {coordinate_diagram(
        points=[(30, 30, "P1", "#5B24F9"), (170, 120, "P2", "#DB2777")],
        rect=(30, 30, 170, 120),
        caption="Пунктирный прямоугольник — это те же координаты, что вы передали в create_oval(); сам овал строится внутри него.",
        width=380, height=260,
    )}
    {image_figure(f"{IMG}/oval-final.png", "Реальное окно: овал, аккуратно вписанный в невидимую прямоугольную область между двумя точками", "Реальное окно: create_oval(x1, y1, x2, y2) — овал касается всех четырёх сторон невидимого прямоугольника.", width=380)}
    {callout(
        "info",
        "Не «центр + радиус», а именно ограничивающий прямоугольник",
        "У Canvas нет отдельного <code class=\"inline\">create_circle()</code>: круг — это просто "
        "овал, у которого ограничивающий прямоугольник — квадрат "
        "(<code class=\"inline\">x2 - x1 == y2 - y1</code>). Если приложению всё-таки нужны "
        "«центр + радиус» (например, для игровой логики), их несложно пересчитать в границы: "
        "<code class=\"inline\">x1, y1 = cx - r, cy - r</code> и "
        "<code class=\"inline\">x2, y2 = cx + r, cy + r</code>.",
    )}

    {practice_card(
        "18-17",
        "Практика: ограничивающий прямоугольник овала",
        "Автоматическая проверка — переводим координаты между «центр+радиус» и границами create_oval",
        "../../practice/18-17/index.html",
    )}
    """
    out = render_page(
        page_title="Геометрия овала",
        description="create_oval рисует эллипс, вписанный в прямоугольник — не круг из центра и радиуса.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Геометрия овала", "")],
        kicker="Глава 18 · Инструменты рисования",
        h1="Геометрия овала",
        lede="create_oval принимает те же четыре координаты, что и прямоугольник — овал вписан в "
        "невидимые границы.",
        body_html=body,
        sidebar_groups=sidebar("18-17-geometriya-ovala.html"),
        nav=PageNav(prev_href="18-16-geometriya-pryamougolnika.html", prev_label="Геометрия прямоугольника", next_href="18-18-zhivoe-prevyu.html", next_label="Живое превью"),
    )
    write("18-17-geometriya-ovala.html", out)


def build_18() -> None:
    body = f"""
    <h2>Не пересоздавать фигуру на каждое движение</h2>
    <p>Наивный подход к превью — на каждом <code class="inline">&lt;B1-Motion&gt;</code> удалять
    старую черновую фигуру и создавать новую. Работает, но заставляет Canvas без остановки
    выбрасывать и заново строить элементы — а заодно теряет любые индивидуальные настройки,
    которые вы, возможно, ставили только один раз.</p>
    {flowchart([
        {"kind": "start", "label": "on_press: создать превью ОДИН раз"},
        {"kind": "process", "label": "on_drag: coords(preview_id, ...) — обновить координаты"},
        {"kind": "process", "label": "on_drag: coords(preview_id, ...) — снова"},
        {"kind": "process", "label": "on_drag: coords(preview_id, ...) — и так далее"},
        {"kind": "end", "label": "on_release: зафиксировать финальный вид"},
    ], caption="CREATE ONCE → UPDATE MANY TIMES → COMMIT — один и тот же элемент, а не поток одноразовых.")}
    {code_block(
        "zhivoe_prevyu.py",
        "def on_press(self, event):\n"
        "    self.state.preview_id = self.canvas.create_rectangle(\n"
        "        event.x, event.y, event.x, event.y,\n"
        "        outline=self.state.color, width=self.state.width, dash=(4, 2),\n"
        "    )\n\n"
        "def on_drag(self, event):\n"
        "    self.canvas.coords(\n"
        "        self.state.preview_id,\n"
        "        self.state.start_x, self.state.start_y, event.x, event.y,\n"
        "    )\n",
    )}
    {image_figure(f"{IMG}/rectangle-preview.png", "Реальное окно: пунктирный прямоугольник-превью на полпути перетаскивания", "Реальное окно: один и тот же элемент preview_id меняет размер на каждый coords() — не создаётся заново.", width=420)}
    {image_figure(f"{IMG}/oval-preview.png", "Реальное окно: пунктирный овал-превью на полпути перетаскивания", "Реальное окно: та же самая идея работает и для овала — меняется только форма, которую рисует create_oval().", width=420)}
    {callout(
        "tip",
        "coords() принимает столько чисел, сколько нужно фигуре",
        "Для линии и прямоугольника — четыре числа (две точки). Для многоточечной ломаной "
        "(например, растущего карандашного контура) — сколько угодно пар "
        "<code class=\"inline\">x, y</code>. Главное — вызывать <code class=\"inline\">coords()</code> "
        "с тем же <code class=\"inline\">item_id</code>, что вернул исходный "
        "<code class=\"inline\">create_*</code>.",
    )}

    {local_required_card(
        "18-18",
        "Практика: живое превью через coords()",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-18/index.html",
    )}
    """
    out = render_page(
        page_title="Живое превью: coords()",
        description="CREATE ONCE, UPDATE MANY TIMES, COMMIT — обновление одного элемента Canvas вместо пересоздания на каждое движение мыши.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Живое превью", "")],
        kicker="Глава 18 · Инструменты рисования",
        h1="Живое превью: coords()",
        lede="Один элемент создаётся один раз и много раз обновляется — вместо потока "
        "одноразовых фигур.",
        body_html=body,
        sidebar_groups=sidebar("18-18-zhivoe-prevyu.html"),
        nav=PageNav(prev_href="18-17-geometriya-ovala.html", prev_label="Геометрия овала", next_href="18-19-redaktirovanie-elementov.html", next_label="itemconfig, move, delete"),
    )
    write("18-18-zhivoe-prevyu.html", out)


def build_19() -> None:
    body = f"""
    <h2>Три способа изменить уже нарисованное</h2>
    {comparison_table(
        ["Метод", "Что меняет"],
        [
            ["<code class=\"inline\">canvas.coords(id, ...)</code>", "координаты элемента — форму и положение"],
            ["<code class=\"inline\">canvas.itemconfig(id, ...)</code>", "визуальные параметры — цвет, толщину, стиль — без изменения формы"],
            ["<code class=\"inline\">canvas.move(id, dx, dy)</code>", "сдвигает элемент НА dx, dy — а не задаёт абсолютную позицию"],
            ["<code class=\"inline\">canvas.delete(id)</code>", "убирает элемент насовсем"],
        ],
    )}
    {code_block(
        "redaktirovanie.py",
        "item_id = canvas.create_rectangle(10, 10, 80, 60, outline=\"black\", width=2)\n\n"
        'canvas.itemconfig(item_id, outline="blue", width=4)   # тот же прямоугольник, другой вид\n'
        "canvas.move(item_id, 30, 0)                           # сдвинуть на 30px вправо\n"
        "canvas.coords(item_id, 10, 10, 150, 100)               # изменить сами границы\n"
        "canvas.delete(item_id)                                # убрать совсем\n",
    )}
    {callout(
        "warning",
        "move(id, dx, dy) — это смещение, а не координата",
        "<code class=\"inline\">canvas.move(item_id, 30, 0)</code> означает «сдвинь на 30 "
        "пикселей вправо от текущего положения», а не «помести на x=30». Вызвать "
        "<code class=\"inline\">move()</code> дважды подряд с одними и теми же аргументами "
        "сдвинет элемент на общие 60 пикселей, а не оставит его на месте.",
    )}
    <p>Все три способа — <code class="inline">coords()</code>, <code class="inline">itemconfig()</code>,
    <code class="inline">move()</code> — работают и по <code class="inline">item_id</code>, и по
    тегу (раздел 18.11): <code class="inline">canvas.itemconfig("preview", ...)</code> изменит
    сразу все элементы с этим тегом.</p>

    {local_required_card(
        "18-19",
        "Практика: coords, itemconfig, move, delete",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-19/index.html",
    )}
    """
    out = render_page(
        page_title="itemconfig, move, delete",
        description="coords/itemconfig/move/delete — четыре способа изменить уже созданный элемент Canvas.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Редактирование элементов", "")],
        kicker="Глава 18 · Инструменты рисования",
        h1="itemconfig, move, delete",
        lede="Элемент Canvas не обязательно пересоздавать — его можно изменить на месте.",
        body_html=body,
        sidebar_groups=sidebar("18-19-redaktirovanie-elementov.html"),
        nav=PageNav(prev_href="18-18-zhivoe-prevyu.html", prev_label="Живое превью", next_href="18-20-poryadok-sloev.html", next_label="Порядок наложения"),
    )
    write("18-19-redaktirovanie-elementov.html", out)


def build_20() -> None:
    body = f"""
    <h2>Что нарисовано позже — оказывается сверху</h2>
    <p>Элементы Canvas хранятся не только как список, но и в определённом ПОРЯДКЕ — том самом,
    в котором их создали. Если два элемента перекрываются, верхним окажется тот, что был создан
    позже:</p>
    {image_figure(f"{IMG}/stacking-order-before.png", "Реальное окно: три перекрывающихся фигуры — прямоугольник, овал и линия — овал поверх прямоугольника, линия поверх обоих", "Реальное окно: порядок создания — прямоугольник, затем овал, затем линия. Линия оказалась сверху.", width=420)}
    <p>Этот порядок можно изменить явно — поднять элемент выше или опустить ниже остальных:</p>
    {code_block(
        "poryadok_sloev.py",
        'canvas.tag_raise(rect_id)          # поднять прямоугольник НАД всеми остальными\n'
        'canvas.tag_lower(rect_id)          # опустить прямоугольник ПОД всеми остальными\n'
        'canvas.tag_raise(rect_id, oval_id)  # поднять прямоугольник только НАД конкретным овалом\n',
    )}
    {image_figure(f"{IMG}/stacking-order-after.png", "Реальное окно: та же тройка фигур, но прямоугольник теперь поверх овала и линии", "Реальное окно: после tag_raise(rect_id) — прямоугольник теперь выше остальных.", width=420)}
    {callout(
        "info",
        "Небольшой предвкус слоёв графических редакторов",
        "Настоящие графические редакторы строят на этой идее целую систему слоёв — со скрытием, "
        "блокировкой, группами. Здесь мы не реализуем ничего из этого: "
        "<code class=\"inline\">tag_raise</code>/<code class=\"inline\">tag_lower</code> — лишь "
        "демонстрация того, что порядок наложения существует и им можно управлять, если "
        "понадобится.",
    )}

    {practice_card(
        "18-20",
        "Практика: порядок наложения элементов",
        "Автоматическая проверка — предсказываем итоговый порядок после tag_raise/tag_lower",
        "../../practice/18-20/index.html",
    )}
    """
    out = render_page(
        page_title="Порядок наложения",
        description="Canvas хранит элементы в порядке создания — tag_raise/tag_lower меняют, какой элемент окажется сверху.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Порядок наложения", "")],
        kicker="Глава 18 · Инструменты рисования",
        h1="Порядок наложения",
        lede="Позже нарисованный элемент оказывается сверху — если не сказать Canvas иначе.",
        body_html=body,
        sidebar_groups=sidebar("18-20-poryadok-sloev.html"),
        nav=PageNav(prev_href="18-19-redaktirovanie-elementov.html", prev_label="Редактирование элементов", next_href="18-21-sistema-cveta.html", next_label="Система цвета"),
    )
    write("18-20-poryadok-sloev.html", out)


def build_21() -> None:
    swatches = color_swatch_row([
        ("#111827", "Чёрный", "#111827"),
        ("#dc2626", "Красный", "#dc2626"),
        ("#2563eb", "Синий", "#2563eb"),
        ("#16a34a", "Зелёный", "#16a34a"),
        ("#f59e0b", "Оранжевый", "#f59e0b"),
        ("#7c3aed", "Фиолетовый", "#7c3aed"),
    ])
    body = f"""
    <h2>Цвет нужно видеть, а не только читать в коде</h2>
    <p>Шесть цветов палитры финального приложения — не абстрактные строки, а конкретные оттенки:</p>
    {swatches}
    {image_figure(f"{IMG}/color-palette.png", "Реальное окно: ряд цветных кнопок палитры над холстом", "Реальное окно: та же палитра — каждая кнопка красится в свой bg=hex_color.", width=420)}

    <h2>Свой цвет — через colorchooser</h2>
    <p>Готовая палитра — это только шесть вариантов. Модуль <code class="inline">tkinter.colorchooser</code>
    открывает нативный системный диалог выбора любого цвета:</p>
    {code_block(
        "custom_color.py",
        "from tkinter import colorchooser\n\n"
        "def choose_custom_color(self):\n"
        "    _rgb, hex_color = colorchooser.askcolor(color=self.state.color, title=\"Выберите цвет\")\n"
        "    if hex_color is not None:\n"
        "        self.set_color(hex_color)\n",
    )}
    {color_dialog_schematic("#7c3aed", "Схема нативного диалога colorchooser — под headless Xvfb он не рендерится предсказуемо без реального клика пользователя, поэтому здесь показана его структура, а не скриншот.")}
    {callout(
        "warning",
        "askcolor() может вернуть (None, None)",
        "Если пользователь нажимает «Отмена», <code class=\"inline\">askcolor()</code> "
        "возвращает <code class=\"inline\">(None, None)</code>, а не какой-то цвет по умолчанию. "
        "Код обязан проверить <code class=\"inline\">hex_color is not None</code> перед "
        "использованием — иначе следующий вызов, ожидающий строку вроде "
        "<code class=\"inline\">\"#7c3aed\"</code>, получит <code class=\"inline\">None</code> и "
        "упадёт с ошибкой.",
    )}
    {image_figure(f"{IMG}/custom-color-result.png", "Реальное окно: текущий цвет в панели инструментов изменился на нестандартный оттенок, выбранный через диалог", "Реальное окно: результат выбора пользовательского цвета — сам диалог не captured, но эффект от него виден по-настоящему.", width=420)}

    {local_required_card(
        "18-21",
        "Практика: палитра и пользовательский цвет",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-21/index.html",
    )}
    """
    out = render_page(
        page_title="Система цвета",
        description="Палитра цветов, реальные образцы swatches и выбор произвольного цвета через tkinter.colorchooser.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Система цвета", "")],
        kicker="Глава 18 · Инструменты рисования",
        h1="Система цвета",
        lede="Шесть быстрых цветов и colorchooser для любого другого — цвет нужно видеть, а не "
        "только читать hex-код.",
        body_html=body,
        sidebar_groups=sidebar("18-21-sistema-cveta.html"),
        nav=PageNav(prev_href="18-20-poryadok-sloev.html", prev_label="Порядок наложения", next_href="18-22-tolschina-kisti.html", next_label="Толщина кисти"),
    )
    write("18-21-sistema-cveta.html", out)


def build_22() -> None:
    body = f"""
    <h2>Толщина в коде — и толщина на экране</h2>
    <p>Четыре линии одного цвета, нарисованные с разной толщиной — разница видна сразу, без
    необходимости представлять её по числу:</p>
    {image_figure(f"{IMG}/width-comparison.png", "Реальный холст: четыре горизонтальные линии одного цвета толщиной 1, 3, 8 и 16 пикселей с подписанными числами рядом", "Реальный холст: width=1, 3, 8, 16 — одна и та же линия, разная толщина.", width=460)}
    {code_block(
        "tolschina_kisti.py",
        'self.width_scale = tk.Scale(\n'
        '    toolbar, from_=1, to=20, orient="horizontal", command=self.set_width,\n'
        ")\n"
        "self.width_scale.set(4)\n\n"
        "def set_width(self, value):\n"
        "    self.state.width = int(value)\n",
    )}
    {callout(
        "info",
        "command у Scale получает строку, а не Event",
        "Как и в разделе 18.6, обработчик <code class=\"inline\">Scale</code> получает готовое "
        "значение ползунка напрямую строкой — не объект <code class=\"inline\">Event</code>, как "
        "у <code class=\"inline\">.bind()</code>. Отсюда явный <code class=\"inline\">int(value)</code>.",
    )}
    {callout(
        "tip",
        "Толщина хранится в DrawingState, а не только в самом Scale",
        "<code class=\"inline\">self.state.width</code> — источник истины, который читают "
        "<code class=\"inline\">on_press</code>/<code class=\"inline\">on_drag</code>. "
        "<code class=\"inline\">tk.Scale</code> — просто удобный виджет для его изменения, а не "
        "хранилище само по себе: та же логика «виджет отображает состояние, а не является им», "
        "что и в главе 17.",
    )}

    {local_required_card(
        "18-22",
        "Практика: ползунок толщины кисти",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-22/index.html",
    )}
    """
    out = render_page(
        page_title="Толщина кисти",
        description="Scale для выбора толщины линии, реальное сравнение толщин на холсте и связь со состоянием рисования.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Толщина кисти", "")],
        kicker="Глава 18 · Инструменты рисования",
        h1="Толщина кисти",
        lede="Число в коде и толщина линии на экране — покажем разницу вживую, а не только опишем.",
        body_html=body,
        sidebar_groups=sidebar("18-22-tolschina-kisti.html"),
        nav=PageNav(prev_href="18-21-sistema-cveta.html", prev_label="Система цвета", next_href="18-23-lastik.html", next_label="Ластик"),
    )
    write("18-22-tolschina-kisti.html", out)


def build_23() -> None:
    body = f"""
    <h2>Что вообще значит «стереть» на Canvas?</h2>
    <p>В графическом редакторе с обычным растровым изображением ластик очевиден: закрасить
    пиксели цветом фона. Но Canvas хранит не пиксели, а элементы (раздел 18.8) — и у «стереть»
    здесь есть несколько разных честных значений:</p>
    {decision_map([
        ("Закрасить область цветом фона", "ластик = карандаш цветом фона"),
        ("Удалить весь элемент, которого коснулись", "нужен hit-test — find_overlapping()"),
        ("Удалить только часть штриха под курсором", "сложно: пришлось бы резать элемент на части"),
    ], title="Три честных смысла слова «ластик»")}
    <p>Для этого курса выбран первый, самый предсказуемый вариант: ластик — это тот же карандаш
    (раздел 18.14), только цвет штриха принудительно равен цвету фона холста:</p>
    {code_block(
        "lastik.py",
        "def on_drag(self, event):\n"
        "    tool = self.state.tool\n"
        '    if tool in (Tool.PENCIL, Tool.ERASER):\n'
        "        color = CANVAS_BG if tool is Tool.ERASER else self.state.color\n"
        "        self.canvas.create_line(\n"
        "            self.state.last_x, self.state.last_y, event.x, event.y,\n"
        "            fill=color, width=self.state.width, capstyle=tk.ROUND,\n"
        "        )\n"
        "        self.state.last_x, self.state.last_y = event.x, event.y\n",
    )}
    {image_figure(f"{IMG}/eraser-before.png", "Реальное окно: холст с нарисованными фигурами до применения ластика", "Реальное окно: холст с фигурами — до ластика.", width=420)}
    {image_figure(f"{IMG}/eraser-after.png", "Реальное окно: тот же холст с белой полосой на месте штриха ластика поверх фигур", "Реальное окно: после ластика — белая полоса поверх части фигур, а не настоящее удаление затронутых элементов.", width=420)}
    {callout(
        "warning",
        "Это НЕ настоящее удаление затронутых элементов",
        "Такой ластик рисует НОВЫЙ элемент цвета фона поверх старых — сами старые фигуры "
        "остаются в документе, просто визуально перекрыты. Если фон холста когда-нибудь "
        "изменится (например, вы добавите фоновое изображение), «стёртые» линии снова станут "
        "видны — это не баг, а прямое следствие выбранной модели.",
    )}
    {callout(
        "info",
        "Настоящее удаление — необязательное расширение",
        "Метод <code class=\"inline\">canvas.find_overlapping(x1, y1, x2, y2)</code> находит все "
        "элементы в прямоугольной области под курсором ластика — их можно удалить по-настоящему "
        "через <code class=\"inline\">canvas.delete(item_id)</code>. Это честная, но заметно "
        "более сложная альтернатива: она требует решить, что делать, если ластик задел только "
        "ЧАСТЬ длинной фигуры. В этой главе она не реализована, но упомянута как реальное "
        "направление развития.",
    )}

    {local_required_card(
        "18-23",
        "Практика: ластик как штрих цветом фона",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-23/index.html",
    )}
    """
    out = render_page(
        page_title="Ластик",
        description="Ластик на Canvas реализован как штрих цветом фона — что это означает и в чём ограничение такого подхода.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Ластик", "")],
        kicker="Глава 18 · Инструменты рисования",
        h1="Ластик",
        lede="На Canvas «стереть» — не единственно возможное действие. Разберём, какой смысл "
        "выбран здесь и почему.",
        body_html=body,
        sidebar_groups=sidebar("18-23-lastik.html"),
        nav=PageNav(prev_href="18-22-tolschina-kisti.html", prev_label="Толщина кисти", next_href="18-24-otmena-deystviy.html", next_label="Отмена действий"),
    )
    write("18-23-lastik.html", out)


def build_24() -> None:
    body = f"""
    <h2>Отмена по действиям, а не по элементам Canvas</h2>
    <p>Наивная реализация Undo — просто удалить последний созданный элемент Canvas. Проблема:
    один карандашный штрих состоит из МНОГИХ отдельных отрезков (раздел 18.14) — «отменить»
    удалит только последний крошечный кусочек штриха, а не весь его целиком, чего пользователь
    точно не ожидает.</p>
    {code_block(
        "istoriya_deystviy.py",
        "undo_stack = [\n"
        "    [item_id_1, item_id_2, item_id_3],  # один карандашный штрих — три отрезка\n"
        "    [item_id_4],                         # один прямоугольник — один элемент\n"
        "]\n",
    )}
    <p>Финальное приложение решает это через документ (раздел 18.13, 18.29): каждое пользовательское
    действие — один или несколько объектов <code class="inline">Shape</code> — целиком добавляется в
    документ и целиком же может быть отменено:</p>
    {code_block(
        "undo.py",
        "def _commit_action(self, shapes):\n"
        "    self.document.extend(shapes)\n"
        "    self.undo_stack.append(shapes)   # ОДНО действие — даже если shapes из многих отрезков\n"
        "    self.redo_stack.clear()\n"
        "    self.render_document()\n\n"
        "def undo(self):\n"
        "    if not self.undo_stack:\n"
        "        return\n"
        "    shapes = self.undo_stack.pop()\n"
        "    del self.document[len(self.document) - len(shapes):]\n"
        "    self.redo_stack.append(shapes)\n"
        "    self.render_document()\n",
    )}
    {image_figure(f"{IMG}/undo-before.png", "Реальное окно: холст с несколькими фигурами, включая последний нарисованный прямоугольник", "Реальное окно: до Ctrl+Z — виден весь рисунок, включая последнее действие.", width=420)}
    {image_figure(f"{IMG}/undo-after.png", "Реальное окно: тот же холст без последнего прямоугольника, остальные фигуры на месте", "Реальное окно: после Ctrl+Z — последнее ДЕЙСТВИЕ убрано целиком, предыдущие фигуры не тронуты.", width=420)}
    {callout(
        "info",
        "render_document() — то же render(), что и в главе 17",
        "После отмены документ меняется, а холст просто ПЕРЕРИСОВЫВАЕТСЯ из него заново — не "
        "точечное удаление конкретных элементов Canvas. Тот же принцип «модель меняют действия, "
        "Canvas только отображает текущее состояние», что и <code class=\"inline\">render()</code> "
        "в игре «Крестики-нолики».",
    )}

    {practice_card(
        "18-24",
        "Практика: стек отмены по действиям",
        "Автоматическая проверка — undo убирает ВСЕ элементы одного действия, а не один",
        "../../practice/18-24/index.html",
    )}
    """
    out = render_page(
        page_title="Отмена действий (Undo)",
        description="Undo по логическим действиям, а не по отдельным элементам Canvas — один карандашный штрих отменяется целиком.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Отмена действий", "")],
        kicker="Глава 18 · История и документ",
        h1="Отмена действий (Undo)",
        lede="Один пользовательский жест может состоять из многих элементов Canvas — отменяться "
        "он должен целиком.",
        body_html=body,
        sidebar_groups=sidebar("18-24-otmena-deystviy.html"),
        nav=PageNav(prev_href="18-23-lastik.html", prev_label="Ластик", next_href="18-25-povtor-deystviy.html", next_label="Повтор действий"),
    )
    write("18-24-otmena-deystviy.html", out)


def build_25() -> None:
    body = f"""
    <h2>Redo — второй стек, а не «отмена отмены»</h2>
    <p>Раздел 18.24 отменяет действие, снимая его с <code class="inline">undo_stack</code>. Чтобы
    вернуть его назад, само действие нужно куда-то временно положить — во второй стек,
    <code class="inline">redo_stack</code>:</p>
    {code_block(
        "redo.py",
        "def redo(self):\n"
        "    if not self.redo_stack:\n"
        "        return\n"
        "    shapes = self.redo_stack.pop()\n"
        "    self.document.extend(shapes)\n"
        "    self.undo_stack.append(shapes)\n"
        "    self.render_document()\n",
    )}
    {image_figure(f"{IMG}/redo-after.png", "Реальное окно: прямоугольник, ранее убранный через Undo, снова виден на холсте после Redo", "Реальное окно: после Ctrl+Y — действие, отменённое в разделе 18.24, восстановлено.", width=420)}

    <h2>Новое действие обязано опустошить redo_stack</h2>
    <p>Если после Undo пользователь рисует что-то НОВОЕ, старая ветка «которую можно было бы
    повторить» перестаёт иметь смысл — вернуть её означало бы применить действие к документу,
    который уже стал другим. Поэтому <code class="inline">_commit_action()</code> (раздел 18.24)
    всегда очищает <code class="inline">redo_stack</code>:</p>
    {code_block(
        "commit_ochischaet_redo.py",
        "def _commit_action(self, shapes):\n"
        "    self.document.extend(shapes)\n"
        "    self.undo_stack.append(shapes)\n"
        "    self.redo_stack.clear()   # новое действие делает старую ветку redo недействительной\n"
        "    self.render_document()\n",
    )}
    {callout(
        "warning",
        "Забытый redo_stack.clear() — незаметная, но реальная ошибка",
        "Без этой строки Redo мог бы «воскресить» фигуру, которая никак не связана с текущим "
        "состоянием документа — потому что после Undo пользователь успел нарисовать что-то ещё, "
        "а старое отменённое действие всё ещё лежит в очереди «повторить». Раздел 18.31 разбирает "
        "этот случай как отдельный Debug Lab.",
    )}

    {practice_card(
        "18-25",
        "Практика: стек повтора и его очистка новым действием",
        "Автоматическая проверка — redo восстанавливает действие, новое действие обнуляет redo",
        "../../practice/18-25/index.html",
    )}
    """
    out = render_page(
        page_title="Повтор действий (Redo)",
        description="redo_stack как второй стек истории и обязательная его очистка при новом действии после Undo.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Повтор действий", "")],
        kicker="Глава 18 · История и документ",
        h1="Повтор действий (Redo)",
        lede="Redo — второй стек рядом с Undo. Новое действие после отмены должно его опустошить.",
        body_html=body,
        sidebar_groups=sidebar("18-25-povtor-deystviy.html"),
        nav=PageNav(prev_href="18-24-otmena-deystviy.html", prev_label="Отмена действий", next_href="18-26-ochistka-holsta.html", next_label="Очистка холста"),
    )
    write("18-25-povtor-deystviy.html", out)


def build_26() -> None:
    body = f"""
    <h2>«Очистить» — необратимое действие</h2>
    <p>Кнопка «Очистить холст» удаляет ВЕСЬ рисунок разом. В отличие от Undo, здесь нет
    предыдущего состояния, к которому можно легко вернуться, — если история отмены тоже
    очищается вместе с документом. Поэтому перед необратимым действием стоит спросить
    подтверждение, но только если есть что терять:</p>
    {code_block(
        "ochistka_holsta.py",
        "def clear_canvas(self):\n"
        "    if self.document and not messagebox.askyesno(\n"
        '        "Очистить холст", "Удалить весь рисунок без возможности отмены?"\n'
        "    ):\n"
        "        return\n"
        "    self.document.clear()\n"
        "    self.undo_stack.clear()\n"
        "    self.redo_stack.clear()\n"
        "    self.render_document()\n",
    )}
    {callout(
        "warning",
        "Очистка холста, забывшая очистить историю",
        "Если удалить только фигуры (<code class=\"inline\">self.document.clear()</code>), но не "
        "тронуть <code class=\"inline\">undo_stack</code>, — <code class=\"inline\">undo()</code> "
        "после очистки попробует убрать из ПУСТОГО документа фигуры, которых там уже нет. "
        "Раздел 18.31 разбирает этот случай отдельно: история обязана обнуляться вместе с "
        "документом, который она описывает.",
    )}
    {callout(
        "info",
        "Спрашиваем подтверждение не всегда",
        "Если <code class=\"inline\">self.document</code> уже пуст, спрашивать «точно очистить?» "
        "не о чем — лишнее диалоговое окно только раздражает. Проверка "
        "<code class=\"inline\">if self.document and ...</code> пропускает подтверждение именно "
        "в этом случае.",
    )}

    {local_required_card(
        "18-26",
        "Практика: безопасная очистка холста",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-26/index.html",
    )}
    """
    out = render_page(
        page_title="Очистка холста",
        description="Подтверждение перед необратимой очисткой и обязательное обнуление истории отмены вместе с документом.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Очистка холста", "")],
        kicker="Глава 18 · История и документ",
        h1="Очистка холста",
        lede="Необратимое действие заслуживает подтверждения — и обязано обнулить историю "
        "отмены вместе с документом.",
        body_html=body,
        sidebar_groups=sidebar("18-26-ochistka-holsta.html"),
        nav=PageNav(prev_href="18-25-povtor-deystviy.html", prev_label="Повтор действий", next_href="18-27-goryachie-klavishi.html", next_label="Горячие клавиши"),
    )
    write("18-26-ochistka-holsta.html", out)


def build_27() -> None:
    body = f"""
    <h2>Быстрые команды с клавиатуры</h2>
    {comparison_table(
        ["Сочетание", "Действие"],
        [
            ["<code class=\"inline\">Ctrl+Z</code>", "Undo — отменить последнее действие"],
            ["<code class=\"inline\">Ctrl+Y</code>", "Redo — повторить отменённое действие"],
            ["<code class=\"inline\">Ctrl+N</code>", "очистить холст (с подтверждением)"],
            ["<code class=\"inline\">Ctrl+S</code>", "сохранить рисунок в JSON"],
            ["<code class=\"inline\">Ctrl+O</code>", "открыть сохранённый рисунок"],
        ],
    )}
    {code_block(
        "goryachie_klavishi.py",
        'self.root.bind("<Control-z>", lambda _e: self.undo())\n'
        'self.root.bind("<Control-y>", lambda _e: self.redo())\n'
        'self.root.bind("<Control-s>", lambda _e: self.save_document())\n'
        'self.root.bind("<Control-o>", lambda _e: self.load_document())\n'
        'self.root.bind("<Control-n>", lambda _e: self.clear_canvas())\n',
    )}
    {callout(
        "warning",
        "Сочетания клавиш — не универсальны между операционными системами",
        "<code class=\"inline\">Ctrl</code> — стандарт для Windows и Linux. На macOS "
        "пользователи по привычке ждут <code class=\"inline\">Cmd</code>, а не "
        "<code class=\"inline\">Ctrl</code> — Tkinter не подменяет одно другим автоматически. "
        "Полная кроссплатформенная поддержка потребовала бы отдельно проверять "
        "<code class=\"inline\">sys.platform</code> и привязывать оба варианта — эта глава этим "
        "не занимается, но важно не обещать того, чего код не делает.",
    )}
    {callout(
        "info",
        "Привязка на root, а не только на Canvas — вспомним главу 17",
        "Горячие клавиши повешены на <code class=\"inline\">self.root</code>, а не на "
        "<code class=\"inline\">self.canvas</code> — они должны работать независимо от того, "
        "какой именно виджет окна сейчас в фокусе. Если бы в приложении было текстовое поле "
        "(например, для подписи рисунка), пришлось бы учитывать те же правила фокуса и "
        "bindtags, что разбирал раздел 17.11 — горячие клавиши не должны перехватывать ввод "
        "текста в поле, где пользователь печатает.",
    )}

    {local_required_card(
        "18-27",
        "Практика: горячие клавиши приложения",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-27/index.html",
    )}
    """
    out = render_page(
        page_title="Горячие клавиши",
        description="Ctrl+Z/Y/N/S/O для быстрого доступа к Undo/Redo/Clear/Save/Open и заметка о переносимости между ОС.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Горячие клавиши", "")],
        kicker="Глава 18 · Финальные штрихи",
        h1="Горячие клавиши",
        lede="Ctrl+Z, Ctrl+Y и другие быстрые команды — привязаны на root, а не только на холст.",
        body_html=body,
        sidebar_groups=sidebar("18-27-goryachie-klavishi.html"),
        nav=PageNav(prev_href="18-26-ochistka-holsta.html", prev_label="Очистка холста", next_href="18-28-stroka-sostoyaniya.html", next_label="Строка состояния"),
    )
    write("18-27-goryachie-klavishi.html", out)


def build_28() -> None:
    body = f"""
    <h2>Одна строка — четыре факта сразу</h2>
    {image_figure(f"{IMG}/status-bar.png", "Реальное окно: строка состояния внизу окна показывает инструмент, координаты курсора, текущий цвет и толщину", "Реальное окно: строка состояния под холстом — инструмент, координаты, цвет, толщина.", width=460)}
    {code_block(
        "stroka_sostoyaniya.py",
        "def _update_status(self, x, y):\n"
        '    coords = f"x={x} y={y}" if x is not None else "x=— y=—"\n'
        "    self.status_var.set(\n"
        '        f"Инструмент: {TOOL_LABELS[self.state.tool]} | {coords} | "\n'
        '        f"Цвет: {self.state.color} | Толщина: {self.state.width}"\n'
        "    )\n",
    )}
    <p>Строка обновляется в трёх разных местах: при смене инструмента, при движении мыши
    (<code class="inline">&lt;Motion&gt;</code>) и при выборе цвета или толщины — везде, где
    меняется хотя бы одно из четырёх значений.</p>
    {callout(
        "tip",
        "Живое доказательство пользы event.x / event.y",
        "Координаты курсора — не абстракция «где-то в коде»: строка состояния делает их видимыми "
        "в реальном времени, буквально на каждое движение мыши. Это тот же "
        "<code class=\"inline\">event.x</code>/<code class=\"inline\">event.y</code>, который "
        "используют <code class=\"inline\">on_press</code>/<code class=\"inline\">on_drag</code> "
        "для самого рисования.",
    )}

    {local_required_card(
        "18-28",
        "Практика: строка состояния приложения",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-28/index.html",
    )}
    """
    out = render_page(
        page_title="Строка состояния",
        description="Одна строка, показывающая инструмент, координаты курсора, цвет и толщину в реальном времени.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Строка состояния", "")],
        kicker="Глава 18 · Финальные штрихи",
        h1="Строка состояния",
        lede="Инструмент, координаты, цвет и толщина — сразу видны, без необходимости лезть в код.",
        body_html=body,
        sidebar_groups=sidebar("18-28-stroka-sostoyaniya.html"),
        nav=PageNav(prev_href="18-27-goryachie-klavishi.html", prev_label="Горячие клавиши", next_href="18-29-arhitektura-paintapp.html", next_label="Архитектура PaintApp"),
    )
    write("18-28-stroka-sostoyaniya.html", out)


def build_29() -> None:
    body = f"""
    <h2>app HAS-A root — тот же паттерн, что и в главах 16–17</h2>
    {classic_vs_modern(
        "Композиция против наследования",
        "Возможно, но не нужно",
        "class PaintApp(tk.Tk):\n"
        "    def __init__(self):\n"
        "        super().__init__()\n"
        "        ...",
        "Как в главах 16–17",
        "class PaintApp:\n"
        "    def __init__(self, root):\n"
        "        self.root = root\n"
        "        ...",
        "Наследование от <code class=\"inline\">tk.Tk</code> технически работает, но не "
        "согласуется с тем, как строились приложения в этой книге начиная с главы 16. "
        "<code class=\"inline\">app.root</code> — тот же паттерн, что у калькулятора чаевых и "
        "крестиков-ноликов.",
    )}

    <h2>Три обязанности, три группы методов</h2>
    {object_diagram(
        "app", "PaintApp",
        [("root", "Tk"), ("state", "DrawingState"), ("document", "list[Shape]"),
         ("undo_stack", "list[list[Shape]]"), ("redo_stack", "list[list[Shape]]"), ("canvas", "Canvas")],
        caption="app хранит виджеты, параметры инструмента И документ — но не путает их друг с другом.",
    )}
    {comparison_table(
        ["Группа методов", "За что отвечает"],
        [
            ["<code class=\"inline\">build_ui / build_toolbar</code>", "построение виджетов — один раз, при запуске"],
            ["<code class=\"inline\">on_press / on_drag / on_release</code>", "события мыши → изменения state и document"],
            ["<code class=\"inline\">render_document</code>", "документ → Canvas (единственное место, которое рисует по-настоящему)"],
            ["<code class=\"inline\">undo / redo / clear_canvas</code>", "управление историей документа"],
            ["<code class=\"inline\">save_document / load_document</code>", "документ ↔ файл на диске"],
        ],
    )}
    {pipeline_diagram([
        {"kind": "plain", "title": "событие мыши"},
        {"kind": "object", "title": "DrawingState", "rows": ["текущий инструмент, цвет, точка начала"]},
        {"kind": "object", "title": "document: list[Shape]", "rows": ["источник истины"]},
        {"kind": "plain", "title": "render_document()"},
        {"kind": "object", "title": "Canvas"},
    ], caption="Событие меняет СНАЧАЛА состояние и документ — и только потом Canvas перерисовывается из документа.")}
    {callout(
        "info",
        "UI-состояние, документ и отображение — три разных слоя",
        "<code class=\"inline\">DrawingState</code> — что выбрано ПРЯМО СЕЙЧАС (инструмент, "
        "цвет). <code class=\"inline\">document</code> — что уже НАРИСОВАНО и что переживает "
        "смену инструмента. <code class=\"inline\">Canvas</code> — то, что видно на экране, "
        "производное от документа. Смешать первое со вторым — частая причина путаницы: "
        "например, хранить историю Undo внутри <code class=\"inline\">DrawingState</code> вместо "
        "отдельного списка не позволило бы отменять действия, сделанные ДО того, как "
        "пользователь сменил инструмент.",
    )}

    {local_required_card(
        "18-29",
        "Практика: собираем объектный граф PaintApp",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-29/index.html",
    )}
    """
    out = render_page(
        page_title="Архитектура PaintApp",
        description="Композиция вместо наследования от Tk, объектный граф PaintApp и разделение состояния инструмента, документа и отображения.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Архитектура PaintApp", "")],
        kicker="Глава 18 · Финальные штрихи",
        h1="Архитектура PaintApp",
        lede="app.root, состояние инструмента, документ фигур и Canvas — три разных слоя одного "
        "приложения.",
        body_html=body,
        sidebar_groups=sidebar("18-29-arhitektura-paintapp.html"),
        nav=PageNav(prev_href="18-28-stroka-sostoyaniya.html", prev_label="Строка состояния", next_href="18-30-sohranenie-json.html", next_label="Сохранение и загрузка JSON"),
    )
    write("18-29-arhitektura-paintapp.html", out)


def build_30() -> None:
    body = f"""
    <h2>Canvas не сохраняет рисунок как файл — документ сохраняет</h2>
    <p>Важная честная оговорка: <code class="inline">Canvas</code> сам по себе не умеет
    экспортировать себя в обычный PNG или JPEG — надёжный кроссплатформенный растровый экспорт
    требует дополнительных зависимостей и выходит за рамки этой главы. Вместо этого мы сохраняем
    ДОКУМЕНТ — список фигур, из которого Canvas и так строится через
    <code class="inline">render_document()</code> (раздел 18.29):</p>
    {pipeline_diagram([
        {"kind": "object", "title": "document: list[Shape]"},
        {"kind": "plain", "title": "save_document()"},
        {"kind": "object", "title": "JSON-файл на диске"},
    ], caption="Сохранение.")}
    {pipeline_diagram([
        {"kind": "object", "title": "JSON-файл на диске"},
        {"kind": "plain", "title": "load_document()"},
        {"kind": "object", "title": "document: list[Shape]"},
        {"kind": "plain", "title": "render_document()"},
        {"kind": "object", "title": "Canvas"},
    ], caption="Загрузка — обязательно заканчивается перерисовкой, а не просто чтением файла.")}
    {code_block(
        "drawing.json",
        "{\n"
        '  "version": 1,\n'
        '  "canvas": {"background": "#ffffff"},\n'
        '  "items": [\n'
        "    {\n"
        '      "kind": "line",\n'
        '      "coords": [34, 52, 180, 90],\n'
        '      "color": "#2563eb",\n'
        '      "width": 4\n'
        "    },\n"
        "    {\n"
        '      "kind": "rectangle",\n'
        '      "coords": [80, 120, 220, 210],\n'
        '      "color": "#dc2626",\n'
        '      "width": 3\n'
        "    }\n"
        "  ]\n"
        "}\n",
        lang="json",
    )}
    {code_block(
        "sohranenie_json.py",
        "def save_document(self):\n"
        "    path_str = filedialog.asksaveasfilename(\n"
        '        defaultextension=".json", filetypes=[("Рисунок JSON", "*.json")]\n'
        "    )\n"
        '    if not path_str:  # пользователь нажал "Отмена" — path_str == ""\n'
        "        return\n"
        "    data = {\n"
        '        "version": 1,\n'
        '        "canvas": {"background": CANVAS_BG},\n'
        '        "items": [shape.to_dict() for shape in self.document],\n'
        "    }\n"
        "    Path(path_str).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding=\"utf-8\")\n",
    )}
    {image_figure(f"{IMG}/saved-document.png", "Реальное окно: рисунок с несколькими фигурами непосредственно перед сохранением", "Реальное окно: рисунок перед Ctrl+S — этот же документ окажется в JSON-файле.", width=420)}
    {image_figure(f"{IMG}/loaded-document.png", "Реальное окно: тот же самый рисунок, восстановленный после загрузки JSON в новом сеансе", "Реальное окно: тот же рисунок после Ctrl+O в другом запуске программы — восстановлен из JSON, а не из памяти прежнего процесса.", width=420)}
    {callout(
        "warning",
        "Отмена диалога — не ошибка, а нормальный путь",
        "И <code class=\"inline\">asksaveasfilename()</code>, и "
        "<code class=\"inline\">askopenfilename()</code> возвращают пустую строку "
        "<code class=\"inline\">\"\"</code>, если пользователь нажал «Отмена» — не "
        "<code class=\"inline\">None</code> и не бросают исключение. Код обязан проверить это "
        "ДО того, как передавать путь в <code class=\"inline\">Path(...)</code>: "
        "<code class=\"inline\">Path(\"\")</code> — валидный, но бессмысленный объект, "
        "указывающий на текущую директорию, а не на файл, который выбрал пользователь.",
    )}

    {local_required_card(
        "18-30",
        "Практика: сохранение и загрузка рисунка в JSON",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-30/index.html",
    )}
    """
    out = render_page(
        page_title="Сохранение и загрузка JSON",
        description="Документ рисунка сохраняется и загружается как JSON — Canvas не экспортирует себя в PNG напрямую.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Сохранение и загрузка", "")],
        kicker="Глава 18 · Финальные штрихи",
        h1="Сохранение и загрузка JSON",
        lede="Сохраняется не картинка, а документ фигур — Canvas умеет заново построить из него "
        "холст в любой момент.",
        body_html=body,
        sidebar_groups=sidebar("18-30-sohranenie-json.html"),
        nav=PageNav(prev_href="18-29-arhitektura-paintapp.html", prev_label="Архитектура PaintApp", next_href="18-31-debug-labs.html", next_label="Debug Labs"),
    )
    write("18-30-sohranenie-json.html", out)


def build_31() -> None:
    body = f"""
    <p>Небольшая коллекция типичных ошибок рисовалок на Canvas — каждая с симптомом и
    исправлением. Часть из них вы уже видели раньше в главе; здесь они собраны как справочник.</p>

    {debug_lab(
        1,
        "Y растёт вверх, как у Turtle",
        "turtle_privychka.py",
        "def on_drag(event):\n"
        "    # 'привычная' логика: чем выше на экране, тем БОЛЬШЕ Y\n"
        "    if event.y > start_y:\n"
        '        status.config(text="Двигаемся ВВЕРХ")  # неверно для Canvas!\n',
        ["# Курсор двигается вниз по экрану, а статус говорит 'ВВЕРХ' —", "# логика была написана в терминах Turtle, а не Canvas."],
        "У Canvas Y растёт ВНИЗ (раздел 18.9) — <code class=\"inline\">event.y &gt; start_y</code> "
        "означает «курсор ниже, чем был», а не выше. Перенос интуиции с Turtle без пересчёта "
        "знака — частая ошибка именно у тех, кто уже уверенно рисовал Turtle в главах 6–7.",
        "canvas_napravlenie.py",
        "def on_drag(event):\n"
        "    if event.y > start_y:\n"
        '        status.config(text="Двигаемся ВНИЗ")  # верно: Y растёт вниз\n',
    )}

    {debug_lab(
        2,
        "Не запомнили точку начала жеста",
        "zabyli_start.py",
        "def on_press(event):\n"
        "    pass  # забыли сохранить event.x, event.y\n\n"
        "def on_drag(event):\n"
        "    canvas.create_line(start_x, start_y, event.x, event.y)  # start_x не определена\n",
        ["# NameError: name 'start_x' is not defined —", "# программа падает на первом же движении мыши после нажатия."],
        "<code class=\"inline\">on_press()</code> обязан сохранить точку начала (раздел 18.12) — "
        "без неё <code class=\"inline\">on_drag()</code> просто не может знать, откуда рисовать "
        "линию или превью фигуры.",
        "sohranili_start.py",
        "def on_press(event):\n"
        "    global start_x, start_y\n"
        "    start_x, start_y = event.x, event.y\n",
    )}

    {debug_lab(
        3,
        "&lt;Motion&gt; вместо &lt;B1-Motion&gt;",
        "lyuboe_dvizhenie.py",
        'canvas.bind("<Motion>", on_drag)   # сработает при ЛЮБОМ движении мыши\n',
        ["# Линия рисуется, даже если кнопка мыши вообще не нажата —", "# достаточно просто провести курсором над холстом."],
        "<code class=\"inline\">&lt;Motion&gt;</code> реагирует на любое движение мыши над "
        "виджетом. Для рисования только во время перетаскивания нужен именно "
        "<code class=\"inline\">&lt;B1-Motion&gt;</code> — раздел 18.12 объясняет разницу.",
        "b1_motion.py",
        'canvas.bind("<B1-Motion>", on_drag)   # только при зажатой левой кнопке\n',
    )}

    {debug_lab(
        4,
        "Тысячи несвязанных точек вместо линии",
        "tochki_vmesto_linii.py",
        "def on_drag(event):\n"
        "    canvas.create_oval(\n"
        "        event.x - 2, event.y - 2, event.x + 2, event.y + 2,\n"
        "        fill=\"black\",\n"
        "    )\n",
        ["# Быстрое движение мыши оставляет заметные разрывы между кружками —", "# штрих выглядит рваным, а не гладким."],
        "Кружок на каждое отдельное событие не учитывает путь МЕЖДУ двумя последовательными "
        "точками. Раздел 18.14 показывает решение — соединять новую точку с предыдущей через "
        "<code class=\"inline\">create_line()</code>.",
        "linii_mezhdu_tochkami.py",
        "def on_drag(event):\n"
        "    canvas.create_line(last_x, last_y, event.x, event.y, width=3, capstyle=tk.ROUND)\n"
        "    # last_x, last_y обновляются после каждого отрезка\n",
    )}

    {debug_lab(
        5,
        "Превью пересоздаётся на каждый Motion без необходимости",
        "peresozdanie_prevyu.py",
        "def on_drag(event):\n"
        "    canvas.delete(preview_id)\n"
        "    preview_id = canvas.create_rectangle(start_x, start_y, event.x, event.y)\n",
        ["# Работает, но на каждое из десятков событий Motion в секунду", "# Canvas выбрасывает и заново строит один и тот же элемент."],
        "Удалить и создать заново — не ошибка в смысле «сломано», но лишняя работа: у Canvas уже "
        "есть <code class=\"inline\">coords()</code> именно для обновления существующего "
        "элемента (раздел 18.18) — без пересоздания.",
        "coords_vmesto_peresozdaniya.py",
        "def on_drag(event):\n"
        "    canvas.coords(preview_id, start_x, start_y, event.x, event.y)\n",
    )}

    {debug_lab(
        6,
        "Потеряли id превью-фигуры",
        "poteryan_id.py",
        "def on_press(event):\n"
        "    canvas.create_rectangle(event.x, event.y, event.x, event.y, dash=(4, 2))\n"
        "    # id не сохранён — preview_id нигде не появился\n\n"
        "def on_drag(event):\n"
        "    canvas.coords(preview_id, ...)  # NameError: preview_id не определена\n",
        ["# NameError на первом же движении мыши —", "# ссылаться не на что, id черновой фигуры потерян."],
        "<code class=\"inline\">create_*()</code> возвращает <code class=\"inline\">item_id</code> "
        "(раздел 18.10), но только если его СОХРАНИТЬ — иначе фигура нарисуется, но обратиться к "
        "ней позже будет нечем.",
        "sohranili_id.py",
        "def on_press(event):\n"
        "    global preview_id\n"
        "    preview_id = canvas.create_rectangle(event.x, event.y, event.x, event.y, dash=(4, 2))\n",
    )}

    {debug_lab(
        7,
        "Прямоугольник «переворачивается» при перетаскивании вверх-влево",
        "ne_normalizovano.py",
        "def get_bounds():\n"
        "    return start_x, start_y, current_x, current_y  # без учёта направления\n\n"
        "left, top, right, bottom = get_bounds()\n"
        "if left > right:\n"
        '    raise ValueError("это невозможно")  # но перетаскивание вверх-влево именно это и даёт!\n',
        ["# Приложение падает с ValueError, если пользователь начал", "# перетаскивание из правого нижнего угла будущей фигуры."],
        "Мышь можно тянуть в любую из четырёх сторон (раздел 18.16) — код, ожидающий "
        "<code class=\"inline\">left &lt;= right</code> без предварительной нормализации, "
        "работает только для одного из четырёх направлений.",
        "normalizovano.py",
        "left, top, right, bottom = normalize_bounds(start_x, start_y, current_x, current_y)\n"
        "# теперь left <= right и top <= bottom гарантированно, независимо от направления\n",
    )}

    {debug_lab(
        8,
        "item_id использован как индекс списка",
        "id_kak_indeks.py",
        "shapes = []\n"
        "item_id = canvas.create_rectangle(10, 10, 50, 50)\n"
        "shapes.append(\"rectangle\")\n"
        "print(shapes[item_id])   # IndexError, если item_id больше len(shapes) - 1\n",
        ["# IndexError: list index out of range —", "# item_id не совпадает с порядковым номером в собственном списке кода."],
        "<code class=\"inline\">item_id</code> — внутренний номер Canvas (раздел 18.10), а не "
        "позиция в вашем собственном списке фигур. Использовать его как индекс "
        "<code class=\"inline\">shapes[item_id]</code> совпадёт только случайно.",
        "id_kak_klyuch_slovarya.py",
        "shapes_by_id = {}\n"
        "item_id = canvas.create_rectangle(10, 10, 50, 50)\n"
        'shapes_by_id[item_id] = "rectangle"   # словарь — id как КЛЮЧ, а не индекс\n',
    )}

    {debug_lab(
        9,
        "Ластик стирает половину штриха, а не весь",
        "chastichnaya_otmena.py",
        "def undo(self):\n"
        "    item_id = self.undo_stack.pop()   # предполагает ОДИН id на действие\n"
        "    self.canvas.delete(item_id)\n",
        ["# После Ctrl+Z длинный карандашный штрих теряет только", "# последний маленький отрезок, а не исчезает целиком."],
        "Один карандашный штрих — это МНОГО отрезков <code class=\"inline\">create_line()</code> "
        "(раздел 18.14), а не один элемент. Undo обязан хранить список id (или фигур) на КАЖДОЕ "
        "действие целиком, а не один id (раздел 18.24).",
        "otmena_celym_deystviem.py",
        "def undo(self):\n"
        "    shapes = self.undo_stack.pop()   # список фигур ОДНОГО действия\n"
        "    del self.document[len(self.document) - len(shapes):]\n"
        "    self.render_document()\n",
    )}

    {debug_lab(
        10,
        "Redo воскрешает несвязанное действие",
        "redo_bez_ochistki.py",
        "def _commit_action(self, shapes):\n"
        "    self.document.extend(shapes)\n"
        "    self.undo_stack.append(shapes)\n"
        "    # забыли self.redo_stack.clear()\n",
        ["# Undo, затем новый рисунок, затем Redo —", "# и на холсте внезапно появляется фигура, никак не связанная с текущим рисунком."],
        "Если после Undo нарисовать что-то новое, старая ветка redo больше не соответствует "
        "текущему документу. Раздел 18.25 требует явно очищать "
        "<code class=\"inline\">redo_stack</code> при любом новом действии.",
        "redo_s_ochistkoj.py",
        "def _commit_action(self, shapes):\n"
        "    self.document.extend(shapes)\n"
        "    self.undo_stack.append(shapes)\n"
        "    self.redo_stack.clear()\n",
    )}

    {debug_lab(
        11,
        "Очистили холст, но не историю",
        "ochistka_bez_istorii.py",
        "def clear_canvas(self):\n"
        '    self.canvas.delete("all")\n'
        "    self.document.clear()\n"
        "    # undo_stack и redo_stack не тронуты!\n",
        ["# После 'Очистить' нажатие Ctrl+Z пытается убрать фигуры", "# из уже пустого документа — список становится отрицательной длины."],
        "История описывает документ, которого больше нет — как только "
        "<code class=\"inline\">document</code> очищается, <code class=\"inline\">undo_stack</code> "
        "и <code class=\"inline\">redo_stack</code> обязаны очиститься вместе с ним (раздел 18.26).",
        "ochistka_s_istoriej.py",
        "def clear_canvas(self):\n"
        "    self.document.clear()\n"
        "    self.undo_stack.clear()\n"
        "    self.redo_stack.clear()\n"
        "    self.render_document()\n",
    )}

    {debug_lab(
        12,
        "Отмена colorchooser записывает None как цвет",
        "otmena_colorchooser.py",
        "def choose_custom_color(self):\n"
        "    _rgb, hex_color = colorchooser.askcolor()\n"
        "    self.set_color(hex_color)   # не проверили hex_color на None!\n",
        ["# Пользователь нажал 'Отмена' в диалоге —", "# следующая же попытка нарисовать линию падает: fill=None недопустим."],
        "<code class=\"inline\">askcolor()</code> возвращает <code class=\"inline\">(None, None)</code> "
        "при отмене (раздел 18.21) — присвоить это как текущий цвет без проверки значит "
        "сломать рисование при следующей же попытке.",
        "proverka_otmeny.py",
        "def choose_custom_color(self):\n"
        "    _rgb, hex_color = colorchooser.askcolor()\n"
        "    if hex_color is not None:\n"
        "        self.set_color(hex_color)\n",
    )}

    {debug_lab(
        13,
        "Отмена диалога сохранения — Path('') вместо выхода",
        "otmena_sohraneniya.py",
        "def save_document(self):\n"
        "    path_str = filedialog.asksaveasfilename()\n"
        "    Path(path_str).write_text(...)   # не проверили пустую строку!\n",
        ["# Пользователь нажал 'Отмена' в диалоге сохранения —", "# программа пытается записать файл по пути текущей директории."],
        "<code class=\"inline\">asksaveasfilename()</code>/<code class=\"inline\">askopenfilename()</code> "
        "возвращают пустую строку при отмене, а не <code class=\"inline\">None</code> и не "
        "исключение (раздел 18.30) — код обязан проверить это перед использованием пути.",
        "proverka_otmeny_faila.py",
        "def save_document(self):\n"
        "    path_str = filedialog.asksaveasfilename()\n"
        "    if not path_str:\n"
        "        return\n"
        "    Path(path_str).write_text(...)\n",
    )}

    {debug_lab(
        14,
        "JSON загружен, но Canvas не перерисован",
        "zagruzka_bez_render.py",
        "def load_from_path(self, path):\n"
        "    data = json.loads(path.read_text(encoding=\"utf-8\"))\n"
        "    self.document = [Shape.from_dict(item) for item in data[\"items\"]]\n"
        "    # забыли self.render_document()!\n",
        ["# self.document правильно заполнен новыми фигурами,", "# но на экране всё ещё виден старый рисунок — или пустой холст."],
        "Как и в главе 17: изменение модели без вызова отрисовки не долетает до экрана. "
        "<code class=\"inline\">load_from_path()</code> обязан заканчиваться "
        "<code class=\"inline\">render_document()</code> (раздел 18.30).",
        "zagruzka_s_render.py",
        "def load_from_path(self, path):\n"
        "    data = json.loads(path.read_text(encoding=\"utf-8\"))\n"
        "    self.document = [Shape.from_dict(item) for item in data[\"items\"]]\n"
        "    self.undo_stack.clear()\n"
        "    self.redo_stack.clear()\n"
        "    self.render_document()\n",
    )}

    {image_figure(f"{IMG}/resized-window.png", "Реальное окно: то же приложение в увеличенном виде — холст занимает больше места, но ранее нарисованные фигуры остались того же размера в тех же абсолютных координатах", "Реальное окно после увеличения: холст стал больше, но нарисованные фигуры не выросли вместе с ним — именно то, что показывает Debug Lab 15 ниже.", width=460)}

    {debug_lab(
        15,
        "Изменение размера окна не масштабирует рисунок",
        "resize_kak_masshtab.py",
        "# ожидание: если растянуть окно, старые фигуры увеличатся вместе с ним\n"
        "canvas.grid(row=1, column=0, sticky=\"nsew\")\n"
        "# ...но существующие create_line/rectangle/oval координаты никто не пересчитывает\n",
        ["# Сам виджет Canvas становится больше вместе с окном —", "# но уже нарисованные фигуры остаются в прежних абсолютных координатах, не растут."],
        "<code class=\"inline\">sticky=\"nsew\"</code> и веса строк/столбцов (глава 17) заставляют "
        "РАСТИ сам виджет Canvas — это не то же самое, что автоматическое масштабирование "
        "координат уже нарисованных фигур. Раздел 18.29 явно разбирает это различие: увеличенный "
        "холст не означает автоматически увеличенный рисунок.",
        "resize_kak_bolshe_mesta.py",
        "# Честная модель: увеличенное окно даёт БОЛЬШЕ МЕСТА для новых фигур,\n"
        "# а не растягивает уже существующие — если нужно последнее, координаты\n"
        "# пришлось бы пересчитывать вручную при изменении размера.\n",
    )}

    {practice_card(
        "18-31",
        "Практика: находим баг рисовалки по симптому",
        "Автоматическая проверка — для набора описанных симптомов выбираем правильную причину/исправление",
        "../../practice/18-31/index.html",
    )}
    """
    out = render_page(
        page_title="Debug Labs — типичные ошибки рисовалки",
        description="Пятнадцать разобранных багов приложения для рисования на Canvas: координаты, превью, undo/redo, диалоги, JSON.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Debug Labs", "")],
        kicker="Глава 18 · Тестирование",
        h1="Debug Labs — типичные ошибки рисовалки",
        lede="Каждая ошибка здесь встречается в реальных студенческих проектах — научитесь "
        "узнавать симптом раньше, чем откроете отладчик.",
        body_html=body,
        sidebar_groups=sidebar("18-31-debug-labs.html"),
        nav=PageNav(prev_href="18-30-sohranenie-json.html", prev_label="Сохранение и загрузка", next_href="18-32-paint-pro-itogi.html", next_label="Paint Pro — итоги главы"),
    )
    write("18-31-debug-labs.html", out)


def build_32() -> None:
    checklist_model = "".join(f"<li>{x}</li>" for x in [
        "документ (<code class=\"inline\">document</code>) — список фигур, источник истины",
        "DrawingState — параметры инструмента, отдельно от самих фигур",
        "Canvas — только отображение, перерисовывается из документа",
    ])
    checklist_tools = "".join(f"<li>{x}</li>" for x in [
        "карандаш непрерывным штрихом",
        "линия, прямоугольник, овал с живым превью",
        "ластик как штрих цветом фона",
        "выбор инструмента виден на экране, не только в памяти",
    ])
    checklist_history = "".join(f"<li>{x}</li>" for x in [
        "undo/redo по действиям, а не по отдельным элементам Canvas",
        "новое действие очищает redo_stack",
        "очистка холста обнуляет историю вместе с документом",
    ])
    checklist_persistence = "".join(f"<li>{x}</li>" for x in [
        "сохранение и загрузка рисунка через JSON",
        "отмена диалогов сохранения/открытия/выбора цвета обработана честно",
        "строка состояния и горячие клавиши",
    ])
    body = f"""
    <h2>Итоговая программа</h2>
    {image_figure(f"{IMG}/paint-pro-final.png", "Финальное окно Paint Pro с несколькими нарисованными фигурами, панелью инструментов, палитрой, ползунком толщины и строкой состояния", "Реальное окно финальной версии — та же картинка, что открывала главу в разделе 18.1, но теперь мы знаем, из чего она построена.", width=760)}
    <p>Файл целиком, самодостаточный и без невидимых зависимостей от других уроков:</p>
    <p>[[icon:file]] <a href="../../../projects/tkinter/paint-app/paint_app.py">projects/tkinter/paint-app/paint_app.py</a></p>
    {code_block(
        "paint_app.py — структура",
        "class Tool(Enum): ...\n\n"
        "@dataclass\n"
        "class Shape: ...\n\n"
        "@dataclass\n"
        "class DrawingState: ...\n\n"
        "def normalize_bounds(x1, y1, x2, y2): ...\n\n"
        "class PaintApp:\n"
        "    def __init__(self, root): ...\n"
        "    def build_ui(self): ...\n"
        "    def set_tool(self, tool): ...\n"
        "    def set_color(self, hex_color): ...\n"
        "    def choose_custom_color(self): ...\n"
        "    def set_width(self, value): ...\n"
        "    def on_press(self, event): ...\n"
        "    def on_drag(self, event): ...\n"
        "    def on_release(self, event): ...\n"
        "    def render_document(self): ...\n"
        "    def undo(self): ...\n"
        "    def redo(self): ...\n"
        "    def clear_canvas(self): ...\n"
        "    def save_document(self): ...\n"
        "    def load_document(self): ...\n\n"
        "def main():\n"
        "    root = tk.Tk()\n"
        "    app = PaintApp(root)\n"
        "    root.mainloop()\n\n"
        'if __name__ == "__main__":\n'
        "    main()\n",
    )}
    {callout(
        "tip",
        "Запустите приложение у себя",
        "<code class=\"inline\">python paint_app.py</code> в терминале — либо кнопкой Run в VS "
        "Code или PyCharm. Сравните с <code class=\"inline\">paint_app_basic.py</code> (раздел "
        "18.7) — тот же холст и та же идея, но совершенно другая внутренняя архитектура.",
    )}

    <h2>Чек-лист готового приложения</h2>
    <div class="capability-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin:24px 0">
      <div style="background:var(--color-bg-canvas,#fff);border:1.5px solid var(--color-border-default,#E4E1F5);border-radius:16px;padding:16px 18px">
        <div style="font-family:Sora,sans-serif;font-weight:700;color:#5B24F9;margin-bottom:8px">МОДЕЛЬ</div>
        <ul style="margin:0;padding-left:18px;font-size:14px;line-height:1.6">{checklist_model}</ul>
      </div>
      <div style="background:var(--color-bg-canvas,#fff);border:1.5px solid var(--color-border-default,#E4E1F5);border-radius:16px;padding:16px 18px">
        <div style="font-family:Sora,sans-serif;font-weight:700;color:#5B24F9;margin-bottom:8px">ИНСТРУМЕНТЫ</div>
        <ul style="margin:0;padding-left:18px;font-size:14px;line-height:1.6">{checklist_tools}</ul>
      </div>
      <div style="background:var(--color-bg-canvas,#fff);border:1.5px solid var(--color-border-default,#E4E1F5);border-radius:16px;padding:16px 18px">
        <div style="font-family:Sora,sans-serif;font-weight:700;color:#5B24F9;margin-bottom:8px">ИСТОРИЯ</div>
        <ul style="margin:0;padding-left:18px;font-size:14px;line-height:1.6">{checklist_history}</ul>
      </div>
      <div style="background:var(--color-bg-canvas,#fff);border:1.5px solid var(--color-border-default,#E4E1F5);border-radius:16px;padding:16px 18px">
        <div style="font-family:Sora,sans-serif;font-weight:700;color:#5B24F9;margin-bottom:8px">СОХРАНЕНИЕ</div>
        <ul style="margin:0;padding-left:18px;font-size:14px;line-height:1.6">{checklist_persistence}</ul>
      </div>
    </div>

    <h2 id="most-k-glave-19">Мост к главе 19</h2>
    {callout(
        "info",
        "Дальше: движение и повторение вместо ожидания клика",
        "Рисовалка целиком построена вокруг ожидания действий пользователя — программа "
        "реагирует, но сама не «живёт». В следующей главе — игра «Змейка» на Turtle — появится "
        "собственный игровой цикл, где программа сама двигает объекты кадр за кадром, "
        "независимо от того, нажимает ли пользователь что-то прямо сейчас.",
    )}

    {local_required_card(
        "18-32",
        "Практика: Paint Pro целиком",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/18-32/index.html",
    )}

    <h2 id="itogi-glavy">Итоги главы 18</h2>
    {summary_box("Что мы построили и чему научились", [
        "Canvas хранит элементы (items), а не пиксели — create_* добавляет запись в список, "
        "который помнит сам виджет, и возвращает её item_id.",
        "Координаты Canvas растут вправо и вниз от левого верхнего угла — не как у Turtle, где "
        "начало в центре, а Y растёт вверх.",
        "Рисование мышью — жест из трёх событий: press запоминает начало, drag обновляет "
        "черновик, release фиксирует результат.",
        "Живое превью — это ОДИН элемент, который создаётся один раз и обновляется через "
        "coords(), а не пересоздаётся на каждое движение.",
        "Прямоугольник и овал задаются двумя противоположными точками; овал вписан в "
        "получившийся прямоугольник, а не задан центром и радиусом.",
        "Undo/redo работают по логическим ДЕЙСТВИЯМ пользователя, а не по отдельным элементам "
        "Canvas — один карандашный штрих отменяется целиком.",
        "Документ (список фигур) — источник истины; Canvas каждый раз перерисовывается из него "
        "заново через render_document(), тот же принцип, что и render() в главе 17.",
        "Сохраняется не картинка, а документ — как JSON, который можно загрузить и "
        "перестроить заново в любой момент.",
    ])}
    """
    out = render_page(
        page_title="Paint Pro — полная программа и итоги главы",
        description="Финальная архитектура приложения для рисования целиком, чек-лист готового приложения, итоги главы 18 и мост к игровому циклу главы 19.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Paint Pro — итоги", "")],
        kicker="Глава 18 · Финальные штрихи",
        h1="Paint Pro — полная программа и итоги главы",
        lede="Тот же холст, что и в разделе 18.7 — но теперь с документом, историей отмены и "
        "архитектурой, которая выдержит рост проекта.",
        body_html=body,
        sidebar_groups=sidebar("18-32-paint-pro-itogi.html"),
        nav=PageNav(prev_href="18-31-debug-labs.html", prev_label="Debug Labs", next_href="../glava-19/index.html", next_label="Глава 19: Проект: игра «Змейка» с Turtle"),
    )
    write("18-32-paint-pro-itogi.html", out)


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
