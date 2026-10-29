"""Clock, broken mirror, entropy brake (A10)."""

from __future__ import annotations

# Physical constants
PLANCK_TIME: float = 5.391247e-44  # seconds


def planck_refresh_rate() -> float:
    """Maximum refresh rate of the universal monitor (1 / t_P)."""
    return 1.0 / PLANCK_TIME


def cp_violation_tilt() -> float:
    """Built-in matter/antimatter asymmetry (~1 part in 1e9)."""
    return 1e-9


def entropy_brake(disorder_before: float, disorder_after: float) -> float:
    """Reduction in disorder achieved by the midpoint (consciousness)."""
    return disorder_before - disorder_after
