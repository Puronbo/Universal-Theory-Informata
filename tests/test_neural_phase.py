import pytest
from model import simulate_neural_phase_locking, coherence, noise_filtering


def test_simulate_phase_locking():
    hist, theta = simulate_neural_phase_locking(num_neurons=50, time_steps=20, seed=1)
    assert len(hist) == 20
    assert len(theta) == 50
    assert 0.0 <= hist[-1] <= 1.0


def test_coherence_increases():
    hist, _ = simulate_neural_phase_locking(num_neurons=100, time_steps=50, coupling=3.0, seed=2)
    assert hist[-1] > hist[0]


def test_noise_filtering():
    res = noise_filtering(num_neurons=80, time_steps=40)
    assert 0.0 in res
    assert all(0.0 <= v <= 1.0 for v in res.values())
