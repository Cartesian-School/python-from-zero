#!/usr/bin/env python3
"""Строит вводные материалы: Об авторе, О техническом рецензенте, Введение."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from site_lib import NavItem, PageNav, SidebarGroup, callout, render_page

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "front-matter"

SIDEBAR = [
    SidebarGroup("Вводные материалы", [
        NavItem("Об авторе", "ob-avtore.html"),
        NavItem("О техническом рецензенте", "o-tehnicheskom-recenzente.html"),
        NavItem("Введение", "vvedenie.html"),
    ]),
    SidebarGroup("Глава 1", [
        NavItem("А вы знали?", "../chapters/glava-01/index.html"),
    ]),
]


def write(name: str, html_out: str) -> None:
    path = OUT_DIR / name
    path.write_text(html_out, encoding="utf-8")
    print(f"Записано: {path.relative_to(ROOT)}")


def build_ob_avtore() -> None:
    for i, g in enumerate(SIDEBAR):
        for it in g.items:
            it.active = it.href == "ob-avtore.html"

    body = """
    <p>Сергей Соболевски (Siergej Sobolewski) — Software &amp; AI Engineer, основатель Cartesian
    School. Эта книга выросла из практического вопроса: как объяснить программирование человеку,
    который никогда раньше не писал ни строчки кода, не превращая объяснение ни в скучный
    справочник, ни в поверхностную «книжку с картинками».</p>
    <p>Cartesian School — образовательный проект, в основе которого лежит идея, что современный
    инженерный подход и понятное объяснение для начинающих не противоречат друг другу: одно и то
    же занятие может быть одновременно точным и увлекательным.</p>
    """

    out = render_page(
        active_section="o-kurse",
        page_title="Об авторе",
        description="Об авторе книги «Python с нуля» и Cartesian School.",
        depth=1,
        breadcrumb=[("Python с нуля", "../index.html"), ("Об авторе", "")],
        kicker="Вводные материалы",
        h1="Об авторе",
        lede="",
        body_html=body,
        sidebar_groups=SIDEBAR,
        nav=PageNav(next_href="o-tehnicheskom-recenzente.html", next_label="О техническом рецензенте"),
    )
    write("ob-avtore.html", out)


def build_o_tehnicheskom_recenzente() -> None:
    for g in SIDEBAR:
        for it in g.items:
            it.active = it.href == "o-tehnicheskom-recenzente.html"

    body = (
        callout(
            "info",
            "Открытый пункт",
            "Имя технического рецензента будет добавлено сюда после того, как Product Owner "
            "назначит рецензента издания. Раздел сохранён по канонической структуре оглавления "
            "и не удалён — при этом мы не стали придумывать несуществующего человека.",
        )
        + """
    <p>Каждая глава этой книги проходит техническую проверку: весь код автоматически
    компилируется, проверяется линтером <code class="inline">ruff</code>, а примеры в формате
    Jupyter Notebook реально выполняются от начала до конца — результаты вычислений в тексте
    книги получены не «на глаз», а настоящим запуском кода на Python 3.14.</p>
    """
    )

    out = render_page(
        active_section="o-kurse",
        page_title="Статус технической проверки",
        description="Автоматическая верификация кода книги; независимый технический рецензент пока не назначен.",
        depth=1,
        breadcrumb=[("Python с нуля", "../index.html"), ("О техническом рецензенте", "")],
        kicker="Вводные материалы",
        h1="Статус технической проверки",
        lede="",
        body_html=body,
        sidebar_groups=SIDEBAR,
        nav=PageNav(prev_href="ob-avtore.html", prev_label="Об авторе", next_href="vvedenie.html", next_label="Введение"),
    )
    write("o-tehnicheskom-recenzente.html", out)


def build_vvedenie() -> None:
    for g in SIDEBAR:
        for it in g.items:
            it.active = it.href == "vvedenie.html"

    body = """
    <h2>Для кого эта книга</h2>
    <p>Эта книга — для тех, кто раньше не писал код. Совсем. Неважно, сколько вам лет: десять,
    двадцать пять или пятьдесят — если вы умеете пользоваться компьютером и готовы разбираться,
    книга проведёт вас от первой напечатанной строки до собственных игр, приложений и рисунков
    на экране.</p>

    <h2>Как устроена каждая глава</h2>
    <p>Почти в каждом разделе вы встретите один и тот же порядок: сначала — зачем это нужно,
    затем — простое объяснение идеи, потом — рабочий пример, который можно запустить прямо
    сейчас, и в конце — практика и типичные ошибки. Мы намеренно не начинаем с сухого
    определения — сначала должно быть понятно, зачем оно вам, а термин появится следом.</p>

    <h2>Классический подход и современный Python 3.14</h2>
    <p>Python существует больше тридцати лет, и за это время в языке появлялись более удобные
    способы делать привычные вещи. Там, где это важно, книга сначала показывает классический
    приём — потому что именно его вы встретите в старом коде, статьях и ответах на форумах — а
    затем современный вариант для Python 3.14 и объясняет, чем они отличаются и что использовать
    сегодня. Это отмечено специальным блоком «Классический подход → современный Python».</p>

    <h2>Теория на сайте, практика в Jupyter Notebook</h2>
    <p>Теорию вы читаете здесь, на сайте Cartesian School — с подсветкой кода, поиском и
    навигацией. А для практики к каждому разделу прилагается отдельный файл Jupyter Notebook: в
    нём можно менять код и сразу видеть результат, не открывая ничего дополнительного, кроме
    Visual Studio Code или PyCharm.</p>

    <h2>Уровни сложности практики</h2>
    <p>Задания отмечены звёздами: <strong>★</strong> — базовая практика, повторяющая пример из
    раздела; <strong>★★</strong> — самостоятельная задача, требующая немного подумать;
    <strong>★★★</strong> — задача повышенной сложности для тех, кто хочет большего. Не в каждом
    разделе есть все три уровня — только там, где это оправдано.</p>

    <h2>Что понадобится</h2>
    <p>Python 3.14, установленный по инструкции из главы 2, и один из двух редакторов кода:
    Visual Studio Code или PyCharm — оба подробно описаны в книге. Больше почти ничего не нужно:
    все проекты в этой книге можно запустить на обычном ноутбуке.</p>
    """

    out = render_page(
        active_section="o-kurse",
        page_title="Введение",
        description="Как устроена книга «Python с нуля» и как её читать.",
        depth=1,
        breadcrumb=[("Python с нуля", "../index.html"), ("Введение", "")],
        kicker="Вводные материалы",
        h1="Введение",
        lede="Коротко о том, как устроена эта книга и как получить от неё максимум.",
        body_html=body,
        sidebar_groups=SIDEBAR,
        nav=PageNav(prev_href="o-tehnicheskom-recenzente.html", prev_label="О техническом рецензенте", next_href="../chapters/glava-01/index.html", next_label="Глава 1: А вы знали?"),
    )
    write("vvedenie.html", out)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    build_ob_avtore()
    build_o_tehnicheskom_recenzente()
    build_vvedenie()
