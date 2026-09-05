# M02-I01/I02 verification record

Base: `ee8cfd58dbdefbbbc114380ae9ec44e75c29cf29` (fetched main, fast-forward-only update).
Branch: `feat/m02-i01-i02-pl-localization-foundation`.

## Frozen RU baseline

- M01: records=1158, inventory=1158, missing=0; all evidence file hashes unchanged.
- Site: 1160 HTML files; 493 practice entries; 13 projects.
- PDF: 4575 pages, 2294 recursive bookmark destinations.
  The existing publication validator reports 1221 top-level outline entries,
  which includes nested-list containers; both measurements are recorded explicitly.
- PDF SHA-256: `a5b7be5f3e2921e89d784505a6ad7090eb9d234d185d1a406ef3ddeeee786ef7`.
- EPUB SHA-256: `2ba8282bfcc4ca998104e25dd63eae5db231e3203888ca36e82624d407b55c72`.

## Local validation results

| Check | Result |
| --- | --- |
| `python -m pytest tests/ projects/python/safesort/tests/` | 319 passed |
| Localization architectural tests (included above) | 41 passed |
| `python scripts/validate_localization.py` | PASS; all 1160 RU routes preserved |
| `bash scripts/build_vercel.sh` (full mode) | PASS |
| Navigation validator | 1147 classified pages, no broken links/fragments |
| Catalog validator | 24 chapters, 493/493 practice, 13/13 projects |
| SEO validator | PASS, 1147 classified pages; 667 sitemap URLs |
| `npm run test:nav` | PASS; desktop/mobile, anchors/reload, Back to top |
| `npm run test:homepage` | PASS; desktop/tablet/mobile homepage/catalog contracts |
| `npm run test:redesign` | PASS; Projects/Reference and practice presentation |
| `npm run test:author` | PASS |
| `npm run test:pcb` | 47 passed |
| `npm test` | PASS; practice bridge execute/reset/assessment/concurrency |
| `npm run test:i18n` | PASS; synthetic exact-page keyboard switching, desktop/mobile, shared storage |
| `validate_ru_content_review.py --require-records --require-complete-scope` | PASS; 1158/1158 |
| `validate_book.py` | PASS; PDF and EPUB; EPUBCheck zero errors |
| Regeneration from all 24 chapter builders and shared page builders | No tracked RU generated diff |
| Repeated fixture generation | Identical bytes |
| `git diff --check` | PASS |

Browser regressions use the repository's portable build mode; the standalone
full deployment build and final regeneration use full validation. SafeSort was
installed editable with its dev extras, matching CI, after the initial local
pytest collection found it absent from the virtual environment.

## Scope and review boundary

No RU educational wording, existing HTML, redirects, PDF, EPUB, M01 records or
progress code changed. The only added delivery asset is optional switcher CSS;
production pages do not load it or expose PL controls yet. The larger manifest
addition is a baseline URL/hash inventory, not translated or generated HTML.

The bilingual home/practice fixture is generated into temporary test directories
and is excluded from deployment. Production PL seeds remain untranslated. The
foundation validates approval state, source freshness and artifact presence;
a full human-review evidence schema and target-content verification belong to the
next PL review layer. This milestone does not claim translation approval or
complete localization of existing educational templates.

Ready for Product Owner architecture review. Do not merge automatically.
