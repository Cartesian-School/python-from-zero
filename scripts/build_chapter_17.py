#!/usr/bin/env python3
"""Строит Главу 17: «Проект: игра «Крестики-нолики» с Tkinter» (site/chapters/glava-17/)."""

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
    exercise,
    local_required_card,
    practice_card,
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-17"

PAGES = [
    ("index.html", "Обзор главы"),
    ("17-01-privyazka-sobytij.html", "Привязка событий"),
    ("17-02-obyasnenie-nastrojka.html", "Объяснение игры и настройка Tkinter"),
    ("17-03-peremennye-knopki.html", "Глобальные переменные и кнопки"),
    ("17-04-risuem-na-knopke.html", "При нажатии рисуем на кнопке"),
    ("17-05-proverka-pobedy.html", "Проверяем победу"),
    ("17-06-novaya-igra-itogi.html", "Новая игра, полная программа и итоги"),
]

LESSON_IDS = ["17-01", "17-03", "17-04", "17-05", "17-06"]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 17 · Крестики-нолики", items),
        SidebarGroup("Практика", [
            NavItem(f"🐍 {lid}: Практика", f"../../practice/{lid}/index.html") for lid in LESSON_IDS
        ]),
        SidebarGroup("Исходный код", [NavItem("🐍 tic_tac_toe.py", "../../../projects/tkinter/tic-tac-toe/tic_tac_toe.py")]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=17,
        baseline_page=369,
        title="Проект: игра «Крестики-нолики» с Tkinter",
        description="Первая полноценная игра книги — собираем её шаг за шагом, от привязки событий до готовой программы.",
        meta_items=["⏱ ~3 часа", "🎮 первая игра на Tkinter", "📓 5 ноутбуков практики"],
        sections=[
            ChapterSectionLink("17.1", "Привязка событий — делаем приложения динамическими!", "17-01-privyazka-sobytij.html", "369"),
            ChapterSectionLink("17.2", "Игра «Крестики-нолики» — объяснение", "17-02-obyasnenie-nastrojka.html", "372"),
            ChapterSectionLink("", "Настраиваем Tkinter", "17-02-obyasnenie-nastrojka.html#nastrojka", "373"),
            ChapterSectionLink("17.3", "Создаём глобальные переменные", "17-03-peremennye-knopki.html", "374"),
            ChapterSectionLink("", "Создаём кнопки", "17-03-peremennye-knopki.html#knopki", "376"),
            ChapterSectionLink("17.4", "При нажатии на кнопку рисуем на ней", "17-04-risuem-na-knopke.html", "378"),
            ChapterSectionLink("17.5", "Проверяем после каждого хода, победил ли игрок", "17-05-proverka-pobedy.html", "383"),
            ChapterSectionLink("17.6", "Кнопка новой игры", "17-06-novaya-igra-itogi.html", "385"),
            ChapterSectionLink("", "Полная программа", "17-06-novaya-igra-itogi.html#polnaya-programma", "387"),
            ChapterSectionLink("", "Итоги", "17-06-novaya-igra-itogi.html#itogi", "390"),
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
    <p>Функция-обработчик события всегда принимает один параметр — <code class="inline">event</code>
    — объект с подробностями о произошедшем событии: какая клавиша нажата
    (<code class="inline">event.keysym</code>), где кликнула мышь, и так далее.</p>

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

    <h2>Ничья</h2>
    <p>Если все девять клеток заполнены, а победителя нет — это ничья:</p>
    {code_block(
        "proverka_nichyej.py",
        "def polye_zapolneno():\n"
        '    return all(knopka["text"] != "" for knopka in polya)\n',
    )}

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
        nav=PageNav(prev_href="17-04-risuem-na-knopke.html", prev_label="Рисуем на кнопке", next_href="17-06-novaya-igra-itogi.html", next_label="Новая игра, полная программа и итоги"),
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

    <h2 id="polnaya-programma">Полная программа</h2>
    <p>Соберём все части в одну программу — она уже полностью проверена и доступна отдельным
    файлом в этой книге:</p>
    <p>📄 <a href="../../../projects/tkinter/tic-tac-toe/tic_tac_toe.py">projects/tkinter/tic-tac-toe/tic_tac_toe.py</a></p>
    {callout(
        "tip",
        "Запустите игру у себя",
        "Скачайте файл и запустите его через <code class=\"inline\">python tic_tac_toe.py</code> "
        "в терминале (глава 3) — либо кнопкой Run в VS Code или PyCharm.",
    )}

    {exercise(2, "Счёт побед", "Добавьте метки счёта побед X и O, увеличивайте нужный счётчик при каждой победе — счётчик не должен обнуляться кнопкой «Новая игра».")}
    {exercise(3, "Подсветка выигрышной линии", "Когда находится победитель, измените цвет фона трёх выигрышных кнопок — потребуется вернуть из proverit_pobedu() не только победителя, но и индексы линии.")}
{local_required_card(
        "17-06",
        "Практика: новая игра и полная программа",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/17-06/index.html",
    )}

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
        "<code class=\"inline\">.bind()</code> реагирует на любые события — не только клик "
        "по кнопке.",
        "Большие проекты строят по шагам: состояние → интерфейс → обработка событий → правила "
        "→ сброс.",
        "Лямбда с параметром по умолчанию (<code class=\"inline\">lambda i=indeks: ...</code>) "
        "«замораживает» значение переменной цикла в момент создания.",
        "Список кортежей — удобный способ описать несколько похожих проверок (восемь "
        "выигрышных линий) без повторения кода.",
        "У полноценной игры почти всегда есть способ начать заново, не перезапуская программу.",
    ])}
    """
    out = render_page(
        page_title="Кнопка новой игры и полная программа",
        description="Сброс игры кнопкой «Новая игра», ссылка на полный исходный код и итоги главы 17.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 17", "index.html"), ("Новая игра и итоги", "")],
        kicker="Глава 17 · Проект: «Крестики-нолики»",
        h1="Кнопка новой игры",
        lede="Финальный штрих — сброс игры без перезапуска программы — и полная работающая "
        "программа целиком.",
        body_html=body,
        sidebar_groups=sidebar("17-06-novaya-igra-itogi.html"),
        nav=PageNav(prev_href="17-05-proverka-pobedy.html", prev_label="Проверка победы", next_href="../glava-18/index.html", next_label="Глава 18: Проект: приложение для рисования с Tkinter"),
    )
    write("17-06-novaya-igra-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01()
    build_02()
    build_03()
    build_04()
    build_05()
    build_06()
