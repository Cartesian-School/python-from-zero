#!/usr/bin/env python3
"""Выполняет каждый пример из chapter_06_examples.EXAMPLES ПО-НАСТОЯЩЕМУ —
headless, через Xvfb и нативный Tk-холст turtle — и сохраняет реальный
результат в site/assets/img/chapter-06/output/<name>.png.

Ни один вывод в главе 6 не нарисован вручную и не сгенерирован ИИ: это
буквально тот же код, что показан на странице (см. docstring в
chapter_06_examples.py), выполненный по-настоящему.

Пайплайн для одного примера:
  1. Обёртываем код примера + код экспорта холста во временный .py.
  2. Запускаем его под xvfb-run (виртуальный дисплей — окна Tk открываются
     по-настоящему, но невидимо).
  3. turtle сохраняет холст как PostScript (единственный кроссплатформенный
     способ экспортировать содержимое Tk Canvas без стороннего скриншот-тула).
  4. Pillow (через Ghostscript) конвертирует PostScript → PNG с суперсэмплингом
     для чёткости.
  5. Обрезаем финальное изображение по фактической границе рисунка (не по
     границе окна) с отступом — иначе большая часть кадра остаётся пустой,
     потому что рисунок редко занимает весь холст.

Использование:
    .venv/bin/python3 scripts/generate_chapter_06_outputs.py
    .venv/bin/python3 scripts/generate_chapter_06_outputs.py 06-11-triangle 06-14-circle
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chapter_06_examples import EXAMPLES

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-06" / "output"
CROP_PADDING = 36
SUPERSAMPLE = 3

RUNNER_TEMPLATE = '''
{code}

screen = turtle.getscreen()
canvas = screen.getcanvas()
canvas.update()
cw = canvas.winfo_width()
ch = canvas.winfo_height()

# canvas.postscript() only exports canvas ITEMS, not the widget's own
# -background option — so a screen.bgcolor() call is invisible to it unless
# we also draw the background as a real (very large, then lowered-to-back)
# canvas item ourselves.
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


def run_example(name: str, code: str, tmp_dir: Path) -> Path:
    eps_path = tmp_dir / f"{name}.eps"
    script_path = tmp_dir / f"{name}_run.py"
    script_path.write_text(RUNNER_TEMPLATE.format(code=code, eps_path=str(eps_path)), encoding="utf-8")

    result = subprocess.run(
        [
            "xvfb-run", "-a", "--server-args=-screen 0 800x600x24",
            sys.executable, str(script_path),
        ],
        capture_output=True, text=True, timeout=60,
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


def generate_one(name: str, code: str, tmp_dir: Path) -> None:
    eps_path = run_example(name, code, tmp_dir)
    png_path = OUT_DIR / f"{name}.png"
    eps_to_cropped_png(eps_path, png_path)
    size = png_path.stat().st_size
    if size == 0:
        raise RuntimeError(f"{name}: получен нулевой PNG")
    print(f"OK: {name}.png ({size} байт)")


def main() -> None:
    requested = sys.argv[1:]
    names = requested if requested else list(EXAMPLES.keys())
    unknown = [n for n in names if n not in EXAMPLES]
    if unknown:
        print(f"Неизвестные примеры: {unknown}")
        sys.exit(2)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    failed: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        for name in names:
            try:
                generate_one(name, EXAMPLES[name], tmp_dir)
            except Exception as exc:  # noqa: BLE001 — report and continue
                print(f"FAIL: {name}: {exc}")
                failed.append(name)

    print(f"\nГотово: {len(names) - len(failed)}/{len(names)} успешно.")
    if failed:
        print("Не удалось сгенерировать:", failed)
        sys.exit(1)


if __name__ == "__main__":
    main()
