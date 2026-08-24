# SafeSort — upstream relationship

This directory (`projects/python/safesort/`) is an **educational snapshot**
of a real, standalone repository: [Cartesian-School/safesort](https://github.com/Cartesian-School/safesort).
It exists so a reader of Chapter 23 can browse SafeSort's source next to the
book's own repository, without cloning a second one. The canonical,
authoritative home of SafeSort is the standalone repository, not this
directory.

## Canonical reference point

- **Canonical repository:** https://github.com/Cartesian-School/safesort
- **Canonical tag:** `v0.1.0`
- **Canonical commit:** `70e480d5cdaa16e00e6cdb8613ac31c1dbf9c401`

`src/` and `tests/` in this snapshot are kept **byte-identical** to that
commit. `.upstream-sync.json` in this directory records a sha256 hash for
every file under `src/` and `tests/` as of that commit, and
`scripts/validate_safesort_upstream_sync.py` (run as part of
`scripts/build_vercel.sh`) fails the build if the snapshot drifts from those
hashes — whether from an accidental edit here, or from the real repository
moving on without this snapshot being updated to match.

## Allowed intentional differences

A handful of files are **not** part of the sync lock and are expected to
differ from the canonical repository:

| File | Why it differs |
|---|---|
| `README.md` | The canonical repository's README is written in Russian for its own audience on GitHub. This copy's README is written in English, matching the language used across the rest of `projects/` in this course repository. |
| `CHANGELOG.md`, `pyproject.toml`, `LICENSE` | Project metadata — package name/URLs may reference the canonical repository directly; kept here for completeness but not treated as code that must match byte-for-byte. |
| `.github/` (GitHub Actions workflow) | The canonical repository's CI workflow runs against its own repository; not meaningful to duplicate inside this course monorepo, which has its own CI. |

Only `src/` and `tests/` — the actual program and its automated tests — are
covered by the sync lock, because those are the files a reader might copy,
study, or diff against the real thing expecting them to match exactly.

## Sync procedure

When the canonical repository gets a new tagged release that should be
reflected here:

1. Fetch the new tag's tree from the canonical repository (e.g. via
   `gh api repos/Cartesian-School/safesort/tarball/<tag>` or a plain
   `git clone` + `git checkout <tag>`).
2. Diff its `src/` and `tests/` against this directory's `src/` and
   `tests/`. Copy over any real changes.
3. Regenerate `.upstream-sync.json`: recompute the sha256 of every file
   under `src/` and `tests/`, and update `canonical_tag` /
   `canonical_commit` / `synced_at`.
4. Run `python3 scripts/validate_safesort_upstream_sync.py` — it should
   pass cleanly against the newly regenerated lock.
5. Run the test suites (`pytest tests/test_chapter23_safesort.py` and
   `pytest projects/python/safesort/tests/`) to confirm the synced code
   still passes on this side.
6. Commit the updated snapshot together with the updated lock file in one
   change, so the two never land out of step.

This procedure is deliberately manual — a real sync is a decision (does
this course's narrative still match the new upstream code?), not something
that should happen silently in CI.
