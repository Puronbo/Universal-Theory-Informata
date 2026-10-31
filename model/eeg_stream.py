"""Consumer EEG stream processing schematic (OpenBCI-style).

Functions for bandpass filtering, FFT, and coherence computation on raw
multi-channel EEG. Pure Python + numpy (optional).
"""

from __future__ import annotations

import math
from collections.abc import Sequence


def bandpass_filter(
    signal: Sequence[float],
    low: float = 8.0,
    high: float = 13.0,
    fs: float = 250.0,
) -> list[float]:
    """Difference-of-moving-averages bandpass (alpha band by default).

    A short window (``fs/high``) tracks the fast component; a longer window
    (``fs/low``) tracks the slow component. Subtracting the long mean leaves
    the band between ``low`` and ``high``. Returns a new list.
    """
    if fs <= 0 or low <= 0 or high <= low:
        raise ValueError("require fs > 0 and 0 < low < high")
    n = len(signal)
    if n == 0:
        return []
    mean = sum(signal) / n
    prefix = [0.0] * (n + 1)
    for i, value in enumerate(signal):
        prefix[i + 1] = prefix[i] + (value - mean)

    short_w = max(1, int(fs / high))
    long_w = max(short_w + 1, int(fs / low))

    def moving_mean(i: int, width: int) -> float:
        lo = max(0, i - width // 2)
        hi = min(n, i + width // 2 + 1)
        return (prefix[hi] - prefix[lo]) / (hi - lo)

    return [moving_mean(i, short_w) - moving_mean(i, long_w) for i in range(n)]


def fft_magnitude(signal: Sequence[float]) -> list[float]:
    """Return magnitude spectrum (pure Python DFT, small N)."""
    n = len(signal)
    if n == 0:
        return []
    out = []
    for k in range(n // 2):
        re = sum(signal[t] * math.cos(2 * math.pi * k * t / n) for t in range(n))
        im = sum(signal[t] * math.sin(2 * math.pi * k * t / n) for t in range(n))
        out.append(math.hypot(re, im) / n)
    return out


def channel_coherence(ch1: Sequence[float], ch2: Sequence[float]) -> float:
    """Pearson-like coherence between two channels (simplified)."""
    n = min(len(ch1), len(ch2))
    if n == 0:
        return 0.0
    a, b = ch1[:n], ch2[:n]
    ma, mb = sum(a) / n, sum(b) / n
    cov = sum((a[i] - ma) * (b[i] - mb) for i in range(n)) / n
    va = math.sqrt(sum((x - ma) ** 2 for x in a) / n)
    vb = math.sqrt(sum((x - mb) ** 2 for x in b) / n)
    if va == 0 or vb == 0:
        return 0.0
    return cov / (va * vb)


def process_eeg_stream(channels: Sequence[Sequence[float]], fs: float = 250.0) -> dict[str, object]:
    """Process a multi-channel EEG stream into coherence + alpha power.

    channels: list of lists (each channel = list of samples).
    Returns dict with per-channel alpha power and pairwise coherence.
    """
    filtered = [bandpass_filter(ch, low=8, high=13, fs=fs) for ch in channels]
    powers = [sum(x * x for x in f) / len(f) if f else 0.0 for f in filtered]
    cohs: dict[str, float] = {}
    for i in range(len(channels)):
        for j in range(i + 1, len(channels)):
            cohs[f"{i}-{j}"] = channel_coherence(filtered[i], filtered[j])
    return {"alpha_power": powers, "coherence": cohs}
