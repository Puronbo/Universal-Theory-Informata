"""Tests for model.pressing — the five toy checks."""

import math

import pytest

from model import (
    commutator_norm_two_point,
    conditional_state,
    connes_distance_two_point,
    desitter_closed_scale_factor,
    desitter_conformal_time_range,
    desitter_proper_time,
    gps_factory_detune,
    gps_gravitational_drift_us_per_day,
    gps_net_drift_us_per_day,
    gps_velocity_drift_us_per_day,
    modular_flow_bloch,
    modular_frequency,
    modular_hamiltonian,
    page_wootters_state,
    unruh_temperature,
)

# Page-Wootters -------------------------------------------------------------


def test_page_wootters_state_is_normalized():
    state = page_wootters_state([0.0, math.pi / 2.0, math.pi])
    assert sum(abs(amplitude) ** 2 for amplitude in state) == pytest.approx(1.0)


def test_conditional_states_follow_the_clock():
    state = page_wootters_state([0.0, math.pi / 2.0, math.pi])
    assert conditional_state(state, 0) == pytest.approx((1.0 + 0.0j, 0.0 + 0.0j))
    assert conditional_state(state, 1) == pytest.approx(
        (1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0))
    )
    assert conditional_state(state, 2) == pytest.approx((0.0 + 0.0j, 1.0 + 0.0j))


def test_global_state_is_fixed_while_conditionals_evolve():
    state = page_wootters_state([0.0, 0.5, 1.0])
    snapshot = tuple(state)
    conditionals = [conditional_state(state, index) for index in range(3)]
    assert conditionals[0] != pytest.approx(conditionals[1])
    assert conditionals[1] != pytest.approx(conditionals[2])
    assert state == snapshot


def test_conditional_state_rejects_bad_dimensions_and_indices():
    state = page_wootters_state([0.0, 0.5])
    with pytest.raises(ValueError):
        conditional_state(state, 0, system_dimension=3)
    with pytest.raises(ValueError):
        conditional_state(state, 2)
    with pytest.raises(ValueError):
        conditional_state(state, -1)
    with pytest.raises(ValueError):
        conditional_state(state, 0, system_dimension=0)


def test_conditional_state_rejects_a_zero_slice():
    state = (1.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j)
    with pytest.raises(ValueError):
        conditional_state(state, 1)


def test_conditional_state_rejects_non_finite_amplitudes():
    state = (math.nan + 0.0j, 0.0 + 0.0j, 1.0 + 0.0j, 0.0 + 0.0j)
    with pytest.raises(ValueError):
        conditional_state(state, 0)


@pytest.mark.parametrize("angles", [(), [math.inf], [math.nan]])
def test_page_wootters_rejects_bad_angles(angles):
    with pytest.raises(ValueError):
        page_wootters_state(angles)


# GPS -----------------------------------------------------------------------


def test_gps_drift_components():
    gravitational = gps_gravitational_drift_us_per_day()
    velocity = gps_velocity_drift_us_per_day()
    net = gps_net_drift_us_per_day()
    assert gravitational == pytest.approx(45.7, rel=2e-2)
    assert velocity == pytest.approx(-7.2, rel=2e-2)
    assert net == pytest.approx(38.5, rel=2e-2)
    assert net == pytest.approx(gravitational + velocity)


def test_gps_factory_detune():
    assert gps_factory_detune() == pytest.approx(10.22999999543e6, rel=1e-6)


# de Sitter ----------------------------------------------------------------


def test_desitter_conformal_strip_is_finite():
    low, high = desitter_conformal_time_range()
    assert low == pytest.approx(-math.pi / 2.0)
    assert high == pytest.approx(math.pi / 2.0)


def test_desitter_proper_time_from_the_strip():
    hubble = 0.5
    assert desitter_proper_time(0.0, hubble) == pytest.approx(0.0)
    assert desitter_proper_time(math.pi / 4.0, hubble) == pytest.approx(math.asinh(1.0) / hubble)
    assert desitter_proper_time(-0.3, hubble) == pytest.approx(-desitter_proper_time(0.3, hubble))


def test_desitter_proper_time_diverges_at_the_endpoints():
    near = math.pi / 2.0 - 1e-6
    assert desitter_proper_time(near, 1.0) > 10.0
    assert desitter_proper_time(-near, 1.0) < -10.0


def test_desitter_scale_factor_is_positive_inside_the_strip():
    for angle in (-1.0, 0.0, 1.0):
        assert desitter_closed_scale_factor(angle, 0.5) > 0.0
    assert desitter_closed_scale_factor(0.0, 0.5) == pytest.approx(2.0)


@pytest.mark.parametrize("angle", [-math.pi / 2.0, math.pi / 2.0, 2.0, math.inf])
def test_desitter_rejects_angles_outside_the_strip(angle):
    with pytest.raises(ValueError):
        desitter_proper_time(angle, 1.0)
    with pytest.raises(ValueError):
        desitter_closed_scale_factor(angle, 1.0)


@pytest.mark.parametrize("hubble", [0.0, -1.0, math.inf, math.nan])
def test_desitter_rejects_bad_hubble(hubble):
    with pytest.raises(ValueError):
        desitter_proper_time(0.0, hubble)
    with pytest.raises(ValueError):
        desitter_closed_scale_factor(0.0, hubble)


# Connes distance ----------------------------------------------------------


def test_connes_distance_is_inverse_gap():
    for gap in (0.5, 1.0, 2.0):
        assert connes_distance_two_point(gap) == pytest.approx(1.0 / gap)


def test_connes_distance_is_the_supremum():
    gap = 2.0
    distance = connes_distance_two_point(gap)
    assert commutator_norm_two_point(gap, distance) == pytest.approx(1.0)
    assert commutator_norm_two_point(gap, 2.0 * distance) == pytest.approx(2.0)


@pytest.mark.parametrize("gap", [0.0, -1.0, math.inf, math.nan])
def test_connes_rejects_bad_gap(gap):
    with pytest.raises(ValueError):
        connes_distance_two_point(gap)


def test_connes_rejects_bad_difference():
    with pytest.raises(ValueError):
        commutator_norm_two_point(1.0, math.nan)


# Thermal time -------------------------------------------------------------


def test_modular_hamiltonian_of_the_maximally_mixed_state():
    assert modular_hamiltonian(0.5) == pytest.approx((math.log(2.0), math.log(2.0)))


def test_modular_frequency_is_zero_at_maximal_mixing():
    assert modular_frequency(0.5) == pytest.approx(0.0)


def test_modular_frequency_is_antisymmetric():
    assert modular_frequency(0.75) == pytest.approx(math.log(3.0))
    assert modular_frequency(0.25) == pytest.approx(-math.log(3.0))


def test_modular_flow_rotates_the_bloch_vector():
    probability = 0.75
    omega = modular_frequency(probability)
    start = modular_flow_bloch(probability, 0.0)
    quarter = modular_flow_bloch(probability, math.pi / (2.0 * omega))
    assert start == pytest.approx((1.0, 0.0, 0.0))
    assert quarter == pytest.approx((0.0, -1.0, 0.0), abs=1e-12)
    for time in (0.1, 1.0, 2.5):
        x, y, z = modular_flow_bloch(probability, time)
        assert x * x + y * y + z * z == pytest.approx(1.0)


@pytest.mark.parametrize("probability", [0.0, 1.0, -0.1, 1.1, math.nan])
def test_modular_flow_rejects_bad_probability(probability):
    with pytest.raises(ValueError):
        modular_hamiltonian(probability)
    with pytest.raises(ValueError):
        modular_frequency(probability)
    with pytest.raises(ValueError):
        modular_flow_bloch(probability, 1.0)


def test_unruh_temperature_at_earth_gravity():
    assert unruh_temperature(9.81) == pytest.approx(3.98e-20, rel=1e-2)


def test_unruh_temperature_is_linear_in_acceleration():
    base = unruh_temperature(1.0)
    assert unruh_temperature(2.0) == pytest.approx(2.0 * base)
    assert unruh_temperature(0.0) == pytest.approx(0.0)


@pytest.mark.parametrize("acceleration", [-1.0, math.inf, math.nan])
def test_unruh_temperature_rejects_bad_acceleration(acceleration):
    with pytest.raises(ValueError):
        unruh_temperature(acceleration)
