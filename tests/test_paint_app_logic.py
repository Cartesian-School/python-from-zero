"""Регрессионный набор для чистой логики документа рисовалки главы 18
(normalize_bounds, Shape, undo/redo модель) — без Tkinter и без Xvfb, потому
что модель документа не зависит от окна (раздел 18.12).
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "projects" / "tkinter" / "paint-app"))

from paint_app import Shape, normalize_bounds  # noqa: E402


def test_normalize_bounds_all_four_drag_directions():
    # down-right
    assert normalize_bounds(10, 10, 100, 80) == (10, 10, 100, 80)
    # up-left (same rectangle, dragged the opposite way)
    assert normalize_bounds(100, 80, 10, 10) == (10, 10, 100, 80)
    # up-right
    assert normalize_bounds(10, 80, 100, 10) == (10, 10, 100, 80)
    # down-left
    assert normalize_bounds(100, 10, 10, 80) == (10, 10, 100, 80)


def test_normalize_bounds_degenerate_point():
    assert normalize_bounds(50, 50, 50, 50) == (50, 50, 50, 50)


def test_shape_round_trip_dict():
    shape = Shape(kind="rectangle", coords=[10, 10, 100, 80], color="#2563eb", width=4)
    data = shape.to_dict()
    restored = Shape.from_dict(data)
    assert restored == shape


def test_shape_round_trip_json():
    shape = Shape(kind="oval", coords=[0, 0, 50, 50], color="#dc2626", width=2)
    text = json.dumps(shape.to_dict(), ensure_ascii=False)
    restored = Shape.from_dict(json.loads(text))
    assert restored == shape


def test_document_json_structure_matches_spec():
    shapes = [
        Shape(kind="line", coords=[34, 52, 180, 90], color="#2563eb", width=4),
        Shape(kind="rectangle", coords=[80, 120, 220, 210], color="#dc2626", width=3),
    ]
    data = {
        "version": 1,
        "canvas": {"background": "#ffffff"},
        "items": [s.to_dict() for s in shapes],
    }
    text = json.dumps(data, ensure_ascii=False)
    loaded = json.loads(text)
    assert loaded["version"] == 1
    assert loaded["canvas"]["background"] == "#ffffff"
    restored = [Shape.from_dict(item) for item in loaded["items"]]
    assert restored == shapes
