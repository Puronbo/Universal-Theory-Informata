"""Consumer EEG stream processing schematic (OpenBCI-style).

Functions for bandpass filtering, FFT, and coherence computation on raw
multi-channel EEG. Pure Python + numpy (optional).
"""
from __future__ import annotations
import math

try:
    import numpy as np
    _HAS_NUMPY = True
except ImportError:
    _HAS_NUMPY = False


def bandpass_filter(signal, low=8.0, high=13.0, fs=250.0):
    """Simple moving-average bandpass (alpha band). Returns filtered list."""
    # Approximate: subtract running mean, then smooth
    n = len(signal)
    if n == 0:
        return []
    mean = sum(signal) / n
    centered = [s - mean for s in signal]
    # moving average window ~ fs/high
    w = max(1, int(fs / high))
    out = []
    for i in range(n):
        lo = max(0, i - w // 2)
        hi = min(n, i + w // 2 + 1)
        out.append(sum(centered[lo:hi]) / (hi - lo))
    return out


def fft_magnitude(signal):
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


def channel_coherence(ch1, ch2):
    """Pearson-like coherence between two channels (simplified)."""
    n = min(len(ch1), len(ch2))
    if n == 0:
        return 0.0
    a, b = ch1[:n], ch2[:n]
    ma, mb = sum(a) / n, sum(b) / n
    cov = sum((a[i] - ma) * (b[i] - mb) for i in range(n)) / n
    va = (sum((x - ma) ** 2 for x in a) / n) ** 0.5
    vb = (sum((x - mb) ** 2 for x in b) / n) ** 0.5
    if va == 0 or vb == 0:
        return 0.0
    return cov / (va * vb)


def process_eeg_stream(channels, fs=250.0):
    """Process a multi-channel EEG stream into coherence + alpha power.

    channels: list of lists (each channel = list of samples).
    Returns dict with per-channel alpha power and pairwise coherence.
    """
    filtered = [bandpass_filter(ch, low=8, high=13, fs=fs) for ch in channels]
    powers = [sum(x * x for x in f) / len(f) if f else 0.0 for f in filtered]
    cohs = {}
    for i in range(len(channels)):
        for j in range(i + 1, len(channels)):
            cohs[f"{i}-{j}"] = channel_coherence(filtered[i], filtered[j])
    return {"alpha_power": powers, "coherence": cohs}
