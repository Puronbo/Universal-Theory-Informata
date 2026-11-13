"""The spacebar's parameter: what a real argument can and cannot be.

The becoming-one passage ends with "there was never a finger on the
spacebar." If the press is an operator, its argument is not free: it is a
phase, a count of ticks, a gauge label, or an eigenvalue fixed by a
constraint. This module enumerates the candidates and implements the
checkable ones.

The press is

    U(theta) = exp(-i theta).

- A real theta is unitary: ``|U| = 1``. It is the physical clock.
- An imaginary theta gives a real exponential (a Boltzmann weight after the
  standard Wick rotation), not a unit-modulus phase.
- A complex theta does both.

Mass sets the clock: ``theta = m*c**2*tau/hbar``, and one full press is the
Compton period ``T_C = 2*pi*hbar/(m*c**2)``. The dimensionless count
``n = tau/T_C`` is the scale-free real coordinate of the phase; a
dimensionful ``tau`` needs a mass to become a phase, and that mass is the
"finger" if it is chosen freely.

This is formal bookkeeping, not a derivation of a physical theory.
"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass

SPEED_OF_LIGHT: float = 299_792_458.0  # m / s
REDUCED_PLANCK: float = 1.054_571_817e-34  # J s
BARYON_TO_PHOTON_RATIO: float = 6.1e-10  # measured; the passage's "one part in a billion"


def _finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _positive(value: float, name: str) -> float:
    value = _finite(value, name)
    if value <= 0.0:
        raise ValueError(f"{name} must be > 0")
    return value


def _nonnegative(value: float, name: str) -> float:
    value = _finite(value, name)
    if value < 0.0:
        raise ValueError(f"{name} must be >= 0")
    return value


def compton_period(mass: float) -> float:
    """Return ``2*pi*hbar / (m*c**2)``, the rest-frame clock period.

    A massless particle has no rest frame and therefore no Compton period.

    Raises:
        ValueError: If ``mass`` is not finite or not positive.
    """
    mass = _positive(mass, "mass")
    return 2.0 * math.pi * REDUCED_PLANCK / (mass * SPEED_OF_LIGHT**2)


def compton_frequency(mass: float) -> float:
    """Return ``m*c**2/hbar``, the angular frequency of the rest clock.

    Raises:
        ValueError: If ``mass`` is not finite or not positive.
    """
    mass = _positive(mass, "mass")
    return mass * SPEED_OF_LIGHT**2 / REDUCED_PLANCK


def action_from_proper_time(tau: float, mass: float) -> float:
    """Return ``-m*c**2*tau``, the free worldline action.

    Raises:
        ValueError: If ``tau`` is not finite or ``mass`` is not finite and
            positive.
    """
    tau = _finite(tau, "tau")
    mass = _positive(mass, "mass")
    return -mass * SPEED_OF_LIGHT**2 * tau


def phase_from_action(action: float) -> float:
    """Return ``-action/hbar``, the phase of ``exp(-i*S/hbar)``.

    Raises:
        ValueError: If ``action`` is not finite.
    """
    action = _finite(action, "action")
    return -action / REDUCED_PLANCK


def phase_from_proper_time(tau: float, mass: float) -> float:
    """Return ``m*c**2*tau/hbar``, the phase advanced by proper time.

    Raises:
        ValueError: If ``tau`` is not finite or ``mass`` is not finite and
            positive.
    """
    return phase_from_action(action_from_proper_time(tau, mass))


def ticks_from_proper_time(tau: float, mass: float) -> float:
    """Return ``tau / compton_period(mass)``, the count of Compton ticks.

    Raises:
        ValueError: If ``tau`` is not finite or ``mass`` is not finite and
            positive.
    """
    return phase_from_proper_time(tau, mass) / (2.0 * math.pi)


def wrap_ticks(ticks: float) -> float:
    """Return ``ticks`` modulo one, in ``[0, 1)``.

    Raises:
        ValueError: If ``ticks`` is not finite.
    """
    ticks = _finite(ticks, "ticks")
    return ticks % 1.0


def spacebar_from_ticks(ticks: float) -> complex:
    """Return ``exp(-2*pi*i*ticks)``, the press for a tick count.

    The result always has unit modulus for real ``ticks``.

    Raises:
        ValueError: If ``ticks`` is not finite.
    """
    ticks = _finite(ticks, "ticks")
    return cmath.exp(-2j * math.pi * ticks)


def spacebar_from_proper_time(tau: float, mass: float) -> complex:
    """Return ``exp(-i*m*c**2*tau/hbar)``, the press for proper time.

    Raises:
        ValueError: If ``tau`` is not finite or ``mass`` is not finite and
            positive.
    """
    return spacebar_from_ticks(ticks_from_proper_time(tau, mass))


def thermal_weight(energy: float, beta: float) -> float:
    """Return ``exp(-beta*energy)``, the imaginary-time (thermal) press.

    This is the Wick-rotated companion of the unitary press: it is real and
    not of unit modulus, so it cannot be a clock phase.

    Raises:
        ValueError: If ``energy`` is not finite, ``beta`` is not finite, or
            ``beta`` is negative.
    """
    energy = _finite(energy, "energy")
    beta = _nonnegative(beta, "beta")
    return math.exp(-beta * energy)


def mass_shell_residual(energy: float, momentum: float, mass: float) -> float:
    """Return ``E**2 - p**2*c**2 - m**2*c**4``.

    Raises:
        ValueError: If ``energy`` or ``momentum`` is not finite, or ``mass``
            is not finite and positive.
    """
    energy = _finite(energy, "energy")
    momentum = _finite(momentum, "momentum")
    mass = _positive(mass, "mass")
    return energy**2 - (momentum * SPEED_OF_LIGHT) ** 2 - (mass * SPEED_OF_LIGHT**2) ** 2


def is_on_mass_shell(
    energy: float,
    momentum: float,
    mass: float,
    tolerance: float = 1e-9,
) -> bool:
    """Return whether the mass-shell residual is small relative to the scales.

    Raises:
        ValueError: If an argument is invalid or ``tolerance`` is negative.
    """
    energy = _finite(energy, "energy")
    momentum = _finite(momentum, "momentum")
    mass = _positive(mass, "mass")
    tolerance = _nonnegative(tolerance, "tolerance")
    residual = mass_shell_residual(energy, momentum, mass)
    scale = max(
        energy**2,
        (momentum * SPEED_OF_LIGHT) ** 2,
        (mass * SPEED_OF_LIGHT**2) ** 2,
    )
    return abs(residual) <= tolerance * scale


@dataclass(frozen=True)
class ParameterCandidate:
    """One candidate reading of the spacebar's argument."""

    name: str
    domain: str
    status: str
    note: str


def candidate_parameters() -> tuple[ParameterCandidate, ...]:
    """Return every candidate reading of the spacebar's real argument.

    The status is one of ``physical``, ``fundamental``, ``gauge``, ``fixed``,
    ``measured``, ``thermal``, ``non-unitary``, or ``rejected``.
    """
    return (
        ParameterCandidate(
            "proper_time",
            "real, dimensionful",
            "physical",
            "a lift of the phase; needs a mass/clock to fix the phase",
        ),
        ParameterCandidate(
            "phase",
            "circle (mod 2*pi)",
            "fundamental",
            "theta = S/hbar; real theta is unitary",
        ),
        ParameterCandidate(
            "ticks",
            "real (mod 1)",
            "fundamental",
            "n = tau/T_C; the scale-free real coordinate of the phase",
        ),
        ParameterCandidate(
            "affine_parameter",
            "real",
            "gauge",
            "reparametrization label; not observable",
        ),
        ParameterCandidate(
            "mass",
            "positive real",
            "fixed",
            "eigenvalue of p^2 = m^2*c^2, not a knob",
        ),
        ParameterCandidate(
            "baryon_asymmetry",
            "positive real",
            "measured",
            "eta ~ 6.1e-10; the passage's one part in a billion",
        ),
        ParameterCandidate(
            "imaginary_time",
            "imaginary",
            "thermal",
            "tau = -i*hbar*beta gives exp(-beta*H), not a phase",
        ),
        ParameterCandidate(
            "complex_time",
            "complex",
            "non-unitary",
            "oscillation plus decay or growth",
        ),
        ParameterCandidate(
            "free_knob",
            "real",
            "rejected",
            "a freely chosen parameter is the finger the passage denies",
        ),
    )


__all__ = [
    "BARYON_TO_PHOTON_RATIO",
    "REDUCED_PLANCK",
    "SPEED_OF_LIGHT",
    "ParameterCandidate",
    "action_from_proper_time",
    "candidate_parameters",
    "compton_frequency",
    "compton_period",
    "is_on_mass_shell",
    "mass_shell_residual",
    "phase_from_action",
    "phase_from_proper_time",
    "spacebar_from_proper_time",
    "spacebar_from_ticks",
    "thermal_weight",
    "ticks_from_proper_time",
    "wrap_ticks",
]
