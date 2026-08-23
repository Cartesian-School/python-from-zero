#!/usr/bin/env python3
"""Проверяет, что все скриншоты, ожидаемые главой 21, существуют в
site/assets/img/chapter-21/output/, не пустые, не случайный снимок 1x1 и не
однотонная заливка одним цветом.

Использование: python3 scripts/validate_chapter_21_outputs.py
"""

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-21" / "output"

REQUIRED_NAMES = [
    "01-menu",
    "02-empty-playfield",
    "03-player-ship",
    "04-player-left",
    "05-player-center",
    "06-player-right",
    "07-first-enemy",
    "08-enemy-wave",
    "09-first-bullet",
    "10-held-fire-cooldown",
    "11-bullet-before-hit",
    "12-bullet-enemy-hit",
    "13-explosion-frame-1",
    "14-explosion-frame-2",
    "15-score-after-hit",
    "16-player-hit",
    "17-invulnerability",
    "18-lives-hud",
    "19-two-enemy-types",
    "20-wave-1",
    "21-wave-harder",
    "22-paused",
    "23-game-over",
    "24-restarted-game",
    "25-final-gameplay",
]

REQUIRED_COMPOSITES = [
    "player-movement-strip",
    "fire-sequence-strip",
    "damage-sequence-strip",
    "difficulty-strip",
    "game-states-strip",
]

MIN_DIMENSION = 20
MIN_STRIP_WIDTH = 500
MAX_STRIP_WIDTH = 820

BEFORE_AFTER_PAIRS = [
    ("04-player-left", "06-player-right"),
    ("02-empty-playfield", "08-enemy-wave"),
    ("11-bullet-before-hit", "12-bullet-enemy-hit"),
    ("13-explosion-frame-1", "14-explosion-frame-2"),
    ("01-menu", "22-paused"),
    ("22-paused", "23-game-over"),
    ("23-game-over", "24-restarted-game"),
    ("20-wave-1", "21-wave-harder"),
    ("02-empty-playfield", "16-player-hit"),
]


def _is_blank(img: Image.Image) -> bool:
    """True, если изображение — сплошная заливка одним цветом (значит,
    сцена не отрисовалась, а не то, что она действительно так выглядит:
    у нашего фона всегда есть звёзды или HUD, поэтому один цвет — баг)."""
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


def main() -> None:
    errors = validate()
    if errors:
        print(f"Скриншоты главы 21 невалидны — найдено ошибок: {len(errors)}\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    total = len(REQUIRED_NAMES) + len(REQUIRED_COMPOSITES)
    print(f"Скриншоты главы 21 валидны: {total} файлов проверено.")


if __name__ == "__main__":
    main()
