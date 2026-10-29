"""Tests for model.rolling_fold."""
import random

from model import roll_convert, roll_orientation


def test_roll_orientation():
    assert roll_orientation(0) == "photon"
    assert roll_orientation(90) == "dark_energy"
    assert roll_orientation(180) == "photon"
    assert roll_orientation(270) == "dark_energy"
    assert roll_orientation(45) == "dark_energy"
    assert roll_orientation(135) == "photon"


def test_roll_convert_conservation():
    p, d = roll_convert(0.3, 1.0)
    assert abs(p + d - 1.0) < 1e-12
    assert p == 0.3 and d == 0.7


def test_roll_convert_clamping():
    # Clamps to [0, total]
    p, d = roll_convert(1.5, 1.0)
    assert p == 1.0 and d == 0.0
    p, d = roll_convert(-0.5, 1.0)
    assert p == 0.0 and d == 1.0


def test_prop_roll_convert_conservation():
    random.seed(2)
    for _ in range(100):
        cd = random.random()
        total = random.uniform(0.5, 2.0)
        p, d = roll_convert(cd, total)
        assert abs(p + d - total) < 1e-9
