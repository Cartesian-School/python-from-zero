#!/usr/bin/env python3
"""Проверяет, что все скриншоты, ожидаемые главой 17, существуют в
site/assets/img/chapter-17/output/, не пустые и не случайный снимок 1×1.
Также проверяет несколько точечных регрессий финального visual-polish прохода
(терминальная семантика flowchart(), ширина object_diagram(), 3+3+2-раскладка
мини-досок в 17-16, сгенерированный HTML главы 17).

Использование: python3 scripts/validate_chapter_17_outputs.py
"""

import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "site" / "assets" / "img" / "chapter-17" / "output"
CHAPTER_DIR = ROOT / "site" / "chapters" / "glava-17"
sys.path.insert(0, str(ROOT / "scripts"))


def _load_site_lib():
    import site_lib
    return site_lib

REQUIRED_NAMES = [
    "basic-empty-board",
    "basic-first-move",
    "basic-win",
    "basic-draw",
    "basic-new-game-reset",
    "empty-board",
    "x-first-move",
    "x-turn",
    "o-turn",
    "mid-game",
    "x-win",
    "o-win",
    "winning-highlight",
    "draw",
    "hover-preview-x",
    "hover-preview-o",
    "scoreboard",
    "new-round",
    "new-match",
    "adaptive-board-small",
    "adaptive-board-large",
    "adaptive-board-comparison",
    "win-pulse-step-0",
    "win-pulse-step-1",
    "win-pulse-final",
    "tic-tac-toe-pro",
]

MIN_DIMENSION = 40  # anything smaller is almost certainly a capture bug, not a real window


def validate() -> list[str]:
    errors = []
    for name in REQUIRED_NAMES:
        path = OUT_DIR / f"{name}.png"
        if not path.exists():
            errors.append(f"Отсутствует обязательный скриншот: {path.relative_to(ROOT)}")
            continue
        try:
            with Image.open(path) as img:
                width, height = img.size
        except Exception as exc:  # noqa: BLE001 - report and keep validating the rest
            errors.append(f"Не удалось открыть {path.relative_to(ROOT)}: {exc}")
            continue
        if width < MIN_DIMENSION or height < MIN_DIMENSION:
            errors.append(f"{path.relative_to(ROOT)}: подозрительно маленький снимок {width}x{height}")
    errors.extend(_validate_adaptive_pair())
    errors.extend(_validate_flowchart_terminal_semantics())
    errors.extend(_validate_object_diagram_width())
    errors.extend(_validate_winning_lines_layout())
    errors.extend(_validate_visual_coverage())
    return errors


def _validate_flowchart_terminal_semantics() -> list[str]:
    """17-17's terminal-state diagram (and any other flowchart() caller using
    kind="end" inside a decision branch) must never draw an arrow OUT of a
    terminal node — that was exactly the "false merge" bug in Fix 2/11.
    Exercises the shared helper directly with synthetic cases, independent of
    any particular chapter's wording."""
    site_lib = _load_site_lib()
    errors = []

    both_terminal = site_lib.flowchart([
        {"kind": "decision", "label": "q?",
         "yes": [{"kind": "end", "label": "A"}],
         "no": [{"kind": "end", "label": "B"}]},
    ])
    arrows = both_terminal.count("marker-end")
    if arrows != 2:
        errors.append(
            f"flowchart(): decision with BOTH branches terminal should draw exactly 2 arrows "
            f"(one into each branch, no merge) — got {arrows}."
        )

    one_terminal = site_lib.flowchart([
        {"kind": "decision", "label": "q?",
         "yes": [{"kind": "end", "label": "A"}],
         "no": [{"kind": "process", "label": "B"}, {"kind": "process", "label": "C"}]},
    ])
    arrows2 = one_terminal.count("marker-end")
    # into yes-branch (1) + into no-branch (1) + B->C straight arrow (1) = 3;
    # no extra merge/stub arrow past C, since only one branch continues.
    if arrows2 != 3:
        errors.append(
            f"flowchart(): decision with ONE terminal branch should draw exactly 3 arrows "
            f"(into each branch + the continuing chain, no dangling merge stub) — got {arrows2}."
        )
    return errors


def _validate_object_diagram_width() -> list[str]:
    """17-08/17-13 rely on object_diagram(width=...) actually widening the
    box — otherwise long rows (the Event field list, the 9-element board)
    wrap or get clipped again."""
    site_lib = _load_site_lib()
    errors = []
    narrow = site_lib.object_diagram("s", "S", [("a", "x")])
    wide = site_lib.object_diagram("s", "S", [("a", "x")], width=560)

    def _viewbox_width(svg: str) -> float:
        marker = 'viewBox="0 0 '
        start = svg.index(marker) + len(marker)
        end = svg.index(" ", start)
        return float(svg[start:end])

    if not _viewbox_width(wide) > _viewbox_width(narrow):
        errors.append("object_diagram(width=...) does not widen the SVG viewBox as expected.")
    return errors


def _validate_winning_lines_layout() -> list[str]:
    """17-16 must render all 8 mini-boards as 8 separate board_diagram()
    cards grouped 3+3+2 (rows/columns/diagonals), not one flat 8-item grid
    that can overlap at in-between viewport widths."""
    path = CHAPTER_DIR / "17-16-vosem-linij-pobedy.html"
    if not path.exists():
        return []  # covered by the wider site build; nothing to check yet
    html_text = path.read_text(encoding="utf-8")
    errors = []
    board_card_count = html_text.count('grid-template-columns:repeat(3,56px)')
    if board_card_count != 8:
        errors.append(f"17-16: expected 8 board_diagram() mini-boards, found {board_card_count}.")
    for label in ("Строки", "Столбцы", "Диагонали"):
        if f">{label}<" not in html_text:
            errors.append(f"17-16: missing group heading {label!r} — 3+3+2 grouping not rendered.")
    return errors


def _validate_adaptive_pair() -> list[str]:
    """17-21 claims the board genuinely grows with the window — the two
    source screenshots must actually differ in size, not just in filename,
    and the composed comparison image must actually contain both of them
    at their true, unscaled relative size (not independently normalized to
    equal widths, which was the bug this composite was built to fix)."""
    small_path = OUT_DIR / "adaptive-board-small.png"
    large_path = OUT_DIR / "adaptive-board-large.png"
    comparison_path = OUT_DIR / "adaptive-board-comparison.png"
    if not small_path.exists() or not large_path.exists():
        return []  # already reported as missing above
    with Image.open(small_path) as small_img, Image.open(large_path) as large_img:
        sw, sh = small_img.size
        lw, lh = large_img.size
    errors = []
    if not (lw > sw and lh > sh):
        errors.append(
            f"adaptive-board-large.png ({lw}x{lh}) должен быть крупнее adaptive-board-small.png "
            f"({sw}x{sh}) по обеим осям — иначе скриншоты не доказывают, что поле адаптивно."
        )
    if not comparison_path.exists():
        return errors  # already reported as missing above
    with Image.open(comparison_path) as comp_img:
        cw, ch = comp_img.size
    # The composite places both source images unscaled side by side with
    # padding/gaps — its canvas must be at least as wide as both images
    # combined and at least as tall as the taller one, or one of them was
    # cropped/rescaled instead of placed at true size.
    if cw < sw + lw:
        errors.append(
            f"adaptive-board-comparison.png ({cw}x{ch}) уже, чем сумма ширин двух исходных "
            f"скриншотов ({sw}+{lw}={sw + lw}) — похоже, один из них был обрезан или уменьшен."
        )
    if ch < max(sh, lh):
        errors.append(
            f"adaptive-board-comparison.png ({cw}x{ch}) ниже, чем более высокий исходный "
            f"скриншот ({max(sh, lh)}) — похоже, один из них был обрезан или уменьшен."
        )
    return errors


def _validate_visual_coverage() -> list[str]:
    """Required game states must be visible on the lessons that teach them,
    not merely generated and left unused in the asset directory."""
    required_by_page = {
        "17-13-model-sostoyaniya.html": ("x-turn.png", "o-turn.png", "mid-game.png"),
        "17-15-algoritm-hoda.html": ("empty-board.png", "x-first-move.png"),
        "17-17-pobeda-nichya-terminal.html": ("x-win.png", "o-win.png", "draw.png"),
        "17-23-hover-preview.html": ("hover-preview-x.png", "hover-preview-o.png"),
        "17-27-new-round-vs-new-match.html": ("new-round.png", "new-match.png"),
        "17-21-adaptivnoe-pole.html": ("adaptive-board-comparison.png",),
    }
    errors = []
    for page_name, image_names in required_by_page.items():
        page_path = CHAPTER_DIR / page_name
        if not page_path.exists():
            errors.append(f"Отсутствует страница для проверки визуального покрытия: {page_name}")
            continue
        html_text = page_path.read_text(encoding="utf-8")
        for image_name in image_names:
            if image_name not in html_text:
                errors.append(f"{page_name}: обязательный визуальный checkpoint {image_name} не показан.")
    return errors


def main() -> None:
    errors = validate()
    if errors:
        print(f"Скриншоты главы 17 невалидны — найдено ошибок: {len(errors)}\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    print(f"Скриншоты главы 17 валидны: {len(REQUIRED_NAMES)} файлов проверено.")


if __name__ == "__main__":
    main()
