"""Hyperbolic (Poincare) geometry for the canvas (The Antiderivative of Universals)."""
from __future__ import annotations
import math


def _norm(v):
    return math.sqrt(sum(x * x for x in v))


def poincare_distance(u, v):
    """Conformal Poincare distance between u and v in the unit disk."""
    nu = _norm(u)
    nv = _norm(v)
    if nu >= 1.0 or nv >= 1.0:
        raise ValueError("points must be inside the unit disk (norm < 1)")
    diff = [u[i] - v[i] for i in range(len(u))]
    ndiff = _norm(diff)
    denom = (1 - nu * nu) * (1 - nv * nv)
    if denom <= 0:
        raise ValueError("degenerate denominator")
    arg = 1.0 + 2.0 * (ndiff * ndiff) / denom
    # arccosh
    return math.acosh(arg) if arg >= 1.0 else 0.0


def novelty_score(x):
    """Novelty = ||x||_2 in [0,1). Proximity to boundary = anomaly."""
    return _norm(x)


def c0_center():
    """The center C0: unified potentiality (void)."""
    return (0.0, 0.0)
