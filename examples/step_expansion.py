"""Expand the one-step rule: divide by the step ``n / n**n``.

Run from the repository root:

    python examples/step_expansion.py

The printed table is exact up to display rounding: the step, its reciprocal,
the multiplicative expansion ``A_n``, its collapse ``B_n = 1/A_n``, and the
additive partial sum ``S_n``. The final block prints a rigorous decimal
enclosure of the additive limit at ``n = 20``.
"""

from __future__ import annotations

import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.step_expansion import (
    additive_expansion,
    additive_interval,
    divide_by_step,
    expansion_term,
    log_expansion,
    multiplicative_collapse,
    multiplicative_expansion,
    step,
    tail_bound,
)


def decimal(value: Fraction, places: int = 18) -> str:
    """Format a Fraction as a fixed-point decimal string."""
    getcontext().prec = places + 10
    scaled = Decimal(value.numerator) / Decimal(value.denominator)
    return f"{scaled:.{places}f}"


def main() -> None:
    """Print the step, product, collapse, and sum tables."""
    print("== one step: divide by s_n = n / n^n = 1 / n^(n-1) ==")
    print(f"{'n':>2} {'s_n':>12} {'1/s_n':>12} {'A_n':>26} " f"{'B_n':>12} {'S_n':>18}")
    for n in range(1, 11):
        a_n = multiplicative_expansion(n)
        b_n = multiplicative_collapse(n)
        s_n = additive_expansion(n)
        print(
            f"{n:>2} {str(step(n)):>12} {expansion_term(n):>12} {a_n:>26} "
            f"{float(b_n):>12.3e} {float(s_n):>18.15f}"
        )
    print()

    carried = Fraction(1)
    for n in range(1, 6):
        carried = divide_by_step(carried, n)
    print(f"one-step carry: divide 1 by s_1 ... s_5 -> {carried}")
    print(f"A_5 from the closed form: {multiplicative_expansion(5)}")
    print()

    print("== exact additive enclosure at n = 20 ==")
    lower, upper = additive_interval(20)
    print(f"lower  {decimal(lower, 30)}")
    print(f"upper  {decimal(upper, 30)}")
    print(f"tail   {decimal(tail_bound(20), 30)}")
    print(f"width  {decimal(upper - lower, 30)}")
    print()

    print("== one-step logarithm: log(A_n) - log(A_(n-1)) = (n-1) log(n) ==")
    for n in (2, 3, 5, 10, 20):
        delta = log_expansion(n) - log_expansion(n - 1)
        print(f"n={n:>2}  log(A_n)={log_expansion(n):>12.6f}  step log={delta:>10.6f}")
    print()
    print("The product is exact integer arithmetic. The sum is enclosed,")
    print("not identified; the integral representation is a reformulation.")
    print("The zero-th step is the excluded pole, so the expansion starts at 1.")


if __name__ == "__main__":
    main()
