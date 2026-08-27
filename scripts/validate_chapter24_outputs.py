#!/usr/bin/env python3
"""Validate Chapter 24's generated pedagogical and publication contracts."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_chapter_24 import PAGES
from chapter_metadata import chapter

ROOT = Path(__file__).resolve().parent.parent
CHAPTER_DIR = ROOT / "site" / "chapters" / "glava-24"
CANONICAL_TITLE = "Что дальше? Roadmap Python-разработчика"
EXPECTED_FILES = {
    "index.html",
    "24-01-chego-vy-dostigli.html",
    "24-02-pervye-30-dnej.html",
    "24-03-professional-python-core.html",
    "24-04-software-engineering.html",
    "24-05-kak-vybrat-napravlenie.html",
    "24-06-backend-roadmap.html",
    "24-07-data-ml-ai-roadmap.html",
    "24-08-automation-devops-roadmap.html",
    "24-09-desktop-roadmap.html",
    "24-10-game-development-roadmap.html",
    "24-11-portfolio.html",
    "24-12-open-source.html",
    "24-13-kak-uchitsya-dalshe.html",
    "24-14-sleduyushchie-kursy.html",
    "24-15-vash-sleduyushchij-shag.html",
}
FUTURE_COURSES = {
    "Advanced Python",
    "Python Backend Developer",
    "Python Testing & Software Engineering",
    "Python for Data & AI",
    "Python Automation & DevOps",
}


@dataclass
class Element:
    """Minimal element record for portable generated-HTML validation."""

    tag: str
    attrs: dict[str, str]
    text_parts: list[str] = field(default_factory=list)
    descendant_tags: set[str] = field(default_factory=set)

    @property
    def text(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.text_parts)).strip()

    def has_class(self, name: str) -> bool:
        return name in self.attrs.get("class", "").split()


class ContractHTMLParser(HTMLParser):
    """Collect only the element contracts needed by this validator."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.elements: list[Element] = []
        self.stack: list[Element] = []
        self.document_text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for ancestor in self.stack:
            ancestor.descendant_tags.add(tag)
        element = Element(tag=tag, attrs={key: value or "" for key, value in attrs})
        self.elements.append(element)
        self.stack.append(element)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for ancestor in self.stack:
            ancestor.descendant_tags.add(tag)
        self.elements.append(
            Element(tag=tag, attrs={key: value or "" for key, value in attrs})
        )

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data: str) -> None:
        self.document_text_parts.append(data)
        for element in self.stack:
            element.text_parts.append(data)

    @property
    def text(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.document_text_parts)).strip()

    def find_all(self, tag: str, **attrs: str) -> list[Element]:
        return [
            element
            for element in self.elements
            if element.tag == tag
            and all(element.attrs.get(key) == value for key, value in attrs.items())
        ]


def parse_html(source: str) -> ContractHTMLParser:
    parser = ContractHTMLParser()
    parser.feed(source)
    parser.close()
    return parser


def require_tokens(text: str, tokens: list[str], context: str, errors: list[str]) -> None:
    for token in tokens:
        if token not in text:
            errors.append(f"{context}: missing required content {token!r}")


def main() -> None:
    errors: list[str] = []
    if chapter(24).title != CANONICAL_TITLE:
        errors.append(f"canonical Chapter 24 title is {chapter(24).title!r}")
    if len(PAGES) != 16 or {name for name, _title in PAGES} != EXPECTED_FILES:
        errors.append("PAGES must describe exactly the canonical 16-page Chapter 24 set")
    if PAGES[1][1] != "Чего Вы достигли!":
        errors.append("24.1 title must be exactly 'Чего Вы достигли!'")

    actual_files = {path.name for path in CHAPTER_DIR.glob("*.html")}
    if actual_files != EXPECTED_FILES:
        errors.append(f"generated HTML set differs: missing={EXPECTED_FILES - actual_files}, extra={actual_files - EXPECTED_FILES}")
    stale = {
        "24-01-idei-mini-proektov.html",
        "24-02-idei-itogovyh-proektov.html",
        "24-03-chto-izuchat-dalshe-itogi.html",
    } & actual_files
    if stale:
        errors.append(f"stale four-page Chapter 24 routes remain: {sorted(stale)}")

    html_by_name: dict[str, str] = {}
    for filename, title in PAGES:
        path = CHAPTER_DIR / filename
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        html_by_name[filename] = text
        document = parse_html(text)
        if CANONICAL_TITLE not in text:
            errors.append(f"{filename}: canonical chapter title is not visible in generated metadata/navigation")
        if filename == "index.html":
            section_links = [
                element
                for element in document.find_all("a")
                if element.has_class("section-item")
            ]
            if len(section_links) != 15:
                errors.append(f"index.html: expected 15 section links, got {len(section_links)}")
        else:
            headings = document.find_all("h1")
            if len(headings) != 1 or headings[0].text != title:
                errors.append(f"{filename}: h1 does not match PAGES title {title!r}")
            active = [
                element
                for element in document.find_all("a", href=filename)
                if element.has_class("active")
            ]
            if len(active) != 1:
                errors.append(f"{filename}: own sidebar route must be active exactly once")
            for expected_href, _expected_title in PAGES:
                if not document.find_all("a", href=expected_href):
                    errors.append(f"{filename}: sidebar/navigation omits {expected_href}")
                    break

        for anchor in [
            element
            for element in document.find_all("a")
            if "data-chapter-ref" in element.attrs
        ]:
            number = int(anchor.attrs["data-chapter-ref"])
            target = chapter(number)
            if target.title not in anchor.text:
                errors.append(f"{filename}: chapter {number} cross-reference does not use canonical title")
            expected_href = f"../glava-{number:02d}/index.html"
            if anchor.attrs.get("href") != expected_href:
                errors.append(f"{filename}: chapter {number} cross-reference has wrong route")

    combined = "\n".join(html_by_name.values())
    require_tokens(combined, [
        'print("Привет!")', "переменные", "Условия и циклы", "Коллекции и функции",
        "Классы, файлы, исключения", "Turtle", "Tkinter", "Pygame", "Flask",
        "Git", "GitHub", "Issues", "Projects", "Issue", "Pull Request", "CI", "pyproject.toml", "релиз",
        "Professional Python Core", "Software Engineering", "Backend", "Data Science, ML и AI",
        "Automation и DevOps", "Desktop", "Game Development", "Open Source", "tutorial hell",
        "Tutorial", "How-to", "Reference", "Explanation",
    ], "chapter", errors)

    require_tokens(html_by_name.get("24-02-pervye-30-dnej.html", ""), [
        "Конвертер валют", "Гонка в Pygame", "Вариации узоров Turtle", "Змейка на Pygame",
        "Игра на память", "Игра на уклонение", "Идея:", "Минимальная версия:",
        "Расширения:", "Что закрепляет:", "не претендует", "универсальный",
    ], "24.2", errors)
    require_tokens(html_by_name.get("24-03-professional-python-core.html", ""), [
        "Comprehensions", "unpacking", "slicing", "Iterable", "iterator", "generator",
        "Closures", "decorators", "context managers", "dataclasses", "enums", "generics",
        "Protocol", "collections", "datetime", "pathlib", "json", "re", "asyncio",
        "First-class", "Iterator", "Generators",
    ], "24.3", errors)
    require_tokens(html_by_name.get("24-04-software-engineering.html", ""), [
        "fixtures", "parametrize", "mock", "coverage", "Ruff", "mypy", "logging",
        "Профилировщик", "PyPI", "Semantic Versioning", "HTTP", "SQL", "Linux", "CI/CD", "CONTAINERS",
    ], "24.4", errors)
    require_tokens(html_by_name.get("24-06-backend-roadmap.html", ""), [
        "Python Core", "HTTP", "API contract", "Framework", "Database", "Deployment",
    ], "24.6", errors)
    require_tokens(html_by_name.get("24-07-data-ml-ai-roadmap.html", ""), [
        "NumPy", "pandas", "Statistics", "ML baseline", "Evaluation", "PyTorch",
    ], "24.7", errors)

    automation_text = html_by_name.get("24-08-automation-devops-roadmap.html", "")
    if automation_text.count("argparse или другой parser") != 1:
        errors.append("24.8: CLI roadmap row must appear exactly once")

    desktop_document = parse_html(html_by_name.get("24-09-desktop-roadmap.html", ""))
    if not desktop_document.find_all("a", **{"data-chapter-ref": "16"}):
        errors.append("24.9: Tkinter prerequisite must reference Chapter 16")

    require_tokens(html_by_name.get("24-11-portfolio.html", ""), [
        "Учебные повторы", "Инженерное портфолио", "README", "постановкой проблемы",
        "Снимки экрана", "демонстрацию", "Воспроизводимую установку", "Архитектурную схему", "Тесты",
        "Историю Git", "Issues", "CI", "релиз", "LICENSE", "документацию",
    ], "24.11", errors)
    require_tokens(html_by_name.get("24-12-open-source.html", ""), [
        "Выберите проект", "Прочитайте README", "Прочитайте CONTRIBUTING", "Выберите Issue",
        "Воспроизведите", "Создайте fork или branch", "Внесите изменение", "Выполните тесты",
        "Откройте Pull Request", "Пройдите review", "Внесите исправления", "Лицензии",
    ], "24.12", errors)
    require_tokens(html_by_name.get("24-13-kak-uchitsya-dalshe.html", ""), [
        "официальной документации", "Tutorial", "explanation", "how-to", "reference",
        "исходный код", "issue tracker", "примечания к релизу",
    ], "24.13", errors)

    future_document = parse_html(html_by_name.get("24-14-sleduyushchie-kursy.html", ""))
    cards = [
        element
        for element in future_document.find_all("article")
        if "data-future-course" in element.attrs
    ]
    found_courses = {card.attrs.get("data-future-course") for card in cards}
    if found_courses != FUTURE_COURSES:
        errors.append(f"24.14: future course set differs: {found_courses}")
    for card in cards:
        status = card.attrs.get("data-course-status")
        if status not in {"Скоро", "Готовится"}:
            errors.append(f"24.14: invalid status {status!r}")
        if status not in card.text:
            errors.append(f"24.14: status {status!r} is not visible text")
        if "a" in card.descendant_tags:
            errors.append(
                f"24.14: future course {card.attrs.get('data-future-course')} has a fake link"
            )
    if re.search(
        r"(?i)(записаться|купить курс|оплатить|enroll|checkout)",
        future_document.text,
    ):
        errors.append("24.14: fake enrollment or purchase wording found")
    require_tokens(future_document.text, [
        "декораторы", "контекстные менеджеры", "статическая типизация",
        "сборка пакетов", "контейнеры", "наблюдаемость",
    ], "24.14", errors)

    final_text = html_by_name.get("24-15-vash-sleduyushchij-shag.html", "")
    closing = "Книга закончилась. Ваш roadmap — нет."
    if final_text.count(closing) != 1 or 'data-course-closing="true"' not in final_text:
        errors.append("24.15: exact final course line must appear once in the closing block")
    require_tokens(final_text, [
        'data-final-question="true"', "Теперь вопрос уже не:", "«Смогу ли я программировать?»",
        "Следующий вопрос:", "«Каким Python-разработчиком я хочу стать?»",
    ], "24.15", errors)

    if 'class="exercise' in combined or "Базовая практика" in combined:
        errors.append("Chapter 24 must not add graded exercises")
    if combined.count('role="img"') < 10:
        errors.append("Chapter 24 must contain at least 10 semantic roadmap diagrams")
    for match in re.finditer(r'<svg[^>]*role="img"[^>]*>', combined):
        if "aria-label=" not in match.group(0):
            errors.append("roadmap SVG lacks an aria-label")
            break

    if errors:
        print(f"Chapter 24 output validation failed: {len(errors)} problem(s)", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        raise SystemExit(1)

    print(
        "Chapter 24 outputs OK: 16 canonical pages, dependency-aware roadmap, "
        "five honest future-course cards, no fake enrollment, exact finale."
    )


if __name__ == "__main__":
    main()
