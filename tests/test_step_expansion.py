"""Tests for the one-step step expansion."""

from __future__ import annotations

import math
from fractions import Fraction

import pytest

from model.step_expansion import (
    additive_expansion,
    additive_interval,
    divide_by_step,
    expansion_term,
    hyperfactorial,
    log_expansion,
    multiplicative_collapse,
    multiplicative_expansion,
    step,
    tail_bound,
)


def test_step_values() -> None:
    assert step(1) == 1
    assert step(2) == Fraction(1, 2)
    assert step(3) == Fraction(1, 9)
    assert step(4) == Fraction(1, 64)
    assert step(5) == Fraction(1, 625)


def test_step_is_the_reciprocal_of_the_expansion_term() -> None:
    for n in range(1, 11):
        assert step(n) * expansion_term(n) == 1


def test_expansion_term_values() -> None:
    assert [expansion_term(n) for n in range(1, 6)] == [1, 2, 9, 64, 625]


def test_divide_by_step_carries_the_recurrence() -> None:
    value = Fraction(1)
    for n in range(1, 11):
        value = divide_by_step(value, n)
        assert value == multiplicative_expansion(n)


def test_divide_by_step_accepts_integers_and_fractions() -> None:
    assert divide_by_step(6, 2) == 12
    assert divide_by_step(Fraction(3, 2), 3) == Fraction(27, 2)
    assert divide_by_step(0, 5) == 0
    assert divide_by_step(-4, 2) == -8


def test_multiplicative_expansion_values() -> None:
    assert [multiplicative_expansion(n) for n in range(0, 6)] == [1, 1, 2, 18, 1152, 720000]


def test_multiplicative_expansion_is_hyperfactorial_over_factorial() -> None:
    for n in range(0, 11):
        assert multiplicative_expansion(n) == hyperfactorial(n) // math.factorial(n)


def test_multiplicative_expansion_recurrence() -> None:
    for n in range(1, 11):
        expected = multiplicative_expansion(n - 1) * expansion_term(n)
        assert multiplicative_expansion(n) == expected


def test_hyperfactorial_values() -> None:
    assert [hyperfactorial(n) for n in range(0, 5)] == [1, 1, 4, 108, 27648]


def test_multiplicative_collapse_is_the_reciprocal() -> None:
    for n in range(0, 11):
        assert multiplicative_collapse(n) * multiplicative_expansion(n) == 1


def test_multiplicative_collapse_recurrence() -> None:
    for n in range(1, 11):
        assert multiplicative_collapse(n) == multiplicative_collapse(n - 1) * step(n)


def test_additive_expansion_values() -> None:
    assert additive_expansion(0) == 0
    assert additive_expansion(1) == 1
    assert additive_expansion(2) == Fraction(3, 2)
    assert additive_expansion(3) == Fraction(29, 18)
    assert additive_expansion(4) == Fraction(937, 576)


def test_additive_expansion_recurrence() -> None:
    for n in range(1, 11):
        assert additive_expansion(n) == additive_expansion(n - 1) + step(n)


def test_tail_bound_values() -> None:
    assert tail_bound(1) == 1
    assert tail_bound(2) == Fraction(1, 6)
    assert tail_bound(3) == Fraction(1, 48)


def test_tail_bound_dominates_every_finite_tail() -> None:
    for n in (1, 2, 5, 10):
        finite = sum((step(k) for k in range(n + 1, 31)), Fraction(0))
        assert finite < tail_bound(n)


def test_additive_interval_encloses_the_next_partial_sum() -> None:
    for n in range(1, 10):
        lower, upper = additive_interval(n)
        assert lower == additive_expansion(n)
        assert upper == lower + tail_bound(n)
        assert lower < additive_expansion(n + 1) < upper


def test_additive_interval_narrows() -> None:
    widths = [additive_interval(n)[1] - additive_interval(n)[0] for n in range(1, 10)]
    assert all(later < earlier for earlier, later in zip(widths[:-1], widths[1:], strict=True))


def test_additive_interval_at_twenty_is_tiny() -> None:
    lower, upper = additive_interval(20)
    assert upper - lower == tail_bound(20)
    assert upper - lower < Fraction(1, 10**25)


def test_log_expansion_matches_the_logarithm() -> None:
    assert log_expansion(0) == 0.0
    for n in range(1, 21):
        assert log_expansion(n) == pytest.approx(math.log(multiplicative_expansion(n)))


def test_log_expansion_adds_the_step_logarithm() -> None:
    for n in range(2, 21):
        difference = log_expansion(n) - log_expansion(n - 1)
        assert difference == pytest.approx((n - 1) * math.log(n))


@pytest.mark.parametrize(
    "call",
    [
        lambda: step(0),
        lambda: divide_by_step(1, 0),
        lambda: expansion_term(0),
        lambda: hyperfactorial(-1),
        lambda: multiplicative_expansion(-1),
        lambda: multiplicative_collapse(-1),
        lambda: additive_expansion(-1),
        lambda: tail_bound(0),
        lambda: additive_interval(0),
        lambda: log_expansion(-1),
    ],
)
def test_rejects_indices_below_the_minimum(call: object) -> None:
    with pytest.raises(ValueError, match="at least"):
        call()  # type: ignore[operator]


@pytest.mark.parametrize(
    "value",
    [True, 1.0, "1", None],
)
def test_divide_by_step_rejects_non_rational_values(value: object) -> None:
    with pytest.raises(ValueError, match="value must be"):
        divide_by_step(value, 2)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "call",
    [
        lambda: step(True),
        lambda: step(1.0),
        lambda: expansion_term(1.0),
        lambda: hyperfactorial(True),
        lambda: multiplicative_expansion(1.0),
        lambda: additive_expansion(False),
        lambda: tail_bound(1.0),
        lambda: log_expansion(True),
    ],
)
def test_rejects_non_integers(call: object) -> None:
    with pytest.raises(ValueError, match="must be an integer"):
        call()  # type: ignore[operator]
