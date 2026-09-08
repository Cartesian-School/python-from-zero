# Figma Book Design System v1 — Build Log & Handoff

Status: **IN PROGRESS — BLOCKED on Figma API rate limit**

This log records the actual state of the Figma file created for the Cartesian School
Book Design System v1, per `BOOK-DESIGN-SYSTEM-v1.md`, `figma-variables.yaml`, and
`component-inventory.yaml`. It exists so work can resume without re-deriving IDs.

## File

- **Figma file URL:** <https://www.figma.com/design/m19Q51E0vmVek8r4TCJCd8>
- **File key:** `m19Q51E0vmVek8r4TCJCd8`
- **File name:** "Cartesian School — Book Design System v1"
- **Plan used:** "Solo" (team key `team::1126324353100957433`, Full seat)
  - Note: the "Cartesian School" Figma team (`team::1677084431316389117`) only has a
    **View** seat for this account and cannot create/edit files. The file was created
    under the personal "Solo" plan instead. If the design system should live in the
    Cartesian School team, it needs to be moved there by someone with Edit access on
    that team, or the account's seat on that team needs to be upgraded to Full/Dev.
- **Figma plan tier:** Starter — 3-page limit, ~20 MCP tool calls/month. Both limits
  were hit during this session (see Blocker below).

## Pages (2 of 3 Starter-plan page slots used)

| Page | Node ID | Purpose |
| --- | --- | --- |
| `01 — Foundations (Cover, Tokens, Typography)` | `0:1` | Cover, token documentation, Typography reference frame |
| `02 — Page Archetypes (6 reference frames)` | `2:4` | Standard Page, Chapter Opener, Code-Heavy, Table, Diagram/Callout |

One page slot is still free on the Starter plan if a third is needed later.

## Variables created (6 collections, 87 variables) — DONE

All variables follow `figma-variables.yaml`: physical mm/pt values are the canonical
documentation tokens (scope `[]`, not bound to any Figma property); a parallel set of
px-equivalent variables (1 mm = 4 px, 1 pt = 1.41111 px) is bound to actual Figma
properties (`FONT_SIZE`, `LINE_HEIGHT`, `WIDTH_HEIGHT`, `GAP`) so the canvas renders at
true physical proportion. Color primitives are unscoped (hidden) raw values; semantic
color variables alias them with explicit fill/stroke/text scopes — nothing uses
`ALL_SCOPES`.

| Collection | Variable Collection ID | Mode | Vars | Contents |
| --- | --- | --- | --- | --- |
| Page Geometry | `VariableCollectionId:3:2` | `3:0` "Value" | 15 | trim 165×235mm, mirrored margins (inner 20mm/outer 15mm/top 18mm/bottom 20mm), text measure 130mm, px equivalents, `meta/figma_scale_px_per_mm = 4` |
| Spacing | `VariableCollectionId:3:18` | `3:1` "Value" | 13 | `baseline_pt=12`; xs/sm/md/lg/xl/xxl in mm (1.5/2/3/4/6/9) + px |
| Typography — Canonical (pt) | `VariableCollectionId:3:32` | `3:2` "Value" | 19 | one `type/<role>` FLOAT per approved pt value (body 10, chapter_title 24, code 9, table_body 8.5, etc.) — documentation source of truth |
| Typography — Figma (px) | `VariableCollectionId:3:52` | `3:3` "Value" | 18 | `size/<role>` bound to `FONT_SIZE`, `lineheight/body` + `lineheight/code` bound to `LINE_HEIGHT` |
| Color Primitives | `VariableCollectionId:3:102` | `3:6` "Value" | 23 | indigo/violet/gray/amber/green/sky/red raw hex values, scope `[]` |
| Color Semantic | `VariableCollectionId:3:127` | `3:7` "Print" | 18 | `color/paper`, `color/text-primary`, `color/brand-indigo`, `color/warning(-surface)`, `color/code-surface`, `color/table-header-surface`, etc. — all alias primitives |

Full name → variable-ID maps are in `/tmp` build state from this session (not committed;
regenerate via `figma.variables.getLocalVariablesAsync()` if the file is reopened for
continuation — see Resume Protocol below).

### Font selection (approved — none copied from the Lafore reference)

| Role class | Family | Rationale |
| --- | --- | --- |
| Body reading text | **Source Serif 4** (Regular/Italic) | Contemporary open-source serif, full RU/PL/EN + Cyrillic coverage, distinct from reference's PetersburgC |
| Headings / UI / captions / tables / running head / page number | **Inter** (Regular/Medium/SemiBold/Bold/ExtraBold/Italic) | Contemporary geometric sans, distinct from reference's PragmaticaC |
| Code | **JetBrains Mono** (Regular) | Purpose-built code face, distinct from reference's LetterGothic |

All three are broadly available, open-license, and confirmed present in this Figma
account's font list (`listAvailableFontsAsync`) before use.

## Text styles — NOT YET CREATED (blocked)

A `use_figma` call to create all 17 `Book/Typography/*` text styles (Body, BodyItalic,
Section, MajorSection, ChapterLabel, ChapterTitle, TOCTitle, RunningHead, PageNumber,
Code, ListingCaption, TableCaption, TableHeader, TableBody, TableNote, FigureCaption,
DiagramText) was submitted and **hit the Figma MCP rate limit mid-call**. Figma's
transactional rollback means nothing from that call was persisted — the file has
**zero text styles** right now, only the variable collections above.

## The 6 canonical reference frames — NOT YET CREATED (blocked)

None of the required frames (Typography, Standard Page, Chapter Opener, Code-Heavy
Page, Table Page, Diagram/Callout Page) have been created yet. Page `2:4` exists but
is empty.

## Retry attempted 2026-09-08 (same session, reduced scope)

Per Product Owner decision, scope was narrowed to just: finish text styles + the
Typography reference frame, defer the other 5 frames. The text-style creation call
was retried immediately and was **rejected again** with the same
"You've reached the Figma MCP tool call limit on the Starter plan" error, confirming
this is a hard **monthly** quota exhaustion, not a per-call fluke — reducing scope
does not unblock it, since even one more write call is refused. **Text styles and the
Typography frame remain uncreated.** No further Figma MCP calls were attempted this
session. Per the user, the Figma plan is expected to be upgraded in ~3 days; resume
from here once that lands.

## Blocker: Figma MCP rate limit on Starter plan

Per Figma's own `rate-limits-access.md`: a **Starter** plan is capped at **~20 MCP
tool calls per month**, regardless of seat type. This session's tool calls (file
inspection, `get_libraries`, `get_metadata`, and the `use_figma` calls used to create
the 2 pages and 6 variable collections) exhausted that quota, and the next call
(text style creation) was rejected outright:

> "You've reached the Figma MCP tool call limit on the Starter plan."

Remaining scope — 17 text styles, 6 fully composed reference frames (each requiring
multiple `use_figma` calls per the incremental-build discipline the Figma skill
mandates), a QA/screenshot pass, and foundations documentation pages — needs on the
order of 40–60+ further tool calls. That is not achievable on the current plan without
either:

1. **Upgrading the Figma plan** (Professional: 200 calls/day, 15/min) for the "Solo"
   team, or upgrading the seat/plan under which this file lives — a billing decision,
   not something to do without explicit approval; or
2. **Waiting for the monthly quota to reset** and continuing across multiple sessions,
   spending the ~20 calls/month budget carefully; or
3. **Reducing v1 scope** (e.g. ship only the Typography frame + tokens as v1, defer
   the other 5 archetypes to a follow-up pass).

No further Figma MCP calls will be made until a Product Owner decision on the above.

## Resume protocol (reduced v1 scope, per Product Owner decision)

Agreed reduced scope for the remainder of v1: text styles + the Typography reference
frame only. The other 5 reference frames (Standard Page, Chapter Opener, Code-Heavy,
Table, Diagram/Callout) are explicitly deferred to a follow-up pass after this v1 is
reviewed — do not build them until asked.

1. Re-open <https://www.figma.com/design/m19Q51E0vmVek8r4TCJCd8>.
2. Confirm quota has reset or the plan has been upgraded (retry a single cheap
   read-only call, e.g. `get_metadata` with no `nodeId`, before attempting writes).
3. Run one read-only `use_figma` call to reconstruct the `{name → id}` map for all 6
   variable collections (`figma.variables.getLocalVariableCollectionsAsync()` +
   `getVariableByIdAsync` per member) — cheaper than re-deriving from this doc's table
   if IDs are needed precisely.
4. Create the 17 `Book/Typography/*` text styles using the exact font/size/role table
   in this doc (the script was written and rejected twice by the rate limit, never by
   a logic error — reuse it as-is).
5. Build the Typography reference frame on page `02 — Page Archetypes` (`2:4`): one
   sample block per style showing size, line-height, weight, and semantic role label,
   per `BOOK-DESIGN-SYSTEM-v1.md` frame 1 spec.
6. Run a `get_screenshot` QA pass on the Typography frame; check against the approved
   metrics table before calling v1 done.
7. Update this file's status tables and `design/book/figma/README.md` as each stage
   completes. Only after that — and only if asked — resume the other 5 frames.

## Deviations from the approved spec (for Product Owner awareness)

- **Page count**: Starter plan hard-caps Figma files at 3 pages. The 18 archetypes and
  6 reference frames could not each get a dedicated page as component-inventory.yaml's
  `Book/Page/*` naming implies one-per-archetype; the plan consolidates them onto 2
  pages using Sections instead. This does not change component names or token
  structure, only Figma page organization.
- **File location**: created under the personal "Solo" plan, not the "Cartesian
  School" team, because the account's seat on that team is View-only (see File
  section above).
- Everything else — trim size, margins, text measure, type scale, font-family class
  assignments, color role list, semantic icon set — matches the approved spec exactly;
  no metric deviations were introduced.
