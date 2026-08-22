# Cartesian School icon system

Chapter content used decorative Unicode emoji (💡🚀⚠️🐞...) as visual markers in
headings, callout titles, exercise labels, chapter metadata and sidebar links.
They render inconsistently across platforms/fonts and don't belong to any
coherent visual identity. This repo now ships a small, original, locally-owned
SVG icon family instead — no external icon library, no emoji fonts, no remote
assets.

## Where it lives

- **Sprite:** `site/assets/icons/cartesian/icons.svg` — one file, one
  `<symbol id="icon-NAME">` per icon, `viewBox="0 0 24 24"`,
  `stroke="currentColor"`. Referenced everywhere via `<use>`, never inlined
  per call site, so it's fetched once and cached.
- **CSS:** `.cs-icon` / `.cs-icon--NAME` in `site/assets/css/theory.css`
  (cascades to practice pages, which load `theory.css` before
  `practice.css`; homepage-specific overrides live in `homepage.css`).
- **Python API:** `scripts/site_lib.py` — `icon_label(name, text)`,
  `cs_icon(name)`, `CS_ICON_NAMES`.
- **Validator:** `scripts/validate_no_decorative_emoji.py` — run it to catch
  a decorative emoji reintroduced into chapter source.

## Signal levels

A semantic icon exists to be noticed — an emoji worked as an attention
signal precisely because it was bold and colorful. The icon system has
three presentation levels so a symbol's visual weight matches how much
attention it's supposed to demand:

- **Level A — signal.** Important semantic blocks: `callout()`/`exercise()`
  titles, Debug Lab headings. Rendered via `cs_icon_emblem()`: a ~40px tile
  (34px under 480px) tinted with the icon's own semantic color, holding a
  ~26px (22px mobile) fully-opaque symbol. This is deliberately the
  strongest presentation in the system — the reader should recognize
  "warning" or "idea" before reading the title next to it. `callout()` and
  `exercise()` apply this automatically whenever their title starts with an
  `icon_label()` marker; nothing else to do at the call site.
- **Level B — support.** Secondary semantic markers: chapter-hero metadata
  badges (`.chapter-meta .cs-icon`, ~22px). Clearly visible, not shouting.
- **Level C — utility.** Minor inline glyphs: sidebar practice/source-file
  links, directory-tree illustrations, the homepage feature grid and
  reference board (`.cs-icon`'s plain `1.15em` default, ~16–20px in
  context). `cs_icon()`/`icon_label()` without going through `callout()`/
  `exercise()` always render at this level.

Reserve Level A for the categories it exists for — idea, warning, debug/
lab, error, success, experiment, project/launch, official source. Giving
every paragraph a Level A icon defeats the point: if everything shouts,
nothing is important.

## Using it in a chapter script

Never type a decorative emoji in chapter content. Use `icon_label()`
anywhere a plain title/label string is accepted — it just prefixes the text
with a `[[icon:name]]` marker that gets resolved into real `<svg>` markup
once, automatically, when the page is assembled:

```python
from site_lib import callout, icon_label

callout("tip", icon_label("idea", "Почему preview создаём один раз"), body_html)
```

This works anywhere a title/label string flows into `render_page()` or
`render_chapter_opener()` — `callout()`, `exercise()`, `NavItem(...)` sidebar
labels, `meta_items=[...]` chapter-hero badges, or a raw string like
`f"<h2>{icon_label('experiment', 'Что происходит глубже')}</h2>"`. You never
need to worry about HTML-escaping order: the marker is plain ASCII text, so
it survives `html.escape()` unchanged and is only ever turned into markup by
`_render_icon_markers()`, called once on the fully-assembled page HTML.

If you're writing raw HTML that never passes through `html.escape()` (an SVG
diagram, an inline `<div>`), you can call `cs_icon(name)` directly instead —
it returns the same `<svg class="cs-icon cs-icon--name">` markup with no
marker indirection.

Both functions raise `ValueError` for a name not in `CS_ICON_NAMES` — this is
deliberate; it catches a typo at build time instead of shipping a silently
broken icon reference.

## The icon set

Every icon below exists because real chapter content used the emoji it
replaces — audited across `scripts/build_chapter_*.py` and
`scripts/build_site_index.py` before any icon was drawn. None are
speculative or unused.

| Icon | Replaces | Used for | CSS color |
|---|---|---|---|
| `idea` | 💡 | Insight / "why this works" callouts | violet (brand) |
| `launch` | 🚀 | Project / "let's build" markers | violet (brand) |
| `warning` | ⚠️ ⛔ | Warning callouts, gotchas | amber |
| `success` | ✅ | Correct-answer / pass markers | green |
| `error` | ❌ | Incorrect-answer / fail markers | red |
| `debug` | 🐞 | Debug Lab headings | red |
| `experiment` | 🔬 🧪 | "Deeper theory" / experiment sections | brand blue |
| `timer` | ⏱ | Chapter metadata: estimated time | inherits text |
| `practice` | 📓, decorative 🐍 | Practice/exercise headings, practice sidebar links, "N практик" badges | inherits text |
| `code` | 💻 🖥 🔢 🧮 🔤 🔀, 🐍 (source-file links) | "Uses module X" badges, links to a project's `.py` source file | inherits text |
| `file` | 📄 | File references, single-document links | inherits text |
| `folder` | 📁 | Directory-structure illustrations | inherits text |
| `game` | 🎮 🕹 | Game-project badges | inherits text |
| `architecture` | 🧩 🧱 📦 | Component/architecture sections | inherits text |
| `palette` | 🎨 🖌, 🖼 | Visual/design topics, "real visual output" badges | inherits text |
| `tools` | 🔧 | Tooling notes | inherits text |
| `loop` | 🔁 | Loop/iteration notes | inherits text |
| `note` | 📚 📖 📇 🔶 🌐 🧭 | "Further reading" / reference callouts | inherits text |
| `compare` | ⚖️ | "Classic vs modern" framing (homepage) | inherits text |
| `profile` | 👤 | Author bio link (homepage) | inherits text |
| `search` | 🔍 | Reviewer / "look closer" link (homepage) | inherits text |
| `device` | 📱 | Mobile-format download link (homepage) | inherits text |

Five icons carry a fixed semantic color (violet/amber/green/red/blue) because
that color *is* the meaning — a warning is always amber regardless of where
it appears, matching the existing callout border colors. Everything else
inherits the surrounding text color, because these are wayfinding markers
sitting inline in metadata rows, sidebar links and headings of varying color
contexts, not standalone illustrations.

## What was deliberately left alone

Not every character in the original audit was a decorative emoji. These stay
as plain Unicode text, not icons, because they're either functional UI
state or already-restrained typography — turning them into icons would be
the "icon parade" this system explicitly avoids:

- **`→ ↓ ↑ ← ↔ ⇄` and `❯`** — prose arrow notation (`текст → интерпретатор
  → результат`) and breadcrumb separators. Structural typography, not
  emoji.
- **`★`** — difficulty-rating stars (`★★★ Обязательная практика`). An
  established repeated-glyph rating pattern, not a single decorative marker.
- **`✓ ✗`** — JS-driven practice-completion indicators
  (`localStorage`-backed, toggled by `practice.bundle.js` / `progress.js`).
  Functional state, not editorial decoration; touching these risks the
  progress-tracking UI.
- **`☐ ↺ ↻ ▷ ▼ ● ■`** — a checklist glyph, turtle-rotation notation, the
  literal VS Code "Run" button glyph being described, and turtle/game-board
  cell markers (Chapter 19's Snake board literally renders `●`/`■` as game
  state). Either literal UI references or in-game data.
- **`☰`** — the mobile navigation hamburger toggle button (`nav.js`). Global
  site chrome, not chapter content; out of scope for this pass to avoid
  touching the sidebar/drawer logic stabilized in an earlier round of work.

## What was left as legitimate instructional data

Per the "don't alter meaningful emoji data" rule: an emoji is only decorative
if it's a heading/callout/metadata marker. When the emoji is the literal
subject being taught — `print()` output, a terminal transcript, a
Unicode-length lesson — it stays untouched, because that's not decoration,
it's the lesson. Every such occurrence is enumerated explicitly in
`DATA_ALLOWLIST` inside `scripts/validate_no_decorative_emoji.py` (not a
heuristic — a hand-verified exact-substring list), for example:

- Chapter 3's simulated PySH terminal session and shell-prompt banner.
- Chapter 8's `len("код 🐍")` and `"Python — это 🐍 и 🎉"` Unicode-counting
  examples.
- Chapter 15's `"Питон🐍"` string-length example.
- Chapter 4/5/9's `print("🎉 Вы угадали!")`, `["🎁", "🎈", "🎉"]`, and the
  🍬-repeated `random.choices()` output — all literal program output shown
  to the reader.
- Chapter 12's `print("✅ Верно!")` / `print(f"❌ Неверно...")` quiz-script
  output (the *decorative* ✅/❌ used as standalone card titles elsewhere in
  the same chapter *were* migrated to the `success`/`error` icons — only the
  ones inside the printed program output were left alone).

## Adding a new icon

1. Confirm real usage first — grep `scripts/build_chapter_*.py` for the
   emoji you'd replace. Don't add a speculative icon nobody uses yet.
2. Add a `<symbol id="icon-NAME" viewBox="0 0 24 24">` to
   `site/assets/icons/cartesian/icons.svg`, matching the existing family:
   `stroke="currentColor"`, `stroke-width="1.75"`, `stroke-linecap="round"`,
   `stroke-linejoin="round"`, occasional small `fill="currentColor"` accent
   dots, no baked-in color.
3. Add the name to `CS_ICON_NAMES` in `scripts/site_lib.py`.
4. If the icon needs a fixed semantic color (not `currentColor` inherited),
   add a `.cs-icon--name { color: var(--token); }` rule next to the existing
   ones in `theory.css`, reusing an existing design token — never a new hex
   color.
5. Run `python3 scripts/validate_no_decorative_emoji.py` before and after —
   it should stay `PASS`.
