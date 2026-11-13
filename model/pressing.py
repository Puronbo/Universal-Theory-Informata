"""Five toy checks for the mutual-press essay.

The essay's five theses each have a small, checkable core. This module
implements that core and leaves the interpretations in ``PRESSING.md``.

1. Page-Wootters: a fixed history state whose conditional system state
   depends on the clock reading. This is a toy illustration, not the full
   constraint formalism.
2. GPS: the gravitational and velocity contributions to the satellite clock
   drift, and the factory detune.
3. de Sitter: proper time diverges while the closed-slicing conformal angle
   stays in ``(-pi/2, pi/2)``.
4. Connes: the two-point spectral distance ``1/gap`` from the Dirac operator.
5. Thermal time: the modular Hamiltonian and flow of a qubit Gibbs state,
   plus the Unruh temperature.

None of these toys establishes a metaphysical thesis. They check arithmetic
and definitions.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

from model.spacebar import REDUCED_PLANCK, SPEED_OF_LIGHT

BOLTZMANN: float = 1.380_649e-23  # J / K
EARTH_GM: float = 3.986_004_418e14  # m**3 / s**2
EARTH_RADIUS: float = 6.371e6  # m
GPS_ORBIT_RADIUS: float = 26.56e6  # m
GPS_CLOCK_FREQUENCY: float = 10.23e6  # Hz
SECONDS_PER_DAY: float = 86_400.0


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


def _probability(value: float) -> float:
    value = _finite(value, "probability")
    if not 0.0 < value < 1.0:
        raise ValueError("probability must be in (0, 1)")
    return value


# Page-Wootters -------------------------------------------------------------


def page_wootters_state(angles: Sequence[float]) -> tuple[complex, ...]:
    """Return ``(1/sqrt(N)) sum_k |k>_C ⊗ |psi_k>_S``.

    Each system qubit is ``cos(theta_k/2)|0> + sin(theta_k/2)|1>``. The
    returned tuple is ordered by clock index, with two amplitudes per clock
    reading.

    Raises:
        ValueError: If ``angles`` is empty or contains a non-finite value.
    """
    if not angles:
        raise ValueError("angles must be non-empty")
    values = tuple(_finite(angle, "angle") for angle in angles)
    scale = 1.0 / math.sqrt(len(values))
    amplitudes: list[complex] = []
    for angle in values:
        amplitudes.append(scale * complex(math.cos(angle / 2.0), 0.0))
        amplitudes.append(scale * complex(math.sin(angle / 2.0), 0.0))
    return tuple(amplitudes)


def conditional_state(
    state: Sequence[complex],
    clock_index: int,
    system_dimension: int = 2,
) -> tuple[complex, ...]:
    """Return the normalized system state conditioned on one clock reading.

    The clock dimension is inferred from ``len(state) / system_dimension``.

    Raises:
        ValueError: If the state length is not a multiple of
            ``system_dimension``, the clock index is out of range, or the
            selected slice has zero norm.
    """
    if system_dimension < 1:
        raise ValueError("system_dimension must be >= 1")
    if len(state) % system_dimension != 0:
        raise ValueError("state length must be a multiple of system_dimension")
    clock_dimension = len(state) // system_dimension
    if not 0 <= clock_index < clock_dimension:
        raise ValueError("clock_index out of range")
    start = clock_index * system_dimension
    slice_ = tuple(complex(value) for value in state[start : start + system_dimension])
    if any(not math.isfinite(value.real) or not math.isfinite(value.imag) for value in slice_):
        raise ValueError("state amplitudes must be finite")
    norm = math.sqrt(sum(abs(value) ** 2 for value in slice_))
    if norm == 0.0:
        raise ValueError("selected clock slice has zero norm")
    return tuple(value / norm for value in slice_)


# GPS -----------------------------------------------------------------------


def gps_gravitational_drift_us_per_day() -> float:
    """Return the gravitational clock gain in microseconds per day."""
    delta_phi = EARTH_GM * (1.0 / EARTH_RADIUS - 1.0 / GPS_ORBIT_RADIUS)
    fraction = delta_phi / SPEED_OF_LIGHT**2
    return fraction * SECONDS_PER_DAY * 1e6


def gps_velocity_drift_us_per_day() -> float:
    """Return the special-relativistic clock loss in microseconds per day."""
    speed = math.sqrt(EARTH_GM / GPS_ORBIT_RADIUS)
    fraction = -0.5 * (speed / SPEED_OF_LIGHT) ** 2
    return fraction * SECONDS_PER_DAY * 1e6


def gps_net_drift_us_per_day() -> float:
    """Return the net satellite clock gain in microseconds per day."""
    return gps_gravitational_drift_us_per_day() + gps_velocity_drift_us_per_day()


def gps_factory_detune() -> float:
    """Return the factory clock frequency that pre-compensates the net drift."""
    fraction = gps_net_drift_us_per_day() * 1e-6 / SECONDS_PER_DAY
    return GPS_CLOCK_FREQUENCY * (1.0 - fraction)


# de Sitter ----------------------------------------------------------------


def desitter_conformal_time_range() -> tuple[float, float]:
    """Return the closed-slicing conformal-time interval ``(-pi/2, pi/2)``."""
    return (-math.pi / 2.0, math.pi / 2.0)


def _conformal_angle(angle: float) -> float:
    angle = _finite(angle, "conformal_angle")
    if not -math.pi / 2.0 < angle < math.pi / 2.0:
        raise ValueError("conformal_angle must lie in (-pi/2, pi/2)")
    return angle


def desitter_closed_scale_factor(conformal_angle: float, hubble: float) -> float:
    """Return ``1 / (H cos(T))`` for closed-slicing de Sitter.

    Raises:
        ValueError: If the angle is outside the strip or ``hubble`` is not
            finite and positive.
    """
    angle = _conformal_angle(conformal_angle)
    hubble = _positive(hubble, "hubble")
    return 1.0 / (hubble * math.cos(angle))


def desitter_proper_time(conformal_angle: float, hubble: float) -> float:
    """Return ``asinh(tan(T)) / H``, the proper time from the finite strip.

    The proper time diverges as ``T`` approaches either endpoint.

    Raises:
        ValueError: If the angle is outside the strip or ``hubble`` is not
            finite and positive.
    """
    angle = _conformal_angle(conformal_angle)
    hubble = _positive(hubble, "hubble")
    return math.asinh(math.tan(angle)) / hubble


# Connes distance ----------------------------------------------------------


def commutator_norm_two_point(gap: float, difference: float) -> float:
    """Return the operator norm of ``[D, diag(f1, f2)]``.

    With ``D = [[0, gap], [gap, 0]]`` and ``f = diag(f1, f2)``, the
    commutator has norm ``gap * |f1 - f2|``.

    Raises:
        ValueError: If ``gap`` is not finite and positive, or ``difference``
            is not finite.
    """
    gap = _positive(gap, "gap")
    difference = _finite(difference, "difference")
    return gap * abs(difference)


def connes_distance_two_point(gap: float) -> float:
    """Return ``1/gap`` for the two-point spectral triple.

    The Dirac operator is ``D = [[0, gap], [gap, 0]]``. Its eigenvalue gap is
    ``2*gap``, while the commutator scale is ``gap``; the spectral distance
    between the two eigenstates is ``1/gap``.

    Raises:
        ValueError: If ``gap`` is not finite and positive.
    """
    gap = _positive(gap, "gap")
    return 1.0 / gap


# Thermal time -------------------------------------------------------------


def modular_hamiltonian(probability: float) -> tuple[float, float]:
    """Return ``(-log(p), -log(1-p))`` for a qubit Gibbs state.

    Raises:
        ValueError: If ``probability`` is not in ``(0, 1)``.
    """
    value = _probability(probability)
    return (-math.log(value), -math.log(1.0 - value))


def modular_frequency(probability: float) -> float:
    """Return ``log(p/(1-p))``, the modular flow frequency.

    Raises:
        ValueError: If ``probability`` is not in ``(0, 1)``.
    """
    value = _probability(probability)
    return math.log(value / (1.0 - value))


def modular_flow_bloch(probability: float, time: float) -> tuple[float, float, float]:
    """Return the Bloch vector of ``sigma_x`` under the modular flow.

    The flow rotates in the ``x-y`` plane at ``omega = log(p/(1-p))``.

    Raises:
        ValueError: If ``probability`` is not in ``(0, 1)`` or ``time`` is
            not finite.
    """
    omega = modular_frequency(probability)
    time = _finite(time, "time")
    return (math.cos(omega * time), -math.sin(omega * time), 0.0)


def unruh_temperature(acceleration: float) -> float:
    """Return ``hbar*a / (2*pi*c*k_B)``, the Unruh temperature.

    Raises:
        ValueError: If ``acceleration`` is not finite or negative.
    """
    acceleration = _finite(acceleration, "acceleration")
    if acceleration < 0.0:
        raise ValueError("acceleration must be >= 0")
    return REDUCED_PLANCK * acceleration / (2.0 * math.pi * SPEED_OF_LIGHT * BOLTZMANN)


__all__ = [
    "BOLTZMANN",
    "EARTH_GM",
    "EARTH_RADIUS",
    "GPS_CLOCK_FREQUENCY",
    "GPS_ORBIT_RADIUS",
    "SECONDS_PER_DAY",
    "commutator_norm_two_point",
    "conditional_state",
    "connes_distance_two_point",
    "desitter_closed_scale_factor",
    "desitter_conformal_time_range",
    "desitter_proper_time",
    "gps_factory_detune",
    "gps_gravitational_drift_us_per_day",
    "gps_net_drift_us_per_day",
    "gps_velocity_drift_us_per_day",
    "modular_flow_bloch",
    "modular_frequency",
    "modular_hamiltonian",
    "page_wootters_state",
    "unruh_temperature",
]
