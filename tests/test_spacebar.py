"""Tests for model.spacebar — every candidate parameter of the press."""

import cmath
import math

import pytest

from model import (
    BARYON_TO_PHOTON_RATIO,
    REDUCED_PLANCK,
    SPEED_OF_LIGHT,
    action_from_proper_time,
    candidate_parameters,
    compton_frequency,
    compton_period,
    is_on_mass_shell,
    mass_shell_residual,
    phase_from_action,
    phase_from_proper_time,
    spacebar_from_proper_time,
    spacebar_from_ticks,
    thermal_weight,
    ticks_from_proper_time,
    wrap_ticks,
)

ELECTRON_MASS = 9.1093837015e-31
PROTON_MASS = 1.67262192369e-27


def test_zero_press_is_identity():
    assert spacebar_from_ticks(0.0) == pytest.approx(1.0 + 0.0j)


def test_quarter_and_half_presses():
    assert spacebar_from_ticks(0.25) == pytest.approx(-1j)
    assert spacebar_from_ticks(0.5) == pytest.approx(-1.0 + 0.0j)
    assert spacebar_from_ticks(0.75) == pytest.approx(1j)


def test_full_press_is_identity():
    for ticks in (1.0, 2.0, -3.0, 7.0):
        assert spacebar_from_ticks(ticks) == pytest.approx(1.0 + 0.0j)


@pytest.mark.parametrize("ticks", [-2.3, -1.0, 0.0, 0.1, 0.5, 12.25])
def test_real_parameter_is_unitary(ticks):
    assert abs(spacebar_from_ticks(ticks)) == pytest.approx(1.0)


def test_press_is_a_homomorphism():
    for left, right in [(0.1, 0.2), (0.3, -0.7), (2.5, 0.25)]:
        assert spacebar_from_ticks(left + right) == pytest.approx(
            spacebar_from_ticks(left) * spacebar_from_ticks(right)
        )


def test_ticks_are_periodic():
    for ticks in (0.0, 0.1, -0.4, 3.7):
        for shift in (-3, -1, 0, 1, 5):
            assert spacebar_from_ticks(ticks + shift) == pytest.approx(spacebar_from_ticks(ticks))


def test_wrap_ticks_lands_in_the_unit_interval():
    for ticks in (-2.3, -0.1, 0.0, 0.25, 0.999, 1.0, 2.5):
        wrapped = wrap_ticks(ticks)
        assert 0.0 <= wrapped < 1.0
        assert spacebar_from_ticks(wrapped) == pytest.approx(spacebar_from_ticks(ticks))


def test_electron_compton_period_and_frequency():
    assert compton_period(ELECTRON_MASS) == pytest.approx(8.0933e-21, rel=1e-3)
    assert compton_frequency(ELECTRON_MASS) == pytest.approx(7.7634e20, rel=1e-3)
    assert compton_period(ELECTRON_MASS) == pytest.approx(
        2.0 * math.pi / compton_frequency(ELECTRON_MASS)
    )


def test_one_compton_period_is_one_full_press():
    period = compton_period(ELECTRON_MASS)
    assert spacebar_from_proper_time(period, ELECTRON_MASS) == pytest.approx(1.0 + 0.0j)


def test_phase_and_ticks_agree():
    tau = 3.0e-21
    phase = phase_from_proper_time(tau, ELECTRON_MASS)
    assert phase == pytest.approx(2.0 * math.pi * ticks_from_proper_time(tau, ELECTRON_MASS))
    assert spacebar_from_proper_time(tau, ELECTRON_MASS) == pytest.approx(cmath.exp(-1j * phase))


def test_action_and_phase_are_consistent():
    tau = 2.0e-21
    action = action_from_proper_time(tau, ELECTRON_MASS)
    assert action == pytest.approx(-ELECTRON_MASS * SPEED_OF_LIGHT**2 * tau)
    assert phase_from_action(action) == pytest.approx(phase_from_proper_time(tau, ELECTRON_MASS))
    assert phase_from_action(action) == pytest.approx(action / -REDUCED_PLANCK)


def test_proper_time_alone_does_not_fix_the_press():
    tau = 1.0e-21
    electron = phase_from_proper_time(tau, ELECTRON_MASS)
    proton = phase_from_proper_time(tau, PROTON_MASS)
    assert electron != pytest.approx(proton)
    assert spacebar_from_proper_time(tau, ELECTRON_MASS) != pytest.approx(
        spacebar_from_proper_time(tau, PROTON_MASS)
    )


def test_tick_count_is_the_scale_free_parameter():
    period = compton_period(ELECTRON_MASS)
    assert ticks_from_proper_time(period, ELECTRON_MASS) == pytest.approx(1.0)
    assert wrap_ticks(ticks_from_proper_time(period, ELECTRON_MASS)) == pytest.approx(
        0.0, abs=1e-12
    )


def test_negative_proper_time_is_the_conjugate_press():
    tau = 2.0e-21
    assert spacebar_from_proper_time(-tau, ELECTRON_MASS) == pytest.approx(
        spacebar_from_proper_time(tau, ELECTRON_MASS).conjugate()
    )


def test_imaginary_parameter_is_a_thermal_weight_not_a_phase():
    beta = 0.5
    weight = thermal_weight(1.0, beta)
    assert weight == pytest.approx(math.exp(-beta))
    assert 0.0 < weight < 1.0
    assert abs(weight) != pytest.approx(1.0)


def test_hot_and_cold_limits_of_the_thermal_weight():
    assert thermal_weight(1.0, 0.0) == pytest.approx(1.0)
    assert thermal_weight(1.0, 10.0) < thermal_weight(1.0, 1.0) < 1.0
    assert thermal_weight(-1.0, 1.0) > 1.0


def test_mass_shell_at_rest():
    energy = ELECTRON_MASS * SPEED_OF_LIGHT**2
    assert mass_shell_residual(energy, 0.0, ELECTRON_MASS) == pytest.approx(0.0, abs=1e-40)
    assert is_on_mass_shell(energy, 0.0, ELECTRON_MASS)


def test_mass_shell_for_a_moving_particle():
    beta = 0.6
    gamma = 1.0 / math.sqrt(1.0 - beta * beta)
    energy = gamma * ELECTRON_MASS * SPEED_OF_LIGHT**2
    momentum = gamma * ELECTRON_MASS * beta * SPEED_OF_LIGHT
    assert mass_shell_residual(energy, momentum, ELECTRON_MASS) == pytest.approx(0.0, abs=1e-40)
    assert is_on_mass_shell(energy, momentum, ELECTRON_MASS)


def test_off_shell_is_rejected():
    energy = 2.0 * ELECTRON_MASS * SPEED_OF_LIGHT**2
    assert not is_on_mass_shell(energy, 0.0, ELECTRON_MASS)


def test_candidate_catalog_covers_every_reading():
    candidates = candidate_parameters()
    names = {candidate.name for candidate in candidates}
    assert names == {
        "proper_time",
        "phase",
        "ticks",
        "affine_parameter",
        "mass",
        "baryon_asymmetry",
        "imaginary_time",
        "complex_time",
        "free_knob",
    }
    statuses = {candidate.status for candidate in candidates}
    assert {
        "physical",
        "fundamental",
        "gauge",
        "fixed",
        "measured",
        "thermal",
        "non-unitary",
        "rejected",
    } <= statuses


def test_baryon_asymmetry_is_one_part_in_a_billion():
    assert 1e-10 < BARYON_TO_PHOTON_RATIO < 1e-9
    assert BARYON_TO_PHOTON_RATIO == pytest.approx(6.1e-10)


@pytest.mark.parametrize("mass", [0.0, -1.0, math.inf, -math.inf, math.nan])
def test_massless_or_invalid_mass_has_no_clock(mass):
    with pytest.raises(ValueError):
        compton_period(mass)
    with pytest.raises(ValueError):
        compton_frequency(mass)
    with pytest.raises(ValueError):
        action_from_proper_time(1.0, mass)
    with pytest.raises(ValueError):
        phase_from_proper_time(1.0, mass)
    with pytest.raises(ValueError):
        ticks_from_proper_time(1.0, mass)
    with pytest.raises(ValueError):
        spacebar_from_proper_time(1.0, mass)


@pytest.mark.parametrize("ticks", [math.inf, -math.inf, math.nan])
def test_ticks_must_be_finite(ticks):
    with pytest.raises(ValueError):
        spacebar_from_ticks(ticks)
    with pytest.raises(ValueError):
        wrap_ticks(ticks)


@pytest.mark.parametrize("tau", [math.inf, -math.inf, math.nan])
def test_proper_time_must_be_finite(tau):
    with pytest.raises(ValueError):
        phase_from_proper_time(tau, ELECTRON_MASS)


@pytest.mark.parametrize("action", [math.inf, -math.inf, math.nan])
def test_action_must_be_finite(action):
    with pytest.raises(ValueError):
        phase_from_action(action)


@pytest.mark.parametrize("beta", [-1.0, math.inf, -math.inf, math.nan])
def test_thermal_beta_must_be_finite_and_nonnegative(beta):
    with pytest.raises(ValueError):
        thermal_weight(1.0, beta)


@pytest.mark.parametrize("energy", [math.inf, -math.inf, math.nan])
def test_thermal_energy_must_be_finite(energy):
    with pytest.raises(ValueError):
        thermal_weight(energy, 1.0)


def test_mass_shell_tolerance_must_be_nonnegative():
    with pytest.raises(ValueError):
        is_on_mass_shell(1.0, 0.0, 1.0, tolerance=-1.0)


def test_mass_shell_rejects_invalid_momentum():
    with pytest.raises(ValueError):
        mass_shell_residual(1.0, math.nan, 1.0)
