"""End-to-end demo of the model pipeline.

Run: python simulate.py
"""
from model import (
    ternarize, iterate, purge_if_flat, erosion_step, Playhead,
    w_cpl, rho_lambda_ratio, delta_norm, milestone_date, milestone_reached,
)


def main():
    # 1. Recursion / awakening
    x, steps, conv, _ = iterate(lambda v: __import__("math").cos(v), 1.0)
    print(f"[recursion] fixed point = {x:.6f} in {steps} steps (converged={conv})")

    # 2. Purge when flat
    trace = [1.0, 0.7, 0.7000001]
    print(f"[purge] flat? {purge_if_flat(trace)}")

    # 3. Ternary net-zero + erosion
    state = [1, 1, -1, -1, 0, 1, -1]
    print(f"[ternary] before erosion: {state} sum={sum(state)}")
    state = erosion_step(state, pairs=2)
    print(f"[ternary] after  erosion: {state} sum={sum(state)}")

    # 4. Playhead reads a block
    block = ["frame0", "frame1", "frame2"]
    ph = Playhead(block, tau=1.0)
    print(f"[playhead] read(0.5)={ph.read(0.5)} read(2.3)={ph.read(2.3)} step={ph.step()}")

    # 5. Dark energy (DESI-anchored)
    w0, wa = -0.75, -0.87
    print(f"[darkE] w(0.5)={w_cpl(0.5,w0,wa):.3f} rho(z=1)={rho_lambda_ratio(1.0,w0,wa):.4f} "
          f"delta(z=1)={delta_norm(1.0,w0,wa):.4f}")

    # 6. Timeline
    print(f"[timeline] milestone {milestone_date()} reached={milestone_reached()}")


if __name__ == "__main__":
    main()