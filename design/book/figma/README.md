# Figma Handoff

Store Figma design-file links, page/node IDs, component mappings, review notes, and approved handoff metadata here.

Figma remains a design and review surface only. The canonical book pipeline remains the sole publishing implementation.

## v1 build — Cover art-direction reconstruction complete, ready for Product Owner review

- **Figma file:** <https://www.figma.com/design/m19Q51E0vmVek8r4TCJCd8/Cartesian-School-%E2%80%94-Book-Design-System-v1>
- **File key:** `m19Q51E0vmVek8r4TCJCd8`
- **Status:** Sixteen rounds of live Product Owner review/direction so far. Rounds
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
  name (`Siergej Sobolewski` → `Сергей Соболевский`) file-wide. Round 12-14 built
  and expanded `Book/Illustration/MotherboardSystem`, the Cover's full-page
  circuit background, adding flowing curved light trails and curved hero-beam
  connectors. Round 15 was a subtractive cleanup, removing dirty full-height
  vertical lines. Round 16: the Product Owner rejected round 15 as "technically
  correct but artistically insufficient" and required real reconstruction, not
  further cleanup. Found and fixed the actual root cause of the hero's "rectangle
  pasted in the middle" feeling — `HeroNetwork`'s own isolated grid/glow backdrop,
  hard-clipped to its rounded-rect bounds regardless of how the surrounding Cover
  background changed — by deleting it entirely and replacing it with a new
  `Layer/CoreField`: a 4-stop concentric glow with no boundary by construction,
  plus a 196-fragment grid that radially dissolves rather than cutting off at an
  edge. Added 4 cardinal "reach-in" traces connecting the field directly into the
  hero's core ring through the real gaps between panels (8 connection points, was
  4), 3 more varied data-flow trajectories with traveling-pulse markers, and an
  individual glow behind each of the 4 technical panels. This round was net
  additive — the only deletions were the actual root-cause backdrop and two
  pulse markers found sitting too close to the subtitle's text line during QA.
  The End Page was out of scope and was not touched. No screenshot/raster
  shortcuts were used for any illustration; every photograph, logo asset, and
  code (QR/barcode) is either a real sourced file from the repo or a genuinely
  functional/credible generated asset, never an invented or decorative
  substitute.
- A few archetypes were evaluated and marked N/A/deferred because the underlying
  content doesn't exist yet (Conclusion, Glossary, References) — see the build log.
- Full build log, node/variable/component/style IDs, content-audit findings, defect
  root causes and fixes, QA results, recto/verso rules, and deviations for Product
  Owner review: see [`HANDOFF-v1-build-log.md`](HANDOFF-v1-build-log.md).
