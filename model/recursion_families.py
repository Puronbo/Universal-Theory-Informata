"""Recursion families (R4): Mandelbrot / Kené-style complex iteration."""

from __future__ import annotations


def kene_step(z: complex, c: complex) -> complex:
    """One step of the Kené/Mandelbrot-style recursion: z -> z^2 + c."""
    return z * z + c


def mandelbrot_escape(c: complex, max_iter: int = 100, radius: float = 2.0) -> tuple[bool, int]:
    """Iterate z_{n+1}=z_n^2+c from z0=0; return (escaped, n)."""
    z = 0 + 0j
    for n in range(1, max_iter + 1):
        z = z * z + c
        if abs(z) > radius:
            return True, n
    return False, max_iter


def julia_escape(z0, c, max_iter=100, radius=2.0):
    """Iterate z -> z^2 + c from z0 (Julia set); return (escaped, n)."""
    z = z0
    for n in range(1, max_iter + 1):
        z = z * z + c
        if abs(z) > radius:
            return True, n
    return False, max_iter


def rg_fixed_point(g, target=0.0, steps=1000, lr=0.01):
    """Toy RG flow toward a fixed point."""
    x = g
    for _ in range(steps):
        x = x - lr * (x - target)
    return x


def fractal_dimension(points, box_sizes=None):
    """Box-counting fractal dimension estimate for a set of (x,y) points."""
    if not points:
        return 0.0
    if box_sizes is None:
        box_sizes = [0.5, 0.25, 0.125, 0.0625]
    counts = []
    for eps in box_sizes:
        boxes = set()
        for x, y in points:
            boxes.add((int(x / eps), int(y / eps)))
        counts.append(len(boxes))
    import math
    if len(counts) < 2:
        return 0.0
    xs = [math.log(1.0 / e) for e in box_sizes]
    ys = [math.log(c) if c > 0 else 0.0 for c in counts]
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    return num / den if den != 0 else 0.0


def rg_flow_trajectory(g0, target=0.0, steps=50, lr=0.1):
    """Return the full RG flow trajectory toward a fixed point."""
    traj = [g0]
    x = g0
    for _ in range(steps):
        x = x - lr * (x - target)
        traj.append(x)
    return traj
