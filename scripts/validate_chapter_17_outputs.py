#!/usr/bin/env python3
"""Проверяет, что все скриншоты, ожидаемые главой 17, существуют в
site/assets/img/chapter-17/output/, не пустые и не случайный снимок 1×1.

Использование: python3 scripts/validate_chapter_17_outputs.py
"""

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-17" / "output"

REQUIRED_NAMES = [
    "basic-empty-board",
    "basic-first-move",
    "basic-win",
    "basic-draw",
    "basic-new-game-reset",
    "empty-board",
    "x-first-move",
    "x-turn",
    "o-turn",
    "mid-game",
    "x-win",
    "o-win",
    "winning-highlight",
    "draw",
    "hover-preview-x",
    "hover-preview-o",
    "scoreboard",
    "new-round",
    "tic-tac-toe-pro",
]

MIN_DIMENSION = 40  # anything smaller is almost certainly a capture bug, not a real window


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
    return errors


def main() -> None:
    errors = validate()
    if errors:
        print(f"Скриншоты главы 17 невалидны — найдено ошибок: {len(errors)}\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    print(f"Скриншоты главы 17 валидны: {len(REQUIRED_NAMES)} файлов проверено.")


if __name__ == "__main__":
    main()
