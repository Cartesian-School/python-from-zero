# Cover Art SVG Asset Pack

Reusable SVG decomposition of the approved Cartesian School book-cover background concept
(the "computational core / data fabric" art direction developed for *Python с нуля*).

This pack is **design source material only**. It does not participate in, alter, or duplicate
the canonical publishing pipeline — see [Pipeline isolation](#pipeline-isolation).

---

## What this is

The approved cover background was authored parametrically. Rather than slicing a bitmap, the
artwork was decomposed **semantically**: every meaningful visual element — each wave, each glow,
each particle field, the core energy shell — was re-emitted from the original geometry as its own
standalone SVG on a shared coordinate system.

The result is a library you can reassemble, restage, or partially reuse in Figma without
re-deriving the art direction.

60 assets across 9 categories.

## Artistic intent

The concept is a **premium technical publication**, not a generic gradient background:

- deep indigo / violet base with genuine atmospheric depth
- elegant luminous flowing wave-lines as the primary gesture
- soft volumetric glow rather than flat vector fills
- a subtle star / particle field
- a central computational energy zone framing the Python focal point
- restrained data-science and engineering accents
- visually rich, never noisy

Three rules govern every asset:

1. **No UI-card look.** No panels, windows, frames or dashboard furniture anywhere in the pack.
   GRAPH / CODE / DATA ideas appear as mathematics, glyph drift and topology — never as boxes.
2. **Nothing crosses protected typography.** Every curve and particle field is verified against the
   title, subtitle, author, lockup and footer safe areas at generation time.
3. **Density hierarchy.** Quiet upper field → energy at the core → dispersal → quiet footer.

## Canvas and coordinate system

The shared canvas is **660 × 940** units, matching the canonical cover frame in points
(165 × 235 mm trim). Assets use one of two coordinate systems, declared per asset in the manifest
as `coordinate_system`:

| Value | Meaning | How to place |
| --- | --- | --- |
| `cover_canvas_660x940` | Canvas-aligned. `viewBox="0 0 660 940"`, geometry already in its final position. | Import into a 660 × 940 frame at (0, 0). It lands correctly with no manual positioning. |
| `component_local` | Tight `viewBox` around the component itself. Reusable anywhere. | Position manually. `placement.width` / `placement.height` give the natural size. |

Canvas-aligned covers the atmospheric system (background, waves, glows, particles, central energy,
footer). Component-local covers the reusable motifs (technical accents, graph/statistical motifs)
that are meant to be restaged freely.

## Category structure

| Category | Count | Layer role |
| --- | --- | --- |
| `background_base/` | 9 | **Background** — ground plate, colour fields, nebula volumetrics, vignette, reading mask |
| `wave_lines/` | 6 | **Midground** — the luminous flowing waves, one file per wave |
| `atmospheric_glows/` | 5 | **Background/midground** — diffuse bloom masses including the core bloom |
| `particle_fields/` | 7 | **Midground → foreground** — star, dust, halo, dispersal and foreground specks |
| `technical_accents/` | 5 | **Midground detail** — circuit echo, chip outline, connector, tick row |
| `central_energy/` | 9 | **Focal support** — rings, arcs, machined tick shell, nodes, streaks, hero halo |
| `data_science_motifs/` | 8 | **Midground detail** — topology clusters, plot curve, distribution, code streams |
| `footer_atmosphere/` | 4 | **Lower page** — grounding gradient plus optional sweeps and specks |
| `guides/` | 7 | **Utility** — safe-area and grid guides. Never composite into production. |

## Naming conventions

```
<role>_<position|variant>_<NN>.svg
```

Examples: `wave_upper_01.svg`, `glow_core_01.svg`, `particles_field_mid_01.svg`,
`energy_ring_02.svg`, `tech_trace_left_01.svg`, `guide_title_safe_area.svg`.

Inside each file:

- one top-level `<g>` whose `id` equals the `asset_id`
- child ids namespaced `assetid__part` (e.g. `wave_mid_01__glow`, `wave_mid_01__core`)
- gradients and filters carry descriptive, collision-resistant ids

Waves follow the project's existing **`__glow` + `__core`** convention (a blurred pass beneath a
crisp stroke), matching the `Atmosphere/WaveGlow` / `WaveCore` naming already used on the End Page.

## Reassembling in Figma

1. Create a frame **660 × 940**.
2. Import the canvas-aligned assets and place each at (0, 0). Stack them by the manifest's
   `z_order` (ascending = furthest back).
3. Set blend modes: assets whose markup carries `mix-blend-mode:screen` are additive light.
   Figma honours this on import, but verify — a screen layer that lands on Normal will look flat
   and milky.
4. Place the **real Python logo** (approved Figma master, component `Book/Illustration/PythonCore`,
   node `103:52`) at 252 pt wide, centred on **(310, 527)**. Use `rescale()`, not `resize()` —
   resizing an instance moves its bounding box without scaling its vector contents.
5. Sandwich the logo correctly — this ordering is what stops it looking pasted on:

   ```
   energy_core_halo_01   →   [ PYTHON LOGO ]   →   particles_foreground_sharp_01
                                                    particles_bokeh_foreground_01
   ```

6. Apply `background_quiet_mask_01` above all illustration layers and below all typography.
7. Add the approved typography and the Cartesian School lockup last.

`previews/assembly_preview.svg` is the whole canvas-aligned stack already composited in z-order —
use it as the reference for what step 2 should look like.

### Layer roles at a glance

- **Background:** `background_base/*`, `atmospheric_glows/glow_upper_left_01`,
  `glow_lower_right_01`, `glow_cyan_mid_01`, `glow_footer_01`, `wave_echo_far_01`
- **Midground:** `wave_lines/*`, `data_science_motifs/*`, `technical_accents/*`,
  `particle_fields/particles_field_*`
- **Focal support:** `central_energy/*`, `atmospheric_glows/glow_core_01`,
  `particle_fields/particles_halo_core_01`
- **Foreground:** `particles_foreground_sharp_01`, `particles_bokeh_foreground_01`
- **Utility:** `guides/*` — layout aids, never shipped

## Manifests

- `manifest_cover_art.json` — full record per asset: id, filename, category, name, description,
  usage, preferred zone, z-order, avoid zones, dependencies, coordinate system, placement, status,
  notes.
- `manifest_cover_art.csv` — same data, flattened for spreadsheets. List fields are `|`-separated.

`avoid_zones` names the protected typographic areas an asset must never be moved into. If you
restage an asset, re-check it against `guides/`.

## Known import caveats

Two assets are not purely declarative geometry. Both are isolated and documented rather than
silently embedded:

1. **`background_base/background_nebula_texture_01.svg`** uses an SVG `feTurbulence` filter to
   generate the volumetric cloud layer. Figma **discards the unsupported filter on import** — the
   asset arrives as a vector with an empty fill and no visible content (observed on import, not
   rasterised into a bitmap layer). It therefore contributes nothing in Figma and is excluded from
   the Figma cover assembly; it remains usable where SVG filters render, such as browser rendering
   and print output. No raster file is embedded in the pack, and no raster replacement was added.
2. **`data_science_motifs/code_stream_01.svg` / `code_stream_02.svg`** use live `<text>` elements
   with a monospace stack. Figma substitutes an available font on import, so exact glyph metrics
   will shift slightly. This is cosmetic — the glyphs are atmospheric texture, not readable copy.
   **Convert to outlines before any print export.**

Everything else is plain vector geometry, gradients and blend modes.

## Print notes

Geometry is sized for offset print at 165 mm width: structural strokes stay at or above roughly
0.7 pt, and no particle is smaller than about 0.45 pt radius, so nothing vanishes on press. The
`background_quiet_mask_01` and `footer_grounding_gradient_01` layers exist specifically to hold
tonal separation under typography — do not remove them to "brighten" the artwork.

## Previews

`previews/` holds verification aids only:

- `assembly_preview.svg` / `.png` — the canvas-aligned stack composited in z-order
- `contact_sheet.png` — every asset as a labelled thumbnail
- `_contact_sheet.html` — source for the contact sheet

These are **not** production artefacts and are not referenced by any build.

## Pipeline isolation

This pack deliberately sits outside the publishing system:

- it lives at `assets/cover_art/`, which no build script reads
- the EPUB adapter only walks `site/assets/{img,brand,icons}` — this path is not in that set
- no build, export or page-generation code was modified to create it
- the canonical Cover (`43:3`) and End Page (`48:55`) Figma nodes are untouched
- it introduces no second publishing path

Adopting any of these assets into a production page is a separate, explicit decision.
