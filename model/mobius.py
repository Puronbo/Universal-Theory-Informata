"""Möbius transformations on the Riemann sphere (tooling).

A Möbius transformation is a fractional linear map

    z -> (a z + b) / (c z + d),   a d - b c != 0.

The reciprocal map ``z -> 1/z`` is the order-two element represented by the
matrix ``[[0, 1], [1, 0]]``. This module makes composition, powers, and
fixed-point solving explicit. It is infrastructure for the UV/IR inversion
analogy, not a physical claim.
"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Mobius:
    """Fractional linear map ``z -> (a z + b) / (c z + d)``."""

    a: complex
    b: complex
    c: complex
    d: complex

    def __post_init__(self) -> None:
        if not all(cmath.isfinite(v) for v in (self.a, self.b, self.c, self.d)):
            raise ValueError("Möbius matrix entries must be finite")
        if abs(self.det) == 0.0:
            raise ValueError("Möbius matrix must be invertible: ad - bc != 0")

    @property
    def det(self) -> complex:
        """Determinant ``ad - bc``."""
        return self.a * self.d - self.b * self.c

    @property
    def matrix(self) -> tuple[tuple[complex, complex], tuple[complex, complex]]:
        """Row-major 2x2 matrix representation."""
        return ((self.a, self.b), (self.c, self.d))

    @classmethod
    def inversion(cls) -> Mobius:
        """Return the reciprocal map ``z -> 1/z``."""
        return cls(0, 1, 1, 0)

    @classmethod
    def translation(cls, shift: float = 1.0) -> Mobius:
        """Return the parabolic map ``z -> z + shift``.

        Raises:
            ValueError: If ``shift`` is not finite or is zero.
        """
        if not math.isfinite(shift) or shift == 0.0:
            raise ValueError("shift must be finite and nonzero")
        return cls(1, shift, 0, 1)

    @classmethod
    def contraction(cls, rate: float = 0.5) -> Mobius:
        """Return the hyperbolic contraction ``z -> rate * z``.

        Raises:
            ValueError: If ``rate`` is not finite or not in ``(0, 1)``.
        """
        if not math.isfinite(rate) or not 0.0 < rate < 1.0:
            raise ValueError("rate must be finite and satisfy 0 < rate < 1")
        return cls(rate, 0, 0, 1)

    def __call__(self, z: complex | float) -> complex:
        """Apply the map to a finite point.

        Raises:
            ZeroDivisionError: If ``z`` is the pole ``-d/c``.
        """
        value = complex(z)
        denominator = self.c * value + self.d
        if denominator == 0:
            raise ZeroDivisionError("point is the pole of the Möbius map")
        return (self.a * value + self.b) / denominator

    def compose(self, other: Mobius) -> Mobius:
        """Return ``self ∘ other`` (``other`` is applied first)."""
        return Mobius(
            self.a * other.a + self.b * other.c,
            self.a * other.b + self.b * other.d,
            self.c * other.a + self.d * other.c,
            self.c * other.b + self.d * other.d,
        )

    def inverse(self) -> Mobius:
        """Return the inverse map (the adjugate matrix; scale is irrelevant)."""
        return Mobius(self.d, -self.b, -self.c, self.a)

    def power(self, n: int) -> Mobius:
        """Return the ``n``-fold composition; ``n < 0`` gives the inverse."""
        if n < 0:
            return self.inverse().power(-n)
        result = Mobius(1, 0, 0, 1)
        base = self
        while n:
            if n & 1:
                result = result.compose(base)
            base = base.compose(base)
            n >>= 1
        return result

    def fixed_points(self) -> tuple[complex, ...]:
        """Return the finite fixed points of the map.

        The fixed-point equation is ``c z^2 + (d - a) z - b = 0``. A map with
        no finite fixed points (a nontrivial translation) returns ``()``. The
        identity raises ``ValueError`` because every point is fixed.
        """
        if abs(self.c) < 1e-15:
            if abs(self.d - self.a) < 1e-15:
                if abs(self.b) < 1e-15:
                    raise ValueError("identity fixes every point")
                return ()
            return (self.b / (self.d - self.a),)
        linear = self.d - self.a
        discriminant = cmath.sqrt(linear * linear + 4.0 * self.b * self.c)
        denominator = 2.0 * self.c
        return (
            (-linear + discriminant) / denominator,
            (-linear - discriminant) / denominator,
        )

    def is_identity(self, tol: float = 1e-9) -> bool:
        """Return whether the map is the identity, projectively (up to ``tol``)."""
        scale = max(abs(self.a), abs(self.b), abs(self.c), abs(self.d))
        if scale == 0.0:
            return False
        a, b, c, d = (v / scale for v in (self.a, self.b, self.c, self.d))
        return abs(b) <= tol and abs(c) <= tol and abs(a - d) <= tol

    def order(self, max_order: int = 12, tol: float = 1e-9) -> int | None:
        """Return the smallest ``n >= 1`` with ``self.power(n)`` the identity.

        Returns ``None`` when no order ``<= max_order`` is found. The check is
        tolerant because the entries are floating point.
        """
        for n in range(1, max_order + 1):
            if self.power(n).is_identity(tol=tol):
                return n
        return None

    def classify(self, tol: float = 1e-9) -> str:
        """Classify the map by its dynamical type.

        Returns ``"periodic"`` when the map has finite order. Otherwise the
        trace-discriminant ``(a + d)^2 - 4 det`` distinguishes ``"parabolic"``,
        ``"hyperbolic"``, and ``"elliptic"``; complex trace data yields
        ``"loxodromic"``.

        The classification is a convention for real Möbius maps extended to
        complex entries; it is descriptive, not a physical claim.
        """
        if self.order(max_order=12, tol=tol) is not None:
            return "periodic"
        discriminant = (self.a + self.d) ** 2 - 4.0 * self.det
        if abs(discriminant.imag) > tol:
            return "loxodromic"
        real = discriminant.real
        if abs(real) <= tol:
            return "parabolic"
        return "hyperbolic" if real > 0.0 else "elliptic"
