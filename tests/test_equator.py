"""Tests for model.equator."""
from model import gauge_node, imaginary_rotate, scale_midpoint


def test_scale_midpoint():
    m = scale_midpoint(1e-35, 1e26)
    assert abs(m - 10**-4.5) < 1e-5


def test_imaginary_rotate():
    assert imaginary_rotate(1.0) == 1j
    assert imaginary_rotate(2.0) == 2j
    assert imaginary_rotate(0.0) == 0j


def test_gauge_node():
    n = gauge_node((1, 2, 3))
    assert n["location"] == (1, 2, 3)
    assert n["identity"] is None

    n2 = gauge_node("test")
    assert n2["location"] == "test"
    assert n2["identity"] is None
