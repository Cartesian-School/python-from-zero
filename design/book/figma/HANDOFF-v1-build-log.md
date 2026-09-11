# Figma Book Design System v1 — Build Log & Handoff

Status: **v1 fixes complete — ready for Product Owner re-review**

A live Product Owner review of the previous "v1 COMPLETE" state found blocking visual
defects (white backgrounds inside colored callouts, and text overflow/wrap issues on
several frames). Both root causes are documented and fixed below — see "Visual defect
fixes (post-review round)" for the full detail the Product Owner asked for: exact
defects, root causes, fixes, affected node IDs, and QA evidence.

This log records the actual state of the Figma file created for the Cartesian School
Book Design System v1, per `BOOK-DESIGN-SYSTEM-v1.md`, `figma-variables.yaml`, and
`component-inventory.yaml`. It exists so work can be reviewed and, if needed, resumed
without re-deriving IDs.

## File

- **Figma file URL:** <https://www.figma.com/design/m19Q51E0vmVek8r4TCJCd8/Cartesian-School-%E2%80%94-Book-Design-System-v1>
- **File key:** `m19Q51E0vmVek8r4TCJCd8`
- **File name:** "Cartesian School — Book Design System v1"
- **Plan used:** "Solo" (team key `team::1126324353100957433`, Full seat), **tier: Pro**
  (upgraded from Starter mid-project — see "Rate-limit history" below).
  - Note: the "Cartesian School" Figma team (`team::1677084431316389117`) still only
    has a **View** seat for this account and cannot host an editable file. **Open
    question for the Product Owner**: transfer/duplicate this file into that team once
    edit access is available, or keep it under "Solo" and share a view link?

## Pages

| Page | Node ID | Contents |
| --- | --- | --- |
| `01 — Foundations (Cover, Tokens, Typography)` | `0:1` | Typography reference frame (`Book/Reference/Typography`, node `8:2`) |
| `02 — Page Archetypes (6 reference frames)` | `2:4` | Shared component shelf + the 5 page-archetype reference frames |

## Variables — 6 collections, 89 variables total — DONE

All variables follow `figma-variables.yaml`: physical mm/pt values are the canonical
documentation tokens (scope `[]`, not bound to any Figma property); a parallel set of
px-equivalent variables (1 mm = 4 px, 1 pt = 1.41111 px) is bound to actual Figma
properties (`FONT_SIZE`, `LINE_HEIGHT`, `WIDTH_HEIGHT`, `GAP`) so the canvas renders at
true physical proportion. Color primitives are unscoped (hidden) raw values; semantic
color variables alias them with explicit fill/stroke/text scopes — nothing uses
`ALL_SCOPES` anywhere in the file.

| Collection | Variable Collection ID | Mode | Vars | Contents |
| --- | --- | --- | --- | --- |
| Page Geometry | `VariableCollectionId:3:2` | `3:0` "Value" | 15 | trim 165×235mm, mirrored margins (inner 20mm/outer 15mm/top 18mm/bottom 20mm), text measure 130mm, px equivalents, `meta/figma_scale_px_per_mm = 4` |
| Spacing | `VariableCollectionId:3:18` | `3:1` "Value" | 13 | `baseline_pt=12`; xs/sm/md/lg/xl/xxl in mm (1.5/2/3/4/6/9) + px |
| Typography — Canonical (pt) | `VariableCollectionId:3:32` | `3:2` "Value" | 19 | one `type/<role>` FLOAT per approved pt value — documentation source of truth |
| Typography — Figma (px) | `VariableCollectionId:3:52` | `3:3` "Value" | 18 | `size/<role>` bound to `FONT_SIZE`, `lineheight/body` + `lineheight/code` bound to `LINE_HEIGHT` |
| Color Primitives | `VariableCollectionId:3:102` | `3:6` "Value" | 24 | indigo/violet/gray/amber/green/sky/red raw hex values, scope `[]` |
| Color Semantic | `VariableCollectionId:3:127` | `3:7` "Print" | **20** | 18 original roles + 2 added this session: `color/python-insight` (`VariableID:10:2`, aliases `indigo/600`) and `color/python-insight-surface` (`VariableID:10:3`, aliases `indigo/50`) — needed for the `Callout/PythonInsight` variant, not covered by warning/info/success/danger |

(Corrects a typo in the original checkpoint: Color Primitives has 24 variables, not 23 —
miscounted in the first handoff pass, verified by direct read this session.)

### Font selection (approved — none copied from the Lafore reference)

| Role class | Family | Rationale |
| --- | --- | --- |
| Body reading text | **Source Serif 4** (Regular/Italic) | Contemporary open-source serif, full RU/PL/EN + Cyrillic coverage, distinct from reference's PetersburgC |
| Headings / UI / captions / tables / running head / page number | **Inter** (Regular/Medium/SemiBold/Bold/ExtraBold/Italic) | Contemporary geometric sans, distinct from reference's PragmaticaC |
| Code | **JetBrains Mono** (Regular) | Purpose-built code face, distinct from reference's LetterGothic |

## Text styles — 18 created — DONE

All bound to the Typography — Figma (px) variables (or explicit percent line-height for
roles without an approved leading value). Retried twice against the rate limit before
the plan upgrade (see history below) — both attempts were rejected before any write
executed (Figma's plugin transactions roll back atomically), so nothing needed
cleanup; the third attempt, after the upgrade, succeeded outright.

| Style | Node ID | Font | Size (canonical pt → bound px) |
| --- | --- | --- | --- |
| Book/Typography/Body | `S:7587e740ec6a5e53268a900dbf3df3c0559a65d5,` | Source Serif 4 Regular | 10pt → 14.11px, leading 12pt → 16.93px |
| Book/Typography/BodyItalic | `S:dbf24c274026bce7d991c3c9fd668304c37c6bb6,` | Source Serif 4 Italic | 10pt → 14.11px |
| Book/Typography/Section | `S:fe045fe70193cb6d46007d9a3699d3bd698ba2cf,` | Inter Bold | 14pt → 19.76px |
| Book/Typography/MajorSection | `S:80e38d0d0683b130ace847c496723f129913e630,` | Inter Bold | 16pt → 22.58px |
| Book/Typography/ChapterLabel | `S:ad2f6babeb8d51cfb48e898ac72efa0a246b8b78,` | Inter Bold | 20pt → 28.22px |
| Book/Typography/ChapterTitle | `S:6efdd836b5ccbabe15482efacb5b24347db437bf,` | Inter Extra Bold | 24pt → 33.87px |
| Book/Typography/TOCTitle | `S:d3f4f392cce0cd9f1d8246f48f83721eaa35243e,` | Inter Extra Bold | 24pt → 33.87px |
| Book/Typography/TOCEntry | `S:3b486630c04384bf677bee2c6934754275977910,` | Inter Regular | 9pt → 12.70px (added — defined in `adopted-values.yaml`, not explicitly in the original 17-name list) |
| Book/Typography/RunningHead | `S:5ffaaa9acdbb0181a324d01059181c3e398b36a7,` | Inter Regular | 9pt → 12.70px |
| Book/Typography/PageNumber | `S:40cfcb1878c79d512eb4496f60eda094ecb0cf1c,` | Inter Medium | 10.5pt → 14.82px |
| Book/Typography/Code | `S:aab7ec060817db8554af84a002256c9250a364cc,` | JetBrains Mono Regular | 9pt → 12.70px, leading 10.75pt → 15.17px |
| Book/Typography/ListingCaption | `S:cd76d7ca9bb85a04bb7f5ce9f3a10eed349a9719,` | Inter Italic | 9pt → 12.70px |
| Book/Typography/TableCaption | `S:89cc5d00daa28030b909494ee856b07aac35bb60,` | Inter Medium | 9pt → 12.70px |
| Book/Typography/TableHeader | `S:417989d5ee58d65ad684783b17c2ce72450e3400,` | Inter Semi Bold | 8.5pt → 11.99px |
| Book/Typography/TableBody | `S:7120a8b15c1a622ea9af34cc3378dcb87cbd35d4,` | Inter Regular | 8.5pt → 11.99px |
| Book/Typography/TableNote | `S:39f2fc4e9bd8d820da2c61c5c854543c714ae2e1,` | Inter Regular | 8pt → 11.29px |
| Book/Typography/FigureCaption | `S:91a9c9749e118992d55c451caaa818943b577269,` | Inter Regular | 8.5pt → 11.99px |
| Book/Typography/DiagramText | `S:39355ff20c08c14a0e0737dafc294c124beda6b4,` | Inter Medium | 9pt → 12.70px (>=9pt effective minimum) |

## Components — 10 created — DONE

| Component | Node ID | Notes |
| --- | --- | --- |
| Book/Component/RunningHead | `9:2` | 9pt, quiet, mirrored left/right label pair, bottom rule |
| Book/Component/PageNumber | `9:5` | Renamed from an interim "Folio" name to match `component-inventory.yaml` exactly |
| Book/Component/Callout | `10:24` (component set) | 4 variants via `Role` property: `Warning` (`10:4`), `Info` (`10:9`), `Verification` (`10:14`), `PythonInsight` (`10:19`). Icon + label + accent border + surface tint — color is never the only signal |
| Book/Component/CodeBlock | `11:2` | JetBrains Mono 9pt, compact padding, real selectable text (not a screenshot) |
| Book/Component/ListingCaption | `11:4` | 9pt, placed immediately below its listing |
| Book/Component/Table | `11:6` | Semantic frame-built table (no native Figma table primitive exists); caption 9pt / header 8.5pt / body 8.5pt / note 8pt |
| Book/Component/FigureCaption | `12:2` | 8.5pt, documented as an atomic pair with its figure |
| Book/Component/Diagram | `12:4` | Renamed from an interim "DiagramContainer" name to match `component-inventory.yaml`. Orthogonal (right-angle) connectors only, 3 labeled nodes, ≥9pt effective label text |
| Book/Component/ChapterHeader | `13:2` | Label (20pt) + title (24pt) + compact deck, restrained accent bar |
| Book/Component/SectionHeader | `21:103` | Added this session (present in `component-inventory.yaml`, not yet built in the prior checkpoint): MajorSection (16pt) + Section (14pt) pair |

**Deferred, not built this round** (out of the explicit scope given for this pass —
flagged for a follow-up, not silently dropped):

- `Book/Component/Callout/AntiPattern` (❌) and `Callout/Milestone` (🎉) — the component
  is built as a variant set, so adding these later is a matter of adding two more
  variants to the existing `10:24` set, not rebuilding it.
- `Book/Component/TableContinuation` (repeated-header continuation behavior) and a
  generic `Book/Component/Figure` (distinct from `FigureCaption`) — both listed in
  `component-inventory.yaml` but not requested in this pass's component list.

## The 6 canonical reference frames — DONE

| # | Frame | Node ID | Page |
| --- | --- | --- | --- |
| 1 | Typography | `8:2` (`Book/Reference/Typography`) | `01 — Foundations` (`0:1`) |
| 2 | Standard Page | `14:2` (`Book/Page/Standard`) | `02 — Page Archetypes` (`2:4`) |
| 3 | Chapter Opener | `15:9` (`Book/Page/ChapterOpener`) | `02 — Page Archetypes` (`2:4`) |
| 4 | Code-Heavy Page | `16:13` (`Book/Page/CodeHeavy`) | `02 — Page Archetypes` (`2:4`) |
| 5 | Table Page | `17:22` (`Book/Page/Table`) | `02 — Page Archetypes` (`2:4`) |
| 6 | Diagram & Callout Page | `18:115` (`Book/Page/DiagramCallout`) | `02 — Page Archetypes` (`2:4`) |

All 5 page-archetype frames (2-6) are built at true physical trim (660×940px = 165×235mm
at the repo's 4px/mm convenience scale), with a non-printing dashed margin guide at the
mirrored text-safe area (80px inner / 60px outer / 72px top / 80px bottom = 20/15/18/20mm),
a `RunningHead` instance, and a `PageNumber` instance placed at the outer edge — modeled
as a recto (right-hand) page; a verso page mirrors the margins and folio position.
Sample content is Russian, for review readability only — structure is language-independent
(no RU-specific components exist; PL/EN would use the same components with different text).

**Note on frame naming**: `Book/Page/DiagramCallout` is a new archetype name, not present
in the original `component-inventory.yaml` 18-page list (which has separate `Figure` and
`Diagram` page entries) — it merges both concerns into the single "Diagram & Callout Page"
this task's brief explicitly asked for. **Open question for the Product Owner**: keep
this merged page as the canonical archetype, or split it into two later?

## Rate-limit history

1. **First session**: Starter plan (~20 MCP calls/month) exhausted while creating the 6
   variable collections. Text-style creation was rejected mid-call.
2. **Retry, same session, reduced scope**: rejected again immediately — confirmed a hard
   monthly quota, not a per-call fluke.
3. **This session**: `whoami` confirmed the "Solo" plan is now **tier: pro**. All
   subsequent writes succeeded normally (200 calls/day, 15/min budget). No further rate
   limiting encountered.

## Build notes / defects found and fixed during this session

- **Text clipping bug**: the `Callout` master component's inner text column was created
  with a fixed 420px width. When the Diagram & Callout page needed a 2×2 grid of
  narrower (~253px) callout instances, their body text clipped instead of wrapping.
  Fixed by changing the master component's content column to `layoutSizingHorizontal:
  FILL` — this self-heals every existing and future instance, since it's a master-
  component-level fix, not a per-instance patch.
- **Page overflow**: the Diagram & Callout page's first layout (diagram + caption + 4
  stacked callouts) ran 116px past the physical page height. Fixed by rebuilding the
  callout section as a 2×2 grid instead of a 4-row stack — content now ends at y=710
  against an 860px safe-area bottom (no overflow).
- **Component shelf overlap**: master components were initially positioned by
  assumption rather than measured height, causing the `CodeBlock` (187px tall) to
  overlap the row below it. Fixed by re-laying the shelf out using each row's actual
  measured max height.
- **Diagram arrow direction**: connector arrowheads initially pointed backward (toward
  the source instead of the destination) due to a rotation-sign assumption. Fixed by
  flipping the rotation from +90° to -90°, verified visually.

## QA result

Performed against the approved metrics in `BOOK-DESIGN-SYSTEM-v1.md`,
`adopted-values.yaml`, and `reference-metrics.yaml`:

| Check | Result |
| --- | --- |
| Page geometry (165×235mm / 660×940px) | ✅ all 5 page frames exact |
| Mirrored margins (inner 20mm/outer 15mm/top 18mm/bottom 20mm) | ✅ verified via guide rectangle bounds on every page frame |
| Typography bound to tokens, not hardcoded | ✅ every text node uses a `Book/Typography/*` style or an explicit variable-bound size |
| No text below approved minimums | ✅ smallest is 8pt (table note), matches spec floor |
| Diagram labels ≥9pt effective | ✅ `DiagramText` style = 9pt / 12.70px |
| Code = 9pt | ✅ `Code` style, JetBrains Mono |
| Body = 10/12pt | ✅ `Body`/`BodyItalic`, 1.20 ratio via bound line-height variable |
| Table text = 8–9pt system | ✅ caption 9 / header 8.5 / body 8.5 / note 8 |
| Semantic emoji rules | ✅ one emoji max per callout heading, only on unnumbered semantic headings, never on numbered section/chapter headings, same icon per role across all 4 usages |
| No locale-specific layout duplication | ✅ single component/frame set; RU is sample content only |
| No overflow/clipping | ✅ both defects found (above) were fixed and re-verified visually |
| Fonts approved (no Lafore fonts) | ✅ Source Serif 4 / Inter / JetBrains Mono only, confirmed via `listAvailableFontsAsync` before use |
| Visual identity — Cartesian School, not Lafore | ✅ restrained indigo/violet, no oversized cards/gradients/heavy shadows, dense print-first layout, confirmed across all screenshots |
| Screenshots captured | ✅ every component and frame screenshotted during the build; final tidy overview screenshots taken of both pages |

**One non-blocking observation**: the 🐍 (Python insight) emoji renders as a fallback
glyph (a running-figure icon) in the headless screenshot service used for this QA pass,
while ⚠️/ℹ️/✅ render correctly. The underlying character is the correct U+1F40D
codepoint — this is very likely a limitation of the screenshot renderer's font stack,
not a defect in the file itself. **Recommend the Product Owner confirm by opening the
file directly in the Figma app** before sign-off.

Cosmetic note: JetBrains Mono renders `->` and `==` as programming-font ligatures in
code samples (e.g. `->` shows as a single arrow glyph). This is a font feature — the
underlying characters are the literal ASCII text, unchanged and fully selectable.

## Visual defect fixes (post-review round)

A live Product Owner review of the "v1 COMPLETE" state (previous section of this log)
found blocking defects that the headless screenshot QA pass had missed or under-
weighted. This section documents each defect, its exact root cause, the fix, and the
affected node IDs — verified against the actual Figma document properties (fills,
`strokeAlign`, `textAutoResize`, `layoutSizingHorizontal`), not just screenshots.

### Defect 1 — white background rectangles inside colored callouts

**Symptom**: in the `Callout` component (all 4 semantic variants) and in the `Table`
header row, text appeared to sit on a paler/whiter patch instead of directly on the
intended tinted surface.

**Root cause**: `figma.createAutoLayout()` (and `figma.createFrame()`) default to an
**opaque white solid fill** unless explicitly cleared. Two inner wrapper frames were
created this way and never had their fill cleared:

- the `Content` auto-layout frame inside each `Callout` variant (holds the label +
  body text) — sat on top of the variant's own semantic surface color (e.g.
  `color/warning-surface`), rendering a white layer over part of the tinted card.
- the `Cell` auto-layout frame used for every header and body cell inside `Table` —
  sat on top of the header row's `color/table-header-surface` tint, making the header
  row render as plain white instead of the intended indigo tint.

**Fix**: set `fills = []` (fully transparent) on every `Content` and `Cell` wrapper.
Because these are **master component** fixes, every existing instance on every page
inherited the correction automatically — no per-instance patches were needed.

**Affected node IDs**:

- `Book/Component/Callout` variants — `Content` frames: `10:6` (Warning), `10:11`
  (Info), `10:16` (Verification), `10:21` (PythonInsight)
- `Book/Component/Table` (`11:6`) — all 20 `Cell` frames across the header row and 4
  body rows (found via `findAll(n => n.name === "Cell")`, not individually enumerated
  by ID since they're structural, not named uniquely)

**Also fixed defensively** (same root cause, present but not visually broken since
these sit against the white page paper rather than a tint): cleared `fills = []` on
the root frames of `Book/Component/ChapterHeader` (`13:2`), `Book/Component/
SectionHeader` (`21:103`), `Book/Component/ListingCaption` (`11:4`), and
`Book/Component/FigureCaption` (`12:2`).

### Defect 2 — text overflow / no-wrap text nodes

**Symptom**: reported as text crossing component/page bounds, especially flagged on
Chapter Opener, Code-Heavy Page, and Diagram & Callout Page.

**Root cause A — missing wrap configuration**: several text nodes were created with
`characters` set but **no** `textAutoResize`/width configuration, leaving Figma's
default `textAutoResize: "WIDTH_AND_HEIGHT"` in effect — single-line, auto-width, **no
wrap capability at all**. For the sample RU text used, the un-wrapped width happened to
fit inside the 520px safe column, so this rendered correctly by coincidence, not by
design — a longer chapter title (a longer RU title, or a PL/EN translation) would have
extended past the page's right margin with nothing to stop it. This is the literal
mechanism behind "must wrap long titles if needed... remain language-independent for
RU/PL/EN."

**Fix**: applied the same recipe used elsewhere in the file — `textAutoResize =
"HEIGHT"` plus `layoutSizingHorizontal = "FILL"` (parent is already auto-layout in
every case) — to every text node that lacked it:

- `Book/Component/ChapterHeader` (`13:2`): label text `13:4` ("Глава 14"), title text
  `13:5` ("Хеш-таблицы и коллизии"). The deck text (`13:6`) already had correct
  FIXED-width + HEIGHT config from the original build and was left unchanged.
- `Book/Component/SectionHeader` (`21:103`): both text children, `21:104` and `21:105`.
- `Book/Component/ListingCaption` (`11:4`): text `11:5`.
- `Book/Component/FigureCaption` (`12:2`): text `12:3`.
- `Book/Component/Diagram` (`12:4`): all 3 node-label texts (`12:6`, `12:8`, `12:10`).
- `Book/Component/Table` (`11:6`): the caption text `11:7` and the note text `11:54`
  (both direct children of the table's root, not inside a `Cell`).
- `Book/Component/Callout` label text (the small uppercase role label, e.g. "ЧАСТАЯ
  ОШИБКА") in all 4 variants — same fix, for the same PL/EN-length-robustness reason.

**Root cause B — an unrealistic code line length**: the Code-Heavy page's `CodeBlock`
instance (`16:20`) contained the line `self._buckets: list[list[tuple]] = [[] for _ in
range(size)]`, long enough that Figma's word-wrap (correctly configured — this text
node already had `textAutoResize: HEIGHT` + `FILL` from the original build) broke it
mid-statement after "in", onto a orphaned `range(size)]` line. Technically not a pixel
overflow (the container grew to fit), but it reads as a layout defect in a print-code
context and violates "wrap only where the source formatting allows, otherwise choose a
realistic line length."

**Fix**: reformatted the sample to drop the inline generic type annotation on that one
line (`self._buckets = [[] for _ in range(size)]`), which fits the 496px code column
with no line exceeding it. No config/property changed — content only. Node: `16:20`'s
text child.

**Root cause C — zero-margin grid**: the Diagram & Callout page's 2×2 callout grid
(`18:135`, `18:140`, `18:145`, `18:150`) was sized so the right column's right edge
landed **exactly** on the print-safe-area boundary (x=600, safe area is 80–600px).
Combined with the `Callout` frame's default `strokeAlign: CENTER` (which renders half
the 1px stroke weight outside the node's nominal bounding box), the border could
visibly breach the safe area by up to 0.5px at 100% zoom — not visible in a downscaled
screenshot, exactly the kind of thing the Product Owner's live-app review would catch
that the headless renderer wouldn't.

**Fix**: two changes — (1) set `strokeAlign = "INSIDE"` on the `Callout` component set
and on `Table`'s grid/row frames, so borders always render fully inside the nominal
bounding box everywhere in the file, not just on this page; (2) narrowed the grid
columns from 253px to 244px and added an 8px inset from each safe-area edge, so the
right column's right edge now sits at x=588 — a 12px margin, not flush.

### QA re-verification (this round)

Re-screenshotted every affected frame after each fix and confirmed by direct property
read (not just visual inspection) that: `Content`/`Cell` fills are empty arrays; text
nodes have `textAutoResize: "HEIGHT"` and `layoutSizingHorizontal: "FILL"`; `strokeAlign`
is `"INSIDE"` on all bordered components; the 2×2 grid's right edge is at 588px against
a 600px safe-area boundary. Frames re-checked: `Book/Component/Callout` (master set),
`Book/Page/Standard` (`14:2`, uses an Info callout instance), `Book/Page/ChapterOpener`
(`15:9`), `Book/Page/CodeHeavy` (`16:13`, uses a Warning callout instance),
`Book/Page/Table` (`17:22`), `Book/Page/DiagramCallout` (`18:115`, all 4 variants). No
overflow, no clipping, no white-patch artifacts remained in any of them, including on
pages where a *fixed instance* of the callout was used rather than the master directly
— confirming the master-component fix correctly propagated to every instance without
needing per-instance patches.

**Not independently re-verifiable from this environment**: this build runs headlessly
against the Figma Plugin API and cannot drive the live Figma web/desktop app directly.
Per the Product Owner's instruction, **please confirm the fixes visually in the live
Figma app at 100% zoom** before final sign-off — the property-level fixes above are
verified at the data level (which is a stronger guarantee for the *mechanism* of the
bugs than a screenshot), but a live-app pixel check is still the right final gate for
anything display/rendering-specific.

### No component geometry changed beyond what's listed above

Trim size, margins, text measure, and every approved type-scale value (20pt chapter
label, 24pt chapter title, 9pt code, 8.5/8.5/8pt table system, etc.) are unchanged. The
only geometry change was the Diagram & Callout page's grid column width (253px →
244px) and position, to create a safe margin; everything else was a fill/stroke/text-
config property fix or a content-only edit (the code sample), not a size or spacing
change to any approved token.

## Deviations from the approved spec (for Product Owner awareness)

- **File location**: still hosted under the personal "Solo" plan, not the "Cartesian
  School" team (View-seat only for this account). Unresolved — see "File" section.
- **Component naming fixes applied this session**: renamed two components to match
  `component-inventory.yaml` exactly (`Folio` → `PageNumber`, `DiagramContainer` →
  `Diagram`). If anything already referenced the old names outside this file, update
  those references.
- **Callout component structure**: built as one `COMPONENT_SET` with a `Role` variant
  property (4 variants) rather than as 6 separate flat components named
  `Book/Component/Callout/<Role>`. This is the more correct Figma pattern (one
  component, one set of variants) and is functionally equivalent, but the literal
  path-style names from `component-inventory.yaml` don't exist as separate components.
  AntiPattern and Milestone variants are not yet added (see "Deferred" list above).
- **`Book/Page/DiagramCallout`** is a new merged archetype name not in the original
  18-page list — see "Open question" under the frames table above.
- **Page count**: still 2 Figma pages (not one per archetype) — this worked fine even
  after the Pro upgrade (Pro removes the 3-page cap, but reorganizing wasn't necessary
  or requested), organized via named frames/sections instead. No token or component
  structure was affected by this choice.
- Everything else — trim size, margins, text measure, full type scale, font-family
  class assignments, color role list, semantic icon set — matches the approved spec
  exactly; no metric deviations were introduced.

## Resume / extension protocol (for the deferred items above)

1. Re-open <https://www.figma.com/design/m19Q51E0vmVek8r4TCJCd8>.
2. To add `AntiPattern`/`Milestone` callout variants: read component set `10:24`,
   create 2 more variant components following the existing 4 as a template (icon ❌ /
   🎉, using `color/danger(-surface)` and a new milestone color respectively — no
   milestone-specific semantic color variable exists yet, would need to be added),
   then `figma.combineAsVariants` is not re-appliable to an existing set — instead add
   the new components as children of the existing `COMPONENT_SET` node directly and
   register the `Role` variant property value on each.
3. To split `Book/Page/DiagramCallout` into separate `Figure`/`Diagram` archetype
   pages, or to add the remaining 12 archetypes from `component-inventory.yaml`'s
   18-page list: follow the same pattern as frames 2–6 (660×940 frame, margin guide
   rectangle, `RunningHead`/`PageNumber` instances, compose from the existing shared
   components).
