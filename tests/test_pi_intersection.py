"""Tests for pi as a nested Archimedes intersection."""

from __future__ import annotations

import math
from fractions import Fraction

import pytest

from model.pi_intersection import (
    PiIntersection,
    PiInterval,
    _sqrt_bounds,
    archimedes_intersection,
    archimedes_interval,
    archimedes_intervals,
)


def test_hexagon_bounds() -> None:
    interval = archimedes_interval(0)
    assert interval.sides == 6
    assert interval.lower == 3
    assert 3.4641 < float(interval.upper) < 3.4642


def test_twelve_gon_bounds() -> None:
    interval = archimedes_interval(1)
    assert interval.sides == 12
    assert 3.1058 < float(interval.lower) < 3.1059
    assert 3.2153 < float(interval.upper) < 3.2155


def test_every_interval_contains_pi() -> None:
    for interval in archimedes_intervals(8):
        assert float(interval.lower) < math.pi < float(interval.upper)


def test_intervals_are_nested() -> None:
    intervals = archimedes_intervals(8)
    for earlier, later in zip(intervals[:-1], intervals[1:], strict=True):
        assert later.lower >= earlier.lower
        assert later.upper <= earlier.upper


def test_widths_strictly_decrease() -> None:
    intervals = archimedes_intervals(8)
    for earlier, later in zip(intervals[:-1], intervals[1:], strict=True):
        assert later.width < earlier.width


def test_side_counts_double_from_six() -> None:
    assert [interval.sides for interval in archimedes_intervals(4)] == [6, 12, 24, 48, 96]


def test_interval_properties() -> None:
    interval = PiInterval(6, Fraction(3), Fraction(4))
    assert interval.width == 1
    assert interval.midpoint == Fraction(7, 2)
    assert interval.contains(3)
    assert interval.contains(Fraction(7, 2))
    assert not interval.contains(4 + Fraction(1, 10))


def test_interval_rejects_bad_values() -> None:
    with pytest.raises(ValueError, match="sides"):
        PiInterval(2, Fraction(3), Fraction(4))
    with pytest.raises(ValueError, match="lower"):
        PiInterval(6, Fraction(4), Fraction(3))


def test_intersection_properties() -> None:
    family = archimedes_intersection(4)
    assert len(family) == 5
    assert family.sides == 96
    assert family.lower == max(interval.lower for interval in family.intervals)
    assert family.upper == min(interval.upper for interval in family.intervals)
    assert family.width == family.upper - family.lower
    assert family.width == family.intervals[-1].width


def test_intersection_rejects_empty_family() -> None:
    with pytest.raises(ValueError, match="empty"):
        PiIntersection(())


def test_intersection_rejects_non_nested_family() -> None:
    outer = PiInterval(6, Fraction(3), Fraction(4))
    wider = PiInterval(12, Fraction(2), Fraction(5))
    with pytest.raises(ValueError, match="nested"):
        PiIntersection((outer, wider))


def test_sqrt_bounds_are_outward() -> None:
    lower, upper = _sqrt_bounds(Fraction(2), 20)
    assert lower * lower <= 2 <= upper * upper
    assert upper - lower <= Fraction(1, 10**20)


def test_sqrt_bounds_handle_zero_and_exact_squares() -> None:
    assert _sqrt_bounds(Fraction(0), 5) == (Fraction(0), Fraction(0))
    assert _sqrt_bounds(Fraction(4), 5) == (Fraction(2), Fraction(2))


def test_sqrt_bounds_reject_negative_values() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        _sqrt_bounds(Fraction(-1), 5)


@pytest.mark.parametrize(
    "call",
    [
        lambda: archimedes_intervals(-1),
        lambda: archimedes_intervals(1, 0),
        lambda: archimedes_intervals(True),
        lambda: archimedes_intervals(1, 1.0),
        lambda: archimedes_interval(-1),
        lambda: archimedes_intersection(-1),
    ],
)
def test_rejects_invalid_indices(call: object) -> None:
    with pytest.raises(ValueError):
        call()  # type: ignore[operator]
