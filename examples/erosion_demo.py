"""Example: ternary erosion preserving net-zero."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model import erosion_step, net_zero

state = [1, 1, -1, -1, 0, 1, -1, 1, -1]
print("before:", state, "sum=", sum(state), "net_zero=", net_zero(state))
out = erosion_step(state, pairs=3)
print("after: ", out, "sum=", sum(out), "net_zero=", net_zero(out))
