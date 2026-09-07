#!/usr/bin/env python3
"""Canonical CLI entry point for the book publication pipeline.

    python scripts/build_book.py --language ru --format pdf
    python scripts/build_book.py --language ru --format epub
    python scripts/build_book.py --language pl --format pdf
    python scripts/build_book.py --language pl --format epub
    python scripts/build_book.py --language ru --format all
    python scripts/build_book.py --all

Every combination routes through the exact same canonical pipeline
(book_pipeline.build_book) — language selects locale content, format selects
the publication adapter; see docs/contracts/BOOK-BUILD-PIPELINE-CONTRACT.md.
Stops at the first target that fails — a broken EPUB or missing chapter must
never be masked by a "successful" later stage. When more than one target is
built in a single invocation, the combined artifacts are validated
(validate_book.py) at the end.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from book_pipeline import SUPPORTED_FORMATS, SUPPORTED_LANGUAGES, build_book


def _parse_args(argv: list[str]) -> list[tuple[str, str]]:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--language", choices=sorted(SUPPORTED_LANGUAGES), help="Language edition to build")
    parser.add_argument(
        "--format", choices=[*sorted(SUPPORTED_FORMATS), "all"], help="Publication format to build ('all' for every supported format)"
    )
    parser.add_argument(
        "--all", action="store_true", help="Build the full supported language x format matrix"
    )
    args = parser.parse_args(argv)

    if args.all:
        if args.language or args.format:
            parser.error("--all cannot be combined with --language/--format")
        return [(language, fmt) for language in SUPPORTED_LANGUAGES for fmt in SUPPORTED_FORMATS]

    if not args.language or not args.format:
        parser.error("--language and --format are required unless --all is given")

    formats = SUPPORTED_FORMATS if args.format == "all" else (args.format,)
    return [(args.language, fmt) for fmt in formats]


def main(argv: list[str] | None = None) -> None:
    targets = _parse_args(sys.argv[1:] if argv is None else argv)

    for language, output_format in targets:
        label = f"{language} x {output_format}"
        print(f"\n{'=' * 60}\nBuilding {label}\n{'=' * 60}")
        try:
            build_book(language=language, output_format=output_format)
        except Exception as exc:
            print(f"\nBUILD STOPPED: {label} failed: {exc}", file=sys.stderr)
            sys.exit(1)

    if len(targets) > 1:
        print(f"\n{'=' * 60}\nValidating combined publication artifacts\n{'=' * 60}")
        result = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_book.py")], cwd=ROOT)
        if result.returncode != 0:
            sys.exit(result.returncode)

    print(f"\n{'=' * 60}\nPublication build complete.\n{'=' * 60}")


if __name__ == "__main__":
    main()
