"""The quotient dual to the reciprocal involution (toy counter-model).

The framework's core map ``f(x) = 1/x`` is an involution: it preserves the
distinction between a scale and its reciprocal. The algebraic opposite is not
a one-way flow but the quotient that forgets that distinction:

    q(x) = x + 1/x,    q(1/x) = q(x).

``q`` is two-to-one on ``(0, infinity)``, has image ``[2, infinity)``, and is
minimised at the self-dual point ``x = 1``. It is genuinely non-invertible,
unlike the contraction ``g(x) = rate * x``, which has the expansion inverse
``x / rate``. This is a toy model, not a physical claim.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class FoldComparison:
    """A scale, its dual, the quotient, and the fundamental-domain value."""

    initial: float
    dual: float
    quotient: float
    representative: float


def _validate_scale(x: float) -> None:
    if not math.isfinite(x) or x <= 0.0:
        raise ValueError("x must be finite and > 0")


def fold(x: float) -> float:
    """Return the inversion-invariant quotient ``x + 1/x``.

    ``fold(x) == fold(1/x)``; the value is at least 2 on positive scales.

    Raises:
        ValueError: If ``x`` is not finite or is not positive.
    """
    _validate_scale(x)
    return x + 1.0 / x


def fold_from_log(t: float) -> float:
    """Return ``fold(exp(t))``, which is ``2*cosh(t)``.

    The log coordinate turns the quotient of the reciprocal involution into an
    even function of ``t``: ``fold(exp(t)) == fold(exp(-t))``. This is the
    fold-side analogue of the contraction/translation conjugacy.

    Raises:
        ValueError: If ``t`` is not finite or ``2*cosh(t)`` overflows.
    """
    if not math.isfinite(t):
        raise ValueError("t must be finite")
    try:
        result = 2.0 * math.cosh(t)
    except OverflowError:
        raise ValueError("t is too large; 2*cosh(t) overflows") from None
    if not math.isfinite(result):
        raise ValueError("t is too large; 2*cosh(t) overflows")
    return result


def _chebyshev_pair(n: int, y: float) -> tuple[float, float]:
    """Return ``(T_n(y), T_{n+1}(y))`` by fast doubling."""
    if n == 0:
        return 1.0, y
    a, b = _chebyshev_pair(n // 2, y)
    c = 2.0 * a * a - 1.0
    d = 2.0 * a * b - y
    if n % 2 == 0:
        return c, d
    return d, 2.0 * b * b - 1.0


def fold_power(x: float, exponent: int) -> float:
    """Return ``fold(x**exponent)`` through the Chebyshev recurrence.

    With ``t = log x``, ``fold(x) = 2*cosh(t)``, so powers of the scale become

        fold(x**n) = 2 * T_n(fold(x) / 2),

    where ``T_n`` is the Chebyshev polynomial of the first kind. The recurrence
    is used instead of forming ``x**n`` directly, and negative exponents reduce
    to positive ones because the fold is inversion-invariant.

    Raises:
        ValueError: If ``x`` is not finite and positive, ``exponent`` is not an
            integer, or the result overflows.
    """
    _validate_scale(x)
    if isinstance(exponent, bool) or not isinstance(exponent, int):
        raise ValueError("exponent must be an integer")
    n = abs(exponent)
    if n == 0:
        return 2.0
    value, _ = _chebyshev_pair(n, fold(x) / 2.0)
    result = 2.0 * value
    if not math.isfinite(result):
        raise ValueError("exponent is too large; fold(x**exponent) overflows")
    return result


def representative(x: float) -> float:
    """Return ``max(x, 1/x)``, the representative in ``[1, infinity)``.

    Every inversion orbit ``{x, 1/x}`` has exactly one representative here.

    Raises:
        ValueError: If ``x`` is not finite or is not positive.
    """
    _validate_scale(x)
    return max(x, 1.0 / x)


def fold_preimages(y: float) -> tuple[float, ...]:
    """Return the positive ``x`` with ``x + 1/x == y``.

    For ``y > 2`` there are two distinct preimages; for ``y == 2`` the single
    self-dual preimage ``x = 1`` is returned.

    Raises:
        ValueError: If ``y`` is not finite or is less than 2.
    """
    if not math.isfinite(y) or y < 2.0:
        raise ValueError("y must be finite and >= 2")
    root = math.sqrt(y * y - 4.0)
    low = (y - root) / 2.0
    high = (y + root) / 2.0
    if high - low <= 1e-12:
        return (1.0,)
    return (low, high)


def compare_fold(x: float) -> FoldComparison:
    """Return the scale, its dual, the quotient, and the representative.

    Raises:
        ValueError: If ``x`` is not finite or is not positive.
    """
    _validate_scale(x)
    return FoldComparison(
        initial=x,
        dual=1.0 / x,
        quotient=fold(x),
        representative=representative(x),
    )
