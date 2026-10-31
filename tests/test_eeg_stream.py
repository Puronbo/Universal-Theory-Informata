import math

import pytest

from model import bandpass_filter, channel_coherence, fft_magnitude, process_eeg_stream


def test_bandpass_filter():
    sig = [1.0] * 100
    out = bandpass_filter(sig, low=8, high=13, fs=250)
    assert len(out) == 100


def test_fft_magnitude():
    sig = [1.0, 0.0, -1.0, 0.0] * 8
    mag = fft_magnitude(sig)
    assert len(mag) == len(sig) // 2
    assert any(m > 0 for m in mag)


def test_channel_coherence():
    a = [1.0, 2.0, 3.0, 4.0]
    assert channel_coherence(a, a) == pytest.approx(1.0, abs=1e-9)
    assert channel_coherence(a, [4.0, 3.0, 2.0, 1.0]) == pytest.approx(-1.0, abs=1e-9)


def test_process_eeg_stream():
    ch1 = [1.0, 2.0, 3.0, 4.0, 5.0]
    ch2 = [5.0, 4.0, 3.0, 2.0, 1.0]
    res = process_eeg_stream([ch1, ch2], fs=250.0)
    assert "alpha_power" in res
    assert "coherence" in res
    assert len(res["alpha_power"]) == 2
    assert "0-1" in res["coherence"]


def test_empty_inputs():
    assert bandpass_filter([]) == []
    assert fft_magnitude([]) == []
    assert channel_coherence([], []) == 0.0
    assert process_eeg_stream([]) == {"alpha_power": [], "coherence": {}}


def test_constant_channel_has_no_coherence():
    assert channel_coherence([1.0, 1.0, 1.0], [2.0, 2.0, 2.0]) == 0.0


def test_bandpass_passes_alpha_and_removes_dc():
    fs = 250.0
    alpha = [math.sin(2 * math.pi * 10 * t / fs) for t in range(500)]
    out = bandpass_filter(alpha, low=8, high=13, fs=fs)
    alpha_rms = math.sqrt(sum(x * x for x in out) / len(out))
    assert alpha_rms > 0.25

    gamma = [math.sin(2 * math.pi * 50 * t / fs) for t in range(500)]
    gamma_rms = math.sqrt(
        sum(x * x for x in bandpass_filter(gamma, low=8, high=13, fs=fs)) / len(gamma)
    )
    assert gamma_rms < alpha_rms / 3

    dc = [1.0] * 500
    filtered_dc = bandpass_filter(dc, low=8, high=13, fs=fs)
    assert max(abs(x) for x in filtered_dc) < 1e-12


def test_bandpass_rejects_bad_parameters():
    with pytest.raises(ValueError):
        bandpass_filter([1.0], low=0)
    with pytest.raises(ValueError):
        bandpass_filter([1.0], low=13, high=8)
    with pytest.raises(ValueError):
        bandpass_filter([1.0], fs=0)
