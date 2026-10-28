"""Minimal game-engine-style simulation built on the model.

Concepts mapped:
- World state = canvas (A2) + agents (particles as stretched points, A3.6)
- Frame loop = playhead (A4.1, A4.4)
- Update = ternary attention + erosion (A7.4) + canvas stretch (A3.6)
- Render = stroboscopic alias (A4.6)
"""
from __future__ import annotations
import math
from engine import (net_zero, erosion_step, stretched_distance,
                    attention_trace, conscious_moment, delta_norm)


class World:
    def __init__(self, n_agents=5, seed=0):
        self.t = 0
        self.scale = 1.0
        self.agents = [[0, 0, 0] for _ in range(n_agents)]
        self.history = []

    def update(self, stimulus=0.0, stretch=1.0, erosion_pairs=1):
        self.t += 1
        self.scale *= stretch
        # attention
        new_states = []
        for a in self.agents:
            trace = a[1:] if a else []
            val = 1 if stimulus > 0.5 else (-1 if stimulus < -0.5 else 0)
            trace.append(val)
            trace = erosion_step(trace, pairs=erosion_pairs)
            new_states.append(trace)
        self.agents = new_states
        self.history.append([a[-1] for a in self.agents])

    def render(self):
        positions = [i * self.scale for i in range(len(self.agents))]
        states = [a[-1] for a in self.agents]
        print(f"t={self.t:3d} scale={self.scale:.3f} states={states} "
              f"balanced={sum(1 for a in self.agents if sum(a)==0)}/{len(self.agents)}")

    def run(self, stimuli, stretch=1.01, erosion_pairs=1):
        for s in stimuli:
            self.update(stimulus=s, stretch=stretch, erosion_pairs=erosion_pairs)
            self.render()


if __name__ == "__main__":
    w = World(n_agents=4)
    w.run([0.9, -0.8, 0.2, 0.9, -0.9, 0.1, 0.7, -0.6])
