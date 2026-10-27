"""Engine for the model.

Modules:
- ternary: three-state grammar and net-zero invariant.
- recursion: fixed-point iteration (awakening) and purge (y'=0).
- cusp: cusp catastrophe roots, bifurcation set, crease density proxy.
- dark_energy: CPL w(a), rho_Lambda(z), DESI-anchored predictions.

Pure Python, no external dependencies.
"""
from __future__ import annotations

import math
from typing import Callable, Iterable, List, Tuple


# ---------------------------------------------------------------------------
# 1. Ternary logic (A0.2, A0.3)
# ---------------------------------------------------------------------------

VOID, ACTIVE, BALANCE = 0, 1, -1
VALID_STATES = (VOID, ACTIVE, BALANCE)


def is_valid_state(v) -> bool:
    return v in VALID_STATES


def net_zero(states: Iterable[int]) -> bool:
    """Net-zero invariant (A0.3): sum of states in a closed subsystem == 0."""
    return sum(states) == 0


def ternarize(x: float) -> int:
    """Map a real drive to the nearest ternary state."""
    if x > 1.0 / 3.0:
        return ACTIVE
    if x < -1.0 / 3.0:
        return BALANCE
    return VOID


# ---------------------------------------------------------------------------
# 2. Recursion / awakening (A5.1, A1.5 purge)
# ---------------------------------------------------------------------------

def iterate(f: Callable[[float], float], x0: float, n: int = 10000,
            tol: float = 1e-12) -> Tuple[float, int, bool]:
    """Iterate x_{k+1}=f(x_k) until fixed point or max steps.

    Returns (x, steps, converged).
    """
    x = x0
    for i in range(1, n + 1):
        xn = f(x)
        if not math.isfinite(xn):
            return x, i, False
        if abs(xn - x) < tol:
            return xn, i, True
        x = xn
    return x, n, False


def purge_if_flat(ys: List[float], eps: float = 1e-9) -> bool:
    """Automated purge (A1.5): True if the last change is ~0 (y'=0)."""
    if len(ys) < 2:
        return False
    return abs(ys[-1] - ys[-2]) < eps


# ---------------------------------------------------------------------------
# 3. Cusp catastrophe (candidate formalization, see FOLDING_CALIBRATION.md)
# ---------------------------------------------------------------------------

def cusp_roots(a: float, b: float) -> List[complex]:
    """Roots of x^3 - a*x - b = 0 (equilibrium surface V'=0).

    Uses Cardano's formula; returns all three roots (real or complex).
    """
    # depressed cubic t^3 + p t + q = 0 with p=-a, q=-b
    p, q = -a, -b
    disc = (q / 2.0) ** 2 + (p / 3.0) ** 3
    if disc >= 0:
        # one real root
        u = (-q / 2.0 + math.sqrt(disc)) ** (1.0 / 3.0)
        v = (-q / 2.0 - math.sqrt(disc)) ** (1.0 / 3.0)
        r1 = u + v
        # complex pair
        w = complex(-0.5, math.sqrt(3) / 2.0)
        r2 = w * u + (w ** 2) * v
        r3 = (w ** 2) * u + w * v
        return [r1, r2, r3]
    # three real roots (casus irreducibilis)
    rho = 2.0 * math.sqrt(-p / 3.0)
    theta = math.acos((3.0 * q) / (2.0 * p) * math.sqrt(-3.0 / p)) if p != 0 else 0.0
    r1 = rho * math.cos(theta / 3.0)
    r2 = rho * math.cos((theta + 2 * math.pi) / 3.0)
    r3 = rho * math.cos((theta + 4 * math.pi) / 3.0)
    return [r1, r2, r3]


def bifurcation_value(a: float, b: float) -> float:
    """8 a^3 - 27 b^2. Zero on the cusp curve."""
    return 8.0 * a ** 3 - 27.0 * b ** 2


def on_cusp(a: float, b: float, tol: float = 1e-9) -> bool:
    return abs(bifurcation_value(a, b)) < tol


def crease_density_proxy(a: float, b: float, xs: Iterable[float],
                        eps: float = 0.05) -> float:
    """Fraction of xs lying within eps of any root of x^3 - a x - b = 0.

    Toy analog of crease density: how many sample points sit at the
    switching boundary. Only meaningful in controlled settings.
    """
    roots = cusp_roots(a, b)
    real_roots = [r.real for r in roots if abs(r.imag) < 1e-9]
    if not real_roots:
        real_roots = [r.real for r in roots]
    n = 0
    total = 0
    for x in xs:
        total += 1
        if any(abs(x - r) < eps for r in real_roots):
            n += 1
    return n / total if total else 0.0


# ---------------------------------------------------------------------------
# 4. Dynamic dark energy (A2.2, GROUNDING.md)
# ---------------------------------------------------------------------------

def w_cpl(a: float, w0: float, wa: float) -> float:
    """CPL equation of state w(a) = w0 + wa*(1 - a)."""
    return w0 + wa * (1.0 - a)


def rho_lambda_ratio(z: float, w0: float, wa: float) -> float:
    """rho_DE(z)/rho_DE(0) for CPL. a = 1/(1+z)."""
    a = 1.0 / (1.0 + z)
    # rho ~ (1+z)^{3(1+w0+wa)} * exp(-3*wa*z/(1+z))
    return (1.0 + z) ** (3.0 * (1.0 + w0 + wa)) * math.exp(
        -3.0 * wa * z / (1.0 + z)
    )


def delta_norm(z: float, w0: float, wa: float) -> float:
    """Normalized delta(t) of A2.2: delta/rho0 = rho_DE(z)/rho_DE(0) - 1.

    Present (z=0) is zero. Positive in the past for the DESI-anchored
    (quintom B) case, i.e. density was higher in the past and is decaying.
    """
    return rho_lambda_ratio(z, w0, wa) - 1.0


def delta_derivative_present(w0: float, wa: float, h: float = 1e-5) -> float:
    """Numerical derivative d(delta_norm)/dz at z=0 (present).

    For the grounded (decaying) case this should be > 0? Note delta_norm(z)
    for z>0 (past) positive and decreasing toward 0 as z->0+, so as z
    increases from 0, delta increases => derivative at 0+ > 0. We report
    derivative w.r.t. z at 0.
    """
    return (delta_norm(h, w0, wa) - delta_norm(0.0, w0, wa)) / h


# ---------------------------------------------------------------------------
# 5. Playhead sampling (A4.1, A4.3, A4.4)
# ---------------------------------------------------------------------------

class Playhead:
    """Reads a static 4D block frame-by-frame at Planck intervals.

    No frame is skipped and no frame is repeated (A4.4).
    """

    def __init__(self, block: List, tau: float = 1.0):
        self.block = list(block)
        self.tau = tau
        self._i = 0

    def reset(self) -> None:
        self._i = 0

    @property
    def index(self) -> int:
        return self._i

    def read(self, t: float):
        """Frame at time t: index = floor(t/tau), clamped to block bounds."""
        if t < 0:
            return None
        idx = int(t // self.tau)
        if idx >= len(self.block):
            idx = len(self.block) - 1
        return self.block[idx]

    def step(self):
        """Advance exactly one Planck interval and return that frame."""
        if self._i >= len(self.block):
            return None
        frame = self.block[self._i]
        self._i += 1
        return frame

    def read_all(self) -> List:
        """Read every frame once, in order, then stop."""
        out = list(self.block)
        self._i = len(self.block)
        return out


def check_predictions(w0: float, wa: float,
                      sigma_w0: float, sigma_wa: float) -> dict:
    """Evaluate P1-P3 from GROUNDING.md against a reported (w0, wa).

    P1: wa < 0 (weakening) at >=3 sigma  -> wa/sigma_wa < -3 (approx)
    P2: |w0+1| >= 0.1 at >=3 sigma      -> |w0+1|/sigma_w0 >= 3
    P3: if w0 < -1 (phantom today) -> sign flip needed
    """
    p1 = (wa < 0) and (abs(wa) / max(sigma_wa, 1e-12) >= 3.0)
    p2 = (abs(w0 + 1.0) / max(sigma_w0, 1e-12) >= 3.0) and (abs(w0 + 1.0) >= 0.1)
    p3_flip = w0 < -1.0
    return {
        "P1_weakening_3sigma": p1,
        "P2_amplitude_3sigma": p2,
        "P3_phantom_sign_flip_needed": p3_flip,
        "quintom_B_quadrant": (w0 > -1.0) and (wa < 0.0),
    }


# DESI DR2 anchored reference values (GROUNDING.md)
DESI_REFERENCE = {
    "w0_range": (-0.85, -0.66),
    "wa_range": (-1.11, -0.61),
    "sig_DESI_CMB": 3.1,
    "sig_with_SNe": (2.8, 4.2),
}


if __name__ == "__main__":
    # small demo
    print("ternary net_zero([1,-1,0]):", net_zero([1, -1, 0]))
    print("cusp roots a=1,b=0:", cusp_roots(1.0, 0.0))
    print("bifurcation a=1,b=0:", bifurcation_value(1.0, 0.0))
    print("w(0.5) CPL:", w_cpl(0.5, -0.75, -0.87))
    print("rho ratio z=1:", rho_lambda_ratio(1.0, -0.75, -0.87))
    x, steps, conv = iterate(lambda x: math.cos(x), 1.0)
    print("fixed point cos:", x, steps, conv)
