# Figma Handoff

Store Figma design-file links, page/node IDs, component mappings, review notes, and approved handoff metadata here.

Figma remains a design and review surface only. The canonical book pipeline remains the sole publishing implementation.

## v1 build — canonical Cover promoted from approved Cover-E, ready for Product Owner review

- **Figma file:** <https://www.figma.com/design/m19Q51E0vmVek8r4TCJCd8/Cartesian-School-%E2%80%94-Book-Design-System-v1>
- **File key:** `m19Q51E0vmVek8r4TCJCd8`
- **Canonical Cover:** `Book/Page/Cover` `43:3` (node ID preserved across the promotion)
- **Cover artwork component:** `Book/Illustration/CoverDataFabric` `264:2641`
  (page `06 — Illustration Library`)
- **Status:** Twenty rounds of live Product Owner review/direction. Round 20 promoted
  the approved Cover-E art direction into the canonical production Cover. The legacy
  `MotherboardSystem`/`HeroNetwork` Cover instances were retired in favour of a single
  `Book/Illustration/CoverDataFabric` component instance; `43:3` kept its node ID and
  all of its existing shared editorial components (`BookTitle`, `AuthorCredit`, the
  real `CartesianLockup`, kicker, footer rule/domain/series, RECTO) untouched in place.
  The artwork component holds **no** editorial or locale text, so one artwork serves
  every language edition — the language remains an input parameter to the single
  canonical book pipeline, which this round did not modify. Equivalence against the
  approved concept `252:236` was verified by pixel diff: 22 of 620,400 pixels differ
  (0.004%, max channel delta 5 — anti-aliasing only). Rounds 18–19 preceded it: the
  art-direction reset that produced Cover-E, the decomposition of that artwork into the
  committed 60-asset SVG library at `assets/cover_art/svg/`, the rebuild of Cover-E from
  that library, and a bounded optical-polish pass (Python core 226→214 pt, softer
  dominant-wave glow, selective core thinning). Concept `252:236`, its pre-polish
  snapshot `259:1222` and the before/after QA `261:1989` are preserved as immutable
  design evidence.
- Seventeen earlier rounds preceded those.
  Round 17 was a full art-direction rebuild of the Cover hero: the Product Owner
  correctly rejected round 16's result as "Python surrounded by four dashboard
  widgets" in a rigid 2×2 grid — a compositional failure independent of how
  clean the underlying connector geometry was. The four `GraphPanel`/`CodePanel`/
  `GamePanel`/`AppPanel` instances had their rectangular card chrome (fill,
  stroke, divider) stripped, then were rescaled and repositioned asymmetrically
  as floating data fragments at varying distance/scale from a rebuilt, off-center
  Python computational core (new dashed/solid orbital rings, irregular orbit
  nodes, sparse coordinate ticks). Four organic tendrils of visibly different
  curvature/weight replace the old symmetric radial beams. The background's
  `Layer/DetailZones` — 105 literal DIP-chip-package nodes, a "literal
  motherboard diagram" — was deleted and replaced with 16 sparse schematic
  marks; `Layer/CoreField`'s concentric glow and dissolving grid were
  regenerated centered exactly on the new core position. Verified with numeric
  bounding-box sweeps (zero collisions after one fix), close-crop screenshots of
  every protected zone, and full-page renders at thumbnail/half/full size. The
  End Page was inspected and found already consistent with the new Cover's
  visual language; it was not modified. Full detail, node IDs, and the
  self-rejection checklist are in the HANDOFF log's "Full art-direction rebuild
  — Computational Core / Data Fabric (seventeenth round)" section.
- Sixteen earlier rounds of Product Owner review/direction preceded this one. Rounds
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
