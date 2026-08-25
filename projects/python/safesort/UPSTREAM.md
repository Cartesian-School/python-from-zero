# SafeSort upstream relationship

This directory is an educational snapshot of the standalone
[Cartesian-School/safesort](https://github.com/Cartesian-School/safesort)
repository. The standalone repository is SafeSort's canonical home; this copy
lets Chapter 23 readers inspect and run the project without a second clone.

## Verified base and course corrections

- **Canonical tag:** `v0.1.0`
- **Canonical commit:** `fe610cf09392bee999ab8daac814779df7306eeb`
- **Last comparison:** 2026-08-25

The snapshot was compared with that exact tag and commit. Most files under
`src/` and `tests/` remain byte-identical. A small, explicit correction layer
differs from upstream because Chapter 23 now teaches contracts that the tagged
sample did not implement:

- category-specific TOML values overlay built-in extension defaults;
- `safesort.toml` remains configuration input and is never sorted;
- one digest bucket is partitioned into exact byte-content groups;
- bounded reads have a directly testable stream interaction contract;
- the configured console log format displays the logger name;
- executor documentation distinguishes forward `apply` from reverse `undo` mutation.

`.upstream-sync.json` records the upstream hash and reason for every changed
file under `course_corrections`. Its `locked_files` table pins the complete
course snapshot after those corrections. This is intentionally not described
as byte-identical to upstream.

`scripts/validate_safesort_upstream_sync.py` checks the declared relationship
without network access. A passing result proves only that the local course
snapshot matches its lock. It cannot prove that GitHub still points at the same
commit or that a newer upstream release does not exist.

## Files outside the lock

| File | Why it differs |
|---|---|
| `README.md` | The course copy uses English to match other `projects/` documentation. |
| `CHANGELOG.md`, `pyproject.toml`, `LICENSE` | Included as project metadata, but not treated as synchronized source or test code. |
| `.github/` | The standalone repository and course monorepo use different CI workflows. |

Only Python files under `src/` and `tests/` are locked. The
`course_corrections` table makes their provenance reviewable file by file.

## Manual update procedure

When a new tagged upstream release should enter the course:

1. Fetch the tag from the canonical repository and verify its commit ID.
2. Diff upstream `src/` and `tests/` against this directory.
3. Reapply or retire each documented course correction deliberately.
4. Recompute every `locked_files` hash. For each remaining correction, record
   the upstream hash and a specific reason.
5. Update `canonical_tag`, `canonical_commit`, and `synced_at`.
6. Run `python3 scripts/validate_safesort_upstream_sync.py`.
7. Run `pytest tests/test_chapter23_safesort.py` and the SafeSort test suite.
8. Commit the snapshot and lock together.

The process stays manual because synchronizing code is a curriculum decision,
not an operation CI should perform silently.
