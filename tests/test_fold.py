"""Tests for model.fold."""

import math

import pytest

from model import (
    FoldComparison,
    compare_fold,
    contract_orbit,
    fold,
    fold_from_log,
    fold_power,
    fold_preimages,
    representative,
)


@pytest.mark.parametrize("x", [0.25, 0.5, 1.0, 2.0, 4.0, 10.0])
def test_fold_is_inversion_invariant(x):
    assert fold(1.0 / x) == pytest.approx(fold(x))


def test_fold_values():
    assert fold(1.0) == pytest.approx(2.0)
    assert fold(2.0) == pytest.approx(2.5)
    assert fold(0.5) == pytest.approx(2.5)
    assert fold(4.0) == pytest.approx(4.25)


@pytest.mark.parametrize("x", [0.1, 0.5, 1.0, 2.0, 10.0])
def test_fold_is_at_least_two(x):
    assert fold(x) >= 2.0


@pytest.mark.parametrize("y", [2.0, 2.5, 4.25, 10.0])
def test_preimages_fold_back(y):
    roots = fold_preimages(y)
    assert all(fold(root) == pytest.approx(y) for root in roots)


def test_preimages_are_the_expected_pair():
    assert fold_preimages(2.0) == (1.0,)
    low, high = fold_preimages(2.5)
    assert low == pytest.approx(0.5)
    assert high == pytest.approx(2.0)
    assert low * high == pytest.approx(1.0)


@pytest.mark.parametrize("y", [1.999, 0.0, -2.0, math.inf, -math.inf, math.nan])
def test_preimages_reject_bad_y(y):
    with pytest.raises(ValueError):
        fold_preimages(y)


@pytest.mark.parametrize("x", [0.0, -1.0, math.inf, -math.inf, math.nan])
def test_fold_rejects_bad_scale(x):
    with pytest.raises(ValueError):
        fold(x)
    with pytest.raises(ValueError):
        representative(x)
    with pytest.raises(ValueError):
        compare_fold(x)


def test_representative_is_in_fundamental_domain():
    assert representative(0.5) == pytest.approx(2.0)
    assert representative(2.0) == pytest.approx(2.0)
    assert representative(1.0) == pytest.approx(1.0)
    for x in [0.1, 0.5, 1.0, 2.0, 10.0]:
        chosen = representative(x)
        assert chosen >= 1.0
        assert fold(chosen) == pytest.approx(fold(x))


def test_compare_fold():
    comparison = compare_fold(2.0)
    assert isinstance(comparison, FoldComparison)
    assert comparison.initial == 2.0
    assert comparison.dual == pytest.approx(0.5)
    assert comparison.quotient == pytest.approx(2.5)
    assert comparison.representative == pytest.approx(2.0)


@pytest.mark.parametrize("t", [-3.0, -1.0, 0.0, 1.0, 2.5])
def test_fold_from_log_is_fold_of_exponential(t):
    assert fold_from_log(t) == pytest.approx(fold(math.exp(t)))


def test_fold_from_log_is_two_cosh_and_even():
    assert fold_from_log(0.0) == pytest.approx(2.0)
    assert fold_from_log(1.0) == pytest.approx(2.0 * math.cosh(1.0))
    for t in [0.3, 1.0, 2.5]:
        assert fold_from_log(-t) == pytest.approx(fold_from_log(t))


def test_fold_from_log_along_a_contraction_orbit():
    x, steps, rate = 2.0, 4, 0.5
    step = math.log(rate)

    for index, value in enumerate(contract_orbit(x, steps, rate)):
        assert fold(value) == pytest.approx(fold_from_log(math.log(x) + index * step))


@pytest.mark.parametrize("t", [math.inf, -math.inf, math.nan])
def test_fold_from_log_rejects_non_finite(t):
    with pytest.raises(ValueError):
        fold_from_log(t)


def test_fold_from_log_rejects_overflow():
    with pytest.raises(ValueError):
        fold_from_log(1000.0)


@pytest.mark.parametrize(
    ("x", "y"),
    [(2.0, 3.0), (0.5, 4.0), (1.25, 0.8), (10.0, 10.0)],
)
def test_fold_product_identity(x, y):
    assert fold(x) * fold(y) == pytest.approx(fold(x * y) + fold(x / y))


@pytest.mark.parametrize("x", [0.25, 0.5, 1.0, 2.0, 10.0])
def test_fold_square_identity(x):
    assert fold(x) ** 2 == pytest.approx(fold(x * x) + 2.0)


@pytest.mark.parametrize("x", [0.25, 0.5, 1.0, 2.0, 10.0])
def test_fold_discriminant_identity(x):
    assert fold(x) ** 2 - 4.0 == pytest.approx((x - 1.0 / x) ** 2)


@pytest.mark.parametrize("x", [0.25, 0.5, 1.0, 2.0, 10.0])
@pytest.mark.parametrize("exponent", [-4, -1, 0, 1, 2, 3, 5])
def test_fold_power_matches_direct_fold(x, exponent):
    assert fold_power(x, exponent) == pytest.approx(fold(x**exponent))


def test_fold_power_is_inversion_invariant():
    assert fold_power(2.0, 3) == pytest.approx(fold_power(0.5, 3))


@pytest.mark.parametrize("exponent", [1.5, True, "2"])
def test_fold_power_rejects_bad_exponent(exponent):
    with pytest.raises(ValueError):
        fold_power(2.0, exponent)


@pytest.mark.parametrize("x", [0.0, -1.0, math.inf, math.nan])
def test_fold_power_rejects_bad_scale(x):
    with pytest.raises(ValueError):
        fold_power(x, 2)


def test_fold_power_rejects_overflow():
    with pytest.raises(ValueError):
        fold_power(1e300, 2)
