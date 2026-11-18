"""Tests for the cache-topology audit helpers."""

from __future__ import annotations

import math

import pytest

from model.cache_topology import (
    CacheStats,
    hit_rate_curve,
    merge_gaps,
    reuse_distances,
    saturation_capacity,
    simulate_lru,
    working_set_candidates,
    working_set_estimate,
    working_set_keys,
    working_set_splits,
)


def test_reuse_distances_first_touch_is_infinite() -> None:
    assert reuse_distances([7]) == [math.inf]


def test_reuse_distances_consecutive_is_zero() -> None:
    assert reuse_distances([1, 1, 1]) == [math.inf, 0.0, 0.0]


def test_reuse_distances_counts_distinct_keys_since_last_use() -> None:
    # 1, 2, 3 came after the last 1, so the stack distance is 2.
    assert reuse_distances([1, 2, 3, 1]) == [math.inf, math.inf, math.inf, 2.0]


def test_reuse_distances_repeated_key_does_not_add_depth() -> None:
    # 2 appears twice, but only the distinct keys matter.
    assert reuse_distances([1, 2, 2, 1]) == [math.inf, math.inf, 0.0, 1.0]


def test_reuse_distances_rejects_non_integer_keys() -> None:
    with pytest.raises(ValueError, match="trace keys must be int"):
        reuse_distances([1, "x"])  # type: ignore[list-item]


def test_reuse_distances_rejects_bool() -> None:
    with pytest.raises(ValueError, match="trace keys must be int"):
        reuse_distances([True])


def test_merge_gaps_returns_consecutive_gaps() -> None:
    assert merge_gaps([0.0, 1.0, 4.0]) == [(0.0, 1.0), (0.0, 3.0)]


def test_merge_gaps_deduplicates_and_sorts() -> None:
    assert merge_gaps([2.0, 1.0, 2.0, 4.0]) == [(0.0, 1.0), (0.0, 2.0)]


def test_merge_gaps_ignores_non_finite() -> None:
    assert merge_gaps([math.inf, 1.0, math.nan, 3.0]) == [(0.0, 2.0)]


def test_merge_gaps_rejects_negative() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        merge_gaps([-1.0])


def test_merge_gaps_single_value_has_no_bar() -> None:
    assert merge_gaps([2.0]) == []


def test_working_set_estimate_finds_the_widest_gap() -> None:
    threshold, count = working_set_estimate([0.0, 1.0, 2.0, 20.0, 21.0])
    assert threshold == pytest.approx(11.0)
    assert count == 3


def test_working_set_estimate_degenerate_input() -> None:
    threshold, count = working_set_estimate([math.inf, 4.0])
    assert math.isinf(threshold)
    assert count == 1


def test_working_set_splits_returns_every_tied_threshold() -> None:
    # The widest gap (4) occurs at 1->5 and at 6->10.
    assert working_set_splits([0.0, 1.0, 5.0, 6.0, 10.0, 11.0]) == [(3.0, 2), (8.0, 4)]
    assert working_set_splits([4.0]) == []


def test_working_set_candidates_lists_every_widest_gap() -> None:
    # Gaps are 1, 4, 1, 4, 1, so the widest gap occurs twice.
    assert working_set_candidates([0.0, 1.0, 5.0, 6.0, 10.0, 11.0]) == [2, 4]


def test_working_set_candidates_is_empty_without_a_gap() -> None:
    assert working_set_candidates([]) == []
    assert working_set_candidates([4.0, 4.0]) == []


def test_working_set_estimate_breaks_ties_at_the_earliest_gap() -> None:
    assert working_set_estimate([0.0, 1.0, 5.0, 6.0, 10.0, 11.0]) == (3.0, 2)


def test_working_set_keys_counts_keys_inside_the_threshold() -> None:
    trace = [1, 2, 1, 3, 2, 2, 4]
    # key 1 gaps [2] median 2; key 2 gaps [3, 1] median 2; key 3 no repeat.
    assert working_set_keys(trace, 2.0) == 2
    assert working_set_keys(trace, 1.9) == 0


def test_working_set_keys_rejects_negative_threshold() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        working_set_keys([1, 1], -1.0)


def test_cache_stats_hit_rate() -> None:
    assert CacheStats(capacity=2, hits=3, misses=1).hit_rate == pytest.approx(0.75)
    assert CacheStats(capacity=1, hits=0, misses=0).hit_rate == 0.0


def test_simulate_lru_capacity_two_keeps_the_reused_key() -> None:
    stats = simulate_lru([1, 2, 1], capacity=2)
    assert stats.hits == 1
    assert stats.misses == 2
    assert stats.capacity == 2


def test_simulate_lru_capacity_one_misses_every_alternation() -> None:
    stats = simulate_lru([1, 2, 1, 2], capacity=1)
    assert stats.hits == 0
    assert stats.misses == 4


def test_simulate_lru_rejects_bad_capacity() -> None:
    with pytest.raises(ValueError, match="capacity must be at least 1"):
        simulate_lru([1], 0)


def test_simulate_lru_rejects_empty_trace() -> None:
    with pytest.raises(ValueError, match="trace must not be empty"):
        simulate_lru([], 4)


def test_hit_rate_is_monotone_in_capacity() -> None:
    # Each extra slot converts at least one miss into a hit.
    trace = [1, 1, 2, 1, 2, 3, 1, 2, 3]
    rates = hit_rate_curve(trace, [1, 2, 3])
    assert rates[0] < rates[1] < rates[2]


def test_hit_rate_curve_rejects_empty_capacities() -> None:
    with pytest.raises(ValueError, match="capacities must not be empty"):
        hit_rate_curve([1], [])


def test_saturation_capacity_finds_the_target() -> None:
    capacities = [1, 2, 4, 8]
    rates = [0.1, 0.4, 0.8, 1.0]
    assert saturation_capacity(capacities, rates, 0.9) == 8
    # 0.5 * peak = 0.5, and the first rate at or above it is 0.8 at capacity 4.
    assert saturation_capacity(capacities, rates, 0.5) == 4


def test_saturation_capacity_returns_first_when_nothing_helps() -> None:
    assert saturation_capacity([1, 2], [0.0, 0.0]) == 1


def test_saturation_capacity_rejects_misaligned_inputs() -> None:
    with pytest.raises(ValueError, match="non-empty and aligned"):
        saturation_capacity([1, 2], [0.5])


def test_saturation_capacity_rejects_bad_fraction() -> None:
    with pytest.raises(ValueError, match=r"fraction must be in \(0, 1\]"):
        saturation_capacity([1, 2], [0.5, 0.6], 1.5)


def test_saturation_capacity_rejects_non_increasing_capacities() -> None:
    with pytest.raises(ValueError, match="strictly increasing"):
        saturation_capacity([2, 2], [0.5, 0.6])


def test_saturation_capacity_rejects_non_positive_capacities() -> None:
    with pytest.raises(ValueError, match="capacities must be positive"):
        saturation_capacity([0, 1], [0.5, 0.6])


def test_saturation_capacity_rejects_non_finite_or_out_of_range_rates() -> None:
    with pytest.raises(ValueError, match="finite hit rates"):
        saturation_capacity([1, 2], [math.nan, 0.6])
    with pytest.raises(ValueError, match="finite hit rates"):
        saturation_capacity([1, 2], [0.5, 1.5])
