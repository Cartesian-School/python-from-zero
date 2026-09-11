# Figma Handoff

Store Figma design-file links, page/node IDs, component mappings, review notes, and approved handoff metadata here.

Figma remains a design and review surface only. The canonical book pipeline remains the sole publishing implementation.

## v1 build — front/back matter system complete, ready for Product Owner review

- **Figma file:** <https://www.figma.com/design/m19Q51E0vmVek8r4TCJCd8/Cartesian-School-%E2%80%94-Book-Design-System-v1>
- **File key:** `m19Q51E0vmVek8r4TCJCd8`
- **Status:** Three rounds of live Product Owner review/direction so far. Round 1:
  white background rectangles inside colored callouts, horizontal text-wrap issues.
  Round 2: text protruding below callout card bottoms (fixed HUG-vertical sizing at
  the master-component level). Round 3: added the complete front matter (Cover,
  Title, Copyright, About Author, From Author, TOC + continuation) and back matter
  (Index, About Cartesian School, Colophon, End Page) system on two new pages, backed
  by a repository content audit so nothing was invented — real book title, author,
  license, Introduction text, and all 24 real chapter titles are used throughout.
  Completed the semantic Callout set to all 6 roles (added AntiPattern, Milestone).
- A few archetypes were evaluated and marked N/A/deferred because the underlying
  content doesn't exist yet (Conclusion, Glossary, References) — see the build log.
- Full build log, node/variable/component/style IDs, content-audit findings, defect
  root causes and fixes, QA results, recto/verso rules, and deviations for Product
  Owner review: see [`HANDOFF-v1-build-log.md`](HANDOFF-v1-build-log.md).
