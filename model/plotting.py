"""Optional visualization (matplotlib)."""

from __future__ import annotations

import math
from typing import Any

from model.dark_energy import delta_norm


def plot_delta(
    w0: float = -0.75,
    wa: float = -0.87,
    zmax: float = 2.0,
    n: int = 100,
) -> Any:
    """Plot delta_norm(z) for a CPL model. Requires matplotlib."""
    if n < 2:
        raise ValueError("n must be >= 2")
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise RuntimeError("matplotlib not installed") from e

    zs = [i * zmax / (n - 1) for i in range(n)]
    ds = [delta_norm(z, w0, wa) for z in zs]
    plt.figure()
    plt.plot(zs, ds, label=f"w0={w0}, wa={wa}")
    plt.axhline(0, color="k", linewidth=0.5)
    plt.xlabel("redshift z")
    plt.ylabel("delta_norm(z)")
    plt.title("Dark energy density deviation")
    plt.legend()
    plt.tight_layout()
    return plt


def plot_cosmic_web(depth: int = 4, scale: float = 1.0) -> Any:
    """Plot a simple fractal tree (cosmic web analogue). Requires matplotlib."""
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise RuntimeError("matplotlib not installed") from e

    lines: list[tuple[tuple[float, float], tuple[float, float]]] = []

    def branch(x: float, y: float, angle: float, length: float, remaining: int) -> None:
        if remaining == 0:
            return
        x2 = x + length * math.cos(angle)
        y2 = y + length * math.sin(angle)
        lines.append(((x, y), (x2, y2)))
        branch(x2, y2, angle - 0.4, length * 0.7, remaining - 1)
        branch(x2, y2, angle + 0.4, length * 0.7, remaining - 1)

    branch(0.0, 0.0, math.pi / 2, 1.0 * scale, depth)
    _, ax = plt.subplots()
    for (x1, y1), (x2, y2) in lines:
        ax.plot([x1, x2], [y1, y2], color="steelblue", linewidth=0.8)
    ax.set_aspect("equal")
    ax.set_title("Cosmic Web (fractal tree)")
    ax.axis("off")
    plt.tight_layout()
    return plt
