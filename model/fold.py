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
