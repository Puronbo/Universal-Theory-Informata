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
    liouvillian_resolvent,
    matadd,
    matmul,
    matscale,
    matsub,
    resolvent_diagonal,
    resolvent_norm,
    trace,
    truncated_annihilation,
    truncated_creation,
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


def test_liouvillian_spectrum_sums_to_zero():
    for spectrum in ([1.0, 2.0, 3.0], [0.0, 0.0, 2.5], [1.0 + 0.5j, -2.0j, 4.0]):
        assert sum(liouvillian_eigenvalues(spectrum)) == pytest.approx(0j)


def test_liouvillian_spectrum_is_negation_symmetric():
    transitions = liouvillian_eigenvalues([1.0 + 0.5j, 2.0, 4.0])
    for value in transitions:
        assert any(abs(value + other) <= 1e-12 for other in transitions)


def test_commutator_trace_is_zero():
    hamiltonian = ((1.0, 2.0), (3.0, 4.0))
    observable = ((0.0, 1.0), (1.0, 0.0))
    result = commutator(hamiltonian, observable)
    assert result[0][0] + result[1][1] == pytest.approx(0j)


def test_commutant_dimension_is_sum_of_multiplicity_squares():
    assert commutant_dimension([1.0, 2.0, 3.0]) == 1 + 1 + 1
    assert commutant_dimension([1.0, 2.0, 2.0]) == 1 + 4
    assert commutant_dimension([1.0, 1.0, 2.0, 2.0]) == 4 + 4
    assert commutant_dimension([5.0, 5.0, 5.0, 5.0]) == 16


def test_liouvillian_is_a_derivation():
    hamiltonian = diagonal([1.0, 2.0])
    left = ((1.0, 2.0), (3.0, 4.0))
    right = ((0.0, 1.0), (1.0, 0.0))
    assert_matrix_close(
        liouvillian(hamiltonian, matmul(left, right)),
        matadd(
            matmul(liouvillian(hamiltonian, left), right),
            matmul(left, liouvillian(hamiltonian, right)),
        ),
    )


def test_commutant_is_closed_under_products():
    hamiltonian = diagonal([1.0, 2.0, 2.0])
    left = ((1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.0, 0.0, 0.0))
    right = ((0.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))
    assert commutes(hamiltonian, left)
    assert commutes(hamiltonian, right)
    assert commutes(hamiltonian, matmul(left, right))


def test_trace_of_a_commutator_is_zero():
    pairs = [
        (((1.0, 2.0), (3.0, 4.0)), ((0.0, 1.0), (1.0, 0.0))),
        (((0.0, 1.0), (0.0, 0.0)), ((0.0, 0.0), (1.0, 0.0))),
    ]
    for left, right in pairs:
        assert trace(commutator(left, right)) == pytest.approx(0j)


def test_finite_dimensional_ccr_is_impossible():
    # [a, a^dagger] = 1 would need a commutator with nonzero trace.
    lowering = ((0.0, 1.0), (0.0, 0.0))
    raising = ((0.0, 0.0), (1.0, 0.0))
    residue = commutator(lowering, raising)
    assert trace(residue) == pytest.approx(0j)
    assert trace(identity(2)) == 2
    assert residue != identity(2)


def test_resolvent_diagonal_entries():
    assert resolvent_diagonal([1.0, 2.0], 3.0) == pytest.approx((0.5, 1.0))
    assert resolvent_diagonal([1.0 + 1.0j], 3.0) == pytest.approx((1.0 / (2.0 - 1.0j),))


def test_resolvent_has_poles_at_eigenvalues():
    for z in (1.0, 2.0):
        with pytest.raises(ValueError):
            resolvent_diagonal([1.0, 2.0], z)
        with pytest.raises(ValueError):
            resolvent_norm([1.0, 2.0], z)


def test_resolvent_norm_diverges_near_a_pole():
    far = resolvent_norm([1.0], 2.0)
    near = resolvent_norm([1.0], 1.0 + 1e-3)
    nearer = resolvent_norm([1.0], 1.0 + 1e-6)
    assert far < near < nearer
    assert near == pytest.approx(1e3)
    assert nearer == pytest.approx(1e6)


def test_truncated_oscillator_residue_is_one_except_at_the_top():
    for dimension in (2, 3, 5):
        lowering = truncated_annihilation(dimension)
        raising = truncated_creation(dimension)
        residue = commutator(lowering, raising)
        for index in range(dimension - 1):
            assert residue[index][index] == pytest.approx(1.0)
        assert residue[dimension - 1][dimension - 1] == pytest.approx(1.0 - dimension)
        for row in range(dimension):
            for column in range(dimension):
                if row != column:
                    assert residue[row][column] == pytest.approx(0j)
        assert trace(residue) == pytest.approx(0j)


def test_truncated_oscillator_lowering_and_raising():
    lowering = truncated_annihilation(4)
    raising = truncated_creation(4)
    assert all(lowering[row][0] == 0 for row in range(4))
    assert raising[3][3] == 0
    assert lowering[0][1] == pytest.approx(1.0)
    assert lowering[1][2] == pytest.approx(math.sqrt(2.0))
    assert raising[1][0] == pytest.approx(1.0)
    assert raising[2][1] == pytest.approx(math.sqrt(2.0))


@pytest.mark.parametrize("dimension", [0, -1])
def test_truncated_oscillator_rejects_bad_dimension(dimension):
    with pytest.raises(ValueError):
        truncated_annihilation(dimension)
    with pytest.raises(ValueError):
        truncated_creation(dimension)


def test_liouvillian_resolvent_poles_are_transition_frequencies():
    values = [1.0, 2.0, 3.0]
    assert liouvillian_resolvent(values, 0.5) == pytest.approx(
        resolvent_diagonal(liouvillian_eigenvalues(values), 0.5)
    )
    for z in (0.0, 1.0, 2.0):
        with pytest.raises(ValueError):
            liouvillian_resolvent(values, z)
    with pytest.raises(ValueError):
        liouvillian_resolvent([1.0, 1.0], 0.0)


@pytest.mark.parametrize("values", [(), [math.inf], [math.nan]])
def test_resolvent_rejects_bad_eigenvalues(values):
    with pytest.raises(ValueError):
        resolvent_diagonal(values, 0.0)


@pytest.mark.parametrize("z", [math.inf, math.nan, complex(math.inf, 0.0)])
def test_resolvent_rejects_bad_z(z):
    with pytest.raises(ValueError):
        resolvent_diagonal([1.0], z)


def test_trace_rejects_invalid_matrices():
    with pytest.raises(ValueError):
        trace(())
    with pytest.raises(ValueError):
        trace(((1.0, 0.0),))


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
