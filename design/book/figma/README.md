# Figma Handoff

Store Figma design-file links, page/node IDs, component mappings, review notes, and approved handoff metadata here.

Figma remains a design and review surface only. The canonical book pipeline remains the sole publishing implementation.

## v1 build — final art-direction pass complete, ready for Product Owner review

- **Figma file:** <https://www.figma.com/design/m19Q51E0vmVek8r4TCJCd8/Cartesian-School-%E2%80%94-Book-Design-System-v1>
- **File key:** `m19Q51E0vmVek8r4TCJCd8`
- **Status:** Nine rounds of live Product Owner review/direction so far. Rounds 1-5
  covered callout surface/sizing fixes, the complete front/back matter system, and a
  systemic pt→px text-sizing bug (see below). Round 6 extracted the Cartesian School
  website's hero visual language into an 8-component vector-native
  `Book/Illustration/*` library. Round 7 added a real vector Python logo and a
  `ProjectCard` set for all 13 real projects. Round 8 replaced a hand-drawn
  Cartesian School mark approximation with the actual repo assets from
  `cartesian_logo/`, and rebuilt the Cover's hero network and the End Page as a
  denser, atmospheric, tonally-matched pair. Round 9: corrected the About Cartesian
  School page's brand treatment (a lone icon read as an app icon, not a publisher
  imprint — now the real horizontal lockup); rebuilt the QA-only Book Sequence
  Overview diagram, which had a genuine geometry bug (connectors anchored well below
  the boxes they should join), into one precisely-connected 3-phase flow; and
  rebuilt the End Page again — from "logo + URL" into a real editorial closing page
  carrying the actual author photograph, a real book summary, a real author bio, and
  the Cartesian School identity. Added the real author portrait and the real Guido
  van Rossum portrait (the same file already used in the book's own Chapter 1) to a
  new, separate "Editorial / Photographic Assets" tier in the illustration library.
  No screenshot/raster shortcuts were used for any illustration; every photograph
  and logo asset is a real, sourced file from the repo, never an invented
  substitute.
- A few archetypes were evaluated and marked N/A/deferred because the underlying
  content doesn't exist yet (Conclusion, Glossary, References) — see the build log.
- Full build log, node/variable/component/style IDs, content-audit findings, defect
  root causes and fixes, QA results, recto/verso rules, and deviations for Product
  Owner review: see [`HANDOFF-v1-build-log.md`](HANDOFF-v1-build-log.md).
