"""Universal impedance & mass gap (L.O.R.E. proof sectors)."""

from __future__ import annotations

import math

# Physical constants
PLANCK_TIME: float = 5.391247e-44  # seconds


def resonance_w0(L: float, C: float) -> float:
    """Resonant angular frequency w0 = 1/sqrt(L*C)."""
    return 1.0 / math.sqrt(L * C)


def impedance_series(R: float, L: float, C: float, w: float) -> complex:
    """Series RLC impedance Z = R + i(wL - 1/(wC))."""
    return complex(R, w * L - 1.0 / (w * C))


def schwinger_mass_gap(e: float) -> float:
    """Schwinger (QED 1+1D) mass gap M = e/sqrt(pi)."""
    return e / math.sqrt(math.pi)


def thirring_gn_mass_gap(Lambda: float, g_eff: float, N: float) -> float:
    """Thirring-GN crossover mass gap M = Lambda/sinh(2*pi/(g_eff^2*(N-1)))."""
    return Lambda / math.sinh(2.0 * math.pi / (g_eff**2 * (N - 1.0)))


def grokking_delay(g_eff: float, V_mem: float, V_post: float) -> float:
    """Grokking delay T = (1/g_eff)*ln(V_mem/V_post)."""
    return (1.0 / g_eff) * math.log(V_mem / V_post)


def planck_refresh_rate() -> float:
    """Maximum refresh rate of the universal monitor (1 / t_P)."""
    return 1.0 / PLANCK_TIME
