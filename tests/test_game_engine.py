"""Tests for game_engine."""
from game_engine import World


def test_game_engine_run():
    w = World(n_agents=3)
    w.run([0.9, -0.8, 0.1], stretch=1.0, erosion_pairs=1)
    assert w.t == 3
    assert len(w.history) == 3
    assert all(len(h) == 3 for h in w.history)


def test_game_engine_scale():
    w = World(n_agents=2)
    w.run([0.9], stretch=2.0, erosion_pairs=0)
    assert w.scale == 2.0
    w.run([0.9], stretch=2.0, erosion_pairs=0)
    assert w.scale == 4.0
