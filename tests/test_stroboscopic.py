"""Tests for model.stroboscopic."""

import random

from model import strobe


def test_strobe():
    sig = list(range(10))
    assert strobe(sig, 2) == [0, 2, 4, 6, 8]
    assert strobe(sig, 3) == [0, 3, 6, 9]
    assert strobe(sig, 1) == sig
    try:
        strobe(sig, 0)
        raise AssertionError()
    except ValueError:
        pass


def test_strobe_empty():
    assert strobe([], 2) == []


def test_prop_strobe_length():
    random.seed(1)
    for _ in range(50):
        n = random.randint(1, 50)
        rate = random.randint(1, 7)
        sig = list(range(n))
        out = strobe(sig, rate)
        assert len(out) == (n + rate - 1) // rate
