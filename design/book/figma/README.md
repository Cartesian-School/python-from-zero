# Figma Handoff

Store Figma design-file links, page/node IDs, component mappings, review notes, and approved handoff metadata here.

Figma remains a design and review surface only. The canonical book pipeline remains the sole publishing implementation.

## v1 build — final art-direction pass complete, ready for Product Owner review

- **Figma file:** <https://www.figma.com/design/m19Q51E0vmVek8r4TCJCd8/Cartesian-School-%E2%80%94-Book-Design-System-v1>
- **File key:** `m19Q51E0vmVek8r4TCJCd8`
- **Status:** Ten rounds of live Product Owner review/direction so far. Rounds 1-5
  covered callout surface/sizing fixes, the complete front/back matter system, and a
  systemic pt→px text-sizing bug (see below). Round 6 extracted the Cartesian School
  website's hero visual language into an 8-component vector-native
  `Book/Illustration/*` library. Round 7 added a real vector Python logo and a
  `ProjectCard` set for all 13 real projects. Round 8 replaced a hand-drawn
  Cartesian School mark approximation with the actual repo assets from
  `cartesian_logo/`, and rebuilt the Cover's hero network and the End Page as a
  denser, atmospheric, tonally-matched pair. Round 9 corrected the About Cartesian
  School page's brand treatment, rebuilt the QA-only Book Sequence Overview diagram
  (which had a genuine connector-geometry bug) into one precisely-connected 3-phase
  flow, and rebuilt the End Page into a real editorial closing page with the actual
  author photograph, a real book summary, and a real author bio. Round 10: added a
  white publication-identifier utility panel (placeholder `ISSN 0000-0000` +
  a placeholder Code128 barcode) and a real, `pyzbar`-verified scannable QR code
  encoding `https://www.cartesianschool.org` to the End Page's lower zone — while
  fixing a pre-existing regression found in the process (the End Page's logo lockup
  had drifted away from its own heading/URL group). No screenshot/raster shortcuts
  were used for any illustration; every photograph, logo asset, and code (QR/
  barcode) is either a real sourced file from the repo or a genuinely
  functional/credible generated asset, never an invented or decorative substitute.
- A few archetypes were evaluated and marked N/A/deferred because the underlying
  content doesn't exist yet (Conclusion, Glossary, References) — see the build log.
- Full build log, node/variable/component/style IDs, content-audit findings, defect
  root causes and fixes, QA results, recto/verso rules, and deviations for Product
  Owner review: see [`HANDOFF-v1-build-log.md`](HANDOFF-v1-build-log.md).
