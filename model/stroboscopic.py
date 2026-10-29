"""Stroboscopic sampling (A4.6)."""

from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def strobe(signal: list[T], rate: int) -> list[T]:
    """Downsample a fine signal by `rate`, producing the frozen alias (blade)."""
    if rate < 1:
        raise ValueError("rate must be >= 1")
    return signal[::rate]
