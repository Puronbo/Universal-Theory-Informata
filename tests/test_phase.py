"""Tests for model.phase."""

import math

import pytest

from model import (
    WaveSample,
    conjugate,
    imaginary_height,
    intensity,
    phase_angle,
    phase_factor,
    real_width,
    rotate_quarter_turn,
    wave_sample,
    wavelength_from_wavenumber,
    wavenumber_from_wavelength,
)


def test_phase_factor_is_unit_modulus():
    for k, x, omega, t in [(1.0, 0.0, 0.0, 0.0), (2.5, 1.3, 0.7, 0.4)]:
        assert abs(phase_factor(k, x, omega, t)) == pytest.approx(1.0)


def test_phase_factor_advances_by_quarter_turn():
    assert phase_factor(1.0, 0.0) == pytest.approx(1.0 + 0.0j)
    assert phase_factor(1.0, math.pi / 2.0) == pytest.approx(1.0j)


def test_intensity_is_modulus_squared():
    assert intensity(3.0 + 4.0j) == pytest.approx(25.0)
    assert intensity(0.0) == 0.0


def test_global_phase_does_not_change_intensity():
    value = 2.0 - 1.0j
    rotated = value * complex(math.cos(0.7), math.sin(0.7))
    assert intensity(rotated) == pytest.approx(intensity(value))


def test_phase_angle():
    assert phase_angle(1.0) == pytest.approx(0.0)
    assert phase_angle(1.0j) == pytest.approx(math.pi / 2.0)
    assert phase_angle(-1.0) == pytest.approx(math.pi)


def test_quarter_turn_is_order_four():
    value = 2.0 + 3.0j
    twice = rotate_quarter_turn(rotate_quarter_turn(value))
    four_times = rotate_quarter_turn(rotate_quarter_turn(twice))
    assert twice == pytest.approx(-value)
    assert four_times == pytest.approx(value)


def test_conjugate_cancels_the_imaginary_part():
    value = 2.0 + 3.0j
    assert conjugate(value) == pytest.approx(2.0 - 3.0j)
    assert real_width(conjugate(value)) == pytest.approx(real_width(value))
    assert imaginary_height(conjugate(value)) == pytest.approx(-imaginary_height(value))


def test_wave_sample_projects_to_intensity_and_phase():
    sample = wave_sample(1.0 + 1.0j, 0.0, 0.0)
    assert isinstance(sample, WaveSample)
    assert sample.amplitude == pytest.approx(1.0 + 1.0j)
    assert sample.intensity == pytest.approx(2.0)
    assert sample.phase == pytest.approx(math.pi / 4.0)


def test_wave_sample_includes_time_dependence():
    sample = wave_sample(1.0, 2.0, 0.5, 3.0, 0.25)
    expected = phase_factor(2.0, 0.5, 3.0, 0.25)
    assert sample.amplitude == pytest.approx(expected)
    assert sample.intensity == pytest.approx(1.0)


def test_wavelength_wavenumber_round_trip():
    for wavelength in [0.1, 1.0, 2.0 * math.pi, 10.0]:
        k = wavenumber_from_wavelength(wavelength)
        assert wavelength_from_wavenumber(k) == pytest.approx(wavelength)


def test_wavelength_from_negative_wavenumber_is_positive():
    assert wavelength_from_wavenumber(-2.0 * math.pi) == pytest.approx(1.0)


@pytest.mark.parametrize("value", [0.0, -1.0, math.inf, math.nan])
def test_wavenumber_rejects_bad_wavelength(value):
    with pytest.raises(ValueError):
        wavenumber_from_wavelength(value)


@pytest.mark.parametrize("value", [0.0, math.inf, math.nan])
def test_wavelength_rejects_bad_wavenumber(value):
    with pytest.raises(ValueError):
        wavelength_from_wavenumber(value)


@pytest.mark.parametrize("value", [math.inf, math.nan])
def test_phase_factor_rejects_non_finite_inputs(value):
    with pytest.raises(ValueError):
        phase_factor(value, 0.0)
    with pytest.raises(ValueError):
        phase_factor(1.0, value)
    with pytest.raises(ValueError):
        phase_factor(1.0, 0.0, value)
    with pytest.raises(ValueError):
        phase_factor(1.0, 0.0, 0.0, value)


@pytest.mark.parametrize("value", [complex(math.inf, 0.0), complex(0.0, math.nan)])
def test_complex_helpers_reject_non_finite_inputs(value):
    for function in (intensity, phase_angle, rotate_quarter_turn, conjugate, real_width):
        with pytest.raises(ValueError):
            function(value)
    with pytest.raises(ValueError):
        imaginary_height(value)
    with pytest.raises(ValueError):
        wave_sample(value, 1.0, 0.0)
