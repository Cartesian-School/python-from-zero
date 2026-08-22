#!/usr/bin/env python3
"""Guards against decorative Unicode emoji creeping back into chapter prose.

Cartesian School chapter content uses a local SVG icon system (see
site/assets/icons/cartesian/icons.svg, scripts/site_lib.py:icon_label(), and
docs/ICON-SYSTEM.md) instead of decorative emoji (💡🚀⚠️✅❌🐞 etc.). This
script scans the canonical chapter-content generators — scripts/build_chapter_*.py
and scripts/build_site_index.py — for emoji characters and reports any that
are not:

  1. Typographic/functional symbols that were never decorative editorial
     emoji in the first place (arrows used as prose notation, ✓/✗ used as
     JS-driven completion state, ☰ as the mobile nav toggle glyph, turtle/
     game-board markers, difficulty-rating stars, ...). See ALLOWED_ALWAYS.
  2. Legitimate instructional/data emoji: literal print() output, terminal
     transcripts, or Unicode-lesson strings that are the actual subject
     being taught, not decorative headings. See DATA_ALLOWLIST — an explicit
     (file, exact substring) list, so a new decorative emoji can never hide
     behind it by accident.

Usage:
    python3 scripts/validate_no_decorative_emoji.py

Exits 0 and prints PASS if nothing new is found; exits 1 and prints FAIL with
a file:line report otherwise.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Broad "could plausibly be a decorative emoji" scan range.
EMOJI_RANGE = re.compile(
    "["
    "\U0001F000-\U0001FFFF"
    "\U00002300-\U000023FF"
    "\U000025A0-\U000027BF"
    "\U00002B00-\U00002BFF"
    "\U0001F1E6-\U0001F1FF"
    "\U0000FE0F"
    "\U00002190-\U000021FF"
    "\U00002600-\U000026FF"
    "]"
)

# Typographic / functional characters in this range that are NOT decorative
# editorial emoji and are never migrated to the icon system: prose arrow
# notation ("текст → результат"), difficulty-rating stars (★), JS-driven
# completion checkmarks (✓/✗), a checklist glyph (☐), the mobile-nav
# hamburger button (☰), turtle/game-board cell markers (● ■), rotation-
# direction notation (↺ ↻ ⇄), and the literal VS Code "Run" button glyph (▷▼).
ALLOWED_ALWAYS = set("→★↓↑←↔❯✓✗☐↺↻●■⇄▷▼☰")

# Exact substrings holding legitimate instructional/data emoji (print()
# output, terminal transcripts, Unicode-lesson strings) — verified by hand
# against the full chapter-content audit. Keep in sync with
# scripts/build_*.py content; do NOT widen this to a pattern/heuristic.
DATA_ALLOWLIST: dict[str, list[str]] = {
    "build_chapter_03.py": [
        "PySH 0.8.2 | Python 3.13.5",
        "┌─🐍 astra@soi",
    ],
    "build_chapter_04.py": ["\U0001F36C" * 17],
    "build_chapter_05.py": ['["\U0001F381", "\U0001F388", "\U0001F389"]'],
    "build_chapter_08.py": [
        "\U0001F40D и \U0001F389",
        'text = "код \U0001F40D"',
    ],
    "build_chapter_09.py": ["\U0001F389 Вы угадали"],
    "build_chapter_12.py": [
        'print("✅ Верно!")',
        "print(f\"❌ Неверно. Правильный ответ: {q",
    ],
    "build_chapter_15.py": ['text = "Питон\U0001F40D"'],
}

TARGET_GLOBS = ["build_chapter_*.py", "build_site_index.py"]


def line_is_covered_by_allowlist(filename: str, line: str) -> bool:
    return any(snippet in line for snippet in DATA_ALLOWLIST.get(filename, []))


def main() -> int:
    violations: list[tuple[str, int, str, str]] = []

    files: list[pathlib.Path] = []
    for pattern in TARGET_GLOBS:
        files.extend(sorted((ROOT / "scripts").glob(pattern)))

    for f in files:
        text = f.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            found = [ch for ch in EMOJI_RANGE.findall(line) if ch not in ALLOWED_ALWAYS]
            if not found:
                continue
            if line_is_covered_by_allowlist(f.name, line):
                continue
            for ch in found:
                violations.append((f.name, lineno, ch, line.strip()[:100]))

    if violations:
        print(f"FAIL — {len(violations)} decorative emoji occurrence(s) found outside the icon system:\n")
        for filename, lineno, ch, snippet in violations:
            print(f"  {filename}:{lineno}: {ch!r} (U+{ord(ch):04X})  {snippet}")
        print(
            "\nReplace with scripts/site_lib.py:icon_label(name, text) (or cs_icon(name) in raw "
            "HTML) — see docs/ICON-SYSTEM.md for the semantic mapping. If this is genuinely "
            "instructional/data content (print() output, a terminal transcript, a Unicode-lesson "
            "string), add the exact substring to DATA_ALLOWLIST in this script instead."
        )
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
