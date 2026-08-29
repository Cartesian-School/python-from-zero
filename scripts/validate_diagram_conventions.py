#!/usr/bin/env python3
"""Enforce textbook diagram conventions across Chapters 1–24.

Every generated SVG arrow must use only horizontal and vertical segments.
Flowcharts must use standard semantic shapes with meaningful colors.  The
validator uses only the standard library so it runs locally, in CI and on
Vercel.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "site" / "chapters"

SVG_RE = re.compile(r"<svg\b.*?</svg>", re.DOTALL | re.IGNORECASE)
ARROW_RE = re.compile(
    r"<(?:path|line)\b(?=[^>]*marker-(?:start|end)\s*=)[^>]*>",
    re.IGNORECASE,
)
ATTR_RE = re.compile(r"([:\w-]+)\s*=\s*(['\"])(.*?)\2", re.DOTALL)
PATH_TOKEN_RE = re.compile(
    r"[A-Za-z]|[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
)
SHAPE_RE = re.compile(
    r"<(rect|polygon)\b[^>]*data-flow-shape\s*=\s*(['\"])(.*?)\2[^>]*>",
    re.IGNORECASE,
)

EXPECTED_SHAPE_TAGS = {
    "terminator": "rect",
    "process": "rect",
    "decision": "polygon",
    "input-output": "polygon",
}
NON_SEMANTIC_FILLS = {
    "#fff",
    "#ffffff",
    "white",
    "#fafafc",
    "none",
    "transparent",
}


def attrs(tag: str) -> dict[str, str]:
    return {name.lower(): value for name, _, value in ATTR_RE.findall(tag)}


def path_error(d: str) -> str | None:
    """Return an error when a connector path is curved or non-orthogonal."""
    tokens = PATH_TOKEN_RE.findall(d.replace(",", " "))
    if not tokens:
        return "empty path"

    command = ""
    index = 0
    current: tuple[float, float] | None = None
    start: tuple[float, float] | None = None
    while index < len(tokens):
        token = tokens[index]
        if token.isalpha():
            command = token
            index += 1
            if command.upper() in {"C", "S", "Q", "T", "A"}:
                return f"curved command {command}"
            if command.upper() not in {"M", "L", "H", "V", "Z"}:
                return f"unsupported command {command}"
            if command.upper() == "Z":
                if start is not None:
                    current = start
                continue
        if not command:
            return "coordinates before command"

        relative = command.islower()
        upper = command.upper()
        try:
            if upper in {"M", "L"}:
                x, y = float(tokens[index]), float(tokens[index + 1])
                index += 2
                if relative and current is not None:
                    x, y = current[0] + x, current[1] + y
                next_point = (x, y)
                if upper == "M":
                    start = next_point
                    command = "l" if relative else "L"
                elif current is not None and current[0] != x and current[1] != y:
                    return f"diagonal segment {current} -> {next_point}"
                current = next_point
            elif upper == "H":
                x = float(tokens[index])
                index += 1
                if current is None:
                    return "H before M"
                if relative:
                    x += current[0]
                current = (x, current[1])
            elif upper == "V":
                y = float(tokens[index])
                index += 1
                if current is None:
                    return "V before M"
                if relative:
                    y += current[1]
                current = (current[0], y)
            elif upper == "Z":
                continue
        except (IndexError, ValueError):
            return "invalid path data"
    return None


def validate() -> tuple[list[str], Counter[str]]:
    errors: list[str] = []
    counts: Counter[str] = Counter()
    expected_chapters = {f"glava-{number:02d}" for number in range(1, 25)}
    actual_chapters = {
        path.name for path in CHAPTERS.glob("glava-*") if path.is_dir()
    }
    missing = sorted(expected_chapters - actual_chapters)
    if missing:
        errors.append(f"missing chapter directories: {', '.join(missing)}")

    for chapter in sorted(expected_chapters):
        chapter_dir = CHAPTERS / chapter
        chapter_svgs = 0
        if not chapter_dir.is_dir():
            continue
        for path in sorted(chapter_dir.glob("*.html")):
            source = path.read_text(encoding="utf-8")
            for svg_index, svg in enumerate(SVG_RE.findall(source), start=1):
                svg_attrs = attrs(svg.split(">", 1)[0] + ">")
                # Navigation icons are repeated on every page and are not
                # instructional diagrams.  Course illustrations are the SVGs
                # exposed to learners as role="img".
                if svg_attrs.get("role") != "img":
                    continue
                chapter_svgs += 1
                counts["svg"] += 1
                diagram_kind = svg_attrs.get("data-diagram", "unclassified")
                counts[f"diagram:{diagram_kind}"] += 1

                for match in ARROW_RE.finditer(svg):
                    tag = match.group(0)
                    tag_attrs = attrs(tag)
                    counts["arrow"] += 1
                    if tag.lower().startswith("<line"):
                        try:
                            x1 = float(tag_attrs["x1"])
                            y1 = float(tag_attrs["y1"])
                            x2 = float(tag_attrs["x2"])
                            y2 = float(tag_attrs["y2"])
                        except (KeyError, ValueError):
                            errors.append(
                                f"{path.relative_to(ROOT)} SVG {svg_index}: invalid arrow line"
                            )
                            continue
                        if x1 == x2 and y1 == y2:
                            errors.append(
                                f"{path.relative_to(ROOT)} SVG {svg_index}: zero-length arrow"
                            )
                        elif x1 != x2 and y1 != y2:
                            errors.append(
                                f"{path.relative_to(ROOT)} SVG {svg_index}: diagonal arrow line"
                            )
                    else:
                        error = path_error(tag_attrs.get("d", ""))
                        if error:
                            errors.append(
                                f"{path.relative_to(ROOT)} SVG {svg_index}: {error}"
                            )

                for shape_match in SHAPE_RE.finditer(svg):
                    tag = shape_match.group(0)
                    shape_attrs = attrs(tag)
                    shape = shape_attrs.get("data-flow-shape", "")
                    tag_name = shape_match.group(1).lower()
                    counts[f"shape:{shape}"] += 1
                    expected_tag = EXPECTED_SHAPE_TAGS.get(shape)
                    if expected_tag is None:
                        errors.append(
                            f"{path.relative_to(ROOT)} SVG {svg_index}: unknown flow shape {shape!r}"
                        )
                    elif tag_name != expected_tag:
                        errors.append(
                            f"{path.relative_to(ROOT)} SVG {svg_index}: "
                            f"{shape} must use <{expected_tag}>"
                        )
                    fill = shape_attrs.get("fill", "").lower()
                    if fill in NON_SEMANTIC_FILLS or not fill:
                        errors.append(
                            f"{path.relative_to(ROOT)} SVG {svg_index}: "
                            f"{shape} lacks semantic color"
                        )

                if diagram_kind == "flowchart" and "data-flow-shape=" not in svg:
                    errors.append(
                        f"{path.relative_to(ROOT)} SVG {svg_index}: "
                        "flowchart lacks standard semantic shapes"
                    )

        if chapter_svgs == 0:
            errors.append(f"{chapter}: no SVG diagrams found")
        counts[f"chapter:{chapter}"] = chapter_svgs

    return errors, counts


def main() -> int:
    errors, counts = validate()
    if errors:
        print("Diagram convention validation FAILED:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    shape_total = sum(
        value for key, value in counts.items() if key.startswith("shape:")
    )
    print(
        "Diagram convention validation passed: "
        f"24 chapters, {counts['svg']} SVG diagrams, "
        f"{counts['arrow']} orthogonal arrows, "
        f"{shape_total} standard flowchart shapes."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
