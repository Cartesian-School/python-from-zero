# Cartesian School — Python from Zero Book Design System v1

Status: APPROVED DESIGN BASIS

This document defines the Figma-facing book design system for the canonical book pipeline. Figma is a design/review source, not a publishing engine. All adopted values must be representable as language-independent design tokens and implemented by the single canonical book-build pipeline.

## 1. Physical page geometry

Canonical trim: **165 × 235 mm**.

Reference proportion derived from the approved technical-book reference. Figma working scale: **1 mm = 4 px**, therefore the canonical page frame is **660 × 940 px**. The millimetre values remain authoritative; Figma pixels are only a design convenience.

Mirrored print margins:
- inner: 20 mm = 80 px
- outer: 15 mm = 60 px
- top: 18 mm = 72 px (initial design target)
- bottom: 20 mm = 80 px (initial design target)

Nominal text measure: ~130 mm = 520 px.

## 2. Baseline rhythm

- body: 10 pt
- body leading: 12 pt
- ratio: 1.20
- baseline grid: 12 pt
- paragraph spacing: compact; no web-style large vertical gaps
- headings and supporting components should align to a 12-pt rhythm where practical

## 3. Typography scale

The metric hierarchy is adopted from the measured technical-book reference; fonts and visual identity are NOT copied.

| Role | Size | Notes |
| --- | ---: | --- |
| Chapter title | 24 pt | bold display sans, compact leading |
| Chapter label | 20 pt | bold sans |
| Major section | 16 pt | bold sans |
| Section | 14 pt | bold sans |
| Body prose | 10 pt | reading face, 12 pt leading |
| TOC entry | 9 pt | compact navigation |
| Running head | 9 pt | quiet utility text |
| Page number | 10.5 pt | visible, unobtrusive |
| Code | 9 pt | monospace, selectable text |
| Listing caption | 9 pt | compact technical caption |
| Table caption | 9 pt | compact technical caption |
| Table header | 8.5 pt | semibold |
| Table body | 8.5 pt | dense but readable |
| Table note | 8 pt | auxiliary |
| Figure caption | 8.5 pt | compact |
| Diagram internal text | >=9 pt effective | hard minimum after scaling |

## 4. Font policy

Use contemporary, broadly available, highly legible fonts with full RU/PL/EN coverage.

Figma candidates:
- body: Noto Serif / Source Serif 4 / IBM Plex Serif
- headings/UI: Inter / IBM Plex Sans / Source Sans 3
- code: JetBrains Mono / IBM Plex Mono / Source Code Pro

The final choice requires visual comparison at physical size before adoption. No font from the reference book is to be copied.

## 5. Page archetypes

Create the following canonical Figma archetypes:

1. Front cover reference frame
2. Half-title / title page
3. Copyright / license page
4. About the author
5. Preface / introduction
6. Contents page
7. Chapter opener
8. Standard prose page
9. Prose + code page
10. Code-heavy page
11. Figure + caption page
12. Diagram page
13. Table page
14. Callout-rich page
15. Practice / exercise page
16. Project opener
17. Chapter summary
18. Index / reference page

Each archetype must use the same variables and components; no locale-specific archetype forks.

## 6. Core components

### 6.1 Running header
- 9 pt
- quiet neutral tone
- mirrored alignment by recto/verso
- thin separator optional

### 6.2 Page number
- 10.5 pt
- consistent baseline
- never competes with body text

### 6.3 Chapter opener
- chapter label: 20 pt
- chapter title: 24 pt
- compact synopsis
- substantive chapter text may begin on the same page where appropriate
- full-page whitespace is not the default

### 6.4 Section headings
- major section: 16 pt
- section: 14 pt
- compact before/after spacing
- keep-with-next where possible without creating pathological white space

### 6.5 Code block
- 9 pt monospace
- 10.5–11 pt line height
- compact print padding
- no decorative oversized web-card spacing
- selectable text required
- long code may split only according to canonical long-block pagination policy

### 6.6 Listing caption
- 9 pt
- placed immediately above/below listing according to chosen canonical convention
- continuation state visually explicit

### 6.7 Table
- caption: 9 pt
- header: 8.5 pt semibold
- body: 8.5 pt
- note: 8 pt
- vertical cell padding: 1.5–2.0 mm
- horizontal cell padding: 2.0–2.5 mm
- semantic table, never rasterized screenshot
- repeated headers on continuation

### 6.8 Figure / diagram
- caption: 8.5 pt
- diagram text: >=9 pt effective print size
- no split across physical pages
- caption kept with figure
- color never the only semantic signal
- flowcharts use professional orthogonal connectors

## 7. Semantic callout system

The visual identity is modern Cartesian School: restrained indigo/violet foundation, high legibility, semantic accent surfaces, and compact geometry.

Starter semantic roles:
- warning / common gotcha — ⚠️
- Python-specific insight — 🐍
- context / aside — ℹ️
- self-check / verification — ✅
- common mistake / anti-pattern — ❌
- milestone / completion — 🎉

Rules:
- max one emoji/icon per heading
- emoji allowed only on unnumbered semantic headings
- never before numbered chapter/section titles
- same semantic role = same icon in every chapter and language
- only codepoints present in the embedded font subset unless the subset is explicitly extended

## 8. Color system direction

Final colors will be Cartesian School identity, not the reference book.

Initial Figma variable groups should include:
- surface / paper
- text / primary
- text / secondary
- rule / subtle
- brand / indigo
- brand / violet
- semantic / warning
- semantic / success
- semantic / info
- semantic / danger
- code / surface
- table / header-surface

Colors must remain usable in grayscale and accessible contrast.

## 9. Figma component naming

Use predictable names:

- `Book/Page/Standard`
- `Book/Page/ChapterOpener`
- `Book/Page/CodeHeavy`
- `Book/Page/Figure`
- `Book/Page/Table`
- `Book/Page/CalloutRich`
- `Book/Typography/ChapterTitle`
- `Book/Typography/ChapterLabel`
- `Book/Typography/H2`
- `Book/Typography/H3`
- `Book/Typography/Body`
- `Book/Typography/Code`
- `Book/Component/RunningHead`
- `Book/Component/PageNumber`
- `Book/Component/CodeBlock`
- `Book/Component/Table`
- `Book/Component/Figure`
- `Book/Component/Callout/*`

## 10. Approval boundary

This v1 defines the design-system skeleton and measured geometry. It does NOT yet authorize publishing-pipeline changes. Before implementation, representative Figma archetypes must be visually approved at true physical scale.

Binding architecture remains:
- exactly one canonical book-build pipeline
- language = input/configuration only
- publication format = output behavior only
- no language-specific layout forks

## 11. Front & back matter (implemented)

The 6 internal body-page archetypes above are complemented by a full front-matter
(Cover, Title, Copyright, About Author, From Author, TOC + continuation) and
back-matter (Index, About Cartesian School, Colophon, End Page) system, built after a
repository content audit so no editorial content was invented — real book title,
author identity, license terms, Introduction text, and all 24 real chapter titles are
used throughout. Conclusion, Glossary, and References archetypes were evaluated and
marked N/A: no such distinct content exists in the book yet.

Full node IDs, the content-audit findings, recto/verso publication rules, and QA
evidence are in `design/book/figma/HANDOFF-v1-build-log.md` — this document is not
duplicated here to avoid drift between the two.
