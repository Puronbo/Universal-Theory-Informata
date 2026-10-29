"""Search utility (meta-audit / exploration)."""

from __future__ import annotations

import re
from pathlib import Path


def search_text(
    root: str | Path,
    pattern: str,
    include: str = "*.md",
    regex: bool = False,
) -> list[tuple[str, int, str]]:
    """Search files under root for pattern.

    Returns list of (path, lineno, line).
    """
    root_path = Path(root)
    results: list[tuple[str, int, str]] = []

    for p in root_path.rglob(include):
        if not p.is_file():
            continue
        try:
            text = p.read_text(encoding="utf-8")
            for i, line in enumerate(text.splitlines(), 1):
                if (pattern in line) if not regex else re.search(pattern, line):
                    results.append((str(p), i, line.strip()))
        except (UnicodeDecodeError, OSError):
            continue
    return results
