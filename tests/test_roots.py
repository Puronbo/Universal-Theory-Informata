"""Tests for model.roots."""

import math

import pytest

from model import nth_root


@pytest.mark.parametrize(
    ("x", "n", "expected"),
    [
        (8.0, 3, 2.0),
        (4.0, 2, 2.0),
        (16.0, 4, 2.0),
        (0.25, 2, 0.5),
        (-8.0, 3, -2.0),
        (-32.0, 5, -2.0),
        (0.0, 3, 0.0),
        (0.0, 1, 0.0),
    ],
)
def test_nth_root_values(x, n, expected):
    assert nth_root(x, n) == pytest.approx(expected)


def test_first_root_is_identity():
    for x in [-2.0, 0.5, 0.0, 3.0]:
        assert nth_root(x, 1) == pytest.approx(x)


def test_negative_one_root_is_reciprocal():
    for x in [-2.0, 0.5, 1.0, 2.0, 10.0]:
        assert nth_root(x, -1) == pytest.approx(1.0 / x)


def test_root_power_duality_at_minus_one():
    for x in [0.25, 1.5, 4.0]:
        assert nth_root(x, -1) == pytest.approx(x**-1)


def test_root_and_power_round_trip():
    for x in [0.5, 2.0, 8.0, 100.0]:
        for n in [1, 2, 3, -1, -2, -3]:
            assert nth_root(x, n) ** n == pytest.approx(x)


@pytest.mark.parametrize("n", [0, -1, -2])
def test_zero_rejects_zero_or_negative_index(n):
    with pytest.raises(ValueError):
        nth_root(0.0, n)


@pytest.mark.parametrize("n", [2, 4, -2, -4])
def test_even_root_of_negative_is_rejected(n):
    with pytest.raises(ValueError):
        nth_root(-4.0, n)


@pytest.mark.parametrize("x", [math.inf, -math.inf, math.nan])
def test_non_finite_radicand_is_rejected(x):
    with pytest.raises(ValueError):
        nth_root(x, 3)
