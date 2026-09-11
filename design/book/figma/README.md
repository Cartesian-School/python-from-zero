# Figma Handoff

Store Figma design-file links, page/node IDs, component mappings, review notes, and approved handoff metadata here.

Figma remains a design and review surface only. The canonical book pipeline remains the sole publishing implementation.

## v1 build — fixes complete, ready for Product Owner re-review

- **Figma file:** <https://www.figma.com/design/m19Q51E0vmVek8r4TCJCd8/Cartesian-School-%E2%80%94-Book-Design-System-v1>
- **File key:** `m19Q51E0vmVek8r4TCJCd8`
- **Status:** A live Product Owner review of the previous "complete" state found
  blocking visual defects — white background rectangles inside colored callouts, and
  text overflow/wrap issues on Chapter Opener, Code-Heavy Page, and Diagram & Callout
  Page. Both root causes (default-white auto-layout fills; missing text-wrap
  configuration) are identified and fixed; every frame was re-screenshotted and
  re-verified at the property level after the fix.
- A handful of secondary items (AntiPattern/Milestone callout variants,
  TableContinuation, a generic Figure component) remain intentionally deferred — see
  the build log for the exact list and how to extend them.
- Full build log, node/variable/component/style IDs, defect root causes and fixes, QA
  results, and deviations for Product Owner review: see
  [`HANDOFF-v1-build-log.md`](HANDOFF-v1-build-log.md).
