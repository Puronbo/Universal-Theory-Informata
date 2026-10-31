import pytest

from model import c0_center, novelty_score, poincare_distance


def test_poincare_distance_origin():
    assert poincare_distance((0.0, 0.0), (0.0, 0.0)) == 0.0


def test_poincare_distance_symmetry():
    u, v = (0.3, 0.4), (0.1, 0.2)
    assert abs(poincare_distance(u, v) - poincare_distance(v, u)) < 1e-9


def test_novelty_score():
    assert novelty_score((0.3, 0.4)) == pytest.approx(0.5, abs=1e-9)
    assert novelty_score((0.0, 0.0)) == 0.0


def test_c0_center():
    assert c0_center() == (0.0, 0.0)


def test_poincare_distance_invalid():
    with pytest.raises(ValueError):
        poincare_distance((1.0, 0.0), (0.0, 0.0))
