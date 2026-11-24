"""The multiplicative group: one as identity, zero as the excluded element.

The sentence "one is divisible by every number" reverses a true statement.
In the integers, one divides every integer because ``n = n * 1``, while only
``±1`` divide one. In a field every nonzero element is a unit, so "divisible by
every nonzero number" is a property of the field, not of one. The set that
deserves the phrase "everything nonzero" is the multiplicative group ``F^x``;
one is its identity, and zero is the one excluded element.

This module builds the finite exact model: the unit group of ``Z/nZ``. For a
prime modulus it is every nonzero residue; for a composite modulus it is a
proper subset, which shows that "nonzero" and "unit" coincide only in a field.

It also builds the projective reciprocal. On the projective line ``P^1``, the
map ``x -> 1/x`` extends by ``0 -> infinity`` and ``infinity -> 0``, becoming an
involution with fixed points ``±1``. The value ``1/0`` is a choice of
compactification, not a definition: the equation ``1/0 = 1/0`` is reflexivity,
not content.

The interpretive readings are not in the code. The exact/rhyme boundary is in
``ZERO_AND_HOLES.md``.
"""

from __future__ import annotations

import math
from fractions import Fraction

__all__ = [
    "divides",
    "is_field_mod",
    "projective_reciprocal",
    "reciprocal",
    "reciprocal_fixed_points",
    "unit_inverse",
    "units_mod",
]


def _integer(value: int, name: str) -> int:
    """Return ``value`` after checking that it is an integer."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def _fraction(value: int | Fraction, name: str) -> Fraction:
    """Return ``value`` as a Fraction after checking its type."""
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise ValueError(f"{name} must be an integer or a Fraction")
    return Fraction(value)


def divides(divisor: int, value: int) -> bool:
    """Return whether ``divisor`` divides ``value`` in the integers.

    ``a`` divides ``b`` when there is an integer ``k`` with ``b = a*k``. One
    divides every integer; only ``±1`` divide one. By the same definition, zero
    divides only zero.

    Args:
        divisor: The candidate divisor.
        value: The candidate multiple.

    Returns:
        ``True`` when the remainder is zero.

    Raises:
        ValueError: If either argument is not an integer.
    """
    divisor = _integer(divisor, "divisor")
    value = _integer(value, "value")
    if divisor == 0:
        return value == 0
    return value % divisor == 0


def units_mod(modulus: int) -> tuple[int, ...]:
    """Return the units of ``Z/modulus Z`` in ascending order.

    An element is a unit when it has a multiplicative inverse modulo
    ``modulus``, equivalently when it is coprime to ``modulus``. The identity
    is one. Zero is never a unit.

    For a prime modulus the units are exactly the nonzero residues; for a
    composite modulus they are a proper subset.

    Args:
        modulus: The modulus.

    Returns:
        The unit residues.

    Raises:
        ValueError: If ``modulus`` is not an integer or is less than two.
    """
    modulus = _integer(modulus, "modulus")
    if modulus < 2:
        raise ValueError(f"modulus must be at least 2, got {modulus}")
    return tuple(value for value in range(1, modulus) if math.gcd(value, modulus) == 1)


def is_field_mod(modulus: int) -> bool:
    """Return whether ``Z/modulus Z`` is a field.

    This holds exactly when every nonzero residue is a unit, which is exactly
    when ``modulus`` is prime.

    Args:
        modulus: The modulus.

    Returns:
        ``True`` when the unit group is every nonzero residue.

    Raises:
        ValueError: If ``modulus`` is not an integer or is less than two.
    """
    units = units_mod(modulus)
    return len(units) == modulus - 1


def unit_inverse(value: int, modulus: int) -> int:
    """Return the inverse of ``value`` modulo ``modulus``.

    Args:
        value: A residue or any integer; it is reduced modulo ``modulus``.
        modulus: The modulus, at least two.

    Returns:
        The residue ``inverse`` with ``value * inverse = 1 (mod modulus)``.

    Raises:
        ValueError: If ``modulus`` is not an integer or is less than two, if
            ``value`` is not an integer, or if ``value`` is not a unit.
    """
    modulus = _integer(modulus, "modulus")
    if modulus < 2:
        raise ValueError(f"modulus must be at least 2, got {modulus}")
    value = _integer(value, "value")
    try:
        return pow(value, -1, modulus)
    except ValueError:
        raise ValueError(f"{value} is not a unit modulo {modulus}") from None


def reciprocal(value: int | Fraction) -> Fraction:
    """Return ``1/value`` in the rationals.

    Args:
        value: A nonzero integer or Fraction.

    Returns:
        The exact reciprocal.

    Raises:
        ValueError: If ``value`` is zero or not an integer or Fraction.
    """
    value = _fraction(value, "value")
    if value == 0:
        raise ValueError("zero has no multiplicative inverse")
    return Fraction(1) / value


def projective_reciprocal(value: int | Fraction | None) -> Fraction | None:
    """Return the reciprocal on the projective line.

    ``None`` denotes the point at infinity. The map sends ``0`` to ``None`` and
    ``None`` to ``0``, and is its own inverse on every other value. The fixed
    points are one and minus one.

    This is a choice of compactification, not a value of ``1/0`` in a field.

    Args:
        value: A rational number, or ``None`` for the point at infinity.

    Returns:
        The projective reciprocal, or ``None`` for infinity.

    Raises:
        ValueError: If ``value`` is not ``None``, an integer, or a Fraction.
    """
    if value is None:
        return Fraction(0)
    value = _fraction(value, "value")
    if value == 0:
        return None
    return Fraction(1) / value


def reciprocal_fixed_points() -> tuple[Fraction, Fraction]:
    """Return the fixed points of the projective reciprocal.

    They solve ``x = 1/x``, equivalently ``x**2 = 1``.

    Returns:
        ``(-1, 1)`` as exact Fractions.
    """
    return (Fraction(-1), Fraction(1))
