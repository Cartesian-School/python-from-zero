# Figma Handoff

Store Figma design-file links, page/node IDs, component mappings, review notes, and approved handoff metadata here.

Figma remains a design and review surface only. The canonical book pipeline remains the sole publishing implementation.

## v1 build — brand-aligned visual refinement complete, ready for Product Owner review

- **Figma file:** <https://www.figma.com/design/m19Q51E0vmVek8r4TCJCd8/Cartesian-School-%E2%80%94-Book-Design-System-v1>
- **File key:** `m19Q51E0vmVek8r4TCJCd8`
- **Status:** Six rounds of live Product Owner review/direction so far. Rounds 1-5
  covered callout surface/sizing fixes, the complete front/back matter system, and a
  systemic pt→px text-sizing bug (see below). Round 6: extracted the Cartesian
  School website's actual hero visual language (a real node/connector network,
  coordinate grid, and technical panels — CSS/hex values pulled directly from
  `cartesianschool.org`, not eyeballed) into a new vector-native
  `Book/Illustration/*` library (new page `06 — Illustration Library`), redesigned
  the Cover around a `HeroNetwork` instance, added a themed accent to the Chapter
  Opener, fixed a real diagram-connector misalignment and an uncontrolled
  callout-grid height mismatch found during re-audit, and rebuilt the QA page's
  sequence diagram at a legible size. No screenshot/raster shortcuts were used
  anywhere.
- A few archetypes were evaluated and marked N/A/deferred because the underlying
  content doesn't exist yet (Conclusion, Glossary, References) — see the build log.
- Full build log, node/variable/component/style IDs, content-audit findings, defect
  root causes and fixes, QA results, recto/verso rules, and deviations for Product
  Owner review: see [`HANDOFF-v1-build-log.md`](HANDOFF-v1-build-log.md).
