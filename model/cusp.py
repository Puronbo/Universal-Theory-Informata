"""Cusp catastrophe (candidate formalization, see FOLDING_CALIBRATION.md)."""

from __future__ import annotations

import math
from collections.abc import Iterable


def cusp_roots(a: float, b: float) -> list[complex]:
    """Roots of x^3 - a*x - b = 0 (equilibrium surface V'=0).

    Uses Cardano's formula; returns all three roots (real or complex).

    Args:
        a: Control parameter a.
        b: Control parameter b.

    Returns:
        List of three complex roots.
    """
    # Depressed cubic t^3 + p t + q = 0 with p=-a, q=-b
    p, q = -a, -b
    disc = (q / 2.0) ** 2 + (p / 3.0) ** 3

    if disc >= 0:
        # One real root
        # Handle negative cube roots properly
        u = _cbrt(-q / 2.0 + math.sqrt(disc))
        v = _cbrt(-q / 2.0 - math.sqrt(disc))
        r1 = u + v
        # Complex conjugate pair
        w = complex(-0.5, math.sqrt(3) / 2.0)
        r2 = w * u + (w**2) * v
        r3 = (w**2) * u + w * v
        return [r1, r2, r3]

    # Three real roots (casus irreducibilis)
    if p == 0:
        # Edge case: x^3 = b, roots are cbrt(b) * (1, w, w^2)
        rho = _cbrt(-q)
        r1 = rho
        w = complex(-0.5, math.sqrt(3) / 2.0)
        r2 = w * rho
        r3 = w**2 * rho
        return [r1, r2, r3]

    rho = 2.0 * math.sqrt(-p / 3.0)
    # Clamp acos argument to [-1, 1] for numerical stability
    arg = (3.0 * q) / (2.0 * p) * math.sqrt(-3.0 / p)
    arg = max(-1.0, min(1.0, arg))
    theta = math.acos(arg)
    r1 = rho * math.cos(theta / 3.0)
    r2 = rho * math.cos((theta + 2 * math.pi) / 3.0)
    r3 = rho * math.cos((theta + 4 * math.pi) / 3.0)
    return [r1, r2, r3]


def _cbrt(x: float) -> float:
    """Real cube root preserving sign."""
    if x >= 0:
        result: float = x ** (1.0 / 3.0)
        return result
    result = -((-x) ** (1.0 / 3.0))
    return result


def bifurcation_value(a: float, b: float) -> float:
    """8 a^3 - 27 b^2. Zero on the cusp curve."""
    return 8.0 * a**3 - 27.0 * b**2


def on_cusp(a: float, b: float, tol: float = 1e-9) -> bool:
    """Check if (a, b) lies on the cusp bifurcation curve."""
    return abs(bifurcation_value(a, b)) < tol


def crease_density_proxy(
    a: float,
    b: float,
    xs: Iterable[float],
    eps: float = 0.05,
) -> float:
    """Fraction of xs lying within eps of any real root of x^3 - a x - b = 0.

    Toy analog of crease density: how many sample points sit at the
    switching boundary. Only meaningful in controlled settings.
    """
    roots = cusp_roots(a, b)
    real_roots = [r.real for r in roots if abs(r.imag) < 1e-9]
    if not real_roots:
        real_roots = [r.real for r in roots]

    n = 0
    total = 0
    for x in xs:
        total += 1
        if any(abs(x - r) < eps for r in real_roots):
            n += 1
    return n / total if total else 0.0


def crease_density(values, eps=0.05):
    """Fraction of values within eps of zero (crease density proxy)."""
    if not values:
        return 0.0
    n = sum(1 for v in values if abs(v) < eps)
    return n / len(values)


def fold_spectrum(left_deriv, right_deriv, eps=1e-9):
    """Classify a point as smooth/kink/cusp/tear based on derivative behavior.

    Returns one of: 'smooth', 'kink', 'cusp', 'tear'.
    """
    if left_deriv is None or right_deriv is None:
        return "tear"
    if abs(left_deriv - right_deriv) < eps:
        return "smooth"
    # kink: finite jump in derivative
    if abs(left_deriv) < float("inf") and abs(right_deriv) < float("inf"):
        return "kink"
    return "cusp"
