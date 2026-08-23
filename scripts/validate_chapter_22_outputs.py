#!/usr/bin/env python3
"""Проверяет, что все скриншоты, ожидаемые главой 22, существуют в
site/assets/img/chapter-22/output/, не пустые, не случайный снимок 1x1 и не
однотонная заливка одним цветом.

Использование: python3 scripts/validate_chapter_22_outputs.py
"""

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-22" / "output"

REQUIRED_NAMES = [
    "01-raw-html",
    "02-html-css",
    "03-js-before-click",
    "04-js-after-click",
    "05-flask-todo-final",
    "06-flask-privet",
    "07-api-tasks-json",
    "08-todo-empty",
    "09-todo-after-add",
    "10-todo-completed",
    "11-todo-validation-error",
    "12-todo-persisted-after-restart",
]

MIN_DIMENSION = 20

BEFORE_AFTER_PAIRS = [
    ("01-raw-html", "02-html-css"),
    ("03-js-before-click", "04-js-after-click"),
    ("08-todo-empty", "09-todo-after-add"),
    ("09-todo-after-add", "10-todo-completed"),
    ("10-todo-completed", "12-todo-persisted-after-restart"),
]


def _is_blank(img: Image.Image) -> bool:
    """True, если изображение — сплошная заливка одним цветом (значит,
    страница не отрисовалась, а не то, что она действительно так выглядит)."""
    extrema = img.convert("RGB").getextrema()
    return all(lo == hi for lo, hi in extrema)


def validate() -> list[str]:
    errors = []
    for name in REQUIRED_NAMES:
        path = OUT_DIR / f"{name}.png"
        if not path.exists():
            errors.append(f"Отсутствует обязательный скриншот: {path.relative_to(ROOT)}")
            continue
        try:
            with Image.open(path) as img:
                width, height = img.size
                if _is_blank(img):
                    errors.append(f"{path.relative_to(ROOT)}: изображение выглядит как сплошная заливка")
        except Exception as exc:  # noqa: BLE001 - report and keep validating the rest
            errors.append(f"Не удалось открыть {path.relative_to(ROOT)}: {exc}")
            continue
        if width < MIN_DIMENSION or height < MIN_DIMENSION:
            errors.append(f"{path.relative_to(ROOT)}: подозрительно маленький снимок {width}x{height}")

    errors.extend(_validate_before_after_pairs())
    errors.extend(_validate_no_accidental_duplicates())
    errors.extend(_validate_embedded_in_pages())
    return errors


def _validate_before_after_pairs() -> list[str]:
    errors = []
    for before_name, after_name in BEFORE_AFTER_PAIRS:
        before_path, after_path = OUT_DIR / f"{before_name}.png", OUT_DIR / f"{after_name}.png"
        if not before_path.exists() or not after_path.exists():
            continue
        with Image.open(before_path) as before_img, Image.open(after_path) as after_img:
            before_bytes = before_img.convert("RGB").resize((64, 64)).tobytes()
            after_bytes = after_img.convert("RGB").resize((64, 64)).tobytes()
        if before_bytes == after_bytes:
            errors.append(
                f"{after_name}.png визуально идентичен {before_name}.png — изменение должно быть "
                f"видно на экране, а не только предполагаться."
            )
    return errors


def _validate_no_accidental_duplicates() -> list[str]:
    errors = []
    seen: dict[bytes, str] = {}
    for name in REQUIRED_NAMES:
        path = OUT_DIR / f"{name}.png"
        if not path.exists():
            continue
        with Image.open(path) as img:
            content = img.convert("RGB").tobytes()
        if content in seen:
            errors.append(f"{name}.png побайтово идентичен {seen[content]}.png — вероятно, случайный дубликат.")
        else:
            seen[content] = name
    return errors


def _validate_embedded_in_pages() -> list[str]:
    """Каждый обязательный скриншот должен быть вставлен хотя бы на одной
    странице главы 22 — иначе это осиротевший файл, который никто не видит."""
    errors = []
    chapter_dir = ROOT / "site" / "chapters" / "glava-22"
    combined_html = "\n".join(p.read_text(encoding="utf-8") for p in chapter_dir.glob("*.html"))
    for name in REQUIRED_NAMES:
        if f"{name}.png" not in combined_html:
            errors.append(f"{name}.png не встречается ни на одной странице главы 22 (осиротевший файл)")
    return errors


def main() -> None:
    errors = validate()
    if errors:
        print(f"Скриншоты главы 22 невалидны — найдено ошибок: {len(errors)}\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    print(f"Скриншоты главы 22 валидны: {len(REQUIRED_NAMES)} файлов проверено.")


if __name__ == "__main__":
    main()
