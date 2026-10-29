import pytest
from model import bandpass_filter, fft_magnitude, channel_coherence, process_eeg_stream


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
