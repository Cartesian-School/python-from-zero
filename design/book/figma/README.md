# Figma Handoff

Store Figma design-file links, page/node IDs, component mappings, review notes, and approved handoff metadata here.

Figma remains a design and review surface only. The canonical book pipeline remains the sole publishing implementation.

## v1 build — vertical-sizing fix complete, ready for Product Owner re-review

- **Figma file:** <https://www.figma.com/design/m19Q51E0vmVek8r4TCJCd8/Cartesian-School-%E2%80%94-Book-Design-System-v1>
- **File key:** `m19Q51E0vmVek8r4TCJCd8`
- **Status:** Two rounds of live Product Owner review have found and fixed blocking
  defects. Round 1: white background rectangles inside colored callouts, and
  horizontal text-wrap issues. Round 2: text protruding below callout card bottoms —
  root cause was the outer `Callout` component's vertical axis being pinned `FIXED`
  instead of `HUG`, so cards couldn't grow when wrapped text needed more room. Fixed
  at the master-component level (propagates to all instances), verified with an
  RU/PL/EN language-robustness stress test, and re-screenshotted.
- A handful of secondary items (AntiPattern/Milestone callout variants,
  TableContinuation, a generic Figure component) remain intentionally deferred — see
  the build log for the exact list and how to extend them.
- Full build log, node/variable/component/style IDs, defect root causes and fixes, QA
  results, and deviations for Product Owner review: see
  [`HANDOFF-v1-build-log.md`](HANDOFF-v1-build-log.md).
