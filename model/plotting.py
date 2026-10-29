"""Optional visualization (matplotlib)."""

from __future__ import annotations

from typing import Any

from model.dark_energy import delta_norm


def plot_delta(
    w0: float = -0.75,
    wa: float = -0.87,
    zmax: float = 2.0,
    n: int = 100,
) -> Any:
    """Plot delta_norm(z) for a CPL model. Requires matplotlib."""
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
