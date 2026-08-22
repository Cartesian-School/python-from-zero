#!/usr/bin/env python3
"""Строит Главу 23: «Ещё больше мини-проектов» (site/chapters/glava-23/)."""

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
OUT_DIR = ROOT / "site" / "chapters" / "glava-23"

PAGES = [
    ("index.html", "Обзор главы"),
    ("23-01-kalkulyator.html", "Проект 23-1: Калькулятор с Tkinter"),
    ("23-02-generator-istorij.html", "Проект 23-2: Генератор случайных историй"),
    ("23-03-kamen-nozhnicy-bumaga.html", "Проект 23-3: Камень, ножницы, бумага"),
    ("23-04-otskakivayushij-myach.html", "Проект 23-4: Отскакивающий мяч с Pygame"),
    ("23-05-temperatura.html", "Проект 23-5: Преобразование температуры"),
    ("23-06-fajly-tkinter-itogi.html", "Проект 23-6: Файлы и Tkinter. Итоги"),
]

NOTEBOOKS = [
    "23-01-kalkulyator.ipynb",
    "23-02-generator-istorij.ipynb",
    "23-03-kamen-nozhnicy-bumaga.ipynb",
    "23-04-otskakivayushij-myach.ipynb",
    "23-05-temperatura.ipynb",
    "23-06-fajly-tkinter.ipynb",
]

LESSON_IDS = ["23-01", "23-02", "23-03", "23-04", "23-05", "23-06"]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 23 · Ещё мини-проекты", items),
        SidebarGroup(
            "Практика",
            [NavItem(f"[[icon:practice]] {lid}: Практика", f"../../practice/{lid}/index.html") for lid in LESSON_IDS],
        ),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=23,
        baseline_page=511,
        title="Ещё больше мини-проектов",
        description="Шесть небольших, но полноценных проектов — от калькулятора до собственного файла с заметками.",
        meta_items=["[[icon:timer]] ~4 часа", "[[icon:architecture]] 6 мини-проектов", "[[icon:practice]] 6 ноутбуков практики"],
        sections=[
            ChapterSectionLink("23.1", "Проект 23-1: Калькулятор с Tkinter", "23-01-kalkulyator.html", "511"),
            ChapterSectionLink("23.2", "Проект 23-2: Генератор случайных историй", "23-02-generator-istorij.html", "518"),
            ChapterSectionLink("23.3", "Проект 23-3: Игра «Камень, ножницы, бумага»", "23-03-kamen-nozhnicy-bumaga.html", "521"),
            ChapterSectionLink("23.4", "Проект 23-4: Отскакивающий от четырёх стен мяч с Pygame", "23-04-otskakivayushij-myach.html", "527"),
            ChapterSectionLink("23.5", "Проект 23-5: Приложение для преобразования температуры", "23-05-temperatura.html", "531"),
            ChapterSectionLink("23.6", "Проект 23-6: Знакомство с файлами и Tkinter", "23-06-fajly-tkinter-itogi.html", "534"),
            ChapterSectionLink("", "Итоги", "23-06-fajly-tkinter-itogi.html#itogi", "538"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <h2>Проект 23-1: Калькулятор с Tkinter</h2>
    <p>Собираем настоящий калькулятор: экран сверху, кнопки с цифрами и знаками снизу.
    Идея та же, что и в тренажёре «Крестики-нолики» из главы 19 — сетка кнопок, каждая из
    которых вызывает одну и ту же функцию с разным аргументом:</p>

    {code_block(
        "sozdanie_knopok.py",
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
    {callout(
        "warning",
        "lambda s=podpis — почему нельзя просто lambda: ...(podpis)",
        "Это тот же самый «капкан позднего связывания замыканий», что мы разбирали в главе "
        "17: без <code class=\"inline\">s=podpis</code> все кнопки запомнили бы одну и ту же, "
        "последнюю по циклу переменную <code class=\"inline\">podpis</code> — и нажатие любой "
        "кнопки вставляло бы один и тот же символ.",
    )}

    <h2>Вычисляем выражение</h2>
    <p>Вместо того чтобы писать свой разбор арифметики, используем встроенную функцию
    <code class="inline">eval()</code> — но <strong>осторожно</strong>: проверяем, что в
    строке нет ничего, кроме цифр и знаков, и запрещаем доступ к встроенным функциям Python:</p>
    {code_block(
        "vychislenie.py",
        "def vychislit_vyrazhenie(vyrazhenie):\n"
        "    dopustimye_simvoly = set(\"0123456789+-*/(). \")\n"
        "    if not vyrazhenie or not set(vyrazhenie) <= dopustimye_simvoly:\n"
        '        return "Ошибка"\n'
        "    try:\n"
        "        return str(eval(vyrazhenie, {\"__builtins__\": {}}, {}))\n"
        "    except (SyntaxError, ZeroDivisionError, ValueError):\n"
        '        return "Ошибка"\n',
    )}
    {callout(
        "info",
        "Почему просто не написать eval(vyrazhenie)?",
        "Обычный <code class=\"inline\">eval()</code> выполнит <em>любой</em> Python-код, "
        "который ему передать — например, команду для удаления файлов. Проверка разрешённых "
        "символов и пустой словарь <code class=\"inline\">{\"__builtins__\": {}}</code> "
        "не дают выражению сделать ничего, кроме простой арифметики.",
    )}

    <p>Полный код: [[icon:file]] <a href="../../../projects/tkinter/calculator/calculator.py">projects/tkinter/calculator/calculator.py</a></p>

    {local_required_card(
        "23-01",
        "Практика: вычисления и последовательности нажатий",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/23-01/index.html",
    )}
    """
    out = render_page(
        page_title="Проект 23-1: Калькулятор с Tkinter",
        description="Собираем работающий калькулятор: сетка кнопок и безопасное вычисление выражений через eval().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Калькулятор", "")],
        kicker="Глава 23 · Ещё больше мини-проектов",
        h1="Проект 23-1: Калькулятор с Tkinter",
        lede="Экран, сетка кнопок и функция vychislit_vyrazhenie() — вот и весь калькулятор.",
        body_html=body,
        sidebar_groups=sidebar("23-01-kalkulyator.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="23-02-generator-istorij.html", next_label="Генератор случайных историй"),
    )
    write("23-01-kalkulyator.html", out)


def build_02() -> None:
    body = f"""
    <h2>Проект 23-2: Генератор случайных историй</h2>
    <p>Заполняем шаблон предложения случайно выбранными словами из нескольких списков —
    иногда получаются смешные истории («безумные библиотеки», mad libs). Вся идея — в
    <code class="inline">random.choice()</code> (глава 5) и методе строк
    <code class="inline">.format()</code> (глава 8):</p>

    {code_block(
        "story_generator.py",
        'PRILAGATELNYE = ["храбрый", "любопытный", "рассеянный", "весёлый", "загадочный"]\n'
        'SUSHESTVITELNYE = ["дракон", "программист", "кот", "путешественник", "робот"]\n'
        'MESTA = ["в тёмном лесу", "на далёкой планете", "в старой библиотеке"]\n'
        'GLAGOLY = ["нашёл", "потерял", "починил", "изобрёл", "испугался"]\n'
        'PREDMETY = ["волшебный ноутбук", "древний свиток", "сломанный компас"]\n\n'
        'SHABLON = (\n'
        '    "Однажды {prilagatelnoe} {sushestvitelnoe} {mesto} {glagol} {predmet}. "\n'
        '    "С тех пор жизнь его больше не была прежней."\n'
        ")\n\n"
        "def sluchajnaya_istoriya():\n"
        "    return SHABLON.format(\n"
        "        prilagatelnoe=random.choice(PRILAGATELNYE),\n"
        "        sushestvitelnoe=random.choice(SUSHESTVITELNYE),\n"
        "        mesto=random.choice(MESTA),\n"
        "        glagol=random.choice(GLAGOLY),\n"
        "        predmet=random.choice(PREDMETY),\n"
        "    )\n",
    )}
    {callout(
        "tip",
        "Пять независимых случайных выборов — 5×5×5×5×5 = 3125 историй",
        "Даже с пятью короткими списками по 5 слов получается больше трёх тысяч различных "
        "комбинаций — вот почему такой простой приём кажется таким разнообразным.",
    )}

    <p>Полный код: [[icon:file]] <a href="../../../projects/console/story-generator/story_generator.py">projects/console/story-generator/story_generator.py</a></p>

    {exercise(2, "Ещё один список", "Добавьте список НАРЕЧИЯ (например, \"внезапно\", \"случайно\", \"незаметно\") и вставьте {narechie} в шаблон.")}

    {practice_card(
        "23-02",
        "Практика: случайные истории и random.seed()",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/23-02/index.html",
    )}
    """
    out = render_page(
        page_title="Проект 23-2: Генератор случайных историй",
        description="Заполняем шаблон предложения случайными словами из списков — простой генератор мини-историй.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Генератор историй", "")],
        kicker="Глава 23 · Ещё больше мини-проектов",
        h1="Проект 23-2: Генератор случайных историй",
        lede="random.choice() пять раз подряд — и шаблон превращается в маленькую историю.",
        body_html=body,
        sidebar_groups=sidebar("23-02-generator-istorij.html"),
        nav=PageNav(prev_href="23-01-kalkulyator.html", prev_label="Калькулятор", next_href="23-03-kamen-nozhnicy-bumaga.html", next_label="Камень, ножницы, бумага"),
    )
    write("23-02-generator-istorij.html", out)


def build_03() -> None:
    body = f"""
    <h2>Проект 23-3: Игра «Камень, ножницы, бумага»</h2>
    <p>Классика! Вся логика игры умещается в одном словаре — кто кого побеждает:</p>
    {code_block(
        "logika_pobeditelya.py",
        "POBEZHDAET = {\n"
        '    "камень": "ножницы",\n'
        '    "ножницы": "бумага",\n'
        '    "бумага": "камень",\n'
        "}\n\n"
        "def opredelit_pobeditelya(hod_igroka, hod_kompyutera):\n"
        "    if hod_igroka == hod_kompyutera:\n"
        '        return "ничья"\n'
        "    if POBEZHDAET[hod_igroka] == hod_kompyutera:\n"
        '        return "игрок"\n'
        '    return "компьютер"\n',
    )}
    {callout(
        "tip",
        "Словарь вместо длинной цепочки if/elif",
        "Можно было написать девять условий <code class=\"inline\">if hod_igroka == "
        "\"камень\" and hod_kompyutera == \"ножницы\": ...</code> — но словарь "
        "<code class=\"inline\">POBEZHDAET</code> делает то же самое в трёх строчках и легко "
        "читается: «камень побеждает ножницы».",
    )}

    <h2>Ход компьютера и полный раунд</h2>
    {code_block(
        "raund.py",
        "def hod_kompyutera():\n"
        "    return random.choice(VARIANTY)\n\n"
        "def sygrat_raund(hod_igroka):\n"
        "    hod_pk = hod_kompyutera()\n"
        "    pobeditel = opredelit_pobeditelya(hod_igroka, hod_pk)\n"
        "    return hod_pk, pobeditel\n",
    )}

    <p>Полный код (с меню и счётом): [[icon:file]] <a href="../../../projects/console/rock-paper-scissors/rps.py">projects/console/rock-paper-scissors/rps.py</a></p>

    {exercise(3, "Добавляем ящерицу и Спока", "Реализуйте расширенную версию игры «Камень, ножницы, бумага, ящерица, Спок» — понадобится словарь POBEZHDAET с пятью ключами, каждый побеждает по два варианта.")}

    {practice_card(
        "23-03",
        "Практика: все 9 комбинаций и симуляция раундов",
        "Интерактивный ноутбук прямо в браузере — Python 3.14 через Pyodide, без установки",
        "../../practice/23-03/index.html",
    )}
    """
    out = render_page(
        page_title="Проект 23-3: Камень, ножницы, бумага",
        description="Классическая игра: словарь POBEZHDAET определяет победителя, random.choice() — ход компьютера.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Камень, ножницы, бумага", "")],
        kicker="Глава 23 · Ещё больше мини-проектов",
        h1="Проект 23-3: Игра «Камень, ножницы, бумага»",
        lede="Вся логика игры — один словарь: кто кого побеждает.",
        body_html=body,
        sidebar_groups=sidebar("23-03-kamen-nozhnicy-bumaga.html"),
        nav=PageNav(prev_href="23-02-generator-istorij.html", prev_label="Генератор историй", next_href="23-04-otskakivayushij-myach.html", next_label="Отскакивающий мяч с Pygame"),
    )
    write("23-03-kamen-nozhnicy-bumaga.html", out)


def build_04() -> None:
    body = f"""
    <h2>Проект 23-4: Отскакивающий от четырёх стен мяч с Pygame</h2>
    <p>В главе 20 мяч был устроен через обычные переменные и функции. Теперь, когда мы
    знаем классы (глава 15), опишем мяч как объект — и сразу получим возможность легко
    завести <em>несколько</em> мячей одновременно:</p>

    {code_block(
        "myach_klass.py",
        "class Myach:\n"
        "    def __init__(self, x, y, dx, dy, radius, cvet):\n"
        "        self.x = x\n"
        "        self.y = y\n"
        "        self.dx = dx\n"
        "        self.dy = dy\n"
        "        self.radius = radius\n"
        "        self.cvet = cvet\n"
        "        self.otskokov = 0\n\n"
        "    def shag(self):\n"
        "        self.x += self.dx\n"
        "        self.y += self.dy\n"
        "        if self.x - self.radius < 0 or self.x + self.radius > SHIRINA:\n"
        "            self.dx = -self.dx\n"
        "            self.otskokov += 1\n"
        "        # ... то же самое для self.y и VYSOTA\n\n"
        "    def narisovat(self):\n"
        "        pygame.draw.circle(screen, self.cvet, (int(self.x), int(self.y)), self.radius)\n",
    )}
    {callout(
        "info",
        "Список объектов вместо списка переменных",
        "Раньше пришлось бы заводить отдельные <code class=\"inline\">x1, y1, dx1, dy1, x2, "
        "y2, dx2, dy2, …</code> для каждого мяча. Теперь достаточно "
        "<code class=\"inline\">myachi = [Myach(...), Myach(...), Myach(...)]</code> — и "
        "цикл <code class=\"inline\">for myach in myachi: myach.shag()</code> двигает их все "
        "разом.",
    )}

    <p>Полный код: [[icon:file]] <a href="../../../projects/pygame/bouncing-balls-oop/bouncing_balls.py">projects/pygame/bouncing-balls-oop/bouncing_balls.py</a></p>

    {exercise(2, "Столкновение мячей друг с другом", "Добавьте проверку расстояния между каждой парой мячей — если они соприкоснулись, поменяйте местами их dx и dy.")}

    {local_required_card(
        "23-04",
        "Практика: класс Myach и несколько мячей сразу",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/23-04/index.html",
    )}
    """
    out = render_page(
        page_title="Проект 23-4: Отскакивающий от четырёх стен мяч с Pygame",
        description="Версия мяча из главы 20, переписанная в виде класса Myach — и сразу несколько мячей одновременно.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Отскакивающий мяч", "")],
        kicker="Глава 23 · Ещё больше мини-проектов",
        h1="Проект 23-4: Отскакивающий от четырёх стен мяч",
        lede="Та же физика, что и в главе 20, — но теперь мяч это класс, а значит, их может быть сколько угодно.",
        body_html=body,
        sidebar_groups=sidebar("23-04-otskakivayushij-myach.html"),
        nav=PageNav(prev_href="23-03-kamen-nozhnicy-bumaga.html", prev_label="Камень, ножницы, бумага", next_href="23-05-temperatura.html", next_label="Преобразование температуры"),
    )
    write("23-04-otskakivayushij-myach.html", out)


def build_05() -> None:
    body = f"""
    <h2>Проект 23-5: Приложение для преобразования температуры</h2>
    <p>Небольшое, но по-настоящему полезное приложение: вводим температуру, выбираем
    единицу через переключатели (<code class="inline">Radiobutton</code>) и сразу видим
    значение во всех трёх шкалах:</p>

    {code_block(
        "preobrazovanie.py",
        "def celsij_v_farengejt(c):\n"
        "    return c * 9 / 5 + 32\n\n"
        "def celsij_v_kelvin(c):\n"
        "    return c + 273.15\n\n"
        "def preobrazovat(znachenie, iz_edinicy):\n"
        '    if iz_edinicy == "C":\n'
        "        c = znachenie\n"
        '    elif iz_edinicy == "F":\n'
        "        c = farengejt_v_celsij(znachenie)\n"
        "    else:\n"
        "        c = kelvin_v_celsij(znachenie)\n\n"
        "    return {\n"
        '        "C": c,\n'
        '        "F": celsij_v_farengejt(c),\n'
        '        "K": celsij_v_kelvin(c),\n'
        "    }\n",
    )}
    {callout(
        "tip",
        "Всегда переводим через Цельсий",
        "Вместо шести отдельных формул (C→F, C→K, F→C, F→K, K→C, K→F) достаточно уметь "
        "переводить <em>в</em> Цельсий и <em>из</em> Цельсия — остальные пять переводов "
        "получаются сами собой через промежуточный шаг.",
    )}

    <h2>Переключатели Radiobutton</h2>
    {code_block(
        "radiobutton.py",
        'edinica = tk.StringVar(value="C")\n\n'
        'for kod, podpis in [("C", "Цельсий"), ("F", "Фаренгейт"), ("K", "Кельвин")]:\n'
        "    tk.Radiobutton(root, text=podpis, variable=edinica, value=kod).grid(...)\n",
    )}
    {callout(
        "info",
        "Radiobutton — «выбери один из нескольких»",
        "Все переключатели с одинаковой <code class=\"inline\">variable=edinica</code> "
        "работают как группа — можно выбрать только один одновременно, а "
        "<code class=\"inline\">edinica.get()</code> всегда возвращает значение выбранного.",
    )}

    <p>Полный код: [[icon:file]] <a href="../../../projects/tkinter/temperature-converter/temperature_converter.py">projects/tkinter/temperature-converter/temperature_converter.py</a></p>

    {local_required_card(
        "23-05",
        "Практика: формулы и симуляция ввода пользователя",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/23-05/index.html",
    )}
    """
    out = render_page(
        page_title="Проект 23-5: Приложение для преобразования температуры",
        description="Radiobutton для выбора шкалы и функции перевода между Цельсием, Фаренгейтом и Кельвином.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Температура", "")],
        kicker="Глава 23 · Ещё больше мини-проектов",
        h1="Проект 23-5: Преобразование температуры",
        lede="Одна функция перевода в Цельсий — и все шесть направлений пересчёта готовы.",
        body_html=body,
        sidebar_groups=sidebar("23-05-temperatura.html"),
        nav=PageNav(prev_href="23-04-otskakivayushij-myach.html", prev_label="Отскакивающий мяч", next_href="23-06-fajly-tkinter-itogi.html", next_label="Файлы и Tkinter. Итоги"),
    )
    write("23-05-temperatura.html", out)


def build_06() -> None:
    body = f"""
    <h2>Проект 23-6: Знакомство с файлами и Tkinter</h2>
    <p>Последний мини-проект главы объединяет файлы (глава 14) и Tkinter (главы 16-19):
    простое приложение «Заметки» с текстовым полем и тремя кнопками — сохранить, загрузить,
    очистить:</p>

    {code_block(
        "sohranenie_zagruzka.py",
        'FAJL_ZAMETOK = Path(__file__).parent / "zametka.txt"\n\n'
        "def sohranit_zametku():\n"
        '    tekst = polye_teksta.get("1.0", "end-1c")\n'
        '    FAJL_ZAMETOK.write_text(tekst, encoding="utf-8")\n'
        '    status_text.set(f"Сохранено в {FAJL_ZAMETOK.name}")\n\n'
        "def zagruzit_zametku():\n"
        "    if not FAJL_ZAMETOK.exists():\n"
        '        status_text.set("Файл заметки ещё не создан — сначала сохраните.")\n'
        "        return\n"
        '    tekst = FAJL_ZAMETOK.read_text(encoding="utf-8")\n'
        '    polye_teksta.delete("1.0", "end")\n'
        '    polye_teksta.insert("1.0", tekst)\n',
    )}
    {callout(
        "tip",
        "\"1.0\" и \"end-1c\" — адресация текста в Text",
        "У виджета <code class=\"inline\">Text</code> (в отличие от <code class=\"inline\">"
        "Entry</code>) текст адресуется парой «строка.столбец»: <code class=\"inline\">"
        "\"1.0\"</code> — самое начало (строка 1, столбец 0), <code class=\"inline\">"
        "\"end-1c\"</code> — конец текста без завершающего невидимого перевода строки, "
        "который Tkinter добавляет сам.",
    )}
    {callout(
        "warning",
        "Проверка exists() перед чтением",
        "Если попытаться прочитать несуществующий файл через <code class=\"inline\">"
        "read_text()</code>, программа упадёт с <code class=\"inline\">FileNotFoundError</code>. "
        "Проверка <code class=\"inline\">if not FAJL_ZAMETOK.exists():</code> превращает "
        "падение программы в понятное сообщение для пользователя.",
    )}

    <p>Полный код: [[icon:file]] <a href="../../../projects/tkinter/notes-app/notes_app.py">projects/tkinter/notes-app/notes_app.py</a></p>

    {exercise(2, "Предупреждение о несохранённых изменениях", "Заведите переменную byli_izmeneniya = False, ставьте её в True при любом изменении текста и показывайте предупреждение при попытке «Очистить поле», если она True.")}

    {local_required_card(
        "23-06",
        "Практика: сохранение, загрузка и отсутствующий файл",
        "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/23-06/index.html",
    )}

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
        "Шесть небольших проектов показывают, как уже знакомые инструменты — Tkinter, "
        "Pygame, файлы, классы, словари — снова и снова складываются в новые приложения.",
        "Безопасный <code class=\"inline\">eval()</code> с проверкой символов и пустым "
        "<code class=\"inline\">__builtins__</code> позволяет вычислять арифметические "
        "выражения, не рискуя выполнить произвольный код.",
        "Словарь — отличный способ описать отношения между вариантами (кто кого "
        "побеждает, что во что переводится), избегая длинных цепочек if/elif.",
        "Класс превращает набор связанных переменных (позиция, скорость, цвет мяча) в "
        "один объект — и сразу же позволяет завести их сколько угодно через список.",
        "Перед чтением файла стоит проверять <code class=\"inline\">Path.exists()</code> — "
        "это превращает возможный крах программы в понятное сообщение для пользователя.",
    ])}
    """
    out = render_page(
        page_title="Проект 23-6: Файлы и Tkinter. Итоги",
        description="Приложение «Заметки»: сохранение и загрузка текста из файла — и итоги главы 23.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 23", "index.html"), ("Файлы и Tkinter", "")],
        kicker="Глава 23 · Ещё больше мини-проектов",
        h1="Проект 23-6: Знакомство с файлами и Tkinter",
        lede="Простое приложение «Заметки» — и подведение итогов главы.",
        body_html=body,
        sidebar_groups=sidebar("23-06-fajly-tkinter-itogi.html"),
        nav=PageNav(prev_href="23-05-temperatura.html", prev_label="Температура", next_href="../glava-24/index.html", next_label="Глава 24: Что дальше?"),
    )
    write("23-06-fajly-tkinter-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01()
    build_02()
    build_03()
    build_04()
    build_05()
    build_06()
