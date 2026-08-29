#!/usr/bin/env python3
"""Geometric audit of every inline SVG diagram in site/chapters/glava-01..24.

Two defect classes:
  1. Curved connectors: any <path> with a cubic/quadratic Bezier command
     (C/Q) that also carries an arrowhead marker-end -> it is an "arrow",
     and it is curved, not straight/rectangular.
  2. Text overflow: for each <text>/<tspan> pair immediately preceded (in
     document order) by a filled <rect> or <polygon> "box" sibling, measure
     the tspan's rendered width with the REAL font file (JetBrains Mono /
     Sora, matched by weight) at the declared font-size, and compare it
     against the enclosing shape's usable width at that tspan's y
     (exact for rect; edge-interpolated for polygon, which correctly
     narrows near a diamond's top/bottom vertices).

Run from the repo root: python scripts/audit_diagrams.py
Requires: pip install beautifulsoup4 fonttools
Requires system fonts: fonts-jetbrains-mono, fonts-sora (apt) — or edit
FONT_FILES below to point at wherever those two families are installed.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS_DIR = ROOT / "site" / "chapters"

_JB = os.environ.get("AUDIT_JETBRAINS_MONO_DIR", "/usr/share/fonts/truetype/jetbrains-mono")
_SORA = os.environ.get("AUDIT_SORA_DIR", "/usr/share/fonts/opentype/sora")

FONT_FILES = {
    ("JetBrains Mono", "400"): f"{_JB}/JetBrainsMono-Regular.ttf",
    ("JetBrains Mono", "500"): f"{_JB}/JetBrainsMono-Medium.ttf",
    ("JetBrains Mono", "600"): f"{_JB}/JetBrainsMono-SemiBold.ttf",
    ("JetBrains Mono", "700"): f"{_JB}/JetBrainsMono-Bold.ttf",
    ("Sora", "400"): f"{_SORA}/Sora-Regular.ttf",
    ("Sora", "600"): f"{_SORA}/Sora-SemiBold.ttf",
    ("Sora", "700"): f"{_SORA}/Sora-Bold.ttf",
    ("Sora", "800"): f"{_SORA}/Sora-ExtraBold.ttf",
    ("Inter", "400"): None,  # not used inside diagram boxes; fallback below
}

_glyph_width_cache: dict[tuple[str, str], dict] = {}


def _load_metrics(family: str, weight: str):
    key = (family, weight)
    if key in _glyph_width_cache:
        return _glyph_width_cache[key]
    path = FONT_FILES.get(key)
    if path is None:
        candidates = [k for k in FONT_FILES if k[0] == family and FONT_FILES[k]]
        if not candidates:
            candidates = [("JetBrains Mono", "600")]
        path = FONT_FILES[candidates[0]]
    font = TTFont(path)
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    units_per_em = font["head"].unitsPerEm
    cache = {"cmap": cmap, "hmtx": hmtx, "upm": units_per_em}
    _glyph_width_cache[key] = cache
    return cache


def text_width_px(text: str, family: str, weight: str, size_px: float) -> float:
    m = _load_metrics(family, weight)
    total = 0.0
    for ch in text:
        glyph_name = m["cmap"].get(ord(ch))
        if glyph_name is None:
            total += 0.55 * m["upm"]
            continue
        adv, _lsb = m["hmtx"][glyph_name]
        total += adv
    return total / m["upm"] * size_px


def polygon_points(pts_attr: str) -> list[tuple[float, float]]:
    pts = []
    for pair in pts_attr.strip().split():
        x, y = pair.split(",")
        pts.append((float(x), float(y)))
    return pts


def polygon_width_at_y(pts: list[tuple[float, float]], y: float) -> float | None:
    xs = []
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        if y1 == y2:
            if y1 == y:
                xs.extend([x1, x2])
            continue
        lo, hi = (y1, y2) if y1 < y2 else (y2, y1)
        if lo <= y <= hi:
            t = (y - y1) / (y2 - y1)
            xs.append(x1 + t * (x2 - x1))
    if not xs:
        return None
    return max(xs) - min(xs)


def rect_geom(tag):
    return {"kind": "rect", "x": float(tag["x"]), "y": float(tag["y"]),
            "w": float(tag["width"]), "h": float(tag["height"])}


def poly_geom(tag):
    pts = polygon_points(tag["points"])
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return {"kind": "polygon", "pts": pts, "x": min(xs), "y": min(ys),
            "w": max(xs) - min(xs), "h": max(ys) - min(ys)}


def shape_width_at_y(geom, y):
    if geom["kind"] == "rect":
        if geom["y"] - 0.5 <= y <= geom["y"] + geom["h"] + 0.5:
            return geom["w"]
        return None
    return polygon_width_at_y(geom["pts"], y)


def audit_svg(svg, file_rel, findings, counters):
    counters["svg_total"] += 1
    for path in svg.find_all("path"):
        d = path.get("d", "")
        stroke = path.get("stroke")
        marker_end = path.get("marker-end")
        if stroke and marker_end and re.search(r"[CQ]-?\d", d):
            counters["curved_arrows"] += 1
            findings["curved_arrows"].append({"file": file_rel, "d": d[:120], "stroke": stroke})

    last_shape = None
    for el in svg.find_all(["rect", "polygon", "text"], recursive=True):
        if el.name in ("rect", "polygon"):
            fill = el.get("fill", "")
            if fill and fill not in ("none", "transparent"):
                last_shape = rect_geom(el) if el.name == "rect" else poly_geom(el)
            continue
        family_attr = el.get("font-family", "")
        weight = el.get("font-weight", "400")
        size = float(el.get("font-size", "13"))
        family = "Sora" if "Sora" in family_attr else ("JetBrains Mono" if "JetBrains" in family_attr else "Inter")
        for tspan in el.find_all("tspan"):
            txt = tspan.get_text()
            if not txt.strip():
                continue
            ty = float(tspan.get("y", el.get("y", 0)))
            w = text_width_px(txt, family, weight, size)
            counters["tspans_checked"] += 1
            if last_shape is None:
                continue
            avail = shape_width_at_y(last_shape, ty)
            if avail is None:
                continue
            budget = avail - 14
            if w > budget:
                counters["overflow"] += 1
                findings["overflow"].append({
                    "file": file_rel, "text": txt, "text_width": round(w, 1),
                    "available": round(budget, 1), "shape": last_shape["kind"],
                    "y": ty, "excess": round(w - budget, 1),
                })


def main():
    findings = {"curved_arrows": [], "overflow": []}
    counters = {"svg_total": 0, "curved_arrows": 0, "tspans_checked": 0, "overflow": 0}
    files = sorted(CHAPTERS_DIR.glob("glava-*/*.html"))
    print(f"Scanning {len(files)} files under site/chapters/glava-01..24 ...", file=sys.stderr)
    for f in files:
        rel = str(f.relative_to(ROOT))
        html = f.read_text(encoding="utf-8")
        if "<svg" not in html:
            continue
        soup = BeautifulSoup(html, "html.parser")
        for svg in soup.find_all("svg"):
            audit_svg(svg, rel, findings, counters)

    out_path = ROOT / "audit_report.json"
    out_path.write_text(json.dumps({"counters": counters, "findings": findings}, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=== SUMMARY ===")
    print(f"SVG figures scanned:      {counters['svg_total']}")
    print(f"tspans measured:          {counters['tspans_checked']}")
    print(f"Curved arrows found:      {counters['curved_arrows']}")
    print(f"Text-overflow instances:  {counters['overflow']}")
    print(f"Full report: {out_path}")
    curve_files = sorted({x["file"] for x in findings["curved_arrows"]})
    overflow_files = sorted({x["file"] for x in findings["overflow"]})
    print(f"\nFiles with >=1 curved arrow: {len(curve_files)}")
    print(f"Files with >=1 text overflow: {len(overflow_files)}")
    if curve_files:
        print("Curved-arrow files:", *curve_files, sep="\n  ")


if __name__ == "__main__":
    main()
