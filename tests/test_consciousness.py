"""Tests for model.consciousness."""

import random

from model import attention_trace, closure_check, conscious_moment


def test_attention_trace():
    assert attention_trace([0.1, 0.8, -0.9, 0.0]) == [0, 1, -1, 0]


def test_conscious_moment():
    assert conscious_moment([1, 2, 3, 4, 5], 2) == [1, 3, 5]


def test_closure_check():
    assert closure_check([1.0, 2.0], [1.0, 2.0])
    assert not closure_check([1.0], [1.0, 2.0])
    assert closure_check([], [])


def test_prop_attention_trace_range():
    random.seed(3)
    for _ in range(50):
        stim = [random.uniform(-2, 2) for _ in range(20)]
        tr = attention_trace(stim)
        assert all(v in (-1, 0, 1) for v in tr)
