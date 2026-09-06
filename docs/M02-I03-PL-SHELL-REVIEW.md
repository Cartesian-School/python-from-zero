# M02-I03 — Polish website shell: linguistic and technical review

This is the human-readable companion to the machine-checked evidence in
`evidence/pl/*.json` (validated by `scripts/validate_pl_review.py`). It
explains *why* each check passed, not just that it did. All three pages
were reviewed as **mechanical QA + linguistic audit by the implementing
agent**, per the M02-I03 human-approval-boundary contract — **Product
Owner sign-off on Polish phrasing, legal translation, and visual design is
still required before merge.**

## Scope reminder

Catalog/shell metadata only: homepage shell, 24 chapter titles (catalog
metadata), 13 project cards (catalog metadata), Kompendium card copy, and
two front-matter pages (author, license), translated faithfully. **Chapter
lesson bodies, the 493 exercise bodies, and full project tutorial bodies
are explicitly out of scope** and are not touched.

## Page 1: `home` → `/pl/index.html`

| | |
|---|---|
| Source | `scripts/build_site_index.py` (+ `author_profile.py`, `data/chapters.json`, `data/book-pagination.json`, `manifest/practice_manifest.json`, `manifest/projects_manifest.json`, `manifest/projects_presentation.json`) |
| Target | `manifest/i18n/content/pl/home.json` |
| Terminology | `manifest/i18n/pl_terminology.json` |

**Fidelity.** Hero, "O kursie", the four-stage format section, Rozdziały,
Praktyka, Projekty and Kompendium all have direct RU counterparts;
numeric metrics (24 chapters, 493 exercises, 13 projects, page count,
browser/local counts) are read from the same manifests as RU, never
invented. The elaborate embedded author-bio panel (portrait, affiliations,
metadata strip — RU `id="avtor"`) is **intentionally omitted**: it isn't
reachable from top navigation, isn't one of the required PL shell
sections, and skipping it avoids a second, lower-fidelity translation of
content the dedicated `front-matter-author` page already covers
faithfully. This is a deliberate scope decision, not an oversight.

**Terminology.** Praktyka (not Ćwiczenia) is the main-nav/section label;
Rozdział/Rozdziały for chapters; Kompendium (not Referencje) for the
reference section. Exercise counts use `localization.polish_count()`
against `pl_terminology.json`'s `practice_rule.exercise_forms` — e.g. 493
→ "493 ćwiczenia praktyczne" (few form, not naively "ćwiczeń"). Verified
by `scripts/validate_pl_terminology.py` (structural heading check + a
genuine negative test that a wrong label is actually caught).

**RU leakage.** Zero — verified by `scripts/validate_pl_leakage.py`
(visible text + `aria-label`/`title`/`alt`/`placeholder`). Two real
leakage sources were found and fixed *before* this passed: (1) several
manifest project "topics" are plain Russian words (e.g. "Игры",
"Файлы") rather than protected technical terms — now translated via
`home.json`'s `topic_translations`; (2) three shared decorative SVG
illustration generators (`practice_illustration()`,
`reference_illustration()`, `_notes_app_scene()` inside
`project_illustration()`) had Russian labels baked directly into
site-wide functions — they now take an optional `locale` param (RU
branch verified byte-identical).

**Link integrity.** Roadmap (24), practice groups (24) and project cards
(13) render as non-interactive spans/divs (`aria-disabled="true"
title="Tłumaczenie niedostępne"`, reusing the exact convention already
shipped in `Routes.switcher()`'s unavailable branch) — no `href`, so
`validate_navigation.py`'s `<a>`/`<link>`-only regex correctly never
flags them, and no misleading cross-language navigation is possible.
Kompendium: `O autorze` and `Licencja` are real links to the two other
approved PL pages; PDF and EPUB stay real links (they are real files)
with descriptions explicitly reading "wersja rosyjska"; the remaining
five cards (indeks, wprowadzenie, recenzent, CLI, official resources)
render disabled since their target pages aren't translated.

**SEO.** `<html lang="pl">`, self canonical
`https://www.cartesianschool.org/pl/index.html`, reciprocal
`hreflang="ru"`/`"pl"`/`"x-default"` (x-default → RU), `og:locale=pl_PL`,
distinct PL `<title>`/description. RU's `/index.html` now carries the
reciprocal `hreflang="pl"` alternate. Verified by
`tests/test_pl_shell.py::test_pl_homepage_seo` and
`test_ru_homepage_has_reciprocal_pl_alternate`.

**Accessibility.** Disabled cards use `aria-disabled="true"` +
descriptive `title`, keeping them out of the tab-focus flow the way a
real interactive control would be; the language switcher (already
shipped) uses `aria-current`/`aria-disabled` correctly for both
directions. No new ARIA landmarks were needed beyond what `site_header`/
`mobile_nav_links` already provide.

**Responsive.** Reuses the exact same CSS classes as the RU homepage
(`.jn-card`, `.project-card`, `.reference-card`, etc.) — swapping
`<a>`→`<span>`/`<div>` doesn't change layout since those selectors are
class-based, not tag-qualified. Manually reviewed at 1440×900 and
390×844 (screenshots delivered separately); Polish strings run longer
than Russian in a few places (notably Kompendium card titles and the
roadmap note) but none overflowed or clipped at either breakpoint.

**Reviewer decision: approved** (mechanical QA + linguistic audit).
Pending: Product Owner sign-off on natural Polish phrasing.

## Page 2: `front-matter-author` → `/pl/front-matter/o-autorze.html`

| | |
|---|---|
| Source | `scripts/build_front_matter.py` (untouched — see below) |
| Target | `manifest/i18n/content/pl/front-matter-author.json` |

**Fidelity.** Faithful translation of the currently approved RU page:
hero (name/role/specializations/portrait unchanged — `author_profile.py`
is a single untouched source of truth for both locales), core paragraphs,
professional path, engineering domains (Polish counterpart of
`Domain.title_ru`/`desc_ru`, index-parallel and length-matched to
`author_profile.DOMAINS`), projects and systems (6 protected proper
nouns: GuardBSD, AstraDesk, AeroNerve, PySH, ECLI, Cartesian School
Agency AI — unchanged), educator, and Cartesian School sections. No new
claims introduced; every fact traces to the same source as RU.

**RU leakage.** Zero, including the portrait `alt` text, which was
previously RU-only (`author_profile.PORTRAIT_ALT`) and is now translated
in `front-matter-author.json`.

**Link integrity.** Sidebar shows only the translated item (O autorze,
active); the two untranslated front-matter pages (technical reviewer,
introduction) are **omitted rather than linked**, per the no-misleading-
navigation contract — no fake PL route, no RU fallback link.

**SEO.** Own `Person`/`worksFor` JSON-LD (Glaeron LLC, Cartesian School)
now renders correctly — `build_seo_meta.py`'s author-page detection was
previously keyed to the single RU path only; extended to a set covering
both locales, verified byte-unaffected for RU.

**M01 note.** `scripts/build_front_matter.py` is **not edited** — it
backs three M01-tracked supplementary units, and M02's frozen baseline
locks every M01 evidence file's exact bytes. The visible RU|PL switcher
on the RU counterpart (`ob-avtore.html`) is added by a dedicated
post-processing script, `scripts/inject_ru_author_switcher.py`, which
never touches the builder — verified idempotent
(`strip(inject(fresh)) == fresh`) and confirmed the M01 evidence/
inventory files are byte-identical to `main` (`git status` shows nothing
under `evidence/m01/` or `manifest/ru_content_audit_inventory.json`).

**Reviewer decision: approved** (mechanical QA + linguistic audit).
Pending: Product Owner sign-off.

## Page 3: `front-matter-license` → `/pl/front-matter/licencja.html`

| | |
|---|---|
| Source | `scripts/build_license_page.py` (not M01-tracked — see its own docstring) |
| Target | `manifest/i18n/content/pl/front-matter-license.json` |

**Fidelity.** Full faithful translation: rightsholder line, CC BY-NC-SA
4.0 explanation (what it covers, what Attribution/NonCommercial/
ShareAlike mean), the code-license section (MIT, explicitly not covered
by CC BY-NC-SA 4.0 even when code appears inside CC-licensed prose),
`rel="license"` explanation, third-party materials, trademark, and an
attribution example. **Legal substance is unchanged**: CC BY-NC-SA 4.0
for educational/editorial content, MIT for all code including inline
snippets. No Harvard/CS50 wording introduced. `CC_DEED_URL`/
`CC_LEGALCODE_URL`/`REPO_URL`/`SAFESORT_REPO_URL` are imported from
`build_license_page.py`, not duplicated, so the two locales' legal links
can never drift apart.

**RU leakage.** Zero. The rightsholder line uses `ap.NAME` ("Siergej
Sobolewski") only, dropping the RU Cyrillic parenthetical the RU page
uses — a deliberate simplification since `ap.NAME` already reads as a
normal Latin name.

**Link integrity.** Sidebar shows only Licencja (active); the reference
index page (not translated) is omitted, not linked.

**SEO.** Same reciprocal-hreflang mechanism as the other two pages;
`rel="license"` head link applies site-wide via the existing SEO
injection and is unaffected by locale.

**Reviewer decision: approved** (mechanical QA + linguistic audit).
Pending: Product Owner sign-off on the legal translation specifically.

## Deferred by design (documented per task §40)

`/pl/llms.txt` / `/pl/llms-full.txt` are **not created** in this
milestone. The existing shared `site/llms-full.txt` already lists the
two new PL front-matter pages (via `site_structure.iter_pages()`'s
existing locale-generic classification — no code change needed), which
is accurate metadata, not translated lesson corpus, so it does not need
deferring. A dedicated PL machine-readable corpus is deferred because
the approved PL content (3 pages) does not yet support a *meaningful*
standalone crawler overview distinct from what the shared file already
provides; building one now would either duplicate the shared file or
imply a broader PL corpus than exists.

## Governance counts (PL, reported separately from M01)

| Status | Count | Page IDs |
|---|---|---|
| approved | 3 | home, front-matter-author, front-matter-license |
| untranslated | 1 | practice-03-01 |
| translated / reviewed | 0 | — |
| stale | 0 | — |
| missing evidence | 0 | — |

M01 (RU) is unaffected: `validate_ru_content_review.py
--require-records --require-complete-scope` reports
`records=1158; inventory_units=1158` (unchanged from `main`).
