"""Shared real-Turtle-output pipeline, used by both
generate_chapter_06_outputs.py and generate_chapter_07_outputs.py so the
capture/convert/crop/validate logic exists in exactly one place.

Pipeline for one example:
  1. Wrap the example's code + a small capture tail into a temp .py file.
  2. Run it under xvfb-run (a real, invisible Tk window actually opens).
  3. turtle exports the canvas as PostScript (canvas.postscript()) — the one
     cross-platform way to get real vector content out of a Tk Canvas.
  4. Pillow (via Ghostscript) converts PostScript -> PNG, supersampled for
     sharpness.
  5. Crop to the actual drawn content's bounding box (with padding) — a
     drawing rarely fills the whole canvas, so a naive full-canvas capture
     is mostly wasted white space.

Two rendering quirks are worked around in the runner tail itself (not by
touching example code): canvas.postscript() silently ignores
screen.bgcolor() (it's a widget property, not a canvas item), so a
non-white background is redrawn as a real, z-order-lowered canvas
rectangle before export; and Turtle's default colormode (1.0) makes
screen.bgcolor() return fractional RGB floats rather than a Tk color
string, which needs explicit conversion.

CONVENTION every EXAMPLES entry must follow: create the screen as
`screen = turtle.Screen()` (that exact name). The runner tail reuses that
same `screen` binding directly — it deliberately does NOT call
`turtle.getscreen()` to "re-find" it. That extra lookup was tried and
reintroduced a real, reproducible bug: canvas.postscript() would export a
stale render — a ghost of an earlier item's position (e.g. the turtle
cursor's position before a penup()+goto() move) bleeding into the capture,
even though Tk's own canvas.find_all()/coords() already showed only the
correct, current items. It reproduced 100% of the time with
turtle.getscreen() in the tail and 0% of the time without it, across
repeated and parallel runs — so the fix is to never call it here, not to
paper over the symptom with extra update()/sleep() calls.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops

CROP_PADDING = 36
SUPERSAMPLE = 3

RUNNER_TEMPLATE = '''
{code}

canvas = screen.getcanvas()
canvas.update()
cw = canvas.winfo_width()
ch = canvas.winfo_height()

_bg = screen.bgcolor()
if isinstance(_bg, tuple):
    # turtle's default colormode (1.0) returns bgcolor() as fractional RGB
    # floats — Tk's canvas needs a "#rrggbb" string, not a Python tuple.
    _bg = "#%02x%02x%02x" % tuple(round(c * 255) for c in _bg)
if str(_bg).lower() not in ("white", "#fff", "#ffffff"):
    _bg_id = canvas.create_rectangle(-cw, -ch, cw, ch, fill=_bg, outline=_bg)
    canvas.tag_lower(_bg_id)

canvas.postscript(file={eps_path!r}, x=-cw / 2, y=-ch / 2, width=cw, height=ch)
screen.bye()
'''


def run_example(name: str, code: str, tmp_dir: Path, *, timeout: int = 60) -> Path:
    eps_path = tmp_dir / f"{name}.eps"
    script_path = tmp_dir / f"{name}_run.py"
    script_path.write_text(RUNNER_TEMPLATE.format(code=code, eps_path=str(eps_path)), encoding="utf-8")

    result = subprocess.run(
        [
            "xvfb-run", "-a", "--server-args=-screen 0 800x600x24",
            sys.executable, str(script_path),
        ],
        capture_output=True, text=True, timeout=timeout,
    )
    if result.returncode != 0 or not eps_path.exists():
        raise RuntimeError(
            f"Пример {name} не выполнился:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        )
    return eps_path


def eps_to_cropped_png(eps_path: Path, png_path: Path) -> None:
    img = Image.open(eps_path)
    img.load(scale=SUPERSAMPLE)
    img = img.convert("RGB")

    bg = Image.new("RGB", img.size, (255, 255, 255))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    if bbox:
        left, top, right, bottom = bbox
        left = max(0, left - CROP_PADDING)
        top = max(0, top - CROP_PADDING)
        right = min(img.width, right + CROP_PADDING)
        bottom = min(img.height, bottom + CROP_PADDING)
        img = img.crop((left, top, right, bottom))

    png_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(png_path, "PNG")


def generate_one(name: str, code: str, out_dir: Path, tmp_dir: Path) -> None:
    eps_path = run_example(name, code, tmp_dir)
    png_path = out_dir / f"{name}.png"
    eps_to_cropped_png(eps_path, png_path)
    size = png_path.stat().st_size
    if size == 0:
        raise RuntimeError(f"{name}: получен нулевой PNG")
    print(f"OK: {name}.png ({size} байт)")


def generate_all(examples: dict[str, str], out_dir: Path, names: list[str] | None = None) -> None:
    """Generates (or regenerates) the given names — default: every key in
    examples. Prints OK/FAIL per example and exits nonzero if any failed."""
    names = names if names else list(examples.keys())
    unknown = [n for n in names if n not in examples]
    if unknown:
        print(f"Неизвестные примеры: {unknown}")
        sys.exit(2)

    out_dir.mkdir(parents=True, exist_ok=True)
    failed: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        for name in names:
            try:
                generate_one(name, examples[name], out_dir, tmp_dir)
            except Exception as exc:  # noqa: BLE001 — report and continue
                print(f"FAIL: {name}: {exc}")
                failed.append(name)

    print(f"\nГотово: {len(names) - len(failed)}/{len(names)} успешно.")
    if failed:
        print("Не удалось сгенерировать:", failed)
        sys.exit(1)


def validate_outputs(examples: dict[str, str], out_dir: Path) -> None:
    """Checks every examples[name] has a non-empty generated PNG in out_dir
    — catches code/image drift and missing/zero-byte outputs."""
    missing: list[str] = []
    empty: list[str] = []
    for name in examples:
        path = out_dir / f"{name}.png"
        if not path.exists():
            missing.append(name)
        elif path.stat().st_size == 0:
            empty.append(name)

    extra = [p.stem for p in out_dir.glob("*.png") if p.stem not in examples]

    if missing:
        print(f"ОТСУТСТВУЮТ изображения ({len(missing)}): {missing}")
    if empty:
        print(f"НУЛЕВОЙ РАЗМЕР ({len(empty)}): {empty}")
    if extra:
        print(f"ЛИШНИЕ файлы без примера в EXAMPLES ({len(extra)}): {extra}")

    if missing or empty:
        sys.exit(1)

    print(f"OK: все {len(examples)} примеров имеют непустой PNG в {out_dir}")
    if extra:
        print("(лишние файлы — не ошибка сборки, но стоит проверить вручную)")
