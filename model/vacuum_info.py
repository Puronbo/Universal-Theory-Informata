"""What "nothing" can hold: vacuum information bounds (toy bookkeeping).

A literal void has one state and therefore zero bits. The physically meaningful
"empty" structures are different:

- The vacuum is a state of quantum fields, not an absence of degrees of freedom.
- A horizon is a causal boundary with a finite entropy.
- A constraint selects a code subspace of allowed states.

This module makes the standard bounds explicit:

- Bekenstein: ``I <= 2*pi*R*E / (hbar*c*ln 2)`` bits.
- Holographic: ``I <= A / (4*l_P**2*ln 2)`` bits.
- de Sitter horizon: ``R_H = c/H`` and ``A = 4*pi*R_H**2``.
- Landauer erasure: ``E = k_B*T*ln 2``.
- Two-mode squeezing: the entanglement entropy of a Gaussian vacuum.
- No-signaling: a local unitary on one subsystem leaves the other marginal
  unchanged.

None of these bounds creates information. They describe the capacity and the
protection of correlations. The interpretations are in ``VACUUM_INFO.md``.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

from model.pressing import BOLTZMANN
from model.spacebar import REDUCED_PLANCK, SPEED_OF_LIGHT

BITS_PER_NAT: float = 1.0 / math.log(2.0)
PLANCK_LENGTH: float = 1.616_255e-35  # m


def _finite(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _nonnegative(value: float, name: str) -> float:
    value = _finite(value, name)
    if value < 0.0:
        raise ValueError(f"{name} must be >= 0")
    return value


def _positive(value: float, name: str) -> float:
    value = _finite(value, name)
    if value <= 0.0:
        raise ValueError(f"{name} must be > 0")
    return value


# Capacity bounds -----------------------------------------------------------


def bekenstein_bits(radius: float, energy: float) -> float:
    """Return ``2*pi*R*E / (hbar*c*ln 2)``, the Bekenstein bit bound.

    The bound is a capacity, not a guarantee: a region with zero radius or zero
    energy has zero capacity.

    Raises:
        ValueError: If ``radius`` or ``energy`` is not finite and nonnegative.
    """
    radius = _nonnegative(radius, "radius")
    energy = _nonnegative(energy, "energy")
    denominator = REDUCED_PLANCK * SPEED_OF_LIGHT * math.log(2.0)
    return 2.0 * math.pi * radius * energy / denominator


def holographic_bits(area: float) -> float:
    """Return ``A / (4*l_P**2*ln 2)``, the holographic bit bound.

    One Planck area carries ``1/(4*ln 2)`` bits, about ``0.3607`` bits.

    Raises:
        ValueError: If ``area`` is not finite and nonnegative.
    """
    area = _nonnegative(area, "area")
    denominator = 4.0 * PLANCK_LENGTH**2 * math.log(2.0)
    return area / denominator


def desitter_horizon_radius(hubble: float) -> float:
    """Return ``c/H``, the de Sitter horizon radius.

    Raises:
        ValueError: If ``hubble`` is not finite and positive.
    """
    hubble = _positive(hubble, "hubble")
    return SPEED_OF_LIGHT / hubble


def desitter_bits(hubble: float) -> float:
    """Return the holographic bit capacity of the de Sitter horizon.

    The horizon area is ``4*pi*(c/H)**2``. For the observed Hubble scale this is
    of order ``1e122`` bits.

    Raises:
        ValueError: If ``hubble`` is not finite and positive.
    """
    radius = desitter_horizon_radius(hubble)
    return holographic_bits(4.0 * math.pi * radius**2)


# Erasure and noise ---------------------------------------------------------


def landauer_energy(temperature: float) -> float:
    """Return ``k_B*T*ln 2``, the minimum energy to erase one bit.

    Raises:
        ValueError: If ``temperature`` is not finite and nonnegative.
    """
    temperature = _nonnegative(temperature, "temperature")
    return BOLTZMANN * temperature * math.log(2.0)


# Gaussian vacuum entanglement ---------------------------------------------


def two_mode_squeezing_photon_number(squeezing: float) -> float:
    """Return ``sinh(squeezing)**2``, the mean photon number per mode.

    Raises:
        ValueError: If ``squeezing`` is not finite or the result overflows.
    """
    squeezing = _finite(squeezing, "squeezing")
    try:
        amplitude = math.sinh(squeezing)
    except OverflowError:
        raise ValueError("squeezing is too large; sinh(squeezing)**2 overflows") from None
    value = amplitude * amplitude
    if not math.isfinite(value):
        raise ValueError("squeezing is too large; sinh(squeezing)**2 overflows")
    return value


def two_mode_mutual_information(squeezing: float) -> float:
    """Return the mutual information of a two-mode squeezed vacuum in bits.

    For a pure two-mode state the mutual information is twice the entropy of
    one mode. With ``n = sinh(r)**2``,

        S = (n+1)*ln(n+1) - n*ln(n),

    and the result is ``2*S/ln(2)`` bits. At ``r = 0`` the state is the vacuum
    and the mutual information is zero.

    Raises:
        ValueError: If ``squeezing`` is not finite or the result overflows.
    """
    photons = two_mode_squeezing_photon_number(squeezing)
    if photons == 0.0:
        return 0.0
    entropy = (photons + 1.0) * math.log(photons + 1.0) - photons * math.log(photons)
    return 2.0 * entropy * BITS_PER_NAT


# No-signaling toy ----------------------------------------------------------


def _validate_dimensions(dimensions: tuple[int, int]) -> tuple[int, int]:
    if len(dimensions) != 2:
        raise ValueError("dimensions must contain two positive integers")
    left, right = dimensions
    if isinstance(left, bool) or isinstance(right, bool):
        raise ValueError("dimensions must contain two positive integers")
    if not isinstance(left, int) or not isinstance(right, int) or left < 1 or right < 1:
        raise ValueError("dimensions must contain two positive integers")
    return left, right


def marginal_probabilities(
    state: Sequence[complex],
    subsystem: int = 1,
    dimensions: tuple[int, int] = (2, 2),
) -> tuple[float, ...]:
    """Return normalized marginal probabilities for one subsystem.

    The state is ordered row-major: amplitude ``(a, b)`` is at
    ``a*dimensions[1] + b``. ``subsystem=0`` returns the left marginal;
    ``subsystem=1`` returns the right marginal.

    Raises:
        ValueError: If the dimensions, state length, subsystem, or amplitudes
            are invalid, or the state has zero norm.
    """
    left, right = _validate_dimensions(dimensions)
    if len(state) != left * right:
        raise ValueError("state length must equal dimensions[0] * dimensions[1]")
    if subsystem not in (0, 1):
        raise ValueError("subsystem must be 0 or 1")
    amplitudes = tuple(complex(value) for value in state)
    if any(not math.isfinite(value.real) or not math.isfinite(value.imag) for value in amplitudes):
        raise ValueError("state amplitudes must be finite")
    norm_squared = sum(abs(value) ** 2 for value in amplitudes)
    if norm_squared == 0.0:
        raise ValueError("state must have nonzero norm")
    if subsystem == 0:
        return tuple(
            sum(abs(amplitudes[a * right + b]) ** 2 for b in range(right)) / norm_squared
            for a in range(left)
        )
    return tuple(
        sum(abs(amplitudes[a * right + b]) ** 2 for a in range(left)) / norm_squared
        for b in range(right)
    )


def apply_local_unitary(
    state: Sequence[complex],
    matrix: Sequence[Sequence[complex]],
    subsystem: int = 0,
    dimensions: tuple[int, int] = (2, 2),
) -> tuple[complex, ...]:
    """Apply a unitary to one subsystem of a bipartite pure state.

    The state is ordered row-major. ``subsystem=0`` mixes the left index;
    ``subsystem=1`` mixes the right index.

    Raises:
        ValueError: If the dimensions, state, matrix, or subsystem are invalid.
    """
    left, right = _validate_dimensions(dimensions)
    if len(state) != left * right:
        raise ValueError("state length must equal dimensions[0] * dimensions[1]")
    if subsystem not in (0, 1):
        raise ValueError("subsystem must be 0 or 1")
    size = left if subsystem == 0 else right
    if len(matrix) != size or any(len(row) != size for row in matrix):
        raise ValueError("matrix must be square with the subsystem dimension")
    amplitudes = tuple(complex(value) for value in state)
    if any(not math.isfinite(value.real) or not math.isfinite(value.imag) for value in amplitudes):
        raise ValueError("state amplitudes must be finite")
    entries = tuple(tuple(complex(value) for value in row) for row in matrix)
    if any(
        not math.isfinite(value.real) or not math.isfinite(value.imag)
        for row in entries
        for value in row
    ):
        raise ValueError("matrix entries must be finite")
    result = [0j] * (left * right)
    if subsystem == 0:
        for a in range(left):
            for source in range(left):
                coefficient = entries[a][source]
                if coefficient == 0:
                    continue
                for b in range(right):
                    result[a * right + b] += coefficient * amplitudes[source * right + b]
    else:
        for b in range(right):
            for source in range(right):
                coefficient = entries[b][source]
                if coefficient == 0:
                    continue
                for a in range(left):
                    result[a * right + b] += coefficient * amplitudes[a * right + source]
    return tuple(result)


__all__ = [
    "BITS_PER_NAT",
    "PLANCK_LENGTH",
    "apply_local_unitary",
    "bekenstein_bits",
    "desitter_bits",
    "desitter_horizon_radius",
    "holographic_bits",
    "landauer_energy",
    "marginal_probabilities",
    "two_mode_mutual_information",
    "two_mode_squeezing_photon_number",
]
