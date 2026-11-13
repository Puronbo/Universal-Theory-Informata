"""Spontaneous symmetry breaking in a double-well potential (toy model).

The passage's "one is what a symmetric zero cannot hold" has a standard
mathematical form. For a real scalar order parameter ``phi``, take

    V(phi) = -mu_squared * phi**2 + quartic * phi**4,

with ``mu_squared > 0`` and ``quartic > 0``. Zero is a symmetric critical point
but a local maximum: its curvature is ``-2*mu_squared``. The stable minima are

    phi = +/- sqrt(mu_squared / (2 * quartic)),

and their magnitude is the toy analogue of a vacuum expectation value. The
mechanism is spontaneous symmetry breaking; the numerical Higgs value is a
measurement, not a prediction of this module.

This is a classical toy model, not a quantum field theory and not evidence for
the framework.
"""

from __future__ import annotations

import math


def _validate_parameters(mu_squared: float, quartic: float) -> None:
    if not math.isfinite(mu_squared) or mu_squared <= 0.0:
        raise ValueError("mu_squared must be finite and > 0")
    if not math.isfinite(quartic) or quartic <= 0.0:
        raise ValueError("quartic must be finite and > 0")


def _validate_field(phi: float) -> None:
    if not math.isfinite(phi):
        raise ValueError("phi must be finite")


def double_well_potential(phi: float, mu_squared: float = 1.0, quartic: float = 1.0) -> float:
    """Return ``-mu_squared*phi**2 + quartic*phi**4``.

    Raises:
        ValueError: If ``phi`` or the parameters are not finite, or either
            parameter is not positive.
    """
    _validate_field(phi)
    _validate_parameters(mu_squared, quartic)
    return -mu_squared * phi * phi + quartic * phi**4


def double_well_minima(
    mu_squared: float = 1.0,
    quartic: float = 1.0,
) -> tuple[float, float]:
    """Return the two stable minima ``-v`` and ``+v``.

    Raises:
        ValueError: If the parameters are not finite and positive.
    """
    _validate_parameters(mu_squared, quartic)
    vev = math.sqrt(mu_squared / (2.0 * quartic))
    return (-vev, vev)


def vev_magnitude(mu_squared: float = 1.0, quartic: float = 1.0) -> float:
    """Return ``sqrt(mu_squared / (2*quartic))``, the nonzero vacuum value.

    Raises:
        ValueError: If the parameters are not finite and positive.
    """
    _validate_parameters(mu_squared, quartic)
    return math.sqrt(mu_squared / (2.0 * quartic))


def double_well_curvature(
    phi: float,
    mu_squared: float = 1.0,
    quartic: float = 1.0,
) -> float:
    """Return ``V''(phi) = -2*mu_squared + 12*quartic*phi**2``.

    Raises:
        ValueError: If ``phi`` or the parameters are not finite, or either
            parameter is not positive.
    """
    _validate_field(phi)
    _validate_parameters(mu_squared, quartic)
    return -2.0 * mu_squared + 12.0 * quartic * phi * phi


def is_symmetric_zero_unstable(
    mu_squared: float = 1.0,
    quartic: float = 1.0,
) -> bool:
    """Return whether ``phi = 0`` is an unstable critical point.

    For this potential the answer is always true when the parameters are
    positive: ``V''(0) = -2*mu_squared < 0``.

    Raises:
        ValueError: If the parameters are not finite and positive.
    """
    _validate_parameters(mu_squared, quartic)
    return double_well_curvature(0.0, mu_squared, quartic) < 0.0


__all__ = [
    "double_well_curvature",
    "double_well_minima",
    "double_well_potential",
    "is_symmetric_zero_unstable",
    "vev_magnitude",
]
