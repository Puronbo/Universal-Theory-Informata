"""Tests for the lattice puncture/hole helpers."""

from __future__ import annotations

import math

import pytest

from model.grid_topology import (
    bounded_background_components,
    disk_cells,
    grid_hole_depth,
    grid_hole_scale,
    hole_is_resolved,
    lattice_euler_characteristic,
    lattice_step,
)


def full_grid(size: int) -> set[tuple[int, int]]:
    """Return every cell of a square lattice."""
    return {(row, column) for row in range(size) for column in range(size)}


def test_lattice_step_centres_a_span() -> None:
    assert lattice_step(21) == pytest.approx(0.15)
    assert lattice_step(2, span=1.0) == pytest.approx(1.0)


def test_lattice_step_rejects_small_size() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        lattice_step(1)


@pytest.mark.parametrize("span", [0.0, -1.0, math.inf, math.nan])
def test_lattice_step_rejects_bad_span(span: float) -> None:
    with pytest.raises(ValueError, match="finite and positive"):
        lattice_step(5, span=span)


def test_disk_cells_is_a_disk() -> None:
    cells = disk_cells(21, 1.0)
    assert (10, 10) in cells
    assert lattice_euler_characteristic(cells) == 1


def test_disk_cells_annulus_has_a_hole() -> None:
    cells = disk_cells(21, 1.0, inner=0.3)
    assert (10, 10) not in cells
    assert lattice_euler_characteristic(cells) == 0


def test_disk_cells_puncture_removes_only_the_centre() -> None:
    disk = disk_cells(21, 1.0)
    punctured = disk_cells(21, 1.0, puncture=True)
    assert punctured == disk - {(10, 10)}


def test_disk_cells_puncture_requires_a_foreground_centre() -> None:
    with pytest.raises(ValueError, match="centre cell"):
        disk_cells(21, 0.1, inner=0.05, puncture=True)


@pytest.mark.parametrize("radius", [0.0, -1.0, math.inf, math.nan])
def test_disk_cells_rejects_bad_radius(radius: float) -> None:
    with pytest.raises(ValueError, match="radius must be finite and positive"):
        disk_cells(21, radius)


@pytest.mark.parametrize("inner", [-0.1, math.inf, math.nan])
def test_disk_cells_rejects_bad_inner(inner: float) -> None:
    with pytest.raises(ValueError, match="inner must be finite and non-negative"):
        disk_cells(21, 1.0, inner=inner)


def test_disk_cells_rejects_inner_not_smaller_than_radius() -> None:
    with pytest.raises(ValueError, match="smaller than radius"):
        disk_cells(21, 1.0, inner=1.0)


def test_bounded_components_of_a_disk_are_empty() -> None:
    assert bounded_background_components(disk_cells(21, 1.0), 21) == []


def test_bounded_components_of_a_puncture_is_one_cell() -> None:
    components = bounded_background_components(disk_cells(21, 1.0, puncture=True), 21)
    assert components == [{(10, 10)}]


def test_bounded_components_are_sorted() -> None:
    components = bounded_background_components(full_grid(9) - {(2, 2), (6, 6)}, 9)
    assert components == [{(2, 2)}, {(6, 6)}]


def test_bounded_components_reject_small_size() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        bounded_background_components(set(), 1)


def test_bounded_components_reject_outside_cells() -> None:
    with pytest.raises(ValueError, match="outside"):
        bounded_background_components({(0, 5)}, 5)


@pytest.mark.parametrize("cell", [(0,), (0.0, 1.0), (True, 0)])
def test_bounded_components_reject_malformed_cells(cell: tuple[object, ...]) -> None:
    with pytest.raises(ValueError):
        bounded_background_components({cell}, 5)  # type: ignore[arg-type]


def test_depth_is_zero_without_a_hole() -> None:
    assert grid_hole_depth(disk_cells(21, 1.0), 21) == 0
    assert grid_hole_depth(set(), 5) == 0
    assert grid_hole_depth(full_grid(5), 5) == 0


def test_puncture_depth_is_one_at_every_size() -> None:
    for size in (21, 41, 81):
        assert grid_hole_depth(disk_cells(size, 1.0, puncture=True), size) == 1


def test_depth_tracks_the_annulus_radius() -> None:
    assert grid_hole_depth(disk_cells(21, 1.0, inner=0.3), 21) == 2
    assert grid_hole_depth(disk_cells(41, 1.0, inner=0.3), 41) == 4
    assert grid_hole_depth(disk_cells(81, 1.0, inner=0.3), 81) == 8


def test_depth_is_one_for_a_two_by_two_block() -> None:
    block = {(3, 3), (3, 4), (4, 3), (4, 4)}
    assert grid_hole_depth(full_grid(9) - block, 9) == 1


def test_depth_is_two_for_a_three_by_three_block() -> None:
    block = {(row, column) for row in (3, 4, 5) for column in (3, 4, 5)}
    assert grid_hole_depth(full_grid(9) - block, 9) == 2


def test_depth_rejects_small_size() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        grid_hole_depth(set(), 1)


def test_scale_is_depth_times_step() -> None:
    cells = disk_cells(41, 1.0, inner=0.3)
    assert grid_hole_scale(cells, 41, 0.075) == pytest.approx(0.3)


def test_scale_of_a_puncture_is_the_step() -> None:
    cells = disk_cells(41, 1.0, puncture=True)
    assert grid_hole_scale(cells, 41, 0.075) == pytest.approx(0.075)


@pytest.mark.parametrize("step", [0.0, -0.1, math.inf, math.nan])
def test_scale_rejects_bad_step(step: float) -> None:
    with pytest.raises(ValueError, match="finite and positive"):
        grid_hole_scale(set(), 5, step)


def test_hole_is_resolved_at_depth_two() -> None:
    assert not hole_is_resolved(disk_cells(21, 1.0, puncture=True), 21)
    assert hole_is_resolved(disk_cells(21, 1.0, inner=0.3), 21)
    block = {(3, 3), (3, 4), (4, 3), (4, 4)}
    assert not hole_is_resolved(full_grid(9) - block, 9)


def test_a_subresolution_annulus_reads_as_a_puncture() -> None:
    coarse = disk_cells(21, 1.0, inner=0.1)
    assert grid_hole_depth(coarse, 21) == 1
    assert not hole_is_resolved(coarse, 21)
    fine = disk_cells(41, 1.0, inner=0.1)
    assert grid_hole_depth(fine, 41) == 2
    assert hole_is_resolved(fine, 41)


def test_a_subresolution_annulus_is_the_same_cell_set_as_a_puncture() -> None:
    # At this step the annulus has no cell between the centre and the next
    # ring, so the two different surfaces produce the same lattice object.
    assert disk_cells(21, 1.0, inner=0.1) == disk_cells(21, 1.0, puncture=True)


def test_chi_and_bounded_components_do_not_separate_puncture_from_annulus() -> None:
    puncture = disk_cells(41, 1.0, puncture=True)
    annulus = disk_cells(41, 1.0, inner=0.3)
    assert lattice_euler_characteristic(puncture) == 0
    assert lattice_euler_characteristic(annulus) == 0
    assert len(bounded_background_components(puncture, 41)) == 1
    assert len(bounded_background_components(annulus, 41)) == 1
    assert grid_hole_depth(puncture, 41) == 1
    assert grid_hole_depth(annulus, 41) == 4


def test_euler_of_a_single_cell() -> None:
    assert lattice_euler_characteristic({(0, 0)}) == 1


def test_euler_of_a_two_by_two_block() -> None:
    block = {(row, column) for row in (0, 1) for column in (0, 1)}
    assert lattice_euler_characteristic(block) == 1


def test_euler_of_a_ring_is_zero() -> None:
    ring = {(row, column) for row in (0, 1, 2) for column in (0, 1, 2)} - {(1, 1)}
    assert lattice_euler_characteristic(ring) == 0


def test_euler_of_the_empty_set_is_zero() -> None:
    assert lattice_euler_characteristic(set()) == 0


@pytest.mark.parametrize("cell", [(0,), (0.0, 1.0), (True, 0)])
def test_euler_rejects_malformed_cells(cell: tuple[object, ...]) -> None:
    with pytest.raises(ValueError):
        lattice_euler_characteristic({cell})  # type: ignore[arg-type]
