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
    compiled = re.compile(pattern) if regex else None

    for path in root_path.rglob(include):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            if compiled.search(line) if compiled else pattern in line:
                results.append((str(path), line_no, line.strip()))
    return results
