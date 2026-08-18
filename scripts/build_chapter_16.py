#!/usr/bin/env python3
"""Строит Главу 16: «Создаём классные приложения с Tkinter» (site/chapters/glava-16/).

Curriculum v2: полноценная основа событийно-ориентированного GUI-программирования.
Путь: ТЕРМИНАЛ → GUI → СОБЫТИЙНЫЙ ЦИКЛ → root/Tk → ДЕРЕВО ВИДЖЕТОВ → CALLBACK/COMMAND →
pack/Frame → grid/адаптивность → place → Entry/Text → Tk-переменные → виджеты выбора →
меню → messagebox/filedialog → Toplevel → focus → after()/таймеры → почему sleep
замораживает интерфейс → валидация → архитектура (чистая логика + виджеты) →
класс приложения → персистентные настройки (мост к главе 15) → проекты → итоги.
Центральная модель: PROGRAM START → CREATE ROOT → BUILD WIDGET TREE → CONFIGURE STATE
→ REGISTER CALLBACKS → mainloop() → WAIT FOR EVENTS → DISPATCH CALLBACK → READ/CHANGE
STATE → UPDATE UI → назад в цикл событий.

Существующие маршруты и практики (16-01..16-08) сохранены на месте и расширены по
тому же шаблону, что и в главах 12-15; новый материал — новые страницы и новые ID
практик (16-09..16-32), без переиспользования занятых ID. Итоги главы переехали на
новую страницу 16-33 (как в 14-27/15-31) — 16-08 остаётся калькулятором чаевых
(теперь как «фундамент» проекта, расширяемого в 16-31 «Tip Calculator Pro»).
"""

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
    comparison_table,
    decision_map,
    exercise,
    flow_diagram,
    image_figure,
    local_required_card,
    object_diagram,
    pipeline_diagram,
    practice_card,
    relationship_diagram,
    render_chapter_opener,
    render_page,
    summary_box,
    tree_diagram,
)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "chapters" / "glava-16"
IMG = "../../assets/img/chapter-16/output"
PLATFORM_NOTE = "Пример внешнего вида на среде курса. На вашей ОС шрифты, размеры и тема могут немного отличаться."

PAGES = [
    ("index.html", "Обзор главы"),
    ("16-01-nastraivaem-tkinter.html", "Tkinter — правильно всё настраиваем!"),
    ("16-02-metki-knopki-pack.html", "Метки, кнопки и pack"),
    ("16-03-polya-vvoda.html", "Поля ввода"),
    ("16-04-peremennye-tkinter.html", "Переменные Tkinter"),
    ("16-05-mnozhestvo-variantov.html", "Множество вариантов!"),
    ("16-06-menu.html", "Меню"),
    ("16-07-grid.html", "Идеальная компоновка — grid"),
    ("16-08-mini-proekt-chaevye-itogi.html", "Мини-проект: калькулятор чаевых"),
    ("16-09-ot-terminala-k-gui.html", "От терминала к GUI: событийная модель"),
    ("16-10-event-loop-i-mainloop.html", "Как работает событийный цикл и mainloop"),
    ("16-11-derevo-widgetov.html", "Виджет и дерево интерфейса"),
    ("16-12-tk-i-ttk.html", "tk и ttk: классические и тематизированные виджеты"),
    ("16-13-frame-i-labelframe.html", "Frame и LabelFrame: организуем интерфейс"),
    ("16-14-pack-podrobno.html", "pack подробно: fill, expand и вложенные фреймы"),
    ("16-15-adaptivny-grid.html", "Адаптивный grid: sticky и weight"),
    ("16-16-widgety-vybora.html", "Виджеты выбора: Combobox, Listbox, Spinbox, Scale"),
    ("16-17-progressbar-i-notebook.html", "Progressbar и вкладки Notebook"),
    ("16-18-messagebox-i-dialogi.html", "Messagebox и диалоги"),
    ("16-19-filedialog-i-pathlib.html", "Открываем и сохраняем файлы: filedialog и pathlib"),
    ("16-20-toplevel.html", "Toplevel: несколько окон"),
    ("16-21-focus-i-dostupnost.html", "Focus, клавиатура и основы доступности"),
    ("16-22-after-tajmery.html", "after(): таймеры без блокировки"),
    ("16-23-validatsiya-vvoda.html", "Валидация ввода и обратная связь"),
    ("16-24-arhitektura-prilozheniya.html", "Архитектура приложения: логика отдельно от виджетов"),
    ("16-25-klass-prilozheniya-i-nastrojki.html", "Класс приложения и персистентные настройки"),
    ("16-26-mini-proekt-schetchik-klikov.html", "Мини-проект: счётчик кликов"),
    ("16-27-mini-proekt-konverter-temperatur.html", "Мини-проект: конвертер температур"),
    ("16-28-mini-proekt-tajmer.html", "Мини-проект: таймер обратного отсчёта"),
    ("16-29-mini-proekt-todo.html", "Мини-проект: список задач"),
    ("16-30-mini-proekt-zametki.html", "Мини-проект: редактор заметок"),
    ("16-31-tip-calculator-pro.html", "Tip Calculator Pro: финальная версия"),
    ("16-32-debugging-i-kachestvo.html", "Отладка интерфейса и качество GUI"),
    ("16-33-itogi-glavy.html", "Итоги главы: инструментарий Tkinter"),
]

PRACTICE_IDS = [
    "16-01", "16-02", "16-03", "16-04", "16-05", "16-06", "16-07", "16-08",
    "16-09", "16-10", "16-11", "16-12", "16-13", "16-14", "16-15", "16-16",
    "16-17", "16-18", "16-19", "16-20", "16-21", "16-22", "16-23", "16-24",
    "16-25", "16-26", "16-27", "16-28", "16-29", "16-30", "16-31", "16-32",
]

LOCAL_REQUIRED_IDS = {
    "16-01", "16-02", "16-03", "16-04", "16-05", "16-06", "16-07", "16-08",
    "16-12", "16-13", "16-14", "16-16", "16-17", "16-18", "16-19", "16-20",
    "16-22", "16-26", "16-30", "16-31",
}


def sidebar(active_href: str) -> list[SidebarGroup]:
    items = [NavItem(title, href) for href, title in PAGES]
    for it in items:
        it.active = it.href == active_href
    return [
        SidebarGroup("Глава 16 · Tkinter", items),
        SidebarGroup("Практика", [
            NavItem(f"🐍 {lid}: Практика", f"../../practice/{lid}/index.html") for lid in PRACTICE_IDS
        ]),
    ]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    clean = "\n".join(line.rstrip() for line in html_out.split("\n"))
    path.write_text(clean, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


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
    """Единый компонент Debug Lab (введён в главе 14): сломанный код → что
    происходит на экране → объяснение → исправленный код."""
    return f"""
    <div style="margin:28px 0;padding:4px 4px 20px;border:2px dashed #DB2777;border-radius:var(--radius-lg,20px)">
      <div style="padding:14px 20px 4px;font-family:Sora,sans-serif;font-weight:700;font-size:13px;
        letter-spacing:.05em;text-transform:uppercase;color:#DB2777">🐞 Debug Lab {n}: {title}</div>
      <div style="padding:0 20px">
{code_block(broken_code_filename, broken_code)}
{terminal_transcript(symptom_lines, caption="Что видно на экране")}
        <p>{explanation_html}</p>
        <div style="font-family:Sora,sans-serif;font-weight:700;font-size:12px;letter-spacing:.05em;
          text-transform:uppercase;color:#059669;margin:16px 0 8px">Исправленный код</div>
{code_block(fixed_code_filename, fixed_code)}
      </div>
    </div>"""


def two_up(left_html: str, right_html: str) -> str:
    return f"""
    <div style="display:flex;gap:20px;flex-wrap:wrap;margin:20px 0;align-items:flex-start">
      <div style="flex:1 1 260px;min-width:220px">{left_html}</div>
      <div style="flex:1 1 260px;min-width:220px">{right_html}</div>
    </div>"""


def gui_checklist(items: list[str], *, title: str = "Чек-лист") -> str:
    rows = "".join(
        f'<div style="display:flex;gap:10px;align-items:flex-start;padding:6px 0">'
        f'<span style="color:#5B24F9;font-weight:700">☐</span><span>{item}</span></div>'
        for item in items
    )
    return f"""
    <div style="margin:24px 0;padding:18px 22px;background:var(--color-bg-surface,#FAFAFC);
      border-radius:var(--radius-lg,20px)">
      <div style="font-family:Sora,sans-serif;font-weight:700;font-size:14px;margin-bottom:10px">{title}</div>
      {rows}
    </div>"""


_HREFS = [h for h, _ in PAGES]
_TITLES = dict(PAGES)


def nav_for(current_href: str) -> PageNav:
    i = _HREFS.index(current_href)
    prev_href, prev_label = (_HREFS[i - 1], _TITLES[_HREFS[i - 1]]) if i > 0 else (None, None)
    if i < len(_HREFS) - 1:
        next_href, next_label = _HREFS[i + 1], _TITLES[_HREFS[i + 1]]
    else:
        next_href, next_label = "../glava-17/index.html", "Глава 17: Проект: игра «Крестики-нолики» с Tkinter"
    return PageNav(prev_href=prev_href, prev_label=prev_label, next_href=next_href, next_label=next_label)


def page(href: str, *, page_title: str, description: str, kicker_suffix: str, h1: str, lede: str, body_html: str) -> None:
    out = render_page(
        page_title=page_title,
        description=description,
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 16", "index.html"), (kicker_suffix, "")],
        kicker="Глава 16 · Создаём классные приложения с Tkinter",
        h1=h1,
        lede=lede,
        body_html=body_html,
        sidebar_groups=sidebar(href),
        nav=nav_for(href),
    )
    write(href, out)


def local_or_practice(lesson_id: str, title: str, sub_browser: str, href: str) -> str:
    if lesson_id in LOCAL_REQUIRED_IDS:
        return local_required_card(
            lesson_id, title,
            "Модуль tkinter открывает нативное окно Python — выполните локально в VS Code, PyCharm или Jupyter",
            href,
        )
    return practice_card(lesson_id, title, sub_browser, href)


def build_opener() -> None:
    out = render_chapter_opener(
        chapter_num=16,
        baseline_page=335,
        title="Создаём классные приложения с Tkinter",
        description="Научимся строить настоящие оконные приложения: разберём событийную модель, "
        "дерево виджетов, адаптивную компоновку, формы, меню, диалоги, таймеры и архитектуру "
        "приложения — и свяжем интерфейс с функциями, объектами и файлами из предыдущих глав.",
        meta_items=["⏱ ~10 часов", "🖼️ tkinter, ttk, mainloop", "📓 32 практики"],
        sections=[
            ChapterSectionLink("16.1", "Tkinter — правильно всё настраиваем!", "16-01-nastraivaem-tkinter.html", "335"),
            ChapterSectionLink("16.2", "Метки, кнопки и pack", "16-02-metki-knopki-pack.html", "338"),
            ChapterSectionLink("16.3", "Поля ввода", "16-03-polya-vvoda.html", "341"),
            ChapterSectionLink("16.4", "Переменные Tkinter", "16-04-peremennye-tkinter.html", "344"),
            ChapterSectionLink("16.5", "Множество вариантов!", "16-05-mnozhestvo-variantov.html", "346"),
            ChapterSectionLink("16.6", "Меню", "16-06-menu.html", "349"),
            ChapterSectionLink("16.7", "Идеальная компоновка — grid", "16-07-grid.html", "351"),
            ChapterSectionLink("16.8", "Мини-проект: калькулятор чаевых", "16-08-mini-proekt-chaevye-itogi.html", "353"),
            ChapterSectionLink("16.9", "От терминала к GUI: событийная модель", "16-09-ot-terminala-k-gui.html", "356"),
            ChapterSectionLink("16.10", "Как работает событийный цикл и mainloop", "16-10-event-loop-i-mainloop.html", "358"),
            ChapterSectionLink("16.11", "Виджет и дерево интерфейса", "16-11-derevo-widgetov.html", "360"),
            ChapterSectionLink("16.12", "tk и ttk", "16-12-tk-i-ttk.html", "362"),
            ChapterSectionLink("16.13", "Frame и LabelFrame", "16-13-frame-i-labelframe.html", "364"),
            ChapterSectionLink("16.14", "pack подробно", "16-14-pack-podrobno.html", "366"),
            ChapterSectionLink("16.15", "Адаптивный grid", "16-15-adaptivny-grid.html", "368"),
            ChapterSectionLink("16.16", "Виджеты выбора", "16-16-widgety-vybora.html", "370"),
            ChapterSectionLink("16.17", "Progressbar и Notebook", "16-17-progressbar-i-notebook.html", "372"),
            ChapterSectionLink("16.18", "Messagebox и диалоги", "16-18-messagebox-i-dialogi.html", "374"),
            ChapterSectionLink("16.19", "filedialog и pathlib", "16-19-filedialog-i-pathlib.html", "376"),
            ChapterSectionLink("16.20", "Toplevel: несколько окон", "16-20-toplevel.html", "378"),
            ChapterSectionLink("16.21", "Focus, клавиатура и доступность", "16-21-focus-i-dostupnost.html", "380"),
            ChapterSectionLink("16.22", "after(): таймеры без блокировки", "16-22-after-tajmery.html", "382"),
            ChapterSectionLink("16.23", "Валидация ввода", "16-23-validatsiya-vvoda.html", "384"),
            ChapterSectionLink("16.24", "Архитектура приложения", "16-24-arhitektura-prilozheniya.html", "386"),
            ChapterSectionLink("16.25", "Класс приложения и настройки", "16-25-klass-prilozheniya-i-nastrojki.html", "388"),
            ChapterSectionLink("16.26", "Мини-проект: счётчик кликов", "16-26-mini-proekt-schetchik-klikov.html", "390"),
            ChapterSectionLink("16.27", "Мини-проект: конвертер температур", "16-27-mini-proekt-konverter-temperatur.html", "391"),
            ChapterSectionLink("16.28", "Мини-проект: таймер обратного отсчёта", "16-28-mini-proekt-tajmer.html", "393"),
            ChapterSectionLink("16.29", "Мини-проект: список задач", "16-29-mini-proekt-todo.html", "395"),
            ChapterSectionLink("16.30", "Мини-проект: редактор заметок", "16-30-mini-proekt-zametki.html", "397"),
            ChapterSectionLink("16.31", "Tip Calculator Pro", "16-31-tip-calculator-pro.html", "399"),
            ChapterSectionLink("16.32", "Отладка интерфейса и качество GUI", "16-32-debugging-i-kachestvo.html", "401"),
            ChapterSectionLink("16.33", "Итоги главы: инструментарий Tkinter", "16-33-itogi-glavy.html", "403"),
        ],
    )
    write("index.html", out)


def build_01() -> None:
    body = f"""
    <p>До сих пор все программы либо выводили текст в терминал (главы 1–5, 8–15), либо рисовали
    на холсте Turtle (главы 6–7, 12). Терминальная программа выполняется <strong>строка за
    строкой</strong>: она делает шаг, ждёт ввода через <code class="inline">input()</code>, делает
    следующий шаг — управление всегда у программы. Оконное приложение устроено иначе: оно строит
    интерфейс один раз, а дальше <strong>ждёт действий пользователя</strong> и реагирует на них в
    произвольном порядке — пользователь может нажать любую кнопку, ввести текст в любое поле,
    изменить размер окна. Это называется <strong>событийно-ориентированным программированием</strong>
    (event-driven programming), и подробно мы разберём эту модель в разделах 16.9–16.10.</p>

    <p>Модуль для оконных приложений называется <code class="inline">tkinter</code> — это интерфейс
    Python к графической библиотеке Tcl/Tk, и, как и <code class="inline">turtle</code>, он входит в
    стандартную поставку Python:</p>
    {flow_diagram([
        ("Ваш код", "объекты и методы Python"),
        ("tkinter", "модуль стандартной библиотеки"),
        ("Tcl/Tk", "GUI-инструментарий"),
        ("Окно ОС", "нативный интерфейс"),
    ], caption="tkinter — мост между Python и системным окружением окон, а не переизобретённый GUI с нуля.")}

    <h2>Проверка: доступен ли Tkinter?</h2>
    <p>Не каждая установка Python обязательно имеет рабочее окружение Tk. Быстрая диагностика:</p>
    {code_block("proverka_tkinter.py", "python -m tkinter\n", lang="text")}
    <p>Если Tkinter и Tk доступны — появится маленькое тестовое окно. Если появляется ошибка
    импорта или окно не открывается — с локальной установкой Python/Tk нужно разобраться отдельно
    (в проверенных инструкциях для вашей ОС), прежде чем продолжать эту главу.</p>

    <h2>Первое окно</h2>
    {code_block(
        "pervoe_okno.py",
        "import tkinter as tk\n\n"
        "root = tk.Tk()\n"
        'root.title("Моё первое приложение")\n\n'
        "root.mainloop()   # запускает цикл обработки событий\n",
    )}
    <p><code class="inline">tk.Tk()</code> создаёт главное окно приложения — примерно как
    <code class="inline">turtle.Screen()</code> создавал холст для рисования. Это прямая связь с
    главой 14: результат <code class="inline">tk.Tk()</code> — обычный Python-объект со своими
    методами.</p>
    {class_diagram(
        "Tk (root)",
        ["— (состояние окна хранится внутри)"],
        ["title(текст)", "geometry(\"ШxВ\")", "minsize(w, h)", "configure(...)", "protocol(...)", "after(...)", "destroy()", "mainloop()"],
        caption="root — экземпляр Tk с собственными методами; это ООП главы 14 в реальной библиотеке.",
    )}

    {callout(
        "info",
        "root — распространённое соглашение об имени",
        "Главное окно принято называть <code class=\"inline\">root</code> («корень») — это не "
        "обязательное правило языка, а широко принятое соглашение, которое вы увидите почти в "
        "любом примере с Tkinter.",
    )}
    {callout(
        "warning",
        "Обычно — один root на приложение",
        "В обычном приложении создаётся <strong>один</strong> объект <code class=\"inline\">Tk()</code> "
        "на весь процесс. Для дополнительных окон (настройки, диалоги) используется "
        "<code class=\"inline\">tk.Toplevel(...)</code> (раздел 16.20), а не второй "
        "<code class=\"inline\">Tk()</code>.",
    )}

    <h2 id="mainloop">mainloop() — не «замирание», а цикл обработки событий</h2>
    <p><code class="inline">root.mainloop()</code> запускает цикл, который активно обрабатывает
    события: клики, ввод текста, изменение размера окна. Программа не «зависает» и не «засыпает» —
    она ждёт и реагирует, оставаясь отзывчивой, пока не будет закрыта. Подробно разберём это
    в разделе 16.10.</p>

    {local_or_practice("16-01", "Практика: создаём первое окно", "", "../../practice/16-01/index.html")}
    """
    page(
        "16-01-nastraivaem-tkinter.html",
        page_title="Tkinter — правильно всё настраиваем!",
        description="Что такое tkinter, проверка доступности Tk, первое окно, root как объект и mainloop() как цикл обработки событий, а не «замирание» программы.",
        kicker_suffix="Настройка Tkinter",
        h1="Tkinter — правильно всё настраиваем!",
        lede="Первое настоящее оконное приложение — и переход от последовательного выполнения к событийной модели.",
        body_html=body,
    )


def build_02() -> None:
    body = f"""
    <h2>Виджет — визуальный объект интерфейса</h2>
    <p><strong>Виджет</strong> (widget) — любой видимый/интерактивный элемент интерфейса: метка,
    кнопка, поле ввода. Как и в главе 14, каждый виджет — экземпляр класса со своими атрибутами и
    методами. <strong>Метка</strong> (<code class="inline">Label</code>) показывает текст,
    <strong>кнопка</strong> (<code class="inline">Button</code>) реагирует на клик.</p>
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
    {image_figure(f"{IMG}/label-button.png", "Окно с меткой «Привет, Tkinter!» и кнопкой «Нажми меня»", f"Результат выполнения кода выше — настоящее окно Tkinter. {PLATFORM_NOTE}", width=300)}
    {callout(
        "warning",
        "Создание виджета — это не то же самое, что его показ",
        "<code class=\"inline\">tk.Button(root, ...)</code> лишь создаёт объект кнопки. Он не "
        "появится в окне, пока вы не разместите его через <strong>менеджер геометрии</strong> "
        "— <code class=\"inline\">.pack()</code> здесь, или <code class=\"inline\">.grid()</code> "
        "(раздел 16.7), или <code class=\"inline\">.place()</code> (раздел 16.15).",
    )}

    <h2>command — функция, а не вызов функции</h2>
    <p>Параметр <code class="inline">command</code> связывает кнопку с функцией — важно
    передать саму функцию, <strong>без скобок</strong>: <code class="inline">command=na_knopku_nazhali</code>,
    а не <code class="inline">command=na_knopku_nazhali()</code>.</p>
    {callout(
        "warning",
        "Частая ошибка: скобки в command",
        "<code class=\"inline\">na_knopku_nazhali</code> — это сама функция как объект (глава 13). "
        "<code class=\"inline\">na_knopku_nazhali()</code> — это <em>вызов</em> функции прямо сейчас. "
        "<code class=\"inline\">command=na_knopku_nazhali()</code> вызовет функцию "
        "<strong>немедленно</strong>, один раз, при создании кнопки — и свяжет кнопку с тем, что "
        "функция <em>вернула</em> (обычно <code class=\"inline\">None</code>), а не с самой "
        "функцией. Клики по кнопке после этого ничего не вызовут.",
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
    <p>Подробнее про <code class="inline">fill</code>/<code class="inline">expand</code> и группировку
    через <code class="inline">Frame</code> — в разделах 16.13–16.14.</p>

    {local_or_practice("16-02", "Практика: Label, Button и pack()", "", "../../practice/16-02/index.html")}
    """
    page(
        "16-02-metki-knopki-pack.html",
        page_title="Метки, кнопки и их размещение",
        description="Виджеты Label и Button в Tkinter, создание отдельно от размещения, обработка нажатий через command и размещение через pack().",
        kicker_suffix="Метки, кнопки, pack",
        h1="Метки, кнопки и их размещение",
        lede="Первые интерактивные виджеты — и то, как Tkinter размещает их в окне.",
        body_html=body,
    )


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
    с которой можно работать, как с любой другой (глава 8). <code class="inline">entry.insert(0, "текст")</code>
    вставляет текст программно, <code class="inline">entry.delete(0, "end")</code> очищает поле.</p>

    <h2 id="tekst">Одна строка текста. Строка за строкой</h2>
    <p><code class="inline">Entry</code> подходит для короткого текста в одну строку — имени,
    числа, пароля. Для многострочного текста используют другой виджет,
    <code class="inline">Text</code>:</p>
    {code_block(
        "mnogostrochnyj_tekst.py",
        "text_box = tk.Text(root, height=5, width=30)\n"
        "text_box.pack()\n\n"
        "def pokazat_tekst():\n"
        '    content = text_box.get("1.0", "end-1c")   # с начала до конца, без завершающего \\n\n'
        "    print(repr(content))\n",
    )}
    {callout(
        "info",
        "Индекс \"1.0\" — не опечатка",
        "У <code class=\"inline\">Text</code> своя система индексов: "
        "<code class=\"inline\">\"1.0\"</code> означает «строка 1, символ 0» — то есть самое "
        "начало текста. Это не связано с числами <code class=\"inline\">float</code> из "
        "главы 4 — просто текстовая метка позиции, и обычная индексация строк Python "
        "(<code class=\"inline\">text[0]</code>) к <code class=\"inline\">Text</code> не применяется.",
    )}
    {callout(
        "warning",
        "\"end\" против \"end-1c\"",
        "<code class=\"inline\">Text</code> всегда добавляет один завершающий символ перевода "
        "строки в конец своего содержимого. <code class=\"inline\">.get(\"1.0\", \"end\")</code> "
        "включает этот лишний <code class=\"inline\">\\n</code>, которого пользователь не "
        "печатал. Если нужен именно видимый пользователем текст без этого технического "
        "довеска — используйте <code class=\"inline\">.get(\"1.0\", \"end-1c\")</code> "
        "(«конец минус один символ»).",
    )}

    {local_or_practice("16-03", "Практика: Entry и Text", "", "../../practice/16-03/index.html")}
    """
    page(
        "16-03-polya-vvoda.html",
        page_title="Множество полей ввода",
        description="Виджеты Entry (однострочный ввод) и Text (многострочный) в Tkinter, и почему Text.get(\"1.0\", \"end\") включает лишний символ перевода строки.",
        kicker_suffix="Поля ввода",
        h1="Множество полей ввода",
        lede="Entry для одной строки, Text — для нескольких: два способа получить текст от пользователя.",
        body_html=body,
    )


def build_04() -> None:
    body = f"""
    <p>Обычные переменные Python не «знают», когда их значение используется в интерфейсе — связь
    с виджетом нужно устанавливать явно, каждый раз заново. Для случаев, когда несколько виджетов
    должны отражать одно и то же значение синхронно, Tkinter предлагает свои специальные
    переменные: <code class="inline">StringVar</code>, <code class="inline">IntVar</code>,
    <code class="inline">BooleanVar</code>, <code class="inline">DoubleVar</code>.</p>
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
    <code class="inline">textvariable</code> (или <code class="inline">variable</code> у
    Radiobutton/Checkbutton), обновляются на экране автоматически.</p>
    {pipeline_diagram([
        {"kind": "object", "title": "imya : StringVar", "rows": ['значение = "Гость"']},
        {"kind": "plain", "title": "label (textvariable=imya)", "note": "связаны через одну переменную"},
    ], caption="Один StringVar может связывать сразу несколько виджетов — все они видят одно значение.")}

    {callout(
        "warning",
        "Tk-переменные не заменяют обычные переменные Python",
        "<code class=\"inline\">StringVar</code> и подобные — специальный инструмент именно для "
        "связи с виджетами, а не universal-замена всех переменных программы. Обычные "
        "<code class=\"inline\">int</code>, <code class=\"inline\">str</code>, "
        "<code class=\"inline\">list</code> по-прежнему отлично подходят для хранения "
        "данных приложения, которые не отображаются напрямую в виджете.",
    )}

    <h2 id="trace">🔬 Чуть глубже: trace_add</h2>
    <p>Можно реагировать на каждое изменение Tk-переменной:</p>
    {code_block(
        "trace_add.py",
        'def pri_izmenenii(*args):\n'
        '    print("Новое значение:", imya.get())\n\n'
        'imya.trace_add("write", pri_izmenenii)\n',
    )}
    <p>Это удобно для «реактивных» интерфейсов, но не обязательно на старте — большинство форм
    прекрасно обходятся обычным чтением значения по кнопке.</p>

    {local_or_practice("16-04", "Практика: StringVar и связанные виджеты", "", "../../practice/16-04/index.html")}
    """
    page(
        "16-04-peremennye-tkinter.html",
        page_title="Переменные Tkinter",
        description="StringVar, IntVar и другие специальные переменные Tkinter для связи данных с виджетами — и почему они не заменяют обычные переменные Python.",
        kicker_suffix="Переменные Tkinter",
        h1="Переменные Tkinter",
        lede="Специальные переменные, которые сами обновляют связанные с ними виджеты на экране.",
        body_html=body,
    )


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
    {callout(
        "info",
        "Группа — это общая переменная",
        "Все переключатели одной группы должны использовать <strong>одну и ту же</strong> "
        "переменную (<code class=\"inline\">variable=vybor</code> у обоих) и <strong>разные</strong> "
        "значения (<code class=\"inline\">value=\"chay\"</code> / <code class=\"inline\">value=\"kofe\"</code>). "
        "Так Tkinter понимает, что это одна группа взаимоисключающих вариантов.",
    )}

    {debug_lab(
        1,
        "У каждого Radiobutton — своя переменная",
        "slomannaya_gruppa.py",
        'chay_var = tk.StringVar()\n'
        'kofe_var = tk.StringVar()\n\n'
        'tk.Radiobutton(root, text="Чай", variable=chay_var, value="chay").pack()\n'
        'tk.Radiobutton(root, text="Кофе", variable=kofe_var, value="kofe").pack()\n',
        ["# Оба переключателя можно выбрать ОДНОВРЕМЕННО —", "# это уже не взаимоисключающий выбор, а два независимых флажка."],
        "У каждой кнопки — своя отдельная переменная, поэтому Tkinter не видит связи между ними: "
        "выбор одной никак не влияет на другую. Групповое поведение переключателей держится "
        "именно на общей переменной, а не на визуальной похожести кнопок.",
        "gruppa_fixed.py",
        'vybor = tk.StringVar(value="chay")\n\n'
        'tk.Radiobutton(root, text="Чай", variable=vybor, value="chay").pack()\n'
        'tk.Radiobutton(root, text="Кофе", variable=vybor, value="kofe").pack()\n',
    )}

    <h2>Checkbutton — независимый выбор</h2>
    {code_block(
        "checkbutton.py",
        'saharok = tk.BooleanVar(value=False)\n'
        'tk.Checkbutton(root, text="С сахаром", variable=saharok).pack()\n\n'
        "def pokazat_flazhok():\n"
        '    print(f"С сахаром: {saharok.get()}")\n',
    )}
    {callout(
        "warning",
        "Checkbutton — не Radiobutton",
        "<code class=\"inline\">Checkbutton</code> — независимое да/нет решение, не связанное "
        "с другими флажками. Не путайте его с группой <code class=\"inline\">Radiobutton</code>, "
        "где выбор одного варианта исключает остальные.",
    )}

    {local_or_practice("16-05", "Практика: Radiobutton и Checkbutton", "", "../../practice/16-05/index.html")}
    """
    page(
        "16-05-mnozhestvo-variantov.html",
        page_title="Множество вариантов!",
        description="Виджеты Radiobutton и Checkbutton в Tkinter — групповой выбор через общую переменную и независимые флажки.",
        kicker_suffix="Множество вариантов",
        h1="Множество вариантов!",
        lede="Переключатели для выбора одного варианта и флажки для независимых да/нет решений.",
        body_html=body,
    )


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
        'fajl_menu.add_command(label="Выход", command=root.destroy)\n'
        'menu_bar.add_cascade(label="Файл", menu=fajl_menu)\n\n'
        "root.config(menu=menu_bar)\n"
        "root.mainloop()\n",
    )}
    {callout(
        "info",
        "tearoff=0",
        "По умолчанию Tkinter добавляет в начало каждого меню пунктирную линию, позволяющую "
        "«оторвать» меню в отдельное окно. <code class=\"inline\">tearoff=0</code> отключает "
        "именно эту возможность отрывать меню — если в вашем интерфейсе она не нужна "
        "(а обычно не нужна), это частый и осознанный выбор, а не универсальное правило "
        "«всегда так делай».",
    )}

    <h2>root.quit() против root.destroy()</h2>
    {comparison_table(
        ["Метод", "Что делает"],
        [
            ["<code class=\"inline\">root.quit()</code>", "останавливает текущий mainloop() — но само окно и виджеты остаются существовать"],
            ["<code class=\"inline\">root.destroy()</code>", "уничтожает окно и всё дерево виджетов целиком, также останавливая mainloop()"],
        ],
    )}
    {callout(
        "warning",
        "Это не взаимозаменяемые синонимы",
        "Для обычного пункта меню «Выход» в этом курсе понятнее и надёжнее "
        "<code class=\"inline\">root.destroy</code> — он завершает работу приложения "
        "полностью. <code class=\"inline\">root.quit()</code> уместен в более специфичных "
        "сценариях, где само окно должно пережить остановку цикла событий.",
    )}

    <h2>Акселераторы — это надпись, не привязка клавиш</h2>
    {code_block("accelerator.py", 'fajl_menu.add_command(label="Сохранить", accelerator="Ctrl+S", command=sohranit)\n')}
    {callout(
        "warning",
        "accelerator сам по себе не создаёт горячую клавишу",
        "<code class=\"inline\">accelerator=\"Ctrl+S\"</code> лишь выводит текст подсказки "
        "рядом с пунктом меню. Он <strong>не</strong> связывает автоматически комбинацию "
        "клавиш с командой — для этого нужен отдельный механизм привязки событий "
        "(<code class=\"inline\">.bind(...)</code>), который подробно разберём в главе 17.",
    )}

    {local_or_practice("16-06", "Практика: строим меню приложения", "", "../../practice/16-06/index.html")}
    """
    page(
        "16-06-menu.html",
        page_title="Меню",
        description="Строим меню приложения в Tkinter: Menu, add_command, add_cascade, точная разница между root.quit() и root.destroy(), и что на самом деле делает accelerator.",
        kicker_suffix="Меню",
        h1="Меню",
        lede="Настоящее приложение почти всегда начинается с меню в верхней части окна.",
        body_html=body,
    )


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
    {comparison_table(
        ["Позиция", "0", "1"],
        [
            ["row=0", "Label «Имя:»", "Entry"],
            ["row=1", "Label «Email:»", "Entry"],
            ["row=2", "Button (columnspan=2 — занимает обе колонки)", ""],
        ],
    )}
    {callout(
        "warning",
        "Не смешивайте pack() и grid() в одном контейнере",
        "Виджеты внутри одного и того же родительского окна (или фрейма) должны использовать "
        "либо только <code class=\"inline\">pack()</code>, либо только "
        "<code class=\"inline\">grid()</code> — смешение вызывает ошибку. Разные контейнеры "
        "(например, вложенные <code class=\"inline\">Frame</code>, раздел 16.13) могут "
        "использовать разные способы размещения независимо друг от друга — подробная схема "
        "«хорошо/плохо» будет в разделе 16.15.",
    )}
    <p>О том, как сделать такую форму отзывчивой к изменению размера окна — в разделе 16.15
    «Адаптивный grid».</p>

    {local_or_practice("16-07", "Практика: компоновка через grid()", "", "../../practice/16-07/index.html")}
    """
    page(
        "16-07-grid.html",
        page_title="Идеальная компоновка — grid",
        description="Метод grid() в Tkinter — размещение виджетов по строкам и столбцам, и почему pack() и grid() нельзя смешивать в одном контейнере.",
        kicker_suffix="Компоновка grid",
        h1="Идеальная компоновка — grid",
        lede="Для форм с несколькими колонками grid() удобнее, чем pack().",
        body_html=body,
    )


def build_08() -> None:
    body = f"""
    <p>Соберём всё изученное в главе в одном настоящем приложении: калькулятор чаевых с полем
    ввода, кнопкой и меткой результата. Это <strong>фундамент</strong> — в разделе 16.31 мы
    вернёмся к нему и превратим в полноценное «Tip Calculator Pro» с классом приложения,
    валидацией и сохранением настроек.</p>
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
        "<code class=\"inline\">grid()</code> — раздел 16.7; <code class=\"inline\">float()</code> "
        "— глава 4; форматирование <code class=\"inline\">:.2f</code> — глава 8; сама формула "
        "чаевых — глава 12, проект 12-2.",
    )}
    {exercise(3, "Проверка ввода", "Оберните вычисление в try/except (забегая немного вперёд — подробно об этом в главе 21) — чтобы приложение не падало, если пользователь введёт не число, а текст. В разделе 16.23 мы разберём это системно.")}

    {local_or_practice("16-08", "Практика: калькулятор чаевых", "", "../../practice/16-08/index.html")}
    """
    page(
        "16-08-mini-proekt-chaevye-itogi.html",
        page_title="Мини-проект — калькулятор чаевых",
        description="Мини-проект главы 16 (фундамент): настоящее приложение-калькулятор чаевых на Tkinter с grid(), полями ввода и вычислением.",
        kicker_suffix="Калькулятор чаевых",
        h1="Мини-проект — калькулятор чаевых",
        lede="Первое полноценное приложение книги — с полями ввода, кнопкой и результатом на экране.",
        body_html=body,
    )


def build_09() -> None:
    body = f"""
    <h2>Терминал: последовательное выполнение</h2>
    <p>Терминальная программа выполняется предсказуемо, строка за строкой — управление всегда у
    самой программы:</p>
    {flow_diagram([
        ("Шаг 1", "print(...)"),
        ("Шаг 2", "input(...)"),
        ("Шаг 3", "следующая строка"),
    ], caption="Терминал: программа сама решает, когда и что делать дальше.")}

    <h2>GUI: событийно-ориентированное выполнение</h2>
    <p>Оконное приложение строит интерфейс один раз, а затем <strong>ждёт события</strong> —
    и на каждое реагирует отдельным, заранее зарегистрированным кусочком кода:</p>
    {pipeline_diagram([
        {"kind": "plain", "title": "инициализация интерфейса"},
        {"kind": "plain", "title": "mainloop()", "note": "переход в цикл событий"},
        {"kind": "object", "title": "событие: клик", "note": "пользователь нажал кнопку"},
        {"kind": "plain", "title": "callback выполняется", "note": "вызывается связанная функция"},
        {"kind": "plain", "title": "снова ожидание", "note": "callback вернулся"},
    ], caption="Управление не остаётся у одной сплошной последовательности кода — оно переходит между обработчиками.")}

    <h2>Источники событий</h2>
    {capability_map([
        ("Пользователь", ["клик мышью", "ввод текста", "действие с окном"]),
        ("Система", ["перерисовка", "изменение размера окна"]),
        ("Программа", ["таймер / after() — раздел 16.22"]),
    ], title="Откуда берутся события")}

    <h2>Событие, callback, command — не синонимы</h2>
    {comparison_table(
        ["Термин", "Что это"],
        [
            ["Событие (event)", "то, что произошло — клик, ввод, таймер"],
            ["Callback", "функция/вызываемый объект, зарегистрированный заранее для вызова позже"],
            ["command", "один из способов Tkinter связать callback с конкретным виджетом"],
        ],
    )}
    <p>Регистрация callback — это ещё не его выполнение:</p>
    {code_block(
        "registraciya_vs_vypolnenie.py",
        'log = []\n\n'
        'def on_click():\n'
        '    log.append("clicked")\n\n'
        'registered = on_click   # регистрация: callback запомнен, но НЕ вызван\n'
        'print(log)              # []\n\n'
        'registered()            # диспетчеризация: callback выполняется именно сейчас\n'
        'print(log)              # [\'clicked\']\n',
    )}
    {callout(
        "info",
        "Это прямая связь с главой 13",
        "Функция как объект, который можно передать и вызвать позже — ровно то же самое "
        "«функция без скобок», о котором шла речь в разделе 16.2 про <code "
        "class=\"inline\">command</code>. Событийная модель Tkinter целиком построена на этой "
        "идее.",
    )}

    {practice_card("16-09", "Практика: регистрация и диспетчеризация callback", "Проверяется без tkinter — чистой логикой на функциях-объектах", "../../practice/16-09/index.html")}
    """
    page(
        "16-09-ot-terminala-k-gui.html",
        page_title="От терминала к GUI: событийная модель",
        description="Последовательное выполнение терминальной программы против событийно-ориентированной модели GUI: источники событий, и точное различие между событием, callback и command.",
        kicker_suffix="От терминала к GUI",
        h1="От терминала к GUI: событийная модель",
        lede="Главный интеллектуальный переход этой главы: управление больше не течёт одной сплошной линией.",
        body_html=body,
    )


def build_10() -> None:
    body = f"""
    <h2>Событийный цикл — не Python while True</h2>
    {callout(
        "warning",
        "Что на самом деле происходит внутри mainloop()",
        "Не думайте о <code class=\"inline\">mainloop()</code> как о вашем собственном "
        "<code class=\"inline\">while True: ...</code> — это внутренний цикл обработки событий "
        "Tcl/Tk. Модель ниже — концептуальная, для понимания порядка событий, а не описание "
        "реальной реализации.",
    )}
    {pipeline_diagram([
        {"kind": "plain", "title": "инициализация UI"},
        {"kind": "plain", "title": "mainloop()"},
        {"kind": "object", "title": "ожидание / обработка событий"},
        {"kind": "plain", "title": "событие?", "note": "да"},
        {"kind": "plain", "title": "callback", "note": "вызов обработчика"},
        {"kind": "plain", "title": "callback вернулся", "note": "return"},
        {"kind": "plain", "title": "следующее событие", "note": "↺ назад к ожиданию"},
    ], caption="Событийный цикл: инициализация → mainloop → ожидание → диспетчеризация → снова ожидание.")}

    <h2>Порядок событий — предсказуемый, но не последовательный в коде</h2>
    {code_block(
        "sobytijnyj_cikl.py",
        'log = []\n\n'
        'def on_click(): log.append("click")\n'
        'def on_timer(): log.append("timer")\n'
        'def on_type(): log.append("type")\n\n'
        'handlers = {"click": on_click, "timer": on_timer, "type": on_type}\n\n'
        'def run_event_loop(queue):\n'
        "    for event in queue:\n"
        "        handlers[event]()\n\n"
        'run_event_loop(["click", "timer", "type"])\n'
        "print(log)   # [\'click\', \'timer\', \'type\']\n",
    )}
    <p>Реальные события Tkinter приходят по мере действий пользователя и системы — но идея та
    же: очередь событий обрабатывается по одному, и каждое запускает свой callback.</p>

    {callout(
        "info",
        "Долгий callback — это уже отдельная тема",
        "Пока обработчик выполняется, событийный цикл ждёт его завершения, прежде чем перейти "
        "к следующему событию. Что происходит, если callback работает слишком долго — подробно "
        "в разделах 16.22 и 16.24.",
    )}

    {practice_card("16-10", "Практика: порядок обработки событий", "Проверяется без tkinter — моделируем очередь событий на чистом Python", "../../practice/16-10/index.html")}
    """
    page(
        "16-10-event-loop-i-mainloop.html",
        page_title="Как работает событийный цикл и mainloop",
        description="Концептуальная модель событийного цикла Tkinter: инициализация, mainloop, ожидание событий, диспетчеризация callback — и почему это не обычный Python while True.",
        kicker_suffix="Событийный цикл",
        h1="Как работает событийный цикл и mainloop",
        lede="mainloop() — не чёрный ящик и не «замирание»: это цикл, который активно ждёт и обрабатывает события.",
        body_html=body,
    )


def build_11() -> None:
    body = f"""
    <h2>У каждого виджета есть родитель</h2>
    <p>Виджеты образуют дерево: у каждого, кроме самого корня, есть родитель (master), который
    определяет контекст размещения и жизненного цикла:</p>
    {tree_diagram(
        ("root", [
            ("menu_bar", []),
            ("main_frame", [
                ("title_label", []),
                ("name_entry", []),
                ("save_button", []),
            ]),
        ]),
        caption="Типичное дерево небольшого приложения: root → main_frame → отдельные виджеты формы.",
    )}
    {code_block(
        "derevo_widgetov.py",
        "import tkinter as tk\n\n"
        "root = tk.Tk()\n"
        "main_frame = tk.Frame(root)\n"
        "main_frame.pack()\n\n"
        'title_label = tk.Label(main_frame, text="Форма")\n'
        "title_label.pack()\n"
        "name_entry = tk.Entry(main_frame)\n"
        "name_entry.pack()\n",
    )}
    <p>Первый аргумент почти любого виджета — его родитель (<code class="inline">main_frame</code>
    выше). Родитель определяет, в каком контейнере разместится виджет — подробно про
    <code class="inline">Frame</code> в разделе 16.13.</p>

    <h2>Жизненный цикл виджета</h2>
    {pipeline_diagram([
        {"kind": "plain", "title": "создан", "note": "Button(...)"},
        {"kind": "plain", "title": "настроен", "note": "configure(...)"},
        {"kind": "plain", "title": "размещён", "note": ".pack() / .grid() / .place()"},
        {"kind": "plain", "title": "интерактивен"},
        {"kind": "plain", "title": "уничтожен", "note": ".destroy()"},
    ], caption="Создание виджета — только первый шаг; интерактивным он становится после размещения.")}
    {callout(
        "info",
        "destroy() — не единственный способ скрыть виджет",
        "<code class=\"inline\">.destroy()</code> уничтожает виджет безвозвратно. Если нужно "
        "лишь временно убрать виджет с экрана, есть более лёгкие варианты (например, "
        "<code class=\"inline\">.grid_remove()</code>) — но для большинства первых приложений "
        "деструктивное удаление ненужных виджетов и есть правильный выбор.",
    )}

    {practice_card("16-11", "Практика: дерево виджетов как данные", "Проверяется без tkinter — моделируем дерево вложенными данными Python", "../../practice/16-11/index.html")}
    """
    page(
        "16-11-derevo-widgetov.html",
        page_title="Виджет и дерево интерфейса",
        description="Каждый виджет имеет родителя; вместе они образуют дерево. Жизненный цикл виджета: создан → настроен → размещён → интерактивен → уничтожен.",
        kicker_suffix="Дерево виджетов",
        h1="Виджет и дерево интерфейса",
        lede="Интерфейс — не плоский список элементов, а дерево вложенных контейнеров.",
        body_html=body,
    )


def build_12() -> None:
    body = f"""
    <h2>tk и ttk — два набора виджетов</h2>
    {comparison_table(
        ["", "tk", "ttk"],
        [
            ["Что это", "классические виджеты Tkinter", "тематизированный (themed) набор поверх Tk"],
            ["Импорт", "<code class=\"inline\">import tkinter as tk</code>", "<code class=\"inline\">from tkinter import ttk</code>"],
            ["Внешний вид", "фиксированный классический стиль", "может адаптироваться под тему/платформу"],
            ["Стилизация", "<code class=\"inline\">fg=</code>/<code class=\"inline\">bg=</code>", "через <code class=\"inline\">ttk.Style()</code>"],
        ],
    )}
    {code_block(
        "tk_vs_ttk.py",
        "import tkinter as tk\n"
        "from tkinter import ttk\n\n"
        "root = tk.Tk()\n\n"
        'ttk.Label(root, text="Современный ttk.Label").pack()\n'
        'ttk.Button(root, text="ttk.Button").pack()\n'
        'ttk.Entry(root).pack()\n',
    )}
    {callout(
        "tip",
        "Для нового кода — ttk, где есть аналог",
        "Начиная с этой главы курс использует <code class=\"inline\">ttk.Label</code>, "
        "<code class=\"inline\">ttk.Button</code>, <code class=\"inline\">ttk.Entry</code> и "
        "другие тематизированные виджеты, где они существуют. Но ttk <strong>не заменяет</strong> "
        "весь Tk целиком — виджеты вроде <code class=\"inline\">tk.Text</code>, "
        "<code class=\"inline\">tk.Canvas</code> и <code class=\"inline\">tk.Menu</code> "
        "остаются классическими, потому что у них нет тематизированного аналога.",
    )}
    {callout(
        "warning",
        "Не используйте fg/bg на ttk-виджетах как на классических",
        "Классические <code class=\"inline\">tk</code>-виджеты понимают "
        "<code class=\"inline\">fg=</code>/<code class=\"inline\">bg=</code> напрямую. Виджеты "
        "<code class=\"inline\">ttk</code> стилизуются иначе — через объект "
        "<code class=\"inline\">ttk.Style()</code> (раздел 16.25). Не переносите привычки "
        "классического Tk на ttk буквально.",
    )}

    <h2>from tkinter import * — не в продакшн-стиле</h2>
    {classic_vs_modern(
        "Импорт: звёздочка → явные имена",
        "Не рекомендуется",
        'from tkinter import *\n\n'
        "root = Tk()\n"
        'Button(root, text="Кнопка")   # откуда взялся Button — неочевидно',
        "Рекомендуется",
        "import tkinter as tk\n"
        "from tkinter import ttk\n\n"
        "root = tk.Tk()\n"
        'ttk.Button(root, text="Кнопка")   # источник имени виден сразу',
        "<code class=\"inline\">from tkinter import *</code> работает, но затрудняет чтение "
        "кода: непонятно, какому модулю принадлежит каждое имя, и легко случайно "
        "перекрыть встроенные имена Python. В примерах курса, начиная с этой главы, — "
        "только явные импорты.",
    )}

    {local_or_practice("16-12", "Практика: собираем форму из tk и ttk", "", "../../practice/16-12/index.html")}
    """
    page(
        "16-12-tk-i-ttk.html",
        page_title="tk и ttk: классические и тематизированные виджеты",
        description="Различие между классическими виджетами tk и тематизированным набором ttk, стилизация через ttk.Style() вместо fg/bg, и почему from tkinter import * не подходит для продакшн-стиля.",
        kicker_suffix="tk и ttk",
        h1="tk и ttk: классические и тематизированные виджеты",
        lede="Начиная с этой главы курс переходит на ttk там, где у виджета есть тематизированный аналог.",
        body_html=body,
    )


def build_13() -> None:
    body = f"""
    <h2>Frame — структура прежде компоновки</h2>
    <p><code class="inline">ttk.Frame</code> — контейнер без собственного видимого содержимого,
    который группирует связанные виджеты в осмысленные регионы:</p>
    {tree_diagram(
        ("root", [
            ("toolbar_frame", []),
            ("content_frame", []),
            ("status_frame", []),
        ]),
        caption="Разбиение окна на именованные регионы упрощает и код, и мышление о layout.",
    )}
    {code_block(
        "frame.py",
        "import tkinter as tk\n"
        "from tkinter import ttk\n\n"
        "root = tk.Tk()\n\n"
        "toolbar_frame = ttk.Frame(root)\n"
        "content_frame = ttk.Frame(root)\n"
        "status_frame = ttk.Frame(root)\n\n"
        'toolbar_frame.pack(side="top", fill="x")\n'
        'content_frame.pack(side="top", fill="both", expand=True)\n'
        'status_frame.pack(side="bottom", fill="x")\n',
    )}
    <p>Внутри каждого фрейма можно независимо использовать <code class="inline">pack()</code>
    или <code class="inline">grid()</code> — правило «не смешивать» действует в пределах одного
    родителя, а не всего окна (подробная схема — в разделе 16.15).</p>

    <h2>LabelFrame — визуально подписанная группа</h2>
    {code_block(
        "labelframe.py",
        'nastrojki = ttk.LabelFrame(root, text="Настройки")\n'
        "nastrojki.pack(padx=10, pady=10, fill=\"x\")\n\n"
        'ttk.Checkbutton(nastrojki, text="Тёмная тема").pack(anchor="w")\n',
    )}
    {callout(
        "tip",
        "LabelFrame — не для каждой мелочи",
        "Используйте <code class=\"inline\">LabelFrame</code> для действительно связанной "
        "группы настроек, а не для каждого отдельного виджета — иначе интерфейс превращается "
        "в лестницу рамочек.",
    )}

    {local_or_practice("16-13", "Практика: организуем интерфейс через Frame", "", "../../practice/16-13/index.html")}
    """
    page(
        "16-13-frame-i-labelframe.html",
        page_title="Frame и LabelFrame: организуем интерфейс",
        description="ttk.Frame группирует виджеты в осмысленные регионы окна; ttk.LabelFrame добавляет визуальную подпись для группы настроек.",
        kicker_suffix="Frame и LabelFrame",
        h1="Frame и LabelFrame: организуем интерфейс",
        lede="Прежде чем размещать десятки виджетов, разбейте окно на понятные регионы.",
        body_html=body,
    )


def build_14() -> None:
    body = f"""
    <h2>pack: как распределяется пространство</h2>
    <p><code class="inline">side</code> определяет, с какой стороны укладывается очередной
    виджет, <code class="inline">fill</code> — растягивать ли его на всю доступную ширину/высоту,
    а <code class="inline">expand</code> — забирать ли ему лишнее свободное место:</p>
    {comparison_table(
        ["Параметр", "Значение", "Эффект"],
        [
            ["fill", "\"x\"", "растянуть виджет по ширине выделенной ему полосы"],
            ["fill", "\"y\"", "растянуть виджет по высоте выделенной ему полосы"],
            ["fill", "\"both\"", "растянуть и по ширине, и по высоте"],
            ["expand", "True", "отдать виджету дополнительное свободное место контейнера"],
        ],
    )}
    {code_block(
        "pack_fill_expand.py",
        'ttk.Label(root, text="Верх", background="#E7DEFF").pack(side="top", fill="x")\n'
        'ttk.Label(root, text="Центр", background="#B9A0FC").pack(side="top", fill="both", expand=True)\n'
        'ttk.Label(root, text="Низ", background="#E7DEFF").pack(side="bottom", fill="x")\n',
    )}
    {callout(
        "info",
        "Внешний отступ и внутренний — не одно и то же",
        "<code class=\"inline\">padx</code>/<code class=\"inline\">pady</code> у "
        "<code class=\"inline\">.pack(...)</code> — это отступ <strong>снаружи</strong> виджета, "
        "между ним и соседями. Отступ <strong>внутри</strong> самого виджета (между его "
        "рамкой и содержимым) настраивается отдельно — например, через "
        "<code class=\"inline\">padding=</code> у <code class=\"inline\">ttk.Frame</code>.",
    )}

    <h2>Вложенные фреймы + pack</h2>
    {code_block(
        "vlozhennye_frejmy.py",
        "forma_frame = ttk.Frame(root, padding=10)\n"
        "forma_frame.pack(fill=\"x\")\n\n"
        'ttk.Label(forma_frame, text="Имя:").pack(side="left")\n'
        "ttk.Entry(forma_frame).pack(side=\"left\", fill=\"x\", expand=True)\n",
    )}
    <p>Метка прижата слева, а поле ввода забирает всё оставшееся горизонтальное пространство
    — типичная комбинация <code class="inline">side="left"</code> + <code class="inline">fill="x"</code>
    + <code class="inline">expand=True</code> для формы «подпись — растягивающееся поле».</p>

    {local_or_practice("16-14", "Практика: pack с fill и expand", "", "../../practice/16-14/index.html")}
    """
    page(
        "16-14-pack-podrobno.html",
        page_title="pack подробно: fill, expand и вложенные фреймы",
        description="Как pack() распределяет пространство: side, fill, expand, разница между внешним и внутренним отступом, и типичная комбинация для формы «подпись — растягивающееся поле».",
        kicker_suffix="pack подробно",
        h1="pack подробно: fill, expand и вложенные фреймы",
        lede="pack — это не просто «сверху вниз»: у него есть управление свободным пространством.",
        body_html=body,
    )


def build_15() -> None:
    body = f"""
    <h2>Адаптивный grid: кто получает лишнее место</h2>
    <p>По умолчанию строки и столбцы <code class="inline">grid()</code> не растут при увеличении
    окна. Чтобы форма подстраивалась под размер окна, столбцам/строкам нужно явно назначить
    <strong>вес</strong>:</p>
    {code_block(
        "adaptivny_grid.py",
        "root.columnconfigure(1, weight=1)   # растягивается именно колонка 1 (с полями ввода)\n"
        "root.rowconfigure(0, weight=1)\n\n"
        'ttk.Label(root, text="Имя:").grid(row=0, column=0, sticky="w")\n'
        'ttk.Entry(root).grid(row=0, column=1, sticky="ew")   # растягивается по ширине ячейки\n',
    )}
    {code_block(
        "raspredelenie_vesa.py",
        'def raspredelit_prostranstvo(weights, extra_space):\n'
        "    total = sum(weights)\n"
        "    if total == 0:\n"
        "        return [0] * len(weights)\n"
        "    return [extra_space * w / total for w in weights]\n\n"
        'print(raspredelit_prostranstvo([1, 2], 300))   # [100.0, 200.0]\n',
    )}
    {callout(
        "info",
        "weight — это пропорция, не пиксели",
        "Вес определяет <strong>долю</strong> дополнительного пространства, а не абсолютный "
        "размер. Колонка с весом 2 получит вдвое больше лишнего места, чем колонка с весом 1 "
        "— но обе продолжат вмещать свой обычный минимальный контент.",
    )}

    <h2>sticky — к какому краю ячейки прилипает виджет</h2>
    {comparison_table(
        ["sticky", "Эффект"],
        [
            ["\"w\" / \"e\" / \"n\" / \"s\"", "прилипает к одному краю ячейки (запад/восток/север/юг)"],
            ["\"ew\"", "растягивается по ширине ячейки"],
            ["\"nsew\"", "растягивается по всей ячейке — и по ширине, и по высоте"],
        ],
    )}

    <h2>Правило одного родителя</h2>
    {two_up(
        f'<div style="padding:16px;border:2px solid #059669;border-radius:14px">'
        f'<div style="font-weight:700;color:#059669;margin-bottom:8px">✓ Верно</div>'
        + tree_diagram(("root (pack)", [("frame (grid внутри)", [("label", []), ("entry", [])])]))
        + '</div>',
        f'<div style="padding:16px;border:2px solid #DB2777;border-radius:14px">'
        f'<div style="font-weight:700;color:#DB2777;margin-bottom:8px">✗ Ошибка</div>'
        + tree_diagram(("root", [("widget_a (.pack())", []), ("widget_b (.grid())", [])]))
        + '</div>',
    )}
    <p>Смешивать <code class="inline">pack()</code> и <code class="inline">grid()</code> нельзя
    у виджетов с <strong>одним и тем же</strong> родителем — но разные контейнеры (root
    использует <code class="inline">pack()</code>, а вложенный <code class="inline">Frame</code>
    внутри — <code class="inline">grid()</code>) полностью независимы друг от друга.</p>

    <h2>place() — точное позиционирование</h2>
    {code_block("place.py", 'label.place(x=20, y=10)\nlabel2.place(relx=0.5, rely=0.5, anchor="center")   # центр контейнера\n')}
    {callout(
        "warning",
        "place() — не первый выбор для обычных форм",
        "<code class=\"inline\">place()</code> удобен для точных наложений и особых случаев, "
        "но не подстраивается под размер окна автоматически, как <code class=\"inline\">grid()</code> "
        "с весами. Для обычных адаптивных форм — <code class=\"inline\">grid()</code>.",
    )}

    <h2>Как выбрать менеджер геометрии</h2>
    {decision_map(
        [
            ("Простое вертикальное расположение / регионы", "pack()"),
            ("Форма/таблица/адаптивные колонки", "grid()"),
            ("Точное или особое позиционирование, наложения", "place() — осознанно"),
            ("Сложный экран", "Frame + разные менеджеры в разных родителях"),
        ],
        title="pack vs grid vs place",
    )}

    {practice_card("16-15", "Практика: распределение веса в адаптивном grid", "Проверяется без tkinter — чистая арифметика распределения пространства", "../../practice/16-15/index.html")}
    """
    page(
        "16-15-adaptivny-grid.html",
        page_title="Адаптивный grid: sticky и weight",
        description="rowconfigure/columnconfigure с weight, sticky, правило одного родителя для pack/grid и итоговая карта решений pack/grid/place.",
        kicker_suffix="Адаптивный grid",
        h1="Адаптивный grid: sticky и weight",
        lede="Форма не обязана оставаться одного размера навсегда — grid умеет подстраиваться.",
        body_html=body,
    )


def build_16() -> None:
    body = f"""
    <h2>Combobox — выбор из списка</h2>
    {code_block(
        "combobox.py",
        'variant = ttk.Combobox(root, values=["Маленький", "Средний", "Большой"], state="readonly")\n'
        "variant.current(0)\n"
        "variant.pack()\n",
    )}
    {callout(
        "tip",
        "state=\"readonly\"",
        "Без <code class=\"inline\">state=\"readonly\"</code> пользователь сможет напечатать в "
        "поле произвольный текст, не входящий в список. Если нужен выбор именно из "
        "предложенных вариантов — используйте <code class=\"inline\">\"readonly\"</code>.",
    )}

    <h2>Listbox — список для выбора одного/нескольких элементов</h2>
    {code_block(
        "listbox.py",
        "spisok = tk.Listbox(root)\n"
        'spisok.insert("end", "Молоко")\n'
        'spisok.insert("end", "Хлеб")\n'
        'spisok.insert("end", "Яблоки")\n'
        "spisok.pack()\n\n"
        "def pokazat_vybor():\n"
        "    indeksy = spisok.curselection()\n"
        '    print([spisok.get(i) for i in indeksy])\n',
    )}

    <h2>Spinbox — ограниченный числовой выбор</h2>
    {code_block("spinbox.py", "kolichestvo = ttk.Spinbox(root, from_=1, to=10)\nkolichestvo.pack()\n")}
    {callout(
        "info",
        "Spinbox vs Entry",
        "<code class=\"inline\">Spinbox</code> удобен, когда значение — число в известном "
        "диапазоне (количество товара, возраст). Для произвольного текста подходит обычный "
        "<code class=\"inline\">Entry</code>.",
    )}

    <h2>Scale — значение из диапазона</h2>
    {code_block("scale.py", 'gromkost = ttk.Scale(root, from_=0, to=100, orient="horizontal")\ngromkost.set(50)\ngromkost.pack()\n')}
    {callout(
        "warning",
        "Scale возвращает float",
        "<code class=\"inline\">.get()</code> у <code class=\"inline\">Scale</code> возвращает "
        "число с плавающей точкой, даже если визуально ползунок стоит на целом делении — "
        "округляйте явно (<code class=\"inline\">round(...)</code>), если нужно целое число.",
    )}

    {local_or_practice("16-16", "Практика: Combobox, Listbox, Spinbox, Scale", "", "../../practice/16-16/index.html")}
    """
    page(
        "16-16-widgety-vybora.html",
        page_title="Виджеты выбора: Combobox, Listbox, Spinbox, Scale",
        description="Combobox для выбора из списка, Listbox для списка с curselection, Spinbox для ограниченного числового выбора и Scale для значения из диапазона.",
        kicker_suffix="Виджеты выбора",
        h1="Виджеты выбора: Combobox, Listbox, Spinbox, Scale",
        lede="Каждый из этих виджетов решает свой вариант одной задачи: выбрать значение из ограниченного множества.",
        body_html=body,
    )


def build_17() -> None:
    body = f"""
    <h2>Progressbar — прогресс, а не украшение</h2>
    {code_block(
        "progressbar.py",
        'progress = ttk.Progressbar(root, mode="determinate", maximum=100, value=0)\n'
        "progress.pack(fill=\"x\")\n\n"
        "def obnovit_progress(procent):\n"
        "    progress[\"value\"] = procent\n",
    )}
    {comparison_table(
        ["Режим", "Когда использовать"],
        [
            ["determinate", "известно точное количество этапов/процент выполнения"],
            ["indeterminate", "работа идёт, но её объём заранее не известен"],
        ],
    )}
    {callout(
        "warning",
        "Не подделывайте прогресс, которого не знаете",
        "Если приложение реально не может оценить процент выполнения — используйте "
        "<code class=\"inline\">mode=\"indeterminate\"</code> (бегущая полоса), а не "
        "произвольные числа в <code class=\"inline\">determinate</code>. Ложный прогресс хуже "
        "честного «неизвестно, сколько осталось».",
    )}

    <h2>Notebook — вкладки</h2>
    {code_block(
        "notebook.py",
        "vkladki = ttk.Notebook(root)\n"
        "vkladki.pack(fill=\"both\", expand=True)\n\n"
        "obshaya_vkladka = ttk.Frame(vkladki)\n"
        "vneshnij_vid_vkladka = ttk.Frame(vkladki)\n\n"
        'vkladki.add(obshaya_vkladka, text="Общие")\n'
        'vkladki.add(vneshnij_vid_vkladka, text="Внешний вид")\n',
    )}
    <p>Каждая вкладка — обычный <code class="inline">Frame</code>, внутри которого можно
    независимо использовать <code class="inline">pack()</code> или <code class="inline">grid()</code>
    — прекрасно подходит для окна настроек (раздел 16.25).</p>

    {local_or_practice("16-17", "Практика: Progressbar и Notebook", "", "../../practice/16-17/index.html")}
    """
    page(
        "16-17-progressbar-i-notebook.html",
        page_title="Progressbar и вкладки Notebook",
        description="ttk.Progressbar в режимах determinate/indeterminate и ttk.Notebook для вкладок — каждая вкладка как обычный Frame.",
        kicker_suffix="Progressbar и Notebook",
        h1="Progressbar и вкладки Notebook",
        lede="Прогресс должен быть честным, а вкладки — естественным способом уместить много настроек.",
        body_html=body,
    )


def build_18() -> None:
    body = f"""
    <h2>messagebox — стандартные диалоги уведомлений</h2>
    {code_block(
        "messagebox.py",
        "from tkinter import messagebox\n\n"
        'messagebox.showinfo("Готово", "Файл сохранён.")\n'
        'messagebox.showwarning("Внимание", "Поле пустое.")\n'
        'messagebox.showerror("Ошибка", "Не удалось прочитать файл.")\n',
    )}

    <h2>Диалоги с выбором — читайте возвращаемое значение</h2>
    {code_block(
        "messagebox_yesno.py",
        'otvet = messagebox.askyesno("Выход", "Сохранить изменения перед выходом?")\n'
        "if otvet:\n"
        "    sohranit()\n"
        "else:\n"
        "    root.destroy()\n",
    )}
    {callout(
        "warning",
        "Не угадывайте результат по названию кнопки",
        "Не предполагайте заранее, что вернёт диалог — читайте фактическое возвращаемое "
        "значение (<code class=\"inline\">True</code>/<code class=\"inline\">False</code> для "
        "<code class=\"inline\">askyesno</code>) и реагируйте на него, а не на предположение "
        "«пользователь наверняка нажмёт да».",
    )}
    {callout(
        "info",
        "Модальность",
        "Стандартные диалоги <code class=\"inline\">messagebox</code> — модальные: они "
        "блокируют взаимодействие с остальным приложением, пока не будут закрыты. Для "
        "собственных модальных окон есть более тонкие инструменты "
        "(<code class=\"inline\">transient</code>, <code class=\"inline\">grab_set</code>) — "
        "раздел 16.20, помечены как продвинутые.",
    )}

    {local_or_practice("16-18", "Практика: messagebox и диалоги выбора", "", "../../practice/16-18/index.html")}
    """
    page(
        "16-18-messagebox-i-dialogi.html",
        page_title="Messagebox и диалоги",
        description="Стандартные диалоги showinfo/showwarning/showerror и askyesno — модальность и необходимость реагировать на фактически возвращённое значение, а не предполагаемое.",
        kicker_suffix="Messagebox и диалоги",
        h1="Messagebox и диалоги",
        lede="Пользователь должен узнавать об успехе, предупреждении или ошибке — не из терминала.",
        body_html=body,
    )


def build_19() -> None:
    body = f"""
    <p>Прямая связь с главой 15: диалог выбора файла отдаёт путь, а дальше работает всё то же
    <code class="inline">pathlib</code>.</p>
    {code_block(
        "filedialog.py",
        "from tkinter import filedialog\n"
        "from pathlib import Path\n\n"
        'filename = filedialog.askopenfilename(filetypes=[("Текстовые файлы", "*.txt")])\n'
        "if not filename:\n"
        "    pass   # пользователь нажал «Отмена» — ничего не делаем\n"
        "else:\n"
        "    text = Path(filename).read_text(encoding=\"utf-8\")\n",
    )}
    {callout(
        "warning",
        "⚠️ Не забывайте про отмену",
        "Если пользователь закрыл диалог без выбора файла, "
        "<code class=\"inline\">askopenfilename()</code> вернёт <strong>пустую строку</strong>, "
        "а не <code class=\"inline\">None</code> и не путь. Попытка сразу открыть "
        "<code class=\"inline\">Path(\"\")</code> — частая ошибка. Всегда проверяйте результат "
        "перед использованием: <code class=\"inline\">if not filename: return</code>.",
    )}

    <h2>Сохранение файла</h2>
    {code_block(
        "filedialog_save.py",
        'filename = filedialog.asksaveasfilename(defaultextension=".txt")\n'
        "if filename:\n"
        '    Path(filename).write_text(text_widget.get("1.0", "end-1c"), encoding="utf-8")\n',
    )}

    {pipeline_diagram([
        {"kind": "plain", "title": "нажали «Открыть»"},
        {"kind": "plain", "title": "filedialog", "note": "показывается диалог"},
        {"kind": "plain", "title": "отмена?", "note": ""},
        {"kind": "plain", "title": "return", "note": "да — ничего не делаем"},
        {"kind": "file", "title": "Path(filename)", "note": "нет — есть путь"},
        {"kind": "object", "title": "read_text(encoding=\"utf-8\")"},
    ], caption="Правильный порядок: сначала проверка отмены, потом работа с путём.")}

    {local_or_practice("16-19", "Практика: filedialog + pathlib", "", "../../practice/16-19/index.html")}
    """
    page(
        "16-19-filedialog-i-pathlib.html",
        page_title="Открываем и сохраняем файлы: filedialog и pathlib",
        description="askopenfilename/asksaveasfilename в связке с pathlib из главы 15 — и обязательная проверка отмены диалога перед работой с путём.",
        kicker_suffix="filedialog и pathlib",
        h1="Открываем и сохраняем файлы: filedialog и pathlib",
        lede="Диалог выбора файла отдаёт путь — а дальше работает всё, что мы уже знаем из главы 15.",
        body_html=body,
    )


def build_20() -> None:
    body = f"""
    <h2>Toplevel — дополнительное окно</h2>
    <p>Для второго окна (настройки, «О программе», диалог) используется
    <code class="inline">tk.Toplevel</code>, а не второй <code class="inline">tk.Tk()</code>:</p>
    {code_block(
        "toplevel.py",
        "def otkryt_nastrojki():\n"
        "    okno_nastrojek = tk.Toplevel(root)\n"
        '    okno_nastrojek.title("Настройки")\n'
        '    ttk.Label(okno_nastrojek, text="Здесь будут настройки").pack(padx=20, pady=20)\n\n'
        'ttk.Button(root, text="Настройки", command=otkryt_nastrojki).pack()\n',
    )}
    {relationship_diagram("root : Tk", "okno_nastrojek : Toplevel", "создаёт", style="has-a")}
    {callout(
        "warning",
        "Второй Tk() — типичная ошибка",
        "Каждый дополнительный <code class=\"inline\">tk.Tk()</code> создаёт отдельный "
        "интерпретатор Tcl — это не то же самое, что второе окно приложения, и приводит к "
        "неожиданному поведению. Для любого дополнительного окна — только "
        "<code class=\"inline\">Toplevel</code>.",
    )}

    <h2 id="modal">🔬 Чуть глубже: модальное окно</h2>
    <p>Некоторые диалоги должны блокировать взаимодействие с родительским окном, пока не будут
    закрыты:</p>
    {code_block(
        "modalnoe_okno.py",
        "okno = tk.Toplevel(root)\n"
        "okno.transient(root)     # окно принадлежит родителю визуально\n"
        "okno.grab_set()          # забирает весь ввод, пока не закрыто\n"
        "root.wait_window(okno)   # родитель ждёт закрытия этого окна\n",
    )}
    {callout(
        "info",
        "Не обязательно на старте",
        "Собственные модальные окна — продвинутая техника. Для большинства учебных и "
        "небольших приложений обычного <code class=\"inline\">Toplevel</code> без "
        "<code class=\"inline\">grab_set()</code> вполне достаточно.",
    )}

    {local_or_practice("16-20", "Практика: окно настроек через Toplevel", "", "../../practice/16-20/index.html")}
    """
    page(
        "16-20-toplevel.html",
        page_title="Toplevel: несколько окон",
        description="tk.Toplevel для дополнительных окон вместо второго Tk(), и модальное окно как продвинутая техника (transient, grab_set, wait_window).",
        kicker_suffix="Toplevel",
        h1="Toplevel: несколько окон",
        lede="Настоящему приложению почти всегда нужно больше одного окна — но не больше одного root.",
        body_html=body,
    )


def build_21() -> None:
    body = f"""
    <h2>Фокус ввода</h2>
    <p>Клавиатурный ввод всегда идёт только одному виджету — тому, у которого сейчас
    <strong>фокус</strong>:</p>
    {code_block(
        "focus.py",
        "entry.focus_set()      # передать фокус этому полю программно\n"
        "print(root.focus_get())   # какой виджет в фокусе сейчас\n",
    )}
    {callout(
        "info",
        "Готовим почву для главы 17",
        "Фокус — важное понятие для дальнейшей работы с клавиатурными событиями "
        "(<code class=\"inline\">.bind(\"&lt;Key&gt;\", ...)</code>), которые подробно "
        "разберём в главе 17.",
    )}

    <h2>Порядок перехода между полями (Tab)</h2>
    <p>Пользователь должен уметь заполнить форму, используя только клавиатуру — переходя между
    полями клавишей <code class="inline">Tab</code> в разумном порядке. По умолчанию порядок
    определяется порядком <strong>создания</strong> виджетов — создавайте их в том порядке, в
    котором пользователь логично будет заполнять форму.</p>

    <h2>Основы доступности</h2>
    {capability_map([
        ("Метки", ["у каждого поля — видимая подпись", "не только текст-заглушка (placeholder)"]),
        ("Состояние", ["не только цветом — текстом/иконкой тоже", "disabled — когда действие недоступно"]),
        ("Клавиатура", ["разумный порядок Tab", "не только мышь как единственный путь"]),
        ("Сообщения", ["понятный текст ошибки", "что пошло не так и как исправить"]),
    ], title="Небольшой, но настоящий список")}
    {callout(
        "warning",
        "Tkinter сам не решает доступность за вас",
        "Использование Tkinter не гарантирует доступный интерфейс на всех платформах "
        "автоматически. Перечисленные принципы — то, что зависит от решений в вашем коде "
        "и разметке, а не от самого факта использования GUI-библиотеки.",
    )}

    {code_block(
        "proverka_dostupnosti.py",
        'forma = [\n'
        '    {"name": "name_entry", "has_label": True, "tab_index": 0},\n'
        '    {"name": "email_entry", "has_label": True, "tab_index": 1},\n'
        '    {"name": "submit_button", "has_label": True, "tab_index": 2},\n'
        "]\n\n"
        'def vse_imeyut_metku(widgets):\n'
        "    return all(w[\"has_label\"] for w in widgets)\n\n"
        'def poryadok_posledovatelen(widgets):\n'
        '    indeksy = [w["tab_index"] for w in widgets]\n'
        "    return indeksy == sorted(indeksy)\n",
    )}

    {practice_card("16-21", "Практика: проверка доступности формы", "Проверяется без tkinter — на модели формы как списка данных", "../../practice/16-21/index.html")}
    """
    page(
        "16-21-focus-i-dostupnost.html",
        page_title="Focus, клавиатура и основы доступности",
        description="focus_set()/focus_get(), порядок перехода Tab между полями, и практический список основ доступности интерфейса — метки, состояние, клавиатура, сообщения.",
        kicker_suffix="Focus и доступность",
        h1="Focus, клавиатура и основы доступности",
        lede="Не у каждого пользователя мышь — а понятная форма должна работать и без неё.",
        body_html=body,
    )


def build_22() -> None:
    body = f"""
    <h2>after() — отложенный вызов без блокировки</h2>
    {code_block(
        "after_prosto.py",
        'after_id = root.after(1000, lambda: print("Прошла секунда"))\n'
        "# программа продолжает обрабатывать другие события, ожидая эту секунду\n",
    )}
    {pipeline_diagram([
        {"kind": "plain", "title": "событийный цикл"},
        {"kind": "plain", "title": "запланировать через after()", "note": ""},
        {"kind": "object", "title": "другие события продолжают обрабатываться"},
        {"kind": "plain", "title": "время подошло", "note": "callback вызывается"},
    ], caption="after() ставит callback в очередь на будущее — и не блокирует всё остальное в ожидании.")}

    <h2>Повторяющийся таймер</h2>
    {code_block(
        "tik.py",
        "def tik():\n"
        '    label.config(text=f"Секунд: {schet.get()}")\n'
        "    schet.set(schet.get() + 1)\n"
        "    root.after(1000, tik)   # сам себя планирует заново — вот и повторение\n",
    )}
    {callout(
        "info",
        "Не только for/while — это тоже повторение",
        "Из главы 10 мы знаем циклы <code class=\"inline\">for</code>/<code class=\"inline\">while</code>. "
        "Повторяющийся вызов через self-scheduling <code class=\"inline\">after()</code> — "
        "ещё один способ организовать повторение, устроенный на событиях, а не на "
        "последовательном блоке кода.",
    )}

    <h2>Остановка таймера: after_cancel</h2>
    {code_block(
        "after_cancel.py",
        "tikayushij_id = root.after(1000, tik)\n\n"
        "def stop():\n"
        "    root.after_cancel(tikayushij_id)\n",
    )}
    {callout(
        "warning",
        "Не потеряйте идентификатор",
        "Чтобы остановить запланированный вызов, нужно сохранить идентификатор, который "
        "вернул <code class=\"inline\">after()</code>. Без него отменить именно этот "
        "запланированный вызов не получится.",
    )}

    {debug_lab(
        2,
        "Повторный запуск создаёт дублирующиеся таймеры",
        "duplicate_after.py",
        'def start():\n'
        "    tik()   # каждый клик по «Старт» запускает ЕЩЁ один цикл tik()\n\n"
        'ttk.Button(root, text="Старт", command=start).pack()\n',
        ["# После нескольких нажатий «Старт» счётчик начинает прыгать сразу на 2, 3, 4 за секунду —", "# работает уже несколько параллельных цепочек after()."],
        "Каждый клик запускает новую независимую цепочку самопланирующихся вызовов "
        "<code class=\"inline\">tik()</code>, и они не заменяют друг друга, а работают "
        "одновременно. Нужно либо блокировать повторный старт, либо явно отменять предыдущую "
        "цепочку перед новым запуском.",
        "duplicate_after_fixed.py",
        'tikayushij_id = None\n\n'
        'def start():\n'
        "    global tikayushij_id\n"
        "    if tikayushij_id is not None:\n"
        "        return   # уже запущено — повторный клик игнорируем\n"
        "    tik()\n",
    )}

    {callout(
        "warning",
        "Никогда time.sleep() внутри callback",
        "<code class=\"inline\">time.sleep(...)</code> в обработчике останавливает событийный "
        "цикл целиком на всё время сна — интерфейс перестаёт отвечать. Подробный разбор — в "
        "разделе 16.24.",
    )}

    {local_or_practice("16-22", "Практика: таймер обратного отсчёта через after()", "", "../../practice/16-22/index.html")}
    """
    page(
        "16-22-after-tajmery.html",
        page_title="after(): таймеры без блокировки",
        description="root.after() для отложенных и повторяющихся вызовов без блокировки событийного цикла, after_cancel() и типичная ошибка с дублирующимися таймерами при повторном старте.",
        kicker_suffix="after() и таймеры",
        h1="after(): таймеры без блокировки",
        lede="Нужно подождать — не значит нужно остановить всё приложение.",
        body_html=body,
    )


def build_23() -> None:
    body = f"""
    <h2>Валидация — прежде чем считать</h2>
    {pipeline_diagram([
        {"kind": "object", "title": "текст пользователя", "rows": ["entry.get()"]},
        {"kind": "plain", "title": "валидация", "note": "пусто? не число? отрицательное?"},
        {"kind": "plain", "title": "валидно?"},
        {"kind": "plain", "title": "сообщение пользователю", "note": "нет — понятная ошибка"},
        {"kind": "object", "title": "числовое значение", "note": "да — конвертация"},
        {"kind": "plain", "title": "доменная функция"},
    ], caption="Ввод не превращается в число сам — между строкой и вычислением есть проверка.")}
    {code_block(
        "validate_amount.py",
        'def validate_amount(text):\n'
        '    if not text.strip():\n'
        '        return False, "Поле не должно быть пустым"\n'
        "    try:\n"
        "        value = float(text)\n"
        "    except ValueError:\n"
        '        return False, "Введите число"\n'
        "    if value <= 0:\n"
        '        return False, "Число должно быть больше нуля"\n'
        '    return True, ""\n\n'
        'print(validate_amount(""))      # (False, ...)\n'
        'print(validate_amount("abc"))   # (False, ...)\n'
        'print(validate_amount("-5"))    # (False, ...)\n'
        'print(validate_amount("100"))   # (True, "")\n',
    )}

    <h2>Как показать ошибку пользователю</h2>
    {code_block(
        "status_label.py",
        "ok, message = validate_amount(schet_entry.get())\n"
        "if not ok:\n"
        '    status_label.config(text=message, foreground="#DB2777")\n'
        "    return\n",
    )}
    {callout(
        "warning",
        "Ошибка — на экране, а не только в терминале",
        "GUI-пользователь обычно не смотрит в терминал. Показывайте ошибку через "
        "виджет-статус или <code class=\"inline\">messagebox.showerror(...)</code> (раздел "
        "16.18) — печать <code class=\"inline\">print(...)</code> в терминал не считается "
        "обратной связью пользователю в оконном приложении.",
    )}

    <h2 id="validatecommand">🔬 Чуть глубже: validatecommand</h2>
    <p>У Tkinter есть встроенный механизм валидации прямо на уровне виджета
    (<code class="inline">validate=</code>, <code class="inline">validatecommand=</code>,
    <code class="inline">register(...)</code>) — синтаксис у него не самый интуитивный, поэтому
    для большинства форм в этом курсе достаточно ручной проверки перед вычислением, как выше.</p>

    {practice_card("16-23", "Практика: валидация суммы", "Проверяется без tkinter — на чистой функции validate_amount", "../../practice/16-23/index.html")}
    """
    page(
        "16-23-validatsiya-vvoda.html",
        page_title="Валидация ввода и обратная связь",
        description="Проверка пустого, нечислового и отрицательного ввода перед вычислением, и почему ошибка должна быть видна пользователю на экране, а не только в терминале.",
        kicker_suffix="Валидация ввода",
        h1="Валидация ввода и обратная связь",
        lede="Сырой текст пользователя не становится числом сам — между ними должна быть проверка.",
        body_html=body,
    )


def build_24() -> None:
    body = f"""
    <h2>Чистая логика отдельно от виджетов</h2>
    <p>Прямая связь с главой 13: доменную функцию можно написать и протестировать
    <strong>независимо</strong> от интерфейса — просто вход и выход, без единого виджета:</p>
    {code_block(
        "chistaya_logika.py",
        'def calculate_tip(amount, percent, people):\n'
        "    total_tip = amount * percent / 100\n"
        "    return total_tip / people\n\n"
        'print(calculate_tip(1000, 15, 2))   # 75.0\n',
    )}
    {pipeline_diagram([
        {"kind": "plain", "title": "callback (обработчик кнопки)"},
        {"kind": "object", "title": "прочитать значения виджетов"},
        {"kind": "plain", "title": "проверить (раздел 16.23)"},
        {"kind": "object", "title": "calculate_tip(...)", "note": "чистая функция — без единого виджета внутри"},
        {"kind": "plain", "title": "показать результат в виджете"},
    ], caption="Callback — тонкий слой-посредник; вся логика вычисления живёт вне интерфейса.")}
    {callout(
        "warning",
        "Callback не должен разрастаться",
        "Если обработчик кнопки занимает сотню строк с вложенными вычислениями — вероятно, "
        "часть этой логики стоит вынести в отдельную функцию, которую можно понять и "
        "проверить без запуска окна.",
    )}

    <h2 id="lambda-trap">🔬 Чуть глубже: ловушка позднего связывания в lambda</h2>
    {debug_lab(
        3,
        "Все кнопки в цикле «запоминают» одно и то же значение",
        "pozdnee_svyazyvanie.py",
        'for i in range(3):\n'
        '    ttk.Button(root, text=str(i), command=lambda: print(i)).pack()\n',
        ["# Все три кнопки выведут одно и то же число — последнее значение i (2),", "# а не 0, 1, 2 соответственно."],
        "<code class=\"inline\">lambda: print(i)</code> обращается к переменной "
        "<code class=\"inline\">i</code> из окружающей области видимости <strong>в момент "
        "клика</strong>, а не в момент создания кнопки (глава 13, замыкания). К моменту клика "
        "цикл уже закончился, и <code class=\"inline\">i</code> равно своему последнему "
        "значению — 2 — для всех трёх кнопок сразу.",
        "pozdnee_svyazyvanie_fixed.py",
        'for i in range(3):\n'
        '    ttk.Button(root, text=str(i), command=lambda i=i: print(i)).pack()\n'
        "# i=i создаёт значение по умолчанию, зафиксированное ИМЕННО в момент создания lambda\n",
    )}
    {code_block(
        "proverka_lambda_fix.py",
        'callbacks = []\n'
        "for i in range(3):\n"
        "    callbacks.append(lambda i=i: i)\n\n"
        'values = [cb() for cb in callbacks]\n'
        "print(values)   # [0, 1, 2]\n",
    )}

    {practice_card("16-24", "Практика: чистая логика и ловушка lambda", "Проверяется без tkinter — на функциях и замыканиях", "../../practice/16-24/index.html")}
    """
    page(
        "16-24-arhitektura-prilozheniya.html",
        page_title="Архитектура приложения: логика отдельно от виджетов",
        description="Доменная функция без единого виджета внутри, callback как тонкий слой-посредник, и ловушка позднего связывания переменной в lambda внутри цикла.",
        kicker_suffix="Архитектура приложения",
        h1="Архитектура приложения: логика отдельно от виджетов",
        lede="Лучшая GUI-логика — та, которую можно протестировать, даже не открывая окно.",
        body_html=body,
    )


def build_25() -> None:
    body = f"""
    <h2>Класс приложения — композиция, а не наследование Tk</h2>
    <p>Прямая связь с главой 14. Для приложений сложнее пары виджетов удобно собрать всё в один
    класс:</p>
    {code_block(
        "klass_prilozheniya.py",
        "class TipCalculatorApp:\n"
        "    def __init__(self, root):\n"
        "        self.root = root\n"
        '        self.amount_var = tk.StringVar()\n'
        "        self.build_ui()\n\n"
        "    def build_ui(self):\n"
        '        ttk.Entry(self.root, textvariable=self.amount_var).pack()\n'
        '        ttk.Button(self.root, text="Считать", command=self.on_calculate).pack()\n\n'
        "    def on_calculate(self):\n"
        "        ...\n\n"
        "root = tk.Tk()\n"
        "app = TipCalculatorApp(root)\n"
        "root.mainloop()\n",
    )}
    {object_diagram(
        "app", "TipCalculatorApp",
        [("root", "Tk"), ("amount_var", "StringVar"), ("result_var", "StringVar")],
        caption="Объектный граф приложения: App HAS-A root, а не App IS-A Tk.",
    )}
    {callout(
        "info",
        "App содержит root, а не наследует от Tk",
        "<code class=\"inline\">class App:</code> с <code class=\"inline\">self.root = root</code> "
        "— основная модель этого курса: зависимость от Tk видна явно в конструкторе. "
        "Наследование <code class=\"inline\">class App(tk.Tk):</code> тоже возможно и "
        "встречается на практике — но композиция здесь проще для рассуждений, не "
        "«неправильный» вариант против «правильного».",
    )}
    {callout(
        "warning",
        "Не каждый виджет — атрибут self",
        "Сохраняйте в <code class=\"inline\">self.виджет</code> только то, к чему понадобится "
        "обратиться позже из другого метода (поле ввода, метка результата). Временные "
        "виджеты, созданные и размещённые в одном месте, можно оставить локальными "
        "переменными <code class=\"inline\">build_ui()</code>.",
    )}

    <h2>Персистентные настройки — мост к главе 15</h2>
    {code_block(
        "nastroyki_gui.py",
        "import json\n"
        "from pathlib import Path\n\n"
        'DEFAULT_SETTINGS = {"theme": "light", "window_width": 900}\n\n'
        "def load_settings(path):\n"
        "    if not path.exists():\n"
        "        return dict(DEFAULT_SETTINGS)\n"
        '    with path.open("r", encoding="utf-8") as f:\n'
        "        return json.load(f)\n\n"
        "def save_settings(path, settings):\n"
        '    with path.open("w", encoding="utf-8") as f:\n'
        "        json.dump(settings, f, ensure_ascii=False, indent=2)\n",
    )}
    {pipeline_diagram([
        {"kind": "file", "title": "nastroyki.json"},
        {"kind": "object", "title": "load_settings()", "note": "при старте приложения"},
        {"kind": "plain", "title": "TipCalculatorApp(root, settings)"},
        {"kind": "plain", "title": "пользователь меняет настройку"},
        {"kind": "file", "title": "nastroyki.json", "note": "save_settings() перед закрытием"},
    ], caption="Ни одна строчка про JSON и файлы не нова — всё уже было в главе 15.")}
    {callout(
        "tip",
        "Ни единой новой идеи о файлах",
        "<code class=\"inline\">load_settings()</code>/<code class=\"inline\">save_settings()</code> "
        "не используют ничего, кроме того, что уже изучено в главе 15 — <code "
        "class=\"inline\">json</code>, <code class=\"inline\">pathlib</code>, безопасные "
        "значения по умолчанию. GUI просто вызывает эти функции при старте и перед закрытием.",
    )}

    {practice_card("16-25", "Практика: load_settings/save_settings для GUI", "Проверяется без tkinter — переносим функции persistence главы 15", "../../practice/16-25/index.html")}
    """
    page(
        "16-25-klass-prilozheniya-i-nastrojki.html",
        page_title="Класс приложения и персистентные настройки",
        description="App как объект, содержащий root (композиция, а не наследование Tk), объектный граф приложения, и персистентные настройки через load_settings/save_settings из главы 15.",
        kicker_suffix="Класс приложения",
        h1="Класс приложения и персистентные настройки",
        lede="Приложение — тоже объект: со своим состоянием, виджетами-атрибутами и методами-обработчиками.",
        body_html=body,
    )


def build_26() -> None:
    body = f"""
    <p>Самый маленький настоящий проект главы: счётчик кликов. Хорошая возможность увидеть оба
    способа хранить число, связанное с виджетом.</p>
    {code_block(
        "schetchik_intvar.py",
        "import tkinter as tk\n"
        "from tkinter import ttk\n\n"
        "root = tk.Tk()\n"
        'root.title("Счётчик кликов")\n\n'
        "schet = tk.IntVar(value=0)\n"
        'ttk.Label(root, textvariable=schet, font=("Arial", 24)).pack(pady=20)\n\n'
        "def na_klik():\n"
        "    schet.set(schet.get() + 1)\n\n"
        'ttk.Button(root, text="+1", command=na_klik).pack(pady=10)\n\n'
        "root.mainloop()\n",
    )}
    {callout(
        "info",
        "Второй способ — без Tk-переменной",
        "Тот же счётчик можно собрать с обычным <code class=\"inline\">int</code> и явным "
        "<code class=\"inline\">label.config(text=...)</code> после каждого изменения — "
        "работает одинаково хорошо; <code class=\"inline\">IntVar</code> удобен именно когда "
        "значение нужно синхронизировать сразу с несколькими виджетами (раздел 16.4).",
    )}

    {debug_lab(
        4,
        "Забыли mainloop() — окно не работает как надо",
        "bez_mainloop.py",
        "root = tk.Tk()\n"
        'ttk.Button(root, text="+1").pack()\n'
        "# забыли root.mainloop()!\n",
        ["# Скрипт завершается почти сразу — окно либо не появляется,", "# либо мгновенно закрывается, не дожидаясь никаких действий пользователя."],
        "Без <code class=\"inline\">root.mainloop()</code> программа не переходит в цикл "
        "обработки событий (раздел 16.10) — она просто линейно доходит до конца скрипта и "
        "завершается, как обычная терминальная программа. Виджеты созданы и даже размещены, "
        "но никто не ждёт кликов по ним.",
        "s_mainloop.py",
        "root = tk.Tk()\n"
        'ttk.Button(root, text="+1").pack()\n'
        "root.mainloop()   # без этого вызова событий не будет вообще\n",
    )}

    {local_or_practice("16-26", "Практика: счётчик кликов", "", "../../practice/16-26/index.html")}
    """
    page(
        "16-26-mini-proekt-schetchik-klikov.html",
        page_title="Мини-проект: счётчик кликов",
        description="Самый маленький настоящий проект главы — счётчик кликов через IntVar, и почему забытый mainloop() оставляет приложение без единого события.",
        kicker_suffix="Счётчик кликов",
        h1="Мини-проект: счётчик кликов",
        lede="Маленький проект — но уже настоящее взаимодействие: клик → callback → изменение состояния → обновление экрана.",
        body_html=body,
    )


def build_27() -> None:
    body = f"""
    <p>Форма «ввод → проверка → чистая функция → результат» на практике: конвертер температур.</p>
    {code_block(
        "konverter_temperatur.py",
        'def celsius_v_farengejty(celsius):\n'
        "    return celsius * 9 / 5 + 32\n\n"
        'def farengejty_v_celsius(farengejty):\n'
        "    return (farengejty - 32) * 5 / 9\n\n"
        'print(round(celsius_v_farengejty(100), 1))   # 212.0\n'
        'print(round(farengejty_v_celsius(32), 1))    # 0.0\n',
    )}
    {code_block(
        "konverter_gui.py",
        "import tkinter as tk\n"
        "from tkinter import ttk\n\n"
        "root = tk.Tk()\n"
        "celsius_var = tk.StringVar()\n"
        "result_var = tk.StringVar()\n\n"
        "def on_convert():\n"
        "    ok, message = validate_amount(celsius_var.get())\n"
        "    if not ok:\n"
        "        result_var.set(message)\n"
        "        return\n"
        "    farengejty = celsius_v_farengejty(float(celsius_var.get()))\n"
        '    result_var.set(f"{farengejty:.1f} °F")\n\n'
        'ttk.Entry(root, textvariable=celsius_var).pack()\n'
        'ttk.Button(root, text="В Фаренгейты", command=on_convert).pack()\n'
        'ttk.Label(root, textvariable=result_var).pack()\n',
    )}
    {callout(
        "tip",
        "validate_amount уже знаком",
        "Функция <code class=\"inline\">validate_amount</code> — та же самая, что мы написали в "
        "разделе 16.23. Один раз написанная и проверенная функция валидации пригождается в "
        "нескольких проектах.",
    )}
    {exercise(2, "Оба направления", "Добавьте второе поле и кнопку «В Цельсии», использующую farengejty_v_celsius — по образцу существующей кнопки.")}

    {practice_card("16-27", "Практика: конвертер температур", "Проверяется без tkinter — на чистых функциях преобразования", "../../practice/16-27/index.html")}
    """
    page(
        "16-27-mini-proekt-konverter-temperatur.html",
        page_title="Мини-проект: конвертер температур",
        description="Классическая форма ввод → проверка → чистая функция → результат на примере конвертера температур Цельсий/Фаренгейт.",
        kicker_suffix="Конвертер температур",
        h1="Мини-проект: конвертер температур",
        lede="Простая форма — но по образцовой архитектуре: чистая функция преобразования отдельно от интерфейса.",
        body_html=body,
    )


def build_28() -> None:
    body = f"""
    <p>Таймер обратного отсчёта — образцовая демонстрация <code class="inline">after()</code> и
    состояния приложения.</p>
    {code_block(
        "format_time.py",
        'def format_time(sekundy):\n'
        "    minuty, ostatok = divmod(sekundy, 60)\n"
        '    return f"{minuty:02d}:{ostatok:02d}"\n\n'
        'print(format_time(65))    # 01:05\n'
        'print(format_time(600))   # 10:00\n',
    )}
    {code_block(
        "tajmer_gui.py",
        "class TimerApp:\n"
        "    def __init__(self, root):\n"
        "        self.root = root\n"
        "        self.remaining = 60\n"
        "        self.running = False\n"
        "        self.after_id = None\n"
        '        self.label_var = tk.StringVar(value=format_time(self.remaining))\n'
        "        ttk.Label(root, textvariable=self.label_var).pack()\n"
        '        ttk.Button(root, text="Старт", command=self.start).pack()\n'
        '        ttk.Button(root, text="Стоп", command=self.stop).pack()\n\n'
        "    def start(self):\n"
        "        if self.running:\n"
        "            return\n"
        "        self.running = True\n"
        "        self.tick()\n\n"
        "    def tick(self):\n"
        "        if not self.running or self.remaining <= 0:\n"
        "            return\n"
        "        self.remaining -= 1\n"
        "        self.label_var.set(format_time(self.remaining))\n"
        "        self.after_id = self.root.after(1000, self.tick)\n\n"
        "    def stop(self):\n"
        "        self.running = False\n"
        "        if self.after_id is not None:\n"
        "            self.root.after_cancel(self.after_id)\n",
    )}
    {debug_lab(
        5,
        "Таймер продолжает тикать после «Стоп»",
        "tajmer_bez_proverki.py",
        "def tick(self):\n"
        "    self.remaining -= 1\n"
        "    self.label_var.set(format_time(self.remaining))\n"
        "    self.after_id = self.root.after(1000, self.tick)   # планирует себя ВСЕГДА\n\n"
        "def stop(self):\n"
        "    self.running = False   # состояние поменяли, но tick() его не проверяет\n",
        ["# После нажатия «Стоп» таймер продолжает уменьшать remaining и тикать —", "# флаг running изменился, но ничто не проверяет его внутри tick()."],
        "<code class=\"inline\">stop()</code> лишь меняет флаг <code class=\"inline\">running</code>, "
        "но сам метод <code class=\"inline\">tick()</code> не проверяет его перед тем, как "
        "запланировать себя заново — цепочка <code class=\"inline\">after()</code> продолжает "
        "жить независимо от флага.",
        "tajmer_s_proverkoj.py",
        "def tick(self):\n"
        "    if not self.running:   # проверяем состояние ПЕРЕД тем как продолжить\n"
        "        return\n"
        "    self.remaining -= 1\n"
        "    self.label_var.set(format_time(self.remaining))\n"
        "    self.after_id = self.root.after(1000, self.tick)\n",
    )}

    {local_or_practice("16-28", "Практика: таймер обратного отсчёта", "", "../../practice/16-28/index.html")}
    """
    page(
        "16-28-mini-proekt-tajmer.html",
        page_title="Мини-проект: таймер обратного отсчёта",
        description="Таймер на after() с состоянием remaining/running/after_id, и типичная ошибка — самопланирующийся callback, который не проверяет флаг остановки.",
        kicker_suffix="Таймер",
        h1="Мини-проект: таймер обратного отсчёта",
        lede="after() в деле: обратный отсчёт без единой блокирующей операции.",
        body_html=body,
    )


def build_29() -> None:
    body = f"""
    <p>Список задач — интеграция главы 11 (списки), главы 15 (JSON) и Tkinter (Listbox).</p>
    {pipeline_diagram([
        {"kind": "object", "title": "tasks : list[str]", "note": "данные"},
        {"kind": "plain", "title": "Listbox", "note": "отображение"},
        {"kind": "plain", "title": "add_task() / remove_task()", "note": "callback"},
        {"kind": "file", "title": "todo.json", "note": "персистентность"},
    ], caption="Данные, отображение и персистентность — три разных ответственности одного небольшого приложения.")}
    {code_block(
        "todo_logika.py",
        "import json\n"
        "from pathlib import Path\n\n"
        "def load_tasks(path):\n"
        "    if not path.exists():\n"
        "        return []\n"
        '    with path.open("r", encoding="utf-8") as f:\n'
        "        return json.load(f)\n\n"
        "def save_tasks(path, tasks):\n"
        '    with path.open("w", encoding="utf-8") as f:\n'
        "        json.dump(tasks, f, ensure_ascii=False, indent=2)\n\n"
        "def add_task(tasks, text):\n"
        "    if not text.strip():\n"
        "        return tasks\n"
        "    return tasks + [text.strip()]\n\n"
        "def remove_task(tasks, index):\n"
        "    return tasks[:index] + tasks[index + 1:]\n",
    )}
    {code_block(
        "todo_gui.py",
        "def on_add():\n"
        "    nonlocal tasks\n"
        "    tasks = add_task(tasks, novaya_var.get())\n"
        "    obnovit_listbox()\n"
        "    save_tasks(TODO_PATH, tasks)\n\n"
        "def on_delete():\n"
        "    nonlocal tasks\n"
        "    vybrannye = listbox.curselection()\n"
        "    if not vybrannye:\n"
        "        return\n"
        "    tasks = remove_task(tasks, vybrannye[0])\n"
        "    obnovit_listbox()\n"
        "    save_tasks(TODO_PATH, tasks)\n",
    )}
    {callout(
        "tip",
        "Логика проверяема без единого виджета",
        "<code class=\"inline\">add_task</code>, <code class=\"inline\">remove_task</code>, "
        "<code class=\"inline\">load_tasks</code>, <code class=\"inline\">save_tasks</code> — "
        "обычные функции со списками и словарями. Именно их и тестирует практика этого "
        "раздела — ровно то разделение, о котором шла речь в разделе 16.24.",
    )}

    {practice_card("16-29", "Практика: логика списка задач", "Проверяется без tkinter — на функциях работы со списком задач", "../../practice/16-29/index.html")}
    """
    page(
        "16-29-mini-proekt-todo.html",
        page_title="Мини-проект: список задач",
        description="Список задач на Listbox и JSON: данные (list[str]), отображение (Listbox) и персистентность (todo.json) — три чётко разделённые ответственности.",
        kicker_suffix="Список задач",
        h1="Мини-проект: список задач",
        lede="Простой список строк — и уже целое маленькое приложение с сохранением между запусками.",
        body_html=body,
    )


def build_30() -> None:
    body = f"""
    <p>Прямое продолжение дневника заметок из главы 15 (15.4) — теперь с настоящим окном,
    многострочным полем и меню «Файл».</p>
    {code_block(
        "redaktor_zametok.py",
        "import tkinter as tk\n"
        "from tkinter import ttk, filedialog, messagebox\n"
        "from tkinter.scrolledtext import ScrolledText\n"
        "from pathlib import Path\n\n"
        "root = tk.Tk()\n"
        'root.title("Редактор заметок")\n\n'
        "text_widget = ScrolledText(root, wrap=\"word\")\n"
        "text_widget.pack(fill=\"both\", expand=True)\n\n"
        "current_path = None\n\n"
        "def novyj_fajl():\n"
        "    global current_path\n"
        '    text_widget.delete("1.0", "end")\n'
        "    current_path = None\n\n"
        "def otkryt_fajl():\n"
        "    global current_path\n"
        '    filename = filedialog.askopenfilename(filetypes=[("Текстовые файлы", "*.txt")])\n'
        "    if not filename:\n"
        "        return\n"
        "    current_path = Path(filename)\n"
        '    text_widget.delete("1.0", "end")\n'
        '    text_widget.insert("1.0", current_path.read_text(encoding="utf-8"))\n\n'
        "def sohranit_kak():\n"
        "    global current_path\n"
        '    filename = filedialog.asksaveasfilename(defaultextension=".txt")\n'
        "    if not filename:\n"
        "        return\n"
        "    current_path = Path(filename)\n"
        '    current_path.write_text(text_widget.get("1.0", "end-1c"), encoding="utf-8")\n'
        '    messagebox.showinfo("Готово", "Заметки сохранены.")\n\n'
        "menu_bar = tk.Menu(root)\n"
        "fajl_menu = tk.Menu(menu_bar, tearoff=0)\n"
        'fajl_menu.add_command(label="Новый", command=novyj_fajl)\n'
        'fajl_menu.add_command(label="Открыть...", command=otkryt_fajl)\n'
        'fajl_menu.add_command(label="Сохранить как...", command=sohranit_kak)\n'
        "fajl_menu.add_separator()\n"
        'fajl_menu.add_command(label="Выход", command=root.destroy)\n'
        'menu_bar.add_cascade(label="Файл", menu=fajl_menu)\n'
        "root.config(menu=menu_bar)\n\n"
        "root.mainloop()\n",
    )}
    {callout(
        "info",
        "Ничего принципиально нового про файлы",
        "<code class=\"inline\">filedialog</code> (16.19), <code class=\"inline\">Path.read_text/write_text(encoding=\"utf-8\")</code> "
        "(глава 15), <code class=\"inline\">ScrolledText</code> (готовая связка "
        "<code class=\"inline\">Text</code> + <code class=\"inline\">Scrollbar</code>) — все "
        "части уже знакомы, здесь они просто собраны в одно приложение.",
    )}
    {exercise(3, "Отслеживание несохранённых изменений", "Добавьте булев флаг «есть несохранённые изменения» и при попытке открыть новый файл/выйти с несохранёнными изменениями — спрашивайте через messagebox.askyesno, сохранить ли их сначала.")}

    {local_or_practice("16-30", "Практика: редактор заметок", "", "../../practice/16-30/index.html")}
    """
    page(
        "16-30-mini-proekt-zametki.html",
        page_title="Мини-проект: редактор заметок",
        description="Полноценный редактор заметок на ScrolledText, меню «Файл» и filedialog + pathlib из главы 15 — прямое продолжение дневника заметок.",
        kicker_suffix="Редактор заметок",
        h1="Мини-проект: редактор заметок",
        lede="Дневник заметок из главы 15 наконец получает настоящее окно и меню.",
        body_html=body,
    )


def build_31() -> None:
    body = f"""
    <p>Вернёмся к калькулятору чаевых (раздел 16.8) и соберём в нём всё, что изучили в этой
    главе — по стадиям, а не одним огромным финальным куском кода.</p>
    {capability_map([
        ("V1–V2 (16.8)", ["Entry + Button + grid()", "чистая формула чаевых"]),
        ("V3", ["Combobox с типовыми процентами вместо Entry"]),
        ("V4", ["поле «количество человек» — делим чаевые"]),
        ("V5", ["validate_amount() перед вычислением (16.23)"]),
        ("V6", ["меню «Файл» с пунктом «Выход» (16.6)"]),
        ("V7", ["load_settings/save_settings — запоминаем последний процент (16.25)"]),
        ("V8", ["класс TipCalculatorApp — всё внутри одного объекта (16.25)"]),
    ], title="Путь от фундамента до Pro")}

    {code_block(
        "tip_calculator_pro.py",
        "import json\n"
        "import tkinter as tk\n"
        "from tkinter import ttk, messagebox\n"
        "from pathlib import Path\n\n"
        'SETTINGS_PATH = Path("tip_calculator_settings.json")\n'
        'DEFAULT_SETTINGS = {"last_percent": "15"}\n\n'
        "def load_settings():\n"
        "    if not SETTINGS_PATH.exists():\n"
        "        return dict(DEFAULT_SETTINGS)\n"
        '    with SETTINGS_PATH.open("r", encoding="utf-8") as f:\n'
        "        return json.load(f)\n\n"
        "def save_settings(settings):\n"
        '    with SETTINGS_PATH.open("w", encoding="utf-8") as f:\n'
        "        json.dump(settings, f, ensure_ascii=False, indent=2)\n\n"
        "def calculate_tip(amount, percent, people):\n"
        "    return (amount * percent / 100) / people\n\n"
        "def validate_amount(text):\n"
        "    if not text.strip():\n"
        '        return False, "Поле не должно быть пустым"\n'
        "    try:\n"
        "        value = float(text)\n"
        "    except ValueError:\n"
        '        return False, "Введите число"\n'
        "    if value <= 0:\n"
        '        return False, "Число должно быть больше нуля"\n'
        '    return True, ""\n\n'
        "class TipCalculatorApp:\n"
        "    def __init__(self, root):\n"
        "        self.root = root\n"
        "        self.root.title(\"Tip Calculator Pro\")\n"
        "        self.settings = load_settings()\n"
        '        self.amount_var = tk.StringVar()\n'
        '        self.percent_var = tk.StringVar(value=self.settings["last_percent"])\n'
        '        self.people_var = tk.StringVar(value="1")\n'
        '        self.result_var = tk.StringVar()\n'
        "        self.build_ui()\n"
        '        self.root.protocol("WM_DELETE_WINDOW", self.on_close)\n\n'
        "    def build_ui(self):\n"
        '        frame = ttk.Frame(self.root, padding=12)\n'
        '        frame.grid(row=0, column=0, sticky="nsew")\n'
        '        self.root.columnconfigure(0, weight=1)\n\n'
        '        ttk.Label(frame, text="Сумма счёта:").grid(row=0, column=0, sticky="w")\n'
        '        ttk.Entry(frame, textvariable=self.amount_var).grid(row=0, column=1, sticky="ew")\n\n'
        '        ttk.Label(frame, text="Процент чаевых:").grid(row=1, column=0, sticky="w")\n'
        '        ttk.Combobox(frame, textvariable=self.percent_var, values=["10", "15", "20"],\n'
        '            state="readonly").grid(row=1, column=1, sticky="ew")\n\n'
        '        ttk.Label(frame, text="Количество человек:").grid(row=2, column=0, sticky="w")\n'
        '        ttk.Entry(frame, textvariable=self.people_var).grid(row=2, column=1, sticky="ew")\n\n'
        '        ttk.Button(frame, text="Посчитать", command=self.on_calculate).grid(\n'
        '            row=3, column=0, columnspan=2, pady=8)\n'
        '        ttk.Label(frame, textvariable=self.result_var).grid(row=4, column=0, columnspan=2)\n'
        '        frame.columnconfigure(1, weight=1)\n\n'
        "    def on_calculate(self):\n"
        "        ok, message = validate_amount(self.amount_var.get())\n"
        "        if not ok:\n"
        "            self.result_var.set(message)\n"
        "            return\n"
        "        ok_people, message_people = validate_amount(self.people_var.get())\n"
        "        if not ok_people:\n"
        '            self.result_var.set("Количество человек: " + message_people)\n'
        "            return\n"
        "        chaevye = calculate_tip(\n"
        "            float(self.amount_var.get()),\n"
        "            float(self.percent_var.get()),\n"
        "            float(self.people_var.get()),\n"
        "        )\n"
        '        self.result_var.set(f"Чаевые с человека: {chaevye:.2f}")\n'
        '        self.settings["last_percent"] = self.percent_var.get()\n\n'
        "    def on_close(self):\n"
        "        save_settings(self.settings)\n"
        "        self.root.destroy()\n\n"
        "root = tk.Tk()\n"
        "app = TipCalculatorApp(root)\n"
        "root.mainloop()\n",
    )}
    {image_figure(f"{IMG}/tip-calculator-pro.png", "Окно Tip Calculator Pro с суммой счёта 1000, процентом 15 и результатом 75.00", f"Результат выполнения кода выше — настоящее окно, а не иллюстрация. {PLATFORM_NOTE}", width=360)}
    {object_diagram(
        "app", "TipCalculatorApp",
        [("root", "Tk"), ("settings", "dict"), ("amount_var", "StringVar"), ("percent_var", "StringVar"), ("result_var", "StringVar")],
        caption="Финальный объектный граф: одно приложение, явные зависимости, ни одной глобальной переменной.",
    )}

    {local_or_practice("16-31", "Практика: Tip Calculator Pro", "", "../../practice/16-31/index.html")}
    """
    page(
        "16-31-tip-calculator-pro.html",
        page_title="Tip Calculator Pro: финальная версия",
        description="Пошаговая эволюция калькулятора чаевых от раздела 16.8 до класса приложения с валидацией, ttk, адаптивным grid, меню и персистентными настройками.",
        kicker_suffix="Tip Calculator Pro",
        h1="Tip Calculator Pro: финальная версия",
        lede="Тот же проект, что и в разделе 16.8 — но теперь со всем, что мы изучили после него.",
        body_html=body,
    )


def build_32() -> None:
    body = f"""
    <h2>Событийный цикл нельзя занимать надолго</h2>
    {debug_lab(
        6,
        "time.sleep() внутри callback замораживает интерфейс",
        "sleep_v_callback.py",
        "import time\n\n"
        "def on_click():\n"
        "    time.sleep(5)   # \"подождать 5 секунд\"\n"
        '    label.config(text="Готово!")\n',
        ["# На все 5 секунд окно перестаёт перерисовываться и реагировать на клики —", "# событийный цикл заблокирован внутри time.sleep(), а не только сам callback."],
        "<code class=\"inline\">time.sleep(...)</code> останавливает <strong>весь поток</strong>, "
        "в котором работает событийный цикл — а Tkinter обычно работает в одном потоке. Пока "
        "поток спит, цикл не может обработать вообще ничего: ни перерисовку, ни клики, ни "
        "закрытие окна.",
        "after_vmesto_sleep.py",
        "def on_click():\n"
        '    label.config(text="Ждём...")\n'
        "    root.after(5000, lambda: label.config(text=\"Готово!\"))\n"
        "    # событийный цикл продолжает работать все эти 5 секунд\n",
    )}

    {debug_lab(
        7,
        "while True вместо событийного цикла",
        "while_true_gui.py",
        "while True:\n"
        "    if button_nazhata():\n"
        "        obrabotat_klik()\n",
        ["# Такого кода не должно быть в Tkinter-приложении вообще —", "# у Tk уже есть собственный событийный цикл внутри mainloop()."],
        "Tkinter уже предоставляет полноценный событийный цикл. Собственный "
        "<code class=\"inline\">while True</code> для «опроса» состояния виджетов — не "
        "нужная и не работающая архитектура: она либо блокирует mainloop(), либо просто "
        "избыточна.",
        "mainloop_vmesto_while.py",
        'button.config(command=obrabotat_klik)\n'
        "root.mainloop()   # cам обрабатывает события, включая клики по button\n",
    )}

    {debug_lab(
        8,
        "Долгое вычисление напрямую в callback",
        "dolgoe_vychislenie.py",
        "def on_click():\n"
        "    result = obrabotat_million_zapisej()   # секунды вычислений внутри callback\n"
        '    label.config(text=str(result))\n',
        ["# Интерфейс \"подвисает\" на всё время вычисления — ровно так же,", "# как и с time.sleep(), просто по другой причине."],
        "Любая тяжёлая по времени операция внутри callback — не только "
        "<code class=\"inline\">time.sleep()</code> — занимает событийный цикл на всё это "
        "время. Для по-настоящему долгих задач: разбивать работу на части, планируемые через "
        "<code class=\"inline\">after()</code>, или выносить в отдельный поток/процесс с "
        "безопасной передачей результата обратно — это уже продвинутая тема, не требующая "
        "полной реализации в этом курсе.",
        "razbivka_cherez_after.py",
        "def obrabotat_chast(indeks):\n"
        "    if indeks >= len(dannye):\n"
        '        label.config(text="Готово")\n'
        "        return\n"
        "    obrabotat_odnu_zapis(dannye[indeks])\n"
        "    root.after(0, obrabotat_chast, indeks + 1)   # следующая часть — на следующем такте цикла\n",
    )}
    {callout(
        "warning",
        "Обновление виджетов — из потока событийного цикла",
        "Если превью с рабочим потоком вообще встречается в вашем коде — результат нужно "
        "безопасно передавать обратно и обновлять виджеты именно из событийного цикла "
        "Tkinter, а не напрямую из другого потока. Полная многопоточная архитектура — "
        "вне рамок этой главы.",
    )}

    <h2>Тестируем то, что можно протестировать без окна</h2>
    {code_block(
        "test_domennoj_logiki.py",
        "def test_calculate_tip():\n"
        "    assert calculate_tip(100, 10, 2) == 5.0\n\n"
        "test_calculate_tip()\n"
        'print("Доменная логика проверена без единого виджета.")\n',
    )}
    {gui_checklist([
        "Окно открывается",
        "Все виджеты видны",
        "Порядок Tab по клавиатуре разумен",
        "Кнопка вызывает ожидаемый callback",
        "Некорректный ввод обрабатывается понятным сообщением",
        "Изменение размера окна не ломает раскладку",
        "Закрытие окна завершает процесс корректно",
        "Данные сохраняются там, где это нужно",
    ], title="Чек-лист перед тем, как считать GUI-проект готовым")}

    {practice_card("16-32", "Практика: блокирующий vs неблокирующий обработчик", "Проверяется без tkinter — на модели очереди событий", "../../practice/16-32/index.html")}
    """
    page(
        "16-32-debugging-i-kachestvo.html",
        page_title="Отладка интерфейса и качество GUI",
        description="Почему time.sleep() и while True ломают событийный цикл, что делать с по-настоящему долгими вычислениями, и чек-лист качества перед тем, как считать GUI-проект готовым.",
        kicker_suffix="Отладка и качество",
        h1="Отладка интерфейса и качество GUI",
        lede="Отзывчивость интерфейса — не автоматическое следствие использования Tkinter, а результат конкретных решений в коде.",
        body_html=body,
    )


def build_33() -> None:
    body = f"""
    <h2>Инструментарий Tkinter</h2>
    {decision_map(
        [
            ("Нужно главное окно приложения", "tk.Tk() — один на процесс"),
            ("Нужно ещё одно окно", "tk.Toplevel(root)"),
            ("Нужен тематизированный виджет формы", "ttk.Label/Button/Entry/Combobox/..."),
            ("Нужен многострочный редактор", "tk.Text / ScrolledText"),
            ("Простое вертикальное расположение", "pack()"),
            ("Форма/таблица/адаптивные колонки", "grid() + weight/sticky"),
            ("Точное позиционирование", "place() — осознанно"),
            ("Общее состояние нескольких виджетов", "StringVar/IntVar/BooleanVar/DoubleVar"),
            ("Уведомление пользователя", "messagebox"),
            ("Выбор файла", "filedialog + pathlib"),
            ("Отложенный/повторяющийся вызов без блокировки", "root.after(...)"),
            ("Персистентные настройки", "JSON + pathlib (глава 15)"),
            ("Структура крупного приложения", "класс App + мелкие callback + чистая логика"),
            ("Обработка клавиатуры/мыши напрямую", "глава 17 — .bind(...)"),
        ],
        title="Что выбрать для конкретной задачи",
    )}

    {capability_map([
        ("Событийная модель", ["mainloop() — цикл, а не заморозка", "callback ≠ command ≠ event", "function без скобок"]),
        ("Дерево виджетов", ["родитель определяет контекст", "create → configure → размещение → интерактивность"]),
        ("tk и ttk", ["ttk — тема + современные виджеты", "стиль через ttk.Style(), не fg/bg"]),
        ("Компоновка", ["pack — простые регионы", "grid + weight — адаптивные формы", "не смешивать в одном родителе"]),
        ("Ввод и состояние", ["Entry/Text, end-1c", "Tk-переменные ≠ замена Python-переменных"]),
        ("Диалоги и окна", ["messagebox/filedialog — проверяйте результат", "Toplevel, не второй Tk()"]),
        ("Отзывчивость", ["after() вместо sleep()", "долгая работа — не в одном callback"]),
        ("Архитектура", ["чистая логика отдельно от виджетов", "App HAS-A root", "настройки — через JSON главы 15"]),
    ], title="Глава 16 целиком")}

    {tree_diagram(
        ("Tkinter-приложение", [
            ("Событийная модель", [("mainloop", []), ("callback/command", [])]),
            ("Интерфейс", [("дерево виджетов", []), ("tk/ttk", []), ("pack/grid/place", [])]),
            ("Данные", [("Tk-переменные", []), ("валидация", [])]),
            ("Диалоги", [("messagebox", []), ("filedialog", []), ("Toplevel", [])]),
            ("Отзывчивость", [("after()", []), ("не sleep()", [])]),
            ("Архитектура", [("класс приложения", []), ("персистентные настройки", [])]),
        ]),
        caption="Карта главы 16 целиком.",
    )}

    <h2>Что дальше</h2>
    <p>Мы теперь умеем: строить root и дерево виджетов, связывать callback через
    <code class="inline">command</code>, компоновать формы через <code class="inline">pack</code>
    и адаптивный <code class="inline">grid</code>, хранить общее состояние в Tk-переменных,
    показывать диалоги, открывать/сохранять файлы, планировать отложенные вызовы через
    <code class="inline">after()</code> и собирать всё в класс приложения с персистентными
    настройками.</p>
    <p>В главе 17 («Проект: игра «Крестики-нолики» с Tkinter») мы построим полноценную игру — и
    познакомимся с более общим механизмом привязки событий,
    <code class="inline">.bind("&lt;Button-1&gt;", ...)</code>, который реагирует на клик в
    любом месте виджета (например, на конкретную клетку холста), а не только на предопределённое
    действие вроде <code class="inline">command</code> у кнопки.</p>

    {summary_box("Что мы узнали в этой главе", [
        "GUI-программа не выполняется строка за строкой — она ждёт события и реагирует на них через callback.",
        "<code class=\"inline\">root.mainloop()</code> запускает цикл обработки событий, а не «замирает» — программа остаётся отзывчивой.",
        "<code class=\"inline\">command=функция</code> связывает callback с виджетом — без скобок после имени функции.",
        "Каждый виджет создаётся, настраивается и отдельно размещается менеджером геометрии — <code class=\"inline\">pack()</code>, <code class=\"inline\">grid()</code> или <code class=\"inline\">place()</code>, но не смешивая pack/grid в одном родителе.",
        "ttk даёт тематизированные виджеты и стилизацию через <code class=\"inline\">ttk.Style()</code> — но не заменяет tk.Text/Canvas/Menu.",
        "Tk-переменные (StringVar и другие) связывают несколько виджетов с одним значением — и не заменяют обычные переменные Python.",
        "messagebox и filedialog возвращают реальные значения, которые нужно проверять (в том числе на отмену), а не предполагать.",
        "<code class=\"inline\">after()</code> планирует отложенный или повторяющийся вызов без блокировки — <code class=\"inline\">time.sleep()</code> в callback замораживает весь интерфейс.",
        "Доменную логику стоит писать как чистые функции, проверяемые без единого виджета — callback лишь читает ввод, вызывает логику и обновляет экран.",
        "Персистентные настройки GUI-приложения используют те же функции JSON+pathlib, что и глава 15 — ничего принципиально нового.",
    ])}
    """
    out = render_page(
        page_title="Итоги главы: инструментарий Tkinter",
        description="Итоги главы 16: полный инструментарий Tkinter — событийная модель, виджеты, компоновка, диалоги, таймеры и архитектура приложения — и мостик к главе 17.",
        depth=2,
        breadcrumb=[("Python с нуля", "../../index.html"), ("Глава 16", "index.html"), ("Итоги главы", "")],
        kicker="Глава 16 · Создаём классные приложения с Tkinter",
        h1="Итоги главы: инструментарий Tkinter",
        lede="От «программа ждёт событий, а не выполняется по порядку» до класса приложения с персистентными настройками.",
        body_html=body,
        sidebar_groups=sidebar("16-33-itogi-glavy.html"),
        nav=nav_for("16-33-itogi-glavy.html"),
    )
    write("16-33-itogi-glavy.html", out)


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
