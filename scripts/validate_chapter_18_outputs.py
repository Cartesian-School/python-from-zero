#!/usr/bin/env python3
"""Проверяет, что все скриншоты, ожидаемые главой 18, существуют в
site/assets/img/chapter-18/output/, не пустые и не случайный снимок 1×1.

Использование: python3 scripts/validate_chapter_18_outputs.py
"""

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-18" / "output"

REQUIRED_NAMES = [
    "paint-pro-final",
    "empty-canvas",
    "canvas-coordinate-demo",
    "toolbar-tools",
    "tool-pencil-selected",
    "tool-line-selected",
    "mouse-press-start",
    "mouse-drag-preview-line",
    "line-final",
    "rectangle-preview",
    "rectangle-final",
    "oval-preview",
    "oval-final",
    "freehand-naive-dots",
    "freehand-connected-stroke",
    "width-comparison",
    "color-palette",
    "custom-color-result",
    "multiple-shapes",
    "stacking-order-before",
    "stacking-order-after",
    "eraser-before",
    "eraser-after",
    "undo-before",
    "undo-after",
    "redo-after",
    "status-bar",
    "saved-document",
    "loaded-document",
    "resized-window",
]

MIN_DIMENSION = 40  # anything smaller is almost certainly a capture bug, not a real window

# Pairs where the second name must show visible change from the first —
# a validator catching "before == after" (nothing actually happened) bugs.
BEFORE_AFTER_PAIRS = [
    ("stacking-order-before", "stacking-order-after"),
    ("eraser-before", "eraser-after"),
    ("undo-before", "undo-after"),
]


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
        except Exception as exc:  # noqa: BLE001 - report and keep validating the rest
            errors.append(f"Не удалось открыть {path.relative_to(ROOT)}: {exc}")
            continue
        if width < MIN_DIMENSION or height < MIN_DIMENSION:
            errors.append(f"{path.relative_to(ROOT)}: подозрительно маленький снимок {width}x{height}")
    errors.extend(_validate_before_after_pairs())
    errors.extend(_validate_resize_pair())
    return errors


def _validate_before_after_pairs() -> list[str]:
    errors = []
    for before_name, after_name in BEFORE_AFTER_PAIRS:
        before_path, after_path = OUT_DIR / f"{before_name}.png", OUT_DIR / f"{after_name}.png"
        if not before_path.exists() or not after_path.exists():
            continue  # already reported as missing above
        with Image.open(before_path) as before_img, Image.open(after_path) as after_img:
            before_bytes, after_bytes = before_img.convert("RGB").tobytes(), after_img.convert("RGB").tobytes()
        if before_bytes == after_bytes:
            errors.append(
                f"{after_name}.png идентичен {before_name}.png — действие (Undo/Ластик/tag_raise) "
                f"должно быть видно на экране, а не только в данных."
            )
    return errors


def _validate_resize_pair() -> list[str]:
    """18-31 Debug Lab 15 claims a resized window keeps the same drawing —
    but the CANVAS itself must genuinely be bigger, or the screenshot proves
    nothing about the lesson it illustrates."""
    resized_path = OUT_DIR / "resized-window.png"
    if not resized_path.exists():
        return []
    with Image.open(resized_path) as img:
        w, h = img.size
    if w < 700 or h < 500:
        return [f"resized-window.png ({w}x{h}) не выглядит увеличенным окном — ожидались большие размеры."]
    return []


def main() -> None:
    errors = validate()
    if errors:
        print(f"Скриншоты главы 18 невалидны — найдено ошибок: {len(errors)}\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    print(f"Скриншоты главы 18 валидны: {len(REQUIRED_NAMES)} файлов проверено.")


if __name__ == "__main__":
    main()
