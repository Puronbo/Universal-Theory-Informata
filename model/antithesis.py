"""The antithesis of the self-looping framework (toy counter-models).

The main framework is built on the involution ``f(x) = 1/x``: reversible,
order two, with fixed points ``+/-1``. This module implements the opposite
limits: a dissipative contraction ``g(x) = rate * x`` with ``0 < rate < 1``,
a parabolic translation ``x + shift``, and the nilpotent ``N(x, y) = (0, x)``.
It also supplies monotone entropy ``-log(x)``, information-loss and Lyapunov
measures, cycle detection, three-way regime comparison, and the log-coordinate
conjugacy that turns contraction into translation. These are conceptual
counter-models, not physical claims.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from model.self_looping import uv_ir_inversion


@dataclass(frozen=True)
class OrbitComparison:
    """Side-by-side orbits of the involution and the contraction."""

    initial: float
    involution: tuple[float, ...]
    contraction: tuple[float, ...]


@dataclass(frozen=True)
class RegimeComparison:
    """Side-by-side periodic, contracting, and translating orbits."""

    initial: float
    involution: tuple[float, ...]
    contraction: tuple[float, ...]
    translation: tuple[float, ...]


@dataclass(frozen=True)
class LogConjugacy:
    """A contraction orbit in log coordinates and the matching translation."""

    initial: float
    log_orbit: tuple[float, ...]
    translation: tuple[float, ...]


def _validate_rate(rate: float) -> None:
    if not math.isfinite(rate) or not 0.0 < rate < 1.0:
        raise ValueError("rate must be finite and satisfy 0 < rate < 1")


def _validate_steps(steps: int) -> None:
    if steps < 0:
        raise ValueError("steps must be >= 0")


def contract(x: float, rate: float = 0.5) -> float:
    """One step of the one-way contraction ``g(x) = rate * x``.

    Raises:
        ValueError: If ``x`` is not finite or ``rate`` is outside ``(0, 1)``.
    """
    if not math.isfinite(x):
        raise ValueError("x must be finite")
    _validate_rate(rate)
    return rate * x


def contract_orbit(x: float, steps: int, rate: float = 0.5) -> tuple[float, ...]:
    """Return ``(x, g(x), ..., g^steps(x))`` for the contraction.

    Raises:
        ValueError: If ``steps`` is negative or the inputs are invalid.
    """
    _validate_steps(steps)
    if not math.isfinite(x):
        raise ValueError("x must be finite")
    _validate_rate(rate)
    values = [x]
    for _ in range(steps):
        values.append(rate * values[-1])
    return tuple(values)


def translation(x: float, shift: float = 1.0) -> float:
    """One step of the parabolic map ``p(x) = x + shift``.

    A translation has no finite fixed point and never returns. ``shift`` must
    be finite and nonzero.

    Raises:
        ValueError: If ``x`` or ``shift`` is not finite, or ``shift == 0``.
    """
    if not math.isfinite(x) or not math.isfinite(shift) or shift == 0.0:
        raise ValueError("x and shift must be finite, and shift must be nonzero")
    return x + shift


def translation_orbit(x: float, steps: int, shift: float = 1.0) -> tuple[float, ...]:
    """Return ``(x, p(x), ..., p^steps(x))`` for the translation.

    Raises:
        ValueError: If ``steps`` is negative or the inputs are invalid.
    """
    _validate_steps(steps)
    if not math.isfinite(x) or not math.isfinite(shift) or shift == 0.0:
        raise ValueError("x and shift must be finite, and shift must be nonzero")
    values = [x]
    for _ in range(steps):
        values.append(values[-1] + shift)
    return tuple(values)


def log_coordinate(x: float) -> float:
    """Return ``log(x)``, the additive coordinate for positive scales.

    Raises:
        ValueError: If ``x`` is not finite or is not positive.
    """
    if not math.isfinite(x) or x <= 0.0:
        raise ValueError("x must be finite and > 0")
    return math.log(x)


def exp_coordinate(t: float) -> float:
    """Return ``exp(t)``, the inverse of :func:`log_coordinate`.

    Raises:
        ValueError: If ``t`` is not finite or is too large to exponentiate.
    """
    if not math.isfinite(t):
        raise ValueError("t must be finite")
    try:
        return math.exp(t)
    except OverflowError as exc:
        raise ValueError("t is too large to exponentiate") from exc


def log_orbit(x: float, steps: int, rate: float = 0.5) -> tuple[float, ...]:
    """Return the contraction orbit in log coordinates.

    Under ``t = log(x)`` the contraction becomes a translation by
    ``log(rate)``, so this equals
    ``translation_orbit(log_coordinate(x), steps, log(rate))``.

    Raises:
        ValueError: If ``steps`` is negative or the inputs are invalid.
    """
    log_coordinate(x)
    _validate_steps(steps)
    _validate_rate(rate)
    return tuple(math.log(value) for value in contract_orbit(x, steps, rate))


def compare_log_conjugacy(x: float, steps: int, rate: float = 0.5) -> LogConjugacy:
    """Return the log orbit and the matching translation orbit.

    Raises:
        ValueError: If ``steps`` is negative or the inputs are invalid.
    """
    return LogConjugacy(
        initial=x,
        log_orbit=log_orbit(x, steps, rate),
        translation=translation_orbit(log_coordinate(x), steps, math.log(rate)),
    )


def nilpotent_apply(x: float, y: float) -> tuple[float, float]:
    """Apply the nilpotent ``N(x, y) = (0, x)``; ``N^2 = 0``.

    Raises:
        ValueError: If ``x`` or ``y`` is not finite.
    """
    if not math.isfinite(x) or not math.isfinite(y):
        raise ValueError("x and y must be finite")
    return (0.0, x)


def nilpotent_orbit(x: float, y: float, steps: int) -> tuple[tuple[float, float], ...]:
    """Return the orbit of ``N`` from ``(x, y)``.

    The orbit reaches ``(0, 0)`` after at most two steps and stays there.

    Raises:
        ValueError: If ``steps`` is negative or the inputs are not finite.
    """
    _validate_steps(steps)
    values = [(x, y)]
    current = nilpotent_apply(x, y)
    for _ in range(steps):
        values.append(current)
        current = nilpotent_apply(*current)
    return tuple(values)


def entropy(x: float) -> float:
    """Monotone entropy ``-log(x)`` for ``x > 0``.

    As the contraction drives ``x`` toward zero, entropy increases without
    bound.

    Raises:
        ValueError: If ``x`` is not finite or is not positive.
    """
    if not math.isfinite(x) or x <= 0.0:
        raise ValueError("x must be finite and > 0")
    return -math.log(x)


def inversion_orbit(x: float, steps: int) -> tuple[float, ...]:
    """Return ``(x, f(x), ..., f^steps(x))`` for ``f = uv_ir_inversion``.

    Raises:
        ValueError: If ``steps`` is negative or ``x`` is not a positive,
            finite scale.
    """
    _validate_steps(steps)
    values = [x]
    current = uv_ir_inversion(x)
    for _ in range(steps):
        values.append(current)
        current = uv_ir_inversion(current)
    return tuple(values)


def lyapunov_exponent(rate: float) -> float:
    """Return the Lyapunov exponent ``log(rate)`` of the contraction.

    The exponent is negative for ``0 < rate < 1``; the involution is neutral
    (exponent zero).

    Raises:
        ValueError: If ``rate`` is not finite or not in ``(0, 1)``.
    """
    _validate_rate(rate)
    return math.log(rate)


def information_loss(x: float, steps: int, rate: float = 0.5) -> float:
    """Entropy gained by ``steps`` contraction steps.

    This is ``entropy(g^steps(x)) - entropy(x) = -steps * log(rate)``, which is
    positive for ``0 < rate < 1`` and ``x > 0``.

    Raises:
        ValueError: If ``steps`` is negative, ``x`` is not positive and finite,
            or ``rate`` is outside ``(0, 1)``.
    """
    _validate_steps(steps)
    if not math.isfinite(x) or x <= 0.0:
        raise ValueError("x must be finite and > 0")
    _validate_rate(rate)
    return -steps * math.log(rate)


def orbit_period(orbit: tuple[float, ...], tol: float = 1e-12) -> int | None:
    """Return the smallest period consistent with the observed orbit.

    The orbit is periodic with period ``p`` when its last value matches the
    value ``p`` places earlier within ``tol``. Returns ``None`` for a
    non-periodic or too-short window.
    """
    if len(orbit) < 2:
        return None
    last = orbit[-1]
    for period in range(1, len(orbit)):
        if abs(last - orbit[-1 - period]) <= tol:
            return period
    return None


def is_cyclic(orbit: tuple[float, ...], tol: float = 1e-12) -> bool:
    """Return whether the last value repeats an earlier value."""
    return orbit_period(orbit, tol) is not None


def compare_orbits(x: float, steps: int, rate: float = 0.5) -> OrbitComparison:
    """Return the involution and contraction orbits from the same ``x``.

    Raises:
        ValueError: If ``steps`` is negative or the inputs are invalid.
    """
    return OrbitComparison(
        initial=x,
        involution=inversion_orbit(x, steps),
        contraction=contract_orbit(x, steps, rate),
    )


def compare_regimes(
    x: float, steps: int, rate: float = 0.5, shift: float = 1.0
) -> RegimeComparison:
    """Return the periodic, contracting, and translating orbits from ``x``.

    This is the three-way comparison: an involution (periodic), a contraction
    (hyperbolic collapse), and a translation (parabolic drift).

    Raises:
        ValueError: If ``steps`` is negative or the inputs are invalid.
    """
    return RegimeComparison(
        initial=x,
        involution=inversion_orbit(x, steps),
        contraction=contract_orbit(x, steps, rate),
        translation=translation_orbit(x, steps, shift),
    )
