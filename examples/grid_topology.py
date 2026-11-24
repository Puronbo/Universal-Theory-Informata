"""Measure whether the cap/puncture ledger survives a finite lattice.

Run from the repository root:

    python examples/grid_topology.py

A one-cell puncture is a square hole. On the lattice it has the same Euler
characteristic (zero) and the same number of bounded background components
(one) as a thin annulus. The difference is metric: the puncture's inradius is
one lattice step at every resolution, so its physical scale vanishes under
refinement, while a fixed annulus keeps its physical scale. The printed depths
are the measurement.
"""

from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.grid_topology import (
    bounded_background_components,
    disk_cells,
    grid_hole_depth,
    grid_hole_scale,
    hole_is_resolved,
    lattice_euler_characteristic,
    lattice_step,
)

SIZES = (21, 41, 81, 161)
MASKS = (
    ("disk", {"radius": 1.0}),
    ("puncture", {"radius": 1.0, "puncture": True}),
    ("annulus 0.3", {"radius": 1.0, "inner": 0.3}),
    ("annulus 0.1", {"radius": 1.0, "inner": 0.1}),
)


def log_log_slope(steps: list[float], scales: list[float]) -> float:
    """Return the least-squares slope of ``log(scale)`` against ``log(step)``."""
    xs = [math.log(step) for step in steps]
    ys = [math.log(scale) for scale in scales]
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    return sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys, strict=True)) / sum(
        (x - mean_x) ** 2 for x in xs
    )


def main() -> None:
    """Print the lattice table and the refinement slopes."""
    print("== lattice: Euler characteristic, bounded components, and depth ==")
    print(
        f"{'size':>5} {'step':>8} {'mask':>12} {'chi':>4} {'bg':>3} "
        f"{'depth':>5} {'scale':>8} {'resolved':>8}"
    )
    for size in SIZES:
        step = lattice_step(size)
        for name, options in MASKS:
            cells = disk_cells(size, **options)
            chi = lattice_euler_characteristic(cells)
            background = len(bounded_background_components(cells, size))
            depth = grid_hole_depth(cells, size)
            scale = grid_hole_scale(cells, size, step)
            resolved = hole_is_resolved(cells, size)
            print(
                f"{size:>5} {step:>8.5f} {name:>12} {chi:>4} {background:>3} "
                f"{depth:>5} {scale:>8.5f} {str(resolved):>8}"
            )
    print()

    print("== refinement: depth in lattice cells ==")
    print(f"{'size':>5} {'step':>8} {'puncture':>9} {'annulus 0.3':>12} {'annulus 0.1':>12}")
    steps: list[float] = []
    for size in SIZES:
        step = lattice_step(size)
        steps.append(step)
        values = [grid_hole_depth(disk_cells(size, **options), size) for _, options in MASKS[1:]]
        print(f"{size:>5} {step:>8.5f} {values[0]:>9} {values[1]:>12} {values[2]:>12}")
    print()

    print("== refinement: physical scale ==")
    print(f"{'size':>5} {'step':>8} {'puncture':>9} {'annulus 0.3':>12} {'annulus 0.1':>12}")
    scales: dict[str, list[float]] = {name: [] for name, _ in MASKS[1:]}
    for size in SIZES:
        step = lattice_step(size)
        values = [
            grid_hole_scale(disk_cells(size, **options), size, step) for _, options in MASKS[1:]
        ]
        for name, value in zip(scales, values, strict=True):
            scales[name].append(value)
        print(f"{size:>5} {step:>8.5f} {values[0]:>9.5f} {values[1]:>12.5f} {values[2]:>12.5f}")
    print()

    print("log-log slope of physical scale against step:")
    for name, values in scales.items():
        print(f"  {name:>12}: {log_log_slope(steps, values):.4f}")
    print()
    print("A one-cell puncture has depth 1 at every size, so its scale is the step")
    print("(slope 1). A fixed annulus keeps its scale (slope 0). The 0.1 annulus is")
    print("a puncture at size 21 and resolves at size 41: the lattice cannot tell a")
    print("hole smaller than its step from a point puncture.")


if __name__ == "__main__":
    main()
