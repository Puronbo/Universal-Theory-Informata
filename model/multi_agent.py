"""Multi-agent consciousness simulation (phenomenological)."""

from __future__ import annotations

from model.recursion import erosion_step


def multi_agent_step(
    agents: list[list[int]],
    stimuli: list[float],
    threshold: float = 0.5,
    erosion_pairs: int = 1,
) -> list[list[int]]:
    """Advance each agent's attention trace and erode noise.

    agents: list of lists (ternary states per agent).
    Returns updated agents.
    """
    out: list[list[int]] = []
    for a in agents:
        # shift: drop oldest, append new attention state from stimulus
        trace = list(a)
        if trace:
            trace = trace[1:]
        # use the last stimulus value for the new slot
        new_val = stimuli[-1] if stimuli else 0.0
        new_state = 1 if new_val > threshold else (-1 if new_val < -threshold else 0)
        trace.append(new_state)
        trace = erosion_step(trace, pairs=erosion_pairs)
        out.append(trace)
    return out


def network_closure(agents: list[list[int]]) -> float:
    """Fraction of agents whose state is net-zero (balanced awareness)."""
    if not agents:
        return 0.0
    balanced = sum(1 for a in agents if sum(a) == 0)
    return balanced / len(agents)
