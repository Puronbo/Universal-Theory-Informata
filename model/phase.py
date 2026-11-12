"""Complex phase and observable projection (standard complex arithmetic).

The source document's corrected metaphor is ordinary quantum mechanics: a wave
has a complex amplitude, the phase is physically active but not directly
observable, and measurements see the modulus squared. This module makes that
projection explicit and relates wavelength to wavenumber.

It is tooling for the framework's "visible front / hidden back" language, not a
physical claim.
"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class WaveSample:
    """A complex amplitude together with its observable projection."""

    amplitude: complex
    intensity: float
    phase: float


def _finite_complex(value: complex, name: str) -> complex:
    value = complex(value)
    if not cmath.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _finite_float(value: float, name: str) -> float:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def wavenumber_from_wavelength(wavelength: float) -> float:
    """Return ``k = 2*pi / wavelength``.

    Raises:
        ValueError: If ``wavelength`` is not finite or not positive.
    """
    wavelength = _finite_float(wavelength, "wavelength")
    if wavelength <= 0.0:
        raise ValueError("wavelength must be > 0")
    return 2.0 * math.pi / wavelength


def wavelength_from_wavenumber(wavenumber: float) -> float:
    """Return ``2*pi / abs(k)``.

    Raises:
        ValueError: If ``wavenumber`` is not finite or is zero.
    """
    wavenumber = _finite_float(wavenumber, "wavenumber")
    if wavenumber == 0.0:
        raise ValueError("wavenumber must be nonzero")
    return 2.0 * math.pi / abs(wavenumber)


def phase_factor(
    wavenumber: float,
    position: float,
    angular_frequency: float = 0.0,
    time: float = 0.0,
) -> complex:
    """Return the unit phase ``exp(i (k x - omega t))``.

    Raises:
        ValueError: If any argument is not finite.
    """
    k = _finite_float(wavenumber, "wavenumber")
    x = _finite_float(position, "position")
    omega = _finite_float(angular_frequency, "angular_frequency")
    t = _finite_float(time, "time")
    return cmath.exp(1j * (k * x - omega * t))


def wave_sample(
    amplitude: complex,
    wavenumber: float,
    position: float,
    angular_frequency: float = 0.0,
    time: float = 0.0,
) -> WaveSample:
    """Return the complex sample and its observable intensity and phase.

    Raises:
        ValueError: If any argument is not finite.
    """
    value = _finite_complex(amplitude, "amplitude") * phase_factor(
        wavenumber, position, angular_frequency, time
    )
    return WaveSample(
        amplitude=value,
        intensity=abs(value) ** 2,
        phase=cmath.phase(value),
    )


def intensity(amplitude: complex) -> float:
    """Return the observable ``|amplitude|**2``.

    Raises:
        ValueError: If ``amplitude`` is not finite.
    """
    return abs(_finite_complex(amplitude, "amplitude")) ** 2


def phase_angle(amplitude: complex) -> float:
    """Return the phase angle in ``[-pi, pi]``.

    Raises:
        ValueError: If ``amplitude`` is not finite.
    """
    return cmath.phase(_finite_complex(amplitude, "amplitude"))


def rotate_quarter_turn(value: complex) -> complex:
    """Return ``i * value``, a 90-degree rotation in the complex plane.

    Raises:
        ValueError: If ``value`` is not finite.
    """
    return 1j * _finite_complex(value, "value")


def conjugate(value: complex) -> complex:
    """Return the complex conjugate.

    Raises:
        ValueError: If ``value`` is not finite.
    """
    return _finite_complex(value, "value").conjugate()


def real_width(value: complex) -> float:
    """Return the real part, the "width" of the complex sample.

    Raises:
        ValueError: If ``value`` is not finite.
    """
    return _finite_complex(value, "value").real


def imaginary_height(value: complex) -> float:
    """Return the imaginary part, the hidden phase "height".

    Raises:
        ValueError: If ``value`` is not finite.
    """
    return _finite_complex(value, "value").imag
