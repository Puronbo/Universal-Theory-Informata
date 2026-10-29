"""Tests for model.clock."""
from model import PLANCK_TIME, cp_violation_tilt, entropy_brake, planck_refresh_rate


def test_planck_refresh_rate():
    assert planck_refresh_rate() > 1e43
    assert abs(planck_refresh_rate() - 1.0 / PLANCK_TIME) < 1e-12


def test_cp_violation_tilt():
    assert cp_violation_tilt() == 1e-9


def test_entropy_brake():
    assert entropy_brake(10.0, 3.0) == 7.0
    assert entropy_brake(5.0, 5.0) == 0.0
    assert entropy_brake(3.0, 10.0) == -7.0
