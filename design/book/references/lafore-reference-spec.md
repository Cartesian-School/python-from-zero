# REFERENCE-TYPOGRAPHY-001 — Lafore Metric Reference

Status: REFERENCE

Source: Robert Lafore, *Data Structures & Algorithms in Java*, Russian edition (Piter, 2013).

Purpose: provide a measured physical and typographic reference for the Cartesian School book design system. This document records geometry, scale, density, and spacing relationships only. It is **not** a visual-style template and does not authorize copying fonts, decoration, colors, or brand identity.

## 1. Physical page geometry

Measured reference trim: approximately **165 × 235 mm** for the main book block.

Reference aspect ratio: approximately **0.702**.

Observed mirrored-margin model:

- inner margin: approximately **20 mm**
- outer margin: approximately **15 mm**
- usable text width: approximately **130 mm**

The metric reference is intended for print composition, code, tables, diagrams, and heading density.

## 2. Verified typography hierarchy

Values below were verified directly from the supplied PDF in LibreOffice Draw by selecting the relevant text objects.

| Role | Reference family | Size | Weight/style | Notes |
| --- | --- | ---: | --- | --- |
| Body prose | PetersburgC | 10 pt | regular | primary reading text |
| TOC entry | PragmaticaC | 9 pt | regular/bold by level | compact navigation |
| Running/utility text | PragmaticaC | 8–9 pt | regular | headers and service text |
| Section heading | PragmaticaC | 14 pt | bold | local pedagogical section |
| Major section heading | PragmaticaC | 16 pt | bold | major subsection |
| Chapter label | PragmaticaC | 20 pt | bold | e.g. `Глава 1` |
| Chapter title | PragmaticaC | 24 pt | bold | e.g. `Общие сведения` |
| TOC title | PragmaticaC | 24 pt | bold | `Оглавление` |
| Code | LetterGothic | 9 pt | regular | source listings |
| Listing caption | PragmaticaC | 9 pt | italic/bold as needed | `Листинг 1.1` |
| Table caption | PragmaticaC | 9 pt | regular/bold as needed | `Таблица 1.1` |
| Table body | PragmaticaC | 8 pt | regular | dense technical data |
| Figure caption | PragmaticaC | 8 pt | regular/bold as needed | `Рис. 1.1` |
| Figure/internal simple label | serif/sans by artwork | 8 pt | regular | reference only; Cartesian minimum differs |

## 3. Reference metric scale

The reference uses a disciplined size ladder rather than web-style oversized hierarchy:

`8 → 9 → 10 → 14 → 16 → 20 → 24 pt`

Interpretation:

- 10 pt = reading text
- 9 pt = code and supporting technical labels
- 8 pt = dense auxiliary material such as tables/captions
- 14–16 pt = section hierarchy
- 20–24 pt = chapter hierarchy

## 4. Leading and vertical rhythm

Observed body composition is approximately **10/12 pt**, i.e. line-height about **1.20**.

Reference principles:

- paragraph spacing is very tight;
- large web-style vertical margins are absent;
- headings rely on compact controlled spacing rather than card-like whitespace;
- body pages maintain high information density without reducing the primary reading text below 10 pt.

The reference should therefore be treated as a baseline-grid and rhythm model, not merely a set of font sizes.

## 5. Code composition

Verified source-listing reference:

- font size: **9 pt**
- family class: monospace
- compact leading
- minimal surrounding whitespace
- captions at approximately **9 pt**

Cartesian School should preserve code as selectable text and should not emulate web-card padding around every listing.

## 6. Table composition

Verified table reference:

- table title/caption: **9 pt**
- table body: **8 pt**
- compact row height
- low cell padding
- efficient use of the full text measure

The metric lesson is density and legibility, not imitation of the original table styling.

## 7. Figure/caption composition

Verified figure captions are approximately **8 pt**.

Reference internal figure text may reach approximately **8 pt**, but this value is **not adopted as the Cartesian minimum for diagrams**. The Cartesian book has already documented SVG downscaling defects, therefore its own design system must enforce a larger effective minimum for diagram-internal text.

## 8. What may be adopted

Allowed reference dimensions:

- trim proportion
- text measure
- mirrored-margin logic
- typography scale
- code/table/caption size relationships
- baseline density
- compact vertical rhythm
- hierarchy ratios

## 9. What must NOT be copied

Do not copy:

- PetersburgC
- PragmaticaC
- LetterGothic as a brand choice
- original colors
- original decorative rules
- page ornament
- publisher identity
- historical visual styling

Cartesian School will use its own modern visual identity, contemporary typefaces, color system, semantic callouts, diagrams, and controlled emoji/icon language.

## 10. Architecture constraint

This reference is design input only.

It must never create a second publishing path.

The binding architecture remains:

- exactly one canonical book-build pipeline;
- language is an input/configuration parameter only;
- publication format is an output parameter only;
- approved design decisions become language-independent tokens/components consumed by the canonical pipeline.
