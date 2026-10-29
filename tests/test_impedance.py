"""Tests for model.impedance."""
import math

from model import (
    PLANCK_TIME,
    grokking_delay,
    impedance_series,
    planck_refresh_rate,
    resonance_w0,
    schwinger_mass_gap,
    thirring_gn_mass_gap,
)


def test_impedance_resonance():
    R, L, C = 2.0, 1.0, 1.0
    w0 = resonance_w0(L, C)
    Z = impedance_series(R, L, C, w0)
    assert abs(Z.imag) < 1e-9
    assert abs(Z.real - R) < 1e-9


def test_schwinger_mass_gap():
    assert abs(schwinger_mass_gap(math.e) - math.e / math.sqrt(math.pi)) < 1e-12


def test_thirring_gn():
    M = thirring_gn_mass_gap(1.0, 1.0, 2.0)
    assert M > 0
    assert abs(M - 1.0 / math.sinh(2 * math.pi)) < 1e-9


def test_grokking_delay():
    assert abs(grokking_delay(2.0, 4.0, 2.0) - 0.5 * math.log(2.0)) < 1e-12


def test_planck_refresh_rate():
    assert planck_refresh_rate() > 1e43
    assert abs(planck_refresh_rate() - 1.0 / PLANCK_TIME) < 1e-12
