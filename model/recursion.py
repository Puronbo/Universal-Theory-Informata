"""Recursion / awakening (A5.1, A1.5 purge) and erosion (A7.4)."""

from __future__ import annotations

import math
from collections.abc import Callable


def iterate(
    f: Callable[[float], float],
    x0: float,
    n: int = 10000,
    tol: float = 1e-12,
    detect_cycle: bool = False,
) -> tuple[float, int, bool, int]:
    """Iterate x_{k+1}=f(x_k) until fixed point, cycle, or max steps.

    Args:
        f: Function to iterate.
        x0: Initial value.
        n: Maximum iterations.
        tol: Convergence tolerance.
        detect_cycle: Whether to detect cycles.

    Returns:
        Tuple of (final_value, steps_taken, converged, cycle_length).
        cycle_length=0 if no cycle detected.
    """
    x = x0
    seen: dict[float, int] = {}
    for i in range(1, n + 1):
        xn = f(x)
        if not math.isfinite(xn):
            return x, i, False, 0
        if detect_cycle and x in seen:
            return x, i, False, i - seen[x]
        seen[x] = i
        if abs(xn - x) < tol:
            return xn, i, True, 0
        x = xn
    return x, n, False, 0


# Purge threshold constants
PURGE_EPS: float = 1e-9


def purge_if_flat(ys: list[float], eps: float = PURGE_EPS) -> bool:
    """Automated purge (A1.5): True if the last change is ~0 (y'=0).

    Heuristic: compares only the last two samples; not a full derivative.
    """
    if len(ys) < 2:
        return False
    return abs(ys[-1] - ys[-2]) < eps


def purge_derivative(ys: list[float], eps: float = PURGE_EPS) -> bool:
    """Purge if the mean absolute successive difference is below eps."""
    if len(ys) < 2:
        return False
    diffs = [abs(ys[i] - ys[i - 1]) for i in range(1, len(ys))]
    return (sum(diffs) / len(diffs)) < eps


def canvas_energy(scale_factor: float) -> float:
    """Energy density of the canvas at a given scale (E ~ 1/scale)."""
    if scale_factor <= 0:
        raise ValueError("scale_factor must be > 0")
    return 1.0 / scale_factor


# Erosion (A7.4)


def erosion_step(states: list[int], pairs: int = 1) -> list[int]:
    """Erode `pairs` of (+1,-1) into (0,0), preserving net-zero.

    Returns a new list. If fewer than `pairs` opposing pairs exist, erodes
    as many as possible.
    """
    out = list(states)
    pos = [i for i, v in enumerate(out) if v == 1]
    neg = [i for i, v in enumerate(out) if v == -1]
    k = min(pairs, len(pos), len(neg))
    for a, b in zip(pos[:k], neg[:k], strict=False):
        out[a] = 0
        out[b] = 0
    return out
