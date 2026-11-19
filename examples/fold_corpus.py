"""Recompute the checkable numbers quoted by the Fold corpus.

Run from the repository root:

    python examples/fold_corpus.py

Every row is a print of `model.fold_corpus`, so the table is reproducible
rather than transcribed. The corpus's own rule applies: the exact rows are
computations; the rhymes are not printed as results.
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.fold_corpus import (
    division_collapse_scale,
    doubling_agrees_with_negation,
    doubling_is_bijective,
    horizon_ratio,
    midpoint_scale,
    solid_angle_fraction,
    two_fold_rotation_angle,
    wheel_turns,
)


def main() -> None:
    distance = 2.281

    print("solid angle, d = 2.281 r")
    print("  radius   Omega/4pi")
    for radius in (1.0, 0.5, 0.25):
        print(f"  {radius:>6.3f}   {100.0 * solid_angle_fraction(radius, distance):>8.4f}%")

    print("\nhorizon ratio k* = 2GM/(c^2 R)")
    bodies = [
        ("Earth", 5.972e24, 6.371e6),
        ("Sun (2.0e30)", 2.0e30, 6.957e8),
        ("Sun (1.988e30)", 1.988e30, 6.957e8),
        ("70 kg water", 70.0, 0.2556),
    ]
    for name, mass, radius in bodies:
        print(f"  {name:<16} {horizon_ratio(mass, radius):.4e}")

    print("\nclosure and doubling")
    for modulus in (1, 3, 4, 6, 7, 9):
        print(
            f"  n = {modulus:>2}: bijective {str(doubling_is_bijective(modulus)):<5}"
            f"  doubling = negation {str(doubling_agrees_with_negation(modulus)):<5}"
            f"  8 turns -> {wheel_turns(modulus, 8, 0)}"
        )

    print("\nmap identities")
    print(f"  midpoint scale at k = 1: {midpoint_scale(1.0):.4f}")
    print(f"  division collapse at t = 2: {division_collapse_scale(2.0):.4f}")
    angle = two_fold_rotation_angle((1.0, 0.0), (math.cos(math.pi / 6.0), math.sin(math.pi / 6.0)))
    print(
        f"  two creases 30 degrees apart -> rotation {angle:.6f} rad ({math.degrees(angle):.1f} degrees)"
    )


if __name__ == "__main__":
    main()
