"""Integer roots and the root/power duality.

Taking the ``n``-th root is the map ``R_n(x) = x ** (1/n)``. The exponent map
``n -> 1/n`` is an involution with fixed points ``n = +/-1``:

- ``R_1`` is the identity;
- ``R_(-1)(x) = 1/x`` is the reciprocal, which is simultaneously the
  ``-1``-th power ``P_(-1)(x) = x ** -1``.

The implementation is real-valued: even roots of negative numbers are rejected
and negative roots of zero are undefined.
"""

from __future__ import annotations

import math


def nth_root(x: float, n: int) -> float:
    """Return the real ``n``-th root of ``x``.

    ``nth_root(x, n)`` is ``x ** (1 / n)`` evaluated over the reals.

    Args:
        x: Radicand; must be finite.
        n: Root index; must be nonzero.

    Raises:
        ValueError: If ``n == 0``, if ``x`` is not finite, if ``n`` is even
            and ``x < 0``, or if ``n < 0`` and ``x == 0``.

    Examples:
        >>> nth_root(8.0, 3)
        2.0
        >>> nth_root(4.0, -1)
        0.25
        >>> nth_root(-8.0, 3)
        -2.0
    """
    if n == 0:
        raise ValueError("root index n must be nonzero")
    if not math.isfinite(x):
        raise ValueError("x must be finite")
    if x == 0.0:
        if n < 0:
            raise ValueError("0 has no negative root")
        return 0.0
    if n < 0:
        return 1.0 / nth_root(x, -n)
    if x < 0.0:
        if n % 2 == 0:
            raise ValueError("even root of a negative number is not real")
        return -float((-x) ** (1.0 / n))
    return float(x ** (1.0 / n))
