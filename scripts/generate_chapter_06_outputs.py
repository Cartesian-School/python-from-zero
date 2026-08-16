#!/usr/bin/env python3
"""Executes every example in chapter_06_examples.EXAMPLES for real — headless,
via Xvfb and a native Tk turtle canvas — and saves the actual result to
site/assets/img/chapter-06/output/<name>.png.

See scripts/turtle_output_lib.py for the shared capture/convert/crop
pipeline (also used by scripts/generate_chapter_07_outputs.py).

Использование:
    .venv/bin/python3 scripts/generate_chapter_06_outputs.py
    .venv/bin/python3 scripts/generate_chapter_06_outputs.py 06-11-triangle 06-14-circle
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chapter_06_examples import EXAMPLES
from turtle_output_lib import generate_all

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-06" / "output"


if __name__ == "__main__":
    generate_all(EXAMPLES, OUT_DIR, sys.argv[1:])
