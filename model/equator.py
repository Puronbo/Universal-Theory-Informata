"""Equator of Scale (A9.1-A9.4)."""

from __future__ import annotations

from typing import Any


def scale_midpoint(micro: float = 1e-35, macro: float = 1e26) -> float:
    """Geometric midpoint scale between micro and macro limits."""
    result: float = (micro * macro) ** 0.5
    return result


def imaginary_rotate(coord: float) -> complex:
    """Rotate a real coordinate by 90 degrees into the imaginary plane (i*coord)."""
    return 1j * coord


def gauge_node(location: Any) -> dict[str, Any]:
    """A node: distinct by location, indistinguishable by identity."""
    return {"location": location, "identity": None}
