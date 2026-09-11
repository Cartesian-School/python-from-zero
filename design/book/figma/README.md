# Figma Handoff

Store Figma design-file links, page/node IDs, component mappings, review notes, and approved handoff metadata here.

Figma remains a design and review surface only. The canonical book pipeline remains the sole publishing implementation.

## v1 build — major professional refinement complete, ready for Product Owner review

- **Figma file:** <https://www.figma.com/design/m19Q51E0vmVek8r4TCJCd8/Cartesian-School-%E2%80%94-Book-Design-System-v1>
- **File key:** `m19Q51E0vmVek8r4TCJCd8`
- **Status:** Seven rounds of live Product Owner review/direction so far. Rounds 1-5
  covered callout surface/sizing fixes, the complete front/back matter system, and a
  systemic pt→px text-sizing bug (see below). Round 6 extracted the Cartesian School
  website's hero visual language into an 8-component vector-native
  `Book/Illustration/*` library. Round 7: replaced the Cover's abstract center mark
  with a faithful vector reproduction of the **real Python logo** (built from the
  site's own SVG source), expanded the illustration library to 27 components —
  including a `ProjectCard` set for all 13 real Cartesian School projects and an
  organized `LogoSet` — added a chapter-subject-tied topic badge to the Chapter
  Opener, gave two previously-bare pages (About Cartesian School, End Page) real
  brand identity, and re-audited every diagram/callout/front-back-matter page (no
  regressions found; round 6's fixes held). No screenshot/raster shortcuts were used
  anywhere.
- A few archetypes were evaluated and marked N/A/deferred because the underlying
  content doesn't exist yet (Conclusion, Glossary, References) — see the build log.
- Full build log, node/variable/component/style IDs, content-audit findings, defect
  root causes and fixes, QA results, recto/verso rules, and deviations for Product
  Owner review: see [`HANDOFF-v1-build-log.md`](HANDOFF-v1-build-log.md).
