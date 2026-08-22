#!/usr/bin/env python3
"""Генерирует настоящие скриншоты первого прототипа snake_basic.py — тот
самый код, который описывают разделы 19.1–19.8 (без «Рекорд» на табло,
серые сегменты тела). Отдельный процесс от generate_chapter_19_outputs.py:
turtle.Screen.bye() необратимо «отравляет» весь процесс (turtle.Terminator
на любом следующем update()), поэтому snake.py (Pro) и snake_basic.py не
могут по очереди делить один и тот же интерпретатор — этот файл открывает
ОДНО окно на весь запуск и сбрасывает состояние прямыми присваиваниями
переменным модуля между сценариями, вместо перезапуска окна.

Требует headless X-сервер (xvfb-run).
Использование: xvfb-run -a python3 scripts/generate_chapter_19_basic_outputs.py
"""

import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageGrab

_LABEL_FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-19" / "output"
sys.path.insert(0, str(ROOT / "projects" / "turtle" / "snake"))

import snake_basic as m  # noqa: E402

WIN_W, WIN_H = 600, 600


def _autocrop(img: Image.Image) -> Image.Image:
    rgb = img.convert("RGB")
    bg = Image.new("RGB", rgb.size, (0, 0, 0))
    bbox = ImageChops.difference(rgb, bg).getbbox()
    return img.crop(bbox) if bbox else img


def capture(name: str) -> None:
    m.screen.update()
    img = ImageGrab.grab(bbox=(0, 0, WIN_W, WIN_H))
    img = _autocrop(img)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{name}.png"
    img.save(path)
    print(f"Сохранено: {path.relative_to(ROOT)} ({img.size[0]}x{img.size[1]})")


def reset() -> None:
    m.golova.goto(0, 0)
    m.napravlenie = "stop"
    m.schet = 0
    m.igra_okonchena = False
    for segment in m.segmenty:
        segment.hideturtle()
    m.segmenty.clear()
    m.novoe_yabloko()
    m.obnovit_tablo()


def compose_strip(names: list[str], out_name: str, labels: list[str]) -> None:
    imgs = [Image.open(OUT_DIR / f"{n}.png").convert("RGB") for n in names]
    h = max(im.height for im in imgs)
    gap = 56
    total_w = sum(im.width for im in imgs) + gap * (len(imgs) - 1)
    strip = Image.new("RGB", (total_w, h + 36), "#0D0230")
    draw = ImageDraw.Draw(strip)
    x = 0
    for i, im in enumerate(imgs):
        strip.paste(im, (x, 0))
        text_w = draw.textlength(labels[i], font=_LABEL_FONT)
        draw.text((x + im.width / 2 - text_w / 2, h + 8), labels[i], fill="#FFFFFF", font=_LABEL_FONT)
        x += im.width
        if i < len(imgs) - 1:
            mid_y = h // 2
            draw.line([(x + 10, mid_y), (x + gap - 10, mid_y)], fill="#B9A0FC", width=4)
            draw.polygon([(x + gap - 10, mid_y - 8), (x + gap - 10, mid_y + 8), (x + gap, mid_y)], fill="#B9A0FC")
            x += gap
    path = OUT_DIR / f"{out_name}.png"
    strip.save(path)
    print(f"Сохранено: {path.relative_to(ROOT)} ({strip.size[0]}x{strip.size[1]})")


def empty_field() -> None:
    reset()
    capture("snake-basic-empty-field")


def head_food() -> None:
    reset()
    m.yabloko.goto(60, 0)
    m.screen.update()
    capture("snake-basic-head-food")


def moving() -> None:
    reset()
    m.napravlenie = "right"
    for _ in range(4):
        m.dvigat_telo()
        m.dvigat_golovu()
    m.screen.update()
    capture("snake-basic-moving")


def eaten() -> None:
    reset()
    m.napravlenie = "right"
    m.yabloko.goto(m.RAZMER_SHAGA, 0)
    m.screen.update()
    capture("snake-basic-eaten-before")
    m.dvigat_telo()
    m.dvigat_golovu()
    m.proverit_edu()
    m.screen.update()
    capture("snake-basic-eaten-after")
    compose_strip(
        ["snake-basic-eaten-before", "snake-basic-eaten-after"],
        "snake-basic-eaten-strip",
        ["до", "после"],
    )


def collision() -> None:
    reset()
    m.golova.goto(m.GRANICA + 10, 0)
    m.proverit_stolknoveniya()
    m.screen.update()
    assert m.igra_okonchena is True
    capture("snake-basic-collision")


def full_game() -> None:
    reset()
    m.napravlenie = "right"
    for _ in range(3):
        m.yabloko.goto(m.golova.xcor() + m.RAZMER_SHAGA, m.golova.ycor())
        m.dvigat_telo()
        m.dvigat_golovu()
        m.proverit_edu()
    m.dvigat_telo()
    m.dvigat_golovu()
    m.screen.update()
    assert len(m.segmenty) == 3
    capture("snake-basic-full-game")


if __name__ == "__main__":
    empty_field()
    head_food()
    moving()
    eaten()
    collision()
    full_game()
    m.screen.bye()
