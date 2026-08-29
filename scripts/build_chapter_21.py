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
    capability_map,
    class_diagram,
    code_block,
    comparison_table,
    decision_map,
    exercise,
    image_figure,
    local_required_card,
    object_diagram,
    pipeline_diagram,
    practice_card,
    practice_revisit_card,
    relationship_diagram,
    render_chapter_opener,
    render_page,
    summary_box,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-21"
IMG = "../../assets/img/chapter-21/output"

PAGES = [
    ("index.html", "Обзор главы"),
    ("21-01-igra-import-init.html", "План игры и подготовка проекта"),
    ("21-02-cikl-korabl.html", "Игровой цикл и корабль игрока"),
    ("21-03-dvizhenie-vragi.html", "Движение корабля и появление врагов"),
    ("21-04-strelba.html", "Стрельба: создаём и двигаем пули"),
    ("21-05-tablo-scheta.html", "Счёт и информация на экране"),
    ("21-06-unichtozhenie.html", "Попадания и столкновения"),
    ("21-07-game-over.html", "Завершение игры и экран «Игра окончена»"),
    ("21-08-polnyj-kod-itogi.html", "Первая рабочая версия игры"),
    ("21-09-arhitektura-proekta.html", "Разделяем игру на классы"),
    ("21-10-assety-i-zvuk.html", "Ресурсы игры: графика и звук"),
    ("21-11-vector2-tochnoe-dvizhenie.html", "Точное движение с Vector2"),
    ("21-12-igrovoe-pole-i-hud.html", "Игровое поле и интерфейс игрока"),
    ("21-13-skorostrelnost.html", "Скорострельность и интервал между выстрелами"),
    ("21-14-poyavlenie-vragov.html", "Как появляются враги"),
    ("21-15-stolknoveniya-i-schet.html", "Попадания во врагов и начисление очков"),
    ("21-16-uron-i-neuyazvimost.html", "Жизни, урон и временная неуязвимость"),
    ("21-17-slozhnost-i-volny.html", "Как растёт сложность игры"),
    ("21-18-sostoyaniya-igry.html", "Меню, игра, пауза и завершение"),
    ("21-19-perezapusk.html", "Перезапуск игры без перезапуска программы"),
    ("21-20-animatsiya-vzryva.html", "Анимация взрыва"),
    ("21-21-zvukovye-effekty.html", "Звуки выстрела, попадания и взрыва"),
    ("21-22-zvyozdnyj-fon.html", "Звёздный фон и порядок отрисовки"),
    ("21-23-otladka-shutera.html", "Как находить и исправлять ошибки в шутере"),
    ("21-24-testiruemost.html", "Как сделать игру удобной для автоматических тестов"),
    ("21-25-finalnaya-arhitektura.html", "Собираем финальную версию игры"),
    ("21-26-itogi-proekta.html", "Что мы построили и как развивать игру дальше"),
]

NOTEBOOKS = [
    "21-01-init.ipynb",
    "21-02-korabl.ipynb",
    "21-03-dvizhenie-vragi.ipynb",
    "21-04-strelba.ipynb",
    "21-06-unichtozhenie.ipynb",
    "21-08-polnaya-igra.ipynb",
    "21-09-arhitektura.ipynb",
    "21-11-vector2.ipynb",
    "21-13-skorostrelnost.ipynb",
    "21-14-poyavlenie-vragov.ipynb",
    "21-15-stolknoveniya.ipynb",
    "21-16-uron.ipynb",
    "21-17-slozhnost.ipynb",
    "21-20-animatsiya.ipynb",
    "21-25-final.ipynb",
]

LESSON_IDS = [
    "21-01", "21-02", "21-03", "21-04", "21-06", "21-08",
    "21-09", "21-11", "21-13", "21-14", "21-15", "21-16", "21-17", "21-20", "21-25",
]

LOCAL_REQUIRED_IDS = {"21-01", "21-02", "21-03", "21-04", "21-06", "21-08", "21-09", "21-25"}
PYODIDE_IDS = {"21-11", "21-13", "21-14", "21-15", "21-16", "21-17", "21-20"}


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 21 · Космический шутер", items),
        SidebarGroup(
            "Практика",
            [NavItem(f"[[icon:practice]] {lid}: Практика", f"../../practice/{lid}/index.html") for lid in LESSON_IDS],
        ),
        SidebarGroup("Исходный код", [NavItem("[[icon:code]] space_shooter.py", "../../../projects/pygame/space-shooter/space_shooter.py")]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    clean = "\n".join(line.rstrip() for line in html_out.split("\n"))
    path.write_text(clean, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=21,
        description="Самый крупный проект книги — корабль, враги, стрельба, счёт, жизни, сложность и "
        "полноценный конец игры, собранные в архитектуру на классах и делта-тайме.",
        meta_items=["[[icon:timer]] ~10–12 часов", "[[icon:launch]] полноценная игра", "[[icon:practice]] 15 практик"],
        sections=[
            ChapterSectionLink("21.1", "План игры и подготовка проекта", "21-01-igra-import-init.html"),
            ChapterSectionLink("", "Импортируем необходимые модули", "21-01-igra-import-init.html#init"),
            ChapterSectionLink("21.2", "Игровой цикл и корабль игрока", "21-02-cikl-korabl.html"),
            ChapterSectionLink("", "Создаём космический корабль", "21-02-cikl-korabl.html#korabl"),
            ChapterSectionLink("21.3", "Движение корабля и появление врагов", "21-03-dvizhenie-vragi.html"),
            ChapterSectionLink("", "Создаём и перемещаем врагов", "21-03-dvizhenie-vragi.html#vragi"),
            ChapterSectionLink("21.4", "Стрельба: создаём и двигаем пули", "21-04-strelba.html"),
            ChapterSectionLink("21.5", "Счёт и информация на экране", "21-05-tablo-scheta.html"),
            ChapterSectionLink("21.6", "Попадания и столкновения", "21-06-unichtozhenie.html"),
            ChapterSectionLink("", "Когда враг уничтожает корабль", "21-06-unichtozhenie.html#korabl-unichtozhen"),
            ChapterSectionLink("21.7", "Завершение игры и экран «Игра окончена»", "21-07-game-over.html"),
            ChapterSectionLink("21.8", "Первая рабочая версия игры", "21-08-polnyj-kod-itogi.html"),
            # С 21.9 главу продолжают страницы, добавленные в цифровой версии
            # книги — у них нет физической страницы бумажного макета (см.
            # render_chapter_opener() / раздел 20.1 сайта), поэтому page здесь
            # намеренно не указывается.
            ChapterSectionLink("21.9", "Разделяем игру на классы", "21-09-arhitektura-proekta.html"),
            ChapterSectionLink("21.10", "Ресурсы игры: графика и звук", "21-10-assety-i-zvuk.html"),
            ChapterSectionLink("21.11", "Точное движение с Vector2", "21-11-vector2-tochnoe-dvizhenie.html"),
            ChapterSectionLink("21.12", "Игровое поле и интерфейс игрока", "21-12-igrovoe-pole-i-hud.html"),
            ChapterSectionLink("21.13", "Скорострельность и интервал между выстрелами", "21-13-skorostrelnost.html"),
            ChapterSectionLink("21.14", "Как появляются враги", "21-14-poyavlenie-vragov.html"),
            ChapterSectionLink("21.15", "Попадания во врагов и начисление очков", "21-15-stolknoveniya-i-schet.html"),
            ChapterSectionLink("21.16", "Жизни, урон и временная неуязвимость", "21-16-uron-i-neuyazvimost.html"),
            ChapterSectionLink("21.17", "Как растёт сложность игры", "21-17-slozhnost-i-volny.html"),
            ChapterSectionLink("21.18", "Меню, игра, пауза и завершение", "21-18-sostoyaniya-igry.html"),
            ChapterSectionLink("21.19", "Перезапуск игры без перезапуска программы", "21-19-perezapusk.html"),
            ChapterSectionLink("21.20", "Анимация взрыва", "21-20-animatsiya-vzryva.html"),
            ChapterSectionLink("21.21", "Звуки выстрела, попадания и взрыва", "21-21-zvukovye-effekty.html"),
            ChapterSectionLink("21.22", "Звёздный фон и порядок отрисовки", "21-22-zvyozdnyj-fon.html"),
            ChapterSectionLink("21.23", "Как находить и исправлять ошибки в шутере", "21-23-otladka-shutera.html"),
            ChapterSectionLink("21.24", "Как сделать игру удобной для автоматических тестов", "21-24-testiruemost.html"),
            ChapterSectionLink("21.25", "Собираем финальную версию игры", "21-25-finalnaya-arhitektura.html"),
            ChapterSectionLink("21.26", "Что мы построили и как развивать игру дальше", "21-26-itogi-proekta.html"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <p>Этот проект — самая крупная игра книги: корабль игрока, враги, спускающиеся сверху,
    стрельба, уничтожение врагов, счёт очков, жизни, растущая сложность и полноценный конец игры
    с перезапуском. Все составные части уже знакомы по главе 20 — <code class="inline">Rect</code>,
    <code class="inline">colliderect()</code>, спрайты, состояния игры, delta time — здесь они
    впервые работают вместе, в одном учебном проекте.</p>

    {image_figure(f"{IMG}/25-final-gameplay.png", "Реальный кадр готовой игры: синий корабль внизу, несколько врагов разных типов и пуль на игровом поле, HUD со счётом и жизнями сверху", "Реальный кадр финальной версии игры — то, что получится в итоге этой главы.", width=320)}

    <h2 id="init">Импортируем необходимые модули</h2>
    {code_block("importy.py", "import random\nfrom dataclasses import dataclass\nfrom enum import Enum, auto\nfrom pathlib import Path\n\nimport pygame\n")}
    <p><code class="inline">dataclasses</code> (глава 14) и <code class="inline">enum</code> (глава
    13) здесь не случайны: класс-описание типа врага и явные состояния игры — тот же приём, что
    <code class="inline">SostoyanieIgry</code> в разделе 20.25.</p>

    <h2>Инициализируем всё необходимое</h2>
    {code_block(
        "inicializaciya.py",
        "SHIRINA, VYSOTA = 480, 720\n"
        "FPS = 60\n\n"
        "pygame.init()\n"
        "screen = pygame.display.set_mode((SHIRINA, VYSOTA))\n"
        'pygame.display.set_caption("Космический шутер")\n'
        "clock = pygame.time.Clock()\n"
        "shrift = pygame.font.SysFont(None, 28)\n",
    )}
    {callout(
        "info",
        "pygame.font — тот же модуль, что и в главе 20",
        "<code class=\"inline\">pygame.font.SysFont(None, 28)</code> создаёт шрифт системным по "
        "умолчанию, размером 28 — понадобится для табло счёта в разделе 21.5. Полная финальная "
        "версия использует сразу три размера шрифта — обычный, крупный (заголовки экранов) и "
        "мелкий (подписи).",
    )}

    <h2>План проекта</h2>
    <p>Прежде чем писать код, полезно увидеть карту того, что получится в итоге. Финальная версия
    (раздел 21.25) состоит из пяти классов с чёткими обязанностями:</p>
    {capability_map([
        ("Game", ["Владеет всем состоянием игры", "Игровой цикл: события → ввод → обновление → отрисовка", "Переключает состояния MENU/PLAYING/PAUSED/GAME_OVER"]),
        ("Player", ["Позиция как Vector2 (раздел 21.11)", "Движение, ограниченное игровым полем", "Интервал между выстрелами и таймер неуязвимости"]),
        ("Bullet", ["Летит вверх с постоянной скоростью", "Удаляет себя за пределами игрового поля"]),
        ("Enemy", ["Летит вниз с индивидуальной скоростью", "Несёт очки за уничтожение"]),
        ("Explosion", ["Анимация из нескольких кадров", "Удаляет себя после последнего кадра"]),
    ], title="Пять классов финальной игры")}
    <p>Этот раздел и разделы 21.2–21.8 повторяют исторический порядок изложения из бумажной книги
    и намеренно начинают проще, чем финальная версия — с обычных функций и списков, как в главе 20.
    С раздела 21.9 книга объясняет, как и почему этот код вырастает в архитектуру на классах.</p>

    {local_required_card(
        "21-01",
        "Практика: импорт и инициализация",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/21-01/index.html",
    )}
    """
    out = render_page(
        page_title="План игры и подготовка проекта",
        description="План проекта «Космический шутер», пять классов финальной версии и первоначальная настройка Pygame.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("План игры и подготовка проекта", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="План игры и подготовка проекта",
        lede="Самая крупная игра книги — все части уже знакомы по главе 20, здесь они впервые работают вместе.",
        body_html=body,
        sidebar_groups=sidebar("21-01-igra-import-init.html"),
        nav=PageNav(prev_href="index.html", prev_label="Обзор главы", next_href="21-02-cikl-korabl.html", next_label="Игровой цикл и корабль игрока"),
    )
    write("21-01-igra-import-init.html", out)


def build_02() -> None:
    body = f"""
    <h2>Игровой цикл</h2>
    <p>Как и в главе 20, цикл — сердце игры. На этот раз он на каждом кадре обновляет сразу
    несколько вещей: положение корабля, врагов, пуль — и проверяет столкновения между ними. С
    самого первого кадра цикл считает delta time (сокращённо dt) — раздел 20.16 уже объяснял,
    зачем: скорость, заданная в пикселях в секунду и применённая через dt, не зависит от частоты
    кадров конкретного компьютера:</p>
    {code_block(
        "igrovoj_cikl_plan.py",
        "while rabotaet:\n"
        "    dt = clock.tick(FPS) / 1000.0   # секунд с прошлого кадра\n\n"
        "    # 1. обработать события (выход, пауза, выстрел по нажатию)\n"
        "    # 2. обработать зажатые клавиши (движение корабля, удержание огня)\n"
        "    # 3. обновить положение врагов и пуль по dt, проверить столкновения\n"
        "    # 4. нарисовать всё заново\n",
    )}
    {callout(
        "info",
        "dt здесь с самого начала, а не добавляется позже",
        "Мини-проект прыгающего мяча (раздел 20.5) начинался с движения «пикселей за кадр» и "
        "переходил на delta time только в разделе 20.16. Здесь так делать не будем: раз глава 20 "
        "уже объяснила, почему движение «пикселей за кадр» зависит от чужого железа, космический "
        "шутер с первого движущегося объекта считает скорость в пикселях в секунду (px/s) и "
        "применяет её через dt.",
    )}

    <h2 id="korabl">Создаём космический корабль</h2>
    <p>Вместо отдельных переменных x, y корабля удобно использовать
    <code class="inline">pygame.Rect</code> — он сразу хранит позицию и размер вместе и
    понадобится для проверки столкновений:</p>
    {code_block(
        "korabl.py",
        "KORABL_SHIRINA, KORABL_VYSOTA = 44, 44\n\n"
        "korabl = pygame.Rect(\n"
        "    SHIRINA // 2 - KORABL_SHIRINA // 2,\n"
        "    VYSOTA - KORABL_VYSOTA - 20,\n"
        "    KORABL_SHIRINA,\n"
        "    KORABL_VYSOTA,\n"
        ")\n\n"
        "# в игровом цикле:\n"
        "pygame.draw.rect(screen, (80, 220, 120), korabl)\n",
    )}
    {image_figure(f"{IMG}/03-player-ship.png", "Реальное окно: крупный план синего треугольного корабля с оранжевым свечением двигателя внизу", "Финальная версия рисует корабль собственным спрайтом (раздел 21.10), а не прямоугольником — но Rect остаётся его хитбоксом.", width=220)}
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
        page_title="Игровой цикл и корабль игрока",
        description="План игрового цикла шутера с delta time и создание корабля игрока через pygame.Rect.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Игровой цикл и корабль игрока", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Игровой цикл и корабль игрока",
        lede="План того, что должно происходить на каждом кадре — и первый персонаж игры.",
        body_html=body,
        sidebar_groups=sidebar("21-02-cikl-korabl.html"),
        nav=PageNav(prev_href="21-01-igra-import-init.html", prev_label="План игры и подготовка проекта", next_href="21-03-dvizhenie-vragi.html", next_label="Движение корабля и появление врагов"),
    )
    write("21-02-cikl-korabl.html", out)


def build_03() -> None:
    body = f"""
    <h2>Перемещаем космический корабль</h2>
    <p>Управление — через <code class="inline">get_pressed()</code> из главы 20 (непрерывное
    движение, пока клавиша зажата). Скорость сразу задана в пикселях в секунду (px/s), а
    позиция корабля хранится отдельным дробным числом — <code class="inline">Rect</code>
    понимает только целые координаты, и обновлять его напрямую по чуть-чуть на каждом кадре
    значило бы терять дробную часть движения:</p>
    {code_block(
        "dvizhenie_korablya.py",
        "KORABL_SKOROST = 260.0   # px/s\n\n"
        "korabl_x = float(korabl.x)   # дробная копия позиции — сам Rect хранит только целые числа\n\n"
        "def obrabotat_klavishi(korabl_x, klavishi, dt):\n"
        "    napravlenie = klavishi[pygame.K_RIGHT] - klavishi[pygame.K_LEFT]\n"
        "    korabl_x += napravlenie * KORABL_SKOROST * dt\n"
        "    return max(0.0, min(korabl_x, SHIRINA - KORABL_SHIRINA))\n\n"
        "# в игровом цикле:\n"
        "korabl_x = obrabotat_klavishi(korabl_x, klavishi, dt)\n"
        "korabl.x = round(korabl_x)\n",
    )}
    {callout(
        "tip",
        "max/min — тот же приём ограничения, что и в главе 20",
        "<code class=\"inline\">max(0.0, min(korabl_x, SHIRINA - KORABL_SHIRINA))</code> "
        "гарантирует, что <code class=\"inline\">korabl_x</code> никогда не выйдет за пределы "
        "<code class=\"inline\">[0, SHIRINA - KORABL_SHIRINA]</code> — тот же самый приём "
        "«зажимания» значения в диапазон, что мы использовали для прыгающего мяча.",
    )}
    {callout(
        "info",
        "napravlenie — число -1, 0 или 1",
        "<code class=\"inline\">klavishi[pygame.K_RIGHT] - klavishi[pygame.K_LEFT]</code> — булевы "
        "значения <code class=\"inline\">True</code>/<code class=\"inline\">False</code> ведут "
        "себя как 1/0 (глава 9), поэтому разность даёт ровно то, что нужно: 1, если зажата только "
        "правая стрелка, −1, если только левая, и 0, если обе или ни одна. Раздел 21.11 обобщит "
        "этот же приём на два измерения сразу через <code class=\"inline\">Vector2</code>.",
    )}

    <h2 id="vragi">Создаём и перемещаем врагов</h2>
    <p>Враг тоже появится позже как отдельный спрайт-класс (раздел 21.9), а пока — словарь с
    <code class="inline">Rect</code> и дробной координатой Y, по той же причине, что и у корабля.
    Врагов будет много, и они появляются со временем — значит, нужен список (глава 11) и таймер
    в секундах до следующего появления:</p>
    {code_block(
        "vragi.py",
        "VRAG_SHIRINA, VRAG_VYSOTA = 32, 28\n"
        "VRAG_SKOROST = 150.0            # px/s\n"
        "INTERVAL_POYAVLENIYA_VRAGA = 0.75   # секунд между новыми врагами\n\n"
        "vragi = []\n"
        "vremya_do_vraga = INTERVAL_POYAVLENIYA_VRAGA\n\n"
        "def sozdat_vraga():\n"
        "    x = random.randint(0, SHIRINA - VRAG_SHIRINA)\n"
        "    return {{\n"
        "        \"rect\": pygame.Rect(x, -VRAG_VYSOTA, VRAG_SHIRINA, VRAG_VYSOTA),\n"
        "        \"y\": float(-VRAG_VYSOTA),\n"
        "    }}\n\n"
        "# в игровом цикле, каждый кадр:\n"
        "vremya_do_vraga -= dt\n"
        "if vremya_do_vraga <= 0.0:\n"
        "    vragi.append(sozdat_vraga())\n"
        "    vremya_do_vraga += INTERVAL_POYAVLENIYA_VRAGA\n\n"
        "for vrag in vragi:\n"
        "    vrag[\"y\"] += VRAG_SKOROST * dt\n"
        "    vrag[\"rect\"].y = round(vrag[\"y\"])\n",
    )}
    {image_figure(f"{IMG}/07-first-enemy.png", "Реальное окно: маленький оранжевый треугольный враг спускается сверху к синему кораблю игрока", "Реальное окно — маленький «разведчик» (scout), один из двух типов врагов финальной версии (раздел 21.17).", width=220)}
    {callout(
        "info",
        "y = -VRAG_VYSOTA — враг появляется чуть выше экрана",
        "Отрицательная стартовая координата Y означает, что враг рождается чуть выше видимой "
        "области и плавно «въезжает» в кадр сверху — а не появляется резко посередине экрана.",
    )}
    {callout(
        "tip",
        "+= interval, а не = interval — вот что сохраняет остаток",
        "После появления врага мы прибавляем интервал к текущему значению таймера, а не "
        "присваиваем интервал заново. Поэтому небольшое превышение времени не теряется: если "
        "<code class=\"inline\">vremya_do_vraga</code> ушёл в −0.01, следующий отсчёт начнётся "
        "именно с этого небольшого долга, а не с чистого интервала. В разделе 21.14 этот же "
        "принцип будет обобщён с помощью <code class=\"inline\">while</code> на случай, когда "
        "один обрабатываемый шаг может охватить сразу несколько интервалов.",
    )}

    {local_required_card(
        "21-03",
        "Практика: движение корабля и врагов",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/21-03/index.html",
    )}
    """
    out = render_page(
        page_title="Движение корабля и появление врагов",
        description="Управление кораблём в пикселях в секунду с ограничением по краям экрана и появление врагов по таймеру в секундах.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Движение корабля и появление врагов", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Движение корабля и появление врагов",
        lede="Скорость в пикселях в секунду с самого начала — и враги, появляющиеся сверху с течением времени.",
        body_html=body,
        sidebar_groups=sidebar("21-03-dvizhenie-vragi.html"),
        nav=PageNav(prev_href="21-02-cikl-korabl.html", prev_label="Игровой цикл и корабль игрока", next_href="21-04-strelba.html", next_label="Стрельба: создаём и двигаем пули"),
    )
    write("21-03-dvizhenie-vragi.html", out)


def build_04() -> None:
    body = f"""
    <p>Пули — словарь с <code class="inline">Rect</code> и дробной координатой Y, появляющийся у
    носа корабля при нажатии пробела и улетающий вверх со скоростью в пикселях в секунду:</p>
    {code_block(
        "strelba.py",
        "PULYA_SHIRINA, PULYA_VYSOTA = 6, 18\n"
        "PULYA_SKOROST = 560.0   # px/s\n\n"
        "puli = []\n\n"
        "def vystrelit():\n"
        "    pulya_rect = pygame.Rect(\n"
        "        korabl.centerx - PULYA_SHIRINA // 2,\n"
        "        korabl.top,\n"
        "        PULYA_SHIRINA,\n"
        "        PULYA_VYSOTA,\n"
        "    )\n"
        "    puli.append({{\"rect\": pulya_rect, \"y\": float(pulya_rect.y)}})\n\n"
        "# в обработке событий:\n"
        "if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:\n"
        "    vystrelit()\n\n"
        "# в обновлении кадра:\n"
        "for pulya in puli:\n"
        "    pulya[\"y\"] -= PULYA_SKOROST * dt\n"
        "    pulya[\"rect\"].y = round(pulya[\"y\"])\n"
        "puli = [p for p in puli if p[\"rect\"].bottom > 0]   # убираем улетевшие за экран\n",
    )}
    {image_figure(f"{IMG}/09-first-bullet.png", "Реальное окно: маленькая жёлтая пуля вылетает из носа синего корабля вверх", "Реальное окно — пуля появляется точно у носа корабля и летит вверх.", width=220)}
    {callout(
        "tip",
        "Список через генератор списков — чистка «мусора»",
        "<code class=\"inline\">[p for p in puli if p[\"rect\"].bottom &gt; 0]</code> (генератор "
        "списков из главы 11) оставляет только те пули, что ещё видны на экране — без этой строки "
        "список пуль рос бы бесконечно, замедляя игру всё сильнее.",
    )}
    {callout(
        "info",
        "KEYDOWN — одно событие на одно нажатие",
        "Событие <code class=\"inline\">pygame.KEYDOWN</code> возникает один раз в момент "
        "физического нажатия клавиши. Автоматический повтор клавиш в Pygame по умолчанию "
        "выключен (включить его можно только явно, через "
        "<code class=\"inline\">pygame.key.set_repeat(...)</code>, а мы этого не делаем) — значит, "
        "удержание пробела не порождает новый <code class=\"inline\">KEYDOWN</code> на каждом "
        "кадре. Здесь это даёт ровно один выстрел за одно нажатие: удобно для одиночной "
        "стрельбы, но не подходит для удержания огня — этим займётся раздел 21.13.",
    )}

    {local_required_card(
        "21-04",
        "Практика: стрельба и движение пуль",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/21-04/index.html",
    )}
    """
    out = render_page(
        page_title="Стрельба: создаём и двигаем пули",
        description="Создаём пули по нажатию пробела, двигаем их со скоростью в пикселях в секунду и убираем пули, улетевшие за пределы экрана.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Стрельба: создаём и двигаем пули", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Стрельба: создаём и двигаем пули",
        lede="Пробел создаёт пулю у носа корабля — она улетает вверх, пока не покинет экран.",
        body_html=body,
        sidebar_groups=sidebar("21-04-strelba.html"),
        nav=PageNav(prev_href="21-03-dvizhenie-vragi.html", prev_label="Движение корабля и появление врагов", next_href="21-05-tablo-scheta.html", next_label="Счёт и информация на экране"),
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
    {image_figure(f"{IMG}/15-score-after-hit.png", "Реальное окно: верхняя полоса интерфейса со счётом 100 слева и числом жизней справа на тёмном фоне", "Финальная версия выделяет счёт и жизни в отдельную HUD-полосу поверху (раздел 21.12) — то же табло, просто отделённое от игрового поля.", width=320)}

    {practice_revisit_card(
        "21-03",
        "Практика: включает вывод счёта",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/21-03/index.html",
    )}
    """
    out = render_page(
        page_title="Счёт и информация на экране",
        description="Отрисовка текста счёта через pygame.font: render() и blit().",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Счёт и информация на экране", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Счёт и информация на экране",
        lede="Текст в Pygame рисуется в два шага: сначала render(), потом blit() на экран.",
        body_html=body,
        sidebar_groups=sidebar("21-05-tablo-scheta.html"),
        nav=PageNav(prev_href="21-04-strelba.html", prev_label="Стрельба: создаём и двигаем пули", next_href="21-06-unichtozhenie.html", next_label="Попадания и столкновения"),
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
        "списки уцелевших пуль и врагов, как показано выше. Финальная версия (раздел 21.9) решает "
        "эту же задачу без ручных списков — через <code class=\"inline\">pygame.sprite.Group</code> "
        "и <code class=\"inline\">groupcollide()</code>.",
    )}
    {image_figure(f"{IMG}/12-bullet-enemy-hit.png", "Реальное окно: оранжевая вспышка взрыва в точке, где пуля попала во врага, счёт увеличился до 100", "Реальное окно — момент попадания: враг уничтожен, счёт увеличился ровно один раз.", width=220)}

    <h2 id="korabl-unichtozhen">Когда враг уничтожает корабль</h2>
    <p>Если враг долетел до низа экрана или столкнулся с кораблём — игра заканчивается:</p>
    {code_block(
        "unichtozhenie_korablya.py",
        "for vrag in vragi:\n"
        "    if vrag.bottom >= VYSOTA or vrag.colliderect(korabl):\n"
        "        igra_okonchena = True\n"
        "        break\n",
    )}
    {callout(
        "warning",
        "Мгновенный конец игры — тоже временное решение",
        "Здесь одно столкновение сразу заканчивает игру. Финальная версия (раздел 21.16) "
        "заменяет это на систему жизней с временной неуязвимостью после удара — так три врага, "
        "столкнувшихся с кораблём в один момент, не отнимают сразу три жизни.",
    )}

    {local_required_card(
        "21-06",
        "Практика: столкновения пуль, врагов и корабля",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/21-06/index.html",
    )}
    """
    out = render_page(
        page_title="Попадания и столкновения",
        description="Проверка столкновений pulya.colliderect(vrag) и условия окончания игры.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Попадания и столкновения", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Попадания и столкновения",
        lede="colliderect() проверяет столкновения — попадание уничтожает врага, а враг может "
        "уничтожить корабль.",
        body_html=body,
        sidebar_groups=sidebar("21-06-unichtozhenie.html"),
        nav=PageNav(prev_href="21-05-tablo-scheta.html", prev_label="Счёт и информация на экране", next_href="21-07-game-over.html", next_label="Завершение игры и экран «Игра окончена»"),
    )
    write("21-06-unichtozhenie.html", out)


def build_07() -> None:
    body = f"""
    <h2>Рисуем кадр заново</h2>
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

    <h2>Экран «Игра окончена»</h2>
    <p>Когда <code class="inline">igra_okonchena</code> становится истинной, вместо обычной
    игровой логики выводится финальный экран:</p>
    {code_block(
        "game_over.py",
        "if igra_okonchena:\n"
        '    nadpis = shrift_bolshoj.render("ИГРА ОКОНЧЕНА", True, (255, 255, 255))\n'
        "    rect = nadpis.get_rect(center=(SHIRINA // 2, VYSOTA // 2))\n"
        "    screen.blit(nadpis, rect)\n",
    )}
    {image_figure(f"{IMG}/23-game-over.png", "Реальное окно: полупрозрачная тёмная накладка на весь экран, крупная надпись ИГРА ОКОНЧЕНА, счёт и подсказка Enter — заново", "Финальная версия добавляет к экрану Game Over счёт, рекорд сессии и явную подсказку, как начать заново (раздел 21.19).", width=220)}
    {callout(
        "tip",
        "get_rect(center=...) — удобное центрирование текста",
        "Вместо ручного вычисления координат текста по его ширине и высоте, "
        "<code class=\"inline\">get_rect(center=(x, y))</code> сам находит нужный левый "
        "верхний угол так, чтобы текст оказался центрирован ровно в точке "
        "<code class=\"inline\">(x, y)</code>.",
    )}
    {callout(
        "warning",
        "Из этого экрана нет выхода без перезапуска Python",
        "У переменной <code class=\"inline\">igra_okonchena</code> нет обратного пути — единственный "
        "способ сыграть ещё раз — запустить программу заново. Раздел 21.18 заменит одну булеву "
        "переменную на явный <code class=\"inline\">enum.Enum</code> с четырьмя состояниями "
        "(MENU/PLAYING/PAUSED/GAME_OVER) и понятными переходами между ними, включая переход "
        "обратно в игру.",
    )}

    {practice_revisit_card(
        "21-06",
        "Практика: включает финальный экран",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/21-06/index.html",
    )}
    """
    out = render_page(
        page_title="Завершение игры и экран «Игра окончена»",
        description="Полная перерисовка кадра каждый цикл и финальный экран «Игра окончена».",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Завершение игры и экран «Игра окончена»", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Завершение игры и экран «Игра окончена»",
        lede="Каждый кадр рисуется заново целиком — а при окончании игры на экране появляется "
        "финальная надпись.",
        body_html=body,
        sidebar_groups=sidebar("21-07-game-over.html"),
        nav=PageNav(prev_href="21-06-unichtozhenie.html", prev_label="Попадания и столкновения", next_href="21-08-polnyj-kod-itogi.html", next_label="Первая рабочая версия игры"),
    )
    write("21-07-game-over.html", out)


def build_08() -> None:
    body = f"""
    <p>Собрав разделы 21.1–21.7 вместе, получаем первую рабочую версию игры, в которую уже можно
    играть — именно на ней заканчивается глава в бумажной книге. Движение корабля, врагов и пуль
    в ней уже не зависит от частоты кадров: скорости заданы в пикселях в секунду, а появление
    врагов — таймером в секундах, как и в разделах 21.2–21.4. Дальше, с раздела 21.9, книга
    продолжает в цифровой версии: тот же проект вырастает в архитектуру на классах, обзаводится
    собственной графикой и звуком, системой жизней, ростом сложности и полноценными состояниями
    игры.</p>
    {callout(
        "info",
        "Цифровое продолжение проекта — ниже в оглавлении главы",
        "Разделы 21.9–21.26 в боковом меню — это не отдельная тема, а следующий этап разработки "
        "той же самой игры: та же механика, но код становится чище, точнее и надёжнее на каждом "
        "шаге.",
    )}

    {exercise(2, "Жизни вместо мгновенного конца", "Добавьте переменную zhizni = 3 — при столкновении корабля с врагом отнимайте одну жизнь и убирайте врага, вместо немедленного окончания игры. (Раздел 21.16 показывает готовое решение с временной неуязвимостью.)")}
    {exercise(3, "Уровни сложности", "Постепенно уменьшайте интервал появления врагов по мере роста счёта — враги должны появляться всё чаще. (Раздел 21.17 показывает, как сделать это без резких скачков.)")}

    {local_required_card(
        "21-08",
        "Практика: первая рабочая версия",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/21-08/index.html",
    )}
    """
    out = render_page(
        page_title="Первая рабочая версия игры",
        description="Итог исторической части главы 21 — первая рабочая, FPS-независимая версия космического шутера, и переход к цифровому продолжению проекта.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Первая рабочая версия игры", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Первая рабочая версия игры",
        lede="Разделы 21.1–21.7 вместе дают рабочую игру, в которую уже можно играть — а глава продолжается дальше.",
        body_html=body,
        sidebar_groups=sidebar("21-08-polnyj-kod-itogi.html"),
        nav=PageNav(prev_href="21-07-game-over.html", prev_label="Завершение игры и экран «Игра окончена»", next_href="21-09-arhitektura-proekta.html", next_label="Разделяем игру на классы"),
    )
    write("21-08-polnyj-kod-itogi.html", out)


# ---------------------------------------------------------------------------
# 21.9–21.26 — цифровое продолжение: архитектура, точность, надёжность
# ---------------------------------------------------------------------------

def build_09() -> None:
    body = f"""
    <p>Исторический код разделов 21.1–21.7 хранит корабль, врагов и пули как отдельные переменные
    и списки <code class="inline">Rect</code>, а всю логику — прямо в теле игрового цикла. Это
    работает для маленькой игры, но плохо растёт: чем больше правил, тем труднее понять, какой
    код за что отвечает. Финальная версия делит игру на пять классов с чёткими обязанностями.</p>

    {class_diagram(
        "Game",
        ["screen", "clock", "assets", "player", "bullets", "enemies", "explosions", "state", "score", "lives"],
        ["handle_events()", "handle_input(dt)", "update(dt)", "render()", "run()"],
        caption="Game владеет всем состоянием игры и координирует остальные классы — сам он не рисует врага и не двигает пулю напрямую.",
    )}

    {relationship_diagram("Game", "Player", "владеет", style="has-a", caption="Game хранит один экземпляр Player.")}
    {relationship_diagram("Game", "Группы спрайтов", "владеет", style="has-a", caption="Game хранит по одной pygame.sprite.Group для Bullet, Enemy и Explosion.")}

    <p><code class="inline">Bullet</code>, <code class="inline">Enemy</code> и
    <code class="inline">Explosion</code> — наследники <code class="inline">pygame.sprite.Sprite</code>
    (раздел 20.19 уже показал, зачем спрайты нужны: у объекта появляются <code class="inline">.image</code>
    и <code class="inline">.rect</code>, которые понимают готовые функции столкновений и группы).
    Хранить их в <code class="inline">pygame.sprite.Group</code>, а не в обычном списке, удобно по
    той же причине, что и в разделе 21.6: группа сама умеет удалять объект (<code class="inline">.kill()</code>)
    без риска «сломать» цикл перебора, а <code class="inline">pygame.sprite.groupcollide()</code>
    (раздел 21.15) проверяет столкновения между целыми группами одним вызовом.</p>

    {code_block(
        "fragment_game_init.py",
        "class Game:\n"
        "    def __init__(self, *, rng=None, debug=False):\n"
        "        pygame.init()\n"
        "        self.screen = pygame.display.set_mode((SHIRINA, VYSOTA))\n"
        "        self.clock = pygame.time.Clock()\n"
        "        self.assets = AssetStore(IMAGE_DIR, AUDIO_DIR)\n"
        "        self.rng = rng if rng is not None else random.Random()\n\n"
        "        self.state = GameStatus.MENU\n"
        "        self.bullets = pygame.sprite.Group()\n"
        "        self.enemies = pygame.sprite.Group()\n"
        "        self.explosions = pygame.sprite.Group()\n"
        "        self.player = self._make_player()\n"
        "        self.score = 0\n"
        "        self.lives = STARTING_LIVES\n",
    )}
    {callout(
        "info",
        "Это набросок, а не полный файл",
        "Полный, готовый к запуску класс <code class=\"inline\">Game</code> — в файле "
        "<code class=\"inline\">projects/pygame/space-shooter/space_shooter.py</code>, который "
        "подробно разбирает раздел 21.25.",
    )}
    {callout(
        "warning",
        "Эта архитектура — не универсальный закон",
        "Разделение на Game/Player/Bullet/Enemy/Explosion — удобное решение именно для проекта "
        "такого размера, а не единственно правильный способ строить любую игру. Раздел 20.8 уже "
        "объяснял: у разных инструментов и проектов архитектура может сильно отличаться.",
    )}

    {local_required_card(
        "21-09",
        "Практика: набросок класса Game",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/21-09/index.html",
    )}
    """
    out = render_page(
        page_title="Разделяем игру на классы",
        description="Как финальная версия космического шутера делится на классы Game, Player, Bullet, Enemy и Explosion, и почему.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Разделяем игру на классы", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Разделяем игру на классы",
        lede="Пять классов с чёткими обязанностями — вместо одних глобальных переменных и списков.",
        body_html=body,
        sidebar_groups=sidebar("21-09-arhitektura-proekta.html"),
        nav=PageNav(prev_href="21-08-polnyj-kod-itogi.html", prev_label="Первая рабочая версия игры", next_href="21-10-assety-i-zvuk.html", next_label="Ресурсы игры: графика и звук"),
    )
    write("21-09-arhitektura-proekta.html", out)


def build_10() -> None:
    body = f"""
    <p>До сих пор корабль, враги и пули рисовались простыми прямоугольниками и кругами —
    удобно для первых шагов (раздел 20.3). Финальная версия использует собственные спрайты,
    нарисованные специально для этого проекта, вместо геометрических заглушек.</p>

    <h2>Спрайты проекта</h2>
    {image_figure(f"{IMG}/19-two-enemy-types.png", "Реальное окно: маленький оранжевый враг-разведчик слева и более крупный розово-красный враг-истребитель справа, синий корабль игрока снизу", "Три собственных спрайта одновременно: разведчик (scout), истребитель (fighter) и корабль игрока — разные силуэты и цвета, чтобы враги считывались с одного взгляда.", width=320)}
    <p>Все изображения сохранены как файлы <code class="inline">.png</code> с прозрачным фоном.
    При загрузке они попадают в Surface, которая поддерживает альфа-канал (флаг
    <code class="inline">pygame.SRCALPHA</code> при создании такой Surface, раздел 20.17, —
    это свойство самой Surface в pygame, а не PNG-файла), поэтому прозрачные пиксели остаются
    прозрачными и на экране. Спрайты нарисованы напрямую через
    <code class="inline">pygame.draw</code> в отдельном скрипте
    <code class="inline">scripts/generate_chapter_21_assets.py</code>, а не скачаны откуда-то —
    простые геометрические фигуры, без единого существующего коммерческого спрайта.</p>

    {comparison_table(
        ["Файл", "Роль", "Особенность"],
        [
            ["player_ship.png", "Корабль игрока", "Стреловидный силуэт, светлая кабина, свечение двигателя"],
            ["enemy_scout.png", "Быстрый, дешёвый враг", "Маленький, оранжево-красный треугольник"],
            ["enemy_fighter.png", "Медленный, дорогой враг", "Крупнее, пурпурно-красный, с боковыми модулями"],
            ["bullet.png", "Снаряд игрока", "Маленькая яркая жёлтая капсула"],
            ["explosion_sheet.png", "Анимация взрыва", "6 кадров в ряд — раздел 21.20 режет их через subsurface()"],
        ],
    )}

    <h2>AssetStore — загрузка один раз</h2>
    <p>Раздел 20.24 уже предупреждал: загрузка файла внутри игрового цикла — частая причина
    просадок кадров. Здесь всё загружается один раз в момент создания игры, в отдельном классе:</p>
    {code_block(
        "fragment_asset_store.py",
        "class AssetStore:\n"
        "    def __init__(self, image_dir, audio_dir):\n"
        "        self.images = {{}}\n"
        "        for key in (\"player_ship\", \"enemy_scout\", \"enemy_fighter\", \"bullet\"):\n"
        "            self.images[key] = pygame.image.load(image_dir / f\"{{key}}.png\").convert_alpha()\n\n"
        "        self.sounds = {{}}\n"
        "        for key in (\"laser\", \"explosion\", \"player_hit\"):\n"
        "            path = audio_dir / f\"{{key}}.wav\"\n"
        "            try:\n"
        "                self.sounds[key] = pygame.mixer.Sound(str(path))\n"
        "            except (pygame.error, FileNotFoundError):\n"
        "                self.sounds[key] = None\n",
    )}
    {callout(
        "info",
        "convert_alpha() — тот же смысл, что и в главе 20",
        "<code class=\"inline\">pygame.image.load(...)</code> уже сохраняет прозрачность "
        "загруженного PNG сама по себе — <code class=\"inline\">.convert_alpha()</code> не "
        "«создаёт» прозрачность, а лишь готовит копию в формате пикселей экрана для быстрой "
        "повторной отрисовки (раздел 20.19). Здесь она вызывается сразу после загрузки, пока "
        "изображений мало и это не нужно откладывать.",
    )}
    {callout(
        "tip",
        "Звук — необязательное условие для запуска игры",
        "Если в системе нет звукового устройства (например, при автоматическом тестировании), "
        "<code class=\"inline\">pygame.mixer.Sound(...)</code> может завершиться ошибкой — тогда "
        "<code class=\"inline\">self.sounds[key]</code> остаётся <code class=\"inline\">None</code>, "
        "а игра всё равно запускается и работает, просто без звука. Раздел 21.21 показывает, как "
        "проигрывание учитывает это на каждом вызове.",
    )}
    """
    out = render_page(
        page_title="Ресурсы игры: графика и звук",
        description="Собственные спрайты и звуки финальной версии игры и класс AssetStore, который загружает их один раз.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Ресурсы игры: графика и звук", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Ресурсы игры: графика и звук",
        lede="Настоящие спрайты вместо прямоугольников — и класс, который загружает их ровно один раз.",
        body_html=body,
        sidebar_groups=sidebar("21-10-assety-i-zvuk.html"),
        nav=PageNav(prev_href="21-09-arhitektura-proekta.html", prev_label="Разделяем игру на классы", next_href="21-11-vector2-tochnoe-dvizhenie.html", next_label="Точное движение с Vector2"),
    )
    write("21-10-assety-i-zvuk.html", out)


def build_11() -> None:
    body = f"""
    <p><code class="inline">pygame.Rect</code> удобен для столкновений и отрисовки, но хранит
    только целые числа. Если на каждом кадре прибавлять к его координате маленькое дробное
    значение, оно молча теряется при округлении — движение на очень низкой скорости может вообще
    не сдвинуться с места, хотя код выглядит правильно.</p>

    {pipeline_diagram([
        {"kind": "plain", "title": "Vector2 (float)", "rows": ["position += velocity * dt", "не теряет дробную часть"]},
        {"kind": "plain", "title": "round()", "rows": ["округление только в момент отрисовки"]},
        {"kind": "plain", "title": "Rect (int)", "rows": ["используется для столкновений и blit()"]},
    ], caption="Позиция всегда живёт как Vector2 с плавающей точкой; Rect каждый кадр пересобирается ИЗ неё, а не обновляется напрямую.")}

    {code_block(
        "fragment_player_move.py",
        "class Player(pygame.sprite.Sprite):\n"
        "    def __init__(self, image, center):\n"
        "        super().__init__()\n"
        "        self.image = image\n"
        "        self.rect = self.image.get_rect()\n"
        "        self.position = pygame.Vector2(center)\n"
        "        self.rect.center = (round(self.position.x), round(self.position.y))\n\n"
        "    def move(self, direction, dt, playfield):\n"
        "        if direction.length_squared() > 0:\n"
        "            direction = direction.normalize()\n"
        "        self.position += direction * self.speed * dt\n"
        "        self.rect.center = (round(self.position.x), round(self.position.y))\n",
    )}
    {callout(
        "warning",
        "direction.normalize() — то же диагональное правило, что и в разделе 20.16",
        "Вектор направления <code class=\"inline\">(1, 1)</code> (вправо-вниз одновременно) без "
        "нормализации по длине больше единицы — √2 ≈ 1.41. Если не привести его к единичной "
        "длине, корабль по диагонали двигался бы на 41% быстрее, чем строго по одной оси.",
    )}
    {callout(
        "info",
        "direction.length_squared() > 0, а не > 0 сразу для длины",
        "У этих двух строк разные задачи. Проверка <code class=\"inline\">> 0</code> — то, что "
        "не даёт вызвать <code class=\"inline\">normalize()</code> у нулевого вектора (когда игрок "
        "вообще не нажимает клавиши движения): нормализация делит вектор на его длину, а длина "
        "нулевого вектора равна нулю. А <code class=\"inline\">length_squared()</code> (квадрат "
        "длины) вместо <code class=\"inline\">length()</code> нужен только затем, чтобы не "
        "извлекать лишний квадратный корень, когда достаточно знать, ненулевой ли вектор — "
        "обычная микрооптимизация в реальном коде на Vector2.",
    )}

    <h2>Игровое поле не отпускает корабль</h2>
    <p>Каждое движение сразу ограничивается границами игрового поля (раздел 21.12) — так же, как
    <code class="inline">max(0, min(...))</code> в разделе 21.3, но теперь применяется и по X, и
    по Y, потому что корабль двигается во всех четырёх направлениях.</p>

    {local_required_card(
        "21-11",
        "Практика: Vector2, нормализация и clamp",
        "Проверяется прямо в браузере — установка Pygame не требуется",
        "../../practice/21-11/index.html",
    )}
    """
    out = render_page(
        page_title="Точное движение с Vector2",
        description="Почему позиция хранится как Vector2 с плавающей точкой, а не как Rect напрямую, и как нормализуется диагональное движение.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Точное движение с Vector2", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Точное движение с Vector2",
        lede="Rect хранит только целые числа — позиция живёт отдельно, как Vector2 с плавающей точкой.",
        body_html=body,
        sidebar_groups=sidebar("21-11-vector2-tochnoe-dvizhenie.html"),
        nav=PageNav(prev_href="21-10-assety-i-zvuk.html", prev_label="Ресурсы игры: графика и звук", next_href="21-12-igrovoe-pole-i-hud.html", next_label="Игровое поле и интерфейс игрока"),
    )
    write("21-11-vector2-tochnoe-dvizhenie.html", out)


def build_12() -> None:
    body = f"""
    <p>Глава 19 уже показывала, что бывает, если интерфейс перекрывает игровое поле: важный текст
    может оказаться под движущимся объектом. Финальная версия шутера с самого начала разделяет
    экран на две чётко разные области: игровое поле и полосу с показаниями для игрока — счётом,
    жизнями, номером волны. Такую полосу поверх игрового мира в индустрии принято называть HUD
    (Heads-Up Display, «приборная панель» — интерфейс, который не является частью самой игры, а
    просто показывает её текущее состояние).</p>

    {image_figure(f"{IMG}/02-empty-playfield.png", "Реальное окно: верхняя тёмная полоса HUD со счётом и жизнями отделена тонкой линией от основного игрового поля со звёздным фоном и кораблём внизу", "Реальное окно — полоса интерфейса сверху (64 пикселя) отделена тонкой линией от игрового поля; ни один враг или снаряд не может оказаться выше этой границы.", width=320)}

    {code_block(
        "fragment_playfield.py",
        "HUD_HEIGHT = 64\n\n"
        "self.playfield = pygame.Rect(0, HUD_HEIGHT, SHIRINA, VYSOTA - HUD_HEIGHT)\n",
    )}
    <p>Игровое поле — обычный <code class="inline">Rect</code>, а не просто число отступа: у него
    сразу есть <code class="inline">.top</code>, <code class="inline">.bottom</code>,
    <code class="inline">.left</code>, <code class="inline">.right</code> — то же самое, что
    возвращает <code class="inline">korabl.top</code> в разделе 21.2, только теперь описывает не
    один объект, а всю разрешённую область движения.</p>

    {comparison_table(
        ["Что где происходит", "Область"],
        [
            ["Счёт, жизни, волна", "HUD-полоса (0 — HUD_HEIGHT)"],
            ["Корабль, враги, пули, взрывы", "Игровое поле (HUD_HEIGHT — низ экрана)"],
            ["Появление врагов", "Чуть выше верхней границы игрового поля"],
            ["Побег врага (раздел 21.16)", "Пересечение нижней границы игрового поля"],
        ],
    )}
    {callout(
        "warning",
        "Корабль ограничен именно игровым полем, а не всем окном",
        "<code class=\"inline\">Player.move()</code> (раздел 21.11) зажимает позицию в границах "
        "<code class=\"inline\">self.playfield</code>, а не всего окна <code class=\"inline\">"
        "SHIRINA × VYSOTA</code> — иначе корабль мог бы заехать под HUD и спрятать сам себя за "
        "текстом счёта.",
    )}
    """
    out = render_page(
        page_title="Игровое поле и интерфейс игрока",
        description="Почему HUD и игровое поле — разные прямоугольники, и как это защищает интерфейс от перекрытия игровыми объектами.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Игровое поле и интерфейс игрока", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Игровое поле и интерфейс игрока",
        lede="Счёт и жизни живут в своей полосе сверху — игровые объекты в неё физически не заходят.",
        body_html=body,
        sidebar_groups=sidebar("21-12-igrovoe-pole-i-hud.html"),
        nav=PageNav(prev_href="21-11-vector2-tochnoe-dvizhenie.html", prev_label="Точное движение с Vector2", next_href="21-13-skorostrelnost.html", next_label="Скорострельность и интервал между выстрелами"),
    )
    write("21-12-igrovoe-pole-i-hud.html", out)


def build_13() -> None:
    body = f"""
    <p>Раздел 21.4 стрелял по событию <code class="inline">KEYDOWN</code> — оно происходит ровно
    один раз на одно физическое нажатие пробела, поэтому даже долгое удержание клавиши там давало
    только один выстрел. Финальной версии игры нужна стрельба очередями, пока пробел зажат, а для
    этого требуется другой источник данных — <code class="inline">pygame.key.get_pressed()</code>,
    которая на каждом обновлении сообщает, зажата ли клавиша прямо сейчас. Без ограничений это
    означало бы выстрел на каждом обновлении игры, то есть скорострельность, зависящую от FPS: 60
    выстрелов в секунду при 60 FPS и 120 — при 120 FPS. Поэтому стрельба через
    <code class="inline">get_pressed()</code> всегда сопровождается минимальным интервалом между
    выстрелами (cooldown, в профессиональной речи — кулдаун), заданным в секундах.</p>

    {code_block(
        "fragment_fire_cooldown.py",
        "FIRE_INTERVAL = 0.20   # секунд между выстрелами\n\n"
        "self.fire_cooldown = max(0.0, self.fire_cooldown - dt)\n\n"
        "if keys[pygame.K_SPACE] and self.fire_cooldown <= 0.0:\n"
        "    self._spawn_bullet()\n"
        "    self.fire_cooldown = FIRE_INTERVAL\n",
    )}
    {callout(
        "warning",
        "Интервал измеряется в секундах, а не в кадрах",
        "Если бы вместо <code class=\"inline\">fire_cooldown -= dt</code> счётчик уменьшался на "
        "единицу каждый кадр (<code class=\"inline\">kadrov_do_vystrela -= 1</code>), скорострельность "
        "зависела бы от FPS точно так же, как нескорректированное движение из раздела 20.16: на "
        "120 FPS корабль стрелял бы вдвое чаще, чем на 60 FPS, при одном и том же коде.",
    )}

    <h2>Почему здесь не используется while, как в таймере появления врагов</h2>
    <p>Раздел 21.14 покажет финальный таймер появления врагов: он продвигает время через
    <code class="inline">+= interval</code>, сохраняя остаток, а <code class="inline">while</code>
    там нужен на случай, если один обрабатываемый шаг способен охватить сразу несколько интервалов.
    Интервал между выстрелами устроен иначе:</p>
    {comparison_table(
        ["", "Таймер появления врагов", "Интервал между выстрелами игрока"],
        [
            ["Источник события", "Автономная симуляция (сама игра решает, когда)", "Ввод игрока (человек решает, когда)"],
            ["Долгий обрабатываемый шаг", "Если шаг способен охватить несколько интервалов, таймер может обработать несколько событий подряд", "не должен выстрелить сразу несколько пуль одним кадром"],
            ["Приём в коде", "while: продолжать, пока накоплено время", "if: не больше одного выстрела за кадр"],
        ],
    )}
    {callout(
        "tip",
        "В текущей игре второй столбец не наступает",
        "<code class=\"inline\">MAX_DT</code> не позволяет одному обработанному шагу стать длиннее "
        "минимального интервала появления врагов (подробности — в разделе 21.14) — поэтому в этой "
        "конкретной игре ни пауза отладчика, ни зависание ОС не приводят к тому, что игра "
        "«наверстывает» всё накопленное реальное время залпом из нескольких врагов сразу.",
    )}
    {callout(
        "info",
        "Это осознанный выбор, а не недосмотр",
        "После действительно долгого кадра (пауза отладчика, зависание ОС) внезапный залп из "
        "десяти пуль ощущался бы как ошибка, а не как честное поведение — поэтому интервал между "
        "выстрелами игрока нарочно даёт максимум один новый выстрел за одно обновление, даже если "
        "<code class=\"inline\">dt</code> оказался большим.",
    )}

    {local_required_card(
        "21-13",
        "Практика: интервал между выстрелами",
        "Проверяется прямо в браузере — установка Pygame не требуется",
        "../../practice/21-13/index.html",
    )}
    """
    out = render_page(
        page_title="Скорострельность и интервал между выстрелами",
        description="Удерживаемая стрельба с ограничением скорострельности через интервал между выстрелами в секундах, и почему он не использует while, в отличие от таймера появления врагов.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Скорострельность и интервал между выстрелами", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Скорострельность и интервал между выстрелами",
        lede="Удержание пробела стреляет с ограниченной частотой — в секундах, а не в кадрах.",
        body_html=body,
        sidebar_groups=sidebar("21-13-skorostrelnost.html"),
        nav=PageNav(prev_href="21-12-igrovoe-pole-i-hud.html", prev_label="Игровое поле и интерфейс игрока", next_href="21-14-poyavlenie-vragov.html", next_label="Как появляются враги"),
    )
    write("21-13-skorostrelnost.html", out)


def build_14() -> None:
    body = f"""
    <p>В разделе 21.3 мы уже измеряли время до следующего врага в секундах: таймер уменьшался на
    <code class="inline">dt</code> каждый кадр, а при срабатывании прибавлял интервал заново, а не
    присваивал его — так остаток не терялся. Теперь перенесём тот же принцип в финальную
    архитектуру игры и сделаем таймер пригодным для интервала, который меняется вместе со
    сложностью.</p>

    {code_block(
        "fragment_spawn_timer.py",
        "self.spawn_timer -= dt\n"
        "while self.spawn_timer <= 0.0:\n"
        "    self._spawn_enemy()\n"
        "    self.spawn_timer += interval_poyavleniya_vraga(self.score)\n",
    )}
    {callout(
        "info",
        "Два независимых механизма, а не один",
        "<code class=\"inline\">self.spawn_timer += interval_poyavleniya_vraga(self.score)</code> "
        "— то, что нужно на каждом кадре: остаток времени сверх интервала не выбрасывается, а "
        "переносится на следующего врага, точно так же, как в разделе 21.3 и как таймер анимации в "
        "разделе 20.23. Это сохранение остатка работает и с обычным <code class=\"inline\">if</code>"
        " — оно не требует <code class=\"inline\">while</code>. Сам <code class=\"inline\">while"
        "</code> нужен для другого: если бы один обрабатываемый шаг длился дольше сразу нескольких "
        "интервалов появления врагов, он честно создал бы несколько врагов подряд за один вызов, а "
        "<code class=\"inline\">if</code> продвинул бы появление только одного врага и молча "
        "потерял остальное накопленное время.",
    )}
    {callout(
        "tip",
        "В этой конкретной игре второй случай пока не наступает",
        "Финальная версия игры ограничивает <code class=\"inline\">dt</code> значением "
        "<code class=\"inline\">MAX_DT = 0.05</code> секунды перед каждым обновлением (защита от "
        "скачка после паузы отладчика или зависания ОС), а нижняя граница интервала появления "
        "врагов — "
        "<code class=\"inline\">MIN_SPAWN_INTERVAL = 0.35</code> секунды: даже самый долгий "
        "допустимый кадр короче любого возможного интервала между врагами. Значит, тело "
        "<code class=\"inline\">while</code> в этой игре сейчас никогда не выполняется больше "
        "одного раза за кадр — и написанный через <code class=\"inline\">if</code> код вёл бы себя "
        "здесь ровно так же. <code class=\"inline\">while</code> оставлен как более общий и "
        "надёжный приём: он не сломается, если позже поднять MAX_DT или уменьшить интервал "
        "появления врагов сильнее, чем сейчас, а <code class=\"inline\">if</code> в этом случае "
        "пришлось бы менять.",
    )}

    <h2>Где именно появляется враг</h2>
    <p>Координата X должна гарантировать, что враг полностью помещается внутри игрового поля —
    без частичного «обрезания» по краю:</p>
    {code_block(
        "fragment_spawn_x.py",
        "def x_poyavleniya_vraga(rng, shirina_vraga, pole):\n"
        "    levaya, pravaya = pole.left, pole.right - shirina_vraga\n"
        "    if pravaya <= levaya:\n"
        "        return float(levaya)\n"
        "    return rng.uniform(levaya, pravaya)\n",
    )}
    <p>Это отдельная, чистая функция — принимает <code class="inline">rng</code> явным аргументом
    (раздел 21.24 объясняет, зачем), а не обращается к глобальному <code class="inline">random</code>
    напрямую, поэтому её удобно тестировать без запуска всей игры.</p>

    <h2>Два типа врагов</h2>
    {image_figure(f"{IMG}/08-enemy-wave.png", "Реальное окно: несколько врагов разных размеров и цветов спускаются по игровому полю группой", "Реальное окно — волна врагов: маленькие быстрые разведчики и более крупные истребители появляются вперемешку.", width=320)}
    {comparison_table(
        ["", "Scout (разведчик)", "Fighter (истребитель)"],
        [
            ["Скорость", "Выше", "Ниже"],
            ["Размер", "Меньше", "Больше"],
            ["Очки за уничтожение", "100", "200"],
            ["Вероятность появления", "Выше в начале игры", "Растёт вместе со счётом (раздел 21.17)"],
        ],
    )}

    {local_required_card(
        "21-14",
        "Практика: таймер появления врагов",
        "Проверяется прямо в браузере — установка Pygame не требуется",
        "../../practice/21-14/index.html",
    )}
    """
    out = render_page(
        page_title="Как появляются враги",
        description="Таймер появления врагов в секундах с сохранением остатка времени сверх интервала, безопасная координата появления и два типа врагов.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Как появляются враги", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Как появляются враги",
        lede="Таймер появления в секундах — с тем же while-накопителем, что и таймер анимации в главе 20.",
        body_html=body,
        sidebar_groups=sidebar("21-14-poyavlenie-vragov.html"),
        nav=PageNav(prev_href="21-13-skorostrelnost.html", prev_label="Скорострельность и интервал между выстрелами", next_href="21-15-stolknoveniya-i-schet.html", next_label="Попадания во врагов и начисление очков"),
    )
    write("21-14-poyavlenie-vragov.html", out)


def build_15() -> None:
    body = f"""
    <p>Раздел 21.6 проверял столкновения пуль и врагов вручную, вложенными циклами по спискам.
    Группы спрайтов (раздел 21.9) решают эту же задачу одним вызовом:</p>
    {code_block(
        "fragment_bullet_enemy_collisions.py",
        "def resolve_bullet_enemy_collisions(self):\n"
        "    collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)\n"
        "    destroyed = {{vrag for vragi in collisions.values() for vrag in vragi}}\n"
        "    for vrag in destroyed:\n"
        "        self._spawn_explosion(vrag.rect.center)\n"
        "    return ochki_za_unichtozhennyh(destroyed)\n",
    )}
    <p><code class="inline">pygame.sprite.groupcollide(a, b, True, True)</code> сравнивает каждый
    спрайт из <code class="inline">a</code> с каждым спрайтом из <code class="inline">b</code> и
    возвращает словарь: пуля → список врагов, которых она задела. Оба флага
    <code class="inline">True</code> означают «удалить из своей группы при столкновении» — сама
    группа берёт на себя ту же задачу, что вручную решали новые списки в разделе 21.6.</p>

    {image_figure(f"{IMG}/12-bullet-enemy-hit.png", "Реальное окно: вспышка взрыва там, где пуля попала во врага, счёт вверху увеличился", "Реальное окно — момент попадания: и пуля, и враг уже удалены из своих групп, взрыв запущен.", width=220)}

    {callout(
        "warning",
        "Почему подсчёт очков идёт через set, а не через сумму по всем парам",
        "Если сразу несколько пуль задели одного и того же врага в одном обновлении, "
        "<code class=\"inline\">groupcollide()</code> вернёт этого врага в списках для каждой из "
        "них — но физически это один и тот же уничтоженный враг. Собирая всех задетых врагов в "
        "множество (<code class=\"inline\">set</code>) перед подсчётом очков, каждый враг "
        "засчитывается ровно один раз, сколько бы пуль его ни задели одновременно.",
    )}

    {local_required_card(
        "21-15",
        "Практика: столкновения и подсчёт очков",
        "Проверяется прямо в браузере — установка Pygame не требуется",
        "../../practice/21-15/index.html",
    )}
    """
    out = render_page(
        page_title="Попадания во врагов и начисление очков",
        description="pygame.sprite.groupcollide() для столкновений пуль и врагов, и почему подсчёт очков защищён от двойного начисления.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Попадания во врагов и начисление очков", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Попадания во врагов и начисление очков",
        lede="groupcollide() проверяет столкновения целых групп одним вызовом — но очки нужно "
        "начислять аккуратно.",
        body_html=body,
        sidebar_groups=sidebar("21-15-stolknoveniya-i-schet.html"),
        nav=PageNav(prev_href="21-14-poyavlenie-vragov.html", prev_label="Как появляются враги", next_href="21-16-uron-i-neuyazvimost.html", next_label="Жизни, урон и временная неуязвимость"),
    )
    write("21-15-stolknoveniya-i-schet.html", out)


def build_16() -> None:
    body = f"""
    <p>Раздел 21.6 заканчивал игру от одного столкновения корабля с врагом. Финальная версия
    вместо этого считает жизни — но здесь есть менее очевидная ловушка: что, если сразу несколько
    врагов столкнутся с кораблём в один и тот же момент?</p>

    {code_block(
        "fragment_player_damage.py",
        "def resolve_enemy_player_collisions(self):\n"
        "    hit = pygame.sprite.spritecollide(self.player, self.enemies, True)\n"
        "    for vrag in hit:\n"
        "        self._spawn_explosion(vrag.rect.center)\n"
        "    return len(hit) > 0\n\n"
        "# в обновлении кадра:\n"
        "collided = self.resolve_enemy_player_collisions()\n"
        "if collided and not self.player.is_invulnerable:\n"
        "    self.lives -= 1\n"
        "    self.player.take_hit()\n",
    )}
    {callout(
        "warning",
        "Три врага одновременно — минус одна жизнь, а не минус три",
        "<code class=\"inline\">spritecollide()</code> удаляет все столкнувшиеся вражеские "
        "спрайты безусловно — но урон кораблю отдельная проверка списывает не более одной жизни "
        "за одно обновление кадра, независимо от того, сколько врагов задели корабль "
        "одновременно. Без этого разделения три одновременно налетевших врага отняли бы три "
        "жизни за один кадр, что ощущалось бы несправедливо резко.",
    )}

    <h2>Временная неуязвимость</h2>
    <p>После удара включается короткое окно неуязвимости — во время него столкновения продолжают
    убирать врагов, но больше не отнимают жизни:</p>
    {code_block(
        "fragment_invulnerability.py",
        "PLAYER_INVULNERABLE_SECONDS = 1.2\n\n"
        "@property\n"
        "def is_invulnerable(self):\n"
        "    return self.invulnerable_timer > 0.0\n\n"
        "def update_timers(self, dt):\n"
        "    self.invulnerable_timer = max(0.0, self.invulnerable_timer - dt)\n\n"
        "def take_hit(self):\n"
        "    self.invulnerable_timer = PLAYER_INVULNERABLE_SECONDS\n",
    )}
    {image_figure(f"{IMG}/17-invulnerability.png", "Реальное окно: тонкое голубое кольцо вокруг корабля игрока — визуальный индикатор временной неуязвимости", "Реальное окно — ровное кольцо вокруг корабля, а не мигание: спокойный, не раздражающий индикатор неуязвимости.", width=220)}
    {callout(
        "tip",
        "Ровное кольцо вместо мигания",
        "Мигающий спрайт — распространённый приём, но при быстром морганье он утомляет глаза. "
        "Здесь вместо этого — постоянное кольцо вокруг корабля, которое просто исчезает, когда "
        "<code class=\"inline\">invulnerable_timer</code> достигает нуля.",
    )}

    {local_required_card(
        "21-16",
        "Практика: урон и неуязвимость",
        "Проверяется прямо в браузере — установка Pygame не требуется",
        "../../practice/21-16/index.html",
    )}
    """
    out = render_page(
        page_title="Жизни, урон и временная неуязвимость",
        description="Система жизней вместо мгновенного конца игры, защита от потери нескольких жизней за одно столкновение и временная неуязвимость.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Жизни, урон и временная неуязвимость", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Жизни, урон и временная неуязвимость",
        lede="Несколько врагов, столкнувшихся одновременно, отнимают одну жизнь — а не одну за каждого.",
        body_html=body,
        sidebar_groups=sidebar("21-16-uron-i-neuyazvimost.html"),
        nav=PageNav(prev_href="21-15-stolknoveniya-i-schet.html", prev_label="Попадания во врагов и начисление очков", next_href="21-17-slozhnost-i-volny.html", next_label="Как растёт сложность игры"),
    )
    write("21-16-uron-i-neuyazvimost.html", out)


def build_17() -> None:
    body = f"""
    <p>Постоянная сложность быстро становится или слишком лёгкой, или слишком тяжёлой. Финальная
    версия растит сложность плавно, через три независимые чистые функции от текущего счёта.</p>

    {code_block(
        "fragment_difficulty.py",
        "def interval_poyavleniya_vraga(score):\n"
        "    return max(MIN_SPAWN_INTERVAL, BASE_SPAWN_INTERVAL - score * SPAWN_INTERVAL_SCORE_FACTOR)\n\n"
        "def mnozhitel_skorosti_vraga(score):\n"
        "    return 1.0 + min(MAX_ENEMY_SPEED_BONUS, score * ENEMY_SPEED_SCORE_FACTOR)\n\n"
        "def veroyatnost_istrebitelya(score):\n"
        "    return min(MAX_FIGHTER_PROBABILITY, score * FIGHTER_PROBABILITY_SCORE_FACTOR)\n",
    )}
    {comparison_table(
        ["Функция", "Растёт со счётом", "Ограничена сверху/снизу"],
        [
            ["interval_poyavleniya_vraga", "Уменьшается — враги появляются чаще", "Не ниже MIN_SPAWN_INTERVAL"],
            ["mnozhitel_skorosti_vraga", "Увеличивается — враги быстрее", "Не выше 1.0 + MAX_ENEMY_SPEED_BONUS"],
            ["veroyatnost_istrebitelya", "Увеличивается — больше истребителей", "Не выше MAX_FIGHTER_PROBABILITY"],
        ],
    )}
    {callout(
        "info",
        "Нижняя и верхняя границы — не случайность",
        "Без <code class=\"inline\">max()</code>/<code class=\"inline\">min()</code> интервал "
        "появления врагов на очень высоком счёте мог бы уйти в ноль или отрицательное число. Тогда "
        "<code class=\"inline\">while self.spawn_timer &lt;= 0.0:</code> в разделе 21.14 никогда "
        "не завершился бы: прибавление неположительного интервала не может поднять таймер выше "
        "нуля, и цикл создавал бы врагов бесконечно на одном и том же кадре. Ограничения защищают "
        "формулы от собственного роста.",
    )}

    {image_figure(f"{IMG}/difficulty-strip.png", "Два реальных окна рядом: слева редкие маленькие враги на низком счёте, справа — заметно больше врагов, включая крупные истребители, на высоком счёте", "Реальное сравнение — та же самая формула сложности, применённая к низкому и высокому счёту.", width=680)}

    <h2>Номер волны — только для интерфейса</h2>
    {code_block("fragment_wave.py", "WAVE_SCORE_STEP = 500\n\ndef nomer_volny(score):\n    return 1 + score // WAVE_SCORE_STEP\n")}
    <p>Волна — не отдельная система с собственными правилами, а просто удобный способ показать
    игроку прогресс: раз в 500 очков номер волны на HUD увеличивается, хотя сама сложность растёт
    непрерывно, без резких скачков в этот момент.</p>

    {local_required_card(
        "21-17",
        "Практика: формулы сложности",
        "Проверяется прямо в браузере — установка Pygame не требуется",
        "../../practice/21-17/index.html",
    )}
    """
    out = render_page(
        page_title="Как растёт сложность игры",
        description="Плавный рост сложности через ограниченные сверху и снизу чистые функции от счёта, и номер волны как индикатор прогресса.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Как растёт сложность игры", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Как растёт сложность игры",
        lede="Три независимые формулы от счёта — с ограничением сверху и снизу, без резких скачков.",
        body_html=body,
        sidebar_groups=sidebar("21-17-slozhnost-i-volny.html"),
        nav=PageNav(prev_href="21-16-uron-i-neuyazvimost.html", prev_label="Жизни, урон и временная неуязвимость", next_href="21-18-sostoyaniya-igry.html", next_label="Меню, игра, пауза и завершение"),
    )
    write("21-17-slozhnost-i-volny.html", out)


def build_18() -> None:
    body = f"""
    <p>Раздел 21.7 хранил конец игры в одной переменной <code class="inline">igra_okonchena</code>
    без пути назад. Финальная версия использует явное перечисление — тот же приём, что и
    <code class="inline">SostoyanieIgry</code> в разделе 20.25:</p>
    {code_block(
        "fragment_game_status.py",
        "class GameStatus(Enum):\n"
        "    MENU = auto()\n"
        "    PLAYING = auto()\n"
        "    PAUSED = auto()\n"
        "    GAME_OVER = auto()\n",
    )}

    {comparison_table(
        ["Из состояния", "В состояние", "Когда"],
        [
            ["MENU", "PLAYING", "нажали Enter"],
            ["PLAYING", "PAUSED", "нажали P"],
            ["PAUSED", "PLAYING", "нажали P ещё раз"],
            ["PLAYING", "GAME_OVER", "жизни закончились"],
            ["GAME_OVER", "PLAYING", "нажали Enter (перезапуск)"],
        ],
    )}
    <p>Выход (<code class="inline">Esc</code> или закрытие окна) работает из любого состояния —
    поэтому в таблице выше он не привязан к конкретной строке: это не переход между игровыми
    состояниями, а завершение самой программы.</p>

    {image_figure(f"{IMG}/game-states-strip.png", "Три реальных окна рядом: пустое игровое поле, экран паузы с полупрозрачной накладкой, экран Игра окончена со счётом", "Реальные кадры трёх разных состояний одной и той же игры.", width=680)}

    {callout(
        "warning",
        "Управление кораблём должно знать о состоянии",
        "Если проверку состояния забыть в <code class=\"inline\">handle_input()</code>, корабль "
        "продолжит двигаться и стрелять даже на экране паузы или Game Over — тот же класс "
        "ошибки, что раздел 21.7 уже почти совершил с "
        "<code class=\"inline\">igra_okonchena</code>.",
    )}
    """
    out = render_page(
        page_title="Меню, игра, пауза и завершение",
        description="Явный GameStatus вместо одной булевой переменной, и таблица разрешённых переходов между состояниями игры.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Меню, игра, пауза и завершение", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Меню, игра, пауза и завершение",
        lede="Явное перечисление GameStatus и таблица разрешённых переходов вместо одной булевой переменной.",
        body_html=body,
        sidebar_groups=sidebar("21-18-sostoyaniya-igry.html"),
        nav=PageNav(prev_href="21-17-slozhnost-i-volny.html", prev_label="Как растёт сложность игры", next_href="21-19-perezapusk.html", next_label="Перезапуск игры без перезапуска программы"),
    )
    write("21-18-sostoyaniya-igry.html", out)


def build_19() -> None:
    body = f"""
    <p>У раздела 21.7 не было пути назад из Game Over. Финальная версия перезапускается прямо в
    процессе — но перезапуск обязан сбросить каждый кусочек переходного состояния, не только счёт.</p>

    {code_block(
        "fragment_start_new_game.py",
        "def start_new_game(self):\n"
        "    self.bullets.empty()\n"
        "    self.enemies.empty()\n"
        "    self.explosions.empty()\n"
        "    self.player = self._make_player()\n"
        "    self.score = 0\n"
        "    self.lives = STARTING_LIVES\n"
        "    self.spawn_timer = interval_poyavleniya_vraga(0)\n"
        "    self._reset_stars()\n"
        "    self.state = GameStatus.PLAYING\n",
    )}
    {comparison_table(
        ["Сбрасывается", "Сохраняется"],
        [
            ["Позиция корабля", "Рекорд сессии (high_score)"],
            ["Все пули, враги, взрывы", ""],
            ["Счёт и жизни", ""],
            ["Таймер появления врагов и интервал между выстрелами", ""],
            ["Таймер неуязвимости", ""],
        ],
    )}
    {callout(
        "warning",
        "Забытая пуля из прошлой игры — реальная ошибка, не гипотетическая",
        "Если <code class=\"inline\">self.bullets.empty()</code> пропустить, старые пули из "
        "предыдущей попытки останутся висеть на экране новой игры — визуально безобидно, но "
        "явно неправильно, и легко упустить при ручном тестировании, если специально не "
        "проверить перезапуск с непустыми группами.",
    )}
    {image_figure(f"{IMG}/24-restarted-game.png", "Реальное окно: чистое игровое поле сразу после перезапуска, счёт 0, три жизни", "Реальное окно сразу после перезапуска — счёт, жизни, таймеры и все группы спрайтов возвращены к начальному состоянию.", width=220)}
    """
    out = render_page(
        page_title="Перезапуск игры без перезапуска программы",
        description="Полный сброс переходного состояния при перезапуске: позиция корабля, все группы спрайтов, счёт, жизни и таймеры.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Перезапуск игры без перезапуска программы", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Перезапуск игры без перезапуска программы",
        lede="Перезапуск обязан сбросить каждый кусочек переходного состояния — не только счёт.",
        body_html=body,
        sidebar_groups=sidebar("21-19-perezapusk.html"),
        nav=PageNav(prev_href="21-18-sostoyaniya-igry.html", prev_label="Меню, игра, пауза и завершение", next_href="21-20-animatsiya-vzryva.html", next_label="Анимация взрыва"),
    )
    write("21-19-perezapusk.html", out)


def build_20() -> None:
    body = f"""
    <p>Взрыв — такой же спрайт, как пуля или враг, но вместо движения у него собственная анимация
    из нескольких кадров. Раздел 20.23 уже показывал правильный приём для таймера анимации — здесь
    он применяется во второй раз, теперь для взрыва:</p>
    {code_block(
        "fragment_explosion.py",
        "class Explosion(pygame.sprite.Sprite):\n"
        "    def __init__(self, frames, center):\n"
        "        super().__init__()\n"
        "        self.frames = frames\n"
        "        self.frame_index = 0\n"
        "        self.animation_time = 0.0\n"
        "        self.image = self.frames[0]\n"
        "        self.rect = self.image.get_rect(center=center)\n\n"
        "    def update(self, dt):\n"
        "        self.animation_time += dt\n"
        "        while self.animation_time >= EXPLOSION_FRAME_INTERVAL:\n"
        "            self.animation_time -= EXPLOSION_FRAME_INTERVAL\n"
        "            self.frame_index += 1\n"
        "            if self.frame_index >= len(self.frames):\n"
        "                self.kill()\n"
        "                return\n"
        "            self.image = self.frames[self.frame_index]\n",
    )}
    {image_figure(f"{IMG}/fire-sequence-strip.png", "Три реальных окна рядом: пуля летит вверх, враг перед попаданием, оранжевая вспышка взрыва после попадания", "Реальная последовательность: выстрел, сближение с врагом, взрыв в момент попадания.", width=680)}
    {callout(
        "info",
        "kill() сразу после последнего кадра",
        "Как только <code class=\"inline\">frame_index</code> выходит за пределы списка кадров, "
        "спрайт удаляет себя из всех групп (<code class=\"inline\">.kill()</code>) — без этого "
        "завершённые взрывы копились бы в <code class=\"inline\">self.explosions</code> "
        "бесконечно, занимая память и время отрисовки без всякой пользы.",
    )}

    {local_required_card(
        "21-20",
        "Практика: таймер анимации взрыва",
        "Проверяется прямо в браузере — установка Pygame не требуется",
        "../../practice/21-20/index.html",
    )}
    """
    out = render_page(
        page_title="Анимация взрыва",
        description="Explosion как спрайт с собственной while-анимацией, сохраняющей остаток времени сверх интервала, и самоудалением после последнего кадра.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Анимация взрыва", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Анимация взрыва",
        lede="Тот же while-накопитель времени, что и в главе 20 — теперь для взрыва, а не для ходьбы.",
        body_html=body,
        sidebar_groups=sidebar("21-20-animatsiya-vzryva.html"),
        nav=PageNav(prev_href="21-19-perezapusk.html", prev_label="Перезапуск игры без перезапуска программы", next_href="21-21-zvukovye-effekty.html", next_label="Звуки выстрела, попадания и взрыва"),
    )
    write("21-20-animatsiya-vzryva.html", out)


def build_21() -> None:
    body = f"""
    <p>Три коротких звука дополняют игру: выстрел, взрыв и попадание по кораблю. Все они —
    оригинальные, синтезированные напрямую в Python через встроенный модуль
    <code class="inline">wave</code> (короткие синус-сигналы и затухающий шум), без единой
    скачанной из интернета записи.</p>
    {code_block(
        "fragment_play_sound.py",
        "def play(self, key):\n"
        "    sound = self.sounds.get(key)\n"
        "    if sound is not None:\n"
        "        sound.play()\n\n"
        "# при выстреле:\n"
        "self.assets.play(\"laser\")\n\n"
        "# при уничтожении врага:\n"
        "self.assets.play(\"explosion\")\n\n"
        "# при ударе по кораблю:\n"
        "self.assets.play(\"player_hit\")\n",
    )}
    {callout(
        "warning",
        "sound может быть None — и это нормально",
        "Раздел 21.10 уже показал: если звуковое устройство недоступно, "
        "<code class=\"inline\">AssetStore</code> хранит <code class=\"inline\">None</code> "
        "вместо объекта <code class=\"inline\">Sound</code>. Проверка <code class=\"inline\">"
        "if sound is not None</code> перед каждым <code class=\"inline\">.play()</code> "
        "гарантирует, что игра (и автоматические тесты, раздел 21.24) не падает без звуковой "
        "карты — просто играет молча.",
    )}
    {callout(
        "info",
        "Звук загружается один раз, как и изображения",
        "Раздел 20.24 уже предупреждал: <code class=\"inline\">pygame.mixer.Sound(...)</code> "
        "читает файл с диска — вызывать его внутри игрового цикла на каждый выстрел означало бы "
        "читать один и тот же файл заново десятки раз в секунду. Здесь загрузка происходит один "
        "раз в <code class=\"inline\">AssetStore.__init__()</code>, а внутри цикла вызывается "
        "только <code class=\"inline\">.play()</code> у уже загруженного объекта.",
    )}
    """
    out = render_page(
        page_title="Звуки выстрела, попадания и взрыва",
        description="Три оригинальных синтезированных звука, загруженных один раз, и безопасное проигрывание, устойчивое к отсутствию звукового устройства.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Звуки выстрела, попадания и взрыва", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Звуки выстрела, попадания и взрыва",
        lede="Три коротких звука — загруженные один раз, и молча пропускаемые без звуковой карты.",
        body_html=body,
        sidebar_groups=sidebar("21-21-zvukovye-effekty.html"),
        nav=PageNav(prev_href="21-20-animatsiya-vzryva.html", prev_label="Анимация взрыва", next_href="21-22-zvyozdnyj-fon.html", next_label="Звёздный фон и порядок отрисовки"),
    )
    write("21-21-zvukovye-effekty.html", out)


def build_22() -> None:
    body = f"""
    <p>Последний штрих атмосферы — звёздный фон. Вместо готового изображения звёзды рисуются
    процедурно: список маленьких точек с собственной скоростью и цветом, каждая из которых
    зацикливается сверху вниз.</p>
    {code_block(
        "fragment_stars.py",
        "def _update_stars(self, dt):\n"
        "    for star in self.stars:\n"
        "        star.y += star.speed * dt\n"
        "        if star.y > self.playfield.bottom:\n"
        "            star.y = self.playfield.top\n"
        "            star.x = self.rng.uniform(0, SHIRINA)\n",
    )}
    <p>У разных звёзд — разная скорость (от 20 до 90 px/s), поэтому они создают лёгкое ощущение
    глубины: быстрые точки ближе, медленные — дальше, тот же зрительный приём, что параллакс в
    более сложных играх, только без отдельных слоёв.</p>

    <h2>Порядок отрисовки решает, что оказывается «поверх»</h2>
    {pipeline_diagram([
        {"kind": "plain", "title": "Фон и звёзды", "rows": ["screen.fill(...)", "_render_stars()"]},
        {"kind": "plain", "title": "Враги", "rows": ["self.enemies.draw(screen)"]},
        {"kind": "plain", "title": "Пули", "rows": ["self.bullets.draw(screen)"]},
        {"kind": "plain", "title": "Корабль игрока", "rows": ["screen.blit(player.image, player.rect)"]},
        {"kind": "plain", "title": "Взрывы", "rows": ["self.explosions.draw(screen)"]},
        {"kind": "plain", "title": "HUD", "rows": ["счёт, жизни, волна — своя полоса сверху"]},
        {"kind": "plain", "title": "Оверлей состояния", "rows": ["меню / пауза / Game Over — поверх всего"]},
    ], caption="Каждый следующий слой рисуется поверх предыдущего — HUD и оверлей состояния всегда видны, что бы ни происходило на игровом поле.")}
    {callout(
        "info",
        "Порядок — линейный список, а не случайное совпадение",
        "Раздел 20.13 (мобильный опыт) и раздел 21.12 уже подчёркивали: интерфейс не должен "
        "теряться под игровыми объектами. Раздел HUD и оверлей рисуются здесь последними именно "
        "поэтому — они физически не могут оказаться под врагом или взрывом.",
    )}
    """
    out = render_page(
        page_title="Звёздный фон и порядок отрисовки",
        description="Процедурный звёздный фон без готового изображения и явный порядок слоёв отрисовки кадра.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Звёздный фон и порядок отрисовки", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Звёздный фон и порядок отрисовки",
        lede="Процедурные звёзды вместо готового изображения — и явный порядок слоёв, чтобы HUD всегда оставался поверх.",
        body_html=body,
        sidebar_groups=sidebar("21-22-zvyozdnyj-fon.html"),
        nav=PageNav(prev_href="21-21-zvukovye-effekty.html", prev_label="Звуки выстрела, попадания и взрыва", next_href="21-23-otladka-shutera.html", next_label="Как находить и исправлять ошибки в шутере"),
    )
    write("21-22-zvyozdnyj-fon.html", out)


def build_23() -> None:
    body = f"""
    <p>По ходу главы уже встретилось больше двадцати способов случайно сломать шутер — от старых,
    основанных на кадрах, приёмов до тонких ошибок с двойным подсчётом очков. Здесь они собраны в
    один справочник.</p>

    {comparison_table(
        ["Симптом", "Причина", "Где подробнее"],
        [
            ["Скорость корабля зависит от FPS", "Движение задано «пикселей за кадр», а не px/s через dt", "21.11"],
            ["Медленное движение вообще не сдвигается", "Позиция хранится только в Rect (целые числа) — дробная часть теряется", "21.11"],
            ["По диагонали корабль быстрее, чем по прямой", "Вектор направления не нормализован", "21.11"],
            ["Корабль вылетает за пределы игрового поля", "Забыт clamp по X и/или Y в Player.move()", "21.11"],
            ["Корабль заезжает под HUD", "Границы движения — всё окно, а не self.playfield", "21.12"],
            ["Пробел стреляет каждый отрисованный кадр", "Нет проверки fire_cooldown перед выстрелом", "21.13"],
            ["Скорострельность зависит от FPS", "Интервал между выстрелами измеряется кадрами (-= 1), а не секундами (-= dt)", "21.13"],
            ["После долгой паузы отладчика — залп из десятков пуль", "Интервал между выстрелами реализован через while вместо if", "21.13"],
            ["Пули летят вечно, игра тормозит сильнее с каждой минутой", "Bullet не удаляет себя за пределами игрового поля", "21.16 (Bullet.update)"],
            ["Появление врагов зависит от FPS", "Таймер появления врагов считает кадры, а не секунды", "21.14"],
            ["После просадки FPS «пропадают» запланированные враги", "Таймер появления врагов использует if вместо while", "21.14"],
            ["Враг появляется наполовину за краем экрана", "x_poyavleniya_vraga не учитывает ширину врага", "21.14"],
            ["Один враг помечен уничтоженным дважды", "Список мутируется прямо во время перебора (как и в разделе 21.6)", "21.15"],
            ["Одному врагу засчитывают очки дважды", "Подсчёт идёт по всем парам пуля–враг, а не по множеству уникальных врагов", "21.15"],
            ["Три одновременных врага отнимают три жизни", "Урон применяется за каждое столкновение, а не один раз за кадр", "21.16"],
            ["Неуязвимость «тикает» на паузе", "Таймер неуязвимости обновляется вне update_playing(), не проверяя state", "21.16, 21.18"],
            ["На экране Game Over корабль всё ещё двигается", "handle_input() не проверяет self.state перед обработкой клавиш", "21.18"],
            ["После перезапуска остаются старые пули или враги", "start_new_game() не очищает все группы спрайтов", "21.19"],
            ["После перезапуска враг появляется мгновенно", "spawn_timer не сброшен к начальному интервалу", "21.19"],
            ["Анимация взрыва «проглатывает» кадры на слабом устройстве", "Explosion.update() использует if вместо while", "21.20"],
            ["Игра подтормаживает перед каждым выстрелом или взрывом", "Изображение или звук загружается внутри игрового цикла, а не в AssetStore", "21.10, 21.21"],
            ["Игра падает без звуковой карты", "Sound.play() вызывается без проверки на None", "21.21"],
            ["HUD перекрыт врагом или взрывом", "Порядок отрисовки не выносит HUD и оверлей последними слоями", "21.22"],
            ["rect и position со временем «расходятся»", "Rect обновлён напрямую, а не пересобран из position", "21.11"],
            ["Тест столкновений то проходит, то падает без изменений в коде", "Random используется напрямую, без переданного seed", "21.24"],
        ],
    )}

    <h2>Разберём три самых незаметных ошибки подробнее</h2>

    {callout(
        "debug",
        "[[icon:debug]] Субпиксельное движение теряется на медленных объектах",
        "<strong>Симптом:</strong> объект со скоростью меньше одного пикселя за кадр вообще не "
        "двигается. <strong>Ломаная версия:</strong> <code class=\"inline\">self.rect.x += "
        "self.speed * dt</code> — Rect хранит только целые числа, и дробное приращение "
        "округляется в ноль на каждом кадре по отдельности. <strong>Почему:</strong> округление "
        "происходит каждый раз, а не один раз в конце. <strong>Исправление:</strong> "
        "накапливать движение в <code class=\"inline\">self.position</code> (Vector2, раздел "
        "21.11), а <code class=\"inline\">rect.center</code> пересобирать из неё через "
        "<code class=\"inline\">round()</code> каждый кадр. <strong>Правило:</strong> позиция — "
        "всегда float, Rect — производная от неё, никогда не наоборот.",
    )}
    {callout(
        "debug",
        "[[icon:debug]] Один враг засчитан дважды",
        "<strong>Симптом:</strong> счёт иногда прыгает на 200 вместо 100 за одного разведчика. "
        "<strong>Ломаная версия:</strong> <code class=\"inline\">for pulya, vragi in "
        "collisions.items(): schet += sum(v.points for v in vragi)</code> — суммирование по всем "
        "парам пуля–враг. <strong>Почему:</strong> если две пули задели одного врага в одном "
        "обновлении, он попадёт в списки обеих пуль. <strong>Исправление:</strong> собрать всех "
        "задетых врагов в <code class=\"inline\">set</code> перед подсчётом очков (раздел 21.15). "
        "<strong>Правило:</strong> считать очки по уникальным уничтоженным объектам, а не по "
        "числу столкновений.",
    )}
    {callout(
        "debug",
        "[[icon:debug]] Три врага одновременно отнимают три жизни",
        "<strong>Симптом:</strong> лобовое столкновение с группой врагов сразу переводит игру в "
        "Game Over, хотя жизней было три. <strong>Ломаная версия:</strong> "
        "<code class=\"inline\">for vrag in hit: self.lives -= 1</code> — урон внутри цикла по "
        "столкнувшимся врагам. <strong>Почему:</strong> цикл списывает жизнь за каждого врага, "
        "а не за сам факт столкновения. <strong>Исправление:</strong> проверить \"было ли хоть "
        "одно столкновение\" один раз после цикла и списать не больше одной жизни за кадр (раздел "
        "21.16). <strong>Правило:</strong> урон измеряется событием «задели», а не количеством "
        "объектов, которые это сделали одновременно.",
    )}

    {practice_revisit_card(
        "21-08",
        "Практика: найдите и исправьте ошибку",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/21-08/index.html",
    )}
    """
    out = render_page(
        page_title="Как находить и исправлять ошибки в шутере",
        description="Справочник типичных ошибок финального проекта по симптому, и разбор трёх самых незаметных из них.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Как находить и исправлять ошибки в шутере", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Как находить и исправлять ошибки в шутере",
        lede="Справочник по симптому — плюс подробный разбор трёх самых незаметных ошибок проекта.",
        body_html=body,
        sidebar_groups=sidebar("21-23-otladka-shutera.html"),
        nav=PageNav(prev_href="21-22-zvyozdnyj-fon.html", prev_label="Звёздный фон и порядок отрисовки", next_href="21-24-testiruemost.html", next_label="Как сделать игру удобной для автоматических тестов"),
    )
    write("21-23-otladka-shutera.html", out)


def build_24() -> None:
    body = f"""
    <p>Игру размером с этот проект нельзя проверить только запуском вручную — слишком много
    комбинаций состояний. Финальная версия написана так, чтобы её можно было тестировать
    автоматически, без единого настоящего окна.</p>

    <h2>Чистые функции: логика без Pygame</h2>
    <p>Формулы сложности (раздел 21.17), координата появления врага (раздел 21.14) и подсчёт
    очков (раздел 21.15) — обычные функции от чисел и списков, без обращения к
    <code class="inline">self</code> или экрану:</p>
    {code_block(
        "fragment_pure_functions.py",
        "def ochki_za_unichtozhennyh(vragi):\n"
        "    return sum(vrag.points for vrag in vragi)\n\n"
        "# Чистой функции не нужен настоящий Enemy со спрайтом и картинкой —\n"
        "# достаточно любого объекта с атрибутом points:\n"
        "class ZaglushkaVraga:\n"
        "    def __init__(self, points):\n"
        "        self.points = points\n\n"
        "assert ochki_za_unichtozhennyh([]) == 0\n"
        "assert ochki_za_unichtozhennyh(\n"
        "    [ZaglushkaVraga(points=100), ZaglushkaVraga(points=200)]\n"
        ") == 300\n",
    )}
    <p>Это не обход правил, а прямое следствие того, что <code class="inline">ochki_za_unichtozhennyh</code>
    вообще не проверяет, какого класса переданные объекты — ей нужен только атрибут
    <code class="inline">.points</code> у каждого. Такую функцию можно протестировать любым
    объектом с этим атрибутом, вплоть до простой заглушки, без запуска Pygame и без создания
    настоящих врагов.</p>

    <h2>Управляемая случайность: Game(rng=...)</h2>
    <p>Игра принимает генератор случайных чисел явным параметром, а не обращается к глобальному
    <code class="inline">random</code> напрямую:</p>
    {code_block(
        "fragment_rng_injection.py",
        "class Game:\n"
        "    def __init__(self, *, rng=None):\n"
        "        self.rng = rng if rng is not None else random.Random()\n\n"
        "# в реальной игре — обычная непредсказуемая случайность:\n"
        "game = Game()\n\n"
        "# в тестах и при генерации скриншотов — воспроизводимая:\n"
        "game = Game(rng=random.Random(42))\n",
    )}
    {callout(
        "tip",
        "Один и тот же seed — один и тот же результат",
        "<code class=\"inline\">random.Random(42)</code> с фиксированным зерном (seed) даёт "
        "одну и ту же последовательность случайных чисел при каждом запуске — поэтому появление "
        "врагов, их тип и позиция становятся воспроизводимыми: удобно и для тестов, и для "
        "детерминированных сценариев — например, для скриншотов, снятых с конкретного, заранее "
        "известного состояния игры.",
    )}

    <h2>Запуск без окна: «пустой» SDL-драйвер (headless)</h2>
    <p>Тот же приём, что и во всех тестах главы 20: переменные окружения переключают Pygame на
    «пустой» (dummy) видео- и аудиодрайвер SDL — окно нигде физически не появляется, но вся
    логика (Surface, Rect, столкновения, звук) работает по-настоящему. Такой запуск без
    настоящего окна в англоязычной терминологии называют headless — «без головы», то есть без
    экрана и без пользовательского интерфейса.</p>
    {code_block(
        "fragment_headless_env.py",
        "import os\n\n"
        "os.environ.setdefault(\"SDL_VIDEODRIVER\", \"dummy\")\n"
        "os.environ.setdefault(\"SDL_AUDIODRIVER\", \"dummy\")\n\n"
        "import space_shooter as ss\n\n"
        "game = ss.Game()   # реальный Game, без настоящего окна\n",
    )}
    {callout(
        "warning",
        "Никакой тяжёлой работы при простом импорте модуля",
        "<code class=\"inline\">space_shooter.py</code> не вызывает "
        "<code class=\"inline\">pygame.init()</code> или <code class=\"inline\">Game().run()</code> "
        "на уровне модуля — вся инициализация происходит внутри "
        "<code class=\"inline\">Game.__init__()</code>, а бесконечный цикл — только внутри "
        "<code class=\"inline\">if __name__ == \"__main__\":</code>. Иначе просто "
        "<code class=\"inline\">import space_shooter</code> в тесте запустил бы настоящую игру.",
    )}
    """
    out = render_page(
        page_title="Как сделать игру удобной для автоматических тестов",
        description="Чистые функции, внедрение генератора случайных чисел с предсказуемым (детерминированным) результатом и запуск игры без окна для автоматических тестов.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Как сделать игру удобной для автоматических тестов", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Как сделать игру удобной для автоматических тестов",
        lede="Чистые функции, Game(rng=...) и запуск без окна — игра, которую можно проверить автоматически.",
        body_html=body,
        sidebar_groups=sidebar("21-24-testiruemost.html"),
        nav=PageNav(prev_href="21-23-otladka-shutera.html", prev_label="Как находить и исправлять ошибки в шутере", next_href="21-25-finalnaya-arhitektura.html", next_label="Собираем финальную версию игры"),
    )
    write("21-24-testiruemost.html", out)


def build_25() -> None:
    body = f"""
    <p>Все разделы 21.9–21.24 собираются в один файл —
    <code class="inline">projects/pygame/space-shooter/space_shooter.py</code>. Он не разбит на
    несколько модулей: проект достаточно компактен, чтобы один читаемый файл был понятнее, чем
    россыпь из десятка мелких.</p>
    <p>[[icon:file]] <a href="../../../projects/pygame/space-shooter/space_shooter.py">projects/pygame/space-shooter/space_shooter.py</a></p>

    {object_diagram(
        "game", "Game",
        [
            ("state", "GameStatus.PLAYING"),
            ("score", "640"),
            ("lives", "3"),
            ("player.position", "(240.0, 612.0)"),
            ("bullets", "3 спрайта"),
            ("enemies", "4 спрайта"),
        ],
        caption="Реальное состояние работающей игры в конкретный момент — то, что на самом деле хранится в памяти между кадрами.",
    )}

    <h2>Что изменилось по сравнению с первой рабочей версией (21.8)</h2>
    {comparison_table(
        ["", "Раздел 21.8 (checkpoint)", "Финальная версия (21.25)"],
        [
            ["Организация кода", "Функции и словари/списки поверх Rect", "Классы Game/Player/Bullet/Enemy/Explosion поверх pygame.sprite.Group"],
            ["Движение", "px/s + dt, дробные координаты хранятся отдельно от Rect", "px/s + dt через Vector2 внутри классов Player/Bullet/Enemy"],
            ["Графика", "Закрашенные прямоугольники", "Собственные PNG-спрайты"],
            ["Звук", "Нет", "Три оригинальных синтезированных звука"],
            ["Конец игры", "Одно столкновение — мгновенный конец", "Система жизней с неуязвимостью"],
            ["Сложность", "Постоянная", "Растёт плавно вместе со счётом"],
            ["Состояния", "Одна булева переменная", "GameStatus: MENU/PLAYING/PAUSED/GAME_OVER"],
            ["Перезапуск", "Только перезапуск Python", "Enter на экране Game Over"],
            ["Взрывы", "Нет", "Анимация из нескольких кадров"],
            ["Тесты", "7 регрессионных тестов таймера и движения (раздел 21.3)", "38 тестов класса Game и вспомогательных функций, включая FPS-независимость"],
        ],
    )}
    {image_figure(f"{IMG}/25-final-gameplay.png", "Реальное окно: насыщенный кадр геймплея — синий корабль, несколько врагов и пуль, звёздный фон, читаемый HUD со счётом 640", "Реальный кадр финальной версии — тот же корабль, что и в разделе 21.2, но выросший в полноценную игру.", width=320)}

    {exercise(3, "Ещё один тип врага", "Добавьте третий EnemySpec — например, \"bomber\": медленный, но с большим количеством очков и собственным спрайтом (расширьте scripts/generate_chapter_21_assets.py).")}
    {exercise(3, "Бонусы на игровом поле", "Добавьте класс PowerUp: подбираемый объект, временно уменьшающий FIRE_INTERVAL после столкновения с кораблём — используйте тот же приём таймера, что и для неуязвимости.")}

    {local_required_card(
        "21-25",
        "Практика: собираем и запускаем финальную игру",
        "Pygame открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
        "../../practice/21-25/index.html",
    )}
    """
    out = render_page(
        page_title="Собираем финальную версию игры",
        description="Полный исходный код финальной версии космического шутера, сравнение с первой рабочей версией и идеи для дальнейшего развития.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Собираем финальную версию игры", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Собираем финальную версию игры",
        lede="Все разделы 21.9–21.24 — в одном читаемом, готовом к запуску файле.",
        body_html=body,
        sidebar_groups=sidebar("21-25-finalnaya-arhitektura.html"),
        nav=PageNav(prev_href="21-24-testiruemost.html", prev_label="Как сделать игру удобной для автоматических тестов", next_href="21-26-itogi-proekta.html", next_label="Что мы построили и как развивать игру дальше"),
    )
    write("21-25-finalnaya-arhitektura.html", out)


def build_26() -> None:
    body = f"""
    <p>Космический шутер завершён — а вместе с ним закрывается и вторая большая тема курса:
    полноценная разработка игр на Pygame, от первого окна в главе 20 до тестируемой, озвученной
    игры с собственной графикой здесь.</p>

    {summary_box("Что мы построили в этой главе", [
        "Полноценную игру из пяти классов: <code class=\"inline\">Game</code>, "
        "<code class=\"inline\">Player</code>, <code class=\"inline\">Bullet</code>, "
        "<code class=\"inline\">Enemy</code>, <code class=\"inline\">Explosion</code> — вместо "
        "глобальных переменных и списков.",
        "Точное движение через <code class=\"inline\">Vector2</code> и delta time — тот же принцип "
        "из главы 20, применённый к настоящему проекту с несколькими типами объектов сразу.",
        "Таймеры, которые различают автономную симуляцию (появление врагов, анимация — сохраняют "
        "остаток времени сверх интервала через while) и реакцию на ввод игрока (интервал между "
        "выстрелами — не более одного события за кадр).",
        "Столкновения через <code class=\"inline\">pygame.sprite.groupcollide()</code> и "
        "<code class=\"inline\">spritecollide()</code>, с защитой от двойного подсчёта очков и "
        "от потери нескольких жизней за одно одновременное столкновение.",
        "Явные состояния игры (<code class=\"inline\">GameStatus</code>) и контракт перезапуска, "
        "сбрасывающий действительно всё переходное состояние — не только счёт.",
        "Собственную графику и звук, загруженные один раз, и игру, которую можно проверить "
        "автоматически — через внедрение генератора случайных чисел и запуск без окна под "
        "«пустым» SDL-драйвером (headless).",
    ])}

    <h2>Куда развивать проект дальше</h2>
    {capability_map([
        ("Больше типов врагов", ["Собственные паттерны движения (зигзаг, наведение на корабль)", "Собственные спрайты и очки"]),
        ("Бонусы и усиления", ["Временные эффекты через тот же приём таймера, что и неуязвимость", "Щит, двойной выстрел, дополнительная жизнь"]),
        ("Боссы", ["Крупный враг с собственным здоровьем (не одно попадание)", "Собственный набор атак"]),
        ("Сохранение рекорда", ["Запись high_score в файл между запусками (глава 15)", "Не только в рамках одной сессии"]),
    ], title="Идеи для самостоятельного развития")}

    <p>Следующая глава меняет направление: от локальных игр на Pygame — к веб-разработке на
    Python. Принципы, освоенные здесь — чёткое разделение обязанностей между классами, явные
    состояния, тестируемый код — пригодятся и там, просто в других декорациях.</p>
    """
    out = render_page(
        page_title="Что мы построили и как развивать игру дальше",
        description="Итоги главы 21: чему научил космический шутер целиком, и идеи для его дальнейшего развития.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 21", "index.html"), ("Что мы построили и как развивать игру дальше", "")],
        kicker="Глава 21 · Проект: космический шутер",
        h1="Что мы построили и как развивать игру дальше",
        lede="От первого окна в главе 20 до тестируемой, озвученной игры с собственной графикой.",
        body_html=body,
        sidebar_groups=sidebar("21-26-itogi-proekta.html"),
        nav=PageNav(prev_href="21-25-finalnaya-arhitektura.html", prev_label="Собираем финальную версию игры", next_href="../glava-22/index.html", next_label="Глава 22: Веб-разработка с Python"),
    )
    write("21-26-itogi-proekta.html", out)


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
