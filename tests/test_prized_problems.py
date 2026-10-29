"""Tests for model.prized_problems."""
import math

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
