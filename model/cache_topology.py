"""Topological reading of cache reuse distance.

The reuse-distance profile of a trace is a finite point set on the line. Its
0-dimensional persistence is the sorted list of consecutive gaps: components
merge at the gap size, and the largest gap is the most persistent feature. The
split it induces is the natural candidate for a working-set threshold.

The module measures that claim instead of asserting it. ``working_set_estimate``
returns the persistence-selected split, ``simulate_lru`` returns the empirical
hit rate, and ``saturation_capacity`` locates the 90% point of the hit-rate
curve so a demo can compare the two. The measurement does not support the
split as a capacity predictor: the widest gap is a scale, not a size. See
``TOPOLOGY_EXPERIMENTS.md``.
"""

from __future__ import annotations

import math
import statistics
from collections import OrderedDict, defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

__all__ = [
    "CacheStats",
    "hit_rate_curve",
    "merge_gaps",
    "reuse_distances",
    "saturation_capacity",
    "simulate_lru",
    "working_set_candidates",
    "working_set_estimate",
    "working_set_keys",
    "working_set_splits",
]


@dataclass(frozen=True)
class CacheStats:
    """Hit and miss counts for one simulated cache."""

    capacity: int
    hits: int
    misses: int

    @property
    def hit_rate(self) -> float:
        """Fraction of accesses that hit."""
        total = self.hits + self.misses
        return self.hits / total if total else 0.0


def reuse_distances(trace: Iterable[int]) -> list[float]:
    """Return the LRU stack distance of every access.

    The stack distance of an access is the number of distinct keys accessed
    since the previous access to the same key; it equals the depth of the key
    in an LRU stack. A first touch has infinite distance and is reported as
    ``math.inf``. A repeated consecutive access has distance ``0``.

    Args:
        trace: Sequence of integer keys.

    Returns:
        One distance per access.

    Raises:
        ValueError: If a key is not an integer.
    """
    stack: OrderedDict[int, None] = OrderedDict()
    out: list[float] = []
    for key in trace:
        if not isinstance(key, int) or isinstance(key, bool):
            raise ValueError(f"trace keys must be int, got {type(key).__name__}")
        if key in stack:
            keys = list(stack)
            position = keys.index(key)
            out.append(float(len(keys) - 1 - position))
            stack.move_to_end(key)
        else:
            out.append(math.inf)
            stack[key] = None
    return out


def merge_gaps(values: Sequence[float]) -> list[tuple[float, float]]:
    """Return the 0-dimensional persistence bars of points on the line.

    Every component is born at scale ``0``; at scale ``gap`` two neighbouring
    components merge, so each finite bar is ``(0.0, gap)``. Duplicate values
    are one point and contribute nothing. Non-finite values are ignored.

    Args:
        values: Reuse distances or any finite point set on the line.

    Returns:
        Bars ``(birth, death)`` sorted by death, so the most persistent bar is
        last.

    Raises:
        ValueError: If a value is negative.
    """
    finite: set[float] = set()
    for value in values:
        if not math.isfinite(value):
            continue
        if value < 0:
            raise ValueError(f"distances must be non-negative, got {value}")
        finite.add(float(value))
    ordered = sorted(finite)
    bars = [(0.0, b - a) for a, b in zip(ordered, ordered[1:], strict=False)]
    bars.sort(key=lambda bar: bar[1])
    return bars


def working_set_splits(values: Sequence[float]) -> list[tuple[float, int]]:
    """Return ``(threshold, count)`` for every maximally wide gap.

    Reuse distances are integer-valued, so equal-width gaps are common and the
    widest gap is not unique in general. This function exposes every tied split
    instead of silently resolving the tie.

    Args:
        values: Reuse distances.

    Returns:
        One split per widest gap, in ascending order. Empty when there are
        fewer than two distinct finite values.
    """
    finite = sorted({float(v) for v in values if math.isfinite(v)})
    if len(finite) < 2:
        return []
    gaps = [high - low for low, high in zip(finite, finite[1:], strict=False)]
    widest = max(gaps)
    return [
        (0.5 * (finite[index] + finite[index + 1]), index + 1)
        for index, gap in enumerate(gaps)
        if gap == widest
    ]


def working_set_candidates(values: Sequence[float]) -> list[int]:
    """Return the working-set count for every maximally wide gap.

    Args:
        values: Reuse distances.

    Returns:
        One count per widest gap, in ascending order. Empty when there are
        fewer than two distinct finite values.
    """
    return [count for _, count in working_set_splits(values)]


def working_set_estimate(values: Sequence[float]) -> tuple[float, int]:
    """Return ``(threshold, count)`` from the most persistent 0-D gap.

    The largest gap between consecutive distinct distances is the most
    persistent feature of the profile. Everything below it is one cluster; the
    number of distinct distances in that cluster is the working-set estimate.
    When several gaps tie for widest, the earliest gap is used, which gives the
    smallest candidate; :func:`working_set_splits` returns the whole set.

    Args:
        values: Reuse distances.

    Returns:
        The midpoint of the widest gap and the count of distinct distances at
        or below its lower edge. With fewer than two distinct finite values the
        threshold is infinite and the count is the number of distinct values.
    """
    splits = working_set_splits(values)
    if splits:
        return splits[0]
    return (math.inf, len({float(v) for v in values if math.isfinite(v)}))


def working_set_keys(trace: Sequence[int], threshold: float) -> int:
    """Count distinct keys whose median reuse gap is at most ``threshold``.

    This is the second estimate of the working set: instead of counting the
    distances themselves, it counts the objects that are reused within the
    short-reuse regime. Keys seen only once are not counted, because they have
    no reuse gap.

    Args:
        trace: Sequence of integer keys.
        threshold: Non-negative gap threshold.

    Returns:
        The number of distinct reused keys below the threshold.

    Raises:
        ValueError: If ``threshold`` is negative.
    """
    if threshold < 0:
        raise ValueError(f"threshold must be non-negative, got {threshold}")
    last_seen: dict[int, int] = {}
    gaps: dict[int, list[int]] = defaultdict(list)
    for position, key in enumerate(trace):
        previous = last_seen.get(key)
        if previous is not None:
            gaps[key].append(position - previous)
        last_seen[key] = position
    return sum(1 for values in gaps.values() if statistics.median(values) <= threshold)


def simulate_lru(trace: Sequence[int], capacity: int) -> CacheStats:
    """Simulate an LRU cache over ``trace``.

    Args:
        trace: Sequence of integer keys.
        capacity: Number of slots; must be at least one.

    Returns:
        The hit and miss counts.

    Raises:
        ValueError: If ``capacity`` is less than one or ``trace`` is empty.
    """
    if capacity < 1:
        raise ValueError(f"capacity must be at least 1, got {capacity}")
    if not trace:
        raise ValueError("trace must not be empty")
    cache: OrderedDict[int, None] = OrderedDict()
    hits = 0
    misses = 0
    for key in trace:
        if key in cache:
            hits += 1
            cache.move_to_end(key)
        else:
            misses += 1
            cache[key] = None
            if len(cache) > capacity:
                cache.popitem(last=False)
    return CacheStats(capacity=capacity, hits=hits, misses=misses)


def hit_rate_curve(trace: Sequence[int], capacities: Sequence[int]) -> list[float]:
    """Return the hit rate at each capacity.

    Args:
        trace: Sequence of integer keys.
        capacities: Non-empty sequence of positive capacities.

    Returns:
        One hit rate per capacity.

    Raises:
        ValueError: If ``capacities`` is empty.
    """
    if not capacities:
        raise ValueError("capacities must not be empty")
    return [simulate_lru(trace, capacity).hit_rate for capacity in capacities]


def saturation_capacity(
    capacities: Sequence[int], rates: Sequence[float], fraction: float = 0.9
) -> int:
    """Return the smallest capacity reaching ``fraction`` of the peak hit rate.

    This is the empirical working-set proxy used to test the topological
    estimate: the smallest cache that captures ``fraction`` of the peak hit
    rate in the sweep.

    Args:
        capacities: Increasing capacities.
        rates: Hit rates aligned with ``capacities``.
        fraction: Target fraction of the peak, in ``(0, 1]``.

    Returns:
        The capacity at which the target is first met.

    Raises:
        ValueError: If the inputs are empty, of different length, not
            increasing, contain a non-positive capacity or a rate outside
            ``[0, 1]``, or ``fraction`` is outside ``(0, 1]``.
    """
    if not capacities or len(capacities) != len(rates):
        raise ValueError("capacities and rates must be non-empty and aligned")
    if not 0 < fraction <= 1:
        raise ValueError(f"fraction must be in (0, 1], got {fraction}")
    if any(capacity < 1 for capacity in capacities):
        raise ValueError("capacities must be positive")
    if any(not math.isfinite(rate) or not 0.0 <= rate <= 1.0 for rate in rates):
        raise ValueError("rates must be finite hit rates in [0, 1]")
    if any(b <= a for a, b in zip(capacities, capacities[1:], strict=False)):
        raise ValueError("capacities must be strictly increasing")
    peak = max(rates)
    if peak <= 0:
        return capacities[0]
    target = fraction * peak
    # The peak rate is one of ``rates`` and ``target <= peak``, so the search
    # always finds a capacity.
    index = next(position for position, rate in enumerate(rates) if rate >= target)
    return capacities[index]
