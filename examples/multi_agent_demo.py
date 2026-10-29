"""Demo: multi-agent consciousness simulation."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model import multi_agent_step, network_closure, net_zero

agents = [[0, 0, 0] for _ in range(5)]
stimuli = [0.9, -0.8, 0.2, 0.9, -0.9, 0.1]
for t, s in enumerate(stimuli):
    agents = multi_agent_step(agents, [s], threshold=0.5, erosion_pairs=1)
    print(f"t={t} stim={s:.1f} closure={network_closure(agents):.2f} "
          f"states={[a[-1] for a in agents]}")
print("final agents:")
for a in agents:
    print(" ", a, "sum=", sum(a), "net_zero=", net_zero(a))
