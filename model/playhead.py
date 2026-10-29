"""Playhead sampling (A4.1, A4.3, A4.4).

Reads a static 4D block frame-by-frame at Planck intervals.
No frame is skipped and no frame is repeated (A4.4).
"""

from __future__ import annotations

from typing import Any


class Playhead:
    """Reads a static 4D block frame-by-frame at Planck intervals."""

    def __init__(self, block: list[Any], tau: float = 1.0) -> None:
        self.block = list(block)
        self.tau = tau
        self._i = 0

    def reset(self) -> None:
        """Reset playhead to start."""
        self._i = 0

    @property
    def index(self) -> int:
        """Current frame index."""
        return self._i

    def read(self, t: float) -> Any | None:
        """Frame at time t: index = floor(t/tau), clamped to block bounds."""
        if t < 0:
            return None
        idx = int(t // self.tau)
        if idx >= len(self.block):
            idx = len(self.block) - 1
        return self.block[idx]

    def step(self) -> Any | None:
        """Advance exactly one Planck interval and return that frame."""
        if self._i >= len(self.block):
            return None
        frame = self.block[self._i]
        self._i += 1
        return frame

    def read_all(self) -> list[Any]:
        """Read every frame once, in order, then stop."""
        out = list(self.block)
        self._i = len(self.block)
        return out
