#!/usr/bin/env python3
"""Строит «Предметный указатель» (site/predmetnyj-ukazatel.html).

Каждый термин ссылается на главу, где он рассматривается. Точные физические
страницы намеренно не дублируются: без отдельного якоря термина число было бы
неточным; каноническая пагинация живёт в data/book-pagination.json.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_lib import NavItem, PageNav, SidebarGroup, render_page

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "predmetnyj-ukazatel.html"

# (термин, номер главы, необязательное примечание)
SYMBOLS_LATIN = [
    ("break и continue", 10, None),
    ("CSS", 22, None),
    ("Entry (поле ввода Tkinter)", 16, None),
    ("eval(), безопасное вычисление выражений", 23, None),
    ("f-строки (f-strings)", 8, None),
    ("Flask", 22, None),
    ("for, цикл", 10, None),
    ("grid, менеджер компоновки Tkinter", 16, None),
    ("HTML", 22, None),
    ("HTTP, протокол передачи данных", 22, None),
    ("IDLE", 3, None),
    ("if / elif / else", 9, None),
    ("Jinja2, шаблоны Flask", 22, None),
    ("pack, менеджер компоновки Tkinter", 16, None),
    ("PyCharm", 3, None),
    ("Pygame", 20, None),
    ("Radiobutton (Tkinter)", 23, None),
    ("random, модуль", 5, None),
    ("range()", 10, None),
    ("Rect, pygame.Rect", 21, None),
    ("StringVar (Tkinter)", 16, None),
    ("Tkinter", 16, None),
    ("Turtle", 6, None),
    ("VS Code", 3, None),
    ("while, цикл", 10, None),
]

CYRILLIC = [
    ("Аргументы функции", 13, None),
    ("Атрибуты объекта", 14, None),
    ("Булевы значения (True/False)", 9, None),
    ("Ввод данных, input()", 8, None),
    ("Вложенные циклы", 10, None),
    ("Возврат значения, return", 13, None),
    ("Глобальные переменные", 13, None),
    ("Декоратор (например, @app.route)", 22, None),
    ("Дуги (Turtle)", 7, None),
    ("Замыкания и позднее связывание", 17, None),
    ("Индексация строк", 8, None),
    ("Классы и объекты", 14, None),
    ("Конкатенация строк", 8, None),
    ("Кортежи (tuple)", 11, None),
    ("Локальные переменные", 13, None),
    ("Лямбда-функции", 13, None),
    ("Массивы", 11, "см. «Списки»"),
    ("Методы строк", 8, None),
    ("Множества (set)", 11, None),
    ("Модули, импорт", 20, None),
    ("Наследование классов", 24, "кратко упомянуто как направление дальнейшего изучения"),
    ("Обработка ошибок (try/except)", 23, "пример использования"),
    ("Объектно-ориентированное программирование (ООП)", 14, None),
    ("Операторы сравнения", 9, None),
    ("Отрицательные индексы", 8, None),
    ("Параметры функции", 13, None),
    ("Переменные", 4, None),
    ("Приоритет операций", 5, None),
    ("Регулярные выражения", 24, "не рассматриваются подробно — направление для дальнейшего изучения"),
    ("Свойства объекта", 14, "см. «Атрибуты объекта»"),
    ("Словари (dict)", 11, None),
    ("Случайные числа", 5, None),
    ("События (events)", 17, None),
    ("Списки (list)", 11, None),
    ("Срезы списков", 11, None),
    ("Срезы строк", 8, None),
    ("Строки (str)", 8, None),
    ("Столкновения объектов (collision)", 19, None),
    ("Таблица истинности (and/or/not)", 9, None),
    ("Файлы, чтение и запись", 15, None),
    ("Форматирование строк", 8, None),
    ("Функции", 13, None),
    ("Целые и дробные числа", 4, None),
    ("Циклы", 10, None),
    ("Черепашья графика", 6, "см. «Turtle»"),
]


def chapter_href(num: int) -> str:
    return f"chapters/glava-{num:02d}/index.html"


def render_entries(entries):
    rows = []
    for term, chapter_num, note in sorted(entries, key=lambda e: e[0].lower()):
        note_html = f' <span class="idx-note">({note})</span>' if note else ""
        rows.append(
            f'<li class="idx-entry"><span class="idx-term">'
            f'<a href="{chapter_href(chapter_num)}">{term}</a>{note_html}</span>'
            f'<span class="idx-page">глава {chapter_num}</span></li>'
        )
    return "".join(rows)


def build() -> None:
    body = f"""
    <p>Термины отсортированы по алфавиту. Ссылка ведёт на главу, где термин
    рассматривается.</p>

    <h2>Символы и англоязычные термины</h2>
    <ul class="idx-list">{render_entries(SYMBOLS_LATIN)}</ul>

    <h2>А—Я</h2>
    <ul class="idx-list">{render_entries(CYRILLIC)}</ul>
    """

    sidebar_groups = [
        SidebarGroup("Справочник", [
            NavItem("Введение", "front-matter/vvedenie.html"),
            NavItem("Об авторе", "front-matter/ob-avtore.html"),
            NavItem("О техническом рецензенте", "front-matter/o-tehnicheskom-recenzente.html"),
            NavItem("Предметный указатель", "predmetnyj-ukazatel.html", active=True),
        ]),
    ]

    out = render_page(
        active_section="spravochnik",
        page_title="Предметный указатель",
        description="Алфавитный указатель терминов книги «Python с нуля» по главам.",
        depth=0,
        breadcrumb=[("Python с нуля", "index.html"), ("Предметный указатель", "")],
        kicker="Справочник",
        h1="Предметный указатель",
        lede="Быстрый способ найти, в какой главе рассматривается нужный термин.",
        body_html=body,
        sidebar_groups=sidebar_groups,
        nav=PageNav(prev_href="chapters/glava-24/24-03-chto-izuchat-dalshe-itogi.html", prev_label="Глава 24: Что дальше?", next_href=None, next_label=None),
    )
    OUT.write_text(out, encoding="utf-8")
    print(f"Записано: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
