"""Example: ternary erosion preserving net-zero."""
from engine import net_zero, erosion_step

state = [1, 1, -1, -1, 0, 1, -1, 1, -1]
print("before:", state, "sum=", sum(state), "net_zero=", net_zero(state))
out = erosion_step(state, pairs=3)
print("after: ", out, "sum=", sum(out), "net_zero=", net_zero(out))
