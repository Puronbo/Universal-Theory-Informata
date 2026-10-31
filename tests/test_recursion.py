"""Tests for model.recursion."""

import math
import random

from model import canvas_energy, erosion_step, iterate, purge_derivative, purge_if_flat


def test_iterate_fixed_point():
    x, steps, conv, _ = iterate(lambda x: math.cos(x), 1.0)
    assert conv
    assert abs(x - 0.7390851332151607) < 1e-9


def test_iterate_no_converge_finite():
    x, steps, conv, _ = iterate(lambda x: x + 1.0, 0.0, n=5)
    assert not conv
    assert steps == 5


def test_iterate_cycle_detection():
    # f(x)=1-x cycles with period 2
    x, steps, conv, cyc = iterate(lambda v: 1.0 - v, 0.0, detect_cycle=True)
    assert not conv
    assert cyc == 2


def test_purge_flat():
    assert purge_if_flat([1.0, 1.0])
    assert not purge_if_flat([1.0, 2.0])


def test_purge_derivative():
    assert purge_derivative([1.0, 1.0, 1.0])
    assert not purge_derivative([1.0, 2.0, 3.0])


def test_canvas_energy():
    assert canvas_energy(2.0) == 0.5
    assert canvas_energy(1.0) == 1.0
    try:
        canvas_energy(0.0)
        raise AssertionError()
    except ValueError:
        pass
    try:
        canvas_energy(-1.0)
        raise AssertionError()
    except ValueError:
        pass


def test_erosion_preserves_net_zero():
    s = [1, -1, 1, -1, 0]
    before = sum(s)
    out = erosion_step(s, pairs=2)
    assert sum(out) == before
    assert out.count(1) == 0 and out.count(-1) == 0


def test_erosion_partial():
    s = [1, 1, -1, 0]
    out = erosion_step(s, pairs=5)  # only one opposing pair
    assert out.count(1) == 1
    assert out.count(-1) == 0
    assert sum(out) == sum(s)


def test_erosion_empty():
    assert erosion_step([]) == []
    assert erosion_step([0, 0, 0]) == [0, 0, 0]


def test_prop_erosion_preserves_sum():
    random.seed(0)
    for _ in range(200):
        n = random.randint(1, 12)
        states = [random.choice([-1, 0, 1]) for _ in range(n)]
        before = sum(states)
        out = erosion_step(states, pairs=random.randint(1, 5))
        assert sum(out) == before, (states, out)
