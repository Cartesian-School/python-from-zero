#!/usr/bin/env python3
"""Строит Главу 18: «Проект: приложение для рисования с Tkinter» (site/chapters/glava-18/)."""

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
OUT_DIR = ROOT / "site" / "chapters" / "glava-18"

PAGES = [
    ("index.html", "Обзор главы"),
    ("18-01-obyasnenie-nachalo.html", "Объяснение и начало работы"),
    ("18-02-ekran-holst.html", "Экран и холст (Canvas)"),
    ("18-03-menu-parametry.html", "Меню фигур и параметры рисования"),
    ("18-04-mysh-linii.html", "Позиция мыши и рисуем линии"),
    ("18-05-figury.html", "Квадраты, прямоугольники, круги и овалы"),
    ("18-06-razmer-cveta.html", "Выбираем размер и цвет"),
    ("18-07-polnaya-programma-itogi.html", "Полная программа и итоги"),
]

NOTEBOOKS = [
    "18-02-holst.ipynb",
    "18-03-parametry.ipynb",
    "18-04-linii.ipynb",
    "18-05-figury.ipynb",
    "18-06-razmer-cveta.ipynb",
    "18-07-polnoe-prilozhenie.ipynb",
]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 18 · Рисовалка", items),
        SidebarGroup("Практика", [NavItem(f"📓 {n}", f"../../../notebooks/chapter-18/{n}") for n in NOTEBOOKS]),
        SidebarGroup("Исходный код", [NavItem("🐍 paint_app.py", "../../../projects/tkinter/paint-app/paint_app.py")]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=18,
        baseline_page=391,
        title="Проект: приложение для рисования с Tkinter",
        description="Собственная «рисовалка» с холстом, выбором фигур, цвета и толщины линии.",
        meta_items=["⏱ ~3 часа", "🎨 виджет Canvas", "📓 6 ноутбуков практики"],
        sections=[
            ChapterSectionLink("18.1", "Приложение для рисования — объяснение", "18-01-obyasnenie-nachalo.html", "391"),
            ChapterSectionLink("", "Начинаем работу", "18-01-obyasnenie-nachalo.html#nachalo", "392"),
            ChapterSectionLink("18.2", "Настраиваем экран. Создаём холст", "18-02-ekran-holst.html", "393"),
            ChapterSectionLink("18.3", "Создаём первое меню (фигуры)", "18-03-menu-parametry.html", "395"),
            ChapterSectionLink("", "Заставляем параметры рисования работать!", "18-03-menu-parametry.html#parametry", "396"),
            ChapterSectionLink("18.4", "Получаем позицию мыши", "18-04-mysh-linii.html", "398"),
            ChapterSectionLink("", "Рисуем линии", "18-04-mysh-linii.html#linii", "399"),
            ChapterSectionLink("18.5", "Квадраты и прямоугольники! Круги и овалы!", "18-05-figury.html", "401"),
            ChapterSectionLink("18.6", "Выбираем размер! Очень много цветов!", "18-06-razmer-cveta.html", "403"),
            ChapterSectionLink("18.7", "Я закончил рисовать! Полная программа", "18-07-polnaya-programma-itogi.html", "407"),
            ChapterSectionLink("", "Итоги", "18-07-polnaya-programma-itogi.html#itogi", "412"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <h2>Приложение для рисования — объяснение</h2>
    <p>Соберём собственный маленький «Paint»: холст, на котором можно рисовать линии,
    прямоугольники, овалы и произвольные каракули мышью — с выбором цвета и толщины. План
    такой же пошаговый, как и в главе 17:</p>
    <ol>
      <li>Холст для рисования (виджет <code class="inline">Canvas</code>);</li>
      <li>Панель инструментов — кнопки выбора фигуры;</li>
      <li>Реакция на движение и клики мыши;</li>
      <li>Собственно рисование линий, прямоугольников, овалов;</li>
      <li>Выбор толщины и цвета;</li>
      <li>Кнопка очистки холста.</li>
    </ol>

    <h2 id="nachalo">Начинаем работу</h2>
    {code_block(
        "nachalo.py",
        "import tkinter as tk\n\n"
        "root = tk.Tk()\n"
        'root.title("Рисовалка")\n',
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "18-02-holst.ipynb · начинаем собирать рисовалку",
        "../../../notebooks/chapter-18/18-02-holst.ipynb",
    )}
    """
    out = render_page(
        page_title="Приложение для рисования — объяснение",
        description="План сборки приложения-рисовалки на Tkinter по шагам.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Объяснение", "")],
        kicker="Глава 18 · Проект: приложение для рисования",
        h1="Приложение для рисования — объяснение",
        lede="Разберём план из шести шагов — от пустого холста до готовой рисовалки.",
        body_html=body,
        sidebar_groups=sidebar("18-01-obyasnenie-nachalo.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="18-02-ekran-holst.html", next_label="Экран и холст"),
    )
    write("18-01-obyasnenie-nachalo.html", out)


def build_02() -> None:
    body = f"""
    <h2>Настраиваем экран</h2>
    {code_block("nastrojka_ekrana.py", 'root.title("Рисовалка")\n')}

    <h2>Создаём холст</h2>
    <p>Виджет <code class="inline">Canvas</code> — прямоугольная область, на которой можно
    рисовать линии, фигуры и текст координатами, как в Turtle (главы 6–7), только внутри окна
    Tkinter:</p>
    {code_block(
        "sozdaem_holst.py",
        'canvas = tk.Canvas(root, width=600, height=400, bg="white")\n'
        "canvas.pack()\n",
    )}
    {callout(
        "info",
        "Координаты Canvas — как у экрана, не как у Turtle",
        "У <code class=\"inline\">Canvas</code> точка (0, 0) — левый верхний угол, а не центр, "
        "как у экрана Turtle, и ось Y растёт <strong>вниз</strong>, а не вверх. Если раньше вы "
        "рисовали Turtle — обратите на это внимание, чтобы не запутаться.",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "18-02-holst.ipynb · создаём Canvas",
        "../../../notebooks/chapter-18/18-02-holst.ipynb",
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
        nav=PageNav(prev_href="18-01-obyasnenie-nachalo.html", prev_label="Объяснение", next_href="18-03-menu-parametry.html", next_label="Меню фигур и параметры"),
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

    <h2 id="parametry">Заставляем параметры рисования работать!</h2>
    <p>Заведём глобальные переменные для текущей фигуры, цвета и толщины линии — их будут
    менять кнопки панели инструментов и читать функции рисования:</p>
    {code_block(
        "parametry.py",
        'tekuschaya_figura = "linia"\n'
        'tekuschij_cvet = "black"\n'
        "tolschina = 3\n",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "18-03-parametry.ipynb · панель инструментов и параметры рисования",
        "../../../notebooks/chapter-18/18-03-parametry.ipynb",
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
    {callout(
        "tip",
        "create_line — как forward() у Turtle, только по координатам",
        "<code class=\"inline\">canvas.create_line(x1, y1, x2, y2)</code> рисует прямую между "
        "двумя точками — концептуально то же самое, что <code class=\"inline\">goto()</code> "
        "у Turtle из главы 6, только без «черепашки», которая сама туда едет.",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "18-04-linii.ipynb · позиция мыши и рисование линий",
        "../../../notebooks/chapter-18/18-04-linii.ipynb",
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
    {callout(
        "warning",
        "Промежуточные фигуры множатся",
        "Если рисовать так, как показано выше, при каждом движении мыши будет создаваться "
        "<strong>новая</strong> фигура поверх предыдущей — а не одна, растущая вместе с "
        "движением. В полной программе (раздел 18.7) эта проблема решена: предыдущая "
        "«черновая» фигура удаляется перед тем, как нарисовать новую.",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "18-05-figury.ipynb · прямоугольники и овалы",
        "../../../notebooks/chapter-18/18-05-figury.ipynb",
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

    <h2>Очень много цветов!</h2>
    <p>Палитру цветов легко построить циклом (глава 10) по списку названий (глава 11) — вместо
    того, чтобы создавать каждую кнопку вручную:</p>
    {code_block(
        "vybor_cveta.py",
        'cveta = ["black", "red", "blue", "green", "orange", "purple"]\n'
        "for cvet in cveta:\n"
        '    tk.Button(toolbar, bg=cvet, width=2, command=lambda c=cvet: vybrat_cvet(c)).pack(side="left")\n',
    )}
    {callout(
        "tip",
        "lambda c=cvet — та же тонкость, что и в главе 17",
        "Без <code class=\"inline\">c=cvet</code> все кнопки палитры выбирали бы <strong>"
        "последний</strong> цвет из списка — та же самая ловушка с лямбдами внутри цикла, что "
        "мы уже разбирали в проекте «Крестики-нолики».",
    )}

    {notebook_card(
        "Практика в Jupyter Notebook",
        "18-06-razmer-cveta.ipynb · Scale и палитра цветов",
        "../../../notebooks/chapter-18/18-06-razmer-cveta.ipynb",
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
        nav=PageNav(prev_href="18-05-figury.html", prev_label="Фигуры", next_href="18-07-polnaya-programma-itogi.html", next_label="Полная программа и итоги"),
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

    <h2 id="polnaya-programma">Полная программа</h2>
    <p>Полная версия приложения, включая исправленную отрисовку «черновых» фигур во время
    перетаскивания мыши, доступна отдельным файлом:</p>
    <p>📄 <a href="../../../projects/tkinter/paint-app/paint_app.py">projects/tkinter/paint-app/paint_app.py</a></p>

    {exercise(2, "Кнопка «Отменить»", "Сохраняйте id каждой нарисованной фигуры (canvas.create_* возвращает id) в список — и добавьте кнопку, удаляющую последнюю через canvas.delete(id).")}
    {exercise(3, "Сохранение рисунка", "Изучите модуль tkinter.filedialog и попробуйте добавить кнопку «Сохранить» — как минимум сохраняющую список нарисованных фигур в текстовый файл (глава 15).")}

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
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
    ])}
    """
    out = render_page(
        page_title="Я закончил рисовать! Полная программа",
        description="Очистка холста, режим свободного рисования, ссылка на полный исходный код и итоги главы 18.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 18", "index.html"), ("Полная программа", "")],
        kicker="Глава 18 · Проект: приложение для рисования",
        h1="Я закончил рисовать! Полная программа",
        lede="Последние штрихи — очистка холста и свободное рисование — и полная работающая "
        "программа целиком.",
        body_html=body,
        sidebar_groups=sidebar("18-07-polnaya-programma-itogi.html"),
        nav=PageNav(prev_href="18-06-razmer-cveta.html", prev_label="Размер и цвет", next_href="../glava-19/index.html", next_label="Глава 19: Проект: игра «Змейка» с Turtle"),
    )
    write("18-07-polnaya-programma-itogi.html", out)


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
