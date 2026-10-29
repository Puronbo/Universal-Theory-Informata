"""Self-Looping Matrix: cosmological coupling & UV/IR inversion (A8)."""

from __future__ import annotations


def cosmological_coupling(M: float, scale_factor: float, kappa: float = 1.0) -> float:
    """Dark energy pumped by a collapsed node of mass M under expansion.

    Pressure ~ kappa * M * (scale_factor - 1): stretching locked pixels
    releases energy. (A8.4)
    """
    return kappa * M * (scale_factor - 1.0)


def uv_ir_inversion(scale: float) -> float:
    """Scale flip: past the pixel limit, scale -> 1/scale (T-duality). (A8.3)"""
    if scale <= 0:
        raise ValueError("scale must be > 0")
    return 1.0 / scale


def portal_journey(t: float, T: float = 1.0) -> dict[str, object]:
    """Candidate trajectory through the Great Attractor portal.

    t in [0,1]: 0=entry (compression), 0.5=inversion (imaginary plane), 1=exit (expansion).
    Returns a dict with phase and scale factor.
    """
    if t < 0.5:
        phase = "compression"
        scale = 1.0 - 2.0 * t  # shrinking toward 0
    elif t < 0.5 + 1e-12:
        phase = "inversion"
        scale = 0.0
    else:
        phase = "expansion"
        scale = 2.0 * (t - 0.5)  # growing from 0
    # at the inversion point use uv_ir_inversion on a tiny epsilon
    if abs(scale) < 1e-9:
        scale = float("inf")
    return {"phase": phase, "scale": scale, "t": t}
