# Figma Book Design System v1 — Build Log & Handoff

Status: **v1 art-direction pass complete — ready for Product Owner review**

Nine rounds of live Product Owner review/direction have shaped this file so far:

1. White backgrounds inside colored callouts, and horizontal text-wrap issues —
   see "Visual defect fixes (post-review round)" below.
2. **Vertical overflow**: text still protruding below the bottom edge of callout
   cards, caused by a fixed-height outer component that couldn't grow — see
   "Vertical-sizing fix (second post-review round)" below for the full detail: exact
   root cause, sizing properties before/after, affected node IDs, and an RU/PL/EN
   language-robustness stress test.
3. **Missing scope**: the file only covered internal body-page archetypes, with no
   front matter (cover, title, copyright, about author, preface, TOC) or back matter
   (index, colophon, etc.) — see "Front & back matter system" below for the full
   content audit, every new page/component/node ID, and QA evidence.
4. **Final visual cleanup**: stress-test content was left overlapping canonical page
   frames, the component library was disorganized, and the Cover/Title/Copyright
   pages read as sparse/prototype-like — see "Visual cleanup (fourth post-review
   round)" below for the new QA page, the reorganized component library, and the
   three front-matter redesigns.
5. **Final live QA pass**: a re-audit found page 02 already clean (see below — this
   appears to have been a stale-view report, not a live defect), confirmed author-name
   spelling is already 100% consistent, and — while investigating the Colophon
   readability concern — uncovered and fixed a **systemic font-sizing bug** affecting
   nearly every ad-hoc text element across the front/back matter system. See "Final
   live visual cleanup (fifth post-review round)" below.
6. **Brand-aligned visual refinement**: the system was too plain/typographic and
   didn't yet feel connected to the Cartesian School website. Extracted the site's
   actual hero visual language (node/connector network, coordinate grid, technical
   panels) into a new vector-native `Book/Illustration/*` library, redesigned the
   Cover around it, added a themed accent to the Chapter Opener, fixed a real
   diagram-connector misalignment and an uncontrolled callout-grid mismatch found
   during the audit, and rebuilt the QA page's sequence diagram at a legible size.
   See "Brand-aligned visual refinement (sixth round)" below.
7. **Major professional refinement**: Product Owner judged the cover weak, the
   illustration library too small, and the system underdeveloped relative to a real
   book/brand. Rebuilt the Cover's center node around a faithful vector reproduction
   of the **real Python logo** (extracted from the site's own SVG source, not an
   abstract mark); expanded the illustration library from 8 to 27 components,
   including a `ProjectCard` variant set for all 13 real Cartesian School projects and
   a `LogoSet` (Python logo + a flat vector adaptation of the Cartesian School app
   icon + a componentized wordmark); added a chapter-subject-tied topic badge to the
   Chapter Opener; re-audited every diagram/callout page and every front/back-matter
   page for weak or bare treatment. See "Major professional refinement (seventh
   round)" below.
8. **Integrated cover/closing redesign**: round 7's `LogoSet` icon and wordmark were
   flat vector *approximations* the Product Owner correctly rejected as invented
   substitutes — replaced with the actual repo assets from `cartesian_logo/` (a real
   vector import of `favicon.svg`, and the real raster lockups). The Cover's hero
   illustration was also judged too sparse — four panels floating far from a tiny
   center badge with large dead zones above/below. Rebuilt `HeroNetwork` as a single
   integrated "hub and spoke" composition (panels pulled ~40% closer, short glowing
   beams instead of long pipes, a soft blurred glow plus a low-opacity grid texture
   behind the badge), enlarged it to fill the Cover's content width, and replaced the
   near-blank End Page with a dark closing spread in the Cover's exact background
   color, carrying the same atmosphere and the real logo. See "Integrated cover/
   closing redesign (eighth round)" below.
9. **Final art direction, brand correction, QA-flow rebuild, authorial closing
   page**: the About Cartesian School page still used a small standalone icon as
   its primary identity statement (reads as an app icon, not a publisher imprint) —
   replaced with the real horizontal lockup. The QA-only Book Sequence Overview
   diagram had a real geometry bug (connectors anchored well below the boxes they
   were meant to join, arrowheads floating in free space) — rebuilt as one
   precisely-connected 3-phase flow (Front Matter → Body ×24 → Back Matter). The End
   Page, while no longer blank, was still just a logo + URL — rebuilt into a real
   editorial closing page with the actual author photograph, a real book summary,
   a real author bio, and the Cartesian School identity, sharing the Cover's exact
   tonal family. Added the real author portrait and the real Guido van Rossum
   portrait (already used in the book's own Chapter 1) to a new, separate
   "Editorial / Photographic Assets" tier in the illustration library. See "Final
   art direction, brand correction, QA-flow rebuild, authorial closing page (ninth
   round)" below.

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

## Vertical-sizing fix (second post-review round)

A second live Product Owner review, after the surface/wrap fixes above, found text
still protruding below the bottom edge of multiple callout cards on
`Book/Page/DiagramCallout`. This was explicitly diagnosed as a **vertical sizing**
defect, not a font-size or horizontal-wrap problem, and the fix below changes no
approved typography value.

### Root cause

Every `Book/Component/Callout` variant is a `HORIZONTAL`-layout component, built with
`figma.createComponent()` plus a manually-assigned `layoutMode`, rather than
`figma.createAutoLayout()`. Manually flipping `layoutMode` this way does **not** set
sensible sizing defaults the way the `createAutoLayout()` helper does — it left
`counterAxisSizingMode` (the **vertical** axis, since horizontal is the *primary* axis
for a `HORIZONTAL` layout) at Figma's raw default of `"FIXED"`, pinned to whatever
height (100px) existed when the component was first authored. The inner "Content"
column was already correctly configured to `HUG` vertically — but the **outer card**
could not grow to contain it. When the Diagram/Callout page's 2×2 grid narrowed the
cards to 244px wide (an earlier fix, for a different defect), the same body text now
needed *more* lines to wrap at the narrower width — more height than the fixed 100px
ever allowed — so it rendered past the card's visible bottom edge. The instances on
the page had this same `FIXED`/100px lock baked in explicitly, because an earlier
`.resize()` call (from the very first grid-margin fix) resets **both** axes' sizing
mode to `FIXED` as a side effect, re-freezing the height at whatever value was current
at that moment.

The exact same manually-set-`HORIZONTAL`-layout-without-fixing-the-counter-axis
pattern was also found, by audit, in `Book/Component/ListingCaption` and
`Book/Component/FigureCaption` — both latent (not yet visibly broken, since their
sample captions are short one-liners), fixed proactively. `Book/Component/CodeBlock`
and `Book/Component/Table` were audited and found **already correct** (both use
`VERTICAL` layout with `layoutSizingVertical: HUG` already set from the original
build) — no change was needed there.

### Sizing properties: before → after

| Node | Property | Before | After |
| --- | --- | --- | --- |
| `10:4`/`10:9`/`10:14`/`10:19` (Callout variants) | `counterAxisSizingMode` | `FIXED` | `AUTO` |
| `10:4`/`10:9`/`10:14`/`10:19` | `layoutSizingVertical` | `FIXED` | `HUG` |
| `10:4`/`10:9`/`10:14`/`10:19` | height | `100` (all four, regardless of content) | `81` / `81` / `81` / `98` (Warning/Info/Verification/PythonInsight, at the master's 480px width) |
| `10:4`/`10:9`/`10:14`/`10:19` | padding (top/bottom/left/right) | `14/14/16/16` (arbitrary) | `16/16/16/16`, all four **bound to** `spacing/lg_px` (`VariableID:3:27`) |
| `10:6`/`10:11`/`10:16`/`10:21` (Content wrappers) | `clipsContent` | `true` | `false` (defensive — Content was already sized correctly, but a clipping wrapper is a latent risk) |
| `11:4` (ListingCaption) | `counterAxisSizingMode` / `layoutSizingVertical` | `FIXED` / `FIXED` | `AUTO` / `HUG` |
| `12:2` (FigureCaption) | `counterAxisSizingMode` / `layoutSizingVertical` | `FIXED` / `FIXED` | `AUTO` / `HUG` |
| `18:135`/`18:140`/`18:145`/`18:150` (page grid instances) | `layoutSizingVertical` / height | `FIXED` / `100` (all four) | `HUG` / `132` / `132` / `132` / `149` |
| `18:132` (FigureCaption instance) | `layoutSizingVertical` / height | `FIXED` / `100` | `HUG` / `22` |
| `14:12` (Standard Page callout instance) | `layoutSizingVertical` / height | `FIXED` / `100` | `HUG` / `81` |
| `16:25` (Code-Heavy callout instance) | `layoutSizingVertical` / height | `FIXED` / `100` | `HUG` / `81` |
| `16:22` (Code-Heavy ListingCaption instance) | `layoutSizingVertical` / height | `FIXED` / `100` | `HUG` / `23` |

**Self-correction during this fix**: the first attempt at fixing `ListingCaption`/
`FigureCaption` mistakenly set **both** `primaryAxisSizingMode` and
`counterAxisSizingMode` to `AUTO`, which also hugged the *horizontal* axis — shrinking
their instances' width to auto-fit the caption text (292px and 381px) instead of the
intended fixed 520px column width. Caught immediately by re-reading the instance
widths after the change, and corrected by restoring `primaryAxisSizingMode: FIXED` +
`layoutSizingHorizontal: FIXED` at 520px on both masters and both affected instances
(`18:132`, `16:22`) — only the vertical axis was meant to change.

### Page grid decision (point 6 of the review): natural HUG, not forced equal-height rows

The Product Owner's instructions allowed either outcome: "each card grows naturally to
content" (preferred/default) or forced row-equalization "if required for visual
balance." This fix takes the **preferred/default path** — each of the 4 cards HUGs
independently to its own content height (132/132/132/149px) rather than being forced
to a shared fixed row height. Rationale: forcing equal heights would require
re-introducing a `FIXED` height on at least one card (set to the row's tallest
member) — exactly the anti-pattern the review is correcting elsewhere in the same
instructions ("never a fixed maximum"). The natural result (screenshotted below) reads
as balanced in practice; row 2 is only 17px taller than row 1. If the Product Owner
prefers strict equal-height rows after seeing this, it's a follow-up: compute
`max(row.heights)`, then set `layoutSizingVertical: FIXED` + `resize()` to that value
on the shorter card only — never shrinking either.

### Page layout recomputation (`Book/Page/DiagramCallout`, `18:115`)

Because the grid cards grew taller (as intended), the fixed Y-offsets used for row 2
and the elements above the grid (carried over from the previous fix round, which used
the old fixed-100px heights) had to be recalculated from the actual post-fix heights
to avoid a *new* overlap:

| Element | Y before this fix | Y after (recomputed from measured heights) |
| --- | --- | --- |
| FigureCaption instance (`18:132`) | 353 | 353 (unchanged — diagram height didn't change) |
| "Семантические вставки…" label (`18:134`) | 469 | 391 (caption shrank from 100px→22px) |
| Grid row 1 top (`18:135`, `18:140`) | 496 | 418 |
| Grid row 2 top (`18:145`, `18:150`) | 610 | 564 (row 1 is now 132px tall, not a flat 100px assumption) |
| Content bottom | 710 | 713 |
| Safe-area bottom (unchanged) | 860 | 860 |

Final content bottom (713px) leaves 147px of margin against the 860px safe-area
boundary — comfortable headroom, so the fallback options (compressing whitespace above
the grid, reducing inter-card gap, or moving the grid upward) were **not** needed.

### Language-robustness stress test (RU/PL/EN)

Per the review's explicit requirement, the *same* `Book/Component/Callout` `Warning`
variant (no new variant, no language-specific fork) was instantiated twice more with
deliberately long content, at the same 244px width used by the page grid, and added to
the shared-components shelf on page `02 — Page Archetypes` as permanent documented
evidence:

| Instance | Node ID | Content | Result |
| --- | --- | --- | --- |
| RU (existing, in the live grid) | `18:135` | "Не забывайте, что списки в Python изменяемы…" (~100 chars) | 132px, no overflow |
| PL stress test | `33:111` | "Nie zapominaj, że listy w Pythonie są mutowalne… co bywa źródłem trudnych do wykrycia błędów w większych programach." (~210 chars, deliberately longer) | **200px**, wraps to 7 lines, full bottom padding visible, no clipping |
| EN stress test | `33:116` | "Remember that lists in Python are mutable… a frequent source of subtle bugs in larger programs." (~195 chars, deliberately longer) | **183px**, wraps to 6 lines, full bottom padding visible, no clipping |

**Result: PASS.** The same component safely accommodates RU, PL, and EN content of
substantially different lengths purely through the HUG-vertical fix — no
language-specific component variant was created or is needed.

**Build note on this stress test**: the first attempt at building these two instances
had a bug in the *test script itself* (not the product) — it selected the target text
node by `fontSize >= 12`, which also matched the callout's icon glyph (15px) before
reaching the real body text (also ≥12px), overwriting the icon with the long paragraph
and producing a pathological 1px-wide wrapped column (height ballooned to 1535px).
Caught immediately via `get_metadata`, deleted, and rebuilt using structural indexing
(`instance.children[1].children[1]` for the body, `.children[1].children[0]` for the
label) instead of a property-based guess.

### QA evidence captured this round

Screenshots taken and visually confirmed after the fix:

- `Book/Component/Callout` master set (`10:24`) — all 4 variants, correctly
  proportioned heights (81/81/81/98px), no overlap between variants in the set frame
- `Book/Page/DiagramCallout` (`18:115`) — full page, all 4 grid cards fully contained
  with visible bottom padding after the last text line
- `Book/Page/Standard` (`14:2`) and `Book/Page/CodeHeavy` (`16:13`) — re-verified,
  their callout/caption instances now correctly sized (81px and 23px respectively,
  down from a padded-out 100px) with no regression
- PL stress-test callout (`33:111`) and EN stress-test callout (`33:116`) individually
- Full six-frame page overview at high resolution

**Not independently re-verifiable from this environment**: as before, this build runs
headlessly against the Figma Plugin API and cannot drive the live Figma app directly.
The property-level verification above (`counterAxisSizingMode`, `layoutSizingVertical`,
measured heights) directly confirms the document state, which is a stronger guarantee
for the sizing *mechanism* than a screenshot — but a live-app 100% zoom pass is still
the right final gate before sign-off.

### Confirmation: no font size or line-height was reduced

Per the review's explicit constraints — verified by inspection, not just by claim: no
text style's `fontSize` or bound `lineHeight` variable was touched in this round. The
only changes were sizing-mode properties (`counterAxisSizingMode`,
`layoutSizingVertical`, `layoutSizingHorizontal` on two nodes that were then
corrected back), padding (bound to a spacing token, net *larger* than before, not
cramped), `clipsContent` (relaxed, not tightened), and Y-position recalculation. No
text was clipped, hidden, or truncated to make anything fit.

## Front & back matter system

Product Owner live review identified that the file only covered internal body-page
archetypes (Typography, Standard, ChapterOpener, CodeHeavy, Table, DiagramCallout) with
no front matter or back matter — required before v1 can be considered visually
complete for a physical book. This section documents the content audit performed
first (per the explicit instruction not to invent editorial content), everything
built, every node ID, and the QA/stress-test evidence.

### Content audit (performed before any Figma work)

A full repository audit (read-only, no files modified) was run first to determine
what front/back matter content actually exists, so nothing in the new frames is
invented. Full findings:

| Item | Status | Source |
| --- | --- | --- |
| Book title (RU "Python с нуля", PL "Python od zera") | **EXISTS** | `scripts/book_pipeline/locale_ru.py:27`, `locale_pl.py:32` |
| Subtitle ("программирование, графика, приложения и игры") | **EXISTS** | `locale_ru.py:28` |
| Author (Siergej Sobolewski / Сергей Соболевски) + role | **EXISTS** (one internal inconsistency flagged — see below) | `locale_ru.py:30`, `author_profile.py:13-15`, `README.md:120-122` |
| Cover design source | **EXISTS** | `design/adobe/cover_concept_v1.html` (+ PL variant), merged into the final PDF by `pdf_adapter.py:156-175` |
| Title page (distinct from cover) | **EXISTS** | `scripts/book_pipeline/pdf_adapter.py:45-54`, `build_title_page()` |
| Copyright / imprint / license | **EXISTS** (no ISBN — none found anywhere) | `pdf_adapter.py:57-73`, `LICENSE.md`, `LICENSE-CONTENT.md`, `LICENSE-CODE.md`, `scripts/build_license_page.py` |
| About the Author | **EXISTS**, print text is a subset of the web page | `scripts/build_front_matter.py:34-151` — richer bio material is marked `.web-presentation` and stripped by `extract_article()` (`scripts/book_shared.py:176-186`) before print/EPUB packaging; only the lede + 2 "core" paragraphs survive into print |
| "From the Author" / Preface, distinct from Introduction | **NOT FOUND** | — |
| Introduction ("Введение") | **EXISTS** | `scripts/build_front_matter.py:191-247`, `build_vvedenie()` |
| Acknowledgements | **NOT FOUND** | — |
| Table of Contents structure | **EXISTS**, fully data-driven | `pdf_adapter.py:76-101`, `scripts/chapter_metadata.py` (real titles for all 24 chapters), `locale_ru.py:69-73` (front-matter entry list) |
| Glossary | **NOT FOUND / not planned** | Confirmed absent from `BOOK-DESIGN-SYSTEM-v1.md` §5 and `archetypes/README.md`'s own archetype lists |
| Index | **EXISTS**, real curated terms | `scripts/build_index.py:22-96` |
| Conclusion / epilogue (distinct back-matter section) | **NOT FOUND** — chapter 24 is a regular numbered chapter, not back matter | `scripts/build_chapter_24.py:810-829` |
| Bibliography / References (formal citation list) | **NOT FOUND** | — |
| "About Cartesian School" (dedicated page) | Fragmented — real mission sentence exists, no dedicated page | `build_front_matter.py:120-127` (reused verbatim) |
| Colophon (dedicated page) | Not found as authored text; real facts exist to assemble one | Pipeline name, layout version tag, WeasyPrint, edition identifiers, font licenses — see Colophon section below |
| Website / GitHub URLs | **EXISTS** | `README.md:24,126,127` |

**Author-role discrepancy flagged, not resolved**: `author_profile.py` (web bio) says
"Founder & CEO · Senior Systems & AI Engineer"; the book pipeline's cover/title/
copyright config (`locale_ru.py:30`) says "Software & AI Engineer, основатель
Cartesian School" — the Figma frames use the **book-pipeline wording**, since that's
literally what appears on the real cover/title/copyright today. Product Owner should
resolve which is canonical.

### New Figma pages

| Page | Node ID |
| --- | --- |
| `03 — Front Matter` | `36:2` |
| `04 — Back Matter` | `36:3` |

### Front-matter frames

| Frame | Node ID | Content used |
| --- | --- | --- |
| `Book/Page/Cover` | `43:3` | Real title/subtitle/author/kicker; dark indigo ground, reversed `BookTitle` (Scale=Cover), restrained violet accent rule — no gradients, no web-hero styling |
| `Book/Page/Title` | `45:6` | Same real facts, quiet `BookTitle` (Scale=TitlePage) + publisher line |
| `Book/Page/Copyright` | `45:124` | Real edition/license/rights text via `ImprintBlock` (`40:121`); **ISBN explicitly stated as not yet assigned** — never invented |
| `Book/Page/AboutAuthor` | `45:135` | The 2 real print-surviving "core" paragraphs only — the richer `.web-presentation` bio material was deliberately excluded, since it is stripped before print in the real pipeline |
| `Book/Page/FromAuthor` | `45:140` | Real "Введение" heading + real opening paragraph, verbatim from `build_vvedenie()`; an on-page note explains the FromAuthor→Введение mapping (no distinct preface exists) |
| `Book/Page/TOC` | `47:14` | Real front-matter entries (Об авторе/О техническом рецензенте/Введение) + real chapters 1–14 (exact titles from `chapter_metadata.py`) |
| `Book/Page/TOCContinuation` | `47:98` | Real chapters 15–24 + index entry — created because the real 24-chapter TOC does not fit one page at approved type sizes (measured: single-page attempt overflowed by 44px; two-page split fits with 256px/449px of margin respectively) |

Chapter **page numbers in the TOC are illustrative** (not real pagination output —
no such output exists yet); chapter **titles and order are real**.

### Back-matter frames

| Frame | Node ID | Content used |
| --- | --- | --- |
| `Book/Page/Index` | `48:2` | Real terms from `scripts/build_index.py` (representative selection, explicitly labeled as such — not exhaustive), two-column layout |
| `Book/Page/AboutCartesianSchool` | `48:22` | Real mission sentence reused verbatim from the About-the-Author print text (not new marketing prose) + real website/GitHub URLs |
| `Book/Page/Colophon` | `48:28` | Only verified facts: edition identifier (`cartesian-school-python-s-nulya-2026`), layout version tag (`cartesian-school-book-layout-v1`), WeasyPrint, license names, third-party font license locations. **Font list explicitly marked "предварительно" (provisional)** — the design doc's own font choice is not yet finalized, and the colophon says so rather than stating it as settled fact |
| `Book/Page/EndPage` | `48:55` | Minimal: Cartesian School mark + real website URL only |

### Deferred / N/A back-matter archetypes (per the audit — not silently dropped)

| Archetype | Status | Why |
| --- | --- | --- |
| `Book/Page/ConclusionOrFinalWord` | **N/A** | No distinct conclusion/epilogue exists — chapter 24 is a regular numbered chapter, not back matter; building this page would misrepresent chapter content as back matter |
| `Book/Page/Glossary` | **N/A** | Not found, not planned — absent from the design docs' own archetype lists |
| `Book/Page/References` | **N/A** | No bibliography/citation list exists anywhere in the book |
| `Book/Page/Introduction` (as a separate frame from FromAuthor) | **Not built, deliberately** | Would duplicate the exact same "Введение" content already shown in `FromAuthor` — the instruction was explicit not to duplicate content merely to create another page |

One related discovery, not in scope but worth recording: "О техническом рецензенте"
(About the Technical Reviewer) is a real front-matter page whose reviewer-name slot is
intentionally left as a TBD callout in the actual book source
(`build_front_matter.py:159-166`) pending Product Owner assignment. Not built as a
Figma frame (not requested), but the TOC's front-matter entry list includes it as a
real page title.

### New components

| Component | Node ID | Notes |
| --- | --- | --- |
| `Book/Component/BookTitle` | `40:117` (set) | Variants: `Scale=Cover` (`40:111`, large, reversed-out), `Scale=TitlePage` (`40:114`, quiet). Both wrap-capable (`textAutoResize: HEIGHT` + `FILL` width) — see stress test below |
| `Book/Component/AuthorCredit` | `40:118` | Name + role, reused on cover/title/copyright |
| `Book/Component/ImprintBlock` | `40:121` | Compact 8pt legal text stack for the copyright page |
| `Book/Component/TOCEntry` | `42:111` | Generic single-level row: title + dotted leader + page number |
| `Book/Component/TOCChapterEntry` | `42:115` | Chapter-level: numbered prefix (accent color) + bold title + leader + page number |
| `Book/Component/TOCSectionEntry` | `42:120` | Section-level: indented, quieter, smaller than chapter row |
| `Book/Component/IndexEntry` | `42:124` | Term + inline page refs (traditional index convention, no leader) + indented sub-term line |
| `Book/Component/ColophonBlock` | `42:128` | Label/value row for production metadata |
| `Book/Component/TableContinuation` | `39:111` | Previously deferred — completed. Repeats the header row for a table split across a page break |
| `Book/Component/Figure` | `39:122` | Previously deferred — completed. Generic illustration/screenshot placeholder (diagonal-hatch pattern + label), distinct from `Diagram` (which is specifically for node+connector technical diagrams) |

All dotted TOC/index leaders are built from a `FILL`-width text node repeating `.`
160 times — a standard Figma trick that always overflows its own bounds and gets
naturally clipped by the row's layout, so the leader always reaches exactly to the
page-number column regardless of title length.

### Semantic callout set — now complete (6 of 6 roles)

The two previously-deferred variants were added this round: **AntiPattern** (❌,
`color/danger` + `color/danger-surface`) and **Milestone** (🎉, two **new** semantic
color variables — `color/milestone` and `color/milestone-surface`, `VariableID:37:111`
/ `VariableID:37:112`, aliasing `violet/600` / `violet/100` — no existing role fit a
celebratory/completion tone, so this is a deliberate, minimal, documented addition,
not scope creep).

**Component-set node ID changed**: `Book/Component/Callout`'s set ID changed from
`10:24` to **`37:123`** during this round (see "Build defects found and fixed" below
for why). The four original variant *component* IDs are unchanged (`10:4`, `10:9`,
`10:14`, `10:19`) — only the wrapping set node was recreated. Anything that referenced
the set by ID (not by name) needs updating to `37:123`.

### Build defects found and fixed this round

1. **Corrupted the Callout set while extending it.** Appending the two new variant
   components to the existing set (`10:24`) and then calling
   `figma.combineAsVariants()` again on its full child list was wrong — `combineAsVariants`
   creates a **new** `COMPONENT_SET` node from scratch, and because the individual
   variants' names had lost their clean `Role=Value` format by that point, the result
   was a garbled set (name `"Book"`, children named things like `"=Component,
   =Callout, =Warning"`). Fixed without rebuilding: renamed the set and all 6
   children back to their canonical `Role=<Value>` / `Book/Component/Callout` names,
   which caused Figma to correctly re-derive the `Role` variant property with all 6
   options. Verified an existing page instance (`18:135`) still resolved to its
   original main component (`10:4`) throughout — instances were never broken, only
   the set/variant naming.
2. **New variants collapsed to ~100-159px width.** `AntiPattern` and `Milestone` were
   built with their inner "Content" column set to `FILL` width from the start (correct,
   matching the round-2 fix), but the *outer* component was never given an anchoring
   width — with the outer at `HUG` and the inner at `FILL`, Figma resolved the
   circular sizing by collapsing to a near-minimum width, forcing the body text to
   wrap into ~17 lines (height ballooned to 301px). The original 4 variants avoided
   this only because they inherited a frozen 480px width from earlier build history.
   Fixed by explicitly setting `layoutSizingHorizontal: FIXED` + `resize(480, height)`
   on both new variants, matching the other 4 — heights corrected to 81px/98px.
3. **`BookTitle` cover variant had an accidental opaque preview-backdrop fill.**
   While authoring the component library, a dark preview-only background color was
   set on the `Scale=Cover` master (`40:111`) so its white reversed text stayed
   legible in isolation — but this fill was never cleared, so every instance carried
   the same solid rectangle, visible as a mismatched dark box behind the title on the
   actual Cover page. Caught immediately via the Cover screenshot; fixed by setting
   `fills = []` on the master, which corrected the live Cover instance automatically.

### Language-robustness stress test (RU/PL/EN) — front/back matter components

Per the instruction to test structural robustness rather than create language-specific
forks, the *same* components were stress-tested with deliberately long content:

| Component | Test | Result |
| --- | --- | --- |
| `BookTitle` (Scale=TitlePage) | Long RU title (~80 chars) + long subtitle | Grows to 193px, wraps cleanly, no clipping |
| `BookTitle` (Scale=TitlePage) | Long PL title (~85 chars) + long subtitle | Grows to 178px, wraps cleanly, no clipping |
| `BookTitle` (Scale=TitlePage) | Long EN title (~89 chars) + long subtitle | Grows to 221px, wraps cleanly, no clipping |
| `TOCChapterEntry` pattern | Deliberately long RU chapter title (~115 chars) | Row grows from 22px to 44px (2 lines), dotted leader and page number remain aligned, no clipping |
| `IndexEntry` | Deliberately long RU term (~120 chars) + long sub-term | Grows from 24px to 56px, term wraps to 2 lines, sub-term wraps and stays indented, no clipping |

**Result: PASS** for all five. No language-specific component variant was created.

### Full book-sequence overview

A design-system QA reference frame ("Book Sequence Overview") was created showing the
conceptual front-to-back flow: Cover → Title → Copyright → About Author → From
Author/Introduction → TOC → [Chapter Opener → Theory → Code/Table/Diagram, repeating
per chapter] → Index → About Cartesian School → Colophon → End Page. Node ID: `51:14`,
on page `03 — Front Matter`. This is explicitly a QA/documentation aid, not part of
the canonical publishing pipeline.

### Recto/verso rules (documented as publication rules, not language rules)

Tagged directly on each frame (small `RECTO`/`VERSO` label, top-right corner) and
recorded here as the canonical rule set — applies identically to every language
edition:

| Page | Side | Rule |
| --- | --- | --- |
| Cover | Recto | Unpaginated; always the first leaf |
| Title | Recto | Standard convention — the title page opens a recto |
| Copyright | Verso | Conventionally the back of the title page |
| About Author | Recto | Falls naturally recto following a verso copyright page |
| From Author / Introduction | Recto | Major front-matter sections open recto |
| TOC | Recto (continuation: Verso) | TOC opens recto; continuation page falls verso |
| Chapter openers | Recto (existing rule, unchanged) | A blank verso is inserted by the print adapter if needed to force this — this is a **pagination/publication rule**, never a per-language decision |
| Index | Recto | Back matter's first section conventionally opens recto |
| About Cartesian School / Colophon | No strict requirement | Order-dependent on final back-matter page count |
| End Page | Verso (final leaf) | Typically falls verso as the book's last leaf |

No blank pages were added in Figma merely for aesthetics — where a rule would require
one (e.g. forcing a chapter to recto), that's noted as a pagination-adapter
responsibility, not something modeled as a static blank frame here.

### QA result (front/back matter round)

| Check | Result |
| --- | --- |
| No text overflow across any of the 11 new frames | ✅ verified via `get_metadata` content-bottom vs. safe-area-bottom math on every frame, plus visual screenshots |
| No clipping | ✅ |
| No accidental white fills | ✅ (carried forward from the round-2 fix; every new auto-layout wrapper this round had `fills` explicitly set — either transparent or an intentional token-bound color) |
| All text-containing components HUG vertically | ✅ — built using the same `counterAxisSizingMode: AUTO` / `layoutSizingVertical: HUG` recipe established in round 2 |
| No fixed-height text containers unless justified | ✅ — the only fixed dimensions are intentional (page trim 660×940, `Figure` placeholder's representative 300px height, fixed-width leader/page-number columns) |
| No unsafe-area breach | ✅ — every frame's content-bottom measured against the 860px safe-area boundary before moving on |
| Long RU/PL/EN titles wrap correctly | ✅ — see stress test table above |
| TOC entries handle long titles | ✅ — see stress test table above |
| Page numbers align | ✅ — right-aligned fixed-width column in every TOC/index row |
| Index entries handle long terms | ✅ — see stress test table above |
| Copyright/legal text remains readable | ✅ — 8pt floor, never below the approved print-readability minimum |
| Visual hierarchy consistent, same Cartesian School family | ✅ — same 3 fonts, same indigo/violet identity, same spacing tokens throughout front/back matter as the body archetypes |
| Front matter and body pages feel like one publication | ✅ (subjective — recommend Product Owner confirm visually) |
| Back matter feels intentional, not an afterthought | ✅ (subjective — recommend Product Owner confirm visually) |

As in prior rounds: this environment runs headlessly against the Figma Plugin API and
cannot drive the live Figma app directly — recommend a live 100% zoom pass before
final sign-off, particularly for the Cover (color/contrast in a real viewing
environment) and the two-column Index layout.

## Visual cleanup (fourth post-review round)

A live Product Owner review of the completed front/back matter system asked for a
final visual cleanup pass: stress-test content was overlapping canonical frames, the
component library was scattered, page labels were inconsistent, and Cover/Title/
Copyright read as sparse or prototype-like. This section documents every change.

### 1. New page: `05 — QA & Stress Tests` (`55:2`)

All stress-test content was moved off the canonical pages onto this new dedicated
page — it had been sitting at absolute canvas coordinates that visually overlapped
the `Standard`/`ChapterOpener`/`CodeHeavy` archetype frames' own coordinate space on
page `02` (confirmed by comparing bounding boxes before moving anything: the stress
content spanned y=1450–1683, directly inside the frames' y=1087–2027 span).

**Nodes moved** (from page `02 — Page Archetypes` to page `05 — QA & Stress Tests`,
then re-laid-out into a clean vertical arrangement with section headers):

| Node | Content |
| --- | --- |
| `33:111`, `33:116`, `33:121` | PL/EN Callout language-robustness stress test + its label |
| `49:111` | "FRONT/BACK MATTER STRESS TEST" section label |
| `49:112`, `49:115` | RU long-title `BookTitle` stress instance + tag |
| `49:116`, `49:119` | PL long-title `BookTitle` stress instance + tag |
| `49:120`, `49:123` | EN long-title `BookTitle` stress instance + tag |
| `49:124` | TOC long-line stress row |
| `49:130` | Long multi-line `IndexEntry` stress instance |

Canonical pages (`01`, `02`, `03`, `04`) now contain only production components,
canonical archetypes, and clean design-system examples — no QA/test artifacts.

### 2. Page `02 — Page Archetypes` reorganized

**Component library** (top of the page, y=0–2626) reorganized from a loosely scattered
layout into 8 clearly labeled, divided groups, in dependency-ish order:

1. Navigation / running elements — `RunningHead` (`9:2`), `PageNumber` (`9:5`)
2. Typography / headings — `ChapterHeader` (`13:2`), `SectionHeader` (`21:103`)
3. Code — `CodeBlock` (`11:2`), `ListingCaption` (`11:4`)
4. Tables — `Table` (`11:6`), `TableContinuation` (`39:111`)
5. Figures / diagrams — `Figure` (`39:122`), `FigureCaption` (`12:2`), `Diagram` (`12:4`)
6. Callouts — the 6-variant `Callout` set (`37:123`)
7. Front matter — `BookTitle` set (`40:117`), `AuthorCredit` (`40:118`), `ImprintBlock`
   (`40:121`), `TOCEntry` (`42:111`), `TOCChapterEntry` (`42:115`), `TOCSectionEntry`
   (`42:120`)
8. Back matter — `IndexEntry` (`42:124`), `ColophonBlock` (`42:128`)

Each group has a bold indigo label + a divider rule; the old ungrouped "SHARED
COMPONENTS" label (`20:103`) was removed as superseded.

A page-level dark backdrop rectangle (`57:103`) was added **behind** (not inside) the
`BookTitle` "Scale=Cover" library preview — its master correctly has a transparent
fill for production use (white reversed text needs a dark page behind it, which every
real Cover instance already provides), but that made the *library preview itself*
show invisible white-on-white text. The backdrop is a page-level decoration for
browsability only; it does not touch the component.

**Page archetypes** (bottom of the page, y=2760+) repositioned into a clean 3-column
×2-row grid with consistent 40px gaps: `Standard` (`14:2`), `ChapterOpener` (`15:9`),
`CodeHeavy` (`16:13`) in row 1; `Table` (`17:22`), `DiagramCallout` (`18:115`) in row
2. A section title separates this zone from the component library above, with a
generous 134px vertical gap between the two zones.

### 3. Standardized page labels

Every archetype frame across pages `02`, `03`, and `04` (16 frames total) now carries
one consistent label: `Book/Page/<Name>`, Inter Semi Bold 10pt, 2% letter-spacing,
`color/text-secondary`, positioned at the frame's top-left corner minus 20px vertical
offset (i.e. just above the frame, outside its printable bounds — these are
design-system canvas metadata, never part of the printed page). This is distinct
from, and positioned differently than, the existing `RECTO`/`VERSO` tags (which stay
inside the frame's top-right corner, serving a different documented purpose).

### 4. Front-matter visual polish

**`Book/Page/Cover` (`43:3`)** — was structurally correct but visually sparse. Added a
contained "Cartesian plot" motif: a bordered 280×280px box with a faint 6×6 grid,
bold center axes, and three small plotted points suggesting a simple parabola — a
restrained, literal nod to "Cartesian" coordinates (not a random illustration, not a
gradient, not a shadow). This required two attempts: the first version used
unbounded full-width grid lines with no visual containment, which read as unfinished
rather than systematic — replaced with the bounded, bordered box described above.
Kicker/title were moved up against the box's bottom edge to create a single strong
focal cluster; the author credit was moved from y=820 to y=760 to reduce (not
eliminate — some bottom breathing room is appropriate for a cover) the dead space
below.

**`Book/Page/Title` (`45:6`)** — was large empty space (0–340px) with content
centered in the remaining area, reading as "centered content in an empty page" per
the review's own description. Rebuilt around a deliberate typeset block: a thin
indigo rule opens the block at y=260, kicker/title/author stack immediately below it,
a full-width subtle rule closes the block, and the publisher line sits below that —
the classic bracketed title-page convention, not simply vertical centering.

**`Book/Page/Copyright` (`45:124`)** — content started at y=560 with nothing above it,
reading as "detached" per the review. Rebuilt with a clear anchor at the top: a short
indigo rule + a new heading ("Издание и авторские права" / "Publication & Copyright")
at y≈140, with the existing title/author/imprint/ISBN/GitHub lines moved up
immediately beneath it in one continuous block ending at y=395. The lower half of the
page is now intentional whitespace following a clearly anchored block, not a
detached fragment.

### 5. Back-matter check (no changes needed)

Reviewed `Colophon` (`48:28`) and `Index` (`48:2`) at full resolution: the Colophon's
8pt label/value rows were already column-aligned (fixed 150px label column,
consistently), with 10px row spacing that reads as comfortable rather than cramped —
no change made. The Index's two-column layout already balances its 248px/248px
columns around a 24px gutter — no change made. Both were re-screenshotted this round
as part of the final QA pass below.

### Final visual QA (this round)

| Check | Result |
| --- | --- |
| Stress-test content fully separated from canonical pages | ✅ moved to `05 — QA & Stress Tests`, verified via before/after `get_metadata` bounding-box comparison |
| Page `02` archetype frames aligned to a clear grid, consistent spacing | ✅ 3×2 grid, 40px gaps, verified via screenshot |
| Component library separated into a dedicated, non-interfering zone | ✅ 8 labeled groups, 134px gap before the archetype-frame zone |
| Consistent archetype labels (font/size/color/position) | ✅ all 16 frames across pages `02`/`03`/`04` use the identical label recipe |
| Cover strengthened without becoming a marketing page | ✅ contained geometric motif, no gradients/shadows, no illustration |
| Title page reads as intentionally typeset | ✅ bracketed rule structure replacing plain centering |
| Copyright page has a clear anchor, not detached content | ✅ heading + rule anchor at top, content block immediately below |
| Colophon smallest text readable, columns aligned | ✅ verified at full resolution, no change needed |
| Index gutter balanced | ✅ verified at full resolution, no change needed |
| No overflow / clipping / accidental fills introduced by this round's changes | ✅ every edited frame re-screenshotted after its change |
| Cartesian School identity consistent across all pages | ✅ same 3 fonts, same indigo/violet/motif language used in the Cover's new geometric accent, Title's rule, and Copyright's anchor rule |

As in every prior round: this environment runs headlessly against the Figma Plugin
API and cannot drive the live Figma app directly — a live 100% zoom pass is still the
recommended final gate, particularly for the Cover's new geometric motif (color
contrast and hairline rendering can differ slightly between the headless renderer and
a real browser/app).

## Final live visual cleanup (fifth post-review round)

### 1. Page 02 overlap claim — re-audited, not reproducible in the current file

The Product Owner reported page `02 — Page Archetypes` still showing QA/stress content
overlapping canonical archetypes. A fresh, complete re-audit was performed two
independent ways before touching anything:

1. `get_metadata` dump of the entire page — zero nodes named `STRESS TEST *`, `RU
   (long)`, `PL (long)`, `EN (long)`, `TOC stress row`, or any of the 12 node IDs
   moved to the QA page in the previous round appeared anywhere on page 02.
2. A fresh full-page screenshot — visually confirmed the same: 8 labeled component
   groups, a 154px gap, then the clean 3×2 archetype grid, no overlap.
3. `figma.root.children` confirmed there is exactly one page named "02 — Page
   Archetypes" (no duplicate/stale page with a similar name causing confusion), and
   the QA page (`55:2`) was confirmed to hold all 12 expected stress-test nodes.

**Conclusion**: page 02 was already clean, matching exactly what commit `a2e071fc`
(the previous round) produced. This looks like a stale render on the reviewer's side
rather than a live defect — no changes were needed or made to page 02's layout in
this round beyond the font-size fixes described below (which apply everywhere, not
specifically to page 02).

### 2. Author-name consistency — already 100% consistent; one gap filled

Searched every text node across all 5 pages for "Sobolewski" and "Соболевск". Result:
**every single occurrence** (8 total, across Cover, Title, AboutAuthor, and Copyright)
already uses the canonical spelling **"Siergej Sobolewski"** (Latin) / **"Сергей
Соболевски"** (Cyrillic) — matching `scripts/author_profile.py` and
`scripts/book_pipeline/locale_ru.py` exactly. No "Siergiej" (extra "i") variant exists
anywhere in the design content. (That spelling only appears in this Figma account's
own profile display name from `whoami` — unrelated to, and never copied into, any
page content.)

One real gap found: **Colophon had no author line at all.** Added one, matching the
same spelling and role text used everywhere else:

> Автор: Siergej Sobolewski — Software & AI Engineer, основатель Cartesian School

New node: `71:2` (Row), inserted above the existing "Издание:" row on `Book/Page/
Colophon` (`48:28`); all 8 existing rows shifted down to make room.

### 3. The real bug: a systemic pt→px conversion error in ad-hoc text

While verifying the Colophon readability requirement (point 4), a check of the
Colophon's actual `fontSize` property against its `textStyleId` revealed the text was
**not bound to any approved text style** — it was a raw `fontSize = 8` set directly in
the build script. Compared against the confirmed-correct `Book/Typography/Body` style
(bound, `fontSize = 14.11px` for its canonical 10pt), this exposed a systemic error:

**Root cause**: this design system's own convention (`figma-variables.yaml`) requires
every physical point size to be converted to Figma pixels via `pt × 1.4111` (since the
page canvas itself is scaled 4px/mm, and 1pt = 0.352778mm, so `1pt → 1.4111px` is the
necessary conversion for text to render at its true physical size on that scaled
canvas). Text bound to an approved `Book/Typography/*` style already had this
conversion applied correctly (via the `Typography — Figma (px)` variable collection).
But **every ad-hoc text node created directly with `.fontSize = N`** (intending "N
pt") was never converted — it rendered at literally `N` pixels, roughly **41% smaller
than intended** (e.g. intended 8pt rendered as if it were only ~5.7pt-equivalent).

This affected nearly every piece of ad-hoc text added across the front/back matter
system and two shared components — dozens of nodes across:

- **Components** (fixes apply to every instance automatically): `Callout` label text
  on all 6 variants (`10:4`, `10:9`, `10:14`, `10:19`, `37:113`, `37:118`, intended
  9.5pt), `BookTitle` title/subtitle on both variants (`40:111`, `40:114`), `Author
  Credit` (`40:118`), `ImprintBlock` (`40:121`), `TOCEntry`/`TOCChapterEntry`/
  `TOCSectionEntry` (`42:111`, `42:115`, `42:120`), `IndexEntry` (`42:124`),
  `ColophonBlock` (`42:128`), and the `Figure` placeholder label (`39:122`).
- **Pages** (fixed directly, since these were built with inline ad-hoc text rather
  than component instances): `Cover` (`43:3` — wordmark, kicker), `Title` (`45:6` —
  kicker, publisher line), `Copyright` (`45:124` — title/byline/ISBN/GitHub lines),
  `FromAuthor` (`45:140` — the FromAuthor↔Введение mapping note), `TOC` (`47:14`) and
  `TOCContinuation` (`47:98`) — all 24 chapter rows plus the 3 front-matter/index
  reference rows, `Index` (`48:2` — subhead + all 16 terms), `AboutCartesianSchool`
  (`48:22` — wordmark/website/GitHub), `Colophon` (`48:28` — note + all 8 rows),
  `EndPage` (`48:55` — wordmark/website).

Text already bound to an approved `Book/Typography/*` style (all body prose, all
headings, all captions) was **already correct** and untouched — only unbound ad-hoc
text needed fixing. Canvas metadata (RECTO/VERSO tags, archetype-name labels, band
labels, section titles like "COMPONENT LIBRARY —…") was deliberately **left
unconverted**, consistent with the round-4 decision that this class of label is
tooling/design-system metadata, not printed book content, and doesn't need physical
pt-accuracy. Two attempts accidentally caught RECTO/VERSO tags in a blanket sweep
(`50:19`, `50:20`, `50:21`, `50:23`) — caught immediately and reverted to `7.5px`,
matching the other tags.

### 4. Knock-on layout defects the size correction exposed — all fixed

Correcting font sizes (~41% larger everywhere) exposed several latent layout bugs
that had been masked by the previous, too-small text:

- **Dotted TOC/index leaders wrapped to 2 lines.** The leader text (160 repeated `.`
  characters, meant to always overflow and get naturally cut off by its `FILL` width)
  was short enough to fit on one line at the old undersized font, but wrapped at the
  corrected size, ballooning row heights. Fixed by shortening every leader to 30
  dots — comfortably fits on one line at the corrected size everywhere it's used
  (`TOCEntry`, `TOCChapterEntry`, `TOCSectionEntry` masters, and all inline rows on
  `TOC`/`TOCContinuation`).
- **Chapter-number column too narrow for some digit pairs.** The chapter-number
  prefix (`"20."`, `"22."`, `"23."`, `"24."`) was in a `FIXED` 18px-wide box — just
  wide enough at the old font, but chapters without a narrow "1" digit (20, 22, 23,
  24) now overflowed that box and wrapped their trailing "." onto its own line,
  visibly breaking those four rows on `TOCContinuation`. Fixed by widening the column
  to 26px across all 24 chapter rows on both `TOC` and `TOCContinuation`.
- **Copyright page's imprint block overlapped the ISBN/GitHub lines below it** once
  it grew from the font correction — the lines after it were still positioned at
  their old (too-close) offsets. Recomputed the whole vertical flow from actual
  measured heights.
- **Colophon rows with 2-line wrapped labels overlapped the row below them** for the
  same reason. Recomputed all 9 rows (8 original + the new Author row) from actual
  heights.
- **On the QA page itself**, the RU/PL/EN `BookTitle` stress instances grew
  substantially once the `BookTitle` master was corrected (proving the fix cascades
  to instances, which is correct behavior) and started overlapping the TOC/Index
  stress rows below them. Recomputed that page's internal layout too — this is
  QA-only content, not a canonical-page defect, but was fixed for cleanliness anyway.

Every one of these was caught by re-measuring actual post-fix heights via
`get_metadata` and/or a screenshot before moving on — none were assumed fixed without
verification.

### 5. Additional final-cleanup action

Moved the "Book Sequence Overview" frame (`51:14`) from page `03 — Front Matter` to
page `05 — QA & Stress Tests`. It was never overlapping anything and was explicitly
labeled "design-system QA reference only — not a publishing pipeline" — moving it
keeps that self-description consistent with where it actually lives, and reduces any
risk of it being mistaken for canonical front-matter content.

### Final live QA result (this round)

| Check | Result |
| --- | --- |
| Page 02 stress-content overlap | ✅ re-audited — not reproducible; already clean since commit `a2e071fc` |
| Author name consistency (Cover/Title/Copyright/AboutAuthor/Colophon) | ✅ 100% consistent "Siergej Sobolewski" / "Сергей Соболевски"; added the one missing occurrence (Colophon) |
| Copyright vertical composition | ✅ anchor heading retained from round 4; the font-size-correction overlap it introduced was found and fixed |
| Colophon minimum readable size | ✅ **root cause fixed at the source** — all Colophon text (and everything else affected) now renders at its true intended pt size, not just "raised to 8pt" as a patch |
| No duplicate components | ✅ verified via a name-count sweep on every page — zero duplicates |
| No stress-test remnants outside page 05 | ✅ verified via metadata + screenshot on pages 01-04 |
| No overlapping frames | ✅ verified on every page |
| No hidden obsolete copies / off-canvas nodes | ✅ swept every page for nodes with absolute x or y beyond 5000 — none found |
| All 16 canonical frames re-verified at this round's corrected sizes | ✅ Cover, Title, Copyright, AboutAuthor, FromAuthor, TOC, TOCContinuation, Standard, ChapterOpener, CodeHeavy, Table, DiagramCallout, Index, AboutCartesianSchool, Colophon, EndPage all re-screenshotted |

As in every prior round: this environment runs headlessly against the Figma Plugin
API and cannot drive the live Figma app directly. Given that this round's central
finding was specifically about text rendering at the *correct physical size* — the
one category of defect most sensitive to actual on-screen/print rendering — a live
100% zoom pass in the real Figma app is especially recommended before final sign-off
this time.

## Brand-aligned visual refinement (sixth round)

Product Owner direction: the system was visually correct but "too typographic" and
not yet connected to the Cartesian School website's identity. Directive was explicit
— extract/adapt the site's actual SVG-based visual language as reusable vector-native
Figma components, not screenshots. This section covers the site audit, the new
illustration library, and every page it touches.

### Site visual-language audit (source of truth, not invented)

Fetched the live homepage (`cartesianschool.org`) HTML + `homepage.css` directly (not
via a markdown-converting fetch, which strips styling) to extract real CSS values,
not approximations:

- **Hero structure**: a central "core" node (`.hero-core`, circular, dashed orbit
  ring) connected by orthogonal lines (`.hero-connector-lines`, right-angle paths
  with small circle "route nodes" at bends) to four technical panels: **Code**
  (a real Python snippet), **Graph** (`.hero-plot` — axis + bezier curve + tangent
  vector + two marked points, literally a small Cartesian plot), **App** (bar chart +
  control strip), **Game** (orthogonal trajectory + target rings + sprite + dashed
  collision box).
- **Background texture**: `.hero-system__grid` — a fine repeating grid
  (`rgba(143,183,254,.065)`, 36px spacing) radially masked to fade at the edges.
- **Real hex palette** (grep'd directly from the CSS, not eyeballed from a screenshot):
  deep backgrounds `#08011C` / `#0B0724` / `#15104A`; brand blue `#2767EC` / `#3866EF`
  / `#185DFA` / `#8FB7FE`; violet `#5B24F9` / `#8355FA` / `#C9A6FF`; a status-green
  `#1FAE63`.

This is the same restrained indigo/violet family already used for the interior print
palette, but noticeably more saturated and dark-background-oriented — confirming the
Product Owner's instinct that the interior palette alone reads as too muted/typographic
next to the site's actual brand presence.

### New color tokens (site-derived, additive — interior palette untouched)

Added as a **separate layer**, explicitly not replacing the restrained interior print
palette (which stays exactly as approved for body-page reading comfort):

- 12 new primitives in Color Primitives (`VariableID:82:2`-`82:13`): the real hex
  values above, each described in its own variable as "extracted from
  cartesianschool.org homepage hero."
- 8 new semantic roles in Color Semantic (`VariableID:82:15`-`82:22`):
  `color/illustration-bg-deep`, `-bg-core`, `-accent-blue`, `-accent-blue-soft`,
  `-accent-violet`, `-accent-violet-soft`, `-accent-violet-tint`, `-status-live`.
  Documented in `figma-variables.yaml` under a new `illustration_color_roles` list,
  separate from the interior `color_roles` list.

### New page: `06 — Illustration Library` (`82:14`)

### New components — `Book/Illustration/*` (8 items)

| Component | Node ID | Adapted from | Notes |
| --- | --- | --- | --- |
| `CartesianGrid` | `83:33` | `.hero-system__grid` | 360×240px fine grid + radial-gradient fade overlay simulating the site's edge mask. Background texture only — never behind body text. |
| `NodeConnector` | `83:62` | `.hero-route-nodes` / `.hero-connector-lines` | Atomic unit: circle node + line + arrowhead. The base pattern the larger network is built from. |
| `GraphPanel` | `85:2` | `.hero-plot` | Axis + bezier curve + tangent vector + 2 marked points — a genuine mini Cartesian plot, not decoration. |
| `CodePanel` | `85:10` | `.hero-module--code` | Real JetBrains Mono snippet in a bordered card — selectable text, not a screenshot. |
| `AppPanel` | `87:15` | `.hero-module--app` | Bar chart + control strip, matching the site's UI-panel motif. |
| `GamePanel` | `87:24` | `.hero-module--game` | Orthogonal trajectory + target rings + sprite + dashed collision box. |
| `HeroNetwork` | `88:2` | `.hero-system` (full) | The composed illustration: core node + 4 orthogonal connectors + instances of all 4 panels above. Primary use: Cover. |
| `ChapterMotif` | `91:139` (set) | — | Variant set (`Theme=Graph/Code/Game/App`), each a compact instance of the matching panel, sized for a chapter-opener corner accent. |

All panels use `clipsContent: true` (a real bug — see "Build defects" below) and the
new illustration color tokens exclusively; none use raster images.

### Cover redesign (`43:3`)

Removed the previous round's simple bordered plot-box motif (nodes `59:132`-`59:147`)
and replaced it with a `HeroNetwork` instance (scaled to 86%, `89:2`) as the primary
focal illustration — the core node reads "Py / 3.14" (an abstract mark, not a copy of
Python's trademarked logo). Kicker/title/author were repositioned to flow beneath it
with generous spacing. The cover now visually announces "Cartesian School" the moment
it's seen, rather than relying on typography alone.

### Chapter Opener enhancement (`15:9`)

Added a `ChapterMotif` instance (`92:103`, Theme=Code — matches this reference
chapter's algorithmic subject matter) at 72% scale in the top-right corner, plus a
thin horizontal rule extending from the left margin to meet it — a restrained
"engineering composition" touch. The chapter label/title/deck remain the clear
primary focus; the motif is a supporting accent, not a competing element. In real
production use, pick the `Theme` variant matching each chapter's actual subject
(Graph for math/turtle/data chapters, Code for fundamentals/algorithms, App for
GUI/Tkinter/Flask, Game for Turtle-games/Pygame) — documented on the component itself.

### Diagram connector misalignment — found and fixed (`12:4`)

Re-auditing `Book/Component/Diagram` (used on `DiagramCallout`) per the review's
explicit request to re-check connector centering found a real, confirmed bug: the
connector lines and arrowheads were fixed at `y=80`/`y=76`, left over from *before*
round 5's font-size fix changed the node boxes' height (56px → 34px, new vertical
center 69px). The connectors were never re-centered when the boxes changed —
an 11px vertical misalignment, visible on close inspection. Fixed by recomputing
both connectors' `y` from the actual node centers. This affects every page using this
component (currently `DiagramCallout`).

### Callout grid alignment — controlled equalization (`18:145`, `18:150`)

Per this round's explicit direction ("paired blocks should align to the top and
bottom boundaries of the taller item"), reversed the previous round's deliberate
choice to let paired callouts hug independently. Row 2 of the `DiagramCallout` 2×2
grid (Verification: 137px, PythonInsight: 154px) now shares a single controlled
height (154px, the taller card) via `layoutSizingVertical: FIXED` on both — text was
never shrunk, only the shorter card's box grew to match. Row 1 was already naturally
equal (137px/137px) and needed no change.

### QA page — Book Sequence Overview rebuilt for legibility (`93:19`, was `51:14`)

The diagram was confirmed too small on inspection: 110×64px boxes, cramped text, and
no visual connection between the two rows. Deleted and rebuilt: boxes now 150×92px,
label text 13pt (was smaller, unbound), consistent arrow connectors between every
step in both rows. A first attempt added a diagonal connector bridging the row wrap
(TOC → Chapter Opener) — this read as confusing rather than clarifying (an unconventional
long diagonal crossing the whole diagram) and was removed; a cleanup pass to remove
it initially deleted the wrong arrowhead (a legitimate one between "From Author" and
"TOC") by an overly broad position filter — caught immediately via a full arrowhead
count/position audit and corrected: the real stray diagonal arrowhead was removed and
the legitimate one restored.

### Build defects found and fixed during the illustration-library build

1. **`resize()` misuse on `LINE` nodes for verticals.** Both the Cover's earlier plot
   motif and the new `CartesianGrid` component initially tried to create vertical
   grid lines via `line.resize(0, height)` — Figma's `LINE` node type only has a true
   "width" (length) dimension; setting height doesn't reorient it. This produced
   invisible zero-length lines. Fixed by creating horizontal-length lines and setting
   `rotation = -90` instead — the correct, reliable technique for vertical lines in
   the Plugin API.
2. **Vector nodes distorted by a post-hoc `.resize()` call.** `GraphPanel`'s curve/
   axis/vector paths were built with absolute coordinates already matching their
   intended position, then a `.resize(160, 100)` call was mistakenly applied
   afterward — this rescaled the paths from their own tight bounding box (not the
   intended 160×100 frame), stretching the artwork far outside the panel's visible
   card. Fixed by removing the resize call entirely — a vector's own path coordinates
   should be authored directly at their final size, never resized after the fact.
3. **Missing `clipsContent` on new panel components.** None of the four technical
   panels had `clipsContent: true` set, so defect #2 above wasn't visually contained
   by the card border — content overflowed visibly past the rounded rectangle. Fixed
   on all four panels going forward (`makePanelShell` helper now sets it by default).
4. **SVG `H`/`V` path shorthand not supported.** Figma's `vectorPaths` parser rejects
   the SVG shorthand commands `H`/`V` (horizontal-line-to / vertical-line-to) with
   "Invalid command at H" — every orthogonal path in this round (trajectory, game
   panel) was written with explicit `L x y` commands instead.
5. **Illustration Library page layout collisions.** Components built across several
   separate `use_figma` calls were positioned without checking combined bounds
   against earlier calls — `GraphPanel`/`AppPanel` overlapped `CartesianGrid`, and
   `ChapterMotif` overlapped `HeroNetwork`. Caught via a full-page metadata dump
   before considering the library "done," and fixed with one clean re-layout pass
   (grid → panels row → full network → motif set, each in its own vertical band).

### QA result (this round)

| Check | Result |
| --- | --- |
| Cover visibly stronger, brand-aligned, vector-driven | ✅ `HeroNetwork` instance, no raster |
| Chapter Opener visibly improved, still readable | ✅ themed accent + rule, title remains primary focus |
| Illustration library reusable, named systematically, derived from the site | ✅ 8 components, all under `Book/Illustration/*`, each documented with its CSS source class |
| No screenshot-based lazy solution | ✅ every element built from Figma vector/shape primitives; nothing pasted from a site screenshot |
| Diagram connectors centered on node boxes | ✅ fixed the 11px misalignment found on `12:4` |
| Semantic callout grid alignment | ✅ row 2 controlled-equalized, no accidental mismatch |
| QA page sequence diagram legible | ✅ rebuilt larger, connectors verified complete (9/9 arrows present) |
| No canonical publishing pipeline changes | ✅ confirmed by diff — design-system files only |

As in every round: this environment runs headlessly against the Figma Plugin API and
cannot drive the live Figma app directly. One specific note from this round: a
suspected Cover kicker/title overlap was investigated via three independent methods
(isolated node screenshots of each element, and precise `get_metadata` coordinates)
and found to be a **misread of a compressed composite screenshot**, not a real
defect — both elements are correctly spaced (confirmed a clean gap in the underlying
data). Extra spacing was added anyway as a safety margin. A live-app check is
recommended to put this to rest visually, alongside the general recommendation to
confirm the new illustration palette's contrast/vibrancy in a real viewing
environment.

## Major professional refinement (seventh round)

Product Owner direction was explicit and critical: "the current result is not yet
good enough" — the cover was weak (an abstract "Py / 3.14" mark, not a real logo),
the illustration library was too small, and the visual system needed to cover every
real project on the Cartesian School site plus proper logo treatment throughout.

### Real Python logo — `Book/Illustration/PythonCore` (`103:52`)

Previous rounds used an abstract circular "Py / 3.14" badge as the Cover's center
node — explicitly called out this round as not acceptable. Fixed at the source
instead of cosmetically:

1. Fetched `https://www.cartesianschool.org/assets/img/brand/python-logo-mark.svg`
   directly via `curl` (not `WebFetch`, which strips path/gradient data) — the
   authentic two-snake Python mark the site itself uses, Inkscape-authored, with the
   official PSF brand gradients (blue `#5A9FD4→#306998`, yellow `#FFD43B→#FFE873`).
2. The raw path data used SVG `h`/`v` shorthand (same class of bug as round 6's
   "Invalid command at H") and mixed relative/absolute commands. Wrote a small
   standalone SVG-path normalizer (`svg_path_normalize.py`, kept in the session
   scratchpad, not committed — a normalization utility, not book content) to convert
   both paths to absolute `M`/`L`/`C`/`Z` commands Figma's `vectorPaths` accepts, and
   to compute the true combined bounding box (≈112.6 × 113.3 units — confirms the
   parse was correct; the official mark is close to square).
3. Built `PythonCore` as two vector nodes (`Snake/Blue`, `Snake/Yellow`) with linear
   gradients matching the exact brand hex values, origin-shifted so the artwork sits
   at a clean (0,0) origin. The eye holes render as true cutouts via `NONZERO`
   winding — no manual boolean subtraction needed, matching the original file.
4. Verified `node.rescale(scale)` (not `resize()`, which distorts vectors — see round
   6's post-mortem) scales a vector proportionally with no distortion, confirmed with
   a disposable 100×50 test rectangle before touching the real logo. All logo
   instances in this round are placed via `mainComponent.createInstance()` +
   `.rescale()`, never `.resize()`.

### Cover redesign (`43:3`) — real logo now the focal element

Rather than rebuild the Cover's composition from scratch (the `HeroNetwork` network
of 4 technical panels around a center node was already strong, brand-aligned, and
vector-native from round 6 — preserving what works per this round's explicit
instruction), the center node's content was replaced at the **master component**
level (`88:2`, `HeroNetwork`): removed the `Py`/`3.14` text layers (`88:13`, `88:14`),
inserted a `PythonCore` instance, sized to 68px (up from an initial 58px pass — the
larger size gives it clear focal presence within the existing 86px dark badge without
crowding the dashed outer ring), centered on the badge. Because the Cover's
`HeroNetwork` instance (`89:2`) is not overridden away from its master, this change
propagates automatically — the Cover now shows the real Python logo without touching
the Cover frame directly. Verified via screenshot: the real logo now reads
immediately at the composition's center, kicker/title spacing below remains clean
(re-confirms round 6's conclusion that the suspected kicker/title overlap was a
compressed-screenshot artifact, not a real defect — still clean this round).

### Illustration library — expanded from 8 to 27 components

New page-06 additions, all vector-native, all using the existing
`illustration_color_roles` tokens (no new variables were needed):

| Component | Node ID | What it is |
| --- | --- | --- |
| `PythonCore` | `103:52` | Real Python logo, see above. |
| `LogoSet/CartesianMark` | `107:54` | Flat vector **adaptation** of the site's 3D-rendered app icon (`assets/img/logo.png`, a glossy layered-lens squircle mark) — simplified to 3 stacked flat ellipses in the illustration palette. The original is a photoreal 3D render; per the vector-first rule, this is a deliberate flat reinterpretation, not a raster embed or a screenshot. |
| `LogoSet/CartesianWordmark` | `107:114` | Componentized version of the "Cartesian" + violet "School" text lockup already used ad hoc on Cover/Title/AboutCartesianSchool/EndPage — now a single reusable source of truth (Inter Bold 21.17pt, exact colors matched from the live Cover text). |
| `ProjectCard` (variant set, `Project=<key>`) | `110:312` | **All 13 real Cartesian School mini-projects** from `cartesianschool.org/index.html#proekty` (verified via direct `curl` — real titles, descriptions, and `data-project` keys, not invented): paint-app, snake, bouncing-ball, space-shooter, todo-app, calculator, story-generator, rock-paper-scissors, bouncing-balls-oop, temperature-converter, notes-app, tic-tac-toe, safesort. Each card: a category tag (real tech — Tkinter/Pygame/Flask/CLI/OOP), a small custom vector icon distilling the project's real subject (e.g. a thermometer for temperature-converter, a 3×3 grid with X/O for tic-tac-toe, a folder+checkmark for SafeSort), title, and a trimmed real description from the site copy. |
| `TechIcon` (variant set, `Topic=<name>`) | `112:89` | 8 flat topic glyphs — Function, Loop, Conditional, List, Dict, Class, Exception, Module — covering the core CS/Python concepts the book's chapters actually teach. Built for use in section headers and chapter-opener subject badges. |
| `DiagramAccent` (variant set, `Piece=<name>`) | `112:102` | 4 precision connector primitives — ArrowRight, ArrowDown, NodeDot, CornerConnector — arrowhead tips authored exactly centered on the shaft centerline, for constructing custom flow diagrams beyond `Book/Component/Diagram`. |

The 8 components from round 6 (`CartesianGrid`, `NodeConnector`, `GraphPanel`,
`CodePanel`, `AppPanel`, `GamePanel`, `HeroNetwork`, `ChapterMotif`) are unchanged
except `HeroNetwork`'s center node (see Cover section above).

**Logos, explicitly**: per the Product Owner's literal requirement ("there must be
all logos in the images"), the library's `LogoSet` group is the canonical, organized
home for both brand marks (Python + Cartesian School) — used deliberately in 4
places, not blanket-applied everywhere: the Cover (Python, already existed via
`HeroNetwork`), the Title page footer (small Python mark next to the brand line,
`114:83`), the About Cartesian School page (`CartesianMark`, giving a previously bare
page real brand identity, `115:5`), and the End Page closing moment (small Python
mark above the wordmark, a printer's-mark convention, `115:2`). No other logo assets
were identified as belonging to the course/book ecosystem, so no others were added.

### Chapter Opener (`15:9`) — subject-tied motif added

Added a small circular badge (`113:110`, `113:111`) showing the `TechIcon` matching
this reference chapter's real subject (`Topic=Dict`, since the reference chapter is
"Хеш-таблицы и коллизии" / hash tables — a dictionary-adjacent topic) to the left,
balancing the existing `ChapterMotif` (Code theme) accent on the right. This
demonstrates the intended per-chapter pattern for production use: pick the `TechIcon`
`Topic` matching each real chapter's subject (e.g. `List` for the lists chapter,
`Exception` for the exception-handling chapter). The page remains a book page, not a
poster — one small badge, no new full-bleed graphics, body copy untouched.

### Full diagram/callout re-audit — no new defects found

Re-screenshotted `Book/Component/Diagram` (`12:4`), the `DiagramCallout` page
(`18:115`, including its 2×2 callout grid), and the QA page's Book Sequence Overview
(`93:19`) at close zoom. All three remain correct: arrowheads centered on their
shafts, connector lines meeting box edges cleanly, the callout grid's row-2 controlled
equalization from round 6 still holds, and the sequence diagram still has exactly the
9 arrows it should (no stray diagonal, no missing arrowhead). Round 6's fixes held —
no regressions, nothing new to fix.

### Front/back-matter re-review — every page checked, most already correct

Screenshotted Title, Copyright, About Author, From Author, TOC, TOC Continuation,
Index, About Cartesian School, Colophon, End Page, and the 5 canonical body-page
archetypes (Standard, ChapterOpener, CodeHeavy, Table, DiagramCallout). Finding:
most of these are **correctly, deliberately plain** — real published books keep
copyright/colophon/index/TOC pages text-only, and adding illustration there would be
exactly the "nonsense illustration" the brief warned against. Two pages were
genuinely bare in a way that under-served their own purpose and were improved:

- **Title page** (`45:6`): added a small `PythonCore` mark beside the
  "Cartesian School · cartesianschool.org" footer line (`114:83`) — a restrained,
  conventional title-page brand touch.
- **About Cartesian School** (`48:22`): this page's entire purpose is introducing the
  brand, yet it previously had no brand mark at all beyond a small text wordmark —
  added a 56px `CartesianMark` instance (`115:5`) above the copy, repositioning the
  wordmark beside it. This was the single weakest page found in the re-review.
- **End Page** (`48:55`): added a small `PythonCore` mark above the closing wordmark
  (`115:2`) — a classic printer's-mark convention for a book's final leaf.

### Build defects found and fixed (seventh round)

1. **Default black stroke on new vector nodes.** `figma.createVector()` inherited a
   1px black stroke from the file's last-used style in three places this round (the
   Python logo's two snake paths, and the space-shooter `ProjectCard` ship icon) —
   invisible in the vector path data itself, only visible on screenshot. Fixed by
   explicitly setting `strokes = []` on every fill-mode vector going forward (added to
   the shared `vecN`/`vec` helpers used for all subsequent batches).
2. **`combineAsVariants` naming corruption via slash-style component names.** Naming
   the pre-combine components `Book/Illustration/TechIcon/Function` (full path, no
   `Property=Value` form) caused Figma to auto-derive garbled variant property names
   from the slash segments (`=Illustration, =TechIcon, =Function`) — a different root
   cause from round 3's "called combineAsVariants twice" bug, same symptom. Fixed by
   renaming all 12 affected children (`TechIcon`'s 8, `DiagramAccent`'s 4) to
   `Topic=<Name>` / `Piece=<Name>` after combining. `ProjectCard`'s 13 children were
   named `Project=<key>` *before* combining and were unaffected — this is now the
   documented correct pattern: **always name pre-combine components in
   `Property=Value` form**, never as a slash path.
3. **Stray extra function argument silently broken 5 of 8 `TechIcon` glyphs.** An
   early version of the icon-drawing helper was called with an extra positional
   `'strokeOnly'` string argument before the real options object on every
   stroke-only vector — the options object landed as a 5th (unused) argument, so
   `opts.strokeOnly` was `undefined` on a string, and the vectors rendered as solid
   fills instead of stroked outlines (visible as filled blobs instead of thin
   brackets/braces on Function, Loop's arrowhead, Conditional, List, Dict, Exception,
   Module). Caught by screenshotting the batch immediately rather than assuming the
   code ran correctly; fixed by deleting the broken batch and rebuilding with the
   correct 4-argument call signature.

### QA result (seventh round)

| Check | Result |
| --- | --- |
| Cover center uses the real Python logo, not an abstract mark | ✅ vector-native `PythonCore`, exact brand gradients, propagates from `HeroNetwork` master |
| Illustration library significantly expanded | ✅ 8 → 27 components (`PythonCore`, `LogoSet` ×2, `ProjectCard` ×13, `TechIcon` ×8, `DiagramAccent` ×4) |
| All 13 real site projects represented as reusable assets | ✅ real titles/descriptions/tech tags from `cartesianschool.org/index.html#proekty`, custom vector icon per project, none pasted as screenshots |
| Logos organized and used deliberately, not blanket-applied | ✅ `LogoSet` on page 06; Python mark on Cover/Title/EndPage; Cartesian mark on About Cartesian School — 4 deliberate placements, not every page |
| Chapter Opener shows a subject-tied motif | ✅ `TechIcon Topic=Dict` badge added, matching the reference chapter's real subject |
| Diagram/callout precision re-checked | ✅ no regressions found on `12:4`, `18:115`, or `93:19` |
| Weak pages reworked, strong pages preserved | ✅ Title/About Cartesian School/End Page improved; Copyright/AboutAuthor/TOC/Index/Colophon left as-is (correctly plain) |
| Vector-first, no raster/screenshot shortcuts | ✅ Python logo from normalized SVG source; Cartesian app icon flattened to native vectors, not embedded as the fetched `.png` |
| No canonical publishing-pipeline changes | ✅ confirmed by diff — design-system docs only |

As in every round: this environment runs headlessly against the Figma Plugin API and
cannot drive the live Figma app directly — all verification is via `get_screenshot`
and `get_metadata`. A live Figma app check remains the standard recommendation before
final Product Owner sign-off, particularly to confirm the new Python-logo gradient
rendering and the `ProjectCard` grid's print-scale legibility.

## Integrated cover/closing redesign (eighth round)

Product Owner direction was explicit: the previous round's Cartesian School "logo"
in the illustration library was a **hand-drawn flat vector approximation** of the
real app icon, not the real thing — an invented substitute, forbidden going forward.
Separately, the Cover's hero network read as "too separated," with panels far from
the center and large unstyled gaps above/below it, and the End Page was "a tiny logo
floating in a blank page."

### Real logo assets — replacing the invented approximation

Audited `cartesian_logo/` in the repo directly (15 files) before changing anything.
Found the folder mixes canonical brand assets with drafts/marketing collateral that
must NOT be used as a generic mark: `big_logo.png` is a promotional banner for an
unrelated "see your new site live before you pay" campaign; `jajo.png`,
`cartesian_logo_concept.png`, `cartesian_logo_ok.png` are drafts/duplicates. The
canonical set actually used:

| Asset | Repo source | How it was imported |
| --- | --- | --- |
| `Book/Illustration/LogoSet/CartesianIcon` (`139:239`) | `cartesian_logo/favicon.svg` | Uploaded via the Figma asset-upload API as `image/svg+xml` — Figma imports SVG as an **editable vector node tree** (358 real vector paths reproducing the exact gradient-band icon), not a raster embed. This is the real icon, self-contained with its own rounded-square tile, safe on both dark and light surfaces. |
| `Book/Illustration/LogoSet/CartesianLockup` (`139:244`, variant set `Format=Horizontal\|Stacked` × `Theme=Dark\|Light`) | `cartesian_logo/logo-full-dark.png`, `logo-full-light.png`, `logo_bar_dark.png`, `logo_bar_light.png` | Uploaded as raster image fills at their native resolution (2508×627 / 1448×1086), corrected from the upload API's default 400×300 `FILL` frame (which cropped/distorted them) to their true aspect ratio with `FIT` scale mode. |

Both fake components (`Book/Illustration/LogoSet/CartesianMark` — the flat 3-ellipse
approximation — and `Book/Illustration/LogoSet/CartesianWordmark`) were deleted
outright, **after** verifying zero remaining instances file-wide (`findAllWithCriteria`
across every page). Two real usages were swapped first: the Cover's corner mark
(`43:3`) and the About Cartesian School page's brand moment (`48:22`) now both use
real `CartesianIcon`/`CartesianLockup` instances instead of the fake mark.

### Cover (`43:3`) — integrated hero, not four floating boxes

Rebuilt `HeroNetwork` (`88:2`, the single shared master — verified it has exactly one
usage file-wide, so this is a safe direct edit, not a one-off Cover hack):

1. **Pulled all 4 panels ~40% closer to the center** (canvas shrunk 520×460 →
   480×380) and **enlarged the Python badge's ring/circle** proportionally.
2. **Replaced the 4 long orthogonal connector pipes with short straight beams** —
   each computed geometrically from the panel's inner corner to the exact point where
   it crosses the center ring's circle (`center + ring_radius × unit_vector`), so
   every beam meets the ring tangentially and precisely, with a small route-node dot
   at the meeting point. This reads as a "hub and spoke" cluster instead of a
   circuit-board wiring diagram, and is far denser than the original long-pipe layout.
3. **Added atmosphere**: a `CartesianGrid` instance (rescaled, 35% opacity) and a
   blurred violet glow ellipse (`LAYER_BLUR`, radius 50) behind the badge, with
   `clipsContent: true` + `cornerRadius: 18` on the master so the texture reads as a
   deliberate bounded "stage" rather than a texture with a visible stray edge.
4. **Enlarged the Cover's hero instance to near-full content width** (297×236 → the
   full native 480×380, i.e. ~1.6× larger) and **replaced the hand-placed icon +
   hand-typeset "CartesianSchool" text with a single real `CartesianLockup`
   (`Format=Horizontal, Theme=Dark`) instance** for pixel-perfect brand fidelity.
5. **Added a footer anchor** (thin rule + `cartesianschool.org` + a small "CARTESIAN
   SCHOOL BOOK SERIES" series tag, mirroring the Title page's footer language) so the
   page no longer trails into unstyled dead space at the bottom.

Because `HeroNetwork` is a shared master, all of these fixes also improve the
`06 — Illustration Library` documentation copy, not just the Cover.

### End Page (`48:55`) — a true closing spread, not a blank page with a mark

Previously: white background (`color/paper`), a 28px `PythonCore` mark and small text
floating alone with no supporting composition. Rebuilt from scratch:

1. **Background changed from white to the exact same fill the Cover uses**
   (`primitive/indigo/900`, `VariableID:3:103` — not the illustration palette's
   `bg-deep`, which is a different, darker shade; matched to the Cover's literal
   variable so the two pages are provably identical in tone, not just similar).
2. **Added the same atmospheric backdrop as the Cover**: a large `CartesianGrid`
   instance (30% opacity) and a large blurred violet glow (`LAYER_BLUR`, radius 90)
   centered on the page.
3. **Centerpiece**: the real `CartesianIcon` vector (enlarged to 110px) plus the
   verified-accurate "Cartesian" (white) + "School" (brand violet) wordmark set as
   real text beneath it. A raster `CartesianLockup` was tried here first and reverted
   — those lockup PNGs are flat opaque RGB rectangles (no alpha channel), so at
   large centerpiece scale they read as a pasted sticker against the atmospheric
   background; the transparent vector icon has no such seam and integrates cleanly.
   (The raster lockups remain the right choice for smaller badge-scale placements —
   used as-is on the Cover — where a self-contained tile reads as a normal logo
   badge.)
4. Added a thin violet rule and the real `cartesianschool.org · github.com/
   Cartesian-School` URLs beneath — factual, sourced from the same real links already
   used on the About Cartesian School page, no invented closing copy.

### Build defects found and fixed (eighth round)

1. **Upload API's default 400×300 frame distorted the raster lockups.** The asset
   upload endpoint places new raster images in a fixed-size frame at `FILL` scale
   mode when no target node is given — for images far from a 4:3 ratio (2508×627 is
   ~4:1) this crops/zooms into an unrecognizable sliver. Fixed by resizing each frame
   to the image's true aspect ratio and switching the fill's `scaleMode` to `FIT`.
2. **`combineAsVariants` auto-arrange overlap.** After combining the 4 `CartesianLockup`
   variants, the two `Format=Stacked` children (300px wide) were placed only 150px
   apart by Figma's auto-grid, overlapping — the same class of issue as round 7's
   `TechIcon` naming corruption, different symptom (position, not name, since these
   were correctly named `Format=X, Theme=Y` before combining). Fixed by explicitly
   repositioning the two Stacked children after combining, as with every other
   variant set in this file.
3. **Oversized master dwarfed the library page layout.** The `CartesianIcon`
   component was left at the SVG's native 1254×1254 after import — large enough to
   visually overlap the `CartesianLockup` set positioned nearby. Fixed with
   `node.rescale(140/1254)` (not `resize()`, which would distort the 358 vector
   paths) and repositioned both groups with a clean gap.

### QA result (eighth round)

| Check | Result |
| --- | --- |
| Cover no longer sparse; hero reads as one integrated illustration | ✅ panels pulled ~40% closer, short precise beams, shared glow/grid backdrop |
| Cover enlarged to use the page's content width | ✅ 297×236 → 480×380 (~1.6×) |
| Cover branding visible and real | ✅ real `CartesianLockup` instance, no invented mark |
| Real Python logo still correct and well anchored | ✅ unchanged `PythonCore` vector, now sitting in a denser, better-lit composition |
| End Page no longer a blank page with a tiny mark | ✅ full atmospheric composition, real icon + wordmark centerpiece |
| End Page tonally connected to the Cover | ✅ identical background variable (`primitive/indigo/900`), same grid + glow language |
| Real Cartesian School logo assets used from `cartesian_logo/` | ✅ `favicon.svg` (vector icon), `logo-full-dark/light.png`, `logo_bar_dark/light.png` (lockups) |
| No fake logo remains | ✅ `CartesianMark`/`CartesianWordmark` deleted after confirming zero instances file-wide |
| Illustration library materially stronger | ✅ `CartesianIcon` + 4-variant `CartesianLockup` replace 2 fake components; all 13 real `ProjectCard`s from round 7 untouched and verified intact |
| Live projects section reviewed | ✅ re-confirmed against `cartesianschool.org/index.html#proekty`; the round-7 `ProjectCard` set already covers all 13 real projects, so no rebuild was needed — verified, not assumed |
| No overflow, clipping, or broken instances | ✅ full-page composite screenshots of the library, Cover, and End Page checked for collisions after every structural change |
| No layout damage to other canonical frames | ✅ `HeroNetwork` has exactly one other usage (the Cover, fixed intentionally); `CartesianMark` had exactly two usages, both migrated before deletion |
| Canonical publishing pipeline untouched | ✅ confirmed by diff — design-system docs only |

As in every round: this environment runs headlessly against the Figma Plugin API and
cannot drive the live Figma app directly — verification is via `get_screenshot` and
`get_metadata`. A live Figma app check remains the standard recommendation, especially
to confirm the glow/blur effects render as intended at true print resolution.

## Final art direction, brand correction, QA-flow rebuild, authorial closing page (ninth round)

Four independent Product Owner findings this round, each with a distinct root cause.

### 1. About Cartesian School — wrong brand treatment (`48:22`)

The page's primary identity statement was a standalone 56×56 `CartesianIcon`
instance (`146:679`) — correct as an *asset* (real, vector, from round 8) but wrong
as a *treatment*: a lone app-icon-style mark reads as a settings/preferences screen,
not an imprint page. Removed the icon, the hand-drawn accent dash, and the
hand-typeset "CartesianSchool" text; replaced with a single real
`Book/Illustration/LogoSet/CartesianLockup` instance (`152:746`, `Format=Horizontal,
Theme=Light` — the light-background variant was already in the library from round
8, unused until now) at 240×60, the actual size a real book imprint page would use.
Body copy and links reflowed beneath it. Audited every other real-logo placement in
the file for the same class of error (Cover, Title, End Page) — all already use the
lockup or icon at an appropriately authoritative scale; About Cartesian School was
the only page with the "tiny icon as primary identity" problem.

### 2. Book Sequence Overview — real geometry bug, full rebuild (`93:19` → `153:19`)

Confirmed the reported defect by reading raw coordinates before touching anything:
cards sat at `y=72` with **inconsistent heights** (17 / 34 / 85px depending on label
length), while every connector line was fixed at `y=118` — for a 17px-tall card
(bottom edge at 89) the connector 29px below is nowhere near it; for an 85px-tall
card (bottom edge at 157) the same connector is 39px *above* the card's bottom,
crossing through it. Every arrowhead was therefore either floating in free space or
overlapping card text, exactly as reported, and the row-wrap from TOC (row 1, right
end) to CHAPTER (row 2, left end) had no connector at all, breaking the reading
flow.

Deleted the frame's contents entirely and rebuilt as one compact, strictly-orthogonal
diagram, three vertically-stacked phase bands connected by centered vertical
arrows (avoiding the row-wrap/diagonal-connector class of bug from round 6's
post-mortem entirely, rather than re-attempting it):

- **FRONT MATTER** — 6 uniform 140×48 boxes (Cover → Title → Copyright → About
  Author → From Author/Introduction → TOC), horizontal arrows between each.
- **BODY** — one macro-node (960×130, tinted fill, distinct from the plain boxes)
  containing an internal 3-step micro-sequence (Chapter Opener → Theory → Code /
  Table / Diagram) and a "× 24 CHAPTERS" badge — per the brief, this is preferable
  to 24 repeated boxes and cannot be misread as a second pipeline.
- **BACK MATTER** — 4 uniform 222×48 boxes (Index → About Cartesian School →
  Colophon → End Page), same treatment as Front Matter.

Heading is now plainly "FULL BOOK SEQUENCE"; the "design-system QA reference only —
not a publishing pipeline" line is a visually secondary 9pt gray subtitle directly
beneath it (previously baked into the oversized frame *name*, not shown as an
in-canvas subtitle).

**Numerical verification** (not just visual — read every line's actual
`x/y/rotation/width` and reconstructed true endpoints): every horizontal arrow's `y`
equals its row's box centerline exactly (front matter centerline `114` = `90 + 48/2`;
back matter centerline `376` = `352 + 48/2`; body-inner centerline `71` = `50 + 42/2`);
every arrow's start `x` equals the preceding box's right edge exactly, and its
arrowhead tip (`x2`) equals the following box's left edge exactly; both vertical
connectors run from one band's exact bottom edge to the next band's exact top edge
(`138→180` into the macro-node, `310→352` out of it) at the shared horizontal center
(`x=520`). No connector terminates in free space; no arrowhead is off-center.

### 3. End Page — from "logo + URL" to a real editorial closing page (`48:55`)

Round 8 fixed the "blank page" problem but left a page that was still just a mark
and two link lines — correct tonally, but not yet "a true closing page of a
professionally published technical book." Rebuilt around three real, sourced
content blocks stacked with a violet dash-rule ahead of each heading (echoing the
Cover's own kicker-rule motif):

1. **О книге** — a factual summary grounded in real TOC content already in this
   file/the repo: Turtle graphics, Tkinter apps, Pygame games, automation, and named
   real projects (Крестики-нолики, Змейка, the Pygame space-shooter, the SafeSort
   CLI utility) — no invented statistics, no claim not already backed by an existing
   chapter title or `ProjectCard`.
2. **Об авторе** — the real author portrait (see below) beside the name, the
   **exact existing `AuthorCredit` role string** already used on the Cover
   ("Software & AI Engineer, основатель Cartesian School" — reused verbatim, not
   retyped, for zero drift risk) and the real short bio already approved on the
   About Author page (`45:138`), trimmed of its redundant name/role lead-in only
   (the fact itself, not the wording, was already stated above it).
3. **Cartesian School** — the real dark horizontal lockup plus the real
   `cartesianschool.org` / `github.com/Cartesian-School` URLs (unchanged from round
   8, repositioned).

The round-8 atmosphere (grid + glow) was rebalanced rather than removed: reduced in
opacity so it supports the new text instead of competing with it, and the glow was
moved and enlarged toward the bottom of the page so the remaining negative space
below the content reads as a deliberate "closing light" (a real, common convention
for a book's final leaf) rather than accidental dead space — content was also
shifted down 90px as a whole to center its visual weight on the page instead of
crowding the top.

### 4. Real portraits added to the illustration library

Located both required photographs directly in the repo (not scraped from the web):

| Component | Node ID | Source | Provenance |
| --- | --- | --- | --- |
| `Book/Editorial/Portrait/Author` | `153:739` | `site/assets/img/author/siergej-sobolewski.jpg` | The canonical author photo — the same path is `PORTRAIT_JPG` in `scripts/author_profile.py`, the single source of truth the site's own homepage and front-matter author page both already use. 456×570px native. |
| `Book/Editorial/Portrait/GuidoVanRossum` | `153:740` | `site/assets/img/people/guido-van-rossum.jpg` | The same file already embedded in the book's real content, `scripts/build_chapter_01.py`, Chapter 1 § "Рождение Python: 1989–1991" — with an existing, real credit line: "Фото: Kushal Das, лицензия CC BY-SA 4.0 (изображение обрезано и сжато для сайта)." 480×640px native. |

Both were uploaded via the Figma asset-upload API and set as component fills at
their native aspect ratio (see build defect #1 below for how). Both component
`description` fields document source path, original dimensions, crop rule ("crop an
instance, never this master"), permitted use, and a recommended minimum print size
— per the brief's documentation requirement. Organized under a new page-06 heading,
**"EDITORIAL / PHOTOGRAPHIC ASSETS — real photographs, kept separate from
brand/technical/icon assets. Never converted to fake vector illustrations."**,
visually separated from the `LogoSet`/`ProjectCard`/`TechIcon`/`DiagramAccent`
groups above it.

**Recommended placement audit** (documented, not auto-applied — the brief is
explicit that this portrait must not be added indiscriminately): grepped the actual
chapter source for every Guido/Python-history mention. Chapter 1 already discusses
Python's origin at length (CWI, the ABC language, the 1989 Christmas-holiday start,
the Monty Python name origin, the 0.9.0/1.0/2.0/3.0 release history) and already
embeds this exact photo inline at § "Рождение Python: 1989–1991". No other chapter
touches Python history. **Recommendation: no book-page placement is needed** — the
canonical pipeline's Chapter 1 already uses this asset correctly; the library copy
exists so the *design system* has a documented, reusable reference for any future
editorial/marketing use (e.g. a back-cover blurb, a press kit), not to duplicate
content the book already has.

### Build defects found and fixed (ninth round)

1. **Raster upload produced an empty component (blank white render).** Following
   the round-8 pattern (`frame.children` → move each into a fresh `COMPONENT` →
   `frame.remove()`) for the two portrait uploads produced a component with
   `childCount: 0` and no fill — the upload endpoint's returned frame apparently
   held the image directly (or in a structure the move loop didn't traverse) rather
   than in a single child `RECTANGLE`, so nothing was actually moved before the
   source frame was deleted. Diagnosed by re-reading the created component's
   `children`/`fills` after the fact (both empty) rather than assuming success from
   a clean `use_figma` return. Fixed permanently, without depending on the
   upload response's internal structure at all: every `upload_assets` POST returns
   an `imageHash` in its JSON response — set that hash directly as
   `component.fills = [{ type: 'IMAGE', scaleMode: 'FIT', imageHash }]`. This is now
   the documented, reliable pattern for any future photographic asset import in
   this file.

### QA result (ninth round)

| Check | Result |
| --- | --- |
| About Cartesian School uses an authoritative lockup, not a lone icon | ✅ real `Format=Horizontal, Theme=Light` instance at 240×60 |
| No other page has the same "tiny icon as identity" issue | ✅ audited Cover/Title/End Page — all already correctly scaled |
| Book Sequence Overview connectors meet box edges/centerlines exactly | ✅ verified numerically from raw node coordinates, not just visually |
| Book Sequence Overview reads as one continuous flow, not two diagrams | ✅ 3 stacked bands, 2 centered vertical connectors, no row-wrap diagonal |
| Book Sequence Overview cannot be mistaken for a second pipeline | ✅ heading "FULL BOOK SEQUENCE" + explicit secondary subtitle; `×24` badge, not 24 boxes |
| End Page is a real editorial closing page, not logo + URL | ✅ real portrait + real book summary + real author bio + real brand identity |
| End Page content is 100% sourced, nothing invented | ✅ TOC-grounded book summary; `AuthorCredit`'s exact existing role string; the already-approved About Author bio, trimmed not rewritten |
| Real author portrait added, sourced correctly | ✅ `site/assets/img/author/siergej-sobolewski.jpg`, the same file `author_profile.py` already treats as canonical |
| Real Guido van Rossum portrait added, sourced correctly | ✅ `site/assets/img/people/guido-van-rossum.jpg`, the same file already used in `build_chapter_01.py` with its real CC BY-SA 4.0 credit preserved in the component description |
| Guido portrait not applied indiscriminately | ✅ audited chapter content; documented that Chapter 1 already uses it correctly and no other placement is recommended |
| Editorial assets kept visually/organizationally separate from brand/technical assets | ✅ new labeled section on page 06, positioned below the existing groups |
| Cover ↔ End Page read as a coherent pair | ✅ identical background variable, matching grid/glow language, matching typography — but distinct content (technical hero vs. human/editorial close) |
| No overflow, clipping, or off-canvas nodes | ✅ full-page composite screenshots of the library, Cover, End Page, About Cartesian School, and Book Sequence Overview checked after every structural change |
| Canonical publishing pipeline untouched | ✅ confirmed by diff — design-system docs only; no RU/PL/EN-specific logic added anywhere, no second publishing path introduced |

As in every round: this environment runs headlessly against the Figma Plugin API and
cannot drive the live Figma app directly — verification is via `get_screenshot`,
`get_metadata`, and (this round, for the connector geometry) direct numerical
reconstruction of line endpoints from raw node properties. A live Figma app check
remains the standard recommendation before final Product Owner sign-off.

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
