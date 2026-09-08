# Book Design System Workspace

This directory is the canonical design workspace for the **Python from Zero** book editions.

## Purpose

Use this area to store design-system specifications, Figma references, print-layout tokens, visual archetypes, and review evidence for the book.

This directory is **not** a second publishing pipeline.

The binding publication architecture remains:

`language -> locale/configuration -> one canonical book model -> publication adapter`

Formatting and publishing logic must remain language-independent. The selected language is only an input parameter. The selected publication format is only an output parameter.

## Structure

- `figma/` — Figma file references, node references, design-review notes, and handoff metadata.
- `tokens/` — canonical typography, spacing, color, diagram, table, code, callout, and page-geometry tokens approved from design review.
- `archetypes/` — specifications for canonical page archetypes such as chapter opener, theory page, code-heavy page, diagram page, project opener, TOC, and index.
- `references/` — screenshots and notes used only as visual references during redesign; do not treat these as publication source assets unless separately registered.
- `evidence/` — before/after review records and approval notes for design-system changes.

## Figma role

Figma is the **design source and review surface** for the book layout system. It is not the final renderer for the full book.

Approved Figma decisions must be translated into canonical, language-independent design tokens and implemented through the existing canonical publication pipeline.

## Publication safety rules

1. Do not introduce RU/PL/EN-specific print CSS or separate builders.
2. Do not copy manual Figma page layouts into per-language publishing code.
3. Keep all book-design tokens language-neutral.
4. Format-specific differences may exist only where output formats genuinely require them, e.g. PDF print geometry versus EPUB reflow.
5. Every approved design change should have an evidence record before global rollout.
