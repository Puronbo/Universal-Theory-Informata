import pytest
from model import mp_discriminant, mp_regime, mp_roots


def test_mp_discriminant():
    assert mp_discriminant(1.0, 1.0, 2.0) == 0.0  # critical
    assert mp_discriminant(1.0, 1.0, 3.0) == 5.0  # overdamped
    assert mp_discriminant(1.0, 1.0, 1.0) == -3.0  # underdamped


def test_mp_regime():
    assert mp_regime(1.0, 1.0, 2.0) == "critical"
    assert mp_regime(1.0, 1.0, 3.0) == "overdamped"
    assert mp_regime(1.0, 1.0, 1.0) == "underdamped"


def test_mp_roots():
    r1, r2 = mp_roots(1.0, 1.0, 2.0)
    assert abs(r1 - 1.0) < 1e-9
    assert abs(r2 - 1.0) < 1e-9
    c1, c2 = mp_roots(1.0, 1.0, 1.0)
    assert isinstance(c1, complex)
