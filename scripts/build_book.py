#!/usr/bin/env python3
"""Single reproducible entry point for the book publication pipeline.

    python scripts/build_book.py

Runs, in order: EPUB build -> PDF build (which itself fails loudly on any
pagination/cover problem, per build_pdf.py) -> combined artifact validation
(validate_book.py). Stops at the first stage that fails — a broken EPUB or
missing chapter must never be masked by a "successful" later stage. Every
stage's own script remains independently runnable for iterating on one
artifact at a time; this just wires them into one command for the full,
must-pass publication build.

Output:
    book/pdf/готовая книга.pdf
    book/epub/python-s-nulya.epub
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
PYTHON = sys.executable


def run_stage(label: str, script: str) -> None:
    print(f"\n{'=' * 60}\n{label}\n{'=' * 60}")
    result = subprocess.run([PYTHON, str(SCRIPTS / script)], cwd=ROOT)
    if result.returncode != 0:
        print(f"\nСБОРКА ОСТАНОВЛЕНА: {label} завершился с ошибкой (exit {result.returncode}).", file=sys.stderr)
        sys.exit(result.returncode)


def main() -> None:
    run_stage("1/3 — EPUB", "build_epub.py")
    run_stage("2/3 — PDF (includes pagination gate)", "build_pdf.py")
    run_stage("3/3 — Validation (PDF + EPUB)", "validate_book.py")
    print(f"\n{'=' * 60}\nПубликация собрана и провалидирована успешно.\n{'=' * 60}")


if __name__ == "__main__":
    main()
