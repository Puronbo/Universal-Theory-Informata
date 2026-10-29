"""Tests for model.cusp."""
import math

from model import bifurcation_value, crease_density, crease_density_proxy, cusp_roots, fold_spectrum, on_cusp


def test_cusp_bifurcation():
    # on cusp: 8a^3 = 27b^2
    a, b = 3.0, 2 * math.sqrt(2)
    assert on_cusp(a, b)
    assert abs(bifurcation_value(a, b)) < 1e-9


def test_cusp_three_real_roots_inside():
    # inside cusp: bifurcation_value > 0 (three real roots)
    a, b = 3.0, 1.0
    assert bifurcation_value(a, b) > 0
    roots = cusp_roots(a, b)
    assert all(abs(r.imag) < 1e-9 for r in roots)


def test_cusp_one_real_root_outside():
    a, b = 1.0, 3.0
    assert bifurcation_value(a, b) < 0
    roots = cusp_roots(a, b)
    real_count = sum(1 for r in roots if abs(r.imag) < 1e-9)
    assert real_count == 1


def test_crease_density_proxy():
    rho = crease_density_proxy(3.0, 1.0, [1.88, -0.35, 5.0], eps=0.05)
    assert 0.0 <= rho <= 1.0
    assert rho > 0.0


def test_cusp_edge_case_p_zero():
    # Test p=0 case (x^3 = b)
    roots = cusp_roots(0.0, 8.0)  # x^3 - 8 = 0 -> x = 2
    # All roots should be real (2, 2*w, 2*w^2)
    assert len(roots) == 3
    # One real root at 2
    real_roots = [r.real for r in roots if abs(r.imag) < 1e-9]
    assert 2.0 in real_roots


def test_bifurcation_value():
    assert bifurcation_value(0, 0) == 0
    assert bifurcation_value(1, 0) == 8
    assert bifurcation_value(0, 1) == -27


def test_crease_density():
    vals = [0.01, 0.02, 0.5, 1.0, -0.03]
    rho = crease_density(vals, eps=0.05)
    assert rho == 3 / 5
    assert crease_density([], 0.05) == 0.0
    assert crease_density([1.0, 2.0], 0.05) == 0.0


def test_fold_spectrum():
    assert fold_spectrum(2.0, 2.0) == "smooth"
    assert fold_spectrum(1.0, 3.0) == "kink"
    assert fold_spectrum(None, 1.0) == "tear"
