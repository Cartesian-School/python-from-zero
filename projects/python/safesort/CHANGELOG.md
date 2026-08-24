# Changelog

All notable changes to SafeSort are documented in this file.

## [0.1.0]

### Added
- `scan` command: recursively lists files under a directory and reports
  counts per category (read-only).
- `plan` command: builds a non-destructive plan of file moves into
  `Sorted/<category>/`, without touching the filesystem.
- `apply` command: executes a plan's moves and writes a JSON manifest of
  what happened.
- `duplicates` command: detects groups of files with byte-for-byte
  identical content, using size grouping followed by chunked SHA-256
  hashing (read-only, reports only).
- `undo` command: reverses the most recent `apply` run using its manifest.
- Optional `safesort.toml` config file to override the destination
  directory, excluded directory names, and the extension-to-category
  mapping.

### Safety
- `scan`, `plan`, and `duplicates` never modify, move, or delete anything
  on disk — dry-run by default.
- Duplicate detection only ever reports groups; there is no delete code
  path in this version, not even a disabled one.
- Planned and applied moves never silently overwrite an existing file or
  another queued move; colliding destination names are automatically
  disambiguated with a `name (1).ext`, `name (2).ext`, ... pattern.
- `undo` refuses to overwrite a file that now occupies a move's original
  source path; it reports that conflict and still restores every other
  non-conflicting move in the same run.
- Symbolic links (files and directories) are never followed or moved.
- The configured destination directory (and SafeSort's own `.safesort`
  state directory) is always excluded from scanning, so re-running
  `scan`/`plan`/`apply` never re-processes already-sorted output.
