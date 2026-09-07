#!/usr/bin/env python3
"""Inject exact route-manifest RU/PL switchers into every localized pair."""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from localization import ROOT, Routes

CSS = '<link rel="stylesheet" href="/assets/css/localization.css" />'
SWITCHER_RE = re.compile(
    r'<nav(?=[^>]*\bclass="language-switcher")[^>]*>.*?</nav>', re.S
)
EMPTY_DESKTOP_RE = re.compile(
    r'[ \t\r\n]*<div class="language-switcher-desktop">\s*</div>[ \t\r\n]*'
)


def _remove_empty_desktop_div(match: "re.Match[str]") -> str:
    """Collapse the empty desktop-switcher div together with whatever
    whitespace-only runs flank it into one canonical run.

    Deleting just the div (leaving its neighbors alone) can splice two
    previously separate — and separately parser-normalized — whitespace
    runs into one new adjacent run that nothing has canonicalized yet.
    PR #117: the homepage template places this div *before* the
    nav-toggle button (every other page's template places it after,
    right where ``_collapse_blank_run_before`` below already handles the
    equivalent merge before ``</header>``), so removing it left a bare
    newline (from before the div) directly adjacent to a bare space (from
    after the div) — "\\n " right before ``<button>`` — whose exact
    byte count stdlib html.parser does not treat as part of any stable
    contract (confirmed to already vary for this exact node between local
    and CI CPython patch releases). Collapsing the whole removed span
    (div plus its flanking whitespace) to a single canonical run — a bare
    newline if any part of the removed span contained one, otherwise a
    single space — fixes this at the exact point of removal, without
    touching any of the surrounding hand-authored RU/PL markup.
    """
    removed = match.group(0)
    return "\n" if "\n" in removed else (" " if removed else "")


def _collapse_blank_run_before(source: str, literal: str) -> str:
    """Collapse any run of blank/whitespace-only lines right before ``literal``
    to a single newline.

    Removing an already-injected switcher (via ``SWITCHER_RE``/
    ``EMPTY_DESKTOP_RE`` below) leaves the newline that used to separate it
    from its neighbours in place. Re-running this script on its own prior
    output therefore left one extra blank line behind each time, silently
    accumulating across repeated builds. Collapsing the whole run before
    every fresh injection keeps the operation idempotent regardless of how
    many times it has already run.
    """
    pattern = re.compile(r"(?:\r?\n[ \t]*)+(?=" + re.escape(literal) + r")")
    return pattern.sub("\n", source)


def _inject(path: Path, switcher: str) -> None:
    source = SWITCHER_RE.sub("", path.read_text(encoding="utf-8"))
    source = EMPTY_DESKTOP_RE.sub(_remove_empty_desktop_div, source)
    source = _collapse_blank_run_before(source, "</header>")
    if not re.search(r'<link[^>]+href="/assets/css/localization\.css"[^>]*>', source):
        source = source.replace("</head>", CSS + "\n</head>", 1)
    desktop = f'<div class="language-switcher-desktop">{switcher}</div>'
    if "</header>" not in source:
        raise ValueError(f"Localized page has no header: {path}")
    source = source.replace("</header>", desktop + "\n</header>", 1)
    mobile = re.search(r'(<nav(?=[^>]*\bid="mobile-nav-panel")[^>]*>.*?</nav>)', source, re.S)
    if mobile:
        panel = _collapse_blank_run_before(mobile.group(1), "</nav>")
        panel = panel.replace("</nav>", switcher + "\n</nav>", 1)
        source = source[:mobile.start()] + panel + source[mobile.end():]
    path.write_text(source, encoding="utf-8")


def main() -> None:
    routes = Routes()
    changed = 0
    for page_id, page in routes.pages.items():
        variants = routes.available(page_id)
        if not {"ru", "pl"} <= variants.keys():
            continue
        for locale in ("ru", "pl"):
            _inject(ROOT / "site" / variants[locale].lstrip("/"), routes.switcher(page_id, locale))
            changed += 1
    print(f"Language switchers injected into {changed} localized documents")


if __name__ == "__main__":
    main()
