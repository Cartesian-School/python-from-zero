# Course path PCB rework

Base: `e054d2fd8222dfccd028bad86a2e45da8e5692e1`, including Claude's merged PR #101 (`b7ac98e`).

The supplied attachment contained the task, but no Product Owner screenshot. The before image was captured from the unchanged base implementation at 1440×900. The after images show the same roadmap further down the section to expose several connected modules.

- [Before, current main](before-1440.png)
- [After, desktop](after-1440.png)
- [After, mobile](after-390.png)
- [Motion, first eight-second cycle](cycle-1.png)
- [Motion, second eight-second cycle](cycle-2.png)

## Source classification

KEEP: `.journey-node`, semantic `.jn-card` links, chapter titles, metadata, lesson IDs, state badges, `.jn-progress-fill`, summary fields, and the real progress aggregation contract.

MODIFY: the card body, status colors, mounted depth, progress conductor, summary module, and responsive chapter layout. Four families use `data-module`; the catalog validator's exact class/attribute prefix is preserved. Current state gains `aria-current="step"`; the next node receives only a decorative preview class.

DELETE: `.glavy__geometry`, `.journey-rail::before/::after`, `.jn-dot::before`, the old `.jn-card::before` stripe, `journey-signal-travel`, and `chip-led-pulse`. Source search finds no remaining references to these rejected decorations. The separate four-stage course overview's `.course-path__signal` remains in use and is unrelated to the 24-chapter roadmap.

## Visual and functional contract

One decorative SVG routing pattern supplies 18 orthogonal traces in six parallel routing groups, 24 circular vias per tile, two IC footprints, resistors, a capacitor, a connector header, and small silkscreen identifiers. It repeats without stretching circular vias. Each chapter adds two local vias, four side contacts, three edge pads, and two orthogonal routes. A three-conductor central bus connects the master status module to the chapter network.

The desktop alternates modules; at 860px and below the bus moves left and the modules use one column. The eight requested viewports (1920×1080, 1440×900, 1280×800, 1024×900, 768×1024, 430×932, 390×844, 360×800) were captured and visually inspected, with no horizontal overflow, clipped modules, or text collisions.

The current chapter alone carries the travelling packet. Its eight-second CSS cycle is shared with the LED/contact/edge response. The packet is visible immediately on the incoming bus and its displacement is tested at 1.1 seconds. Two complete cycles were captured at half-second intervals and visually reviewed: inbound bus → active contacts → outbound bus. A weaker next-route preview follows. Completed modules remain static green; theory-only modules have no practical conductor or fabricated completion state. Reduced motion disables all board animation and preserves a static packet and current-state prominence. No animation loop or progress writes were introduced.

The browser contract covers all 24 canonical titles/routes, real seeded completion, partial completion/current state, theory-only state, the fully completed course, keyboard focus, no-JavaScript links, reduced motion, live animation, and actual connector geometry at every requested viewport. Seeded progress exists only in isolated browser tests.

## Verification commands

```sh
python scripts/build_site_index.py
bash scripts/build_vercel.sh
npm --prefix web run test:pcb
npm --prefix web run test:homepage
npm --prefix web run test:redesign
npm --prefix web run test:author
xvfb-run -a python -m pytest tests/ projects/python/safesort/tests/
python scripts/validate_book.py
python scripts/validate_ru_content_review.py --require-records --require-complete-scope
git diff --check
```

Local evidence: PCB 47 assertions; homepage 471 assertions; Projects/Reference 723 assertions; Author Profile 154 assertions; repository/SafeSort 267 tests (182 + 85). Full non-portable site build passes navigation, catalog, canonical-title, pagination, source, chapter, and SEO checks. The publication validator passes all 4,575 PDF pages, 1,221 bookmarks and EPUBCheck with zero errors. Running every generator in CI order, followed by SEO/sitemap/LLMs generation, leaves every tracked file byte-identical.

## M01 merge blocker inherited from main (resolved)

The complete M01 validator originally failed with **31 hash-binding diagnostics across 27 records** (24 chapter openers and three front-matter records), reproduced identically on untouched base main — this was a pre-existing, repo-wide staleness issue from the author redesign (`9d84f5bca29c8b1786eb6a4a04daa27d0ab5d69f`), unrelated to this branch's changes. [Historical diagnostics](m01-failures.txt) are kept for context.

This was repaired separately on `main` in PR #103 (`fix/m01-review-checksum-resync`, merged as `3adec5920e2ffaa4d4c41d74a9a6ccc8de595fda`): 26 records received a mechanical checksum/status-machine resync (their reviewed content was byte-identical; only pagination/shared-file artifacts moved), and `supplementary_ob-avtore-r001.json` received a genuine content re-review, since its content substantively changed. No validator was weakened and no record was fabricated. This branch is now rebased onto that repaired `main`, and `python scripts/validate_ru_content_review.py --require-records --require-complete-scope` passes: `records=1158; inventory_units=1158`.
