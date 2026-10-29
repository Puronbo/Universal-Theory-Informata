"""Consciousness / attention (phenomenological, A3.2, A4.6, A5.3)."""

from __future__ import annotations

from model.stroboscopic import strobe


def attention_trace(stimuli: list[float], threshold: float = 0.5) -> list[int]:
    """Map a stimulus stream to ternary attention states.

    active (+1) if stimulus > threshold, balance (-1) if < -threshold, else void (0).
    """
    out: list[int] = []
    for s in stimuli:
        if s > threshold:
            out.append(1)
        elif s < -threshold:
            out.append(-1)
        else:
            out.append(0)
    return out


def conscious_moment(stream: list[float], sample_rate: int = 1) -> list[float]:
    """A conscious 'now' is a stroboscopic alias of the stimulus stream (A4.6)."""
    return strobe(list(stream), sample_rate)


def closure_check(exterior: list[float], interior: list[float], tol: float = 1e-9) -> bool:
    """Awakening criterion: exterior and interior states coincide (A5.3, E≡I)."""
    if len(exterior) != len(interior):
        return False
    return all(abs(e - i) < tol for e, i in zip(exterior, interior, strict=False))
