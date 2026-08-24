# SafeSort

SafeSort is a local command-line tool that organizes a messy directory
(like `~/Downloads`) by moving files into category subfolders — `Sorted/documents/`,
`Sorted/images/`, `Sorted/archives/`, and so on — based on their extension.
It also finds files with duplicate content so you can review them yourself.
Nothing is ever moved or deleted until you explicitly ask it to, and every
`apply` run can be undone.

SafeSort has no third-party runtime dependencies — it's built entirely on
the Python standard library (`pathlib`, `argparse`, `hashlib`, `shutil`,
`json`, `tomllib`).

## Features

- **scan** — recursively lists files under a directory and reports how
  many fall into each category.
- **plan** — computes exactly which files would move where, without
  touching the filesystem.
- **apply** — performs the moves from a plan and writes a manifest so the
  run can be undone later.
- **duplicates** — finds groups of files whose content is byte-for-byte
  identical (by size, then SHA-256), and reports them — it never deletes
  anything.
- **undo** — reverses the most recent `apply` run, refusing to overwrite
  anything that has since appeared at a file's original location.
- Optional `safesort.toml` config file to customize the destination
  folder name, excluded directories, and the extension-to-category
  mapping — never required for normal use.

## Safety

SafeSort is built around one rule: **you decide when files move.**

- `scan`, `plan`, and `duplicates` are strictly read-only. They never
  create, move, or delete anything on disk, no matter how many times you
  run them.
- `apply` is the only command that moves files, and it does so because
  you explicitly ran it — there's no separate confirmation prompt to
  half-trust.
- Duplicate detection only ever *reports* what it finds. There is no
  delete feature in SafeSort, not even a hidden or "coming soon" one.
- A move never overwrites an existing file. If two files would land on
  the same destination name, SafeSort automatically renames the second
  one to `name (1).ext`, `name (2).ext`, and so on.
- `undo` never overwrites either: if something now exists at a file's
  original location, that one restoration is refused and reported, while
  every other move in the same undo run still goes through.
- Symbolic links (to files or directories) are always skipped — never
  followed, never moved.
- SafeSort never re-processes its own output. The destination folder
  (`Sorted/` by default) and its own `.safesort/` bookkeeping folder are
  always excluded from scanning, so running SafeSort again after sorting
  won't try to re-sort what it already sorted.

## Installation

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e projects/python/safesort/
```

For running the test suite too:

```bash
pip install -e "projects/python/safesort/[dev]"
```

This installs the `safesort` command. You can also run it as a module
without installing the console script, via `python -m safesort`.

## Usage

```
safesort scan <root>          List files under <root> by category.
safesort plan <root>          Show the moves that would happen (no changes made).
safesort apply <root>         Perform the moves and write an undo manifest.
safesort duplicates <root>    Report groups of files with identical content.
safesort undo [root]          Undo the most recent apply under [root] (default: current directory).
```

Run `safesort --help` or `safesort <command> --help` for details on any
subcommand.

### Configuration

Drop an optional `safesort.toml` in the directory you're organizing to
override the defaults:

```toml
destination = "Sorted"
exclude = [".git", ".venv"]

[extensions]
documents = [".pdf", ".docx", ".txt"]
images = [".jpg", ".jpeg", ".png", ".webp"]
```

No config file is required — SafeSort works out of the box with sensible
built-in categories (documents, images, video, audio, archives, code,
data, and an `other` fallback).

## Examples

```
$ safesort scan ~/Downloads
Files scanned: 48
Documents: 12
Images: 18
Archives: 5
Other: 13

$ safesort plan ~/Downloads
12 move operations planned.
No files have been changed.

$ safesort apply ~/Downloads
Applied 12 moves.
Manifest written to:
/home/you/Downloads/.safesort/history/20260824T153000123456.json

$ safesort duplicates ~/Downloads
Found 1 duplicate group(s):
Group 1: 2 files, 204800 bytes each, sha256=9f86d0818...
  /home/you/Downloads/report.pdf
  /home/you/Downloads/report (copy).pdf

$ safesort undo ~/Downloads
Restored 12 moves.
```

## Development

SafeSort lives at `projects/python/safesort/` inside this repository and
is a standalone, installable package — it doesn't depend on anything else
in the repo, and nothing else in the repo depends on it.

```bash
cd projects/python/safesort
pip install -e ".[dev]"
```

Project layout:

```
src/safesort/
  cli.py          argparse subcommands, exit codes, user-facing output
  models.py       frozen dataclasses shared across modules
  scanner.py      read-only directory walk
  classifier.py   extension -> category mapping
  planner.py      pure move-plan construction (no filesystem writes)
  executor.py     the only module allowed to move files
  duplicates.py   size + chunked-SHA256 duplicate detection
  manifest.py     JSON manifest read/write and undo
  config.py       defaults + optional safesort.toml overlay
```

## Tests

```bash
pip install -e ".[dev]"
pytest tests/
```

Every test runs against pytest's `tmp_path` fixture — a real temporary
directory created fresh per test — so the suite never touches your actual
files.

## License

MIT — see [LICENSE](LICENSE).
