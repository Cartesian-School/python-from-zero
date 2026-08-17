#!/usr/bin/env python3
"""Checks every example in chapter_13_examples.EXAMPLES has a non-empty
generated PNG in site/assets/img/chapter-13/output/ — i.e. code and image
never drift apart, and nothing went missing.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chapter_13_examples import EXAMPLES
from turtle_output_lib import validate_outputs

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-13" / "output"


if __name__ == "__main__":
    validate_outputs(EXAMPLES, OUT_DIR)
