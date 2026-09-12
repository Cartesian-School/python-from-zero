# Cartesian School — Reference Hero Asset Pack v2

This package contains the **actual image-based hero elements** extracted from the supplied approved computational reference.

## Important
The supplied reference elements are raster artwork. They cannot be faithfully recovered as native vector SVG geometry simply by renaming/converting the files. Therefore the package contains:

- `source/` — untouched uploaded source crops;
- `raster/` — cleaned PNG assets with connected white screenshot margins removed to transparency where applicable;
- `svg_wrappers/` — self-contained SVG files that embed the cleaned PNG so they can be placed/imported as single Figma assets; these are **raster-backed SVG wrappers, not vector redraws**;
- `reference_full` — the complete approved composition for visual matching.

## Hero elements
1. `circuit_traces_upper_left` — upper-left circuit framing.
2. `compute_chip_single` — luminous compute-chip module.
3. `data_cube_3d` — 3D data/embedding cube.
4. `compute_substrate_dual_chip` — dual-chip lower engineering field.
5. `data_wave_left` — sampled luminous data-wave surface.
6. `analytics_bars` — analytical bars/data trajectory.
7. `reference_full` — complete art-direction reference.

## Figma
For maximum fidelity, place the cleaned PNG files from `raster/`. The `svg_wrappers/` files are provided when the workflow expects `.svg`, but Figma will still treat their embedded artwork as raster image content. A true editable SVG version requires a deliberate vector redraw of these elements.
