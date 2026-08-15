#!/usr/bin/env python3
"""Строит «Предметный указатель» (site/predmetnyj-ukazatel.html).

Каждый термин ссылается на страницу главы, где он рассматривается, и указывает
канонический номер страницы (соответствует manifest/coverage_manifest.json).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_lib import NavItem, PageNav, SidebarGroup, render_page

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "site" / "predmetnyj-ukazatel.html"

# (термин, номер главы, каноническая страница, необязательное примечание)
SYMBOLS_LATIN = [
    ("break и continue", 10, 207, None),
    ("CSS", 22, 502, None),
    ("Entry (поле ввода Tkinter)", 16, 348, None),
    ("eval(), безопасное вычисление выражений", 23, 511, None),
    ("f-строки (f-strings)", 8, 157, None),
    ("Flask", 22, 507, None),
    ("for, цикл", 10, 197, None),
    ("grid, менеджер компоновки Tkinter", 16, 363, None),
    ("HTML", 22, 499, None),
    ("HTTP, протокол передачи данных", 22, 497, None),
    ("IDLE", 3, 33, None),
    ("if / elif / else", 9, 180, None),
    ("Jinja2, шаблоны Flask", 22, 507, None),
    ("pack, менеджер компоновки Tkinter", 16, 342, None),
    ("PyCharm", 3, 27, None),
    ("Pygame", 20, 445, None),
    ("Radiobutton (Tkinter)", 23, 531, None),
    ("random, модуль", 5, 75, None),
    ("range()", 10, 197, None),
    ("Rect, pygame.Rect", 21, 471, None),
    ("StringVar (Tkinter)", 16, 355, None),
    ("Tkinter", 16, 335, None),
    ("Turtle", 6, 83, None),
    ("VS Code", 3, 27, None),
    ("while, цикл", 10, 205, None),
]

CYRILLIC = [
    ("Аргументы функции", 13, 291, None),
    ("Атрибуты объекта", 14, 315, None),
    ("Булевы значения (True/False)", 9, 175, None),
    ("Ввод данных, input()", 8, 161, None),
    ("Вложенные циклы", 10, 201, None),
    ("Возврат значения, return", 13, 292, None),
    ("Глобальные переменные", 13, 299, None),
    ("Декоратор (например, @app.route)", 22, 507, None),
    ("Дуги (Turtle)", 7, 114, None),
    ("Замыкания и позднее связывание", 17, 376, None),
    ("Индексация строк", 8, 145, None),
    ("Классы и объекты", 14, 314, None),
    ("Конкатенация строк", 8, 143, None),
    ("Кортежи (tuple)", 11, 240, None),
    ("Локальные переменные", 13, 298, None),
    ("Лямбда-функции", 13, 301, None),
    ("Массивы", 11, 225, "см. «Списки»"),
    ("Методы строк", 8, 149, None),
    ("Множества (set)", 11, 244, None),
    ("Модули, импорт", 20, 446, None),
    ("Наследование классов", 24, 542, "кратко упомянуто как направление дальнейшего изучения"),
    ("Обработка ошибок (try/except)", 23, 511, "пример использования"),
    ("Объектно-ориентированное программирование (ООП)", 14, 312, None),
    ("Операторы сравнения", 9, 179, None),
    ("Отрицательные индексы", 8, 147, None),
    ("Параметры функции", 13, 288, None),
    ("Переменные", 4, 40, None),
    ("Приоритет операций", 5, 67, None),
    ("Регулярные выражения", 24, 542, "не рассматриваются подробно — направление для дальнейшего изучения"),
    ("Свойства объекта", 14, 315, "см. «Атрибуты объекта»"),
    ("Словари (dict)", 11, 247, None),
    ("Случайные числа", 5, 75, None),
    ("События (events)", 17, 369, None),
    ("Списки (list)", 11, 225, None),
    ("Срезы списков", 11, 227, None),
    ("Срезы строк", 8, 148, None),
    ("Строки (str)", 8, 137, None),
    ("Столкновения объектов (collision)", 19, 434, None),
    ("Таблица истинности (and/or/not)", 9, 184, None),
    ("Файлы, чтение и запись", 15, 323, None),
    ("Форматирование строк", 8, 157, None),
    ("Функции", 13, 283, None),
    ("Целые и дробные числа", 4, 47, None),
    ("Циклы", 10, 195, None),
    ("Черепашья графика", 6, 83, "см. «Turtle»"),
]


def chapter_href(num: int) -> str:
    return f"chapters/glava-{num:02d}/index.html"


def render_entries(entries):
    rows = []
    for term, chapter_num, page, note in sorted(entries, key=lambda e: e[0].lower()):
        note_html = f' <span class="idx-note">({note})</span>' if note else ""
        rows.append(
            f'<li class="idx-entry"><span class="idx-term">'
            f'<a href="{chapter_href(chapter_num)}">{term}</a>{note_html}</span>'
            f'<span class="idx-page">стр. {page}</span></li>'
        )
    return "".join(rows)


def build() -> None:
    body = f"""
    <p>Термины отсортированы по алфавиту. Номер страницы соответствует канонической
    вёрстке книги; ссылка ведёт на страницу главы, где термин рассматривается.</p>

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
        description="Алфавитный указатель терминов книги «Python с нуля» с номерами страниц.",
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
