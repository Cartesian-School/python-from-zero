# Figma Handoff

Store Figma design-file links, page/node IDs, component mappings, review notes, and approved handoff metadata here.

Figma remains a design and review surface only. The canonical book pipeline remains the sole publishing implementation.

## v1 build — luminous flow art-direction pass finished, ready for Product Owner review

- **Figma file:** <https://www.figma.com/design/m19Q51E0vmVek8r4TCJCd8/Cartesian-School-%E2%80%94-Book-Design-System-v1>
- **File key:** `m19Q51E0vmVek8r4TCJCd8`
- **Status:** Fourteen rounds of live Product Owner review/direction so far. Rounds
  1-5 covered callout surface/sizing fixes, the complete front/back matter system,
  and a systemic pt→px text-sizing bug (see below). Round 6 extracted the Cartesian
  School website's hero visual language into an 8-component vector-native
  `Book/Illustration/*` library. Round 7 added a real vector Python logo and a
  `ProjectCard` set for all 13 real projects. Round 8 replaced a hand-drawn
  Cartesian School mark approximation with the actual repo assets from
  `cartesian_logo/`. Round 9 corrected the About Cartesian School page's brand
  treatment and rebuilt the QA-only Book Sequence Overview diagram. Round 10 added
  a publication-identifier utility panel and a real, `pyzbar`-verified QR code.
  Round 11 rebuilt the End Page from scratch and corrected the author's Russian
  name (`Siergej Sobolewski` → `Сергей Соболевский`) file-wide. Round 12-13 built
  and then substantially expanded `Book/Illustration/MotherboardSystem`, the
  Cover's full-page circuit background. Round 14: added the one register still
  missing from the brief — genuinely *flowing* curved light trails, not just
  orthogonal traces. Converted the hero's four straight beams into curved
  glow-duplicate connectors; added a new `Layer/LuminousFlow` to the Cover (six
  large sweeping bezier trajectories crossing the full page, including behind the
  title/hero/footer at calibrated low opacity); applied the same glow technique to
  the End Page's wave arcs; and added a small, margin-confined data-science
  atmosphere near the portrait (a signal-plot sparkline, a node-link cluster, a
  quiet dot-grid hint). The ISSN/barcode module gained corner ticks and a
  "PUBLICATION DATA" label so it reads as an engineered plate rather than a
  sticker. No screenshot/raster shortcuts were used for any illustration; every
  photograph, logo asset, and code (QR/barcode) is either a real sourced file from
  the repo or a genuinely functional/credible generated asset, never an invented
  or decorative substitute.
- A few archetypes were evaluated and marked N/A/deferred because the underlying
  content doesn't exist yet (Conclusion, Glossary, References) — see the build log.
- Full build log, node/variable/component/style IDs, content-audit findings, defect
  root causes and fixes, QA results, recto/verso rules, and deviations for Product
  Owner review: see [`HANDOFF-v1-build-log.md`](HANDOFF-v1-build-log.md).
