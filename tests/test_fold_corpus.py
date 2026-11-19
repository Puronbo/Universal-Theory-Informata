"""Tests for the executable core of the Fold corpus."""

from __future__ import annotations

import cmath
import math

import pytest

from model.fold_corpus import (
    SurfaceLedger,
    compose_reflections,
    division_collapse_scale,
    division_point,
    doubling_agrees_with_negation,
    doubling_is_bijective,
    fold_orbit,
    horizon_ratio,
    midpoint_map,
    midpoint_scale,
    observer_split,
    projection_onto_crease,
    reflect_point,
    reflection_matrix,
    rotation_matrix,
    scale_determinant,
    scale_point,
    schwarzschild_radius,
    solid_angle_fraction,
    two_fold_rotation_angle,
    wheel_turn,
    wheel_turns,
)

# Scale ---------------------------------------------------------------------


def test_scale_point_about_the_origin() -> None:
    assert scale_point(3.0, (1.0, -2.0)) == (3.0, -6.0)


def test_scale_point_about_a_datum_fixes_the_datum() -> None:
    assert scale_point(7.0, (2.0, 2.0), datum=(2.0, 2.0)) == (2.0, 2.0)


def test_scale_point_composition_is_multiplication() -> None:
    point = (1.0, 4.0)
    once = scale_point(2.0, point)
    twice = scale_point(3.0, once)
    assert twice == scale_point(6.0, point)


def test_scale_point_zero_collapses_to_the_datum() -> None:
    assert scale_point(0.0, (4.0, 5.0), datum=(1.0, 1.0)) == (1.0, 1.0)


def test_scale_point_rejects_non_finite_k() -> None:
    with pytest.raises(ValueError, match="k must be finite"):
        scale_point(math.inf, (1.0,))


def test_scale_point_rejects_empty_point() -> None:
    with pytest.raises(ValueError, match="point must have at least one coordinate"):
        scale_point(1.0, ())


def test_scale_point_rejects_non_finite_coordinates() -> None:
    with pytest.raises(ValueError, match="point must have finite coordinates"):
        scale_point(1.0, (1.0, math.nan))


def test_scale_point_rejects_dimension_mismatch() -> None:
    with pytest.raises(ValueError, match="same dimension"):
        scale_point(1.0, (1.0, 2.0), datum=(0.0,))


def test_scale_determinant_in_one_dimension_is_signed_length() -> None:
    assert scale_determinant(-3.0, 1) == -3.0


def test_scale_determinant_in_three_dimensions_reverses_orientation() -> None:
    assert scale_determinant(-2.0, 3) == -8.0


def test_scale_determinant_rejects_bad_dimension() -> None:
    with pytest.raises(ValueError, match="dimension must be >= 1"):
        scale_determinant(2.0, 0)


def test_scale_determinant_rejects_a_bool_as_a_dimension() -> None:
    with pytest.raises(ValueError, match="dimension must be an integer"):
        scale_determinant(2.0, True)  # type: ignore[arg-type]


# Fold and crease -----------------------------------------------------------


def test_reflect_point_across_the_axis() -> None:
    assert reflect_point((2.0, 3.0), (1.0, 0.0)) == (-2.0, 3.0)


def test_reflect_point_across_an_offset_hyperplane() -> None:
    assert reflect_point((4.0, 0.0), (1.0, 0.0), offset=1.0) == (-2.0, 0.0)


def test_reflect_point_fixes_a_point_on_the_crease() -> None:
    assert reflect_point((1.0, 2.0), (0.0, 1.0), offset=2.0) == (1.0, 2.0)


def test_reflect_point_is_an_involution() -> None:
    point = (0.3, -1.7)
    normal = (1.0, 2.0)
    once = reflect_point(point, normal, offset=0.5)
    assert reflect_point(once, normal, offset=0.5) == pytest.approx(point, abs=1e-15)


def test_reflect_point_rejects_zero_normal() -> None:
    with pytest.raises(ValueError, match="normal must be nonzero"):
        reflect_point((1.0, 2.0), (0.0, 0.0))


def test_reflect_point_rejects_dimension_mismatch() -> None:
    with pytest.raises(ValueError, match="same dimension"):
        reflect_point((1.0, 2.0), (1.0, 0.0, 0.0))


def test_reflection_matrix_is_symmetric_and_involutive() -> None:
    matrix = reflection_matrix((1.0, 1.0))
    assert matrix[0][1] == pytest.approx(matrix[1][0])
    squared = compose_reflections((1.0, 1.0), (1.0, 1.0))
    # R . R is the identity, so it fixes both basis vectors.
    assert squared[0][0] == pytest.approx(1.0)
    assert squared[0][1] == pytest.approx(0.0)
    assert squared[1][0] == pytest.approx(0.0)
    assert squared[1][1] == pytest.approx(1.0)


def test_reflection_matrix_requires_two_dimensions() -> None:
    with pytest.raises(ValueError, match="two-dimensional"):
        reflection_matrix((1.0, 0.0, 0.0))


def test_rotation_matrix_quarter_turn() -> None:
    matrix = rotation_matrix(math.pi / 2.0)
    assert matrix[0][0] == pytest.approx(0.0, abs=1e-15)
    assert matrix[0][1] == pytest.approx(-1.0)
    assert matrix[1][0] == pytest.approx(1.0)


def test_two_reflections_compose_to_a_rotation() -> None:
    matrix = compose_reflections((1.0, 0.0), (0.0, 1.0))
    expected = rotation_matrix(-math.pi)
    for row in range(2):
        for column in range(2):
            assert matrix[row][column] == pytest.approx(expected[row][column])


def test_two_fold_rotation_angle_is_twice_the_crease_angle() -> None:
    # Normals at 0 and 30 degrees describe creases at 90 and 120 degrees.
    angle = two_fold_rotation_angle((1.0, 0.0), (math.cos(math.pi / 6), math.sin(math.pi / 6)))
    assert angle == pytest.approx(math.pi / 3.0)


def test_two_fold_rotation_angle_is_normalized_to_the_half_turn() -> None:
    angle = two_fold_rotation_angle((1.0, 1.0), (1.0, -1.0))
    assert abs(angle) == pytest.approx(math.pi)


def test_two_fold_rotation_angle_requires_two_dimensions() -> None:
    with pytest.raises(ValueError, match="two-dimensional"):
        two_fold_rotation_angle((1.0, 0.0, 0.0), (1.0, 0.0, 0.0))


def test_fold_orbit_of_a_fixed_point_is_a_singleton() -> None:
    def fold(point: tuple[float, ...]) -> tuple[float, ...]:
        return point

    assert fold_orbit((1.0, 2.0), fold) == ((1.0, 2.0),)


def test_fold_orbit_of_a_moved_point_is_a_pair() -> None:
    def fold(point: tuple[float, ...]) -> tuple[float, ...]:
        return (-point[0],) + point[1:]

    assert fold_orbit((1.0, 2.0), fold) == ((1.0, 2.0), (-1.0, 2.0))


def test_fold_orbit_rejects_empty_point() -> None:
    with pytest.raises(ValueError, match="at least one coordinate"):
        fold_orbit((), lambda point: point)


# Midpoint and division -----------------------------------------------------


def test_midpoint_scale_closes_at_minus_one() -> None:
    assert midpoint_scale(-1.0) == 0.0


def test_midpoint_of_a_point_and_its_reflection_is_the_crease_projection() -> None:
    point = (2.0, 5.0)
    normal = (0.6, 0.8)
    reflected = reflect_point(point, normal)
    midpoint = tuple(0.5 * (a + b) for a, b in zip(point, reflected, strict=True))
    assert midpoint == pytest.approx(projection_onto_crease(point, normal))


def test_midpoint_map_with_k_minus_one_collapses_to_the_datum() -> None:
    assert midpoint_map(-1.0, (2.0, 5.0), datum=(1.0, 1.0)) == (1.0, 1.0)


def test_division_point_at_zero_is_the_start() -> None:
    point = (1.0, 2.0)
    assert division_point(0.0, 4.0, point) == point


def test_division_point_at_one_is_the_fold_image() -> None:
    point = (1.0, 2.0)
    assert division_point(1.0, 4.0, point) == scale_point(4.0, point)


def test_division_collapse_scale_maps_to_the_vanishing_factor() -> None:
    for t in (0.25, 0.5, 2.0, -3.0):
        k = division_collapse_scale(t)
        assert 1.0 - t + t * k == pytest.approx(0.0)


def test_division_collapse_scale_rejects_zero() -> None:
    with pytest.raises(ValueError, match="t must be nonzero"):
        division_collapse_scale(0.0)


def test_projection_onto_crease_moves_along_the_normal() -> None:
    assert projection_onto_crease((2.0, 3.0), (1.0, 0.0)) == (0.0, 3.0)


def test_projection_onto_crease_respects_the_offset() -> None:
    assert projection_onto_crease((4.0, 1.0), (1.0, 0.0), offset=1.0) == (1.0, 1.0)


def test_projection_onto_crease_rejects_dimension_mismatch() -> None:
    with pytest.raises(ValueError, match="same dimension"):
        projection_onto_crease((1.0, 2.0), (1.0, 0.0, 0.0))


# Observer split ------------------------------------------------------------


def test_observer_split_endpoints() -> None:
    assert observer_split(1.0 + 0.0j) == pytest.approx((1.0, 0.0))
    assert observer_split(1.0j) == pytest.approx((0.5, 0.5))
    assert observer_split(-1.0 + 0.0j) == pytest.approx((0.0, 1.0))


def test_observer_split_sums_to_one() -> None:
    for degrees in range(0, 91, 5):
        k = cmath.exp(1j * math.radians(degrees))
        crease, sky = observer_split(k)
        assert crease + sky == pytest.approx(1.0)


def test_observer_split_matches_the_solid_angle() -> None:
    for degrees in range(0, 91, 5):
        theta = math.radians(degrees)
        _, sky = observer_split(cmath.exp(1j * theta))
        assert sky == pytest.approx(solid_angle_fraction(math.sin(theta), 1.0), abs=1e-15)


def test_observer_split_is_fold_invariant() -> None:
    k = cmath.exp(0.7j)
    assert observer_split(k) == pytest.approx(observer_split(1.0 / k))


def test_observer_split_rejects_off_circle() -> None:
    with pytest.raises(ValueError, match="unit circle"):
        observer_split(2.0 + 0.0j)


def test_observer_split_rejects_zero() -> None:
    with pytest.raises(ValueError, match="finite and nonzero"):
        observer_split(0.0j)


def test_observer_split_rejects_non_finite() -> None:
    with pytest.raises(ValueError, match="finite and nonzero"):
        observer_split(complex(math.inf, 0.0))


# Cap and puncture ----------------------------------------------------------


def test_surface_ledger_cap_and_uncap_are_inverse() -> None:
    ledger = SurfaceLedger(chi=0, boundary=1, punctures=0)
    assert ledger.cap().uncap() == ledger


def test_surface_ledger_cap_consumes_boundary() -> None:
    assert SurfaceLedger(0, 1, 0).cap() == SurfaceLedger(1, 0, 0)


def test_surface_ledger_cap_needs_boundary() -> None:
    with pytest.raises(ValueError, match="cap requires a boundary component"):
        SurfaceLedger(2, 0, 0).cap()


def test_surface_ledger_puncture_and_fill_are_inverse() -> None:
    ledger = SurfaceLedger(chi=2, boundary=0, punctures=0)
    assert ledger.puncture().fill() == ledger


def test_surface_ledger_fill_needs_a_puncture() -> None:
    with pytest.raises(ValueError, match="fill requires a puncture"):
        SurfaceLedger(2, 0, 0).fill()


def test_surface_ledger_rejects_negative_counts() -> None:
    with pytest.raises(ValueError, match="boundary must be >= 0"):
        SurfaceLedger(2, -1, 0)
    with pytest.raises(ValueError, match="punctures must be >= 0"):
        SurfaceLedger(2, 0, -1)


def test_cap_and_puncture_cancel_on_chi_but_not_on_the_triple() -> None:
    disk = SurfaceLedger(chi=0, boundary=1, punctures=0)
    capped_then_punctured = disk.cap().puncture()
    assert capped_then_punctured.chi == disk.chi
    assert capped_then_punctured.boundary != disk.boundary
    assert capped_then_punctured.punctures != disk.punctures
    assert capped_then_punctured != disk


# Closure -------------------------------------------------------------------


def test_wheel_turn_advances_one_spoke() -> None:
    assert wheel_turn(5, 3) == 4


def test_wheel_turn_wraps_at_the_rim() -> None:
    assert wheel_turn(5, 4) == 0


def test_wheel_turn_single_spoke_is_stationary() -> None:
    assert wheel_turn(1, 0) == 0


def test_wheel_turns_is_additive() -> None:
    mark = 3
    for _ in range(10):
        mark = wheel_turn(7, mark)
    assert wheel_turns(7, 10, 3) == mark


def test_wheel_turns_rejects_negative_steps() -> None:
    with pytest.raises(ValueError, match="steps must be >= 0"):
        wheel_turns(7, -1, 0)


def test_doubling_is_bijective_on_odd_moduli() -> None:
    assert doubling_is_bijective(1)
    assert doubling_is_bijective(3)
    assert doubling_is_bijective(9)


def test_doubling_is_not_bijective_on_even_moduli() -> None:
    assert not doubling_is_bijective(2)
    assert not doubling_is_bijective(6)


def test_doubling_is_bijective_rejects_zero() -> None:
    with pytest.raises(ValueError, match="n must be >= 1"):
        doubling_is_bijective(0)


def test_doubling_agrees_with_negation_exactly_when_n_divides_three() -> None:
    answers = [n for n in range(1, 13) if doubling_agrees_with_negation(n)]
    assert answers == [1, 3]


# Observer and horizon ------------------------------------------------------


def test_solid_angle_at_the_surface_is_a_half_space() -> None:
    assert solid_angle_fraction(1.0, 1.0) == pytest.approx(0.5)


def test_solid_angle_inside_is_the_whole_sky() -> None:
    assert solid_angle_fraction(2.0, 1.0) == 1.0


def test_solid_angle_of_a_point_is_zero() -> None:
    assert solid_angle_fraction(0.0, 5.0) == 0.0


def test_solid_angle_fraction_matches_the_printed_rows() -> None:
    distance = 2.281
    observed = [solid_angle_fraction(radius, distance) for radius in (1.0, 0.5, 0.25)]
    assert observed[0] == pytest.approx(0.05061, abs=5e-5)
    assert observed[1] == pytest.approx(0.01216, abs=5e-5)
    assert observed[2] == pytest.approx(0.00301, abs=5e-5)


def test_solid_angle_rejects_negative_radius() -> None:
    with pytest.raises(ValueError, match="radius must be >= 0"):
        solid_angle_fraction(-1.0, 2.0)


def test_schwarzschild_radius_of_the_sun() -> None:
    # 2GM/c^2 with M = 1.988e30 kg is about 2.95 km.
    assert schwarzschild_radius(1.988e30) == pytest.approx(2953.0, rel=2e-3)


def test_schwarzschild_radius_rejects_negative_mass() -> None:
    with pytest.raises(ValueError, match="mass must be >= 0"):
        schwarzschild_radius(-1.0)


def test_horizon_ratio_of_the_earth() -> None:
    assert horizon_ratio(5.972e24, 6.371e6) == pytest.approx(1.392e-9, rel=5e-3)


def test_horizon_ratio_of_a_water_sphere() -> None:
    # 70 kg of water is a sphere of radius ~0.2556 m.
    assert horizon_ratio(70.0, 0.2556) == pytest.approx(4.067e-25, rel=5e-3)


def test_horizon_ratio_rejects_zero_radius() -> None:
    with pytest.raises(ValueError, match="radius must be > 0"):
        horizon_ratio(1.0, 0.0)
