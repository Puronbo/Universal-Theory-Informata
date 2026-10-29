"""Tests for model.playhead."""
from model import Playhead


def test_playhead_index_and_step():
    ph = Playhead(["a", "b", "c"], tau=1.0)
    assert ph.read(0.0) == "a"
    assert ph.read(0.5) == "a"
    assert ph.read(1.0) == "b"
    assert ph.read(10.0) == "c"  # clamped
    assert ph.step() == "a"
    assert ph.step() == "b"
    assert ph.step() == "c"
    assert ph.step() is None


def test_playhead_read_all():
    ph = Playhead([1, 2, 3])
    assert ph.read_all() == [1, 2, 3]
    assert ph.index == 3


def test_playhead_real_block():
    data = list(range(10))
    ph = Playhead(data, tau=2.0)
    assert ph.read(0.0) == 0
    assert ph.read(3.9) == 1  # floor(3.9/2)=1
    assert ph.read(100.0) == 9  # clamped


def test_playhead_reset():
    ph = Playhead([1, 2, 3])
    ph.step()
    ph.step()
    assert ph.index == 2
    ph.reset()
    assert ph.index == 0
    assert ph.step() == 1


def test_playhead_negative_time():
    ph = Playhead([1, 2, 3])
    assert ph.read(-1.0) is None
    assert ph.read(-0.5) is None
