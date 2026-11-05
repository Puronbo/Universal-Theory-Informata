"""Tests for model.antithesis."""

import math

import pytest

from model import (
    LogConjugacy,
    OrbitComparison,
    RegimeComparison,
    compare_log_conjugacy,
    compare_orbits,
    compare_regimes,
    contract,
    contract_orbit,
    entropy,
    exp_coordinate,
    information_loss,
    inversion_orbit,
    is_cyclic,
    log_coordinate,
    log_orbit,
    lyapunov_exponent,
    nilpotent_apply,
    nilpotent_orbit,
    orbit_period,
    translation,
    translation_orbit,
)


def test_contract_step():
    assert contract(1.0) == 0.5
    assert contract(0.5, rate=0.5) == 0.25
    assert contract(-2.0) == -1.0
    assert contract(3.0, rate=0.25) == 0.75


def test_contract_orbit():
    assert contract_orbit(2.0, 3) == pytest.approx((2.0, 1.0, 0.5, 0.25))
    assert contract_orbit(2.0, 0) == pytest.approx((2.0,))


@pytest.mark.parametrize("rate", [0.0, 1.0, -0.1, 1.1, math.inf, math.nan])
def test_contract_rejects_bad_rate(rate):
    with pytest.raises(ValueError):
        contract(1.0, rate)


@pytest.mark.parametrize("x", [math.inf, -math.inf, math.nan])
def test_contract_rejects_non_finite(x):
    with pytest.raises(ValueError):
        contract(x)


def test_orbits_reject_negative_steps():
    with pytest.raises(ValueError):
        contract_orbit(1.0, -1)
    with pytest.raises(ValueError):
        inversion_orbit(1.0, -1)
    with pytest.raises(ValueError):
        compare_orbits(1.0, -1)


def test_inversion_orbit_alternates():
    assert inversion_orbit(2.0, 3) == pytest.approx((2.0, 0.5, 2.0, 0.5))
    assert inversion_orbit(1.0, 3) == pytest.approx((1.0, 1.0, 1.0, 1.0))
    assert inversion_orbit(2.0, 0) == pytest.approx((2.0,))


@pytest.mark.parametrize("x", [0.0, -1.0])
def test_inversion_orbit_rejects_bad_scale(x):
    with pytest.raises(ValueError):
        inversion_orbit(x, 1)


def test_entropy_is_monotone_under_contraction():
    for x in [0.25, 0.5, 1.0, 2.0, 4.0]:
        assert entropy(contract(x)) > entropy(x)


def test_entropy_values():
    assert entropy(1.0) == pytest.approx(0.0)
    assert entropy(0.5) == pytest.approx(math.log(2.0))
    assert entropy(0.25) == pytest.approx(math.log(4.0))


@pytest.mark.parametrize("x", [0.0, -1.0, math.inf, math.nan])
def test_entropy_rejects_non_positive_or_non_finite(x):
    with pytest.raises(ValueError):
        entropy(x)


def test_compare_orbits():
    comparison = compare_orbits(2.0, 3)
    assert isinstance(comparison, OrbitComparison)
    assert comparison.initial == 2.0
    assert comparison.involution == pytest.approx((2.0, 0.5, 2.0, 0.5))
    assert comparison.contraction == pytest.approx((2.0, 1.0, 0.5, 0.25))
    assert comparison.contraction[-1] < comparison.contraction[0]
    assert comparison.involution[-1] == pytest.approx(comparison.involution[1])


def test_contraction_never_returns_for_positive_start():
    orbit = contract_orbit(3.0, 8)
    assert all(value > 0.0 for value in orbit)
    assert orbit[-1] < orbit[0] / 100
    assert all(value != orbit[0] for value in orbit[1:])


def test_translation_orbit():
    assert translation_orbit(0.0, 3) == (0.0, 1.0, 2.0, 3.0)
    assert translation_orbit(0.0, 3, shift=-1.0) == (0.0, -1.0, -2.0, -3.0)
    assert translation_orbit(2.0, 0) == (2.0,)


@pytest.mark.parametrize("shift", [0.0, math.inf, -math.inf, math.nan])
def test_translation_rejects_bad_shift(shift):
    with pytest.raises(ValueError):
        translation(0.0, shift)
    with pytest.raises(ValueError):
        translation_orbit(0.0, 2, shift)


def test_nilpotent_collapses():
    assert nilpotent_apply(3.0, 4.0) == (0.0, 3.0)
    assert nilpotent_apply(0.0, 3.0) == (0.0, 0.0)
    assert nilpotent_orbit(3.0, 4.0, 3) == (
        (3.0, 4.0),
        (0.0, 3.0),
        (0.0, 0.0),
        (0.0, 0.0),
    )


def test_nilpotent_square_is_zero():
    once = nilpotent_apply(3.0, 4.0)
    assert nilpotent_apply(*once) == (0.0, 0.0)


@pytest.mark.parametrize("bad", [math.inf, -math.inf, math.nan])
def test_nilpotent_rejects_non_finite(bad):
    with pytest.raises(ValueError):
        nilpotent_apply(bad, 1.0)
    with pytest.raises(ValueError):
        nilpotent_apply(1.0, bad)
    with pytest.raises(ValueError):
        nilpotent_orbit(bad, 1.0, 1)


def test_lyapunov_exponent_is_negative_for_contraction():
    assert lyapunov_exponent(0.5) == pytest.approx(math.log(0.5))
    assert lyapunov_exponent(0.5) < 0.0


@pytest.mark.parametrize("rate", [0.0, 1.0, -0.5, math.inf, math.nan])
def test_lyapunov_exponent_rejects_bad_rate(rate):
    with pytest.raises(ValueError):
        lyapunov_exponent(rate)


def test_information_loss_matches_entropy_difference():
    x, steps, rate = 3.0, 5, 0.5
    assert information_loss(x, steps, rate) == pytest.approx(
        entropy(contract_orbit(x, steps, rate)[-1]) - entropy(x)
    )
    assert information_loss(x, steps, rate) > 0.0


@pytest.mark.parametrize("x", [0.0, -1.0, math.inf, math.nan])
def test_information_loss_rejects_bad_x(x):
    with pytest.raises(ValueError):
        information_loss(x, 2)


def test_orbit_period():
    assert orbit_period((1.0, 1.0, 1.0)) == 1
    assert orbit_period((2.0, 0.5, 2.0, 0.5)) == 2
    assert orbit_period((2.0, 1.0, 0.5, 0.25)) is None
    assert orbit_period((1.0,)) is None


def test_is_cyclic():
    assert is_cyclic((2.0, 0.5, 2.0))
    assert not is_cyclic((2.0, 1.0, 0.5))


def test_compare_regimes():
    comparison = compare_regimes(2.0, 3)
    assert isinstance(comparison, RegimeComparison)
    assert comparison.initial == 2.0
    assert comparison.involution == pytest.approx((2.0, 0.5, 2.0, 0.5))
    assert comparison.contraction == pytest.approx((2.0, 1.0, 0.5, 0.25))
    assert comparison.translation == pytest.approx((2.0, 3.0, 4.0, 5.0))
    assert orbit_period(comparison.involution) == 2
    assert orbit_period(comparison.contraction) is None
    assert orbit_period(comparison.translation) is None


def test_log_coordinate():
    assert log_coordinate(1.0) == pytest.approx(0.0)
    assert log_coordinate(math.e) == pytest.approx(1.0)


def test_exp_coordinate_round_trip():
    for x in [0.25, 1.0, 2.0, 10.0]:
        assert exp_coordinate(log_coordinate(x)) == pytest.approx(x)


@pytest.mark.parametrize("x", [0.0, -1.0, math.inf, math.nan])
def test_log_coordinate_rejects_bad_scale(x):
    with pytest.raises(ValueError):
        log_coordinate(x)


@pytest.mark.parametrize("t", [math.inf, -math.inf, math.nan])
def test_exp_coordinate_rejects_non_finite(t):
    with pytest.raises(ValueError):
        exp_coordinate(t)


def test_exp_coordinate_rejects_overflow():
    with pytest.raises(ValueError):
        exp_coordinate(1000.0)


def test_log_orbit_is_translation():
    rate = 0.5
    logged = log_orbit(2.0, 3, rate)
    assert logged == pytest.approx(translation_orbit(log_coordinate(2.0), 3, math.log(rate)))
    assert logged == pytest.approx(tuple(math.log(value) for value in contract_orbit(2.0, 3, rate)))


def test_log_conjugacy_dataclass():
    comparison = compare_log_conjugacy(2.0, 3)
    assert isinstance(comparison, LogConjugacy)
    assert comparison.initial == 2.0
    assert comparison.log_orbit == pytest.approx(comparison.translation)


def test_log_orbit_rejects_bad_input():
    with pytest.raises(ValueError):
        log_orbit(0.0, 1)
    with pytest.raises(ValueError):
        log_orbit(2.0, -1)
    with pytest.raises(ValueError):
        log_orbit(2.0, 1, 1.0)
