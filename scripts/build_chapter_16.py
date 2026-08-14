#!/usr/bin/env python3
"""Строит Главу 16: «Создаём классные приложения с Tkinter» (site/chapters/glava-16/)."""

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
    notebook_card,
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-16"

PAGES = [
    ("index.html", "Обзор главы"),
    ("16-01-nastraivaem-tkinter.html", "Tkinter — правильно всё настраиваем!"),
    ("16-02-metki-knopki-pack.html", "Метки, кнопки и pack"),
    ("16-03-polya-vvoda.html", "Поля ввода"),
    ("16-04-peremennye-tkinter.html", "Переменные Tkinter"),
    ("16-05-mnozhestvo-variantov.html", "Множество вариантов!"),
    ("16-06-menu.html", "Меню"),
    ("16-07-grid.html", "Идеальная компоновка — grid"),
    ("16-08-mini-proekt-chaevye-itogi.html", "Мини-проект: калькулятор чаевых и итоги"),
]

NOTEBOOKS = [
    "16-01-nastrojka.ipynb",
    "16-02-metki-knopki.ipynb",
    "16-03-polya-vvoda.ipynb",
    "16-04-peremennye.ipynb",
    "16-05-varianty.ipynb",
    "16-06-menu.ipynb",
    "16-07-grid.ipynb",
    "16-08-kalkulyator-chaevyh.ipynb",
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 16 · Tkinter", items),
        SidebarGroup("Практика", [NavItem(f"📓 {n}", f"../../../notebooks/chapter-16/{n}") for n in NOTEBOOKS]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=16,
        baseline_page=335,
        title="Создаём классные приложения с Tkinter",
        description="Настоящие оконные приложения с кнопками, полями ввода и меню — модуль Tkinter.",
        meta_items=["⏱ ~3–4 часа", "🖼️ модуль tkinter", "📓 8 ноутбуков практики"],
        sections=[
            ChapterSectionLink("16.1", "Tkinter — правильно всё настраиваем!", "16-01-nastraivaem-tkinter.html", "335"),
            ChapterSectionLink("16.2", "Метки, кнопки и их размещение", "16-02-metki-knopki-pack.html", "337"),
            ChapterSectionLink("", "Подробно о pack", "16-02-metki-knopki-pack.html#pack", "342"),
            ChapterSectionLink("16.3", "Множество полей ввода", "16-03-polya-vvoda.html", "348"),
            ChapterSectionLink("", "Одна строка текста. Строка за строкой", "16-03-polya-vvoda.html#tekst", "349"),
            ChapterSectionLink("16.4", "Переменные Tkinter", "16-04-peremennye-tkinter.html", "355"),
            ChapterSectionLink("16.5", "Множество вариантов!", "16-05-mnozhestvo-variantov.html", "357"),
            ChapterSectionLink("16.6", "Меню", "16-06-menu.html", "361"),
            ChapterSectionLink("16.7", "Идеальная компоновка — grid", "16-07-grid.html", "363"),
            ChapterSectionLink("16.8", "Мини-проект — приложение-калькулятор чаевых", "16-08-mini-proekt-chaevye-itogi.html", "365"),
            ChapterSectionLink("", "Итоги", "16-08-mini-proekt-chaevye-itogi.html#itogi", "367"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <p>До сих пор все программы либо выводили текст в терминал (главы 1–5, 8–15), либо рисовали
    на холсте Turtle (главы 6–7, 12). Пришло время настоящих <strong>оконных приложений</strong>
    с кнопками, полями ввода и меню — таких, как большинство привычных вам программ. Модуль для
    этого называется <code class="inline">Tkinter</code> и, как и <code class="inline">turtle</code>,
    входит в стандартную поставку Python.</p>

    {code_block(
        "pervoe_okno.py",
        "import tkinter as tk\n\n"
        "root = tk.Tk()\n"
        'root.title("Моё первое приложение")\n'
        'root.geometry("400x300")   # ширина x высота в пикселях\n\n'
        "root.mainloop()   # запускает приложение и ждёт действий пользователя\n",
    )}
    <p><code class="inline">tk.Tk()</code> создаёt главное окно приложения — примерно как
    <code class="inline">turtle.Screen()</code> создавал холст для рисования.
    <code class="inline">root.mainloop()</code> запускает <strong>цикл событий</strong>:
    программа «замирает» в ожидании действий пользователя (клика, ввода текста) и реагирует на
    них — и продолжает работать, пока окно не будет закрыто.</p>

    {callout(
        "info",
        "root — распространённое соглашение об имени",
        "Главное окно принято называть <code class=\"inline\">root</code> («корень») — это не "
        "обязательное правило языка, а широко принятое соглашение, которое вы увидите почти в "
        "любом примере с Tkinter.",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "16-01-nastrojka.ipynb · создаём первое окно",
        "../../../notebooks/chapter-16/16-01-nastrojka.ipynb",
    )}
    """
    out = render_page(
        page_title="Tkinter — правильно всё настраиваем!",
        description="Первое окно Tkinter: tk.Tk(), title(), geometry() и mainloop().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 16", "index.html"), ("Настройка Tkinter", "")],
        kicker="Глава 16 · Создаём классные приложения с Tkinter",
        h1="Tkinter — правильно всё настраиваем!",
        lede="Первое настоящее оконное приложение — с заголовком, размером и циклом событий.",
        body_html=body,
        sidebar_groups=sidebar("16-01-nastraivaem-tkinter.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="16-02-metki-knopki-pack.html", next_label="Метки, кнопки и pack"),
    )
    write("16-01-nastraivaem-tkinter.html", out)


def build_02() -> None:
    body = f"""
    <h2>Метки, кнопки и их размещение</h2>
    <p><strong>Метка</strong> (<code class="inline">Label</code>) показывает текст,
    <strong>кнопка</strong> (<code class="inline">Button</code>) реагирует на клик. Оба виджета
    сначала создаются, а затем <strong>размещаются</strong> в окне — отдельным действием:</p>
    {code_block(
        "metki_knopki.py",
        "import tkinter as tk\n\n"
        "root = tk.Tk()\n\n"
        'label = tk.Label(root, text="Привет, Tkinter!")\n'
        "label.pack()\n\n"
        "def na_knopku_nazhali():\n"
        '    print("Кнопку нажали!")\n\n'
        'button = tk.Button(root, text="Нажми меня", command=na_knopku_nazhali)\n'
        "button.pack()\n\n"
        "root.mainloop()\n",
    )}
    <p>Параметр <code class="inline">command</code> связывает кнопку с функцией — важно
    передать саму функцию, <strong>без скобок</strong>: <code class="inline">command=na_knopku_nazhali</code>,
    а не <code class="inline">command=na_knopku_nazhali()</code>.</p>

    {callout(
        "warning",
        "Частая ошибка: скобки в command",
        "<code class=\"inline\">command=na_knopku_nazhali()</code> вызовет функцию "
        "<strong>немедленно</strong>, один раз, при создании кнопки — а не при каждом клике. "
        "Кнопка свяжется с тем, что функция <em>вернёт</em>, а не с самой функцией.",
    )}

    <h2 id="pack">Подробно о pack</h2>
    <p><code class="inline">.pack()</code> — самый простой способ разместить виджет в окне.
    По умолчанию виджеты укладываются друг под другом сверху вниз, но есть полезные параметры:</p>
    {code_block(
        "pack_podrobno.py",
        'label.pack(side="left", padx=10, pady=10)\n'
        "# side: top (по умолчанию), bottom, left, right\n"
        "# padx/pady: внешний отступ по горизонтали/вертикали\n",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "16-02-metki-knopki.ipynb · Label, Button и pack()",
        "../../../notebooks/chapter-16/16-02-metki-knopki.ipynb",
    )}
    """
    out = render_page(
        page_title="Метки, кнопки и их размещение",
        description="Виджеты Label и Button в Tkinter, обработка нажатий и размещение через pack().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 16", "index.html"), ("Метки, кнопки, pack", "")],
        kicker="Глава 16 · Создаём классные приложения с Tkinter",
        h1="Метки, кнопки и их размещение",
        lede="Первые интерактивные виджеты — и то, как Tkinter размещает их в окне.",
        body_html=body,
        sidebar_groups=sidebar("16-02-metki-knopki-pack.html"),
        nav=PageNav(prev_href="16-01-nastraivaem-tkinter.html", prev_label="Настройка Tkinter", next_href="16-03-polya-vvoda.html", next_label="Поля ввода"),
    )
    write("16-02-metki-knopki-pack.html", out)


def build_03() -> None:
    body = f"""
    <h2>Множество полей ввода</h2>
    <p><strong>Поле ввода</strong> (<code class="inline">Entry</code>) — однострочное текстовое
    поле, куда пользователь может что-то напечатать:</p>
    {code_block(
        "polya_vvoda.py",
        "import tkinter as tk\n\n"
        "root = tk.Tk()\n\n"
        'label = tk.Label(root, text="Введите имя:")\n'
        "label.pack()\n\n"
        "entry = tk.Entry(root)\n"
        "entry.pack()\n\n"
        "def pokazat_imya():\n"
        "    imya = entry.get()   # достаём текст из поля\n"
        '    print(f"Привет, {imya}!")\n\n'
        'button = tk.Button(root, text="Отправить", command=pokazat_imya)\n'
        "button.pack()\n\n"
        "root.mainloop()\n",
    )}
    <p><code class="inline">entry.get()</code> возвращает текущий текст поля — обычную строку,
    с которой можно работать, как с любой другой (глава 8).</p>

    <h2 id="tekst">Одна строка текста. Строка за строкой</h2>
    <p><code class="inline">Entry</code> подходит для короткого текста в одну строку — имени,
    числа, пароля. Для многострочного текста используют другой виджет,
    <code class="inline">Text</code>:</p>
    {code_block(
        "mnogostrochnyj_tekst.py",
        "text_box = tk.Text(root, height=5, width=30)\n"
        "text_box.pack()\n\n"
        "def pokazat_tekst():\n"
        '    content = text_box.get("1.0", "end")   # с начала (строка 1, символ 0) до конца\n'
        "    print(content)\n",
    )}
    {callout(
        "info",
        "Индекс \"1.0\" — не опечатка",
        "У <code class=\"inline\">Text</code> своя система индексов: "
        "<code class=\"inline\">\"1.0\"</code> означает «строка 1, символ 0» — то есть самое "
        "начало текста. Это не связано с числами <code class=\"inline\">float</code> из "
        "главы 4 — просто текстовая метка позиции.",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "16-03-polya-vvoda.ipynb · Entry и Text",
        "../../../notebooks/chapter-16/16-03-polya-vvoda.ipynb",
    )}
    """
    out = render_page(
        page_title="Множество полей ввода",
        description="Виджеты Entry (однострочный ввод) и Text (многострочный) в Tkinter.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 16", "index.html"), ("Поля ввода", "")],
        kicker="Глава 16 · Создаём классные приложения с Tkinter",
        h1="Множество полей ввода",
        lede="Entry для одной строки, Text — для нескольких: два способа получить текст от "
        "пользователя.",
        body_html=body,
        sidebar_groups=sidebar("16-03-polya-vvoda.html"),
        nav=PageNav(prev_href="16-02-metki-knopki-pack.html", prev_label="Метки, кнопки, pack", next_href="16-04-peremennye-tkinter.html", next_label="Переменные Tkinter"),
    )
    write("16-03-polya-vvoda.html", out)


def build_04() -> None:
    body = f"""
    <p>Обычные переменные Python не «знают», когда их значение меняется в интерфейсе. Для
    виджетов, которые должны реагировать на изменения (переключатели, флажки — раздел 16.5),
    Tkinter предлагает свои специальные переменные: <code class="inline">StringVar</code>,
    <code class="inline">IntVar</code>, <code class="inline">BooleanVar</code>,
    <code class="inline">DoubleVar</code>.</p>
    {code_block(
        "peremennye_tkinter.py",
        "import tkinter as tk\n\n"
        "root = tk.Tk()\n\n"
        'imya = tk.StringVar(value="Гость")\n\n'
        "label = tk.Label(root, textvariable=imya)   # метка сама обновится при смене imya\n"
        "label.pack()\n\n"
        "def smenit_imya():\n"
        '    imya.set("Cartesian")\n\n'
        'button = tk.Button(root, text="Сменить имя", command=smenit_imya)\n'
        "button.pack()\n\n"
        "root.mainloop()\n",
    )}
    <p>Значение достают методом <code class="inline">.get()</code> и меняют методом
    <code class="inline">.set()</code> — а виджеты, связанные через
    <code class="inline">textvariable</code>, обновляются на экране автоматически.</p>

    {notebook_card(
        "Практика в Jupyter Notebook",
        "16-04-peremennye.ipynb · StringVar и связанные виджеты",
        "../../../notebooks/chapter-16/16-04-peremennye.ipynb",
    )}
    """
    out = render_page(
        page_title="Переменные Tkinter",
        description="StringVar, IntVar и другие специальные переменные Tkinter для связи данных с виджетами.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 16", "index.html"), ("Переменные Tkinter", "")],
        kicker="Глава 16 · Создаём классные приложения с Tkinter",
        h1="Переменные Tkinter",
        lede="Специальные переменные, которые сами обновляют связанные с ними виджеты на "
        "экране.",
        body_html=body,
        sidebar_groups=sidebar("16-04-peremennye-tkinter.html"),
        nav=PageNav(prev_href="16-03-polya-vvoda.html", prev_label="Поля ввода", next_href="16-05-mnozhestvo-variantov.html", next_label="Множество вариантов!"),
    )
    write("16-04-peremennye-tkinter.html", out)


def build_05() -> None:
    body = f"""
    <p>Для выбора из нескольких вариантов у Tkinter есть переключатели
    (<code class="inline">Radiobutton</code> — выбрать один из нескольких) и флажки
    (<code class="inline">Checkbutton</code> — включить/выключить каждый независимо).</p>

    {code_block(
        "radiobutton.py",
        "import tkinter as tk\n\n"
        "root = tk.Tk()\n"
        'vybor = tk.StringVar(value="chay")\n\n'
        'tk.Radiobutton(root, text="Чай", variable=vybor, value="chay").pack()\n'
        'tk.Radiobutton(root, text="Кофе", variable=vybor, value="kofe").pack()\n\n'
        "def pokazat_vybor():\n"
        '    print(f"Вы выбрали: {vybor.get()}")\n\n'
        'tk.Button(root, text="Готово", command=pokazat_vybor).pack()\n'
        "root.mainloop()\n",
    )}

    {code_block(
        "checkbutton.py",
        'saharok = tk.BooleanVar(value=False)\n'
        'tk.Checkbutton(root, text="С сахаром", variable=saharok).pack()\n\n'
        "def pokazat_flazhok():\n"
        '    print(f"С сахаром: {saharok.get()}")\n',
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "16-05-varianty.ipynb · Radiobutton и Checkbutton",
        "../../../notebooks/chapter-16/16-05-varianty.ipynb",
    )}
    """
    out = render_page(
        page_title="Множество вариантов!",
        description="Виджеты Radiobutton и Checkbutton в Tkinter для выбора из нескольких вариантов.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 16", "index.html"), ("Множество вариантов", "")],
        kicker="Глава 16 · Создаём классные приложения с Tkinter",
        h1="Множество вариантов!",
        lede="Переключатели для выбора одного варианта и флажки для независимых да/нет "
        "решений.",
        body_html=body,
        sidebar_groups=sidebar("16-05-mnozhestvo-variantov.html"),
        nav=PageNav(prev_href="16-04-peremennye-tkinter.html", prev_label="Переменные Tkinter", next_href="16-06-menu.html", next_label="Меню"),
    )
    write("16-05-mnozhestvo-variantov.html", out)


def build_06() -> None:
    body = f"""
    <p>Настоящее приложение редко обходится без меню в верхней части окна. В Tkinter меню
    строится из объекта <code class="inline">Menu</code>:</p>
    {code_block(
        "menu.py",
        "import tkinter as tk\n\n"
        "root = tk.Tk()\n\n"
        "def novyj_fajl():\n"
        '    print("Создаём новый файл...")\n\n'
        "menu_bar = tk.Menu(root)\n"
        "fajl_menu = tk.Menu(menu_bar, tearoff=0)\n"
        'fajl_menu.add_command(label="Новый", command=novyj_fajl)\n'
        "fajl_menu.add_separator()\n"
        'fajl_menu.add_command(label="Выход", command=root.quit)\n'
        'menu_bar.add_cascade(label="Файл", menu=fajl_menu)\n\n'
        "root.config(menu=menu_bar)\n"
        "root.mainloop()\n",
    )}
    {callout(
        "info",
        "tearoff=0",
        "По умолчанию Tkinter добавляет в начало каждого меню пунктирную линию, позволяющую "
        "«оторвать» меню в отдельное окно — устаревшая функция, которую в современных "
        "интерфейсах почти всегда отключают параметром <code class=\"inline\">tearoff=0</code>.",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "16-06-menu.ipynb · строим меню приложения",
        "../../../notebooks/chapter-16/16-06-menu.ipynb",
    )}
    """
    out = render_page(
        page_title="Меню",
        description="Строим меню приложения в Tkinter: Menu, add_command, add_cascade.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 16", "index.html"), ("Меню", "")],
        kicker="Глава 16 · Создаём классные приложения с Tkinter",
        h1="Меню",
        lede="Настоящее приложение почти всегда начинается с меню в верхней части окна.",
        body_html=body,
        sidebar_groups=sidebar("16-06-menu.html"),
        nav=PageNav(prev_href="16-05-mnozhestvo-variantov.html", prev_label="Множество вариантов", next_href="16-07-grid.html", next_label="Идеальная компоновка — grid"),
    )
    write("16-06-menu.html", out)


def build_07() -> None:
    body = f"""
    <p><code class="inline">.pack()</code> прекрасно подходит для простых случаев, но у него
    есть предел: сложные формы с несколькими колонками собрать сложно. Для этого есть
    <code class="inline">.grid()</code> — размещение по строкам и столбцам, как в таблице:</p>
    {code_block(
        "grid.py",
        "import tkinter as tk\n\n"
        "root = tk.Tk()\n\n"
        'tk.Label(root, text="Имя:").grid(row=0, column=0)\n'
        "tk.Entry(root).grid(row=0, column=1)\n\n"
        'tk.Label(root, text="Email:").grid(row=1, column=0)\n'
        "tk.Entry(root).grid(row=1, column=1)\n\n"
        'tk.Button(root, text="Отправить").grid(row=2, column=0, columnspan=2)\n\n'
        "root.mainloop()\n",
    )}
    {callout(
        "warning",
        "Не смешивайте pack() и grid() в одном контейнере",
        "Виджеты внутри одного и того же родительского окна (или фрейма) должны использовать "
        "либо только <code class=\"inline\">pack()</code>, либо только "
        "<code class=\"inline\">grid()</code> — смешение вызывает ошибку или зависание "
        "интерфейса. Разные контейнеры (например, вложенные <code class=\"inline\">Frame</code>) "
        "могут использовать разные способы размещения независимо друг от друга.",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "16-07-grid.ipynb · компоновка через grid()",
        "../../../notebooks/chapter-16/16-07-grid.ipynb",
    )}
    """
    out = render_page(
        page_title="Идеальная компоновка — grid",
        description="Метод grid() в Tkinter — размещение виджетов по строкам и столбцам.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 16", "index.html"), ("Компоновка grid", "")],
        kicker="Глава 16 · Создаём классные приложения с Tkinter",
        h1="Идеальная компоновка — grid",
        lede="Для форм с несколькими колонками grid() удобнее, чем pack().",
        body_html=body,
        sidebar_groups=sidebar("16-07-grid.html"),
        nav=PageNav(prev_href="16-06-menu.html", prev_label="Меню", next_href="16-08-mini-proekt-chaevye-itogi.html", next_label="Калькулятор чаевых и итоги"),
    )
    write("16-07-grid.html", out)


def build_08() -> None:
    body = f"""
    <p>Соберём всё изученное в главе в одном настоящем приложении: калькулятор чаевых с полем
    ввода, кнопкой и меткой результата.</p>
    {code_block(
        "kalkulyator_chaevyh.py",
        "import tkinter as tk\n\n"
        "root = tk.Tk()\n"
        'root.title("Калькулятор чаевых")\n\n'
        'tk.Label(root, text="Сумма счёта:").grid(row=0, column=0, padx=10, pady=10)\n'
        "schet_entry = tk.Entry(root)\n"
        "schet_entry.grid(row=0, column=1)\n\n"
        'tk.Label(root, text="Процент чаевых:").grid(row=1, column=0, padx=10, pady=10)\n'
        "procent_entry = tk.Entry(root)\n"
        "procent_entry.grid(row=1, column=1)\n\n"
        'rezultat_label = tk.Label(root, text="", font=(\"Arial\", 14, \"bold\"))\n'
        "rezultat_label.grid(row=3, column=0, columnspan=2, pady=10)\n\n"
        "def poschitat():\n"
        "    schet = float(schet_entry.get())\n"
        "    procent = float(procent_entry.get())\n"
        "    chaevye = schet * procent / 100\n"
        '    rezultat_label.config(text=f"Чаевые: {chaevye:.2f}")\n\n'
        'tk.Button(root, text="Посчитать", command=poschitat).grid(row=2, column=0, columnspan=2)\n\n'
        "root.mainloop()\n",
    )}
    {callout(
        "info",
        "Какие темы здесь встретились",
        "<code class=\"inline\">grid()</code> — этот раздел; <code class=\"inline\">float()</code> "
        "— глава 4; форматирование <code class=\"inline\">:.2f</code> — глава 8; сама формула "
        "чаевых — глава 12, проект 12-2.",
    )}
    {exercise(3, "Проверка ввода", "Оберните вычисление в try/except (забегая немного вперёд — подробно об этом в главе 21) — чтобы приложение не падало, если пользователь введёт не число, а текст.")}

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
        "<code class=\"inline\">tk.Tk()</code> создаёт главное окно; "
        "<code class=\"inline\">mainloop()</code> запускает цикл обработки событий.",
        "Основные виджеты: <code class=\"inline\">Label</code>, <code class=\"inline\">Button</code>, "
        "<code class=\"inline\">Entry</code>, <code class=\"inline\">Text</code>, "
        "<code class=\"inline\">Radiobutton</code>, <code class=\"inline\">Checkbutton</code>.",
        "<code class=\"inline\">command=функция</code> связывает кнопку с действием — без "
        "скобок после имени функции.",
        "<code class=\"inline\">pack()</code> и <code class=\"inline\">grid()</code> — два "
        "способа размещения виджетов; не смешивать их в одном контейнере.",
        "Специальные переменные Tkinter (<code class=\"inline\">StringVar</code> и другие) "
        "автоматически обновляют связанные с ними виджеты.",
    ])}
    """
    out = render_page(
        page_title="Мини-проект — приложение-калькулятор чаевых",
        description="Итоговый мини-проект главы 16: настоящее приложение-калькулятор чаевых на Tkinter — и краткие итоги.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 16", "index.html"), ("Калькулятор чаевых", "")],
        kicker="Глава 16 · Создаём классные приложения с Tkinter",
        h1="Мини-проект — приложение-калькулятор чаевых",
        lede="Первое полноценное приложение книги — с полями ввода, кнопкой и результатом на "
        "экране.",
        body_html=body,
        sidebar_groups=sidebar("16-08-mini-proekt-chaevye-itogi.html"),
        nav=PageNav(prev_href="16-07-grid.html", prev_label="Компоновка grid", next_href="../glava-17/index.html", next_label="Глава 17: Проект: игра «Крестики-нолики» с Tkinter"),
    )
    write("16-08-mini-proekt-chaevye-itogi.html", out)


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
