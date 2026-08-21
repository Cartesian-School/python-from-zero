#!/usr/bin/env python3
"""Строит Главу 17: «Проект: игра «Крестики-нолики» с Tkinter» (site/chapters/glava-17/)."""

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
OUT_DIR = ROOT / "site" / "chapters" / "glava-17"
IMG = "../../assets/img/chapter-17/output"

PAGES = [
    ("index.html", "Обзор главы"),
    ("17-01-privyazka-sobytij.html", "Привязка событий"),
    ("17-02-obyasnenie-nastrojka.html", "Объяснение игры и настройка Tkinter"),
    ("17-03-peremennye-knopki.html", "Глобальные переменные и кнопки"),
    ("17-04-risuem-na-knopke.html", "При нажатии рисуем на кнопке"),
    ("17-05-proverka-pobedy.html", "Проверяем победу"),
    ("17-06-novaya-igra-itogi.html", "Новая игра и первая полная версия"),
    ("17-07-event-callback-command-binding.html", "Event, callback, command и binding"),
    ("17-08-obyekt-event.html", "Объект Event"),
    ("17-09-sintaksis-sobytij.html", "Синтаксис событий Tk"),
    ("17-10-command-vs-bind.html", "command vs bind — что выбирать"),
    ("17-11-focus-i-klaviatura.html", "Focus и клавиатура"),
    ("17-12-enter-leave-hover.html", "Mouse Enter/Leave и hover"),
    ("17-13-model-sostoyaniya.html", "Модель игрового состояния"),
    ("17-14-indeksy-stroki-stolbcy.html", "Индексы, строки и столбцы"),
    ("17-15-algoritm-hoda.html", "Правильный алгоритм хода"),
    ("17-16-vosem-linij-pobedy.html", "Восемь выигрышных линий"),
    ("17-17-pobeda-nichya-terminal.html", "Победа, ничья и terminal state"),
    ("17-18-model-a-ne-widgets.html", "От widgets-as-state к board model"),
    ("17-19-gamestate-dataclass.html", "GameState с dataclass"),
    ("17-20-arhitektura-app.html", "Архитектура TicTacToeApp"),
    ("17-21-adaptivnoe-pole.html", "Адаптивное игровое поле"),
    ("17-22-vizualnyj-stil.html", "Визуальный стиль X/O"),
    ("17-23-hover-preview.html", "Hover preview через bind()"),
    ("17-24-upravlenie-klaviaturoj.html", "Управление клавиатурой"),
    ("17-25-podsvetka-linii.html", "Подсветка выигрышной линии"),
    ("17-26-schyot-matchej.html", "Счёт матчей"),
    ("17-27-new-round-vs-new-match.html", "New Round vs New Match"),
    ("17-28-testiruem-bez-tkinter.html", "Тестируем игру без Tkinter"),
    ("17-29-debug-labs.html", "Debug Labs"),
    ("17-30-visual-effects-after.html", "Visual effects и after()"),
    ("17-31-tic-tac-toe-pro-itogi.html", "Tic-Tac-Toe Pro — итоги главы"),
]

LESSON_IDS = [
    "17-01", "17-03", "17-04", "17-05", "17-06",
    "17-07", "17-08", "17-09", "17-10", "17-11", "17-12", "17-13", "17-14",
    "17-15", "17-16", "17-17", "17-18", "17-19", "17-20", "17-21", "17-22",
    "17-23", "17-24", "17-25", "17-26", "17-27", "17-28", "17-29", "17-30", "17-31",
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 17 · Крестики-нолики", items),
        SidebarGroup("Практика", [
            NavItem(f"🐍 {lid}: Практика", f"../../practice/{lid}/index.html") for lid in LESSON_IDS
        ]),
        SidebarGroup("Исходный код", [
            NavItem("🐍 tic_tac_toe_basic.py — первый прототип (17.6)", "../../../projects/tkinter/tic-tac-toe/tic_tac_toe_basic.py"),
            NavItem("🐍 tic_tac_toe.py — финальная версия Pro (17.31)", "../../../projects/tkinter/tic-tac-toe/tic_tac_toe.py"),
        ]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    clean = "\n".join(line.rstrip() for line in html_out.split("\n"))
    path.write_text(clean, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


# ---------------------------------------------------------------------------
# Локальные помощники главы 17
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
    """Единый компонент Debug Lab (введён в главе 14, переиспользован в 15/16):
    сломанный код → что происходит на экране → объяснение → исправленный код."""
    return f"""
    <div style="margin:28px 0;padding:4px 4px 20px;border:2px dashed #DB2777;border-radius:var(--radius-lg,20px)">
      <div style="padding:14px 20px 4px;font-family:Sora,sans-serif;font-weight:700;font-size:13px;
        letter-spacing:.05em;text-transform:uppercase;color:#DB2777">🐞 Debug Lab {n}: {html.escape(title)}</div>
      <div style="padding:0 20px">
{code_block(broken_code_filename, broken_code)}
{terminal_transcript(symptom_lines, caption="Что видно на экране")}
        <p>{explanation_html}</p>
        <div style="font-family:Sora,sans-serif;font-weight:700;font-size:12px;letter-spacing:.05em;
          text-transform:uppercase;color:#059669;margin:16px 0 8px">Исправленный код</div>
{code_block(fixed_code_filename, fixed_code)}
      </div>
    </div>"""


_BOARD_MARK_COLOR = {"X": "#5B24F9", "O": "#DB2777"}


def board_diagram(cells: list[str], *, highlighted: tuple = (), indices: bool = False, caption: str = "") -> str:
    """3×3 HTML/CSS доска — переиспользуемый примитив главы 17 (раздел 107 брифа).
    cells: 9 строк ('', 'X', 'O' или произвольная метка, например индекс/'i').
    highlighted: индексы клеток победной линии (заливаются зелёным).
    indices: если True — в каждой клетке маленьким шрифтом показан её номер 0..8."""
    highlighted_set = set(highlighted)

    def cell_html(i: int, value: str) -> str:
        is_hl = i in highlighted_set
        mark_color = _BOARD_MARK_COLOR.get(value, "#0D0230")
        bg = "#D1FAE5" if is_hl else "#fff"
        border = "#059669" if is_hl else "#E4E1F5"
        index_html = (
            f'<div style="position:absolute;top:4px;left:7px;font-size:10px;color:#B9A0FC;'
            f'font-family:\'JetBrains Mono\',monospace">{i}</div>'
            if indices
            else ""
        )
        value_html = (
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-weight:700;font-size:26px;'
            f'color:{mark_color}">{html.escape(value)}</div>'
            if value
            else ""
        )
        return (
            f'<div style="position:relative;width:56px;height:56px;display:flex;align-items:center;'
            f'justify-content:center;background:{bg};border:1.5px solid {border};border-radius:10px">'
            f'{index_html}{value_html}</div>'
        )

    grid_html = "".join(cell_html(i, v) for i, v in enumerate(cells))
    cap = f'<figcaption style="text-align:center;font-size:13px;color:var(--ink-soft,#6B6B7D);margin-top:10px">{html.escape(caption)}</figcaption>' if caption else ""
    return (
        f'<figure style="margin:20px 0;padding:16px;background:var(--color-bg-surface,#FAFAFC);'
        f'border-radius:var(--radius-lg,20px);display:flex;flex-direction:column;align-items:center">'
        f'<div style="display:grid;grid-template-columns:repeat(3,56px);gap:4px">{grid_html}</div>{cap}</figure>'
    )


# ---------------------------------------------------------------------------
# Опener
# ---------------------------------------------------------------------------

def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=17,
        baseline_page=369,
        title="Проект: игра «Крестики-нолики» с Tkinter",
        description=(
            "Построим первую полноценную GUI-игру как настоящий небольшой программный проект: "
            "разберём систему событий Tkinter, отделим игровое состояние от виджетов, реализуем "
            "правила и тесты, добавим управление мышью и клавиатурой, визуальную обратную связь, "
            "счёт матчей и финальную архитектуру приложения."
        ),
        meta_items=["⏱ ~6–7 часов", "🎮 события · состояние · правила · архитектура", "📓 30 практик"],
        sections=[
            ChapterSectionLink("17.1", "Привязка событий — делаем приложения динамическими!", "17-01-privyazka-sobytij.html", "369"),
            ChapterSectionLink("17.2", "Игра «Крестики-нолики» — объяснение", "17-02-obyasnenie-nastrojka.html", "372"),
            ChapterSectionLink("", "Настраиваем Tkinter", "17-02-obyasnenie-nastrojka.html#nastrojka", "373"),
            ChapterSectionLink("17.3", "Создаём глобальные переменные", "17-03-peremennye-knopki.html", "374"),
            ChapterSectionLink("", "Создаём кнопки", "17-03-peremennye-knopki.html#knopki", "376"),
            ChapterSectionLink("17.4", "При нажатии на кнопку рисуем на ней", "17-04-risuem-na-knopke.html", "378"),
            ChapterSectionLink("17.5", "Проверяем после каждого хода, победил ли игрок", "17-05-proverka-pobedy.html", "383"),
            ChapterSectionLink("17.6", "Новая игра и первая полная версия", "17-06-novaya-igra-itogi.html", "385"),
            ChapterSectionLink("17.7", "Event, callback, command и binding", "17-07-event-callback-command-binding.html", "391"),
            ChapterSectionLink("17.8", "Объект Event", "17-08-obyekt-event.html", "393"),
            ChapterSectionLink("17.9", "Синтаксис событий Tk", "17-09-sintaksis-sobytij.html", "395"),
            ChapterSectionLink("17.10", "command vs bind — что выбирать", "17-10-command-vs-bind.html", "397"),
            ChapterSectionLink("17.11", "Focus и клавиатура", "17-11-focus-i-klaviatura.html", "399"),
            ChapterSectionLink("17.12", "Mouse Enter/Leave и hover", "17-12-enter-leave-hover.html", "401"),
            ChapterSectionLink("17.13", "Модель игрового состояния", "17-13-model-sostoyaniya.html", "403"),
            ChapterSectionLink("17.14", "Индексы, строки и столбцы", "17-14-indeksy-stroki-stolbcy.html", "405"),
            ChapterSectionLink("17.15", "Правильный алгоритм хода", "17-15-algoritm-hoda.html", "407"),
            ChapterSectionLink("17.16", "Восемь выигрышных линий", "17-16-vosem-linij-pobedy.html", "409"),
            ChapterSectionLink("17.17", "Победа, ничья и terminal state", "17-17-pobeda-nichya-terminal.html", "411"),
            ChapterSectionLink("17.18", "От widgets-as-state к board model", "17-18-model-a-ne-widgets.html", "413"),
            ChapterSectionLink("17.19", "GameState с dataclass", "17-19-gamestate-dataclass.html", "415"),
            ChapterSectionLink("17.20", "Архитектура TicTacToeApp", "17-20-arhitektura-app.html", "417"),
            ChapterSectionLink("17.21", "Адаптивное игровое поле", "17-21-adaptivnoe-pole.html", "419"),
            ChapterSectionLink("17.22", "Визуальный стиль X/O", "17-22-vizualnyj-stil.html", "421"),
            ChapterSectionLink("17.23", "Hover preview через bind()", "17-23-hover-preview.html", "423"),
            ChapterSectionLink("17.24", "Управление клавиатурой", "17-24-upravlenie-klaviaturoj.html", "425"),
            ChapterSectionLink("17.25", "Подсветка выигрышной линии", "17-25-podsvetka-linii.html", "427"),
            ChapterSectionLink("17.26", "Счёт матчей", "17-26-schyot-matchej.html", "429"),
            ChapterSectionLink("17.27", "New Round vs New Match", "17-27-new-round-vs-new-match.html", "431"),
            ChapterSectionLink("17.28", "Тестируем игру без Tkinter", "17-28-testiruem-bez-tkinter.html", "433"),
            ChapterSectionLink("17.29", "Debug Labs", "17-29-debug-labs.html", "435"),
            ChapterSectionLink("17.30", "Visual effects и after()", "17-30-visual-effects-after.html", "439"),
            ChapterSectionLink("17.31", "Tic-Tac-Toe Pro — итоги главы", "17-31-tic-tac-toe-pro-itogi.html", "441"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <p>В главе 16 кнопки реагировали на клик через параметр <code class="inline">command</code>
    — это самый частый, но не единственный способ связать код с действием пользователя.
    <strong>Привязка событий</strong> (<code class="inline">.bind()</code>) позволяет реагировать
    на что угодно: нажатие клавиши, движение мыши, наведение курсора.</p>
    {code_block(
        "privyazka_sobytij.py",
        "import tkinter as tk\n\n"
        "root = tk.Tk()\n"
        'label = tk.Label(root, text="Нажмите любую клавишу", font=("Arial", 14))\n'
        "label.pack(padx=20, pady=20)\n\n"
        "def na_klavishu(event):\n"
        '    label.config(text=f"Вы нажали: {event.keysym}")\n\n'
        'root.bind("<Key>", na_klavishu)\n'
        "root.mainloop()\n",
    )}
    <p>Функция-обработчик, переданная в <code class="inline">.bind()</code>, принимает один
    параметр — <code class="inline">event</code> — объект с подробностями о произошедшем событии:
    какая клавиша нажата (<code class="inline">event.keysym</code>), где кликнула мышь, и так
    далее. Это правило именно для <code class="inline">.bind()</code>: коллбэк, переданный в
    <code class="inline">command=</code> (как в главе 16), вызывается вообще БЕЗ аргументов —
    раздел 17.8 разберёт разницу подробнее.</p>

    {callout(
        "info",
        "Пригодится в главе 19",
        "Именно <code class=\"inline\">.bind()</code> позволит змейке в главе 19 реагировать "
        "на нажатия клавиш со стрелками — тот же самый приём, только с другим типом события.",
    )}

    {local_required_card(
        "17-01",
        "Практика: привязка событий клавиатуры",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/17-01/index.html",
    )}
    """
    out = render_page(
        page_title="Привязка событий — делаем приложения динамическими!",
        description="Метод bind() в Tkinter: реагируем на нажатия клавиш и другие события, а не только на клик по кнопке.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Привязка событий", "")],
        kicker="Глава 17 · Проект: «Крестики-нолики»",
        h1="Привязка событий — делаем приложения динамическими!",
        lede="command — не единственный способ реагировать на действия пользователя: bind() "
        "открывает события любого рода.",
        body_html=body,
        sidebar_groups=sidebar("17-01-privyazka-sobytij.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="17-02-obyasnenie-nastrojka.html", next_label="Объяснение игры и настройка"),
    )
    write("17-01-privyazka-sobytij.html", out)


def build_02() -> None:
    body = f"""
    <h2>Игра «Крестики-нолики» — объяснение</h2>
    <p>Правила знакомы почти всем: поле 3×3, два игрока по очереди ставят «X» и «O», первый,
    выстроивший три своих символа подряд — по горизонтали, вертикали или диагонали — побеждает.
    Соберём эту игру шаг за шагом — так, как её строил бы разработчик, а не одним куском кода
    сразу:</p>
    <ol>
      <li>Настроить окно;</li>
      <li>Создать переменные состояния игры;</li>
      <li>Создать поле из девяти кнопок;</li>
      <li>Реагировать на клик — рисовать X или O;</li>
      <li>Проверять после каждого хода, есть ли победитель;</li>
      <li>Добавить кнопку «Новая игра».</li>
    </ol>
    {image_figure(f"{IMG}/basic-empty-board.png", "Пустое окно с полем из девяти кнопок и статусом Ход игрока: X", "Забегая вперёд: примерно так будет выглядеть окно к концу раздела 17.6, после всех шести шагов. Дальше эта же страница пока не выполняет весь этот код — только настраивает окно (шаг 1).", width=260)}

    <h2 id="nastrojka">Настраиваем Tkinter</h2>
    {code_block(
        "nastrojka_okna.py",
        "import tkinter as tk\n\n"
        "root = tk.Tk()\n"
        'root.title("Крестики-нолики")\n',
    )}

    {local_required_card(
        "17-03",
        "Практика: начинаем собирать игру",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/17-03/index.html",
    )}
    """
    out = render_page(
        page_title="Игра «Крестики-нолики» — объяснение",
        description="План сборки игры «Крестики-нолики» по шагам и настройка главного окна Tkinter.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Объяснение и настройка", "")],
        kicker="Глава 17 · Проект: «Крестики-нолики»",
        h1="Игра «Крестики-нолики» — объяснение",
        lede="Разберём план из шести шагов, по которому мы соберём игру — от пустого окна до "
        "готовой программы.",
        body_html=body,
        sidebar_groups=sidebar("17-02-obyasnenie-nastrojka.html"),
        nav=PageNav(prev_href="17-01-privyazka-sobytij.html", prev_label="Привязка событий", next_href="17-03-peremennye-knopki.html", next_label="Переменные и кнопки"),
    )
    write("17-02-obyasnenie-nastrojka.html", out)


def build_03() -> None:
    body = f"""
    <h2>Создаём глобальные переменные</h2>
    <p>Игре нужно помнить своё состояние между ходами — чей сейчас ход, закончена ли игра, и
    сами кнопки поля, чтобы менять их текст:</p>
    {code_block(
        "globalnye_peremennye.py",
        'tekuschij_igrok = "X"\n'
        "polya = []             # список из 9 кнопок поля\n"
        "igra_okonchena = False\n",
    )}

    <h2 id="knopki">Создаём кнопки</h2>
    <p>Поле 3×3 — это девять кнопок, расположенных через <code class="inline">grid()</code>
    (глава 16). Создадим их циклом, а не девятью одинаковыми строками кода вручную (глава 10):</p>
    {code_block(
        "sozdaem_knopki.py",
        "pole_frame = tk.Frame(root)\n"
        "pole_frame.grid(row=1, column=0, columnspan=3)\n\n"
        "for indeks in range(9):\n"
        "    knopka = tk.Button(\n"
        "        pole_frame,\n"
        '        text="",\n'
        '        font=("Arial", 24, "bold"),\n'
        "        width=3, height=1,\n"
        "    )\n"
        "    knopka.grid(row=indeks // 3, column=indeks % 3)\n"
        "    polya.append(knopka)\n",
    )}
    {callout(
        "info",
        "indeks // 3 и indeks % 3 — координаты из номера",
        "Числа от 0 до 8 нужно превратить в строку и столбец таблицы 3×3. Целочисленное "
        "деление <code class=\"inline\">//</code> (глава 5) даёт номер строки "
        "(<code class=\"inline\">0,0,0,1,1,1,2,2,2</code>), а остаток <code class=\"inline\">%</code> "
        "— номер столбца (<code class=\"inline\">0,1,2,0,1,2,0,1,2</code>).",
    )}
    {image_figure(f"{IMG}/basic-empty-board.png", "Девять пустых кнопок в сетке 3×3 и статус Ход игрока: X", "Реальное окно полного файла прототипа: девять пустых кнопок, расставленных этим циклом.", width=260)}

    {local_required_card(
        "17-03",
        "Практика: переменные состояния и поле из кнопок",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/17-03/index.html",
    )}
    """
    out = render_page(
        page_title="Создаём глобальные переменные и кнопки",
        description="Переменные состояния игры и создание поля 3x3 из кнопок циклом.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Переменные и кнопки", "")],
        kicker="Глава 17 · Проект: «Крестики-нолики»",
        h1="Создаём глобальные переменные",
        lede="Игре нужна память между ходами — заведём переменные состояния и построим поле "
        "из кнопок циклом.",
        body_html=body,
        sidebar_groups=sidebar("17-03-peremennye-knopki.html"),
        nav=PageNav(prev_href="17-02-obyasnenie-nastrojka.html", prev_label="Объяснение и настройка", next_href="17-04-risuem-na-knopke.html", next_label="Рисуем на кнопке"),
    )
    write("17-03-peremennye-knopki.html", out)


def build_04() -> None:
    body = f"""
    <p>Каждой кнопке нужна своя функция-обработчик клика, которая знает <em>какая именно</em>
    кнопка нажата. Хитрость в том, чтобы связать <code class="inline">command</code> с номером
    кнопки — для этого используем лямбда-функцию из главы 13:</p>
    {code_block(
        "risuem_na_knopke.py",
        "def na_knopku_nazhali(indeks):\n"
        "    global tekuschij_igrok\n\n"
        '    if polya[indeks]["text"] != "":\n'
        "        return   # клетка уже занята\n\n"
        "    polya[indeks][\"text\"] = tekuschij_igrok\n"
        '    tekuschij_igrok = "O" if tekuschij_igrok == "X" else "X"\n\n'
        "# при создании каждой кнопки:\n"
        "knopka.config(command=lambda i=indeks: na_knopku_nazhali(i))\n",
    )}
    {callout(
        "warning",
        "Зачем lambda i=indeks, а не просто lambda: na_knopku_nazhali(indeks)?",
        "Без <code class=\"inline\">i=indeks</code> все девять кнопок запомнили бы одну и ту "
        "же переменную <code class=\"inline\">indeks</code> — а не её значение в момент "
        "создания. К моменту клика цикл давно завершится, и <code class=\"inline\">indeks</code> "
        "будет равен 8 для всех кнопок сразу. Значение по умолчанию "
        "<code class=\"inline\">i=indeks</code> «замораживает» текущее значение при создании "
        "каждой лямбды — классическая и важная тонкость Python.",
    )}
    {image_figure(f"{IMG}/basic-first-move.png", "На кнопке клетки 0 появилась X, статус сменился на Ход игрока: O", "Реальное окно полного файла прототипа: клик по первой клетке — на ней нарисован X, ход перешёл к O.", width=260)}

    {local_required_card(
        "17-04",
        "Практика: обработка клика по клетке поля",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/17-04/index.html",
    )}
    """
    out = render_page(
        page_title="При нажатии на кнопку рисуем на ней",
        description="Обработка клика по клетке игрового поля и важная тонкость с lambda в цикле.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Рисуем на кнопке", "")],
        kicker="Глава 17 · Проект: «Крестики-нолики»",
        h1="При нажатии на кнопку рисуем на ней",
        lede="Каждая кнопка должна знать свой номер — здесь прячется одна из самых известных "
        "тонкостей Python.",
        body_html=body,
        sidebar_groups=sidebar("17-04-risuem-na-knopke.html"),
        nav=PageNav(prev_href="17-03-peremennye-knopki.html", prev_label="Переменные и кнопки", next_href="17-05-proverka-pobedy.html", next_label="Проверяем победу"),
    )
    write("17-04-risuem-na-knopke.html", out)


def build_05() -> None:
    body = f"""
    <p>После каждого хода нужно проверить: не выстроились ли три одинаковых символа подряд.
    Всего в игре восемь возможных «выигрышных линий» — три строки, три столбца и две
    диагонали:</p>
    {code_block(
        "proverka_pobedy.py",
        "def proverit_pobedu():\n"
        "    linii_pobedy = [\n"
        "        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # строки\n"
        "        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # столбцы\n"
        "        (0, 4, 8), (2, 4, 6),             # диагонали\n"
        "    ]\n"
        "    for a, b, c in linii_pobedy:\n"
        '        znacheniya = (polya[a]["text"], polya[b]["text"], polya[c]["text"])\n'
        '        if znacheniya[0] != "" and znacheniya[0] == znacheniya[1] == znacheniya[2]:\n'
        "            return znacheniya[0]   # 'X' или 'O' — есть победитель\n"
        "    return None   # победителя пока нет\n",
    )}
    {callout(
        "tip",
        "Список кортежей — компактный способ описать 8 линий",
        "Каждая линия — кортеж (глава 11) из трёх индексов поля. Список из восьми таких "
        "кортежей заменяет восемь отдельных проверок <code class=\"inline\">if</code>, которые "
        "пришлось бы писать вручную.",
    )}
    {image_figure(f"{IMG}/basic-win.png", "Верхняя строка занята X, статус говорит Победил игрок X!", "Реальное окно полного файла прототипа: X собрал верхнюю строку — proverit_pobedu() нашла победителя.", width=260)}

    <h2>Ничья</h2>
    <p>Если все девять клеток заполнены, а победителя нет — это ничья:</p>
    {code_block(
        "proverka_nichyej.py",
        "def polye_zapolneno():\n"
        '    return all(knopka["text"] != "" for knopka in polya)\n',
    )}
    {image_figure(f"{IMG}/basic-draw.png", "Поле полностью заполнено X и O без выигрышной линии, статус говорит Ничья!", "Реальное окно полного файла прототипа: все девять клеток заняты, но выигрышной линии нет.", width=260)}

    {practice_card(
        "17-05",
        "Практика: проверка победы и ничьей",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/17-05/index.html",
    )}
    """
    out = render_page(
        page_title="Проверяем после каждого хода, победил ли игрок",
        description="Проверка восьми выигрышных линий и определение ничьей в крестиках-ноликах.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Проверка победы", "")],
        kicker="Глава 17 · Проект: «Крестики-нолики»",
        h1="Проверяем после каждого хода, победил ли игрок",
        lede="Восемь возможных выигрышных линий — три строки, три столбца, две диагонали.",
        body_html=body,
        sidebar_groups=sidebar("17-05-proverka-pobedy.html"),
        nav=PageNav(prev_href="17-04-risuem-na-knopke.html", prev_label="Рисуем на кнопке", next_href="17-06-novaya-igra-itogi.html", next_label="Новая игра и первая полная версия"),
    )
    write("17-05-proverka-pobedy.html", out)


def build_06() -> None:
    body = f"""
    <h2>Кнопка новой игры</h2>
    <p>Чтобы не перезапускать программу заново после каждой партии, добавим кнопку сброса —
    она возвращает все переменные и все клетки в начальное состояние:</p>
    {code_block(
        "novaya_igra.py",
        "def novaya_igra():\n"
        "    global tekuschij_igrok, igra_okonchena\n"
        '    tekuschij_igrok = "X"\n'
        "    igra_okonchena = False\n"
        "    for knopka in polya:\n"
        '        knopka.config(text="")\n',
    )}
    {image_figure(f"{IMG}/basic-new-game-reset.png", "Поле снова пустое, статус Ход игрока: X, после победы X в предыдущей партии", "Реальное окно полного файла прототипа: нажата «Новая игра» после победы X — поле и статус сброшены.", width=260)}

    <h2 id="polnaya-programma">Полная программа</h2>
    <p>Соберём все части в одну программу — она уже полностью проверена и доступна отдельным
    файлом в этой книге:</p>
    <p>📄 <a href="../../../projects/tkinter/tic-tac-toe/tic_tac_toe_basic.py">projects/tkinter/tic-tac-toe/tic_tac_toe_basic.py</a></p>
    {callout(
        "tip",
        "Запустите игру у себя",
        "Скачайте файл и запустите его через <code class=\"inline\">python tic_tac_toe_basic.py</code> "
        "в терминале (глава 3) — либо кнопкой Run в VS Code или PyCharm.",
    )}
    {callout(
        "info",
        "Это ПЕРВЫЙ рабочий прототип, не финал главы",
        "Мы построили настоящую играющую программу — с ходами, победой, ничьей и сбросом. Это "
        "честная, полная маленькая игра. Но начиная со следующего раздела мы будем смотреть на "
        "неё внимательнее: откуда узнаёт callback, что его вообще кто-то вызвал; почему "
        "хранить состояние в тексте кнопки не лучшая идея надолго; как сделать интерфейс, "
        "который реагирует на мышь и клавиатуру одним и тем же кодом. К концу главы (раздел "
        "17.31) та же самая игра станет <code class=\"inline\">tic_tac_toe.py</code> — с "
        "отдельной моделью состояния, подсветкой победной линии, счётом матчей и полными "
        "тестами.",
    )}

    {exercise(2, "Счёт побед", "Добавьте метки счёта побед X и O, увеличивайте нужный счётчик при каждой победе — счётчик не должен обнуляться кнопкой «Новая игра».")}
    {exercise(3, "Подсветка выигрышной линии", "Когда находится победитель, измените цвет фона трёх выигрышных кнопок — потребуется вернуть из proverit_pobedu() не только победителя, но и индексы линии.")}
{local_required_card(
        "17-06",
        "Практика: новая игра и первая полная версия",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/17-06/index.html",
    )}

    <h2 id="itogi">Итоги раздела</h2>
    {summary_box("Что мы узнали", [
        "<code class=\"inline\">.bind()</code> реагирует на любые события — не только клик "
        "по кнопке.",
        "Большие проекты строят по шагам: состояние → интерфейс → обработка событий → правила "
        "→ сброс.",
        "Лямбда с параметром по умолчанию (<code class=\"inline\">lambda i=indeks: ...</code>) "
        "«замораживает» значение переменной цикла в момент создания.",
        "Список кортежей — удобный способ описать несколько похожих проверок (восемь "
        "выигрышных линий) без повторения кода.",
        "У полноценной игры почти всегда есть способ начать заново, не перезапуская программу.",
        "Это только начало главы — дальше мы разберём систему событий Tkinter глубже и "
        "перестроим саму игру на более надёжной архитектуре.",
    ])}
    """
    out = render_page(
        page_title="Кнопка новой игры и первая полная версия",
        description="Сброс игры кнопкой «Новая игра», первая полностью рабочая версия и мост к остальной части главы 17.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Новая игра и итоги", "")],
        kicker="Глава 17 · Проект: «Крестики-нолики»",
        h1="Новая игра — и первая полная версия",
        lede="Финальный штрих первого прототипа — сброс игры без перезапуска программы. Но "
        "глава только начинается.",
        body_html=body,
        sidebar_groups=sidebar("17-06-novaya-igra-itogi.html"),
        nav=PageNav(prev_href="17-05-proverka-pobedy.html", prev_label="Проверка победы", next_href="17-07-event-callback-command-binding.html", next_label="Event, callback, command и binding"),
    )
    write("17-06-novaya-igra-itogi.html", out)


def build_07() -> None:
    body = f"""
    <h2>Кто вызывает on_click()?</h2>
    <p>Сравним два знакомых способа получить действие от пользователя.</p>
    {code_block(
        "posledovatelno.py",
        'imya = input("Как вас зовут? ")\n'
        "print(f\"Привет, {imya}!\")\n",
    )}
    <p>Здесь всё просто: программа сама, в известной строке кода, спрашивает и ждёт ответа.</p>
    {code_block(
        "gui.py",
        "def on_click():\n"
        '    print("Кнопка нажата")\n\n'
        'button = ttk.Button(root, text="OK", command=on_click)\n',
    )}
    <p><strong>Кто вызывает <code class="inline">on_click()</code></strong>? Не мы — в коде нет
    строки <code class="inline">on_click()</code>. Функция может выполниться через секунду,
    через час или никогда — в зависимости от того, нажмёт ли пользователь кнопку.</p>
    {pipeline_diagram([
        {"kind": "object", "title": "ваш код", "rows": ["регистрирует callback"]},
        {"kind": "plain", "title": "событийный цикл", "note": "ждёт / обрабатывает"},
        {"kind": "plain", "title": "действие пользователя"},
        {"kind": "object", "title": "Tk вызывает callback"},
        {"kind": "object", "title": "ваш код выполняется"},
        {"kind": "plain", "title": "возврат в событийный цикл"},
    ], caption="Callback — это код, вызов которого откладывается до наступления события.")}
    {callout(
        "info",
        "Ответ",
        "Callback вызывает <strong>система событий Tk</strong> — в момент, когда происходит "
        "соответствующее действие пользователя (или другое событие). Не ваш код, не "
        "интерпретатор Python сам по себе.",
    )}

    <h2>Event, callback, command, binding — четыре разных слова</h2>
    {comparison_table(
        ["Термин", "Что это"],
        [
            ["EVENT (событие)", "Факт: что-то произошло — клик, нажатие клавиши, наведение курсора"],
            ["CALLBACK (обратный вызов)", "Функция, которую вызывают В ОТВЕТ на событие"],
            ["COMMAND (команда)", "Высокоуровневый крючок конкретного виджета для его основного действия (например, клика по Button)"],
            ["BINDING (привязка)", "Связь между событием (последовательностью) и callback-функцией"],
        ],
    )}
    {callout(
        "warning",
        "Они связаны, но не взаимозаменяемы",
        "Событие — это ЧТО произошло. Callback — функция, которая ОТРЕАГИРУЕТ. Command — "
        "частный случай, специфичный для конкретного виджета. Binding — механизм, который "
        "соединяет событие с callback-ом. Спутать эти слова — источник путаницы в объяснении "
        "собственного кода.",
    )}

    {practice_card(
        "17-07",
        "Практика: классификация event/callback/command/binding",
        "Автоматическая проверка — классифицируем короткие примеры кода по этим четырём терминам",
        "../../practice/17-07/index.html",
    )}
    """
    out = render_page(
        page_title="Event, callback, command и binding",
        description="Кто вызывает callback в GUI-программе, и чем четыре термина event/callback/command/binding отличаются друг от друга.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Event/callback/command/binding", "")],
        kicker="Глава 17 · События глубже",
        h1="Event, callback, command и binding",
        lede="«Tkinter buttons are the game» — неверная модель. Начнём с вопроса: кто вообще "
        "вызывает ваш callback?",
        body_html=body,
        sidebar_groups=sidebar("17-07-event-callback-command-binding.html"),
        nav=PageNav(prev_href="17-06-novaya-igra-itogi.html", prev_label="Новая игра и первая версия", next_href="17-08-obyekt-event.html", next_label="Объект Event"),
    )
    write("17-07-event-callback-command-binding.html", out)


def build_08() -> None:
    body = f"""
    <h2>Не каждый callback получает event</h2>
    <p>Частое заблуждение: «обработчик события всегда принимает event». Это неточно.</p>
    {classic_vs_modern(
        "command= против bind()",
        "command= — БЕЗ event",
        "def new_game():\n"
        "    ...\n\n"
        'ttk.Button(root, text="Новая игра", command=new_game)',
        "bind() — С event",
        "def on_key(event):\n"
        "    ...\n\n"
        'root.bind("<KeyPress>", on_key)',
        "<code class=\"inline\">command=</code> вызывает функцию БЕЗ аргументов. "
        "<code class=\"inline\">.bind(sequence, callback)</code> вызывает функцию С ОДНИМ "
        "аргументом — объектом <code class=\"inline\">Event</code>. Перепутать сигнатуру — "
        "частая причина <code class=\"inline\">TypeError</code>.",
    )}

    <h2>Объект Event — что внутри</h2>
    {object_diagram(
        "event", "Event",
        [("widget", "виджет-источник"), ("type", "тип события"), ("keysym", "'Return', 'a', ..."),
         ("char", "текстовый символ"), ("keycode", "числовой код"), ("x", "координата X внутри виджета"), ("y", "координата Y внутри виджета")],
        width=480,
        caption="Не каждое поле имеет смысл для каждого события — подробнее ниже.",
    )}
    {callout(
        "warning",
        "event.x не имеет смысла для нажатия клавиши",
        "<code class=\"inline\">Event</code> — один класс на все типы событий, поэтому у него "
        "много полей сразу. Но <code class=\"inline\">event.x</code>/<code class=\"inline\">event.y</code> "
        "осмысленны для событий мыши, а не клавиатуры; <code class=\"inline\">event.keysym</code>/"
        "<code class=\"inline\">event.char</code> — для клавиатуры, а не для наведения мыши. "
        "Не читайте поле, если не уверены, что оно применимо к этому типу события.",
    )}

    <h2>event.widget</h2>
    {code_block(
        "event_widget.py",
        "def on_enter(event):\n"
        "    print(event.widget)   # какой именно виджет получил событие\n",
    )}
    <p><code class="inline">event.widget</code> — виджет, к которому относится событие. Это
    источник UI-события, а не игровое состояние (важное различие — раздел 17.18).</p>

    {local_required_card(
        "17-08",
        "Практика: инспектор объекта Event",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/17-08/index.html",
    )}
    """
    out = render_page(
        page_title="Объект Event",
        description="Что внутри объекта tkinter.Event, какие поля когда имеют смысл, и почему command= обычно не передаёт event.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Объект Event", "")],
        kicker="Глава 17 · События глубже",
        h1="Объект Event",
        lede="command= обычно не даёт вам event — bind() почти всегда даёт. Разберём, что внутри "
        "этого объекта.",
        body_html=body,
        sidebar_groups=sidebar("17-08-obyekt-event.html"),
        nav=PageNav(prev_href="17-07-event-callback-command-binding.html", prev_label="Event/callback/command/binding", next_href="17-09-sintaksis-sobytij.html", next_label="Синтаксис событий"),
    )
    write("17-08-obyekt-event.html", out)


def build_09() -> None:
    body = f"""
    <h2>Анатомия последовательности событий</h2>
    <p>Строка вроде <code class="inline">"&lt;Control-Button-1&gt;"</code> — это не магическое
    заклинание, а структура <code class="inline">&lt;модификатор-тип-деталь&gt;</code>, где
    часть элементов может отсутствовать:</p>
    {comparison_table(
        ["Запись", "Что означает"],
        [
            ["<code class=\"inline\">&lt;KeyPress&gt;</code>", "любая клавиша нажата (то же, что <code class=\"inline\">&lt;Key&gt;</code>)"],
            ["<code class=\"inline\">&lt;Return&gt;</code>", "конкретная клавиша Enter"],
            ["<code class=\"inline\">&lt;Escape&gt;</code>", "конкретная клавиша Escape"],
            ["<code class=\"inline\">&lt;Button-1&gt;</code>", "нажатие левой кнопки мыши"],
            ["<code class=\"inline\">&lt;Enter&gt;</code>", "курсор вошёл в границы виджета"],
            ["<code class=\"inline\">&lt;Leave&gt;</code>", "курсор покинул границы виджета"],
            ["<code class=\"inline\">&lt;Control-r&gt;</code>", "модификатор Control + клавиша r"],
        ],
    )}
    {callout(
        "info",
        "Не нужно запоминать всю грамматику Tk целиком",
        "У Tk десятки поддерживаемых последовательностей событий. Для главы 17 достаточно этого "
        "небольшого набора — при необходимости остальные ищутся в официальной документации "
        "Tcl/Tk по мере надобности, а не заучиваются заранее.",
    )}

    <h2>Button-1 — левая кнопка мыши</h2>
    {code_block(
        "button_1_demo.py",
        "def on_raw_click(event):\n"
        '    print("Клик мышью в координатах", event.x, event.y)\n\n'
        'label.bind("<Button-1>", on_raw_click)\n',
    )}
    {callout(
        "warning",
        "Не главный способ активировать клетки игры",
        "<code class=\"inline\">&lt;Button-1&gt;</code> полезен для демонстрации низкоуровневого "
        "события мыши — но для клеток игрового поля мы всё равно будем использовать "
        "<code class=\"inline\">command=</code> у Button (раздел 17.10). Здесь это просто "
        "иллюстрация синтаксиса.",
    )}

    {practice_card(
        "17-09",
        "Практика: синтаксис событий",
        "Автоматическая проверка — сопоставляем описание действия с правильной строкой последовательности события",
        "../../practice/17-09/index.html",
    )}
    """
    out = render_page(
        page_title="Синтаксис событий Tk",
        description="Анатомия строки-последовательности события Tk: <модификатор-тип-деталь> — на конкретных примерах.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Синтаксис событий", "")],
        kicker="Глава 17 · События глубже",
        h1="Синтаксис событий Tk",
        lede="<модификатор-тип-деталь> — не всегда нужны все три части сразу.",
        body_html=body,
        sidebar_groups=sidebar("17-09-sintaksis-sobytij.html"),
        nav=PageNav(prev_href="17-08-obyekt-event.html", prev_label="Объект Event", next_href="17-10-command-vs-bind.html", next_label="command vs bind"),
    )
    write("17-09-sintaksis-sobytij.html", out)


def build_10() -> None:
    body = f"""
    <h2>command= или bind() — как выбирать</h2>
    {decision_map([
        ("Нужна семантическая активация кнопки (клик мышью ИЛИ пробел/Enter при фокусе)", "command="),
        ("Нужны координаты движения мыши", "bind(\"&lt;Motion&gt;\", ...)"),
        ("Нужно знать, какая именно клавиша нажата", "bind(\"&lt;Key&gt;\", ...)"),
        ("Нужна реакция на наведение курсора (без клика)", "bind(\"&lt;Enter&gt;\"/\"&lt;Leave&gt;\", ...)"),
        ("Виджет вообще не предоставляет command (например, Label, Frame)", "bind()"),
    ], title="Что выбрать?")}

    {callout(
        "warning",
        "Не заменяйте Button.command на bind('<Button-1>', ...) по умолчанию",
        "Это профессиональное правило. <code class=\"inline\">command=</code> у Button — "
        "семантическая активация: у Button есть собственные встроенные привязки клавиатуры "
        "(как правило, пробел, когда кнопка в фокусе — клавиатурная доступность, глава 16, "
        "раздел 16.21), и именно они вызывают <code class=\"inline\">command</code>. Точное "
        "поведение (например, участвует ли Enter) может отличаться между "
        "<code class=\"inline\">tk.Button</code> и <code class=\"inline\">ttk.Button</code> и "
        "между платформами — но в любом случае это ГОТОВАЯ клавиатурная активация, за которую "
        "не нужно отвечать самому. Голая привязка <code class=\"inline\">&lt;Button-1&gt;</code> "
        "реагирует ТОЛЬКО на клик мышью и не даёт вообще никакой клавиатурной активации — вы "
        "молча теряете доступность. Замена command на bind «просто потому что можно» — "
        "типичная архитектурная ошибка, не стилистическая мелочь.",
    )}

    <h2>Как это распределится в игре</h2>
    {capability_map([
        ("Ход по клетке", ["command= у Button", "семантическая активация + доступность"]),
        ("Наведение — превью", ["bind(&lt;Enter&gt;/&lt;Leave&gt;)", "нет готового command для этого"]),
        ("Клавиши 1–9 / R", ["bind(&lt;Key&gt;) на root", "не привязано к одному виджету"]),
    ], title="Три задачи — три разных инструмента")}

    {practice_card(
        "17-10",
        "Практика: command vs bind — что выбрать",
        "Автоматическая проверка — для набора сценариев выбираем правильный инструмент",
        "../../practice/17-10/index.html",
    )}
    """
    out = render_page(
        page_title="command vs bind — что выбирать",
        description="Профессиональное правило выбора между command= и bind() — и почему заменять command на голый Button-1 вредно для доступности.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("command vs bind", "")],
        kicker="Глава 17 · События глубже",
        h1="command vs bind — что выбирать",
        lede="Не «bind существует, значит используем его везде» — у каждого инструмента своя "
        "работа.",
        body_html=body,
        sidebar_groups=sidebar("17-10-command-vs-bind.html"),
        nav=PageNav(prev_href="17-09-sintaksis-sobytij.html", prev_label="Синтаксис событий", next_href="17-11-focus-i-klaviatura.html", next_label="Focus и клавиатура"),
    )
    write("17-10-command-vs-bind.html", out)


def build_11() -> None:
    body = f"""
    <h2>Клавиатурным событиям нужен адресат</h2>
    <p>Окно, в котором есть привязка к клавише, не значит, что нажатие ЛЮБОЙ клавиши где угодно
    попадёт в этот обработчик. Каждое клавиатурное событие сначала приходит в виджет, у которого
    сейчас <strong>фокус ввода</strong> — а уже оттуда Tk проверяет привязки по цепочке
    <em>bindtags</em>: сам виджет → его класс → окно верхнего уровня (root) → "all".</p>
    {code_block(
        "focus_demo.py",
        "print(root.focus_get())   # какой виджет сейчас в фокусе (или None)\n\n"
        "entry.focus_set()         # явно передать фокус этому виджету\n",
    )}
    {callout(
        "warning",
        "«Привязка не работает» часто означает «класс виджета перехватил событие раньше»",
        "root.bind(\"&lt;Key&gt;\", ...) стоит в цепочке ПОСЛЕ привязок самого сфокусированного "
        "виджета и его класса — не вместо них. Если фокус на поле ввода, класс "
        "<code class=\"inline\">Entry</code> первым обрабатывает нажатие цифры (вписывает "
        "символ в поле); привязка на <code class=\"inline\">root</code> при этом обычно ВСЁ "
        "РАВНО срабатывает следом, если только обработчик явно не вернул "
        "<code class=\"inline\">\"break\"</code>, прервав цепочку. Значит символ и появится в "
        "поле ввода, И одновременно уйдёт в игровую логику — редко то, чего вы хотели. Смотрите "
        "Debug Lab 4 (раздел 17.29).",
    )}
    <p>Для главы 17 клавиатурные привязки повешены на <code class="inline">root</code> — но, как
    только что было показано, фокус на Entry или Text сам по себе НЕ отключает привязку на root
    (у нашей игры таких полей нет — все клетки это кнопки). В приложении с текстовыми полями
    важно не «удерживать фокус на root», а осознанно решить: должны ли игровые горячие клавиши
    работать, пока пользователь печатает текст? Если нет — обработчик может проверить
    <code class="inline">focus_get()</code> и сам проигнорировать нажатие, когда фокус находится
    на текстовом поле.</p>

    {local_required_card(
        "17-11",
        "Практика: focus_get() и focus_set()",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/17-11/index.html",
    )}
    """
    out = render_page(
        page_title="Focus и клавиатура",
        description="Клавиатурные события требуют фокуса ввода — focus_get()/focus_set() и типичная ловушка «привязка как будто не работает».",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Focus и клавиатура", "")],
        kicker="Глава 17 · События глубже",
        h1="Focus и клавиатура",
        lede="Окно существует — не значит, что оно получает все нажатия клавиш. Нужен фокус.",
        body_html=body,
        sidebar_groups=sidebar("17-11-focus-i-klaviatura.html"),
        nav=PageNav(prev_href="17-10-command-vs-bind.html", prev_label="command vs bind", next_href="17-12-enter-leave-hover.html", next_label="Mouse Enter/Leave и hover"),
    )
    write("17-11-focus-i-klaviatura.html", out)


def build_12() -> None:
    body = f"""
    <h2>Enter / Leave — идеальны для визуальных эффектов</h2>
    {pipeline_diagram([
        {"kind": "plain", "title": "курсор входит в клетку", "note": ""},
        {"kind": "object", "title": "&lt;Enter&gt;", "rows": ["on_cell_enter(index)"]},
        {"kind": "plain", "title": "курсор покидает клетку", "note": "без клика"},
        {"kind": "object", "title": "&lt;Leave&gt;", "rows": ["on_cell_leave(index)"]},
    ], caption="Наведение — не клик: ни одно из этих событий не должно менять игровое состояние.")}
    {code_block(
        "hover_bind.py",
        "button.bind(\n"
        '    "<Enter>",\n'
        "    lambda _event, i=index: self.on_cell_enter(i),\n"
        ")\n",
    )}
    {callout(
        "tip",
        "_event — намеренно неиспользуемое имя",
        "Callback от <code class=\"inline\">.bind()</code> обязан принять аргумент "
        "<code class=\"inline\">event</code>, даже если он не нужен внутри. Имя "
        "<code class=\"inline\">_event</code> (с подчёркиванием) — общепринятый сигнал "
        "«параметр существует по требованию сигнатуры, но сознательно не используется».",
    )}

    <h2>Binding scope — где действует привязка</h2>
    {comparison_table(
        ["Вызов", "Область действия"],
        [
            ["<code class=\"inline\">widget.bind(...)</code>", "только для этого конкретного виджета"],
            ["<code class=\"inline\">root.bind(...)</code>", "для главного окна (например, глобальные клавиши игры)"],
        ],
    )}
    {callout(
        "info",
        "🔬 ЧУТЬ ГЛУБЖЕ — bind_class / bind_all",
        "Tk также поддерживает <code class=\"inline\">bind_class(...)</code> (все виджеты "
        "одного класса) и <code class=\"inline\">bind_all(...)</code> (буквально всё "
        "приложение). Для главы 17 они не нужны — упомянуты, чтобы вы знали, что они "
        "существуют, если понадобятся в собственных проектах.",
    )}
    {callout(
        "info",
        "🔬 ЧУТЬ ГЛУБЖЕ — add=\"+\" и unbind()",
        "По умолчанию <code class=\"inline\">bind(sequence, callback)</code> ЗАМЕНЯЕТ предыдущий "
        "обработчик этой же последовательности на этом виджете. Необязательный третий аргумент "
        "<code class=\"inline\">add=\"+\"</code> вместо замены добавляет ЕЩЁ ОДИН обработчик — "
        "оба будут вызваны. <code class=\"inline\">widget.unbind(sequence)</code> убирает "
        "привязку целиком. Для главы 17 не нужны — но Debug Lab 20 (раздел 17.29) показывает, "
        "почему неосторожный <code class=\"inline\">add=\"+\"</code> может незаметно запустить "
        "один и тот же код дважды.",
    )}

    {local_required_card(
        "17-12",
        "Практика: hover через Enter/Leave",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/17-12/index.html",
    )}
    """
    out = render_page(
        page_title="Mouse Enter/Leave и hover",
        description="События <Enter>/<Leave>, binding scope (widget vs root) и краткий взгляд на bind_class/bind_all.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Enter/Leave и hover", "")],
        kicker="Глава 17 · События глубже",
        h1="Mouse Enter/Leave и hover",
        lede="Наведение курсора — событие само по себе, без клика. Идеально для визуальных "
        "подсказок.",
        body_html=body,
        sidebar_groups=sidebar("17-12-enter-leave-hover.html"),
        nav=PageNav(prev_href="17-11-focus-i-klaviatura.html", prev_label="Focus и клавиатура", next_href="17-13-model-sostoyaniya.html", next_label="Модель игрового состояния"),
    )
    write("17-12-enter-leave-hover.html", out)


def build_13() -> None:
    body = f"""
    <h2>Что вообще должна помнить программа?</h2>
    {object_diagram(
        "state", "GameState",
        [("board", "['', '', '', '', '', '', '', '', '']"), ("current_player", "'X'"), ("game_over", "False"),
         ("winner", "None"), ("winning_line", "None"), ("score_x", "0"), ("score_o", "0")],
        width=560,
        caption="Это данные — ни одной кнопки Tkinter здесь нет.",
    )}
    {callout(
        "warning",
        "Виджеты — НЕ каноническое игровое состояние",
        "Кнопки на экране ОТОБРАЖАЮТ состояние — они не являются им. Если наведение мыши "
        "временно рисует «X» на кнопке (раздел 17.23), это не значит, что ход сделан — "
        "настоящее состояние живёт отдельно от того, что нарисовано на экране прямо сейчас.",
    )}

    <h2>Прототип: state в глобальных переменных</h2>
    <p>Раздел 17.3 использовал ровно такой подход:</p>
    {code_block(
        "prototip_globals.py",
        'tekuschij_igrok = "X"\n'
        "polya = []\n"
        "igra_okonchena = False\n",
    )}
    {callout(
        "info",
        "Прототип: сначала делаем состояние видимым",
        "Глобальные переменные — приемлемый выбор для самого первого маленького прототипа: "
        "их легко читать и легко объяснить. Проблема появляется, когда проект растёт — "
        "глобальные переменные создают скрытые связи между функциями, которые неявно ожидают, "
        "что кто-то другой уже их изменил в правильном порядке. Это не значит «глобальные "
        "переменные — зло»: это значит, что у них есть компромисс между простотой и "
        "сопровождаемостью, который стоит замечать.",
    )}

    <h2>Путь этой главы</h2>
    {capability_map([
        ("V1 — глобальные (17.3)", ["3 отдельные переменные", "просто, но растёт бесконтрольно"]),
        ("V2 — словарь", ["{'board': [...], ...}", "один объект вместо трёх переменных"]),
        ("V3 — GameState (17.19)", ["@dataclass", "типизировано, читаемо, тестируемо"]),
    ], title="От глобальных переменных к GameState")}

    {practice_card(
        "17-13",
        "Практика: моделируем игровое состояние",
        "Автоматическая проверка — строим и проверяем словарь-состояние без Tkinter",
        "../../practice/17-13/index.html",
    )}
    """
    out = render_page(
        page_title="Модель игрового состояния",
        description="Что программа обязана помнить между ходами, и почему виджеты не являются каноническим состоянием игры.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Модель состояния", "")],
        kicker="Глава 17 · Модель и правила",
        h1="Модель игрового состояния",
        lede="Tkinter отображает игру и доставляет ввод. Игровое СОСТОЯНИЕ — отдельная вещь.",
        body_html=body,
        sidebar_groups=sidebar("17-13-model-sostoyaniya.html"),
        nav=PageNav(prev_href="17-12-enter-leave-hover.html", prev_label="Enter/Leave и hover", next_href="17-14-indeksy-stroki-stolbcy.html", next_label="Индексы, строки и столбцы"),
    )
    write("17-13-model-sostoyaniya.html", out)


def build_14() -> None:
    board_indices = board_diagram([str(i) for i in range(9)], indices=False, caption="Индексы клеток поля 0..8 — слева направо, сверху вниз.")
    body = f"""
    <h2>Поле — плоский список из девяти элементов</h2>
    {board_indices}
    <p>Хотя визуально поле — таблица 3×3, в памяти это ОДИН плоский список из девяти
    элементов (<code class="inline">board[0]</code> .. <code class="inline">board[8]</code>),
    как и в разделе 17.3.</p>

    <h2>Индекс → строка и столбец</h2>
    {code_block(
        "indeks_v_koordinaty.py",
        "row = index // 3\n"
        "column = index % 3\n",
    )}
    <table class="compare-table">
      <thead><tr><th>index</th><th>row</th><th>column</th></tr></thead>
      <tbody>
        {"".join(f"<tr><td>{i}</td><td>{i // 3}</td><td>{i % 3}</td></tr>" for i in range(9))}
      </tbody>
    </table>

    <h2>Обратное направление: строка и столбец → индекс</h2>
    {code_block(
        "koordinaty_v_indeks.py",
        "index = row * 3 + column\n",
    )}
    {callout(
        "tip",
        "Пригодится не только здесь",
        "Формула <code class=\"inline\">row * ширина + column</code> — общий приём для любой "
        "прямоугольной сетки, хранящейся плоским списком (изображения, карты уровней, "
        "электронные таблицы).",
    )}

    {practice_card(
        "17-14",
        "Практика: индекс, строка, столбец",
        "Автоматическая проверка — прямое и обратное преобразование координат для всех 9 клеток",
        "../../practice/17-14/index.html",
    )}
    """
    out = render_page(
        page_title="Индексы, строки и столбцы",
        description="Плоский список из 9 элементов как модель поля 3×3: index // 3, index % 3 и обратное преобразование.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Индексы, строки, столбцы", "")],
        kicker="Глава 17 · Модель и правила",
        h1="Индексы, строки и столбцы",
        lede="Поле выглядит как таблица 3×3 — но в памяти это один список из девяти элементов.",
        body_html=body,
        sidebar_groups=sidebar("17-14-indeksy-stroki-stolbcy.html"),
        nav=PageNav(prev_href="17-13-model-sostoyaniya.html", prev_label="Модель состояния", next_href="17-15-algoritm-hoda.html", next_label="Алгоритм хода"),
    )
    write("17-14-indeksy-stroki-stolbcy.html", out)


def build_15() -> None:
    body = f"""
    <h2>Валидный ход — что это?</h2>
    <p><code class="inline">attempt_move(index)</code> — единый путь для мыши и клавиатуры
    (раздел 17.24). Разберём его в двух шагах: сначала фильтр валидности, потом — что происходит
    после того, как ход уже принят.</p>

    <h3>Диаграмма 1 — фильтр валидности хода</h3>
    {flowchart([
        {"kind": "start", "label": "клик / клавиша на клетке index"},
        {"kind": "decision", "label": "игра окончена?",
         "yes": [{"kind": "end", "label": "ход игнорируется"}],
         "no": [{"kind": "decision", "label": "клетка занята?",
                 "yes": [{"kind": "end", "label": "ход игнорируется"}],
                 "no": [{"kind": "end", "label": "ВАЛИДНЫЙ ХОД"}]}]},
    ], caption="Оба «нет» должны выполниться, чтобы ход дошёл до диаграммы 2.")}
    {callout(
        "warning",
        "Невалидный ход НЕ переключает игрока",
        "Это частая ошибка (Debug Lab 10, раздел 17.29): если клик проигнорирован — очередь "
        "хода должна остаться прежней. Переключение игрока происходит только ПОСЛЕ успешного "
        "хода.",
    )}

    <h3>Диаграмма 2 — что происходит после валидного хода</h3>
    {flowchart([
        {"kind": "start", "label": "ВАЛИДНЫЙ ХОД (из диаграммы 1)"},
        {"kind": "process", "label": "board[index] = current_player"},
        {"kind": "decision", "label": "find_winner(board) есть победитель?",
         "yes": [{"kind": "end", "label": "TERMINAL: победа — render()"}],
         "no": [{"kind": "decision", "label": "all(board) заполнено?",
                 "yes": [{"kind": "end", "label": "TERMINAL: ничья — render()"}],
                 "no": [{"kind": "process", "label": "сменить игрока"},
                        {"kind": "process", "label": "render()"}]}]},
    ], caption="Коммит в модель, проверка правил (раздел 17.17), и только потом — смена игрока.")}

    <h2>Переключение игрока — три эквивалентных способа</h2>
    {code_block(
        "smena_igroka_razvernuto.py",
        'if current_player == "X":\n'
        '    current_player = "O"\n'
        "else:\n"
        '    current_player = "X"\n',
    )}
    {code_block(
        "smena_igroka_kratko.py",
        'current_player = "O" if current_player == "X" else "X"\n',
    )}
    {callout(
        "tip",
        "Читаемость важнее лаконичности — сначала",
        "Обе версии делают одно и то же. Развёрнутая явно читается как «если/иначе» — с ней "
        "проще начинать. Короткая версия (тернарный оператор, глава 9) — не «умнее», просто "
        "компактнее, когда вы уже уверенно её читаете.",
    )}

    {practice_card(
        "17-15",
        "Практика: логика одного хода",
        "Автоматическая проверка — валидация хода и переключение игрока на чистых функциях",
        "../../practice/17-15/index.html",
    )}
    """
    out = render_page(
        page_title="Правильный алгоритм хода",
        description="Что делает валидный ход, почему невалидный ход не переключает игрока, и три эквивалентных способа сменить текущего игрока.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Алгоритм хода", "")],
        kicker="Глава 17 · Модель и правила",
        h1="Правильный алгоритм хода",
        lede="Один путь для любого способа сделать ход — проверка, ход, правила, смена игрока.",
        body_html=body,
        sidebar_groups=sidebar("17-15-algoritm-hoda.html"),
        nav=PageNav(prev_href="17-14-indeksy-stroki-stolbcy.html", prev_label="Индексы, строки, столбцы", next_href="17-16-vosem-linij-pobedy.html", next_label="Восемь выигрышных линий"),
    )
    write("17-15-algoritm-hoda.html", out)


def build_16() -> None:
    row0 = board_diagram(["X", "X", "X", "", "", "", "", "", ""], highlighted=(0, 1, 2), caption="Строка 1")
    row1 = board_diagram(["", "", "", "X", "X", "X", "", "", ""], highlighted=(3, 4, 5), caption="Строка 2")
    row2 = board_diagram(["", "", "", "", "", "", "X", "X", "X"], highlighted=(6, 7, 8), caption="Строка 3")
    col0 = board_diagram(["X", "", "", "X", "", "", "X", "", ""], highlighted=(0, 3, 6), caption="Столбец 1")
    col1 = board_diagram(["", "X", "", "", "X", "", "", "X", ""], highlighted=(1, 4, 7), caption="Столбец 2")
    col2 = board_diagram(["", "", "X", "", "", "X", "", "", "X"], highlighted=(2, 5, 8), caption="Столбец 3")
    diag0 = board_diagram(["X", "", "", "", "X", "", "", "", "X"], highlighted=(0, 4, 8), caption="Диагональ 0-4-8")
    diag1 = board_diagram(["", "", "X", "", "X", "", "X", "", ""], highlighted=(2, 4, 6), caption="Диагональ 2-4-6")
    body = f"""
    <h2>Все восемь выигрышных линий</h2>
    <h3 style="text-align:center;font-size:15px;color:var(--color-text-muted,#6B6B7D);margin-bottom:8px">Строки</h3>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px;margin-bottom:28px">
      {row0}{row1}{row2}
    </div>
    <h3 style="text-align:center;font-size:15px;color:var(--color-text-muted,#6B6B7D);margin-bottom:8px">Столбцы</h3>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px;margin-bottom:28px">
      {col0}{col1}{col2}
    </div>
    <h3 style="text-align:center;font-size:15px;color:var(--color-text-muted,#6B6B7D);margin-bottom:8px">Диагонали</h3>
    <div style="display:flex;flex-wrap:wrap;justify-content:center;gap:20px">
      {diag0}{diag1}
    </div>

    <h2>Константа WINNING_LINES</h2>
    {code_block(
        "winning_lines.py",
        "WINNING_LINES = (\n"
        "    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # строки\n"
        "    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # столбцы\n"
        "    (0, 4, 8), (2, 4, 6),             # диагонали\n"
        ")\n",
    )}
    {callout(
        "tip",
        "ЗАГЛАВНЫМИ — это данные правил, а не алгоритм",
        "<code class=\"inline\">WINNING_LINES</code> написана заглавными по соглашению Python "
        "для констант модуля (глава 13) — это данные о правилах игры, отдельные от кода, "
        "который их использует. <code class=\"inline\">find_winner()</code> сам по себе не "
        "знает о размере 3×3 — он просто перебирает готовые линии. Но константа решает не всё: "
        "индексная арифметика (<code class=\"inline\">// 3</code>, <code class=\"inline\">% "
        "3</code>), длина <code class=\"inline\">[\"\"] * 9</code> и сама 3×3-сетка виджетов "
        "тоже жёстко зашиты на размер поля — реальная поддержка другого размера потребовала бы "
        "менять всё это, а не только <code class=\"inline\">WINNING_LINES</code>.",
    )}

    <h2>find_winner() — чистая функция</h2>
    {code_block(
        "find_winner.py",
        "def find_winner(board):\n"
        "    for a, b, c in WINNING_LINES:\n"
        "        mark = board[a]\n"
        "        if mark and mark == board[b] == board[c]:\n"
        "            return mark, (a, b, c)\n"
        "    return None, None\n",
    )}
    {callout(
        "info",
        "Возвращает И победителя, И саму линию",
        "Раздел 17.5 возвращал только победителя. <code class=\"inline\">find_winner()</code> "
        "возвращает пару <code class=\"inline\">(winner, winning_line)</code> — индексы линии "
        "нужны, чтобы подсветить именно её (раздел 17.25), не пересчитывая победителя заново.",
    )}
    {callout(
        "warning",
        "Ничего не знает про Tkinter",
        "<code class=\"inline\">find_winner(board)</code> принимает обычный список строк — "
        "никаких кнопок, никакого <code class=\"inline\">root</code>. Это то, что делает "
        "функцию тестируемой без единого открытого окна (раздел 17.28).",
    )}

    {practice_card(
        "17-16",
        "Практика: find_winner для всех восьми линий",
        "Автоматическая проверка — find_winner на каждой из восьми линий для X и O",
        "../../practice/17-16/index.html",
    )}
    """
    out = render_page(
        page_title="Восемь выигрышных линий",
        description="Все восемь выигрышных линий визуально, константа WINNING_LINES и чистая функция find_winner(board).",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Восемь линий победы", "")],
        kicker="Глава 17 · Правила игры",
        h1="Восемь выигрышных линий",
        lede="Три строки, три столбца, две диагонали — и одна чистая функция, которая их все "
        "проверяет.",
        body_html=body,
        sidebar_groups=sidebar("17-16-vosem-linij-pobedy.html"),
        nav=PageNav(prev_href="17-15-algoritm-hoda.html", prev_label="Алгоритм хода", next_href="17-17-pobeda-nichya-terminal.html", next_label="Победа, ничья, terminal state"),
    )
    write("17-16-vosem-linij-pobedy.html", out)


def build_17() -> None:
    full_win_diag = board_diagram(["O", "O", "X", "X", "X", "O", "X", "X", "O"], highlighted=(2, 4, 6), caption="9-й ход одновременно заполняет поле И выигрывает диагональ 2-4-6.")
    body = f"""
    <h2>is_draw() — чистая функция</h2>
    {code_block(
        "is_draw.py",
        "def is_draw(board):\n"
        "    winner, _ = find_winner(board)\n"
        "    return winner is None and all(board)\n",
    )}
    {callout(
        "warning",
        "«Поле заполнено» — недостаточное условие ничьей",
        "Заполненное поле само по себе не гарантирует ничью — если последний ход одновременно "
        "выигрывает линию, это ПОБЕДА, а не ничья. Порядок проверки решает всё.",
    )}

    <h2>Последний ход: победа побеждает ничью</h2>
    {full_win_diag}
    {callout(
        "info",
        "Обязательное упражнение-предсказание",
        "Прежде чем читать код — предскажите: если 9-й ход заполняет ПОСЛЕДНЮЮ пустую клетку И "
        "выстраивает линию, что покажет программа? «Ничья» или «Победа X»? Правильный ответ — "
        "«Победа», если <code class=\"inline\">find_winner()</code> проверяется РАНЬШЕ "
        "<code class=\"inline\">is_draw()</code>. Именно поэтому <code class=\"inline\">is_draw</code> "
        "внутри себя сначала зовёт <code class=\"inline\">find_winner</code> и только потом "
        "смотрит на заполненность.",
    )}

    <h2>Terminal state</h2>
    <p>ПОБЕДА и НИЧЬЯ — истинные тупики: как только партия туда попала, обратного пути в
    «игра продолжается» нет. Ниже это показано буквально — у терминальных узлов нет исходящих
    стрелок.</p>
    {flowchart([
        {"kind": "start", "label": "После валидного хода"},
        {"kind": "decision", "label": "find_winner(board) есть победитель?",
         "yes": [{"kind": "end", "label": "TERMINAL: ПОБЕДА X/O"}],
         "no": [{"kind": "decision", "label": "all(board) заполнено?",
                 "yes": [{"kind": "end", "label": "TERMINAL: НИЧЬЯ"}],
                 "no": [{"kind": "process", "label": "игра продолжается"},
                        {"kind": "process", "label": "сменить игрока"}]}]},
    ], caption="ПОБЕДА и НИЧЬЯ — терминальные состояния: партия закончилась и больше не принимает ходов.")}

    {practice_card(
        "17-17",
        "Практика: победа против ничьей — порядок проверки",
        "Автоматическая проверка — в том числе тест на «последний ход выигрывает, а не заканчивается ничьей»",
        "../../practice/17-17/index.html",
    )}
    """
    out = render_page(
        page_title="Победа, ничья и terminal state",
        description="is_draw(board), обязательный порядок проверки (сначала победа, потом ничья) и понятие terminal state.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Победа, ничья, terminal state", "")],
        kicker="Глава 17 · Правила игры",
        h1="Победа, ничья и terminal state",
        lede="Заполненное поле — не всегда ничья. Порядок проверки — часть правил игры.",
        body_html=body,
        sidebar_groups=sidebar("17-17-pobeda-nichya-terminal.html"),
        nav=PageNav(prev_href="17-16-vosem-linij-pobedy.html", prev_label="Восемь линий победы", next_href="17-18-model-a-ne-widgets.html", next_label="От widgets-as-state к модели"),
    )
    write("17-17-pobeda-nichya-terminal.html", out)


def build_18() -> None:
    body = f"""
    <h2>Раздел 17.3 хранил состояние В ТЕКСТЕ кнопки</h2>
    {code_block(
        "widget_kak_istochnik.py",
        '# text кнопки — единственное место, где хранится "занята клетка или нет"\n'
        'if polya[indeks]["text"] != "":\n'
        "    return\n",
    )}
    <p>Это работало для маленького прототипа. Но представьте эффект наведения (раздел 17.23):
    он временно показывает «X» на пустой кнопке, ещё не сделав хода. Если состояние ЖИВЁТ в
    тексте кнопки — программа больше не может отличить «наведение» от «настоящего хода».</p>

    {converge_diagram(["наведение (превью)", "настоящий клик (ход)"], "button['text'] изменился", caption="Если у обоих один и тот же сигнал — как отличить один от другого?")}

    <h2>Модель отдельно, кнопка — только отображение</h2>
    {pipeline_diagram([
        {"kind": "object", "title": "MODEL", "rows": ["board[4] = 'X'"]},
        {"kind": "plain", "title": "render()"},
        {"kind": "object", "title": "VIEW", "rows": ["buttons[4] показывает 'X'"]},
    ], caption="Данные текут в одну сторону: модель → render() → виджет. Никогда наоборот.")}
    {callout(
        "warning",
        "Кнопка может ВРЕМЕННО показывать не то, что в модели",
        "Во время наведения <code class=\"inline\">buttons[4][\"text\"] == \"X\"</code>, а "
        "<code class=\"inline\">board[4] == \"\"</code> — и это НОРМАЛЬНО, если модель "
        "остаётся источником истины. Проблема начинается только тогда, когда код (например, "
        "проверка победителя) читает состояние из текста кнопки вместо модели — см. Debug Lab "
        "6, раздел 17.29.",
    )}

    <h2>board = список строк — окончательная модель</h2>
    {code_block(
        "board_model.py",
        'board = ["", "", "", "", "", "", "", "", ""]\n'
        '# board[4] = "X"  — это НАСТОЯЩИЙ ход, кнопка лишь отображает это значение\n',
    )}

    {practice_card(
        "17-18",
        "Практика: модель против виджета-как-состояния",
        "Автоматическая проверка — на игрушечной модели виджета без Tkinter показываем, почему widget-as-state ломается",
        "../../practice/17-18/index.html",
    )}
    """
    out = render_page(
        page_title="От widgets-as-state к board model",
        description="Почему хранить игровое состояние в тексте кнопки — плохая архитектура, и как отделить модель от отображения.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Модель, а не виджеты", "")],
        kicker="Глава 17 · Архитектура",
        h1="От widgets-as-state к board model",
        lede="Наведение мыши временно рисует X на пустой кнопке. Если это и есть «состояние» — "
        "игра сломана.",
        body_html=body,
        sidebar_groups=sidebar("17-18-model-a-ne-widgets.html"),
        nav=PageNav(prev_href="17-17-pobeda-nichya-terminal.html", prev_label="Победа, ничья, terminal state", next_href="17-19-gamestate-dataclass.html", next_label="GameState с dataclass"),
    )
    write("17-18-model-a-ne-widgets.html", out)


def build_19() -> None:
    body = f"""
    <h2>GameState — @dataclass (глава 14)</h2>
    {code_block(
        "game_state.py",
        "from dataclasses import dataclass, field\n\n"
        "@dataclass\n"
        "class GameState:\n"
        '    board: list[str] = field(default_factory=lambda: [""] * 9)\n'
        '    current_player: str = "X"\n'
        "    game_over: bool = False\n"
        "    winner: str | None = None\n"
        "    winning_line: tuple[int, int, int] | None = None\n"
        "    score_x: int = 0\n"
        "    score_o: int = 0\n"
        "    draws: int = 0\n",
    )}

    {callout(
        "warning",
        "НЕ board: list[str] = [\"\"] * 9",
        "Для <code class=\"inline\">@dataclass</code> это даже не тихий баг: Python замечает "
        "изменяемое значение по умолчанию (<code class=\"inline\">list</code>, "
        "<code class=\"inline\">dict</code>, <code class=\"inline\">set</code>) прямо при "
        "определении класса и сразу отказывает — <code class=\"inline\">ValueError: mutable "
        "default &lt;class 'list'&gt; for field board is not allowed: use default_factory</code>. "
        "Класс с такой строкой вообще не создастся, значит до «расшаривания между экземплярами» "
        "(глава 14 разбирала эту ловушку для обычных изменяемых аргументов по умолчанию) дело "
        "не дойдёт. <code class=\"inline\">field(default_factory=lambda: [\"\"] * 9)</code> — "
        "единственный способ, которым dataclass разрешит дать полю новый список при каждом "
        "создании экземпляра.",
    )}

    {class_diagram(
        "GameState",
        ["board: list[str]", "current_player: str", "game_over: bool",
         "winner: str | None", "winning_line: tuple | None", "score_x: int",
         "score_o: int", "draws: int"],
        [],
        caption="GameState хранит ТОЛЬКО данные партии — ни одного виджета внутри.",
    )}

    {practice_card(
        "17-19",
        "Практика: GameState как dataclass",
        "Автоматическая проверка — умолчания, независимость экземпляров, поля состояния",
        "../../practice/17-19/index.html",
    )}
    """
    out = render_page(
        page_title="GameState с dataclass",
        description="GameState как @dataclass, безопасная фабрика умолчания для изменяемого поля board и структура класса.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("GameState dataclass", "")],
        kicker="Глава 17 · Архитектура",
        h1="GameState с dataclass",
        lede="От прототипных глобальных переменных — к одному типизированному объекту "
        "состояния.",
        body_html=body,
        sidebar_groups=sidebar("17-19-gamestate-dataclass.html"),
        nav=PageNav(prev_href="17-18-model-a-ne-widgets.html", prev_label="Модель, а не виджеты", next_href="17-20-arhitektura-app.html", next_label="Архитектура TicTacToeApp"),
    )
    write("17-19-gamestate-dataclass.html", out)


def build_20() -> None:
    body = f"""
    <h2>app HAS-A root — не наследование от Tk</h2>
    {classic_vs_modern(
        "Композиция против наследования",
        "Возможно, но не нужно",
        "class TicTacToeApp(tk.Tk):\n"
        "    def __init__(self):\n"
        "        super().__init__()\n"
        "        ...",
        "Как в главе 16",
        "class TicTacToeApp:\n"
        "    def __init__(self, root):\n"
        "        self.root = root\n"
        "        ...",
        "Наследование от <code class=\"inline\">tk.Tk</code> технически работает, но не "
        "нужно и не согласуется с тем, как строились приложения в главе 16. "
        "<code class=\"inline\">app.root</code> (композиция, «HAS-A») — тот же паттерн, что и "
        "у Tip Calculator Pro и редактора заметок.",
    )}

    <h2>Объектный граф приложения</h2>
    {object_diagram(
        "app", "TicTacToeApp",
        [("root", "Tk"), ("state", "GameState"), ("buttons", "list[Button]"),
         ("status_var", "StringVar"), ("score_var", "StringVar")],
        caption="app хранит виджеты и ССЫЛКУ на состояние — не наоборот.",
    )}

    <h2>Домен против UI — разделение ответственности</h2>
    {comparison_table(
        ["Чистая доменная логика (без Tkinter)", "UI-логика (внутри TicTacToeApp)"],
        [
            ["find_winner(board)", "on_cell_click / attempt_move — вызывает домен, потом render"],
            ["is_draw(board)", "on_cell_enter / on_cell_leave — превью"],
            ["index → row/column", "render() — рисует виджеты ИЗ модели (state)"],
            ["", "new_round() / new_match() — жизненный цикл"],
        ],
    )}
    {callout(
        "tip",
        "Проверка «можно ли протестировать без окна?»",
        "Хороший тест архитектуры: если для проверки функции обязательно открывать окно "
        "Tkinter — это, вероятно, UI-логика. Если можно вызвать её с обычными списком/строкой "
        "и получить результат — это доменная логика, и её МОЖНО было бы вынести в отдельный "
        "модуль.",
    )}

    {local_required_card(
        "17-20",
        "Практика: собираем объектный граф TicTacToeApp",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/17-20/index.html",
    )}
    """
    out = render_page(
        page_title="Архитектура TicTacToeApp",
        description="Композиция вместо наследования от Tk, объектный граф приложения и разделение доменной логики и UI-логики.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Архитектура TicTacToeApp", "")],
        kicker="Глава 17 · Архитектура",
        h1="Архитектура TicTacToeApp",
        lede="app.root, а не class TicTacToeApp(tk.Tk) — та же композиция, что и в главе 16.",
        body_html=body,
        sidebar_groups=sidebar("17-20-arhitektura-app.html"),
        nav=PageNav(prev_href="17-19-gamestate-dataclass.html", prev_label="GameState dataclass", next_href="17-21-adaptivnoe-pole.html", next_label="Адаптивное игровое поле"),
    )
    write("17-20-arhitektura-app.html", out)


def build_21() -> None:
    body = f"""
    <h2>Поле не должно быть хрупкой грудой фиксированных виджетов</h2>
    {code_block(
        "adaptivnoe_pole.py",
        "# outer — родительский контейнер (build_ui); строка 1 — это строка поля\n"
        "outer.rowconfigure(1, weight=1)\n\n"
        "board_frame = ttk.Frame(outer)\n"
        "board_frame.grid(row=1, column=0, columnspan=3, sticky=\"nsew\")\n"
        "for i in range(3):\n"
        "    board_frame.rowconfigure(i, weight=1)\n"
        "    board_frame.columnconfigure(i, weight=1)\n\n"
        "for index in range(9):\n"
        "    btn = tk.Button(board_frame, text=\"\", font=(\"Arial\", 28, \"bold\"), width=3, height=1)\n"
        '    btn.grid(row=index // 3, column=index % 3, sticky="nsew", padx=3, pady=3)\n',
    )}
    {callout(
        "info",
        "sticky='nsew' + weight — на КАЖДОМ уровне вложенности",
        "Те же приёмы адаптивного <code class=\"inline\">grid()</code>, что и в разделе 16.15 — "
        "но их нужно применить на обоих уровнях сразу. Внутри <code class=\"inline\">board_frame</code> "
        "уже недостаточно дать вес строкам/столбцам, если сам "
        "<code class=\"inline\">board_frame</code> не растягивается в своей ячейке "
        "<code class=\"inline\">outer</code>: нужны И <code class=\"inline\">outer.rowconfigure(1, "
        "weight=1)</code> на родителе, И <code class=\"inline\">sticky=\"nsew\"</code> на самом "
        "<code class=\"inline\">board_frame.grid()</code>. Пропустить любое из двух — и поле "
        "перестанет расти вместе с окном по вертикали.",
    )}
    {callout(
        "warning",
        "Не обещаем идеально квадратные клетки на любой платформе",
        "<code class=\"inline\">width=3, height=1</code> у <code class=\"inline\">tk.Button</code> "
        "задаёт размер в текстовых единицах (символах/строках шрифта), а не в пикселях — "
        "точное соотношение сторон зависит от шрифта и темы конкретной ОС. Мы делаем поле "
        "адаптивным и опрятным — не гарантируем математически точный квадрат на всех "
        "платформах одновременно.",
    )}

    <h2>Видно на реальном окне, а не только в коде</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;align-items:start">
      {image_figure(f"{IMG}/adaptive-board-small.png", "Обычный размер окна: поле умещается компактно", "Обычный размер окна", width=300)}
      {image_figure(f"{IMG}/adaptive-board-large.png", "Окно увеличено: то же самое состояние партии, но клетки крупнее", "Окно увеличено вручную", width=460)}
    </div>
    <p style="text-align:center;font-size:14px;color:var(--color-text-muted,#6B6B7D);margin-top:4px">
    Одно и то же приложение, одно и то же состояние партии: <code class="inline">board_frame</code>
    растёт вместе с окном, потому что вес и <code class="inline">sticky</code> настроены на
    каждом уровне <code class="inline">grid()</code>.</p>

    {local_required_card(
        "17-21",
        "Практика: адаптивное поле при изменении размера окна",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/17-21/index.html",
    )}
    """
    out = render_page(
        page_title="Адаптивное игровое поле",
        description="grid() с sticky='nsew' и weight делает поле адаптивным к изменению размера окна — приём из главы 16.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Адаптивное поле", "")],
        kicker="Глава 17 · Интерфейс игры",
        h1="Адаптивное игровое поле",
        lede="Игра не должна разваливаться при изменении размера окна — grid() и weight решают "
        "это так же, как в главе 16.",
        body_html=body,
        sidebar_groups=sidebar("17-21-adaptivnoe-pole.html"),
        nav=PageNav(prev_href="17-20-arhitektura-app.html", prev_label="Архитектура TicTacToeApp", next_href="17-22-vizualnyj-stil.html", next_label="Визуальный стиль X/O"),
    )
    write("17-21-adaptivnoe-pole.html", out)


def build_22() -> None:
    swatches = color_swatch_row([
        ("#5B24F9", "Игрок X", "#5B24F9"),
        ("#DB2777", "Игрок O", "#DB2777"),
        ("#059669", "Победная линия", "#D1FAE5"),
        ("#6B6B7D", "Недоступно (конец игры)", "#F1EEFC"),
    ])
    body = f"""
    <h2>Палитра игры — сначала увиденная, потом числовая</h2>
    {swatches}
    <p>X — фиолетовый (<code class="inline">#5B24F9</code>), O — розовый
    (<code class="inline">#DB2777</code>) — те же фирменные цвета курса, что и везде на сайте.
    Победная линия подсвечивается мягким зелёным фоном, а после конца игры отметки становятся
    приглушёнными — виджет <code class="inline">disabled</code> сигнализирует «здесь больше
    нельзя ходить».</p>

    <h2>Почему здесь используется классический tk.Button, а не ttk</h2>
    {callout(
        "info",
        "Осознанный выбор, а не «забыли про ttk»",
        "Глава 16 учит предпочитать <code class=\"inline\">ttk</code> там, где есть "
        "тематизированный аналог (раздел 16.12). Но покраска отдельной клетки в цвет игрока "
        "напрямую через <code class=\"inline\">fg=</code>/<code class=\"inline\">bg=</code> — "
        "именно то, что <code class=\"inline\">tk.Button</code> делает просто и предсказуемо, "
        "а тема <code class=\"inline\">ttk</code> обычно перекрывает подобную покраску по "
        "виджету через <code class=\"inline\">ttk.Style()</code>. Рамка, статус и счёт при "
        "этом всё равно построены на <code class=\"inline\">ttk</code> — выбор виджета "
        "принят осознанно ради конкретной задачи, не по привычке.",
    )}
    {code_block(
        "cvet_otmetki.py",
        "MARK_COLOR = {\"X\": \"#5B24F9\", \"O\": \"#DB2777\"}\n\n"
        "btn.config(text=mark, fg=MARK_COLOR.get(mark, \"#0D0230\"))\n",
    )}
    {callout(
        "warning",
        "Не только цвет — ещё и буква, и текст статуса",
        "Победителя видно не только по зелёной подсветке: буквы «X»/«O» остаются на месте, а "
        "статус явно пишет «Победил игрок X!». Раздел 55 брифа книги специально предупреждает: "
        "нельзя полагаться только на цвет как на единственный сигнал.",
    )}

    {local_required_card(
        "17-22",
        "Практика: покраска X и O",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/17-22/index.html",
    )}
    """
    out = render_page(
        page_title="Визуальный стиль X/O",
        description="Цветовая палитра игры, осознанный выбор tk.Button для клеток поля, и почему цвет — не единственный сигнал победы.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Визуальный стиль X/O", "")],
        kicker="Глава 17 · Интерфейс игры",
        h1="Визуальный стиль X/O",
        lede="X и O должны различаться с первого взгляда — и не только по цвету.",
        body_html=body,
        sidebar_groups=sidebar("17-22-vizualnyj-stil.html"),
        nav=PageNav(prev_href="17-21-adaptivnoe-pole.html", prev_label="Адаптивное поле", next_href="17-23-hover-preview.html", next_label="Hover preview через bind()"),
    )
    write("17-22-vizualnyj-stil.html", out)


def build_23() -> None:
    body = f"""
    <h2>Наведение — сигнатурный визуальный эффект главы</h2>
    {image_figure(f"{IMG}/hover-preview-x.png", "Наведение на пустую клетку показывает бледный превью X", f"Реальное окно полной версии игры: курсор навёлся на пустую клетку — превью показывает X бледным цветом, ход ещё не сделан. Фрагмент ниже — это только код, который отвечает за сам эффект наведения.", width=320)}
    {code_block(
        "hover_preview.py",
        "def on_cell_enter(self, index):\n"
        "    state = self.state\n"
        "    if state.game_over or state.board[index]:\n"
        "        return   # не показываем превью — конец игры или клетка занята\n"
        "    self.buttons[index].config(text=state.current_player, fg=HOVER_COLOR)\n\n"
        "def on_cell_leave(self, index):\n"
        "    self.render()   # не 'text=\"\"' — а render() из МОДЕЛИ\n",
    )}
    {callout(
        "warning",
        "on_cell_leave НЕ должен просто стирать текст",
        "Наивная реализация <code class=\"inline\">on_cell_leave</code> вида "
        "<code class=\"inline\">self.buttons[index].config(text=\"\")</code> сотрёт уже "
        "СДЕЛАННЫЙ ход, если игрок наводит мышь на занятую клетку каким-то другим путём — "
        "Debug Lab 16 (раздел 17.29) разбирает это подробно. Правильный код всегда "
        "перерисовывает из модели, а не гадает, что стереть.",
    )}

    <h2>Доказательство: модель не меняется</h2>
    {code_block(
        "hover_ne_menyaet_model.py",
        "assert app.state.board[4] == \"\"\n"
        "app.on_cell_enter(4)\n"
        "assert app.state.board[4] == \"\"     # ПОСЛЕ наведения — всё ещё пусто\n"
        "app.on_cell_leave(4)\n"
        "assert app.state.board[4] == \"\"     # и после ухода курсора — тоже\n",
    )}

    {local_required_card(
        "17-23",
        "Практика: hover preview на реальном поле",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/17-23/index.html",
    )}
    """
    out = render_page(
        page_title="Hover preview через bind()",
        description="Реализация наведения-превью на пустую клетку и доказательство, что оно никогда не меняет игровую модель.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Hover preview", "")],
        kicker="Глава 17 · Интерфейс игры",
        h1="Hover preview через bind()",
        lede="Показать возможный ход — не значит его сделать. Именно этот эффект доказывает, "
        "зачем нужна модель.",
        body_html=body,
        sidebar_groups=sidebar("17-23-hover-preview.html"),
        nav=PageNav(prev_href="17-22-vizualnyj-stil.html", prev_label="Визуальный стиль X/O", next_href="17-24-upravlenie-klaviaturoj.html", next_label="Управление клавиатурой"),
    )
    write("17-23-hover-preview.html", out)


def build_24() -> None:
    body = f"""
    <h2>Мышь и клавиатура сходятся в одной точке</h2>
    {converge_diagram(["Button command (клик)", "клавиатурная привязка (1-9)"], "attempt_move(index)", caption="Оба пути ведут в ОДНУ И ТУ ЖЕ функцию — правила не дублируются.")}
    {code_block(
        "keyboard_control.py",
        "def on_key(self, event):\n"
        "    if event.keysym in (\"r\", \"R\"):\n"
        "        self.new_round()\n"
        "        return\n"
        "    if event.char and event.char.isdigit():\n"
        "        n = int(event.char)\n"
        "        if 1 <= n <= 9:\n"
        "            self.attempt_move(n - 1)   # клавиша 1 -> индекс 0, ... 9 -> индекс 8\n",
    )}
    {callout(
        "warning",
        "Клавиатура не получает свою копию правил",
        "Обработчик клавиатуры ТОЛЬКО переводит нажатую клавишу в номер клетки и зовёт "
        "<code class=\"inline\">attempt_move()</code> — ту же функцию, что вызывает клик "
        "мышью. Если бы клавиатурный путь копировал проверку победителя отдельно, два набора "
        "правил рано или поздно разошлись бы (Debug Lab 12, раздел 17.29 — похожая ошибка с "
        "опечаткой в линии).",
    )}
    <table class="compare-table">
      <thead><tr><th>Клавиша</th><th>Индекс клетки</th></tr></thead>
      <tbody>
        {"".join(f"<tr><td>{n}</td><td>{n - 1}</td></tr>" for n in range(1, 10))}
      </tbody>
    </table>
    {callout(
        "info",
        "keysym против char — здесь выбран char",
        "Раздел 17.8 показал разницу: <code class=\"inline\">event.char</code> — фактический "
        "введённый символ. Для цифровых клавиш верхнего ряда он предсказуемо равен самой цифре; "
        "с дополнительной цифровой клавиатурой (NumPad) поведение обычно совпадает, если "
        "включён NumLock, но может отличаться в зависимости от платформы, раскладки и состояния "
        "NumLock — если клавиатура важна для вашего проекта, проверьте оба варианта на целевой "
        "системе. Здесь <code class=\"inline\">event.char</code> всё равно удобнее, чем "
        "сравнение по <code class=\"inline\">event.keysym</code>.",
    )}

    {local_required_card(
        "17-24",
        "Практика: клавиши 1-9 и R",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/17-24/index.html",
    )}
    """
    out = render_page(
        page_title="Управление клавиатурой",
        description="Клавиши 1-9 ведут в тот же attempt_move(), что и клик мышью — мышь и клавиатура сходятся в одном пути, не дублируя правила.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Управление клавиатурой", "")],
        kicker="Глава 17 · Интерфейс игры",
        h1="Управление клавиатурой",
        lede="1-9 — те же ходы, что и клик мышью, через тот же самый код.",
        body_html=body,
        sidebar_groups=sidebar("17-24-upravlenie-klaviaturoj.html"),
        nav=PageNav(prev_href="17-23-hover-preview.html", prev_label="Hover preview", next_href="17-25-podsvetka-linii.html", next_label="Подсветка выигрышной линии"),
    )
    write("17-24-upravlenie-klaviaturoj.html", out)


def build_25() -> None:
    body = f"""
    <h2>Данные о линии ведут к подсветке</h2>
    {pipeline_diagram([
        {"kind": "plain", "title": "find_winner(board)"},
        {"kind": "object", "title": "('X', (0, 4, 8))"},
        {"kind": "plain", "title": "state.winning_line = (0, 4, 8)"},
        {"kind": "plain", "title": "render()"},
        {"kind": "object", "title": "buttons[0], [4], [8] — зелёный фон"},
    ], caption="Модель определяет, КАКИЕ клетки победили — render() их просто красит.")}
    {code_block(
        "podsvetka_linii.py",
        "for index, btn in enumerate(self.buttons):\n"
        "    is_win_cell = state.winning_line is not None and index in state.winning_line\n"
        "    btn.config(bg=WIN_BG if is_win_cell else NEUTRAL_BG)\n",
    )}
    {callout(
        "warning",
        "Подсвечиваем ИМЕННО линию — не любые совпавшие символы",
        "Если на поле есть, скажем, четыре «X», но победили только три из них по диагонали — "
        "подсвечивается СТРОГО <code class=\"inline\">winning_line</code>, а не каждая клетка "
        "с меткой «X». Проверка <code class=\"inline\">index in state.winning_line</code> "
        "гарантирует это.",
    )}
    {image_figure(f"{IMG}/winning-highlight.png", "Диагональ 0-4-8 подсвечена зелёным, статус говорит Победил игрок X", f"Реальное окно полной версии игры: победная диагональ подсвечена, буквы остаются видимыми. Фрагмент выше — это только код самой подсветки, а не весь путь до победы.", width=320)}

    {practice_card(
        "17-25",
        "Практика: подсветка выигрышной линии",
        "Автоматическая проверка — вычисляем, какие клетки должны подсветиться, на чистых данных",
        "../../practice/17-25/index.html",
    )}
    """
    out = render_page(
        page_title="Подсветка выигрышной линии",
        description="Как winning_line из find_winner() определяет, какие именно клетки подсветить в render().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Подсветка победной линии", "")],
        kicker="Глава 17 · Интерфейс игры",
        h1="Подсветка выигрышной линии",
        lede="Модель уже знает, какие три клетки победили — render() их просто красит.",
        body_html=body,
        sidebar_groups=sidebar("17-25-podsvetka-linii.html"),
        nav=PageNav(prev_href="17-24-upravlenie-klaviaturoj.html", prev_label="Управление клавиатурой", next_href="17-26-schyot-matchej.html", next_label="Счёт матчей"),
    )
    write("17-25-podsvetka-linii.html", out)


def build_26() -> None:
    body = f"""
    <h2>Счёт живёт в GameState, не в отдельной переменной где попало</h2>
    {image_figure(f"{IMG}/scoreboard.png", "Строка счёта: X: 2, O: 1, Ничьи: 1", f"Реальное окно полной версии игры: счёт матча под игровым полем. Фрагмент ниже показывает, как значения счёта попадают в эту строку.", width=320)}
    {code_block(
        "schet.py",
        "if winner == \"X\":\n"
        "    state.score_x += 1\n"
        "else:\n"
        "    state.score_o += 1\n\n"
        "self.score_var.set(f\"X: {state.score_x}  |  O: {state.score_o}  |  Ничьи: {state.draws}\")\n",
    )}
    {callout(
        "warning",
        "Осторожно с редким символом-разделителем в Tkinter-метках",
        "Красивый символ вроде типографской точки «•» иногда рендерится испорченным набором "
        "символов в headless-окружениях с ограниченным набором шрифтов — как выяснилось при "
        "подготовке скриншотов этой самой главы. Простой ASCII-разделитель "
        "<code class=\"inline\">\" | \"</code> работает предсказуемо везде.",
    )}
    <p>Счёт увеличивается ровно один раз за партию — внутри <code class="inline">attempt_move()</code>,
    сразу после того как найден победитель или зафиксирована ничья, а не где-то ещё.</p>

    {practice_card(
        "17-26",
        "Практика: учёт счёта матча",
        "Автоматическая проверка — чистые функции обновления счёта по результату раунда",
        "../../practice/17-26/index.html",
    )}
    """
    out = render_page(
        page_title="Счёт матчей",
        description="Счёт X/O/ничьих как часть GameState, и практический урок про надёжные ASCII-разделители в Tkinter-метках.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Счёт матчей", "")],
        kicker="Глава 17 · Раунды и матчи",
        h1="Счёт матчей",
        lede="Партия заканчивается — матч продолжается: счёт живёт дольше одного раунда.",
        body_html=body,
        sidebar_groups=sidebar("17-26-schyot-matchej.html"),
        nav=PageNav(prev_href="17-25-podsvetka-linii.html", prev_label="Подсветка победной линии", next_href="17-27-new-round-vs-new-match.html", next_label="New Round vs New Match"),
    )
    write("17-26-schyot-matchej.html", out)


def build_27() -> None:
    body = f"""
    <h2>Два разных «сброса» — и это не одно и то же</h2>
    {comparison_table(
        ["New Round (новый раунд)", "New Match (новый матч)"],
        [
            ["Очищает поле, текущего игрока, game_over, winner, winning_line", "Делает всё то же, что New Round"],
            ["СОХРАНЯЕТ счёт (score_x, score_o, draws)", "И ДОПОЛНИТЕЛЬНО обнуляет счёт"],
            ["Вызывается после каждой партии", "Вызывается, когда матч целиком завершён"],
        ],
    )}
    {code_block(
        "new_round_vs_new_match.py",
        "def new_round(self):\n"
        '    self.state.board = [""] * 9\n'
        '    self.state.current_player = "X"\n'
        "    self.state.game_over = False\n"
        "    self.state.winner = None\n"
        "    self.state.winning_line = None\n"
        "    self.render()\n\n"
        "def new_match(self):\n"
        "    self.state.score_x = 0\n"
        "    self.state.score_o = 0\n"
        "    self.state.draws = 0\n"
        "    self.new_round()   # New Match полностью включает в себя New Round\n",
    )}
    {callout(
        "warning",
        "Перепутать их — реальная ошибка (Debug Lab 15, раздел 17.29)",
        "Если кнопка «Новая игра» вызывает то, что обнуляет счёт — игроки теряют турнирный "
        "счёт после каждой партии. Если кнопка «Новый матч» не обнуляет счёт — старый счёт "
        "тянется в новый турнир. Названия функций должны отражать это различие однозначно.",
    )}
    {image_figure(f"{IMG}/new-round.png", "Поле пустое, статус Ход игрока X, но счёт X:1 O:0 сохранён", f"Реальное окно полной версии игры: раунд сброшен после победы X, но счёт матча остался. Фрагмент выше показывает функции new_round()/new_match(), которые за это отвечают.", width=320)}

    <h2>Необязательное расширение: сохраняем счёт матча в JSON</h2>
    <p>Ниже показан только фрагмент — тело функции <code class="inline">save_scores()</code> из
    <code class="inline">tic_tac_toe.py</code>. Полный файл уже содержит нужные
    <code class="inline">import json</code>, <code class="inline">from pathlib import Path</code>
    и определение <code class="inline">GameState</code> — здесь они не повторяются.</p>
    {code_block(
        "фрагмент save_scores() из tic_tac_toe.py",
        'SCORES_PATH = Path("tic_tac_toe_scores.json")   # относительно текущей рабочей директории\n\n'
        "def save_scores(state):\n"
        '    with SCORES_PATH.open("w", encoding="utf-8") as f:\n'
        '        json.dump({"x": state.score_x, "o": state.score_o, "draws": state.draws}, f,\n'
        "                  ensure_ascii=False, indent=2)\n",
    )}
    {callout(
        "info",
        "Необязательно для первой играющей версии",
        "Персистентный счёт — приятное расширение (глава 15: <code class=\"inline\">pathlib</code> "
        "+ JSON), но НЕ требование для рабочей игры. В <code class=\"inline\">tic_tac_toe.py</code> "
        "это включается явным флагом <code class=\"inline\">persist_scores=True</code> — по "
        "умолчанию выключено.",
    )}

    {practice_card(
        "17-27",
        "Практика: New Round, New Match и сохранение счёта",
        "Автоматическая проверка — семантика сброса раунда/матча и сохранение JSON на виртуальной файловой системе браузера",
        "../../practice/17-27/index.html",
    )}
    """
    out = render_page(
        page_title="New Round vs New Match",
        description="Чёткое различие между сбросом раунда и сбросом матча, и необязательное сохранение счёта в JSON.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("New Round vs New Match", "")],
        kicker="Глава 17 · Раунды и матчи",
        h1="New Round vs New Match",
        lede="«Новая игра» — это раунд или матч целиком? В этой игре — принципиально разные "
        "вещи.",
        body_html=body,
        sidebar_groups=sidebar("17-27-new-round-vs-new-match.html"),
        nav=PageNav(prev_href="17-26-schyot-matchej.html", prev_label="Счёт матчей", next_href="17-28-testiruem-bez-tkinter.html", next_label="Тестируем без Tkinter"),
    )
    write("17-27-new-round-vs-new-match.html", out)


def build_28() -> None:
    body = f"""
    <h2>Почему чистая логика легко тестируется</h2>
    {code_block(
        "test_bez_okna.py",
        'board = ["X", "X", "X", "", "", "", "", "", ""]\n'
        "winner, line = find_winner(board)\n"
        'assert winner == "X"\n'
        "# Ни одного открытого окна Tkinter — просто список строк и обычная функция.\n",
    )}
    {callout(
        "tip",
        "Прямая награда за архитектуру раздела 17.20",
        "Это возможно именно потому, что <code class=\"inline\">find_winner</code>/"
        "<code class=\"inline\">is_draw</code> ничего не знают про Tkinter. Если бы победитель "
        "определялся прямо внутри обработчика клика по кнопке — тестировать пришлось бы через "
        "настоящее окно и настоящие клики.",
    )}

    <h2>Полная тестовая матрица игры</h2>
    {comparison_table(
        ["Проверка", "Ожидаемый результат"],
        [
            ["X выигрывает все 8 линий", "find_winner возвращает ('X', линия) для каждой"],
            ["O выигрывает все 8 линий", "find_winner возвращает ('O', линия) для каждой"],
            ["Пустое/неполное поле", "find_winner возвращает (None, None)"],
            ["Известная ничья", "is_draw(board) is True"],
            ["Последний ход одновременно выигрывает", "find_winner побеждает, is_draw is False"],
            ["Ход в занятую клетку", "attempt_move ничего не меняет, current_player тот же"],
            ["Ход после game_over", "attempt_move ничего не меняет"],
            ["new_round()", "поле пустое, game_over=False, счёт СОХРАНЁН"],
            ["new_match()", "то же самое, но счёт ОБНУЛЁН"],
        ],
    )}
    {callout(
        "warning",
        "Проверяйте все восемь линий, а не одну строку наугад",
        "Тест только для одной строки не поймает опечатку в описании диагонали — Debug Lab 12 "
        "(раздел 17.29) устроен именно так, чтобы одна строка теста его бы не заметила.",
    )}

    {practice_card(
        "17-28",
        "Практика: полный набор тестов без Tkinter",
        "Автоматическая проверка — вся регрессионная матрица игры: 8 линий × 2 игрока, ничья, последний ход, невалидный ход, сброс",
        "../../practice/17-28/index.html",
    )}
    """
    out = render_page(
        page_title="Тестируем игру без Tkinter",
        description="Полная тестовая матрица игровой логики: все 8 линий для обоих игроков, ничья, последний ход, невалидные ходы, сброс — без единого открытого окна.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Тестируем без Tkinter", "")],
        kicker="Глава 17 · Тестирование",
        h1="Тестируем игру без Tkinter",
        lede="Чистая логика — прямая награда за архитектуру: тестируем правила игры без единого "
        "открытого окна.",
        body_html=body,
        sidebar_groups=sidebar("17-28-testiruem-bez-tkinter.html"),
        nav=PageNav(prev_href="17-27-new-round-vs-new-match.html", prev_label="New Round vs New Match", next_href="17-29-debug-labs.html", next_label="Debug Labs"),
    )
    write("17-28-testiruem-bez-tkinter.html", out)


def build_29() -> None:
    body = f"""
    <p>Небольшая коллекция типичных ошибок событийно-управляемых игр — каждая с симптомом и
    исправлением. Часть из них вы уже видели раньше в главе; здесь они собраны как справочник.</p>

    {debug_lab(
        4,
        "Своя привязка виджета с break глушит клавиши игры",
        "focus_problem.py",
        "root.bind(\"<Key>\", on_key)\n\n"
        "entry = tk.Entry(root)\n"
        "entry.pack()\n"
        "entry.bind(\"<Key>\", lambda e: \"break\")   # останавливает цепочку bindtags\n"
        "entry.focus_set()\n",
        ["# Пока фокус в entry, нажатия цифр не долетают до on_key —", "# entry.bind(..., 'break') обрывает цепочку прямо здесь."],
        "Клавиатурное событие сначала идёт в сфокусированный виджет и дальше по цепочке "
        "bindtags: сам виджет → его класс → root → \"all\" (раздел 17.11). Если КАКОЙ-ТО "
        "обработчик на этом пути явно вернёт <code class=\"inline\">\"break\"</code> — "
        "дальнейшие привязки в цепочке (включая <code class=\"inline\">root.bind</code>) для "
        "этого события просто не вызовутся. Без такого <code class=\"inline\">\"break\"</code> "
        "событие обычно продолжило бы путь и до <code class=\"inline\">root</code> тоже — фокус "
        "сам по себе не блокирует привязку верхнего уровня.",
        "focus_fixed.py",
        "root.bind(\"<Key>\", on_key)\n\n"
        "entry = tk.Entry(root)\n"
        "entry.pack()\n"
        "entry.focus_set()   # без своей <Key>-привязки событие доходит и до root\n",
    )}

    {debug_lab(
        5,
        "lambda без i=indeks — поздняя привязка",
        "lambda_pozdnyaya_privyazka.py",
        "for indeks in range(9):\n"
        "    btn = tk.Button(frame, command=lambda: attempt_move(indeks))\n"
        "    btn.grid(row=indeks // 3, column=indeks % 3)\n",
        ["# Клик по ЛЮБОЙ из девяти кнопок ставит отметку в клетку 8 —", "# потому что все lambda читают ОДНУ И ТУ ЖЕ переменную indeks."],
        "К моменту клика цикл давно закончился, и <code class=\"inline\">indeks</code> равен "
        "8 для всех девяти замыканий разом — они не «запомнили» значение на момент создания, "
        "они ссылаются на переменную. Раздел 17.4 разбирал именно эту ошибку.",
        "lambda_fixed.py",
        "for indeks in range(9):\n"
        "    btn = tk.Button(frame, command=lambda i=indeks: attempt_move(i))\n"
        "    btn.grid(row=indeks // 3, column=indeks % 3)\n",
    )}

    {debug_lab(
        6,
        "Наведение путает превью с настоящим ходом",
        "hover_kak_hod.py",
        "def on_cell_enter(self, index):\n"
        "    self.buttons[index].config(text=self.state.current_player)\n\n"
        "def find_winner_from_widgets(self):\n"
        '    board = [b["text"] for b in self.buttons]   # читает ТЕКСТ КНОПОК\n'
        "    return find_winner(board)\n",
        ["# Просто наведя курсор на три пустые клетки одной линии подряд,", "# можно получить объявление победы без единого клика."],
        "Если проверка победителя читает состояние из <code class=\"inline\">button[\"text\"]</code>, "
        "а наведение временно пишет туда текст — превью становится неотличимо от настоящего "
        "хода. Раздел 17.18 объясняет, почему модель обязана быть источником истины.",
        "hover_ne_hod.py",
        "def on_cell_enter(self, index):\n"
        "    if self.state.game_over or self.state.board[index]:\n"
        "        return\n"
        "    self.buttons[index].config(text=self.state.current_player, fg=HOVER_COLOR)\n\n"
        "def find_winner_call(self):\n"
        "    return find_winner(self.state.board)   # читает МОДЕЛЬ, не кнопки\n",
    )}

    {debug_lab(
        7,
        "Игрок переключается ДО проверки победителя",
        "smena_do_proverki.py",
        "state.board[index] = state.current_player\n"
        'state.current_player = "O" if state.current_player == "X" else "X"\n\n'
        "winner, line = find_winner(state.board)\n"
        "if winner:\n"
        '    status_var.set(f"Победил игрок {winner}!")   # но current_player уже сменился\n',
        ["# Статус верный ('Победил X'), но если где-то дальше по коду", "# используется state.current_player как 'кто только что выиграл' — там уже 'O'."],
        "Порядок операций важен: смена игрока должна произойти ПОСЛЕ проверки победителя и "
        "ТОЛЬКО если игра продолжается. Иначе любой код, который смотрит на "
        "<code class=\"inline\">current_player</code> сразу после хода, увидит уже "
        "следующего игрока, а не автора выигрышного хода.",
        "smena_posle_proverki.py",
        "state.board[index] = state.current_player\n"
        "winner, line = find_winner(state.board)\n"
        "if winner:\n"
        "    state.winner = winner   # 'кто выиграл' зафиксировано ДО смены игрока\n"
        "    state.game_over = True\n"
        "elif not is_draw(state.board):\n"
        '    state.current_player = "O" if state.current_player == "X" else "X"\n',
    )}

    {debug_lab(
        8,
        "Ничья проверяется раньше победы",
        "nichya_do_pobedy.py",
        "if all(state.board):\n"
        '    status_var.set("Ничья!")\n'
        "elif find_winner(state.board)[0]:\n"
        '    status_var.set("Победа!")\n',
        ["# Девятый ход одновременно заполняет поле и выигрывает диагональ —", "# программа объявляет 'Ничья!', хотя есть явный победитель."],
        "Раздел 17.17 показывал именно этот сценарий. Проверка «заполнено ли поле» должна идти "
        "ПОСЛЕ проверки победителя, иначе выигрышный последний ход теряется за ложной ничьей.",
        "pobeda_do_nichyej.py",
        "winner, line = find_winner(state.board)\n"
        "if winner:\n"
        '    status_var.set(f"Победил игрок {winner}!")\n'
        "elif all(state.board):\n"
        '    status_var.set("Ничья!")\n',
    )}

    {debug_lab(
        9,
        "Ход в занятую клетку разрешён",
        "zanyataya_kletka.py",
        "def attempt_move(index):\n"
        "    state.board[index] = state.current_player   # нет проверки!\n",
        ["# Повторный клик по уже занятой клетке перезаписывает X на O", "# (или наоборот) — чужой ход стирается."],
        "Валидация должна идти ПЕРВОЙ строкой, до любого изменения состояния — раздел 17.15 "
        "формулирует это как обязательный первый шаг алгоритма хода.",
        "zanyataya_kletka_fixed.py",
        "def attempt_move(index):\n"
        "    if state.game_over or state.board[index]:\n"
        "        return\n"
        "    state.board[index] = state.current_player\n",
    )}

    {debug_lab(
        10,
        "Игрок переключается даже при невалидном клике",
        "smena_pri_nevalidnom_klike.py",
        "def attempt_move(index):\n"
        "    if not state.board[index]:\n"
        "        state.board[index] = state.current_player\n"
        '    state.current_player = "O" if state.current_player == "X" else "X"   # снаружи if!\n',
        ["# Клик по занятой клетке ничего не рисует —", "# но ход всё равно передаётся сопернику. Игрок теряет очередь ни за что."],
        "Строка смены игрока оказалась ВНЕ блока <code class=\"inline\">if</code> — она "
        "выполняется независимо от того, был ли ход валидным. Раздел 17.15: невалидный ход не "
        "должен переключать игрока.",
        "smena_pri_nevalidnom_klike_fixed.py",
        "def attempt_move(index):\n"
        "    if state.board[index]:\n"
        "        return\n"
        "    state.board[index] = state.current_player\n"
        '    state.current_player = "O" if state.current_player == "X" else "X"\n',
    )}

    {debug_lab(
        11,
        "Нет проверки game_over — игра продолжается после победы",
        "net_game_over.py",
        "def attempt_move(index):\n"
        "    if state.board[index]:\n"
        "        return\n"
        "    state.board[index] = state.current_player\n"
        "    # ... проверка победителя, но НЕТ return/guard в начале функции\n",
        ["# После объявления победы X можно продолжать кликать по пустым клеткам —", "# и даже 'перезаписать' исход партии дополнительными ходами O."],
        "Без явной проверки <code class=\"inline\">state.game_over</code> в начале "
        "<code class=\"inline\">attempt_move()</code> ничего не мешает продолжать партию "
        "после того, как она уже закончилась.",
        "game_over_guard.py",
        "def attempt_move(index):\n"
        "    if state.game_over or state.board[index]:\n"
        "        return\n"
        "    ...\n",
    )}

    {debug_lab(
        12,
        "Опечатка в WINNING_LINES",
        "opechatka_v_linii.py",
        "WINNING_LINES = (\n"
        "    (0, 1, 2), (3, 4, 5), (6, 7, 8),\n"
        "    (0, 3, 6), (1, 4, 7), (2, 5, 8),\n"
        "    (0, 4, 6), (2, 4, 6),   # первая диагональ должна быть (0, 4, 8)!\n"
        ")\n",
        ["# X ставит 0, 4 и 8 — три подряд по настоящей диагонали —", "# но игра не объявляет победителя, потому что такой кортеж не в списке."],
        "Опечатка тихая: код синтаксически верный и даже проходит поверхностный тест на "
        "«какая-то» диагональ. Только регрессионный тест, проверяющий ВСЕ восемь линий "
        "(раздел 17.28), поймал бы конкретно эту ошибку.",
        "linii_fixed.py",
        "WINNING_LINES = (\n"
        "    (0, 1, 2), (3, 4, 5), (6, 7, 8),\n"
        "    (0, 3, 6), (1, 4, 7), (2, 5, 8),\n"
        "    (0, 4, 8), (2, 4, 6),\n"
        ")\n",
    )}

    {debug_lab(
        13,
        "Сбросили интерфейс, но не модель",
        "reset_tolko_ui.py",
        "def new_round(self):\n"
        "    for btn in self.buttons:\n"
        '        btn.config(text="")   # кнопки очищены...\n'
        "    # ...но self.state.board по-прежнему хранит старые X/O!\n",
        ["# Поле выглядит пустым, но следующий attempt_move()", "# натыкается на 'клетка уже занята' там, где на экране пусто."],
        "Визуальный сброс — не то же самое, что сброс модели. Раздел 17.18: кнопки лишь "
        "отображают состояние; если очистить только их, модель продолжает врать об истинном "
        "состоянии партии.",
        "reset_model_i_ui.py",
        "def new_round(self):\n"
        '    self.state.board = [""] * 9\n'
        '    self.state.current_player = "X"\n'
        "    self.state.game_over = False\n"
        "    self.render()   # UI обновляется ИЗ модели, а не отдельно\n",
    )}

    {debug_lab(
        14,
        "Сбросили модель, но не вызвали render()",
        "reset_tolko_model.py",
        "def new_round(self):\n"
        '    self.state.board = [""] * 9\n'
        '    self.state.current_player = "X"\n'
        "    self.state.game_over = False\n"
        "    # забыли self.render() в конце!\n",
        ["# Модель для нового раунда готова правильно —", "# но на экране всё ещё видны старые X и O из прошлой партии."],
        "Обратная сторона той же ошибки: без вызова <code class=\"inline\">render()</code> "
        "изменения модели никогда не попадают на экран. Раздел 17.20 формулирует этот принцип: "
        "<code class=\"inline\">render()</code> — место, которое рисует виджеты ИЗ модели "
        "(state), и его нужно вызывать явно после каждого изменения этой модели.",
        "reset_s_render.py",
        "def new_round(self):\n"
        '    self.state.board = [""] * 9\n'
        '    self.state.current_player = "X"\n'
        "    self.state.game_over = False\n"
        "    self.render()\n",
    )}

    {debug_lab(
        15,
        "«Новая игра» случайно обнуляет счёт матча",
        "novaya_igra_obnulyaet_schet.py",
        "def new_round(self):\n"
        "    self.state.score_x = 0   # это должно быть только в new_match()!\n"
        "    self.state.score_o = 0\n"
        '    self.state.board = [""] * 9\n',
        ["# После каждой победы счёт тут же обнуляется —", "# турнирный счёт невозможно накопить."],
        "Раздел 17.27: New Round и New Match — разные операции. Обнуление счёта принадлежит "
        "ИСКЛЮЧИТЕЛЬНО <code class=\"inline\">new_match()</code>.",
        "new_round_bez_scheta.py",
        "def new_round(self):\n"
        '    self.state.board = [""] * 9\n'
        "    # счёт (score_x/score_o/draws) здесь не трогаем\n",
    )}

    {debug_lab(
        16,
        "on_cell_leave стирает уже сделанный ход",
        "leave_stiraet_hod.py",
        "def on_cell_leave(self, index):\n"
        '    self.buttons[index].config(text="")   # наивно "убрать превью"\n',
        ["# После того как игрок делает настоящий ход и потом уводит курсор,", "# отметка на клетке пропадает с экрана — хотя в модели ход остался."],
        "<code class=\"inline\">on_cell_leave</code> не знает, было ли на клетке превью или "
        "настоящий ход — он просто стирает текст безусловно. Правильный подход: не гадать, а "
        "перерисовать из модели, которая точно знает истину.",
        "leave_fixed.py",
        "def on_cell_leave(self, index):\n"
        "    self.render()   # модель решает, что должно быть на клетке\n",
    )}

    {debug_lab(
        17,
        "event.widget используется как игровое состояние",
        "widget_kak_state.py",
        "def on_click(self, event):\n"
        "    event.widget.config(text=self.state.current_player)\n"
        "    # где здесь запись в board? Её нет — состояние живёт ТОЛЬКО в виджете\n",
        ["# find_winner(self.state.board) никогда не видит эти ходы —", "# победа не определяется, потому что модель не менялась."],
        "<code class=\"inline\">event.widget</code> — источник UI-события (раздел 17.8), а не "
        "домен игры. Запись хода обязана попасть в <code class=\"inline\">state.board</code>, "
        "иначе вся доменная логика (поиск победителя, ничьей) работает вслепую.",
        "widget_i_model.py",
        "def on_click(self, event, index):\n"
        "    self.attempt_move(index)   # меняет state.board, потом render()\n",
    )}

    {debug_lab(
        18,
        "Голый <Button-1> вместо command= ломает клавиатурную активацию",
        "goloj_button1.py",
        'btn.bind("<Button-1>", lambda e, i=index: attempt_move(i))\n'
        "# command= не задан вообще\n",
        ["# Мышь работает нормально.", "# Но Tab + Enter/пробел на сфокусированной кнопке — ничего не делает."],
        "Раздел 17.10: <code class=\"inline\">command=</code> — семантическая активация, "
        "которая срабатывает и по клику, и по клавиатуре у сфокусированного виджета. Голая "
        "привязка мыши реагирует ТОЛЬКО на клик — доступность с клавиатуры молча теряется.",
        "command_fixed.py",
        "btn.config(command=lambda i=index: attempt_move(i))\n",
    )}

    {debug_lab(
        19,
        "time.sleep() в анимации победы замораживает окно",
        "sleep_v_animacii.py",
        "import time\n\n"
        "def pulse_winning_line(self):\n"
        "    for _ in range(6):\n"
        '        self.buttons[0].config(bg="green")\n'
        "        time.sleep(0.15)\n"
        '        self.buttons[0].config(bg="white")\n'
        "        time.sleep(0.15)\n",
        ["# Окно перестаёт отвечать на весь почти секунду анимации —", "# та же ошибка, что и в главе 16 (раздел 16.32)."],
        "<code class=\"inline\">time.sleep()</code> блокирует событийный цикл целиком. Для "
        "анимации без блокировки нужен self-rescheduling через <code class=\"inline\">after()</code> "
        "— раздел 17.30.",
        "after_fixed.py",
        "def pulse_winning_line(self, tick=0):\n"
        "    color = PULSE_BG if tick % 2 == 0 else WIN_BG\n"
        "    for i in self.state.winning_line:\n"
        "        self.buttons[i].config(bg=color)\n"
        "    if tick < 5:\n"
        "        self.root.after(150, self.pulse_winning_line, tick + 1)\n",
    )}

    {debug_lab(
        20,
        "Дополнительный bind(..., add=\"+\") поверх command= вызывает reset дважды",
        "dublirovannaya_privyazka.py",
        'btn = ttk.Button(controls, text="Новый раунд", command=self.new_round)\n'
        "btn.bind(\"<Button-1>\", lambda e: self.new_round(), add=\"+\")\n"
        "# теперь один клик запускает new_round() ЧЕРЕЗ command И через bind — дважды подряд\n",
        ["# Само по себе new_round() дважды подряд не ломает игру —", "# но если бы это была, например, функция увеличения счёта, счёт скакнул бы на 2."],
        "<code class=\"inline\">add=\"+\"</code> добавляет ЕЩЁ ОДИН обработчик, не заменяя "
        "существующий (раздел 17.12 упоминал это как «чуть глубже»). Если один и тот же клик "
        "уже обрабатывается через <code class=\"inline\">command=</code>, дублирующая привязка "
        "через <code class=\"inline\">bind(..., add=\"+\")</code> на том же событии запускает "
        "логику повторно — используйте <code class=\"inline\">add=\"+\"</code> осознанно, "
        "только когда действительно нужно НЕСКОЛЬКО независимых обработчиков одного события.",
        "bez_dublirovaniya.py",
        'btn = ttk.Button(controls, text="Новый раунд", command=self.new_round)\n'
        "# и всё — одной привязки достаточно\n",
    )}

    {practice_card(
        "17-29",
        "Практика: находим баг по симптому",
        "Автоматическая проверка — для набора описанных симптомов выбираем правильную причину/исправление",
        "../../practice/17-29/index.html",
    )}
    """
    out = render_page(
        page_title="Debug Labs — типичные ошибки событийной игры",
        description="Семнадцать разобранных багов событийно-управляемой игры: фокус, поздняя привязка lambda, порядок проверок, hover-как-ход, дублирующиеся привязки и другие.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Debug Labs", "")],
        kicker="Глава 17 · Тестирование",
        h1="Debug Labs — типичные ошибки событийной игры",
        lede="Каждая ошибка здесь встречается в реальных студенческих проектах — научитесь "
        "узнавать симптом раньше, чем откроете отладчик.",
        body_html=body,
        sidebar_groups=sidebar("17-29-debug-labs.html"),
        nav=PageNav(prev_href="17-28-testiruem-bez-tkinter.html", prev_label="Тестируем без Tkinter", next_href="17-30-visual-effects-after.html", next_label="Visual effects и after()"),
    )
    write("17-29-debug-labs.html", out)


def build_30() -> None:
    body = f"""
    <h2>Один ненавязчивый эффект — не фреймворк анимации</h2>
    <p>После победы клетки выигрышной линии мягко мигают несколько раз — коротко и по делу,
    не превращая книгу в курс по анимации. На реальном окне это выглядит как краткий переход
    между базовой подсветкой победы и мягким accent-состоянием; сайт не может показать
    видео-анимацию, поэтому ниже — три реальных кадра, а локальное приложение переключает их
    через <code class="inline">after()</code>.</p>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;align-items:start">
      {image_figure(f"{IMG}/win-pulse-step-0.png", "Тик 0: выигрышная линия в мягком accent-цвете (PULSE_BG)", "Тик 0 — PULSE_BG", width=260)}
      {image_figure(f"{IMG}/win-pulse-step-1.png", "Тик 1: выигрышная линия в базовом цвете подсветки (WIN_BG)", "Тик 1 — WIN_BG", width=260)}
      {image_figure(f"{IMG}/win-pulse-final.png", "После завершения пульса: линия остаётся в базовом цвете подсветки", "После пульса — settled", width=260)}
    </div>
    <p style="text-align:center;font-size:14px;color:var(--color-text-muted,#6B6B7D);margin-top:4px">
    Эффект намеренно сдержанный — никакого резкого высококонтрастного мигания.</p>
    {code_block(
        "pulse_winning_line.py",
        "def pulse_winning_line(self, tick=0):\n"
        "    if not self.state.winning_line:\n"
        "        return\n"
        "    color = PULSE_BG if tick % 2 == 0 else WIN_BG\n"
        "    for index in self.state.winning_line:\n"
        "        self.buttons[index].config(bg=color)\n"
        "    if tick < 5:\n"
        "        self._pulse_job = self.root.after(150, self.pulse_winning_line, tick + 1)\n"
        "    else:\n"
        "        self._pulse_job = None\n",
    )}
    {callout(
        "info",
        "Самопланирующийся after() — знакомый приём из главы 16",
        "Та же техника self-rescheduling, что и в разделе 16.22: каждый вызов "
        "<code class=\"inline\">pulse_winning_line</code> сам планирует свой следующий тик "
        "через <code class=\"inline\">after()</code>, пока не достигнет предела — событийный "
        "цикл ни на миг не блокируется.",
    )}
    {callout(
        "warning",
        "Отменяйте запланированный after() при новом раунде",
        "Если игрок нажимает «Новый раунд» посреди анимации, недоделанный "
        "<code class=\"inline\">after()</code> может сработать уже на пустом поле нового "
        "раунда. <code class=\"inline\">cancel_pulse()</code> вызывает "
        "<code class=\"inline\">after_cancel()</code> перед сбросом — та же трёхсостояньевая "
        "дисциплина, что и у таймера в разделе 16.28.",
    )}
    {code_block(
        "cancel_pulse.py",
        "def cancel_pulse(self):\n"
        "    if self._pulse_job is not None:\n"
        "        self.root.after_cancel(self._pulse_job)\n"
        "        self._pulse_job = None\n",
    )}
    {callout(
        "tip",
        "Никакого time.sleep(), и эффект сознательно короткий",
        "Пауза между тиками — 150 мс, всего 6 тиков (меньше секунды) — достаточно, чтобы победа "
        "была замечена, не превращая её в бесконечную анимацию. Это не проверенная гарантия "
        "комфорта для всех пользователей: частое мигание — тема стандартов доступности "
        "(например, WCAG), и если ваш проект должен им соответствовать, частоту и длительность "
        "стоит проверять и настраивать целенаправленно, а не полагаться на цифры из примера.",
    )}

    {local_required_card(
        "17-30",
        "Практика: ненавязчивая анимация победы",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/17-30/index.html",
    )}
    """
    out = render_page(
        page_title="Visual effects и after()",
        description="Ненавязчивая неблокирующая анимация победной линии через self-rescheduling after() и корректная отмена через after_cancel().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Visual effects и after()", "")],
        kicker="Глава 17 · Финальные штрихи",
        h1="Visual effects и after()",
        lede="Один короткий, неблокирующий эффект — победа должна быть замечена, а не устроить "
        "дискотеку.",
        body_html=body,
        sidebar_groups=sidebar("17-30-visual-effects-after.html"),
        nav=PageNav(prev_href="17-29-debug-labs.html", prev_label="Debug Labs", next_href="17-31-tic-tac-toe-pro-itogi.html", next_label="Tic-Tac-Toe Pro — итоги главы"),
    )
    write("17-30-visual-effects-after.html", out)


def build_31() -> None:
    checklist_model = "".join(f"<li>{x}</li>" for x in [
        "поле (<code class=\"inline\">board</code>) отделено от виджетов",
        "текущий игрок — явное поле состояния",
        "terminal state (game_over/winner) — явное поле, а не вывод из виджетов",
    ])
    checklist_rules = "".join(f"<li>{x}</li>" for x in [
        "невалидные ходы отклоняются и не переключают игрока",
        "все 8 выигрышных линий протестированы для X и O",
        "ничья проверяется ПОСЛЕ победы",
    ])
    checklist_ui = "".join(f"<li>{x}</li>" for x in [
        "статус хода виден всегда",
        "победитель виден не только по цвету",
        "поле адаптивно к изменению размера окна",
        "клавиатура работает",
    ])
    checklist_arch = "".join(f"<li>{x}</li>" for x in [
        "callback-и короткие: валидация → модель → render",
        "чистые правила тестируются без окна",
        "render() — единственное место, где виджеты обновляются ИЗ модели",
    ])
    body = f"""
    <h2>Итоговая программа</h2>
    {image_figure(f"{IMG}/tic-tac-toe-pro.png", "Финальное окно Tic-Tac-Toe Pro с игрой в процессе и счётом X:1 O:2 Ничьи:1", f"Реальное окно финальной версии — модель, правила, счёт, подсветка и клавиатура вместе. Ниже — структура всего файла целиком, а не одного фрагмента.", width=340)}
    <p>Файл целиком, самодостаточный и без невидимых зависимостей от других уроков:</p>
    <p>📄 <a href="../../../projects/tkinter/tic-tac-toe/tic_tac_toe.py">projects/tkinter/tic-tac-toe/tic_tac_toe.py</a></p>
    {code_block(
        "tic_tac_toe.py — структура",
        "WINNING_LINES = (...)\n\n"
        "def find_winner(board): ...\n"
        "def is_draw(board): ...\n\n"
        "@dataclass\n"
        "class GameState:\n"
        "    ...\n\n"
        "class TicTacToeApp:\n"
        "    def __init__(self, root, *, persist_scores=False): ...\n"
        "    def build_ui(self): ...\n"
        "    def build_board(self, outer): ...\n"
        "    def attempt_move(self, index): ...\n"
        "    def on_cell_enter(self, index): ...\n"
        "    def on_cell_leave(self, index): ...\n"
        "    def on_key(self, event): ...\n"
        "    def render(self): ...\n"
        "    def new_round(self): ...\n"
        "    def new_match(self): ...\n"
        "    def pulse_winning_line(self, tick=0): ...\n\n"
        "def main():\n"
        "    root = tk.Tk()\n"
        "    app = TicTacToeApp(root)\n"
        "    root.mainloop()\n\n"
        'if __name__ == "__main__":\n'
        "    main()\n",
    )}
    {callout(
        "tip",
        "Запустите игру у себя",
        "<code class=\"inline\">python tic_tac_toe.py</code> в терминале — либо кнопкой Run в "
        "VS Code или PyCharm. Сравните с <code class=\"inline\">tic_tac_toe_basic.py</code> "
        "(раздел 17.6) — тот же результат для игрока, совершенно другая внутренняя "
        "архитектура.",
    )}

    <h2>Чек-лист готовой игры</h2>
    <div class="capability-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin:24px 0">
      <div style="background:var(--color-bg-canvas,#fff);border:1.5px solid var(--color-border-default,#E4E1F5);border-radius:16px;padding:16px 18px">
        <div style="font-family:Sora,sans-serif;font-weight:700;color:#5B24F9;margin-bottom:8px">MODEL</div>
        <ul style="margin:0;padding-left:18px;font-size:14px;line-height:1.6">{checklist_model}</ul>
      </div>
      <div style="background:var(--color-bg-canvas,#fff);border:1.5px solid var(--color-border-default,#E4E1F5);border-radius:16px;padding:16px 18px">
        <div style="font-family:Sora,sans-serif;font-weight:700;color:#5B24F9;margin-bottom:8px">RULES</div>
        <ul style="margin:0;padding-left:18px;font-size:14px;line-height:1.6">{checklist_rules}</ul>
      </div>
      <div style="background:var(--color-bg-canvas,#fff);border:1.5px solid var(--color-border-default,#E4E1F5);border-radius:16px;padding:16px 18px">
        <div style="font-family:Sora,sans-serif;font-weight:700;color:#5B24F9;margin-bottom:8px">UI</div>
        <ul style="margin:0;padding-left:18px;font-size:14px;line-height:1.6">{checklist_ui}</ul>
      </div>
      <div style="background:var(--color-bg-canvas,#fff);border:1.5px solid var(--color-border-default,#E4E1F5);border-radius:16px;padding:16px 18px">
        <div style="font-family:Sora,sans-serif;font-weight:700;color:#5B24F9;margin-bottom:8px">АРХИТЕКТУРА</div>
        <ul style="margin:0;padding-left:18px;font-size:14px;line-height:1.6">{checklist_arch}</ul>
      </div>
    </div>

    <h2 id="most-k-glave-18">Мост к главе 18</h2>
    {callout(
        "info",
        "Дальше: КУДА, а не только КТО и ЧТО",
        "В этой игре события помогли нам понять, КТО действовал и ЧТО должно произойти. "
        "Дальше события мыши дадут нам ещё и КООРДИНАТЫ — <code class=\"inline\">event.x</code> "
        "и <code class=\"inline\">event.y</code>. В следующей главе координаты мыши станут "
        "основой рисования на Canvas.",
    )}

    {local_required_card(
        "17-31",
        "Практика: Tic-Tac-Toe Pro целиком",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/17-31/index.html",
    )}

    <h2 id="itogi-glavy">Итоги главы 17</h2>
    {summary_box("Что мы построили и чему научились", [
        "Событие, callback, command и binding — четыре разных, связанных понятия; "
        "command= обычно не передаёт event, bind() почти всегда передаёт.",
        "command= — семантическая активация (клик + клавиатура); bind() — для мыши, hover, "
        "низкоуровневых деталей. Замена одного другим «по умолчанию» — архитектурная ошибка.",
        "Игровое СОСТОЯНИЕ — не то же самое, что виджеты, которые его отображают: наведение "
        "мыши доказывает это нагляднее всего.",
        "find_winner(board) и is_draw(board) — чистые функции, тестируемые без единого "
        "открытого окна; порядок «сначала победа, потом ничья» — часть правил, а не деталь "
        "реализации.",
        "Мышь (command=) и клавиатура (bind на root) сходятся в одной функции attempt_move() "
        "— правила игры существуют только в одном месте.",
        "render() — единственное место, которое рисует виджеты ИЗ модели; модель меняют "
        "callback-и, виджеты только отображают её. Наведение мыши и пульс победы красят кнопки "
        "напрямую для временных эффектов — но каждый настоящий ход всё равно идёт через render().",
        "Ненавязчивые визуальные эффекты (hover-превью, подсветка линии, пульс победы) стоят "
        "на прочной архитектуре — они возможны именно потому, что модель отделена от вида.",
    ])}
    """
    out = render_page(
        page_title="Tic-Tac-Toe Pro — полная программа и итоги главы",
        description="Финальная архитектура игры целиком, чек-лист готовой игры, итоги главы 17 и мост к работе с координатами мыши в главе 18.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Tic-Tac-Toe Pro — итоги", "")],
        kicker="Глава 17 · Финальные штрихи",
        h1="Tic-Tac-Toe Pro — полная программа и итоги главы",
        lede="Та же игра, что и в разделе 17.6 — но теперь с моделью, правилами, тестами и "
        "архитектурой, которые выдержат рост проекта.",
        body_html=body,
        sidebar_groups=sidebar("17-31-tic-tac-toe-pro-itogi.html"),
        nav=PageNav(prev_href="17-30-visual-effects-after.html", prev_label="Visual effects и after()", next_href="../glava-18/index.html", next_label="Глава 18: Проект: приложение для рисования с Tkinter"),
    )
    write("17-31-tic-tac-toe-pro-itogi.html", out)


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
