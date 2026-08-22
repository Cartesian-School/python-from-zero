#!/usr/bin/env python3
"""Проверяет, что все скриншоты, ожидаемые главой 19, существуют в
site/assets/img/chapter-19/output/, не пустые и не случайный снимок 1×1.

Использование: python3 scripts/validate_chapter_19_outputs.py
"""

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-19" / "output"

REQUIRED_NAMES = [
    "snake-final-overview",
    "snake-empty-field",
    "snake-head-food",
    "snake-moving-right",
    "snake-moving-up",
    "snake-one-segment",
    "snake-growing",
    "snake-body-follow-1",
    "snake-body-follow-2",
    "snake-body-follow-3",
    "snake-food-eaten-before",
    "snake-food-eaten-after",
    "snake-wall-collision",
    "snake-self-collision",
    "snake-game-over",
    "snake-paused",
    "snake-restarted",
    "snake-score",
    "snake-high-score",
    "snake-normal-speed",
    "snake-fast-speed",
    "snake-grid-demo",
    "snake-final-pro",
    # первый прототип (snake_basic.py) — используется на страницах 19-02..19-08
    "snake-basic-empty-field",
    "snake-basic-head-food",
    "snake-basic-moving",
    "snake-basic-eaten-before",
    "snake-basic-eaten-after",
    "snake-basic-collision",
    "snake-basic-full-game",
]

REQUIRED_COMPOSITES = [
    "snake-body-follow-strip",
    "snake-food-eaten-strip",
    "snake-pause-strip",
    "snake-basic-eaten-strip",
]

MIN_DIMENSION = 40  # anything smaller is almost certainly a capture bug, not a real window
MIN_STRIP_WIDTH = 900  # a composite strip is several native captures wide, not one

# Pairs where the second name must show visible change from the first —
# a validator catching "before == after" (nothing actually happened) bugs.
BEFORE_AFTER_PAIRS = [
    ("snake-food-eaten-before", "snake-food-eaten-after"),
    ("snake-body-follow-1", "snake-body-follow-2"),
    ("snake-body-follow-2", "snake-body-follow-3"),
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
                f"{after_name}.png идентичен {before_name}.png — тик игры (еда/движение тела) "
                f"должен быть виден на экране, а не только в данных."
            )
    return errors


def _validate_no_accidental_duplicates() -> list[str]:
    """Разные сценарии почти никогда не должны рендериться в один и тот же
    кадр — совпадение обычно значит, что состояние не применилось перед
    захватом (see reset_app())."""
    errors = []
    seen: dict[bytes, str] = {}
    # Эти пары — один и тот же реальный кадр, намеренно подписанный дважды
    # под разными именами для двух разных уроков (см. generate_chapter_19_outputs.py).
    allowed_pairs = {
        frozenset({"snake-self-collision", "snake-game-over"}),
        frozenset({"snake-one-segment", "snake-food-eaten-after"}),
        frozenset({"snake-moving-right", "snake-score"}),
        frozenset({"snake-restarted", "snake-high-score"}),
        frozenset({"snake-growing", "snake-normal-speed"}),
        frozenset({"snake-body-follow-3", "snake-moving-right"}),
    }
    for name in REQUIRED_NAMES:
        path = OUT_DIR / f"{name}.png"
        if not path.exists():
            continue
        with Image.open(path) as img:
            content = img.convert("RGB").tobytes()
        if content in seen:
            other = seen[content]
            if frozenset({other, name}) not in allowed_pairs:
                errors.append(f"{name}.png идентичен {other}.png — вероятно, случайный дубликат.")
        else:
            seen[content] = name
    return errors


def main() -> None:
    errors = validate()
    if errors:
        print(f"Скриншоты главы 19 невалидны — найдено ошибок: {len(errors)}\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    total = len(REQUIRED_NAMES) + len(REQUIRED_COMPOSITES)
    print(f"Скриншоты главы 19 валидны: {total} файлов проверено.")


if __name__ == "__main__":
    main()
