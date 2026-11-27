"""Pi as the nested intersection of Archimedes' rational intervals.

Run from the repository root:

    python examples/pi_intersection.py

Each row is a rigorous rational interval containing pi. The intervals are
nested, and their widths shrink by about a factor of four per doubling. The
infinite intersection is the single point ``{pi}``; no row is pi itself.
"""

from __future__ import annotations

import math
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.pi_intersection import archimedes_intersection, archimedes_interval


def decimal(value: Fraction, places: int = 18) -> str:
    """Format a Fraction as a fixed-point decimal string."""
    getcontext().prec = places + 20
    scaled = Decimal(value.numerator) / Decimal(value.denominator)
    return f"{scaled:.{places}f}"


def main() -> None:
    """Print the Archimedes intervals and the finite intersection."""
    print("== pi as a nested intersection of rational intervals ==")
    print(f"{'d':>2} {'sides':>6} {'lower':>22} {'upper':>22} {'width':>12} {'ratio':>6}")
    previous_width: Fraction | None = None
    for doublings in range(0, 11):
        interval = archimedes_interval(doublings)
        ratio = "" if previous_width is None else f"{float(previous_width / interval.width):.2f}"
        print(
            f"{doublings:>2} {interval.sides:>6} "
            f"{decimal(interval.lower, 18):>22} {decimal(interval.upper, 18):>22} "
            f"{float(interval.width):>12.3e} {ratio:>6}"
        )
        previous_width = interval.width
    print()

    family = archimedes_intersection(10)
    print(f"finite intersection after {len(family)} intervals:")
    print(f"  lower = {decimal(family.lower, 24)}")
    print(f"  upper = {decimal(family.upper, 24)}")
    print(f"  width = {decimal(family.width, 24)}")
    print(f"  sides = {family.sides}")
    print()
    print(f"pi reference (float): {math.pi:.15f}")
    print("The infinite intersection is {pi}; every finite row is rational.")


if __name__ == "__main__":
    main()
