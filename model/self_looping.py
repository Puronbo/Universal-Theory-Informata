"""Self-Looping Matrix: cosmological coupling & UV/IR inversion (A8)."""

from __future__ import annotations

import math


def cosmological_coupling(M: float, scale_factor: float, kappa: float = 1.0) -> float:
    """Dark energy pumped by a collapsed node of mass M under expansion.

    Pressure ~ kappa * M * (scale_factor - 1): stretching locked pixels
    releases energy. (A8.4)
    """
    return kappa * M * (scale_factor - 1.0)


def uv_ir_inversion(scale: float) -> float:
    """Scale flip: past the pixel limit, scale -> 1/scale (T-duality). (A8.3)"""
    if not math.isfinite(scale) or scale <= 0:
        raise ValueError("scale must be finite and > 0")
    return 1.0 / scale


def portal_journey(t: float, T: float = 1.0) -> dict[str, object]:
    """Candidate trajectory through the Great Attractor portal.

    Args:
        t: Time coordinate in ``[0, T]``.
        T: Total duration; must be finite and ``> 0``. Defaults to 1.

    The normalized coordinate ``u = t / T`` drives the phases: 0 = entry
    (compression), 0.5 = inversion (imaginary plane), 1 = exit (expansion).
    """
    if not math.isfinite(T) or T <= 0:
        raise ValueError("T must be finite and > 0")
    if not math.isfinite(t):
        raise ValueError("t must be finite")
    u = t / T
    if u < 0.0 or u > 1.0:
        raise ValueError("t must lie in [0, T]")

    if u < 0.5:
        phase = "compression"
        scale = 1.0 - 2.0 * u  # shrinking toward 0
    elif u < 0.5 + 1e-12:
        phase = "inversion"
        scale = 0.0
    else:
        phase = "expansion"
        scale = 2.0 * (u - 0.5)  # growing from 0
    # At the inversion point the scale is singular; represent it as +inf.
    if abs(scale) < 1e-9:
        scale = float("inf")
    return {"phase": phase, "scale": scale, "t": t}
