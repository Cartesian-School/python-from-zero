"""Regression guard for a real data-loss bug found in M02-I07 Phase 2B's
production-integrity amendment: ``scripts/build_polish_course.py``'s
``build()`` used to call ``shutil.rmtree(PL_ROOT)`` unconditionally at its
very top, even in ``--collect`` mode — a supposedly diagnostic, read-mostly
pass. Running it once deleted the entire committed ``site/pl/`` tree (1655
files) before crashing on the first source string with no cached PL
translation, with no rollback. Restored via ``git restore site/pl/`` at the
time; this test exists so that mode can never regress to being destructive
again.

Tests the extracted ``_reset_pl_root()`` helper directly, against a
throwaway temp directory — not the real ``site/pl/`` — so this stays fast
and never touches real repository content.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load_build_polish_course() -> ModuleType:
    """Load scripts/build_polish_course.py directly, without making scripts
    a package (same approach as tests/test_license_consistency.py)."""
    sys.path.insert(0, str(ROOT / "scripts"))
    spec = importlib.util.spec_from_file_location(
        "build_polish_course", ROOT / "scripts" / "build_polish_course.py"
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    # Must be registered before exec_module(): the module defines a
    # @dataclass, and dataclasses.py resolves annotations via
    # sys.modules[cls.__module__] — it would otherwise raise AttributeError
    # on a None lookup.
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def build_polish_course() -> ModuleType:
    return _load_build_polish_course()


def test_reset_pl_root_never_deletes_in_collect_mode(build_polish_course, tmp_path, monkeypatch) -> None:
    fake_pl_root = tmp_path / "pl"
    fake_pl_root.mkdir()
    marker = fake_pl_root / "index.html"
    marker.write_text("currently-published PL homepage", encoding="utf-8")
    nested = fake_pl_root / "chapters" / "rozdzial-01" / "index.html"
    nested.parent.mkdir(parents=True)
    nested.write_text("currently-published PL chapter opener", encoding="utf-8")

    monkeypatch.setattr(build_polish_course, "PL_ROOT", fake_pl_root)

    build_polish_course._reset_pl_root(collect=True)

    assert fake_pl_root.exists(), "--collect must never delete the PL root"
    assert marker.exists()
    assert marker.read_text(encoding="utf-8") == "currently-published PL homepage"
    assert nested.exists()


def test_reset_pl_root_clears_in_normal_mode(build_polish_course, tmp_path, monkeypatch) -> None:
    """The normal (non-collect) full-rebuild path is unchanged: it still
    clears site/pl/ before regenerating it from scratch."""
    fake_pl_root = tmp_path / "pl"
    fake_pl_root.mkdir()
    (fake_pl_root / "index.html").write_text("stale content", encoding="utf-8")

    monkeypatch.setattr(build_polish_course, "PL_ROOT", fake_pl_root)

    build_polish_course._reset_pl_root(collect=False)

    assert not fake_pl_root.exists()


def test_reset_pl_root_is_a_noop_when_pl_root_is_missing(build_polish_course, tmp_path, monkeypatch) -> None:
    """Neither mode should raise if site/pl/ doesn't exist yet (e.g. a
    fresh checkout before the PL course has ever been built)."""
    fake_pl_root = tmp_path / "does-not-exist"
    monkeypatch.setattr(build_polish_course, "PL_ROOT", fake_pl_root)

    build_polish_course._reset_pl_root(collect=True)
    build_polish_course._reset_pl_root(collect=False)

    assert not fake_pl_root.exists()
