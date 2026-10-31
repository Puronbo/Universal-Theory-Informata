"""Tests for model.dark_energy."""

from model import (
    DESI_REFERENCE,
    check_predictions,
    delta_derivative_present,
    delta_norm,
    delta_norm_uncertainty,
    rho_lambda_ratio,
    w_cpl,
)


def test_w_cpl_lambda():
    # Lambda: w0=-1, wa=0 -> w=-1 everywhere
    assert abs(w_cpl(0.3, -1.0, 0.0) + 1.0) < 1e-12
    assert abs(w_cpl(1.0, -1.0, 0.0) + 1.0) < 1e-12


def test_rho_lambda_lambda_constant():
    # For Lambda, rho(z)/rho0 = 1 for all z
    for z in [0.0, 0.5, 1.0, 2.0]:
        assert abs(rho_lambda_ratio(z, -1.0, 0.0) - 1.0) < 1e-9


def test_check_predictions_quintom():
    r = check_predictions(-0.75, -0.87, 0.058, 0.25)
    assert r["quintom_B_quadrant"] is True
    assert r["P3_phantom_sign_flip_needed"] is False


def test_check_predictions_phantom():
    r = check_predictions(-1.2, -0.5, 0.1, 0.2)
    assert r["P3_phantom_sign_flip_needed"] is True


def test_desi_reference_ranges():
    lo, hi = DESI_REFERENCE["w0_range"]
    assert lo < hi
    lo2, hi2 = DESI_REFERENCE["wa_range"]
    assert lo2 < hi2 < 0


def test_delta_norm_present_zero():
    assert abs(delta_norm(0.0, -0.75, -0.87)) < 1e-12


def test_delta_norm_past_positive_quintom():
    assert delta_norm(1.0, -0.75, -0.87) > 0.0


def test_delta_derivative_present_positive():
    assert delta_derivative_present(-0.75, -0.87) > 0.0


def test_delta_norm_uncertainty():
    base, unc = delta_norm_uncertainty(-0.75, -0.87, 0.058, 0.25)
    assert unc >= 0
    assert base == delta_norm(1.0, -0.75, -0.87)


def test_prop_delta_zero_at_present():
    for w0, wa in [(-1.0, 0.0), (-0.75, -0.87), (-0.5, 0.5)]:
        assert abs(delta_norm(0.0, w0, wa)) < 1e-12
