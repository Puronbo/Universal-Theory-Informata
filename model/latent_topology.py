"""Exact Vietoris--Rips persistence in dimensions 0 and 1.

The module computes the persistent homology of a finite point cloud over
:math:`\\mathbb{F}_2` by reducing the boundary matrix of the Rips complex,
truncated at dimension two (triangles are needed to kill one-dimensional
classes). It is intended for small clouds: the triangle count grows cubically
and the reduction is the dominant cost.

The intended use is diagnostic, not predictive. A data manifold with a hole has
a long-lived :math:`H_1` bar, and the death scale of that bar is the scale at
which the hole closes. A cluster has no such bar. That distinction is measured
in the demo, not assumed here.
"""

from __future__ import annotations

import itertools
import math
from collections.abc import Mapping, Sequence

__all__ = [
    "Point",
    "betti_at",
    "distance_matrix",
    "dominant_bar",
    "euclidean",
    "hole_scale",
    "persistence_diagram",
    "rips_persistence",
]

Point = tuple[float, ...]


def euclidean(left: Point, right: Point) -> float:
    """Return the Euclidean distance between two points.

    Args:
        left: First point.
        right: Second point.

    Returns:
        The distance.

    Raises:
        ValueError: If the points have different dimensions.
    """
    if len(left) != len(right):
        raise ValueError("points must have the same dimension")
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(left, right, strict=False)))


def distance_matrix(points: Sequence[Point]) -> list[list[float]]:
    """Return the full symmetric distance matrix of ``points``.

    Args:
        points: Finite point cloud.

    Returns:
        A list of rows with zero diagonal and symmetric entries.

    Raises:
        ValueError: If a point has a different dimension from the first.
    """
    if not points:
        return []
    dimension = len(points[0])
    for point in points:
        if len(point) != dimension:
            raise ValueError("points must have the same dimension")
    size = len(points)
    matrix = [[0.0] * size for _ in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            distance = euclidean(points[i], points[j])
            matrix[i][j] = distance
            matrix[j][i] = distance
    return matrix


def rips_persistence(
    points: Sequence[Point], max_scale: float = math.inf
) -> dict[int, list[tuple[float, float]]]:
    """Return the Rips persistence bars in dimensions 0 and 1.

    Simplices are included up to ``max_scale``; a one-dimensional class that
    would die beyond the truncation is reported as essential, so a finite
    ``max_scale`` can create spurious infinite bars.

    Args:
        points: Finite point cloud.
        max_scale: Largest filtration value retained.

    Returns:
        Bars ``(birth, death)`` keyed by dimension. Death is ``math.inf`` for
        essential classes.

    Raises:
        ValueError: If ``max_scale`` is negative or NaN, or points disagree in
            dimension.
    """
    if math.isnan(max_scale):
        raise ValueError("max_scale must not be NaN")
    if max_scale < 0:
        raise ValueError(f"max_scale must be non-negative, got {max_scale}")
    size = len(points)
    if size == 0:
        return {0: [], 1: []}

    matrix = distance_matrix(points)
    simplices: list[tuple[float, int, tuple[int, ...]]] = [
        (0.0, 0, (index,)) for index in range(size)
    ]
    for i in range(size):
        for j in range(i + 1, size):
            weight = matrix[i][j]
            if weight <= max_scale:
                simplices.append((weight, 1, (i, j)))
    for i in range(size):
        for j in range(i + 1, size):
            weight_ij = matrix[i][j]
            if weight_ij > max_scale:
                continue
            for k in range(j + 1, size):
                weight = max(weight_ij, matrix[i][k], matrix[j][k])
                if weight <= max_scale:
                    simplices.append((weight, 2, (i, j, k)))

    simplices.sort(key=lambda simplex: (simplex[0], simplex[1]))
    index = {
        (dimension, vertices): position
        for position, (_, dimension, vertices) in enumerate(simplices)
    }

    columns: list[int] = []
    for _, dimension, vertices in simplices:
        mask = 0
        if dimension:
            for face in itertools.combinations(vertices, dimension):
                mask |= 1 << index[(dimension - 1, face)]
        columns.append(mask)

    reduced = [0] * len(columns)
    pivot_column: dict[int, int] = {}
    pairs: list[tuple[int, int]] = []
    for position, column in enumerate(columns):
        while column:
            pivot = column.bit_length() - 1
            occupant = pivot_column.get(pivot)
            if occupant is None:
                pivot_column[pivot] = position
                reduced[position] = column
                pairs.append((pivot, position))
                break
            column ^= reduced[occupant]

    bars: dict[int, list[tuple[float, float]]] = {}
    paired: set[int] = set()
    deaths: set[int] = set()
    for birth, death in pairs:
        dimension = simplices[birth][1]
        bars.setdefault(dimension, []).append((simplices[birth][0], simplices[death][0]))
        paired.add(birth)
        deaths.add(death)
    for position, (weight, dimension, _) in enumerate(simplices):
        if dimension <= 1 and position not in paired and position not in deaths:
            bars.setdefault(dimension, []).append((weight, math.inf))
    for values in bars.values():
        values.sort(key=lambda bar: (bar[0], bar[1]))
    bars.setdefault(0, [])
    bars.setdefault(1, [])
    return bars


def betti_at(bars: Mapping[int, Sequence[tuple[float, float]]], scale: float) -> dict[int, int]:
    """Return the Betti numbers at ``scale``.

    Args:
        bars: Persistence bars keyed by dimension.
        scale: Filtration value.

    Returns:
        A mapping from dimension to the number of bars alive at ``scale``.
    """
    return {
        dimension: sum(1 for birth, death in values if birth <= scale < death)
        for dimension, values in bars.items()
    }


def persistence_diagram(
    bars: Mapping[int, Sequence[tuple[float, float]]],
) -> list[tuple[int, float, float]]:
    """Return ``(dimension, birth, death)`` triples sorted by dimension.

    Args:
        bars: Persistence bars keyed by dimension.

    Returns:
        A flat, deterministic list.
    """
    return [
        (dimension, birth, death) for dimension in sorted(bars) for birth, death in bars[dimension]
    ]


def dominant_bar(
    bars: Mapping[int, Sequence[tuple[float, float]]], dimension: int = 1
) -> tuple[float, float] | None:
    """Return the finite bar of ``dimension`` with the largest persistence.

    Args:
        bars: Persistence bars keyed by dimension.
        dimension: Homology dimension to inspect.

    Returns:
        The dominant bar, or ``None`` if the dimension has no finite bar.
    """
    finite = [(birth, death) for birth, death in bars.get(dimension, []) if math.isfinite(death)]
    if not finite:
        return None
    return max(finite, key=lambda bar: bar[1] - bar[0])


def hole_scale(points: Sequence[Point], max_scale: float = math.inf) -> float | None:
    """Return the persistence of the dominant one-dimensional class.

    Args:
        points: Finite point cloud.
        max_scale: Truncation passed to :func:`rips_persistence`.

    Returns:
        ``death - birth`` of the dominant :math:`H_1` bar, or ``None`` when
        there is no finite one. A return of ``0.0`` means every one-dimensional
        class dies at birth: there is no hole at any scale.
    """
    bar = dominant_bar(rips_persistence(points, max_scale=max_scale), dimension=1)
    return None if bar is None else bar[1] - bar[0]
