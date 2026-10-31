"""Tests for model.multi_agent."""

from model import multi_agent_step, network_closure


def test_multi_agent_step():
    agents = [[0, 0], [1, -1]]
    out = multi_agent_step(agents, [0.9], threshold=0.5, erosion_pairs=0)
    assert len(out) == 2
    assert out[0][-1] == 1
    assert out[1][-1] == 1


def test_network_closure():
    agents = [[1, -1], [1, 1]]
    frac = network_closure(agents)
    assert frac == 0.5

    agents2 = [[1, -1], [1, -1, 1, -1]]
    frac2 = network_closure(agents2)
    assert frac2 == 1.0


def test_multi_agent_step_erosion_preserves_sum():
    # Erosion preserves the sum of the trace it receives
    # But the shift + new state changes the sum first
    agents = [[1, -1, 1, -1]]
    out = multi_agent_step(agents, [0.0], threshold=0.5, erosion_pairs=2)
    # After shift: [-1, 1, -1], then append 0: [-1, 1, -1, 0], sum = -1
    # After erosion (1 pair): [0, 0, -1, 0], sum = -1
    # So erosion preserves the sum of what it receives
    assert sum(out[0]) == -1


def test_multi_agent_step_erosion_net_zero_input():
    # If we start with a trace that will be net-zero after shift+append
    agents = [[1, -1, 1]]  # sum = 1
    # After shift: [-1, 1], append 0: [-1, 1, 0], sum = 0
    out = multi_agent_step(agents, [0.0], threshold=0.5, erosion_pairs=2)
    assert sum(out[0]) == 0
