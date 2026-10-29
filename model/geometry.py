"""Geometry: particles as stretched points (A3.6)."""

from __future__ import annotations


def stretched_distance(d0: float, scale_factor: float) -> float:
    """Apparent separation of two points under canvas stretching (A3.6)."""
    return d0 * scale_factor


def apparent_separation(points: list[float], scale_factor: float) -> list[tuple[int, int, float]]:
    """Pairwise distances among points scaled by the canvas stretch factor.

    Returns list of (i, j, distance) for all pairs i < j.
    """
    out: list[tuple[int, int, float]] = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d0 = abs(points[j] - points[i])
            out.append((i, j, d0 * scale_factor))
    return out
