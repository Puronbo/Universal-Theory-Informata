"""Tests for model.superoperator."""

import math

import pytest

from model import (
    commutant_dimension,
    commutator,
    commutes,
    dagger,
    diagonal,
    hilbert_schmidt,
    identity,
    is_self_adjoint,
    is_zero_matrix,
    liouvillian,
    liouvillian_eigenvalues,
    matadd,
    matmul,
    matscale,
    matsub,
    zero_matrix,
    zero_mode_pairs,
)


def assert_matrix_close(actual, expected, tolerance=1e-12):
    assert len(actual) == len(expected)
    for left_row, right_row in zip(actual, expected, strict=True):
        assert len(left_row) == len(right_row)
        for left, right in zip(left_row, right_row, strict=True):
            assert abs(left - right) <= tolerance


def test_identity_and_zero_matrix():
    assert identity(2) == ((1.0 + 0.0j, 0.0j), (0.0j, 1.0 + 0.0j))
    assert zero_matrix(2) == ((0.0j, 0.0j), (0.0j, 0.0j))
    assert_matrix_close(matmul(identity(3), identity(3)), identity(3))


def test_matmul_matadd_matsub_matscale():
    left = ((1.0, 2.0), (3.0, 4.0))
    right = ((0.0, 1.0), (1.0, 0.0))
    assert_matrix_close(matmul(left, right), ((2.0, 1.0), (4.0, 3.0)))
    assert_matrix_close(matadd(left, right), ((1.0, 3.0), (4.0, 4.0)))
    assert_matrix_close(matsub(left, right), ((1.0, 1.0), (2.0, 4.0)))
    assert_matrix_close(matscale(2.0, left), ((2.0, 4.0), (6.0, 8.0)))


def test_dagger_is_conjugate_transpose():
    matrix = ((1.0, 2.0 + 1.0j), (3.0 - 1.0j, 4.0))
    assert_matrix_close(dagger(matrix), ((1.0, 3.0 + 1.0j), (2.0 - 1.0j, 4.0)))


def test_diagonal_and_commutator():
    hamiltonian = diagonal([1.0, 2.0, 2.0])
    observable = diagonal([3.0, 4.0, 5.0])
    assert is_zero_matrix(commutator(hamiltonian, observable))
    assert commutes(hamiltonian, observable)


def test_commutator_detects_off_diagonal_coupling():
    hamiltonian = diagonal([1.0, 2.0])
    observable = ((0.0, 1.0), (0.0, 0.0))
    assert_matrix_close(commutator(hamiltonian, observable), ((0.0, -1.0), (0.0, 0.0)))
    assert not commutes(hamiltonian, observable)


def test_liouvillian_is_the_commutator():
    hamiltonian = diagonal([1.0, 2.0])
    observable = ((0.0, 1.0), (1.0, 0.0))
    assert_matrix_close(
        liouvillian(hamiltonian, observable),
        commutator(hamiltonian, observable),
    )


def test_degenerate_block_commutes():
    hamiltonian = diagonal([1.0, 2.0, 2.0])
    observable = ((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 0.0, 0.0))
    assert commutes(hamiltonian, observable)


def test_hilbert_schmidt_inner_product():
    left = ((1.0, 2.0 + 1.0j), (3.0, 4.0))
    right = ((0.0, 1.0j), (2.0, 1.0))
    inner = hilbert_schmidt(left, right)
    assert inner == pytest.approx(hilbert_schmidt(right, left).conjugate())
    assert hilbert_schmidt(left, left).real > 0.0


def test_liouvillian_is_self_adjoint_under_hilbert_schmidt():
    hamiltonian = diagonal([1.0, 2.0])
    left = ((1.0, 2.0), (3.0, 4.0))
    right = ((0.0, 1.0j), (2.0, 0.0))
    assert hilbert_schmidt(left, liouvillian(hamiltonian, right)) == pytest.approx(
        hilbert_schmidt(liouvillian(hamiltonian, left), right)
    )


@pytest.mark.parametrize(
    ("matrix", "expected"),
    [
        (((1.0, 0.0), (0.0, 1.0)), True),
        (((0.0, 1.0j), (-1.0j, 0.0)), True),
        (((0.0, 1.0), (0.0, 0.0)), False),
    ],
)
def test_is_self_adjoint(matrix, expected):
    assert is_self_adjoint(matrix) is expected


def test_liouvillian_eigenvalues_are_transition_frequencies():
    assert liouvillian_eigenvalues([1.0, 2.0]) == (0.0, -1.0, 1.0, 0.0)


def test_zero_modes_are_degenerate_pairs():
    assert zero_mode_pairs([1.0, 2.0, 2.0]) == (
        (0, 0),
        (1, 1),
        (1, 2),
        (2, 1),
        (2, 2),
    )
    assert commutant_dimension([1.0, 2.0, 2.0]) == 5
    assert commutant_dimension([1.0, 2.0, 3.0]) == 3


@pytest.mark.parametrize("matrix", [(), (((1.0, 0.0),), ((0.0, 1.0), (0.0, 0.0)))])
def test_invalid_matrices_are_rejected(matrix):
    with pytest.raises(ValueError):
        matmul(matrix, matrix)


@pytest.mark.parametrize("value", [math.inf, math.nan])
def test_non_finite_matrix_entries_are_rejected(value):
    with pytest.raises(ValueError):
        is_self_adjoint(((1.0, value), (0.0, 1.0)))


def test_dimension_mismatch_is_rejected():
    with pytest.raises(ValueError):
        matmul(identity(2), identity(3))
    with pytest.raises(ValueError):
        matadd(identity(2), identity(3))
    with pytest.raises(ValueError):
        matsub(identity(2), identity(3))
    with pytest.raises(ValueError):
        hilbert_schmidt(identity(2), identity(3))


def test_invalid_sizes_and_scalars_are_rejected():
    with pytest.raises(ValueError):
        identity(0)
    with pytest.raises(ValueError):
        zero_matrix(0)
    with pytest.raises(ValueError):
        diagonal([])
    with pytest.raises(ValueError):
        matscale(complex(math.inf, 0.0), identity(2))


def test_invalid_tolerance_is_rejected():
    with pytest.raises(ValueError):
        is_self_adjoint(identity(2), -1.0)
    with pytest.raises(ValueError):
        is_zero_matrix(zero_matrix(2), math.inf)
    with pytest.raises(ValueError):
        commutes(identity(2), identity(2), -1.0)


@pytest.mark.parametrize("values", [(), [math.inf], [math.nan]])
def test_invalid_eigenvalues_are_rejected(values):
    with pytest.raises(ValueError):
        liouvillian_eigenvalues(values)
    with pytest.raises(ValueError):
        zero_mode_pairs(values)


def test_zero_mode_tolerance():
    assert zero_mode_pairs([1.0, 1.0 + 1e-9], tolerance=1e-12) == ((0, 0), (1, 1))
    assert zero_mode_pairs([1.0, 1.0 + 1e-9], tolerance=1e-6) == (
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
    )
