# Figma Handoff

Store Figma design-file links, page/node IDs, component mappings, review notes, and approved handoff metadata here.

Figma remains a design and review surface only. The canonical book pipeline remains the sole publishing implementation.

## v1 build — final live cleanup complete, ready for Product Owner review

- **Figma file:** <https://www.figma.com/design/m19Q51E0vmVek8r4TCJCd8/Cartesian-School-%E2%80%94-Book-Design-System-v1>
- **File key:** `m19Q51E0vmVek8r4TCJCd8`
- **Status:** Five rounds of live Product Owner review/direction so far. Rounds 1-4
  covered callout surface/sizing fixes and the complete front/back matter system
  (see below). Round 5: re-audited a page-02-overlap report (not reproducible — the
  file was already clean), confirmed author-name spelling is 100% consistent, and —
  while checking Colophon readability — found and fixed a **systemic bug**: nearly
  every ad-hoc text element across the front/back matter system was missing this
  system's required pt→px conversion (1pt = 1.4111px), rendering ~41% smaller than
  intended everywhere. Fixed at the root across all affected components and pages,
  which in turn exposed and required fixing several latent layout overlaps the
  undersized text had been masking.
- A few archetypes were evaluated and marked N/A/deferred because the underlying
  content doesn't exist yet (Conclusion, Glossary, References) — see the build log.
- Full build log, node/variable/component/style IDs, content-audit findings, defect
  root causes and fixes, QA results, recto/verso rules, and deviations for Product
  Owner review: see [`HANDOFF-v1-build-log.md`](HANDOFF-v1-build-log.md).
