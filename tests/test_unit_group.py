"""Tests for the multiplicative-group and projective-reciprocal helpers."""

from __future__ import annotations

from fractions import Fraction

import pytest

from model.unit_group import (
    divides,
    is_field_mod,
    projective_reciprocal,
    reciprocal,
    reciprocal_fixed_points,
    unit_inverse,
    units_mod,
)


def test_one_divides_every_integer() -> None:
    assert all(divides(1, value) for value in range(-20, 21))


def test_only_units_divide_one() -> None:
    assert [value for value in range(-10, 11) if divides(value, 1)] == [-1, 1]


def test_divides_handles_negative_divisors() -> None:
    assert divides(-3, 6)
    assert not divides(-3, 7)


def test_zero_divides_only_zero() -> None:
    assert divides(0, 0)
    assert not divides(0, 1)


@pytest.mark.parametrize("divisor,value", [(True, 1), (1, True), (1.0, 1), (1, 1.0)])
def test_divides_rejects_non_integers(divisor: object, value: object) -> None:
    with pytest.raises(ValueError, match="must be an integer"):
        divides(divisor, value)  # type: ignore[arg-type]


def test_units_mod_prime_is_every_nonzero_residue() -> None:
    assert units_mod(2) == (1,)
    assert units_mod(7) == (1, 2, 3, 4, 5, 6)


def test_units_mod_composite_is_a_proper_subset() -> None:
    assert units_mod(4) == (1, 3)
    assert units_mod(6) == (1, 5)
    assert units_mod(9) == (1, 2, 4, 5, 7, 8)


def test_units_mod_never_contains_zero() -> None:
    for modulus in (2, 3, 4, 5, 9):
        assert 0 not in units_mod(modulus)


@pytest.mark.parametrize("modulus", [1, 0, -7])
def test_units_mod_rejects_small_modulus(modulus: int) -> None:
    with pytest.raises(ValueError, match="at least 2"):
        units_mod(modulus)


def test_units_mod_rejects_bool_and_non_integer() -> None:
    with pytest.raises(ValueError, match="must be an integer"):
        units_mod(True)
    with pytest.raises(ValueError, match="must be an integer"):
        units_mod(7.0)  # type: ignore[arg-type]


def test_field_mod_is_exactly_the_primes() -> None:
    for modulus in (2, 3, 5, 7, 11, 13):
        assert is_field_mod(modulus)
    for modulus in (4, 6, 8, 9, 10, 12):
        assert not is_field_mod(modulus)


def test_field_mod_rejects_small_modulus() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        is_field_mod(1)


def test_unit_inverse_returns_the_inverse() -> None:
    assert unit_inverse(1, 7) == 1
    assert unit_inverse(2, 7) == 4
    assert unit_inverse(3, 7) == 5
    assert unit_inverse(4, 7) == 2
    assert unit_inverse(5, 7) == 3
    assert unit_inverse(6, 7) == 6
    for value in units_mod(9):
        assert value * unit_inverse(value, 9) % 9 == 1


def test_unit_inverse_rejects_zero_and_non_units() -> None:
    with pytest.raises(ValueError, match="not a unit"):
        unit_inverse(0, 7)
    with pytest.raises(ValueError, match="not a unit"):
        unit_inverse(2, 4)


def test_unit_inverse_rejects_small_modulus() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        unit_inverse(1, 1)


def test_unit_inverse_rejects_non_integers() -> None:
    with pytest.raises(ValueError, match="must be an integer"):
        unit_inverse(True, 7)
    with pytest.raises(ValueError, match="must be an integer"):
        unit_inverse(1, True)


def test_reciprocal_is_exact_for_fractions() -> None:
    assert reciprocal(Fraction(3, 2)) == Fraction(2, 3)
    assert reciprocal(4) == Fraction(1, 4)
    assert reciprocal(Fraction(-5, 7)) == Fraction(-7, 5)


def test_reciprocal_rejects_zero() -> None:
    with pytest.raises(ValueError, match="no multiplicative inverse"):
        reciprocal(0)


@pytest.mark.parametrize("value", [True, 0.5, "2"])
def test_reciprocal_rejects_non_rationals(value: object) -> None:
    with pytest.raises(ValueError, match="integer or a Fraction"):
        reciprocal(value)  # type: ignore[arg-type]


def test_projective_reciprocal_swaps_zero_and_infinity() -> None:
    assert projective_reciprocal(0) is None
    assert projective_reciprocal(None) == 0


def test_projective_reciprocal_is_an_involution() -> None:
    for value in (None, 0, 2, Fraction(-3, 5), 1, -1):
        assert projective_reciprocal(projective_reciprocal(value)) == value


def test_projective_reciprocal_has_fixed_points() -> None:
    fixed = reciprocal_fixed_points()
    assert fixed == (Fraction(-1), Fraction(1))
    for value in fixed:
        assert projective_reciprocal(value) == value


def test_projective_reciprocal_rejects_non_rationals() -> None:
    with pytest.raises(ValueError, match="integer or a Fraction"):
        projective_reciprocal(0.5)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="integer or a Fraction"):
        projective_reciprocal(True)
