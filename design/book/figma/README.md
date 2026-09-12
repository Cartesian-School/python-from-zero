# Figma Handoff

Store Figma design-file links, page/node IDs, component mappings, review notes, and approved handoff metadata here.

Figma remains a design and review surface only. The canonical book pipeline remains the sole publishing implementation.

## v1 build — Cover cleanup complete, ready for Product Owner review

- **Figma file:** <https://www.figma.com/design/m19Q51E0vmVek8r4TCJCd8/Cartesian-School-%E2%80%94-Book-Design-System-v1>
- **File key:** `m19Q51E0vmVek8r4TCJCd8`
- **Status:** Fifteen rounds of live Product Owner review/direction so far. Rounds
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
  Cover's full-page circuit background. Round 14 added flowing curved light
  trails (`Layer/LuminousFlow`) and curved hero-beam connectors. Round 15: two of
  round 14's flow trajectories turned out to be near-vertical curves spanning the
  page's full height — reading as dirty scratches and cutting straight through
  the hero panels, title, author credit, and footer — and two leftover full-height
  verticals from round 13's `BusLines` layer compounded the problem. Removed all
  of them plus one flow curve whose arc dipped into the hero's interior and one
  vertical accent crossing the author credit, verified with a numeric bounding-box
  sweep that zero background elements now intrude on the hero, and left the two
  remaining horizontal flow sweeps and all margin-confined detail in place — the
  Cover is now clean and controlled without being emptied out. The End Page was
  out of scope this round and was not touched. No screenshot/raster shortcuts were
  used for any illustration; every photograph, logo asset, and code (QR/barcode)
  is either a real sourced file from the repo or a genuinely functional/credible
  generated asset, never an invented or decorative substitute.
- A few archetypes were evaluated and marked N/A/deferred because the underlying
  content doesn't exist yet (Conclusion, Glossary, References) — see the build log.
- Full build log, node/variable/component/style IDs, content-audit findings, defect
  root causes and fixes, QA results, recto/verso rules, and deviations for Product
  Owner review: see [`HANDOFF-v1-build-log.md`](HANDOFF-v1-build-log.md).
