"""SafeSort: a safe, non-destructive command-line file organizer.

Scans a directory tree, classifies files by extension, and builds a plan
of moves into ``Sorted/<category>/`` — never touching disk until the user
explicitly runs ``apply``. Also detects duplicate-content files (read-only)
and can undo the most recent ``apply``.
"""

from __future__ import annotations

__version__ = "0.1.0"
