"""Finite-dimensional Liouvillian and commutant zero modes.

For a Hamiltonian ``H`` and an observable ``A``, the Liouvillian is the
superoperator

    L_H(A) = [H, A] = H A - A H.

If ``H`` is self-adjoint, then ``L_H`` is self-adjoint with respect to the
Hilbert-Schmidt inner product. Its kernel is the commutant of ``H``: the
observables that are conserved under the dynamics. On eigen-operators
``|m><n|`` its eigenvalues are ``E_m - E_n``, the transition frequencies.

This is standard finite-dimensional linear algebra, included as tooling for the
source document's "operator for operators" idea. It is not a physical claim.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import TypeAlias

Matrix: TypeAlias = tuple[tuple[complex, ...], ...]


def _finite(value: complex) -> bool:
    return math.isfinite(value.real) and math.isfinite(value.imag)


def _validate_matrix(matrix: Matrix, name: str = "matrix") -> int:
    """Validate a non-empty square finite matrix and return its size."""
    if not matrix:
        raise ValueError(f"{name} must be non-empty")
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError(f"{name} must be square")
    for row in matrix:
        for entry in row:
            if not _finite(entry):
                raise ValueError(f"{name} entries must be finite")
    return size


def _validate_tolerance(tolerance: float) -> float:
    tolerance = float(tolerance)
    if not math.isfinite(tolerance) or tolerance < 0.0:
        raise ValueError("tolerance must be finite and >= 0")
    return tolerance


def identity(size: int) -> Matrix:
    """Return the ``size x size`` identity matrix.

    Raises:
        ValueError: If ``size`` is not positive.
    """
    if size < 1:
        raise ValueError("size must be >= 1")
    return tuple(
        tuple(complex(1.0) if i == j else complex(0.0) for j in range(size)) for i in range(size)
    )


def zero_matrix(size: int) -> Matrix:
    """Return the ``size x size`` zero matrix.

    Raises:
        ValueError: If ``size`` is not positive.
    """
    if size < 1:
        raise ValueError("size must be >= 1")
    return tuple(tuple(complex(0.0) for _ in range(size)) for _ in range(size))


def diagonal(values: Sequence[complex]) -> Matrix:
    """Return the diagonal matrix with ``values`` on the main diagonal.

    Raises:
        ValueError: If ``values`` is empty or contains a non-finite entry.
    """
    if not values:
        raise ValueError("values must be non-empty")
    entries = tuple(complex(value) for value in values)
    if any(not _finite(value) for value in entries):
        raise ValueError("values must be finite")
    size = len(entries)
    return tuple(
        tuple(entries[i] if i == j else complex(0.0) for j in range(size)) for i in range(size)
    )


def matmul(left: Matrix, right: Matrix) -> Matrix:
    """Return the matrix product ``left @ right``.

    Raises:
        ValueError: If the matrices are not finite square matrices of equal size.
    """
    size = _validate_matrix(left, "left")
    if _validate_matrix(right, "right") != size:
        raise ValueError("matrices must have the same dimensions")
    return tuple(
        tuple(
            sum(
                (left[i][k] * right[k][j] for k in range(size)),
                complex(0.0),
            )
            for j in range(size)
        )
        for i in range(size)
    )


def matadd(left: Matrix, right: Matrix) -> Matrix:
    """Return the element-wise sum.

    Raises:
        ValueError: If the matrices are not finite square matrices of equal size.
    """
    size = _validate_matrix(left, "left")
    if _validate_matrix(right, "right") != size:
        raise ValueError("matrices must have the same dimensions")
    return tuple(tuple(left[i][j] + right[i][j] for j in range(size)) for i in range(size))


def matsub(left: Matrix, right: Matrix) -> Matrix:
    """Return the element-wise difference.

    Raises:
        ValueError: If the matrices are not finite square matrices of equal size.
    """
    size = _validate_matrix(left, "left")
    if _validate_matrix(right, "right") != size:
        raise ValueError("matrices must have the same dimensions")
    return tuple(tuple(left[i][j] - right[i][j] for j in range(size)) for i in range(size))


def matscale(factor: complex, matrix: Matrix) -> Matrix:
    """Return ``factor * matrix``.

    Raises:
        ValueError: If ``factor`` or any matrix entry is not finite.
    """
    factor = complex(factor)
    if not _finite(factor):
        raise ValueError("factor must be finite")
    size = _validate_matrix(matrix)
    return tuple(tuple(factor * matrix[i][j] for j in range(size)) for i in range(size))


def dagger(matrix: Matrix) -> Matrix:
    """Return the conjugate transpose.

    Raises:
        ValueError: If ``matrix`` is not a finite square matrix.
    """
    size = _validate_matrix(matrix)
    return tuple(tuple(matrix[j][i].conjugate() for j in range(size)) for i in range(size))


def commutator(hamiltonian: Matrix, observable: Matrix) -> Matrix:
    """Return ``[H, A] = H A - A H``.

    Raises:
        ValueError: If the matrices are not finite square matrices of equal size.
    """
    return matsub(
        matmul(hamiltonian, observable),
        matmul(observable, hamiltonian),
    )


def liouvillian(hamiltonian: Matrix, observable: Matrix) -> Matrix:
    """Return the Liouvillian action ``L_H(A) = [H, A]``.

    Raises:
        ValueError: If the matrices are not finite square matrices of equal size.
    """
    return commutator(hamiltonian, observable)


def hilbert_schmidt(left: Matrix, right: Matrix) -> complex:
    """Return ``Tr(left^dagger right)``.

    Raises:
        ValueError: If the matrices are not finite square matrices of equal size.
    """
    size = _validate_matrix(left, "left")
    if _validate_matrix(right, "right") != size:
        raise ValueError("matrices must have the same dimensions")
    return sum(
        (left[i][j].conjugate() * right[i][j] for i in range(size) for j in range(size)),
        complex(0.0),
    )


def is_self_adjoint(matrix: Matrix, tolerance: float = 1e-12) -> bool:
    """Return whether ``matrix`` equals its conjugate transpose.

    Raises:
        ValueError: If ``matrix`` is invalid or ``tolerance`` is negative.
    """
    tolerance = _validate_tolerance(tolerance)
    size = _validate_matrix(matrix)
    adjoint = dagger(matrix)
    return all(
        abs(matrix[i][j] - adjoint[i][j]) <= tolerance for i in range(size) for j in range(size)
    )


def is_zero_matrix(matrix: Matrix, tolerance: float = 1e-12) -> bool:
    """Return whether every entry has magnitude at most ``tolerance``.

    Raises:
        ValueError: If ``matrix`` is invalid or ``tolerance`` is negative.
    """
    tolerance = _validate_tolerance(tolerance)
    size = _validate_matrix(matrix)
    return all(abs(matrix[i][j]) <= tolerance for i in range(size) for j in range(size))


def commutes(
    hamiltonian: Matrix,
    observable: Matrix,
    tolerance: float = 1e-12,
) -> bool:
    """Return whether ``[H, A]`` is zero within ``tolerance``.

    Raises:
        ValueError: If the matrices are invalid or ``tolerance`` is negative.
    """
    return is_zero_matrix(commutator(hamiltonian, observable), tolerance)


def liouvillian_eigenvalues(eigenvalues: Sequence[complex]) -> tuple[complex, ...]:
    """Return all transition frequencies ``E_m - E_n``.

    Raises:
        ValueError: If ``eigenvalues`` is empty or contains a non-finite entry.
    """
    if not eigenvalues:
        raise ValueError("eigenvalues must be non-empty")
    values = tuple(complex(value) for value in eigenvalues)
    if any(not _finite(value) for value in values):
        raise ValueError("eigenvalues must be finite")
    return tuple(values[m] - values[n] for m in range(len(values)) for n in range(len(values)))


def zero_mode_pairs(
    eigenvalues: Sequence[complex],
    tolerance: float = 1e-12,
) -> tuple[tuple[int, int], ...]:
    """Return ``(m, n)`` pairs with ``E_m == E_n`` within ``tolerance``.

    These are the basis zero modes of the Liouvillian for a diagonal
    Hamiltonian, i.e. a basis of its commutant.

    Raises:
        ValueError: If ``eigenvalues`` is invalid or ``tolerance`` is negative.
    """
    tolerance = _validate_tolerance(tolerance)
    if not eigenvalues:
        raise ValueError("eigenvalues must be non-empty")
    values = tuple(complex(value) for value in eigenvalues)
    if any(not _finite(value) for value in values):
        raise ValueError("eigenvalues must be finite")
    return tuple(
        (m, n)
        for m in range(len(values))
        for n in range(len(values))
        if abs(values[m] - values[n]) <= tolerance
    )


def commutant_dimension(
    eigenvalues: Sequence[complex],
    tolerance: float = 1e-12,
) -> int:
    """Return the dimension of the commutant of a diagonal Hamiltonian.

    Raises:
        ValueError: If ``eigenvalues`` is invalid or ``tolerance`` is negative.
    """
    return len(zero_mode_pairs(eigenvalues, tolerance))


__all__ = [
    "Matrix",
    "commutant_dimension",
    "commutes",
    "commutator",
    "dagger",
    "diagonal",
    "hilbert_schmidt",
    "identity",
    "is_self_adjoint",
    "is_zero_matrix",
    "liouvillian",
    "liouvillian_eigenvalues",
    "matadd",
    "matmul",
    "matscale",
    "matsub",
    "zero_matrix",
    "zero_mode_pairs",
]
