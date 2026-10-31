"""Neural phase-locking simulation (Kuramoto) with external noise.

Phenomenological model of non-invasive BCI: a population of noisy neural
oscillators synchronizes under a coupling ramp, filtering macro-static.
"""

from __future__ import annotations

import math
import random
from collections.abc import Sequence
from typing import Any

try:
    import numpy as np

    _HAS_NUMPY = True
except ImportError:
    _HAS_NUMPY = False


def simulate_neural_phase_locking(
    num_neurons: int = 500,
    time_steps: int = 200,
    center_freq: float = 5.0,
    freq_spread: float = 1.0,
    coupling: float = 2.5,
    dt: float = 0.05,
    noise_amp: float = 0.0,
    seed: int | None = None,
) -> tuple[list[float], Any]:
    """Kuramoto phase-oscillator network.

    Returns (coherence_history, theta_final).
    noise_amp adds external electromagnetic macro-static to each oscillator.
    """
    if seed is not None:
        random.seed(seed)
        if _HAS_NUMPY:
            np.random.seed(seed)
    omega: Any
    theta: Any
    if _HAS_NUMPY:
        omega = np.random.normal(loc=center_freq, scale=freq_spread, size=num_neurons)
        theta = np.random.uniform(0, 2 * math.pi, size=num_neurons)
    else:
        omega = [random.gauss(center_freq, freq_spread) for _ in range(num_neurons)]
        theta = [random.uniform(0, 2 * math.pi) for _ in range(num_neurons)]
    history: list[float] = []
    for _ in range(time_steps):
        if _HAS_NUMPY:
            vec = np.mean(np.exp(1j * theta))
            r = float(abs(vec))
            psi = float(np.angle(vec))
            dtheta = omega + coupling * r * np.sin(psi - theta)
            if noise_amp > 0:
                dtheta = dtheta + np.random.normal(0, noise_amp, size=num_neurons)
            theta = (theta + dtheta * dt) % (2 * math.pi)
        else:
            # pure-python fallback
            cx = sum(math.cos(t) for t in theta) / num_neurons
            cy = sum(math.sin(t) for t in theta) / num_neurons
            r = math.hypot(cx, cy)
            psi = math.atan2(cy, cx)
            dtheta = [
                omega[i] + coupling * r * math.sin(psi - theta[i]) for i in range(num_neurons)
            ]
            if noise_amp > 0:
                dtheta = [d + random.gauss(0, noise_amp) for d in dtheta]
            theta = [(theta[i] + dtheta[i] * dt) % (2 * math.pi) for i in range(num_neurons)]
        history.append(r)
    return history, theta


def coherence(history: Sequence[float]) -> float:
    return history[-1] if history else 0.0


def noise_filtering(
    num_neurons: int = 200,
    time_steps: int = 100,
    noise_levels: Sequence[float] = (0.0, 0.5, 1.0, 2.0),
) -> dict[float, float]:
    """Sweep noise amplitudes; return final coherence per level."""
    out: dict[float, float] = {}
    for nl in noise_levels:
        h, _ = simulate_neural_phase_locking(
            num_neurons=num_neurons, time_steps=time_steps, noise_amp=nl, seed=42
        )
        out[nl] = h[-1]
    return out
