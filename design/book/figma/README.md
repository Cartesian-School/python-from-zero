# Figma Handoff

Store Figma design-file links, page/node IDs, component mappings, review notes, and approved handoff metadata here.

Figma remains a design and review surface only. The canonical book pipeline remains the sole publishing implementation.

## v1 build — End Page complete rebuild finished, ready for Product Owner review

- **Figma file:** <https://www.figma.com/design/m19Q51E0vmVek8r4TCJCd8/Cartesian-School-%E2%80%94-Book-Design-System-v1>
- **File key:** `m19Q51E0vmVek8r4TCJCd8`
- **Status:** Eleven rounds of live Product Owner review/direction so far. Rounds
  1-5 covered callout surface/sizing fixes, the complete front/back matter system,
  and a systemic pt→px text-sizing bug (see below). Round 6 extracted the Cartesian
  School website's hero visual language into an 8-component vector-native
  `Book/Illustration/*` library. Round 7 added a real vector Python logo and a
  `ProjectCard` set for all 13 real projects. Round 8 replaced a hand-drawn
  Cartesian School mark approximation with the actual repo assets from
  `cartesian_logo/`. Round 9 corrected the About Cartesian School page's brand
  treatment and rebuilt the QA-only Book Sequence Overview diagram. Round 10 added
  a publication-identifier utility panel and a real, `pyzbar`-verified QR code.
  Round 11: the End Page was rejected outright (compressed layout, dominant grid,
  thumbnail portrait, too-short bio, floating QR, giant white barcode slab) — torn
  down completely and rebuilt as three integrated zones: a substantial authorial
  closing (large real portrait, a 114-word verified biography, a real expertise
  line), a real book summary, and a Cartesian School closing identity with the real
  lockup, real institutional copy, and the QR code properly integrated rather than
  floating; the ISSN/barcode block was redesigned into a compact 190×54 "publisher
  imprint" module. Also corrected the author's Russian name (`Siergej Sobolewski` →
  `Сергей Соболевский`) across all 9 reader-facing occurrences file-wide. No
  screenshot/raster shortcuts were used for any illustration; every photograph,
  logo asset, and code (QR/barcode) is either a real sourced file from the repo or
  a genuinely functional/credible generated asset, never an invented or decorative
  substitute.
- A few archetypes were evaluated and marked N/A/deferred because the underlying
  content doesn't exist yet (Conclusion, Glossary, References) — see the build log.
- Full build log, node/variable/component/style IDs, content-audit findings, defect
  root causes and fixes, QA results, recto/verso rules, and deviations for Product
  Owner review: see [`HANDOFF-v1-build-log.md`](HANDOFF-v1-build-log.md).
