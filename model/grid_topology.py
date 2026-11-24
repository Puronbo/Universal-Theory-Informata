"""Puncture versus hole on a finite square lattice.

The Fold corpus's ledger distinguishes a cap, a puncture, and an annulus by the
triple ``(chi, boundary, punctures)``. This module asks what survives when the
surface is sampled by a square lattice of closed cells.

A cell complex cannot hold a point puncture. Removing one cell removes a
two-dimensional cell and creates a boundary, so every lattice hole is a small
annulus at the combinatorial level: its Euler characteristic is zero and its
complement has one bounded component, exactly like a thin annulus. The puncture
survives only as a metric limit, a hole whose inradius is one lattice step.

``grid_hole_depth`` is that inradius in lattice steps: the largest number of
four-connected steps from a foreground cell to a bounded background cell. A
one-cell puncture has depth exactly one at every resolution, so its physical
scale is the lattice step and shrinks to zero under refinement. A hole of fixed
physical radius has a depth that grows as the step shrinks, and its physical
scale stays fixed.

This is standard distance-transform geometry, not a new invariant. The
measurement is in ``PUNCTURE_RESOLUTION.md``.
"""

from __future__ import annotations

import math
from collections import deque
from collections.abc import Iterable

__all__ = [
    "Cell",
    "bounded_background_components",
    "disk_cells",
    "grid_hole_depth",
    "grid_hole_scale",
    "hole_is_resolved",
    "lattice_euler_characteristic",
    "lattice_step",
]

Cell = tuple[int, int]

_NEWS = ((-1, 0), (1, 0), (0, -1), (0, 1))


def _cell_parts(cell: Cell) -> Cell:
    """Return ``cell`` after checking that it is a pair of integers."""
    if len(cell) != 2:
        raise ValueError("cells must be (row, column) pairs")
    row, column = cell
    if (
        isinstance(row, bool)
        or isinstance(column, bool)
        or not isinstance(row, int)
        or not isinstance(column, int)
    ):
        raise ValueError("cell coordinates must be integers")
    return (row, column)


def _checked_cells(cells: Iterable[Cell], size: int) -> set[Cell]:
    """Return ``cells`` as a set, rejecting coordinates outside the lattice."""
    result: set[Cell] = set()
    for cell in cells:
        row, column = _cell_parts(cell)
        if not (0 <= row < size and 0 <= column < size):
            raise ValueError(f"cell {(row, column)} lies outside a {size}x{size} lattice")
        result.add((row, column))
    return result


def _on_border(cell: Cell, size: int) -> bool:
    """Return whether ``cell`` touches the outer edge of the lattice."""
    row, column = cell
    return row in (0, size - 1) or column in (0, size - 1)


def lattice_step(size: int, span: float = 3.0) -> float:
    """Return the physical width of one cell of a square lattice.

    The lattice spans ``[-span/2, span/2]`` in both directions.

    Args:
        size: Number of cells per side.
        span: Physical side length of the lattice.

    Returns:
        ``span / (size - 1)``.

    Raises:
        ValueError: If ``size`` is less than two, or ``span`` is not finite and
            positive.
    """
    if size < 2:
        raise ValueError(f"size must be at least 2, got {size}")
    if not math.isfinite(span) or span <= 0:
        raise ValueError(f"span must be finite and positive, got {span}")
    return span / (size - 1)


def disk_cells(
    size: int,
    radius: float,
    inner: float = 0.0,
    puncture: bool = False,
    span: float = 3.0,
) -> set[Cell]:
    """Sample a disk, an annulus, or a punctured disk on a square lattice.

    A cell is included when its centre lies between ``inner`` and ``radius``
    from the origin. With ``puncture`` set, the centre cell is removed after
    sampling; this is the lattice shadow of removing a point.

    Args:
        size: Number of cells per side.
        radius: Outer radius of the mask.
        inner: Inner radius; zero gives a disk.
        puncture: Remove the centre cell.
        span: Physical side length of the lattice.

    Returns:
        The included cells.

    Raises:
        ValueError: If ``size``, ``radius``, ``inner``, or ``span`` is invalid,
            if ``inner`` is not smaller than ``radius``, or if a puncture is
            requested where the centre cell is not foreground.
    """
    if not math.isfinite(radius) or radius <= 0:
        raise ValueError(f"radius must be finite and positive, got {radius}")
    if not math.isfinite(inner) or inner < 0:
        raise ValueError(f"inner must be finite and non-negative, got {inner}")
    if inner >= radius:
        raise ValueError(f"inner must be smaller than radius, got {inner} >= {radius}")
    step = lattice_step(size, span)
    offset = 0.5 * span
    centre = size // 2
    cells: set[Cell] = set()
    for row in range(size):
        y = -offset + row * step
        for column in range(size):
            x = -offset + column * step
            squared = x * x + y * y
            if inner * inner <= squared <= radius * radius:
                cells.add((row, column))
    if puncture:
        hole = (centre, centre)
        if hole not in cells:
            raise ValueError("puncture requires the centre cell to be foreground")
        cells.remove(hole)
    return cells


def bounded_background_components(cells: Iterable[Cell], size: int) -> list[set[Cell]]:
    """Return the four-connected background components that do not touch the border.

    A component touching the border is connected to the outside of the lattice
    and is not a hole. The result is sorted by the component's smallest cell so
    that repeated calls are deterministic.

    Args:
        cells: Foreground cells.
        size: Number of cells per side.

    Returns:
        Bounded background components, each a set of cells.

    Raises:
        ValueError: If ``size`` is less than two, or a cell is malformed or
            outside the lattice.
    """
    if size < 2:
        raise ValueError(f"size must be at least 2, got {size}")
    foreground = _checked_cells(cells, size)
    remaining = {(row, column) for row in range(size) for column in range(size)}
    remaining -= foreground
    components: list[set[Cell]] = []
    while remaining:
        start = remaining.pop()
        component = {start}
        stack = [start]
        touches_border = _on_border(start, size)
        while stack:
            row, column = stack.pop()
            for delta_row, delta_column in _NEWS:
                neighbour = (row + delta_row, column + delta_column)
                if neighbour in remaining:
                    remaining.remove(neighbour)
                    component.add(neighbour)
                    stack.append(neighbour)
                    if _on_border(neighbour, size):
                        touches_border = True
        if not touches_border:
            components.append(component)
    components.sort(key=min)
    return components


def grid_hole_depth(cells: Iterable[Cell], size: int) -> int:
    """Return the largest four-step distance from foreground to a bounded background cell.

    The distance is zero for foreground cells. A one-cell puncture has depth
    one; a hole is resolved when at least one of its cells is two or more steps
    from the foreground.

    Args:
        cells: Foreground cells.
        size: Number of cells per side.

    Returns:
        The depth in lattice cells. Zero means there is no bounded background
        component, so there is no hole at this resolution.

    Raises:
        ValueError: If ``size`` is less than two, or a cell is malformed or
            outside the lattice.
    """
    if size < 2:
        raise ValueError(f"size must be at least 2, got {size}")
    foreground = _checked_cells(cells, size)
    bounded = bounded_background_components(foreground, size)
    if not bounded:
        return 0
    distances: dict[Cell, int] = dict.fromkeys(foreground, 0)
    queue = deque(foreground)
    while queue:
        row, column = queue.popleft()
        distance = distances[(row, column)] + 1
        for delta_row, delta_column in _NEWS:
            neighbour = (row + delta_row, column + delta_column)
            if 0 <= neighbour[0] < size and 0 <= neighbour[1] < size and neighbour not in distances:
                distances[neighbour] = distance
                queue.append(neighbour)
    return max(max(distances[cell] for cell in component) for component in bounded)


def grid_hole_scale(cells: Iterable[Cell], size: int, step: float) -> float:
    """Return the physical inradius of the largest bounded background component.

    Args:
        cells: Foreground cells.
        size: Number of cells per side.
        step: Physical width of one cell.

    Returns:
        ``grid_hole_depth(cells, size) * step``; zero when there is no hole.

    Raises:
        ValueError: If ``step`` is not finite and positive, or the lattice or a
            cell is invalid.
    """
    if not math.isfinite(step) or step <= 0:
        raise ValueError(f"step must be finite and positive, got {step}")
    return grid_hole_depth(cells, size) * step


def hole_is_resolved(cells: Iterable[Cell], size: int) -> bool:
    """Return whether the hole has a cell at least two lattice steps deep.

    Depth one is the minimal nonzero value. It is produced by a one-cell
    puncture, and also by any hole whose inradius is one step (for example a
    two-by-two block). Such a hole cannot be told from a puncture by this
    measure.

    Args:
        cells: Foreground cells.
        size: Number of cells per side.

    Returns:
        ``True`` when ``grid_hole_depth`` is at least two.

    Raises:
        ValueError: If ``size`` is less than two, or a cell is malformed or
            outside the lattice.
    """
    return grid_hole_depth(cells, size) >= 2


def lattice_euler_characteristic(cells: Iterable[Cell]) -> int:
    """Return the Euler characteristic of the union of closed cells.

    For a finite cell complex, ``chi = V - E + F``. A disk has ``chi = 1``; a
    one-cell puncture and an annulus both have ``chi = 0``. The function does
    not need a lattice size because it only uses the cells themselves.

    Args:
        cells: Present cells.

    Returns:
        The Euler characteristic.

    Raises:
        ValueError: If a cell is not a pair of integers.
    """
    faces = {_cell_parts(cell) for cell in cells}
    vertices: set[tuple[int, int]] = set()
    edges: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    for row, column in faces:
        corners = (
            (row, column),
            (row + 1, column),
            (row + 1, column + 1),
            (row, column + 1),
        )
        vertices.update(corners)
        for first, second in zip(corners, corners[1:] + corners[:1], strict=True):
            edges.add((first, second) if first <= second else (second, first))
    return len(vertices) - len(edges) + len(faces)
