#!/usr/bin/env python3
"""Проверяет, что для каждого примера в chapter_06_examples.EXAMPLES
существует непустой сгенерированный PNG в site/assets/img/chapter-06/output/
— то есть код и картинка не разошлись, и ни один вывод не потерялся.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chapter_06_examples import EXAMPLES

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-06" / "output"


def main() -> None:
    missing: list[str] = []
    empty: list[str] = []
    for name in EXAMPLES:
        path = OUT_DIR / f"{name}.png"
        if not path.exists():
            missing.append(name)
        elif path.stat().st_size == 0:
            empty.append(name)

    extra = [
        p.stem for p in OUT_DIR.glob("*.png")
        if p.stem not in EXAMPLES
    ]

    if missing:
        print(f"ОТСУТСТВУЮТ изображения ({len(missing)}): {missing}")
    if empty:
        print(f"НУЛЕВОЙ РАЗМЕР ({len(empty)}): {empty}")
    if extra:
        print(f"ЛИШНИЕ файлы без примера в EXAMPLES ({len(extra)}): {extra}")

    if missing or empty:
        sys.exit(1)

    print(f"OK: все {len(EXAMPLES)} примеров имеют непустой PNG в {OUT_DIR.relative_to(ROOT)}")
    if extra:
        print("(лишние файлы — не ошибка сборки, но стоит проверить вручную)")


if __name__ == "__main__":
    main()
