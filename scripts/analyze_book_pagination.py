#!/usr/bin/env python3
"""Canonical PDF pagination diagnostics CLI (M02-I07 Phase 2A — diagnostic only).

    python scripts/analyze_book_pagination.py --language ru
    python scripts/analyze_book_pagination.py --language pl
    python scripts/analyze_book_pagination.py --all
    python scripts/analyze_book_pagination.py --language ru --render-experiments

Reads the already-built PDF and its pagination sidecar for the requested
language (fails clearly if either is missing) and writes a machine-readable
JSON report to evidence/m02-i07-pagination-diagnostics-<language>.json.
``--render-experiments`` additionally re-renders the book with individual
CSS pagination rules swapped, one at a time, to MEASURE their exact
page-count cost (slow: ~10-15 minutes per language). This tool never writes
to a publication artifact and never changes pagination behavior — see
scripts/book_pipeline/pagination_diagnostics.py.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from book_pipeline import SUPPORTED_LANGUAGES
from book_pipeline.pagination_diagnostics import analyze

EVIDENCE_DIR = ROOT / "evidence"


def _run(language: str, *, render_experiments: bool) -> Path:
    print(f"Analyzing {language} pagination ({'with' if render_experiments else 'without'} render experiments)...")
    report = analyze(language, run_render_experiments_flag=render_experiments)
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    out_path = EVIDENCE_DIR / f"m02-i07-pagination-diagnostics-{language}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    totals = report["totals"]
    print(
        f"  {language}: {totals['total_pages']} pages, "
        f"{totals['blank_pages']} zero-text (raw extraction), "
        f"{totals['body_effectively_empty_pages']} body-effectively-empty (chrome-stripped), "
        f"{totals['near_empty_pages']} near-empty, "
        f"median {totals['median_words_per_page']} words/page"
    )
    print(f"  Wrote: {out_path.relative_to(ROOT)}")
    return out_path


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--language", choices=sorted(SUPPORTED_LANGUAGES))
    parser.add_argument("--all", action="store_true", help="Analyze every supported language")
    parser.add_argument(
        "--render-experiments",
        action="store_true",
        help="Additionally measure exact page-count deltas via controlled counterfactual re-renders (slow)",
    )
    args = parser.parse_args(sys.argv[1:] if argv is None else argv)

    if args.all == bool(args.language):
        parser.error("pass exactly one of --language or --all")

    languages = SUPPORTED_LANGUAGES if args.all else (args.language,)
    for language in languages:
        _run(language, render_experiments=args.render_experiments)


if __name__ == "__main__":
    main()
