"""Tests for the Rips persistence helpers."""

from __future__ import annotations

import math
import random

import pytest

from model.latent_topology import (
    betti_at,
    distance_matrix,
    dominant_bar,
    euclidean,
    hole_scale,
    persistence_diagram,
    rips_persistence,
)


def annulus(count: int, inner: float, outer: float, seed: int) -> list[tuple[float, float]]:
    rng = random.Random(seed)
    points = []
    for _ in range(count):
        radius = math.sqrt(rng.uniform(inner**2, outer**2))
        angle = rng.uniform(0.0, 2.0 * math.pi)
        points.append((radius * math.cos(angle), radius * math.sin(angle)))
    return points


def test_euclidean_three_four_five() -> None:
    assert euclidean((0.0, 0.0), (3.0, 4.0)) == pytest.approx(5.0)


def test_euclidean_rejects_dimension_mismatch() -> None:
    with pytest.raises(ValueError, match="same dimension"):
        euclidean((0.0,), (0.0, 1.0))


def test_distance_matrix_is_symmetric_with_zero_diagonal() -> None:
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 2.0)]
    matrix = distance_matrix(points)
    assert matrix[0][0] == 0.0
    assert matrix[0][1] == matrix[1][0] == 1.0
    assert matrix[0][2] == matrix[2][0] == 2.0


def test_distance_matrix_empty() -> None:
    assert distance_matrix([]) == []


def test_distance_matrix_rejects_mixed_dimensions() -> None:
    with pytest.raises(ValueError, match="same dimension"):
        distance_matrix([(0.0, 0.0), (1.0,)])


def test_rips_empty() -> None:
    assert rips_persistence([]) == {0: [], 1: []}


def test_rips_single_point_is_essential() -> None:
    bars = rips_persistence([(0.0, 0.0)])
    assert bars[0] == [(0.0, math.inf)]
    assert bars[1] == []


def test_rips_two_points_merge_at_their_distance() -> None:
    bars = rips_persistence([(0.0, 0.0), (3.0, 0.0)])
    assert bars[0] == [(0.0, 3.0), (0.0, math.inf)]
    assert bars[1] == []


def test_rips_equilateral_triangle_has_no_persistent_cycle() -> None:
    side = 1.0
    height = math.sqrt(3.0) / 2.0
    points = [(0.0, 0.0), (side, 0.0), (0.5, height)]
    bars = rips_persistence(points)
    finite_h1 = [bar for bar in bars[1] if math.isfinite(bar[1])]
    assert len(finite_h1) == 1
    birth, death = finite_h1[0]
    assert death - birth == pytest.approx(0.0, abs=1e-12)


def test_rips_square_has_one_cycle_that_dies_at_the_diagonal() -> None:
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    bars = rips_persistence(points)
    # The extra finite bars have zero persistence: they die as soon as the
    # triangle that kills them is born.
    finite_h1 = [bar for bar in bars[1] if math.isfinite(bar[1]) and bar[1] - bar[0] > 1e-12]
    assert len(finite_h1) == 1
    birth, death = finite_h1[0]
    assert birth == pytest.approx(1.0)
    assert death == pytest.approx(math.sqrt(2.0))


def test_rips_square_h0_has_three_finite_merges() -> None:
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    bars = rips_persistence(points)
    finite_h0 = [bar for bar in bars[0] if math.isfinite(bar[1])]
    assert len(finite_h0) == 3
    assert all(death == pytest.approx(1.0) for _, death in finite_h0)


def test_rips_max_scale_truncates_distant_edges() -> None:
    bars = rips_persistence([(0.0, 0.0), (10.0, 0.0)], max_scale=1.0)
    assert bars[0] == [(0.0, math.inf), (0.0, math.inf)]


def test_rips_max_scale_skips_triangles_above_the_cutoff() -> None:
    # The 0-1 edge is inside the cutoff, but any triangle on 0-1 also needs
    # the long 1-2 edge, so no 2-simplex is born.
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 2.0)]
    bars = rips_persistence(points, max_scale=1.5)
    finite_h1 = [bar for bar in bars[1] if math.isfinite(bar[1])]
    assert finite_h1 == []
    assert sum(1 for _, death in bars[0] if death == math.inf) == 2


def test_rips_truncation_can_leave_a_cycle_essential() -> None:
    # The unit square keeps its cycle at max_scale=1.2: the diagonals that
    # would fill it are above the cutoff, so the one-dimensional class is
    # reported as essential even though it is not a hole in the full complex.
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    bars = rips_persistence(points, max_scale=1.2)
    assert (1.0, math.inf) in bars[1]


def test_rips_rejects_negative_max_scale() -> None:
    with pytest.raises(ValueError, match="max_scale must be non-negative"):
        rips_persistence([(0.0, 0.0)], max_scale=-1.0)


def test_rips_rejects_nan_max_scale() -> None:
    with pytest.raises(ValueError, match="must not be NaN"):
        rips_persistence([(0.0, 0.0)], max_scale=math.nan)


def test_betti_at_counts_live_bars() -> None:
    bars = {0: [(0.0, 1.0), (0.0, math.inf)], 1: [(1.0, 2.0)]}
    assert betti_at(bars, 0.5) == {0: 2, 1: 0}
    assert betti_at(bars, 1.5) == {0: 1, 1: 1}
    assert betti_at(bars, 3.0) == {0: 1, 1: 0}


def test_persistence_diagram_is_sorted_by_dimension() -> None:
    bars = {1: [(2.0, 3.0)], 0: [(0.0, 1.0)]}
    assert persistence_diagram(bars) == [(0, 0.0, 1.0), (1, 2.0, 3.0)]


def test_dominant_bar_returns_none_without_finite_bars() -> None:
    assert dominant_bar({1: [(0.0, math.inf)]}) is None


def test_dominant_bar_picks_the_longest_finite_bar() -> None:
    bars = {1: [(0.0, 0.5), (0.2, 1.6), (0.4, 0.6)]}
    assert dominant_bar(bars) == (0.2, 1.6)


def test_hole_scale_is_small_for_a_blob_and_large_for_an_annulus() -> None:
    ring = hole_scale(annulus(40, 0.75, 1.0, seed=1))
    assert ring is not None and ring > 0.5

    rng = random.Random(1)
    blob = []
    for _ in range(40):
        radius = math.sqrt(rng.uniform(0.0, 1.0))
        angle = rng.uniform(0.0, 2.0 * math.pi)
        blob.append((radius * math.cos(angle), radius * math.sin(angle)))
    flat = hole_scale(blob)
    assert flat is not None and flat < 0.5


def test_hole_scale_is_zero_for_a_collinear_set() -> None:
    # Points on a line create only cycles that die at birth, so the dominant
    # H1 persistence is zero: there is no hole at any scale.
    assert hole_scale([(0.0, 0.0), (1.0, 0.0), (2.0, 0.0)]) == pytest.approx(0.0)
