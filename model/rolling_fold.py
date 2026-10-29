"""Rolling-fold duality (A2.5): photon <-> dark energy."""

from __future__ import annotations


def roll_orientation(angle_deg: float) -> str:
    """Orientation of the canvas-fold at a given roll angle.

    0 deg (mod 180) -> 'photon' (crease, folded)
    90 deg (mod 180) -> 'dark_energy' (unfolded tension)
    """
    a = angle_deg % 180.0
    if a < 45.0 or a >= 135.0:
        return "photon"
    return "dark_energy"


def roll_convert(crease_density: float, total: float = 1.0) -> tuple[float, float]:
    """Convert a crease density into (photon_fraction, dark_energy_fraction).

    Conservation: photon + dark_energy = total.
    """
    p = max(0.0, min(total, crease_density))
    return (p, total - p)
