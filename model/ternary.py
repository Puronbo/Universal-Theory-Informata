"""Ternary logic (A0.2, A0.3).

Three-state grammar: {-1, 0, +1} with net-zero invariant.
"""

from __future__ import annotations

from collections.abc import Iterable

# Ternary state constants
VOID: int = 0
ACTIVE: int = 1
BALANCE: int = -1

VALID_STATES: tuple[int, int, int] = (VOID, ACTIVE, BALANCE)

# Threshold for ternarize (heuristic, not derived; see AXIOMS A0.2)
TERNARY_THRESHOLD: float = 1.0 / 3.0


def is_valid_state(v: int) -> bool:
    """Check if value is a valid ternary state."""
    return v in VALID_STATES


def net_zero(states: Iterable[int]) -> bool:
    """Net-zero invariant (A0.3): sum of states in a closed subsystem == 0."""
    return sum(states) == 0


def ternary_compose(states: Iterable[int]) -> float:
    """Compose ternary states into a single normalized value in [-1, 1].

    Returns 0.0 for empty input.
    """
    s: list[int] = list(states)
    if not s:
        return 0.0
    return max(-1.0, min(1.0, sum(s) / len(s)))


def ternarize(x: float) -> int:
    """Map a real drive to the nearest ternary state.

    Thresholds ±1/3 are a heuristic mapping (not derived); see AXIOMS A0.2.
    """
    if x > TERNARY_THRESHOLD:
        return ACTIVE
    if x < -TERNARY_THRESHOLD:
        return BALANCE
    return VOID
