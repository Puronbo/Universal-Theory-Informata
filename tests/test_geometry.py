"""Tests for model.geometry."""
from model import apparent_separation, stretched_distance


def test_stretched_distance():
    assert stretched_distance(2.0, 3.0) == 6.0
    assert stretched_distance(1.0, 1.0) == 1.0
    assert stretched_distance(0.0, 5.0) == 0.0


def test_apparent_separation():
    pts = [0.0, 1.0, 3.0]
    out = apparent_separation(pts, 2.0)
    assert len(out) == 3
    assert out[0] == (0, 1, 2.0)
    assert out[1] == (0, 2, 6.0)
    assert out[2] == (1, 2, 4.0)


def test_apparent_separation_empty():
    assert apparent_separation([], 2.0) == []
    assert apparent_separation([1.0], 2.0) == []


def test_prop_stretched_monotonic():
    for sf in [0.5, 1.0, 2.0, 10.0]:
        assert stretched_distance(3.0, sf) == 3.0 * sf
