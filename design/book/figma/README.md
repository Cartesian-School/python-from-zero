# Figma Handoff

Store Figma design-file links, page/node IDs, component mappings, review notes, and approved handoff metadata here.

Figma remains a design and review surface only. The canonical book pipeline remains the sole publishing implementation.

## v1 build — futuristic engineering art-direction pass finished, ready for Product Owner review

- **Figma file:** <https://www.figma.com/design/m19Q51E0vmVek8r4TCJCd8/Cartesian-School-%E2%80%94-Book-Design-System-v1>
- **File key:** `m19Q51E0vmVek8r4TCJCd8`
- **Status:** Twelve rounds of live Product Owner review/direction so far. Rounds
  1-5 covered callout surface/sizing fixes, the complete front/back matter system,
  and a systemic pt→px text-sizing bug (see below). Round 6 extracted the Cartesian
  School website's hero visual language into an 8-component vector-native
  `Book/Illustration/*` library. Round 7 added a real vector Python logo and a
  `ProjectCard` set for all 13 real projects. Round 8 replaced a hand-drawn
  Cartesian School mark approximation with the actual repo assets from
  `cartesian_logo/`. Round 9 corrected the About Cartesian School page's brand
  treatment and rebuilt the QA-only Book Sequence Overview diagram. Round 10 added
  a publication-identifier utility panel and a real, `pyzbar`-verified QR code.
  Round 11 rebuilt the End Page from scratch (real portrait, a 114-word verified
  biography, a real book summary, a compact ISSN/barcode module) and corrected the
  author's Russian name (`Siergej Sobolewski` → `Сергей Соболевский`) across all 9
  reader-facing occurrences file-wide. Round 12: pushed the system further toward a
  futuristic engineering language — a vector-native PCB/motherboard circuit-trace
  background now fills the Cover's previously-empty side margins and top/bottom
  strips (confined outside the text column, so contrast is unaffected), and the End
  Page's author portrait gained a cybernetic corner-bracket frame with node points
  and a leader-line tag. Also found and fixed a real Figma-API gotcha along the way
  (reassigning `vectorPaths` on an existing, already-positioned vector compounds
  the new coordinates onto its current offset instead of placing them fresh — this
  had displaced a leader-line segment into the middle of unrelated body text; now
  documented as a standing rule: delete and recreate rather than reassign in
  place). No screenshot/raster shortcuts were used for any illustration; every
  photograph, logo asset, and code (QR/barcode) is either a real sourced file from
  the repo or a genuinely functional/credible generated asset, never an invented or
  decorative substitute.
- A few archetypes were evaluated and marked N/A/deferred because the underlying
  content doesn't exist yet (Conclusion, Glossary, References) — see the build log.
- Full build log, node/variable/component/style IDs, content-audit findings, defect
  root causes and fixes, QA results, recto/verso rules, and deviations for Product
  Owner review: see [`HANDOFF-v1-build-log.md`](HANDOFF-v1-build-log.md).
