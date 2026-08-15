#!/usr/bin/env python3
"""Строит Главу 21: «Проект: космический шутер с Pygame» (site/chapters/glava-21/)."""

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
OUT_DIR = ROOT / "site" / "chapters" / "glava-21"

PAGES = [
    ("index.html", "Обзор главы"),
    ("21-01-igra-import-init.html", "Игра, импорт и инициализация"),
    ("21-02-cikl-korabl.html", "Игровой цикл и корабль"),
    ("21-03-dvizhenie-vragi.html", "Движение корабля и врагов"),
    ("21-04-strelba.html", "Стреляем"),
    ("21-05-tablo-scheta.html", "Табло счёта"),
    ("21-06-unichtozhenie.html", "Уничтожаем врагов и корабль"),
    ("21-07-game-over.html", "Перерисовка и «Игра окончена!»"),
    ("21-08-polnyj-kod-itogi.html", "Полный код и итоги"),
]

NOTEBOOKS = [
    "21-01-init.ipynb",
    "21-02-korabl.ipynb",
    "21-03-dvizhenie-vragi.ipynb",
    "21-04-strelba.ipynb",
    "21-06-unichtozhenie.ipynb",
    "21-08-polnaya-igra.ipynb",
]

LESSON_IDS = ["21-01", "21-02", "21-03", "21-04", "21-06", "21-08"]


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 21 · Космический шутер", items),
        SidebarGroup(
            "Практика",
            [NavItem(f"🐍 {lid}: Практика", f"../../practice/{lid}/index.html") for lid in LESSON_IDS],
        ),
        SidebarGroup("Исходный код", [NavItem("🐍 space_shooter.py", "../../../projects/pygame/space-shooter/space_shooter.py")]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=21,
        baseline_page=467,
        title="Проект: космический шутер с Pygame",
        description="Самая крупная игра книги — корабль, враги, стрельба, счёт и конец игры, собранные шаг за шагом.",
        meta_items=["⏱ ~5 часов", "🚀 полноценная игра", "📓 6 ноутбуков практики"],
        sections=[
            ChapterSectionLink("21.1", "Игра «Космический шутер»", "21-01-igra-import-init.html", "467"),
            ChapterSectionLink("", "Импортируем модули. Инициализируем", "21-01-igra-import-init.html#init", "469"),
            ChapterSectionLink("21.2", "Игровой цикл", "21-02-cikl-korabl.html", "470"),
            ChapterSectionLink("", "Создаём космический корабль", "21-02-cikl-korabl.html#korabl", "471"),
            ChapterSectionLink("21.3", "Перемещаем корабль", "21-03-dvizhenie-vragi.html", "473"),
            ChapterSectionLink("", "Создаём и перемещаем врагов", "21-03-dvizhenie-vragi.html#vragi", "475"),
            ChapterSectionLink("21.4", "Стреляем", "21-04-strelba.html", "479"),
            ChapterSectionLink("21.5", "Табло счёта", "21-05-tablo-scheta.html", "482"),
            ChapterSectionLink("21.6", "Уничтожаем врагов", "21-06-unichtozhenie.html", "484"),
            ChapterSectionLink("", "Уничтожаем космический корабль!", "21-06-unichtozhenie.html#korabl-unichtozhen", "487"),
            ChapterSectionLink("21.7", "Перерисовываем врагов. Игра окончена!", "21-07-game-over.html", "488"),
            ChapterSectionLink("21.8", "Полный код", "21-08-polnyj-kod-itogi.html", "491"),
            ChapterSectionLink("", "Итоги", "21-08-polnyj-kod-itogi.html#itogi", "496"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <h2>Игра «Космический шутер»</h2>
    <p>Самый крупный проект книги: корабль игрока внизу экрана, враги, спускающиеся сверху,
    возможность стрелять и уничтожать врагов, счёт очков и полноценный конец игры. Каждая
    часть уже знакома по предыдущим главам — просто теперь они работают вместе.</p>

    <h2 id="init">Импортируем необходимые модули</h2>
    {code_block("importy.py", "import random\nimport pygame\n")}

    <h2>Инициализируем всё необходимое</h2>
    {code_block(
        "inicializaciya.py",
        "SHIRINA, VYSOTA = 500, 600\n"
        "FPS = 60\n\n"
        "pygame.init()\n"
        "screen = pygame.display.set_mode((SHIRINA, VYSOTA))\n"
        'pygame.display.set_caption("Космический шутер")\n'
        "clock = pygame.time.Clock()\n"
        "shrift = pygame.font.SysFont(None, 32)\n",
    )}
    {callout(
        "info",
        "pygame.font — ещё один модуль Pygame",
        "<code class=\"inline\">pygame.font.SysFont(None, 32)</code> создаёт шрифт системным "
        "по умолчанию, размером 32 — понадобится для табло счёта в разделе 21.5.",
    )}

    {local_required_card(
        "21-01",
        "Практика: импорт и инициализация",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/21-01/index.html",
    )}
    """
    out = render_page(
        page_title="Игра, импорт и инициализация",
        description="План проекта «Космический шутер», необходимые модули и первоначальная настройка Pygame.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Игра, импорт, инициализация", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Игра «Космический шутер»",
        lede="Самая крупная игра книги — все части уже знакомы, теперь они работают вместе.",
        body_html=body,
        sidebar_groups=sidebar("21-01-igra-import-init.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="21-02-cikl-korabl.html", next_label="Игровой цикл и корабль"),
    )
    write("21-01-igra-import-init.html", out)


def build_02() -> None:
    body = f"""
    <h2>Игровой цикл</h2>
    <p>Как и в главе 20, цикл — сердце игры. На этот раз он будет обновлять сразу несколько
    вещей на каждом кадре: положение корабля, врагов, пуль — и проверять столкновения:</p>
    {code_block(
        "igrovoj_cikl_plan.py",
        "while rabotaet:\n"
        "    # 1. обработать события (выход, выстрел)\n"
        "    # 2. обработать зажатые клавиши (движение корабля)\n"
        "    # 3. обновить положение врагов и пуль, проверить столкновения\n"
        "    # 4. нарисовать всё заново\n"
        "    # 5. clock.tick(FPS)\n",
    )}

    <h2 id="korabl">Создаём космический корабль</h2>
    <p>Вместо отдельных переменных x, y корабля удобно использовать
    <code class="inline">pygame.Rect</code> — он сразу хранит позицию и размер вместе и
    понадобится для проверки столкновений:</p>
    {code_block(
        "korabl.py",
        "KORABL_SHIRINA, KORABL_VYSOTA = 50, 40\n\n"
        "korabl = pygame.Rect(\n"
        "    SHIRINA // 2 - KORABL_SHIRINA // 2,\n"
        "    VYSOTA - KORABL_VYSOTA - 20,\n"
        "    KORABL_SHIRINA,\n"
        "    KORABL_VYSOTA,\n"
        ")\n\n"
        "# в игровом цикле:\n"
        "pygame.draw.rect(screen, (80, 220, 120), korabl)\n",
    )}
    {callout(
        "tip",
        "Rect хранит четыре числа — и много полезных свойств",
        "<code class=\"inline\">Rect(x, y, ширина, высота)</code> дополнительно вычисляет "
        "<code class=\"inline\">.centerx</code>, <code class=\"inline\">.bottom</code>, "
        "<code class=\"inline\">.top</code> и другие удобные координаты — они пригодятся уже "
        "в следующем разделе.",
    )}

    {local_required_card(
        "21-02",
        "Практика: Rect и первый корабль",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/21-02/index.html",
    )}
    """
    out = render_page(
        page_title="Игровой цикл. Создаём космический корабль",
        description="План игрового цикла шутера и создание корабля игрока через pygame.Rect.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Цикл и корабль", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Игровой цикл",
        lede="План того, что должно происходить на каждом кадре — и первый персонаж игры.",
        body_html=body,
        sidebar_groups=sidebar("21-02-cikl-korabl.html"),
        nav=PageNav(prev_href="21-01-igra-import-init.html", prev_label="Игра, импорт, инициализация", next_href="21-03-dvizhenie-vragi.html", next_label="Движение и враги"),
    )
    write("21-02-cikl-korabl.html", out)


def build_03() -> None:
    body = f"""
    <h2>Перемещаем космический корабль</h2>
    <p>Управление — через <code class="inline">get_pressed()</code> из главы 20 (непрерывное
    движение, пока клавиша зажата), с ограничением, чтобы корабль не улетел за края экрана:</p>
    {code_block(
        "dvizhenie_korablya.py",
        "KORABL_SKOROST = 6\n\n"
        "def obrabotat_klavishi(korabl, klavishi):\n"
        "    if klavishi[pygame.K_LEFT]:\n"
        "        korabl.x -= KORABL_SKOROST\n"
        "    if klavishi[pygame.K_RIGHT]:\n"
        "        korabl.x += KORABL_SKOROST\n"
        "    korabl.x = max(0, min(korabl.x, SHIRINA - KORABL_SHIRINA))\n",
    )}
    {callout(
        "tip",
        "max/min — тот же приём ограничения, что и в главе 20",
        "<code class=\"inline\">max(0, min(korabl.x, SHIRINA - KORABL_SHIRINA))</code> "
        "гарантирует, что <code class=\"inline\">korabl.x</code> никогда не выйдет за пределы "
        "<code class=\"inline\">[0, SHIRINA - KORABL_SHIRINA]</code> — тот же самый приём "
        "«зажимания» значения в диапазон, что мы использовали для прыгающего мяча.",
    )}

    <h2 id="vragi">Создаём и перемещаем врагов</h2>
    <p>Врагов будет много, и они появляются со временем — значит, нужен список (глава 11) и
    счётчик кадров до следующего появления:</p>
    {code_block(
        "vragi.py",
        "VRAG_SHIRINA, VRAG_VYSOTA = 40, 30\n"
        "VRAG_SKOROST = 2\n"
        "INTERVAL_POYAVLENIYA_VRAGA = 45   # кадров между новыми врагами\n\n"
        "vragi = []\n"
        "kadrov_do_vraga = INTERVAL_POYAVLENIYA_VRAGA\n\n"
        "def sozdat_vraga():\n"
        "    x = random.randint(0, SHIRINA - VRAG_SHIRINA)\n"
        "    return pygame.Rect(x, -VRAG_VYSOTA, VRAG_SHIRINA, VRAG_VYSOTA)\n\n"
        "# в игровом цикле, каждый кадр:\n"
        "kadrov_do_vraga -= 1\n"
        "if kadrov_do_vraga <= 0:\n"
        "    vragi.append(sozdat_vraga())\n"
        "    kadrov_do_vraga = INTERVAL_POYAVLENIYA_VRAGA\n\n"
        "for vrag in vragi:\n"
        "    vrag.y += VRAG_SKOROST\n",
    )}
    {callout(
        "info",
        "y = -VRAG_VYSOTA — враг появляется чуть выше экрана",
        "Отрицательная стартовая координата Y означает, что враг рождается чуть выше видимой "
        "области и плавно «въезжает» в кадр сверху — а не появляется резко посередине экрана.",
    )}

    {local_required_card(
        "21-03",
        "Практика: движение корабля и врагов",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/21-03/index.html",
    )}
    """
    out = render_page(
        page_title="Перемещаем корабль. Создаём и перемещаем врагов",
        description="Управление кораблём с ограничением по краям экрана и периодическое появление врагов.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Движение и враги", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Перемещаем космический корабль",
        lede="Управление с ограничением по краям экрана — и первые враги, появляющиеся сверху.",
        body_html=body,
        sidebar_groups=sidebar("21-03-dvizhenie-vragi.html"),
        nav=PageNav(prev_href="21-02-cikl-korabl.html", prev_label="Цикл и корабль", next_href="21-04-strelba.html", next_label="Стреляем"),
    )
    write("21-03-dvizhenie-vragi.html", out)


def build_04() -> None:
    body = f"""
    <p>Пули — тоже список <code class="inline">Rect</code>, появляющийся у носа корабля при
    нажатии пробела и улетающий вверх на каждом кадре:</p>
    {code_block(
        "strelba.py",
        "PULYA_SHIRINA, PULYA_VYSOTA = 4, 12\n"
        "PULYA_SKOROST = 9\n\n"
        "puli = []\n\n"
        "def vystrelit():\n"
        "    pulya = pygame.Rect(\n"
        "        korabl.centerx - PULYA_SHIRINA // 2,\n"
        "        korabl.top,\n"
        "        PULYA_SHIRINA,\n"
        "        PULYA_VYSOTA,\n"
        "    )\n"
        "    puli.append(pulya)\n\n"
        "# в обработке событий:\n"
        "if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:\n"
        "    vystrelit()\n\n"
        "# в обновлении кадра:\n"
        "for pulya in puli:\n"
        "    pulya.y -= PULYA_SKOROST\n"
        "puli = [p for p in puli if p.bottom > 0]   # убираем улетевшие за экран\n",
    )}
    {callout(
        "tip",
        "Список через генератор списков — чистка «мусора»",
        "<code class=\"inline\">[p for p in puli if p.bottom &gt; 0]</code> (генератор списков "
        "из главы 11) оставляет только те пули, что ещё видны на экране — без этой строки "
        "список пуль рос бы бесконечно, замедляя игру всё сильнее.",
    )}

    {local_required_card(
        "21-04",
        "Практика: стрельба и движение пуль",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/21-04/index.html",
    )}
    """
    out = render_page(
        page_title="Стреляем",
        description="Создаём пули, реагируем на пробел и убираем пули, улетевшие за пределы экрана.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Стреляем", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Стреляем",
        lede="Пробел создаёт пулю у носа корабля — она улетает вверх, пока не покинет экран.",
        body_html=body,
        sidebar_groups=sidebar("21-04-strelba.html"),
        nav=PageNav(prev_href="21-03-dvizhenie-vragi.html", prev_label="Движение и враги", next_href="21-05-tablo-scheta.html", next_label="Табло счёта"),
    )
    write("21-04-strelba.html", out)


def build_05() -> None:
    body = f"""
    <p>Счёт выводится готовым шрифтом Pygame (<code class="inline">pygame.font</code>, раздел
    21.1) — в отличие от Turtle, здесь текст сначала «отрисовывается» в отдельное изображение
    (<code class="inline">render()</code>), а затем накладывается на экран
    (<code class="inline">blit()</code>):</p>
    {code_block(
        "tablo_scheta.py",
        "schet = 0\n\n"
        "# в отрисовке кадра:\n"
        'tablo = shrift.render(f"Счёт: {schet}", True, (255, 255, 255))\n'
        "screen.blit(tablo, (10, 10))\n",
    )}
    {callout(
        "info",
        "render() + blit() — тот же принцип, что write() у Turtle",
        "<code class=\"inline\">render(текст, сглаживание, цвет)</code> создаёт изображение "
        "текста; <code class=\"inline\">screen.blit(изображение, позиция)</code> накладывает "
        "его на экран — концептуально то же самое, что <code class=\"inline\">artist.write()"
        "</code> у Turtle из главы 7, просто в два явных шага вместо одного.",
    )}

    {local_required_card(
        "21-03",
        "Практика: включает вывод счёта",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/21-03/index.html",
    )}
    """
    out = render_page(
        page_title="Запускаем табло счёта",
        description="Отрисовка текста счёта через pygame.font: render() и blit().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Табло счёта", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Запускаем табло счёта",
        lede="Текст в Pygame рисуется в два шага: сначала render(), потом blit() на экран.",
        body_html=body,
        sidebar_groups=sidebar("21-05-tablo-scheta.html"),
        nav=PageNav(prev_href="21-04-strelba.html", prev_label="Стреляем", next_href="21-06-unichtozhenie.html", next_label="Уничтожаем врагов и корабль"),
    )
    write("21-05-tablo-scheta.html", out)


def build_06() -> None:
    body = f"""
    <h2>Уничтожаем врагов</h2>
    <p>Столкновение пули с врагом проверяет готовый метод <code class="inline">Rect.colliderect()</code>
    — при попадании оба удаляются из своих списков, а счёт увеличивается:</p>
    {code_block(
        "unichtozhenie_vragov.py",
        "novye_puli = []\n"
        "novye_vragi = list(vragi)\n"
        "for pulya in puli:\n"
        "    popala = False\n"
        "    for vrag in list(novye_vragi):\n"
        "        if pulya.colliderect(vrag):\n"
        "            novye_vragi.remove(vrag)\n"
        "            schet += 10\n"
        "            popala = True\n"
        "            break\n"
        "    if not popala:\n"
        "        novye_puli.append(pulya)\n"
        "puli = novye_puli\n"
        "vragi = novye_vragi\n",
    )}
    {callout(
        "warning",
        "Почему не удалять элементы прямо во время перебора списка?",
        "Удаление элемента из списка <code class=\"inline\">vragi</code> прямо внутри цикла "
        "<code class=\"inline\">for vrag in vragi:</code> может пропустить соседние элементы "
        "— список «сдвигается» под ногами цикла. Безопаснее собрать <strong>новые</strong> "
        "списки уцелевших пуль и врагов, как показано выше.",
    )}

    <h2 id="korabl-unichtozhen">Уничтожаем космический корабль!</h2>
    <p>Если враг долетел до низа экрана или столкнулся с кораблём — игра заканчивается:</p>
    {code_block(
        "unichtozhenie_korablya.py",
        "for vrag in vragi:\n"
        "    if vrag.bottom >= VYSOTA or vrag.colliderect(korabl):\n"
        "        igra_okonchena = True\n"
        "        break\n",
    )}

    {local_required_card(
        "21-06",
        "Практика: столкновения пуль, врагов и корабля",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/21-06/index.html",
    )}
    """
    out = render_page(
        page_title="Уничтожаем врагов и корабль",
        description="Проверка столкновений pulya.colliderect(vrag) и условия окончания игры.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Уничтожение", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Уничтожаем врагов",
        lede="colliderect() проверяет столкновения — попадание уничтожает врага, а враг может "
        "уничтожить корабль.",
        body_html=body,
        sidebar_groups=sidebar("21-06-unichtozhenie.html"),
        nav=PageNav(prev_href="21-05-tablo-scheta.html", prev_label="Табло счёта", next_href="21-07-game-over.html", next_label="Перерисовка и Game Over"),
    )
    write("21-06-unichtozhenie.html", out)


def build_07() -> None:
    body = f"""
    <h2>Перерисовываем врагов</h2>
    <p>После всех проверок и обновлений кадр рисуется заново целиком — фон, корабль, пули,
    враги и счёт, в таком порядке (чтобы более поздние элементы оказывались поверх более
    ранних):</p>
    {code_block(
        "pererisovka.py",
        "screen.fill((10, 10, 20))\n"
        "pygame.draw.rect(screen, (80, 220, 120), korabl)\n"
        "for pulya in puli:\n"
        "    pygame.draw.rect(screen, (240, 220, 80), pulya)\n"
        "for vrag in vragi:\n"
        "    pygame.draw.rect(screen, (230, 60, 60), vrag)\n\n"
        'tablo = shrift.render(f"Счёт: {schet}", True, (255, 255, 255))\n'
        "screen.blit(tablo, (10, 10))\n\n"
        "pygame.display.flip()\n",
    )}

    <h2>Игра окончена!</h2>
    <p>Когда <code class="inline">igra_okonchena</code> становится истинной, вместо обычной
    игровой логики выводится финальный экран:</p>
    {code_block(
        "game_over.py",
        "if igra_okonchena:\n"
        '    nadpis = shrift_bolshoj.render("ИГРА ОКОНЧЕНА", True, (255, 255, 255))\n'
        "    rect = nadpis.get_rect(center=(SHIRINA // 2, VYSOTA // 2))\n"
        "    screen.blit(nadpis, rect)\n",
    )}
    {callout(
        "tip",
        "get_rect(center=...) — удобное центрирование текста",
        "Вместо ручного вычисления координат текста по его ширине и высоте, "
        "<code class=\"inline\">get_rect(center=(x, y))</code> сам находит нужный левый "
        "верхний угол так, чтобы текст оказался центрирован ровно в точке "
        "<code class=\"inline\">(x, y)</code>.",
    )}

    {local_required_card(
        "21-06",
        "Практика: включает финальный экран",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/21-06/index.html",
    )}
    """
    out = render_page(
        page_title="Перерисовываем врагов. Игра окончена!",
        description="Полная перерисовка кадра каждый цикл и финальный экран «Игра окончена».",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Перерисовка и Game Over", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Перерисовываем врагов",
        lede="Каждый кадр рисуется заново целиком — а при окончании игры на экране появляется "
        "финальная надпись.",
        body_html=body,
        sidebar_groups=sidebar("21-07-game-over.html"),
        nav=PageNav(prev_href="21-06-unichtozhenie.html", prev_label="Уничтожение", next_href="21-08-polnyj-kod-itogi.html", next_label="Полный код и итоги"),
    )
    write("21-07-game-over.html", out)


def build_08() -> None:
    body = f"""
    <p>Полная, уже собранная и проверенная игра — отдельным файлом:</p>
    <p>📄 <a href="../../../projects/pygame/space-shooter/space_shooter.py">projects/pygame/space-shooter/space_shooter.py</a></p>
    {callout(
        "tip",
        "Запустите игру у себя",
        "<code class=\"inline\">python space_shooter.py</code> в терминале. Управление: "
        "стрелки влево/вправо — движение, пробел — выстрел.",
    )}

    {exercise(2, "Жизни вместо мгновенного конца", "Добавьте переменную zhizni = 3 — при столкновении корабля с врагом отнимайте одну жизнь и убирайте врага, вместо немедленного окончания игры.")}
    {exercise(3, "Уровни сложности", "Постепенно уменьшайте INTERVAL_POYAVLENIYA_VRAGA по мере роста счёта — враги должны появляться всё чаще.")}

{local_required_card(
        "21-08",
        "Практика: полная игра",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/21-08/index.html",
    )}

    <h2 id="itogi">Итоги</h2>
    {summary_box("Что мы узнали в этой главе", [
        "Крупный проект строится из уже знакомых, более мелких приёмов — корабль, враги и "
        "пули устроены похоже, просто с разными правилами движения.",
        "<code class=\"inline\">pygame.Rect</code> хранит позицию и размер вместе и умеет "
        "проверять столкновения через <code class=\"inline\">.colliderect()</code>.",
        "При удалении элементов по условию безопаснее собрать новый список уцелевших "
        "элементов, чем изменять список во время перебора.",
        "Текст в Pygame рисуется в два шага: <code class=\"inline\">render()</code> создаёт "
        "изображение, <code class=\"inline\">blit()</code> накладывает его на экран.",
        "Порядок отрисовки элементов кадра определяет, что окажется «поверх» — рисуйте фон "
        "первым, интерфейс (счёт, финальный экран) — последним.",
    ])}
    """
    out = render_page(
        page_title="Полный код и итоги",
        description="Ссылка на полный исходный код космического шутера и итоги главы 21.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Полный код и итоги", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Полный код",
        lede="Вся игра целиком — уже собранная и проверенная — и подведение итогов главы.",
        body_html=body,
        sidebar_groups=sidebar("21-08-polnyj-kod-itogi.html"),
        nav=PageNav(prev_href="21-07-game-over.html", prev_label="Перерисовка и Game Over", next_href="../glava-22/index.html", next_label="Глава 22: Веб-разработка с Python"),
    )
    write("21-08-polnyj-kod-itogi.html", out)


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
