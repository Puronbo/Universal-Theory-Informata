"""Tests for model.mobius."""

import pytest

from model import Mobius


def test_inversion_is_reciprocal():
    inversion = Mobius.inversion()
    for z in [2.0, -0.5, 1j, 1 + 1j, 3 - 2j]:
        assert inversion(z) == pytest.approx(1 / z)


def test_inversion_is_order_two():
    inversion = Mobius.inversion()
    assert inversion.order() == 2
    for z in [2.0, 1j, 1 + 1j]:
        assert inversion(inversion(z)) == pytest.approx(z)


def test_inversion_fixed_points():
    roots = sorted(Mobius.inversion().fixed_points(), key=lambda z: z.real)
    assert roots[0] == pytest.approx(-1)
    assert roots[1] == pytest.approx(1)


def test_matrix_representation():
    assert Mobius.inversion().matrix == ((0, 1), (1, 0))


def test_composition_order_matters():
    inversion = Mobius.inversion()
    shift = Mobius(1, 1, 0, 1)  # z -> z + 1
    assert inversion.compose(shift)(1.0) == pytest.approx(0.5)
    assert shift.compose(inversion)(1.0) == pytest.approx(2.0)


def test_identity_composition_is_neutral():
    identity = Mobius(1, 0, 0, 1)
    inversion = Mobius.inversion()
    assert identity.compose(inversion)(2.0) == pytest.approx(0.5)
    assert inversion.compose(identity)(2.0) == pytest.approx(0.5)


def test_power_and_inverse():
    inversion = Mobius.inversion()
    assert inversion.power(0).is_identity()
    assert inversion.power(3)(2.0) == pytest.approx(0.5)
    assert inversion.inverse()(0.5) == pytest.approx(2.0)
    assert inversion.power(-1)(0.5) == pytest.approx(2.0)


def test_translation_power():
    shift = Mobius(1, 1, 0, 1)
    assert shift.power(3)(0.0) == pytest.approx(3.0)


def test_order_of_identity_and_translation():
    assert Mobius(1, 0, 0, 1).order() == 1
    assert Mobius(1, 1, 0, 1).order() is None


def test_identity_detection_is_projective():
    assert Mobius(2, 0, 0, 2).is_identity()
    assert not Mobius.inversion().is_identity()


def test_fixed_points_of_nonzero_c():
    # z -> (2z + 1) / (z + 2) has fixed points +/-1.
    roots = sorted(Mobius(2, 1, 1, 2).fixed_points(), key=lambda z: z.real)
    assert roots[0] == pytest.approx(-1)
    assert roots[1] == pytest.approx(1)


def test_fixed_points_of_translation_are_at_infinity():
    assert Mobius(1, 1, 0, 1).fixed_points() == ()


def test_identity_fixed_points_are_not_unique():
    with pytest.raises(ValueError):
        Mobius(1, 0, 0, 1).fixed_points()


def test_pole_raises():
    with pytest.raises(ZeroDivisionError):
        Mobius.inversion()(0.0)


@pytest.mark.parametrize(
    "matrix",
    [
        (0, 0, 0, 0),
        (1, 2, 2, 4),
        (1, 0, 0, 0),
    ],
)
def test_degenerate_matrix_is_rejected(matrix):
    with pytest.raises(ValueError):
        Mobius(*matrix)


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
def test_non_finite_entries_are_rejected(bad):
    with pytest.raises(ValueError):
        Mobius(bad, 0, 0, 1)
