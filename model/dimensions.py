"""Circle of dimensions (A12)."""
from __future__ import annotations
import math


def dimension_circle(n: int):
    """Angles of n dimensions arranged on a closed circle."""
    if n < 1:
        raise ValueError("n must be >= 1")
    return [2.0 * math.pi * k / n for k in range(n)]


def dimension_bleed(phase_a: float, phase_b: float, threshold: float = 0.1) -> bool:
    """True if two dimension-phases are close enough to bleed through."""
    diff = abs((phase_a - phase_b + math.pi) % (2 * math.pi) - math.pi)
    return diff < threshold
