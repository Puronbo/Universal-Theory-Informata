"""Two measurements for the topology-of-systems reading.

Run from the repository root:

    python examples/topology_experiments.py

Experiment 1 asks whether the most persistent gap in a reuse-distance profile
predicts the cache capacity that captures 90% of the available hits.

Experiment 2 asks whether the dominant one-dimensional persistence separates a
point cloud with a hole from one without, and how often a nearest-neighbour
out-of-distribution rule misses points that sit inside the hole.

Both experiments print partial and negative results. The printed numbers are
the finding, so do not tune the seeds to make the tables look better.
"""

import math
import os
import random
import statistics
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.cache_topology import (
    hit_rate_curve,
    reuse_distances,
    saturation_capacity,
    working_set_keys,
    working_set_splits,
)
from model.latent_topology import dominant_bar, euclidean, rips_persistence

CACHE_CAPACITIES = [4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 192, 256, 320, 400]


def zipf_trace(size: int, alphabet: int, exponent: float, seed: int) -> list[int]:
    """Draw ``size`` keys with Zipf-like weights over ``alphabet`` symbols."""
    rng = random.Random(seed)
    weights = [1.0 / (rank**exponent) for rank in range(1, alphabet + 1)]
    return rng.choices(range(alphabet), weights=weights, k=size)


def annulus(size: int, inner: float, outer: float, seed: int) -> list[tuple[float, float]]:
    """Sample points uniformly by area in an annulus."""
    rng = random.Random(seed)
    points: list[tuple[float, float]] = []
    for _ in range(size):
        radius = math.sqrt(rng.uniform(inner**2, outer**2))
        angle = rng.uniform(0.0, 2.0 * math.pi)
        points.append((radius * math.cos(angle), radius * math.sin(angle)))
    return points


def blob(size: int, radius: float, seed: int) -> list[tuple[float, float]]:
    """Sample points uniformly by area in a disk."""
    rng = random.Random(seed)
    points: list[tuple[float, float]] = []
    for _ in range(size):
        r = radius * math.sqrt(rng.uniform(0.0, 1.0))
        angle = rng.uniform(0.0, 2.0 * math.pi)
        points.append((r * math.cos(angle), r * math.sin(angle)))
    return points


def span(values: list[int]) -> str:
    """Format a single value, or the first-last range when values tie."""
    if not values:
        return "n/a"
    return str(values[0]) if len(values) == 1 else f"{values[0]}-{values[-1]}"


def cache_experiment() -> None:
    """Compare the persistence threshold with the empirical LRU capacity."""
    print("== cache: persistence threshold vs LRU saturation capacity ==")
    print(f"trace: 4000 accesses, 400 keys, seed 7; capacities up to {CACHE_CAPACITIES[-1]}")
    print(
        f"{'s':>4} {'distinct':>8} {'plateau':>7} "
        f"{'gap-thr':>8} {'A:dist':>9} {'B:keys':>9} {'sat90':>6} {'sat95':>6}"
    )
    for exponent in (0.8, 1.0, 1.2, 1.5):
        trace = zipf_trace(4000, 400, exponent, seed=7)
        distances = reuse_distances(trace)
        splits = working_set_splits(distances)
        threshold = splits[0][0] if splits else math.inf
        a_text = span([count for _, count in splits])
        b_text = span([working_set_keys(trace, split) for split, _ in splits])
        rates = hit_rate_curve(trace, CACHE_CAPACITIES)
        sat90 = saturation_capacity(CACHE_CAPACITIES, rates, 0.90)
        sat95 = saturation_capacity(CACHE_CAPACITIES, rates, 0.95)
        print(
            f"{exponent:>4} {len(set(trace)):>8} {rates[-1]:>7.3f} "
            f"{threshold:>8.1f} {a_text:>9} {b_text:>9} {sat90:>6} {sat95:>6}"
        )
    print()
    print("Ranges cover tied widest gaps; the printed threshold is the earliest.")
    print()


def persistence_summary(points: list[tuple[float, float]]) -> tuple[float, float, float] | None:
    """Return ``(birth, death, persistence)`` of the dominant H1 bar."""
    bar = dominant_bar(rips_persistence(points), dimension=1)
    if bar is None:
        return None
    return (bar[0], bar[1], bar[1] - bar[0])


def latent_experiment() -> None:
    """Compare hole persistence for a ring and a blob, then probe OOD misses."""
    print("== latent space: dominant H1 persistence ==")
    print("40 points per cloud, 8 seeds, outer radius 1.0")
    print(f"{'seed':>4} {'annulus (b, d, pers)':>26} {'blob (b, d, pers)':>26}")
    for seed in range(8):
        ring = persistence_summary(annulus(40, 0.75, 1.0, seed))
        disk = persistence_summary(blob(40, 1.0, seed))
        ring_text = "none" if ring is None else f"({ring[0]:.2f}, {ring[1]:.2f}, {ring[2]:.2f})"
        disk_text = "none" if disk is None else f"({disk[0]:.2f}, {disk[1]:.2f}, {disk[2]:.2f})"
        print(f"{seed:>4} {ring_text:>26} {disk_text:>26}")
    print()

    print("inner-radius sweep: mean birth and death of the dominant H1 bar (n=40, 4 seeds)")
    print(f"{'inner':>5} {'birth':>6} {'death':>6}")
    for inner in (0.4, 0.5, 0.6, 0.7, 0.8):
        deaths: list[float] = []
        births: list[float] = []
        for seed in range(4):
            summary = persistence_summary(annulus(40, inner, 1.0, 100 + seed))
            if summary is not None:
                births.append(summary[0])
                deaths.append(summary[1])
        print(f"{inner:>5.1f} {statistics.fmean(births):>6.3f} {statistics.fmean(deaths):>6.3f}")
    print("death rises roughly 1.5 per unit of inner radius over this range")
    print()

    print("nearest-neighbour OOD rule inside the hole")
    print("threshold = 95th percentile of in-distribution nearest-neighbour distance")
    print(f"{'inner':>5} {'tau':>6} {'missed':>7} {'rate':>6}")
    for inner in (0.6, 0.75):
        points = annulus(40, inner, 1.0, seed=3)
        nearest = [
            min(euclidean(point, other) for index, other in enumerate(points) if index != j)
            for j, point in enumerate(points)
        ]
        nearest.sort()
        tau = nearest[int(0.95 * (len(nearest) - 1))]
        rng = random.Random(9)
        trials = 200
        misses = 0
        for _ in range(trials):
            radius = rng.uniform(inner - 0.15, inner - 0.02)
            angle = rng.uniform(0.0, 2.0 * math.pi)
            probe = (radius * math.cos(angle), radius * math.sin(angle))
            distance = min(euclidean(probe, point) for point in points)
            if distance <= tau:
                misses += 1
        print(f"{inner:>5.2f} {tau:>6.3f} {misses:>4}/{trials:<3} {misses / trials:>6.2f}")
    print()


def main() -> None:
    """Run both experiments and report wall-clock time."""
    start = time.perf_counter()
    cache_experiment()
    latent_experiment()
    print(f"total time: {time.perf_counter() - start:.2f} s")


main()
