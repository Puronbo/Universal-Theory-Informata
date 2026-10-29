"""MP-Operator: A_{alpha,beta} = alpha D + beta V (fold + unfold)."""
from __future__ import annotations
import math


def mp_discriminant(alpha: float, beta: float, lam: float) -> float:
    """Discriminant Delta = lam^2 - 4*alpha*beta."""
    return lam * lam - 4.0 * alpha * beta


def mp_regime(alpha: float, beta: float, lam: float) -> str:
    """Classify regime: overdamped / critical / underdamped."""
    d = mp_discriminant(alpha, beta, lam)
    if d > 0:
        return "overdamped"
    if d == 0:
        return "critical"
    return "underdamped"


def mp_roots(alpha: float, beta: float, lam: float):
    """Roots of alpha*r^2 - lam*r + beta = 0 (characteristic equation)."""
    d = mp_discriminant(alpha, beta, lam)
    if d >= 0:
        sq = math.sqrt(d)
        return ((lam + sq) / (2 * alpha), (lam - sq) / (2 * alpha))
    sq = math.sqrt(-d)
    return (complex(lam, sq) / (2 * alpha), complex(lam, -sq) / (2 * alpha))
