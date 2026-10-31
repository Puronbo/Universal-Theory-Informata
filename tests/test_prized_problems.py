"""Tests for model.prized_problems."""

import math

import pytest

from model import collatz_spine_check, collatz_spine_sum, goldbach_check, zeta_partial


def test_collatz_spine():
    for k in range(10):
        assert collatz_spine_check(k)


def test_goldbach():
    for n in [4, 6, 8, 10, 100, 1000]:
        assert goldbach_check(n)


def test_zeta_partial():
    # zeta(2) partial should approach pi^2/6 ~ 1.6449
    val = zeta_partial(2.0, 10000)
    assert abs(val - (math.pi**2 / 6.0)) < 1e-3


def test_collatz_spine_values():
    assert collatz_spine_sum(0) == 1
    assert collatz_spine_sum(1) == 5
    assert collatz_spine_sum(2) == 21


def test_collatz_rejects_negative():
    with pytest.raises(ValueError):
        collatz_spine_sum(-1)


def test_goldbach_rejects_small_and_odd():
    assert not goldbach_check(0)
    assert not goldbach_check(2)
    assert not goldbach_check(3)
    assert not goldbach_check(101)


def test_goldbach_cache_is_reused():
    assert goldbach_check(1000)
    assert goldbach_check(1000)


def test_zeta_partial_validation():
    assert zeta_partial(2.0, 0) == 0.0
    with pytest.raises(ValueError):
        zeta_partial(2.0, -1)
