# Figma Handoff

Store Figma design-file links, page/node IDs, component mappings, review notes, and approved handoff metadata here.

Figma remains a design and review surface only. The canonical book pipeline remains the sole publishing implementation.

## v1 build — integrated cover/closing redesign complete, ready for Product Owner review

- **Figma file:** <https://www.figma.com/design/m19Q51E0vmVek8r4TCJCd8/Cartesian-School-%E2%80%94-Book-Design-System-v1>
- **File key:** `m19Q51E0vmVek8r4TCJCd8`
- **Status:** Eight rounds of live Product Owner review/direction so far. Rounds 1-5
  covered callout surface/sizing fixes, the complete front/back matter system, and a
  systemic pt→px text-sizing bug (see below). Round 6 extracted the Cartesian School
  website's hero visual language into an 8-component vector-native
  `Book/Illustration/*` library. Round 7 added a real vector Python logo, a
  `ProjectCard` set for all 13 real projects, and other library expansion — but its
  `LogoSet` Cartesian School mark was a hand-drawn approximation, not the real asset.
  Round 8: replaced that approximation with the actual repo assets from
  `cartesian_logo/` (a real vector import of `favicon.svg`, real raster lockups from
  `logo-full-*.png`/`logo_bar_*.png`); rebuilt the Cover's hero network as a single
  integrated, denser composition (panels pulled closer, short precise beams, a soft
  glow + grid atmosphere, enlarged to the page's content width) instead of four
  panels floating far from a tiny center badge; and rebuilt the End Page from a
  near-blank page into a proper dark closing spread sharing the Cover's exact
  background color and atmosphere. No screenshot/raster shortcuts were used for any
  illustration; the two logo assets use real vector/raster imports of the authentic
  brand files, never an invented substitute.
- A few archetypes were evaluated and marked N/A/deferred because the underlying
  content doesn't exist yet (Conclusion, Glossary, References) — see the build log.
- Full build log, node/variable/component/style IDs, content-audit findings, defect
  root causes and fixes, QA results, recto/verso rules, and deviations for Product
  Owner review: see [`HANDOFF-v1-build-log.md`](HANDOFF-v1-build-log.md).
