#!/usr/bin/env python3
"""Строит Главу 20: «Станьте разработчиком игр с Pygame» (site/chapters/glava-20/)."""

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
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-20"

PAGES = [
    ("index.html", "Обзор главы"),
    ("20-01-chto-takoe-pygame.html", "Что такое Pygame? Установка"),
    ("20-02-igrovoj-ekran.html", "Игровой экран"),
    ("20-03-personazhi.html", "Создаём персонажей"),
    ("20-04-peremeshenie-klavishi.html", "Перемещаем персонажей. Клавиши"),
    ("20-05-mini-proekt-myach-itogi.html", "Мини-проект: прыгающий мяч и итоги"),
]

NOTEBOOKS = [
    "20-02-ekran.ipynb",
    "20-03-personazhi.ipynb",
    "20-04-dvizhenie-klavishi.ipynb",
    "20-05-myach.ipynb",
]

LESSON_IDS = ["20-02", "20-03", "20-04", "20-05"]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 20 · Pygame", items),
        SidebarGroup(
            "Практика",
            [NavItem(f"🐍 {lid}: Практика", f"../../practice/{lid}/index.html") for lid in LESSON_IDS],
        ),
        SidebarGroup("Исходный код", [NavItem("🐍 bouncing_ball.py", "../../../projects/pygame/bouncing-ball/bouncing_ball.py")]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=20,
        baseline_page=445,
        title="Станьте разработчиком игр с Pygame",
        description="Новый инструмент для игр — быстрее и гибче Turtle, с настоящим игровым циклом и обработкой кадров.",
        meta_items=["⏱ ~2–3 часа", "🕹️ модуль pygame", "📓 4 ноутбука практики"],
        sections=[
            ChapterSectionLink("20.1", "Что такое Pygame?", "20-01-chto-takoe-pygame.html", "445"),
            ChapterSectionLink("", "Устанавливаем и импортируем Pygame", "20-01-chto-takoe-pygame.html#ustanovka", "446"),
            ChapterSectionLink("20.2", "Настраиваем игровой экран!", "20-02-igrovoj-ekran.html", "448"),
            ChapterSectionLink("", "Делаем экран красивым", "20-02-igrovoj-ekran.html#krasivyj", "450"),
            ChapterSectionLink("20.3", "Создаём персонажей на экране", "20-03-personazhi.html", "452"),
            ChapterSectionLink("20.4", "Перемещаем персонажей", "20-04-peremeshenie-klavishi.html", "457"),
            ChapterSectionLink("", "События нажатия клавиш", "20-04-peremeshenie-klavishi.html#klavishi", "459"),
            ChapterSectionLink("20.5", "Мини-проект — прыгающий мяч", "20-05-mini-proekt-myach-itogi.html", "462"),
            ChapterSectionLink("", "Итоги", "20-05-mini-proekt-myach-itogi.html#itogi", "465"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <h2>Что такое Pygame?</h2>
    <p><code class="inline">Pygame</code> — библиотека специально для игр: она даёт гораздо
    больше контроля над кадрами анимации, столкновениями и звуком, чем Turtle (главы 6–7, 12)
    или Tkinter (главы 16–19). В отличие от них, <code class="inline">Pygame</code> не входит
    в стандартную поставку Python — его нужно установить отдельно.</p>

    <h2 id="ustanovka">Устанавливаем и импортируем Pygame</h2>
    {code_block("ustanovka.txt", "pip install pygame\n")}
    {callout(
        "warning",
        "Актуально на момент написания книги: используйте pygame-ce",
        "На Python 3.14 у классического пакета <code class=\"inline\">pygame</code> пока может "
        "не быть готового установочного файла (wheel) — установка попытается собрать его из "
        "исходного кода и упадёт с ошибкой про <code class=\"inline\">sdl-config</code>. "
        "Решение — установить активно поддерживаемый форк с полностью совместимым API: "
        "<code class=\"inline\">pip install pygame-ce</code>. Весь код в этой книге "
        "по-прежнему пишется как <code class=\"inline\">import pygame</code> — оба пакета "
        "используют одно и то же имя модуля.",
    )}
    {code_block("import_pygame.py", "import pygame\n\npygame.init()   # обязательная инициализация перед началом работы\n")}

    {local_required_card(
        "20-02",
        "Практика: установка и первый импорт",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/20-02/index.html",
    )}
    """
    out = render_page(
        page_title="Что такое Pygame? Установка",
        description="Знакомство с библиотекой Pygame для разработки игр и её установка через pip.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 20", "index.html"), ("Что такое Pygame?", "")],
        kicker="Глава 20 · Станьте разработчиком игр с Pygame",
        h1="Что такое Pygame?",
        lede="Специализированный инструмент для игр — с более тонким контролем над кадрами "
        "анимации, чем у Turtle и Tkinter.",
        body_html=body,
        sidebar_groups=sidebar("20-01-chto-takoe-pygame.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="20-02-igrovoj-ekran.html", next_label="Игровой экран"),
    )
    write("20-01-chto-takoe-pygame.html", out)


def build_02() -> None:
    body = f"""
    <h2>Настраиваем игровой экран!</h2>
    <p>Экран Pygame — обычная поверхность (<code class="inline">Surface</code>) заданного
    размера:</p>
    {code_block(
        "igrovoj_ekran.py",
        "import pygame\n\n"
        "pygame.init()\n"
        "screen = pygame.display.set_mode((600, 400))\n"
        'pygame.display.set_caption("Моя первая игра")\n',
    )}

    <h2>Игровой цикл</h2>
    <p>В отличие от Tkinter с его <code class="inline">mainloop()</code>, в Pygame игровой цикл
    пишут вручную — это даёт полный контроль над тем, что происходит на каждом кадре:</p>
    {code_block(
        "igrovoj_cikl.py",
        "clock = pygame.time.Clock()\n"
        "rabotaet = True\n\n"
        "while rabotaet:\n"
        "    for event in pygame.event.get():\n"
        "        if event.type == pygame.QUIT:\n"
        "            rabotaet = False\n\n"
        "    pygame.display.flip()   # показать нарисованный кадр\n"
        "    clock.tick(60)          # не больше 60 кадров в секунду\n\n"
        "pygame.quit()\n",
    )}
    {callout(
        "info",
        "Зачем нужен pygame.QUIT?",
        "Без обработки события <code class=\"inline\">pygame.QUIT</code> (нажатие на "
        "крестик окна) программа не узнает, что пользователь хочет закрыть игру, и окно "
        "перестанет отвечать. Обработка событий в начале каждого кадра цикла — обязательная "
        "часть любой программы на Pygame.",
    )}

    <h2 id="krasivyj">Делаем экран красивым</h2>
    <p><code class="inline">screen.fill(цвет)</code> закрашивает весь экран цветом (в виде
    кортежа RGB, глава 11) — обычно первая команда в каждом кадре, иначе на экране останутся
    «следы» от предыдущего кадра:</p>
    {code_block("zalivka_fona.py", "CVET_FONA = (20, 20, 40)\n\nscreen.fill(CVET_FONA)\n")}

    {local_required_card(
        "20-02",
        "Практика: игровой цикл и заливка фона",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/20-02/index.html",
    )}
    """
    out = render_page(
        page_title="Настраиваем игровой экран! Делаем экран красивым",
        description="Экран и игровой цикл Pygame: display.set_mode(), обработка событий, fill() и flip().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 20", "index.html"), ("Игровой экран", "")],
        kicker="Глава 20 · Станьте разработчиком игр с Pygame",
        h1="Настраиваем игровой экран!",
        lede="Игровой цикл — сердце любой игры на Pygame: он пишется вручную, кадр за кадром.",
        body_html=body,
        sidebar_groups=sidebar("20-02-igrovoj-ekran.html"),
        nav=PageNav(prev_href="20-01-chto-takoe-pygame.html", prev_label="Что такое Pygame?", next_href="20-03-personazhi.html", next_label="Создаём персонажей"),
    )
    write("20-02-igrovoj-ekran.html", out)


def build_03() -> None:
    body = f"""
    <p>Персонажей и объекты в Pygame рисуют прямо на экране каждый кадр — простыми фигурами
    (кругами, прямоугольниками), как мы делали в Turtle, или готовыми изображениями. Начнём с
    фигур — они не требуют внешних файлов и отлично подходят для первых игр:</p>
    {code_block(
        "personazhi.py",
        "CVET_IGROKA = (100, 200, 255)\n"
        "CVET_VRAGA = (255, 80, 80)\n\n"
        "x_igroka, y_igroka = 300, 350\n"
        "x_vraga, y_vraga = 300, 50\n\n"
        "# внутри игрового цикла, после screen.fill(...):\n"
        "pygame.draw.rect(screen, CVET_IGROKA, (x_igroka, y_igroka, 40, 40))\n"
        "pygame.draw.circle(screen, CVET_VRAGA, (x_vraga, y_vraga), 20)\n",
    )}
    <p><code class="inline">pygame.draw.rect()</code> принимает кортеж
    <code class="inline">(x, y, ширина, высота)</code> — <code class="inline">(x, y)</code> это
    левый верхний угол, как у <code class="inline">Canvas</code> в главе 18, а не центр, как у
    <code class="inline">circle()</code>.</p>

    {callout(
        "info",
        "Rect — прямоугольник как объект",
        "Для более сложных игр Pygame предлагает класс <code class=\"inline\">pygame.Rect</code> "
        "— он хранит позицию и размер вместе и умеет проверять пересечения "
        "(<code class=\"inline\">.colliderect()</code>) — то, что понадобится для космического "
        "шутера в главе 21.",
    )}

    {local_required_card(
        "20-03",
        "Практика: рисуем персонажей",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/20-03/index.html",
    )}
    """
    out = render_page(
        page_title="Создаём персонажей на экране",
        description="Рисуем игровых персонажей простыми фигурами: pygame.draw.rect() и pygame.draw.circle().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 20", "index.html"), ("Персонажи", "")],
        kicker="Глава 20 · Станьте разработчиком игр с Pygame",
        h1="Создаём персонажей на экране",
        lede="Первые персонажи — простые фигуры, рисуемые заново на каждом кадре.",
        body_html=body,
        sidebar_groups=sidebar("20-03-personazhi.html"),
        nav=PageNav(prev_href="20-02-igrovoj-ekran.html", prev_label="Игровой экран", next_href="20-04-peremeshenie-klavishi.html", next_label="Движение и клавиши"),
    )
    write("20-03-personazhi.html", out)


def build_04() -> None:
    body = f"""
    <h2>Перемещаем персонажей</h2>
    <p>«Движение» в Pygame — это просто изменение переменных позиции на каждом кадре перед тем,
    как персонаж будет нарисован заново:</p>
    {code_block(
        "peremeshenie.py",
        "x_igroka += skorost_x\n"
        "pygame.draw.rect(screen, CVET_IGROKA, (x_igroka, y_igroka, 40, 40))\n",
    )}

    <h2 id="klavishi">События нажатия клавиш</h2>
    <p>Есть два способа узнать о клавиатуре. Первый — через события, как в
    <code class="inline">pygame.event.get()</code> (удобно для разовых действий вроде прыжка):</p>
    {code_block(
        "sobytiya_klavish.py",
        "for event in pygame.event.get():\n"
        "    if event.type == pygame.KEYDOWN:\n"
        "        if event.key == pygame.K_SPACE:\n"
        '            print("Прыжок!")\n',
    )}
    <p>Второй способ — проверка текущего состояния клавиш на каждом кадре (удобнее для
    непрерывного движения, например, персонажа влево-вправо):</p>
    {code_block(
        "sostoyanie_klavish.py",
        "klavishi = pygame.key.get_pressed()\n"
        "if klavishi[pygame.K_LEFT]:\n"
        "    x_igroka -= 5\n"
        "if klavishi[pygame.K_RIGHT]:\n"
        "    x_igroka += 5\n",
    )}
    {callout(
        "tip",
        "Какой способ выбрать?",
        "События (<code class=\"inline\">event.type == pygame.KEYDOWN</code>) подходят для "
        "действий «один раз за нажатие» — прыжок, выстрел, пауза. "
        "<code class=\"inline\">get_pressed()</code> подходит для непрерывного движения, пока "
        "клавиша зажата, — именно так реализовано управление кораблём в главе 21.",
    )}

    {local_required_card(
        "20-04",
        "Практика: движение и клавиши",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/20-04/index.html",
    )}
    """
    out = render_page(
        page_title="Перемещаем персонажей. События клавиш",
        description="Движение персонажей изменением координат и два способа обработки клавиатуры в Pygame.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 20", "index.html"), ("Движение и клавиши", "")],
        kicker="Глава 20 · Станьте разработчиком игр с Pygame",
        h1="Перемещаем персонажей",
        lede="Движение — это просто изменение координат на каждом кадре; клавиатуру можно "
        "проверять двумя разными способами.",
        body_html=body,
        sidebar_groups=sidebar("20-04-peremeshenie-klavishi.html"),
        nav=PageNav(prev_href="20-03-personazhi.html", prev_label="Персонажи", next_href="20-05-mini-proekt-myach-itogi.html", next_label="Прыгающий мяч и итоги"),
    )
    write("20-04-peremeshenie-klavishi.html", out)


def build_05() -> None:
    body = f"""
    <p>Соберём всё в один мини-проект: мяч, который отскакивает от всех четырёх стен экрана.</p>
    {code_block(
        "prygayushij_myach.py",
        "import pygame\n\n"
        "SHIRINA, VYSOTA = 600, 400\n"
        "RADIUS = 20\n\n"
        "pygame.init()\n"
        "screen = pygame.display.set_mode((SHIRINA, VYSOTA))\n"
        "clock = pygame.time.Clock()\n\n"
        "x, y = SHIRINA // 2, VYSOTA // 2\n"
        "dx, dy = 4, 3\n\n"
        "rabotaet = True\n"
        "while rabotaet:\n"
        "    for event in pygame.event.get():\n"
        "        if event.type == pygame.QUIT:\n"
        "            rabotaet = False\n\n"
        "    x += dx\n"
        "    y += dy\n\n"
        "    if x - RADIUS < 0 or x + RADIUS > SHIRINA:\n"
        "        dx = -dx\n"
        "    if y - RADIUS < 0 or y + RADIUS > VYSOTA:\n"
        "        dy = -dy\n\n"
        "    screen.fill((20, 20, 40))\n"
        "    pygame.draw.circle(screen, (255, 100, 100), (int(x), int(y)), RADIUS)\n"
        "    pygame.display.flip()\n"
        "    clock.tick(60)\n\n"
        "pygame.quit()\n",
    )}
    {callout(
        "info",
        "dx = -dx — отражение одной строкой",
        "Смена знака скорости на противоположный — стандартный приём отражения от стены: "
        "движение продолжается с той же скоростью, только в обратную сторону, без "
        "дополнительных проверок направления.",
    )}
    <p>Полный, уже проверенный файл — отдельно:</p>
    <p>📄 <a href="../../../projects/pygame/bouncing-ball/bouncing_ball.py">projects/pygame/bouncing-ball/bouncing_ball.py</a></p>

    {exercise(2, "Меняем цвет при отскоке", "При каждом отскоке от стены выбирайте новый случайный цвет мяча (random.choice() из главы 5/11).")}
    {exercise(3, "Два мяча", "Добавьте второй мяч с собственными x, y, dx, dy — оба должны двигаться и отскакивать независимо.")}

{local_required_card(
        "20-05",
        "Практика: прыгающий мяч",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/20-05/index.html",
    )}

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
        "Pygame не входит в стандартную поставку Python — устанавливается через "
        "<code class=\"inline\">pip install</code>.",
        "Игровой цикл в Pygame пишут вручную: обработка событий → обновление позиций → "
        "перерисовка → <code class=\"inline\">clock.tick(FPS)</code>.",
        "<code class=\"inline\">screen.fill()</code> в начале каждого кадра предотвращает "
        "«следы» от предыдущих кадров.",
        "Персонажей рисуют заново на каждом кадре — движение реализуется просто изменением "
        "координат перед отрисовкой.",
        "Клавиатуру проверяют либо через события (разовые действия), либо через "
        "<code class=\"inline\">pygame.key.get_pressed()</code> (непрерывное движение).",
    ])}
    """
    out = render_page(
        page_title="Мини-проект — прыгающий мяч",
        description="Итоговый мини-проект главы 20: мяч, отскакивающий от всех стен экрана — и краткие итоги.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 20", "index.html"), ("Прыгающий мяч", "")],
        kicker="Глава 20 · Станьте разработчиком игр с Pygame",
        h1="Мини-проект — прыгающий мяч",
        lede="Первая настоящая мини-игра на Pygame — движение, отскоки и игровой цикл в одном "
        "коротком проекте.",
        body_html=body,
        sidebar_groups=sidebar("20-05-mini-proekt-myach-itogi.html"),
        nav=PageNav(prev_href="20-04-peremeshenie-klavishi.html", prev_label="Движение и клавиши", next_href="../glava-21/index.html", next_label="Глава 21: Проект: космический шутер с Pygame"),
    )
    write("20-05-mini-proekt-myach-itogi.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_opener()
    build_01()
    build_02()
    build_03()
    build_04()
    build_05()
