"""Tests for model.symmetry_breaking."""

import math

import pytest

from model import (
    double_well_curvature,
    double_well_minima,
    double_well_potential,
    is_symmetric_zero_unstable,
    vev_magnitude,
)


def test_potential_is_symmetric_and_zero_at_origin():
    assert double_well_potential(0.0) == pytest.approx(0.0)
    for phi in (0.25, 0.5, 1.0, 2.0):
        assert double_well_potential(phi) == pytest.approx(double_well_potential(-phi))


def test_minima_are_lower_than_the_symmetric_point():
    for mu_squared, quartic in [(1.0, 1.0), (2.0, 0.5), (0.25, 3.0)]:
        low, high = double_well_minima(mu_squared, quartic)
        assert low == pytest.approx(-high)
        assert high == pytest.approx(vev_magnitude(mu_squared, quartic))
        assert double_well_potential(high, mu_squared, quartic) < 0.0
        assert double_well_curvature(high, mu_squared, quartic) > 0.0


def test_zero_is_unstable_and_the_wells_are_stable():
    for mu_squared, quartic in [(1.0, 1.0), (2.0, 0.5), (0.25, 3.0)]:
        assert is_symmetric_zero_unstable(mu_squared, quartic)
        assert double_well_curvature(0.0, mu_squared, quartic) < 0.0
        high = vev_magnitude(mu_squared, quartic)
        assert double_well_curvature(high, mu_squared, quartic) > 0.0


def test_default_vev_is_one_over_sqrt_two():
    assert vev_magnitude() == pytest.approx(1.0 / math.sqrt(2.0))
    assert double_well_minima() == pytest.approx((-1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0)))


@pytest.mark.parametrize(
    ("mu_squared", "quartic"),
    [(0.0, 1.0), (-1.0, 1.0), (1.0, 0.0), (1.0, -1.0), (math.inf, 1.0), (1.0, math.nan)],
)
def test_parameters_must_be_finite_and_positive(mu_squared, quartic):
    with pytest.raises(ValueError):
        double_well_potential(0.5, mu_squared, quartic)
    with pytest.raises(ValueError):
        double_well_minima(mu_squared, quartic)
    with pytest.raises(ValueError):
        vev_magnitude(mu_squared, quartic)
    with pytest.raises(ValueError):
        double_well_curvature(0.5, mu_squared, quartic)
    with pytest.raises(ValueError):
        is_symmetric_zero_unstable(mu_squared, quartic)


@pytest.mark.parametrize("phi", [math.inf, -math.inf, math.nan])
def test_field_must_be_finite(phi):
    with pytest.raises(ValueError):
        double_well_potential(phi)
    with pytest.raises(ValueError):
        double_well_curvature(phi)
