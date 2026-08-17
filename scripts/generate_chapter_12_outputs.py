#!/usr/bin/env python3
"""Executes every example in chapter_12_examples.EXAMPLES for real — headless,
via Xvfb and a native Tk turtle canvas — and saves the actual result to
site/assets/img/chapter-12/output/<name>.png.

See scripts/turtle_output_lib.py for the shared capture/convert/crop
pipeline (also used by chapters 6-7/10's generators).

Использование:
    .venv/bin/python3 scripts/generate_chapter_12_outputs.py
    .venv/bin/python3 scripts/generate_chapter_12_outputs.py 12-elka
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chapter_12_examples import EXAMPLES
from turtle_output_lib import generate_all

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-12" / "output"


if __name__ == "__main__":
    generate_all(EXAMPLES, OUT_DIR, sys.argv[1:])
