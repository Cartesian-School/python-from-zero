#!/usr/bin/env python3
"""Проверяет, что все скриншоты, ожидаемые главой 20, существуют в
site/assets/img/chapter-20/output/, не пустые и не случайный снимок 1×1.

Использование: python3 scripts/validate_chapter_20_outputs.py
"""

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-20" / "output"

REQUIRED_NAMES = [
    "pygame-first-window",
    "game-loop-square",
    "characters-shapes",
    "three-enemies",
    "movement-before",
    "movement-mid",
    "movement-after",
    "bouncing-ball-basic-1",
    "bouncing-ball-basic-2",
    "bouncing-ball-basic-3",
    "virtual-controls-mockup",
    "safe-area-demo",
    "surface-blit-demo",
    "surface-alpha-demo",
    "collision-overlap",
    "collision-no-overlap",
    "hitbox-vs-art",
    "gravity-fall-1",
    "gravity-fall-2",
    "gravity-fall-3",
    "animation-frame-1",
    "animation-frame-2",
    "animation-frame-3",
    "animation-frame-4",
    "debug-missing-fill-trail",
    "game-states-menu",
    "game-states-playing",
    "game-states-paused",
    "game-states-game-over",
    "bouncing-ball-pro-hud",
    "bouncing-ball-pro-paused",
]

REQUIRED_COMPOSITES = [
    "movement-strip",
    "bouncing-ball-basic-strip",
    "gravity-fall-strip",
    "animation-strip",
    "game-states-strip",
]

MIN_DIMENSION = 40
MIN_STRIP_WIDTH = 700
MAX_STRIP_WIDTH = 820  # компактность — полоса не должна раздувать вес страницы

# Пары, где второе имя обязано визуально отличаться от первого — иначе кадр
# на самом деле не изменился между "до" и "после".
BEFORE_AFTER_PAIRS = [
    ("movement-before", "movement-after"),
    ("gravity-fall-1", "gravity-fall-3"),
    ("game-states-menu", "game-states-playing"),
    ("game-states-playing", "game-states-paused"),
    ("collision-overlap", "collision-no-overlap"),
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
    errors.extend(_validate_composites())
    errors.extend(_validate_before_after_pairs())
    errors.extend(_validate_no_accidental_duplicates())
    return errors


def _validate_composites() -> list[str]:
    errors = []
    for name in REQUIRED_COMPOSITES:
        path = OUT_DIR / f"{name}.png"
        if not path.exists():
            errors.append(f"Отсутствует обязательная сравнительная полоса: {path.relative_to(ROOT)}")
            continue
        with Image.open(path) as img:
            w, h = img.size
        if w < MIN_STRIP_WIDTH:
            errors.append(f"{path.relative_to(ROOT)}: полоса сравнения подозрительно узкая ({w}px)")
        if w > MAX_STRIP_WIDTH:
            errors.append(f"{path.relative_to(ROOT)}: полоса сравнения шире компактного лимита ({w}px > {MAX_STRIP_WIDTH}px)")
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
                f"{after_name}.png идентичен {before_name}.png — изменение должно быть видно на "
                f"экране, а не только в данных."
            )
    return errors


def _validate_no_accidental_duplicates() -> list[str]:
    """Разные сцены почти никогда не должны рендериться в один и тот же
    кадр — совпадение обычно значит, что состояние не применилось перед
    захватом."""
    errors = []
    seen: dict[bytes, str] = {}
    for name in REQUIRED_NAMES:
        path = OUT_DIR / f"{name}.png"
        if not path.exists():
            continue
        with Image.open(path) as img:
            content = img.convert("RGB").tobytes()
        if content in seen:
            errors.append(f"{name}.png идентичен {seen[content]}.png — вероятно, случайный дубликат.")
        else:
            seen[content] = name
    return errors


def main() -> None:
    errors = validate()
    if errors:
        print(f"Скриншоты главы 20 невалидны — найдено ошибок: {len(errors)}\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    total = len(REQUIRED_NAMES) + len(REQUIRED_COMPOSITES)
    print(f"Скриншоты главы 20 валидны: {total} файлов проверено.")


if __name__ == "__main__":
    main()
