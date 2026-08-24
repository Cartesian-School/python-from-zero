"""Read-only duplicate-content detection.

Detection is staged so that expensive hashing is only ever done when it
can actually change the answer:

1. Group files by size. Files with a unique size cannot have a duplicate.
2. For every size group with 2+ files, hash each file's content with
   SHA-256, reading it in fixed-size chunks so a large file is never
   loaded into memory all at once.
3. Group by ``(size, digest)``. Any resulting group with 2+ files is a
   duplicate-content group.

This module only ever *reports* duplicate groups — it has no delete code
path at all, not even a disabled or future one.
"""

from __future__ import annotations

import hashlib
import logging
from collections import defaultdict
from pathlib import Path

from safesort.models import DuplicateGroup, FileInfo

logger = logging.getLogger(__name__)

#: Default chunk size used when incrementally hashing file contents.
DEFAULT_CHUNK_SIZE = 1024 * 1024


def sha256_file(path: Path, chunk_size: int = DEFAULT_CHUNK_SIZE) -> str:
    """Compute the SHA-256 hex digest of ``path``'s contents.

    Reads the file in ``chunk_size``-byte chunks rather than loading it
    into memory all at once, so this scales to files much larger than
    available RAM.
    """
    digest = hashlib.sha256()
    with path.open("rb") as file:
        while chunk := file.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def find_duplicates(
    files: list[FileInfo], chunk_size: int = DEFAULT_CHUNK_SIZE
) -> list[DuplicateGroup]:
    """Return groups of files whose content is byte-for-byte identical.

    Read-only: this only opens files for reading. Files that can no longer
    be read (removed or permission-denied between scanning and hashing)
    are logged and skipped rather than aborting the whole scan.
    """
    by_size: dict[int, list[FileInfo]] = defaultdict(list)
    for file in files:
        by_size[file.size].append(file)

    groups: list[DuplicateGroup] = []
    for size, candidates in by_size.items():
        if len(candidates) < 2:
            continue

        by_digest: dict[str, list[FileInfo]] = defaultdict(list)
        for candidate in candidates:
            try:
                digest = sha256_file(candidate.path, chunk_size)
            except (PermissionError, FileNotFoundError, OSError) as exc:
                logger.warning("Could not hash %s, skipping: %s", candidate.path, exc)
                continue
            by_digest[digest].append(candidate)

        for digest, matched in by_digest.items():
            if len(matched) >= 2:
                groups.append(DuplicateGroup(size=size, digest=digest, files=tuple(matched)))

    return groups
