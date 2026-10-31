import model.neural_phase as neural_phase
from model import coherence, noise_filtering, simulate_neural_phase_locking


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


def test_noise_filtering_custom_levels():
    res = noise_filtering(num_neurons=20, time_steps=10, noise_levels=(0.0, 0.3))
    assert set(res) == {0.0, 0.3}


def test_coherence_empty_and_nonempty():
    assert coherence([]) == 0.0
    assert coherence([0.2, 0.6]) == 0.6


def test_pure_python_fallback(monkeypatch):
    monkeypatch.setattr(neural_phase, "_HAS_NUMPY", False)
    history, theta = neural_phase.simulate_neural_phase_locking(
        num_neurons=16, time_steps=8, noise_amp=0.2, seed=7
    )
    assert len(history) == 8
    assert len(theta) == 16
    assert 0.0 <= history[-1] <= 1.0
