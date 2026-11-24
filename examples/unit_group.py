"""The multiplicative group, its identity, and the projective pole.

Run from the repository root:

    python examples/unit_group.py

The printed tables are exact: integer divisibility, the unit groups of
``Z/nZ``, the inverses, and the reciprocal involution on the projective line.
The point at infinity is printed as ``inf``. The interpretive readings are not
printed; they are in ``ZERO_AND_HOLES.md``.
"""

from __future__ import annotations

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.fold import fold
from model.unit_group import (
    divides,
    is_field_mod,
    projective_reciprocal,
    reciprocal_fixed_points,
    unit_inverse,
    units_mod,
)


def show(value: Fraction | None) -> str:
    """Format a projective rational, using ``inf`` for the point at infinity."""
    return "inf" if value is None else str(value)


def main() -> None:
    """Print the divisibility, unit-group, inverse, and reciprocal tables."""
    integers = list(range(-10, 11))
    print("== direction: one divides everything, only units divide one ==")
    print(f"divisors of 1 in Z: {[value for value in integers if divides(value, 1)]}")
    print(f"1 divides n for n in [-10, 10]: {sum(divides(1, value) for value in integers)}/21")
    print()

    print("== unit groups of Z/nZ ==")
    print(f"{'n':>2}  {'units':<20} {'count':>5} {'nonzero':>7} {'field':>6}")
    for modulus in range(2, 11):
        units = units_mod(modulus)
        listed = "(" + ",".join(str(value) for value in units) + ")"
        print(
            f"{modulus:>2}  {listed:<20} {len(units):>5} "
            f"{modulus - 1:>7} {str(is_field_mod(modulus)):>6}"
        )
    print()

    print("== inverses modulo 7 ==")
    print(f"{'x':>2}  {'inverse':>7}  {'x*inverse mod 7':>15}")
    for value in range(7):
        if value == 0:
            print(f"{value:>2}  {'-':>7}  {'not a unit':>15}")
            continue
        inverse = unit_inverse(value, 7)
        print(f"{value:>2}  {inverse:>7}  {value * inverse % 7:>15}")
    print()

    print("== projective reciprocal: 0 <-> inf ==")
    print(f"{'x':>5}  {'1/x':>5}")
    for value in (None, 0, 2, Fraction(1, 2), 1, -1):
        print(f"{show(value):>5}  {show(projective_reciprocal(value)):>5}")
    print()

    fixed = reciprocal_fixed_points()
    print(f"fixed points of x -> 1/x: {', '.join(show(value) for value in fixed)}")
    print(f"fold(2) = fold(1/2) = {fold(2.0):.1f}")
    print(f"fold(1) = {fold(1.0):.1f}")
    print()
    print("The exact object is Q^x, the nonzero rationals, with identity 1.")
    print("Zero is the excluded element; the point at infinity is the boundary,")
    print("not nothing.")


if __name__ == "__main__":
    main()
