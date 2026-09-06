# M02-I01/I02: binding RU/PL localization architecture

## Delivery and baseline

Russian remains the default at the existing root URLs, including `/` and
`/index.html`. There is no `/ru/`, redirect, Accept-Language negotiation, or
browser-language redirect. Polish belongs exclusively under `/pl/`; the home
canonical is `/pl/index.html`, with `/pl/` served by the static index convention.
The frozen commit and full RU URL inventory, publication SHA-256 values, PDF page
and bookmark counts, and M01 file hashes are in `manifest/i18n/ru_baseline.json`.
This is the M02 source baseline, not a replacement for the historical M01 baseline.

M01 remains 1,158 records / 1,158 inventory / missing=0. Its evidence and semantics
are unchanged. PDF and EPUB are unchanged. There are no production PL pages or
visible switchers in this foundation. `build_localization_fixture.py` renders a
synthetic bilingual home and practice pair outside `site/` and `dist/` to exercise
actual shared rendering. Synthetic approval is never curriculum approval.

## Canonical sources and locale resources

Theory lives in `scripts/build_chapter_XX.py`; supplementary pages have dedicated
builders. Notebook sources live in `notebooks/`; project sources are identified
by `manifest/projects_manifest.json`. Homepage source is `build_site_index.py`.
Generated HTML is delivery output and must never become translation input.

`manifest/i18n/locales.json` defines the default, prefixes, language labels,
HTML lang and Open Graph locale. `ui_strings.json` owns shared navigation strings;
`pl_terminology.json` is the binding glossary and protected-term contract.
`Praktyka` is the main section; concrete tasks are `ćwiczenie/ćwiczenia/ćwiczeń`.
`localization.polish_count` accepts nonnegative integer counts and three noun forms;
1 is singular, terminal 2–4 except 12–14 use the few form, all others use many.
Fractional, negative and boolean values fail explicitly. New countable nouns must
supply reviewed forms. Internal categories such as Stopka are not interface labels.
All code identifiers are protected, beyond the glossary's minimum examples.

The registry and resources can later add EN without changing route lookup or
switch rendering. EN is not enabled. Existing RU educational renderers remain
RU-only until their remaining UI resources are extracted; setting a lang attribute
alone must never be treated as translation. The fixture gets lang from metadata.
Shared RU chapter templates now also obtain lang from the default metadata.

## Page identities, routes and publication

`manifest/i18n/routes.json` is version 1 of the route contract, described by `manifest/schemas/localization_routes.schema.json` and validated by
`localization.validate_routes`. The `pages` object is keyed by explicit, immutable
language-neutral IDs. Representative seeds cover home, author, license and practice
03-01. Seeds reserve PL paths but all production PL statuses are untranslated.
Do not infer identity by translating a slug or replacing a prefix. Future content
extraction assigns IDs at the source: `chapter-04-lesson-03`, `practice-03-01`,
`project-<existing-project-id>`. Each canonical unit must receive an ID before
translation; it can then populate this manifest deterministically in sorted order.
The seed manifest deliberately does not claim complete chapter localization scope.

Paths must be unique across variants, absolute site paths, ASCII and free from
traversal or duplicate separators. Existing RU paths are checked against the frozen
inventory. Polish prose slugs are reviewed Polish ASCII, e.g. `o-autorze`,
`licencja`, `rozdzial-01`; visible text retains diacritics. Numeric lesson IDs,
practice IDs and project IDs never change. Practice paths must be exactly
`<locale-prefix>/practice/<practice-id>/index.html`.

A page has a canonical `source` (locale, repository path, SHA-256). A target variant
has a path, state, `source_sha256`, localized `source_path`, and `evidence_path`.
The variant key is its target locale. Hash exact source artifact bytes, not rendered HTML. When canonical imported
content is involved, `source.dependencies` enumerates those inputs. `source_hash`
hashes the UTF-8 canonical JSON path-to-file-hash map (sorted keys, compact
separators); a single input retains its direct file hash. Home and author seeds
include their imported canonical content, so author-profile changes invalidate
translations too. New units must enumerate their content dependencies. Initially source bindings conservatively cover entire builders or
notebooks; changing any part invalidates dependent translations. Future extraction
can narrow this to independently stored content units, with a documented migration.
RU is never overwritten by PL. Translation producers must compare the actual source
hash with the manifest source hash before producing an artifact and record that hash
in the target binding. Update the source record on RU revision while retaining old
target hashes so stale translations remain detectable.

`validate_routes` requires `source.sha256 == source_hash(source, root)` for every
page, including all declared dependencies. A mismatch fails closed with
`Stale canonical source binding: <page-id>`. Changing canonical RU content requires
updating `source.sha256` to the current hash, but never automatically updates a
translation's separate `source_sha256`. That target binding changes only after
actual retranslation/review against the revised RU source; until then the target
remains stale. Neither validation nor status computation rewrites either hash.

The JSON Schema validates structure and SHA-256 syntax; it cannot inspect repository
files. `validate_routes` performs repository-semantic validation, including the
current canonical source hash and dependency freshness. These checks complement
the schema without adding filesystem semantics to it.

States: untranslated → translated → reviewed → approved; stale is explicit or
computed when the actual RU hash differs from the translation's source hash.
An approved variant requires existing localized source and evidence files and a
current source binding. Approval is a human review decision, not inferred from file
existence. Runtime publication additionally requires the generated page to exist.
Stale approved entries fail validation; they must return to review before publishing.
The deployment validator rejects unmapped or unapproved PL HTML. Future PL builders
must also gate output before writing files. Translation does not imply publication.

## Switcher and progress

`Routes.switcher(page_id, locale)` resolves exact counterparts. Shared
`site_header` and `mobile_nav_links` accept explicit page identity, locale and route
provider; omitting identity preserves current RU output byte for byte. The compact
RU | PL component uses no flags, active `aria-current`, normal keyboard-accessible
links, and noninteractive `aria-disabled` spans for missing translations. No home
fallback and no guessed links are allowed. The desktop wrapper is hidden at the
shared mobile breakpoint; the same control belongs inside the mobile panel.
`site/assets/css/localization.css` supplies contrast, selection and focus styles;
future localized templates must include it. The existing nav.js owns the mobile
menu. No client locale redirect or path rewriting is introduced.

`web/src/practice-app.js` stores `cartesian.python.progress.v1`, keyed by lesson ID,
with passed/score and other result fields. Shared inline theory cards read the same
map. Both languages remain on the same origin and use the same ID, so no storage
migration or locale namespace is needed. Local-required completion retains its
existing distinction from automatically verified results. Locale is presentation
metadata, never exercise-progress identity.

## SEO and machine-readable delivery

`build_seo_meta.py` uses the route provider to emit reciprocal ru/pl/x-default only
for existing approved pairs. x-default is the RU page. Both variants retain self
canonicals. Untranslated seeds produce no alternates. `site_structure.py` classifies
locale-prefixed routes using registry metadata. `build_sitemap.py` retains existing
RU output and adds XHTML alternate links when published pairs exist; the namespace
is emitted only when needed. Existing practice shells remain noindex and excluded
from sitemap. Future locale-specific validators must also cover translated content
and structured-data text before production PL launch.

`site/llms.txt` is a manually maintained English crawler overview of the Russian
course. `build_llms_full.py` combines it with chapter metadata and generated page
titles/URLs; it does not export full lesson text. Both root files keep their existing
bytes in this foundation and describe the default RU corpus, not an EN site locale.
Neither is a translation source. The shell rollout must also reconcile legacy
overview assertions (practice coverage, author role and license) with their current
canonical sources. Future PL artifacts will be `/pl/llms.txt` and
`/pl/llms-full.txt`, built only from approved PL canonical units, in stable page-ID
order, with PL URLs and source bindings. Never interleave RU fallback prose into PL
outputs. Extend this builder and its validators in the shell/content rollout before
publishing any PL machine-readable corpus. No mass translation occurs here.

## Review evidence and next delivery

Use `evidence/pl/<page-id>.json` for M02-PL review, separate from M01. Evidence must
bind source and target hashes and reviewer approval, covering fidelity, terminology,
Polish quality, exact preserved code, educational meaning, RU leakage, and links.
Existing evidence_path presence is a foundation gate; the next review layer must
validate this evidence schema and target hash before enabling real content.

Next: extract and review the website shell and localized canonical home/author/license
sources; populate exact routes, approve evidence, build approved pages, enable shared
switchers on both peers, then validate reciprocal SEO and sitemap. Translate no
chapters in this task. Production activation requires Product Owner review.

## Verification

Run `python scripts/validate_localization.py`, `pytest tests/test_localization.py`,
full pytest, `bash scripts/build_vercel.sh`, existing browser contracts, M01 complete
scope validator, and `validate_book.py`. Build the fixture with
`python scripts/build_localization_fixture.py /tmp/cartesian-i18n-fixture`.
Tests cover rendering, source staleness, publication gates, terminology, counts,
path collisions, stable practice identity, reciprocity, self canonical, lang,
missing translations and deterministic fixture regeneration. The frozen baseline
validator is intentionally a milestone guard: later approved content/publication
work must deliberately version it rather than silently updating M02 evidence.

## M02-I03 update: first production PL pages

The "no production PL pages or visible switchers" statement above described
this foundation milestone only and is now historical. M02-I03 published the
first three real, approved PL routes (`home`, `front-matter-author`,
`front-matter-license`) with real evidence (`manifest/schemas/pl_review.schema.json`,
`scripts/validate_pl_review.py`, replacing the file-existence-only gate this
foundation shipped), real RU-leakage/terminology validators
(`scripts/validate_pl_leakage.py`, `scripts/validate_pl_terminology.py`), and
a visible bidirectional RU|PL switcher on all three pairs. See
`docs/M02-I03-PL-SHELL-REVIEW.md` for the full linguistic/technical review and
`manifest/i18n/content/pl/` for the canonical PL sources. Chapter lesson
bodies and exercise bodies remain untranslated; `practice-03-01` is
unaffected. Production merge is still pending Product Owner review.

## M02-I04 update: complete Polish web corpus

M02-I04 replaces the temporary shell with a deterministic Polish build for all
1,160 stable page identities: 24 chapter openers, 624 lessons, 493 practice
units, 13 projects, the homepage, and the complete front-matter/reference
set.  `scripts/build_polish_course.py` consumes the immutable route identities
and the canonical translation memory in
`manifest/i18n/content/pl/course_translation_memory.json`; generated
`site/pl/**/*.html` and localized notebooks remain build outputs rather than
manually maintained translation sources.

The route manifest now carries every RU/PL pair and its current source hash.
The states `translated` and `reviewed` are publishable for this completion
milestone, while `approved` still requires schema-valid human review evidence.
This separation permits a complete, usable course without falsely claiming the
page-by-page linguistic, technical, visual, and pedagogical certification that
belongs to M02-I05.  Stale source hashes remain a hard publication failure.

`scripts/inject_language_switchers.py` installs exact manifest-derived desktop
and mobile counterparts on every pair.  `scripts/build_llms_pl.py`, the SEO
builder, and the sitemap builder cover the complete PL corpus.  The completion
validator enforces cardinality and identity equality, meaningful page content,
zero visible-prose Cyrillic, zero temporary localization copy, localized
notebook availability, exact PL-to-RU routing, and absence of ordinary RU
fallback links.  The canonical Vercel build runs all of these generation and
validation stages automatically.
