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


def ternary_compose(states: Iterable[int]) -> float:
    """Compose ternary states into a single normalized value in [-1, 1]."""
    s = list(states)
    if not s:
        return 0.0
    return max(-1.0, min(1.0, sum(s) / len(s)))


def ternarize(x: float) -> int:
    """Map a real drive to the nearest ternary state.

    Thresholds ±1/3 are a heuristic mapping (not derived); see AXIOMS A0.2.
    """
    if x > 1.0 / 3.0:
        return ACTIVE
    if x < -1.0 / 3.0:
        return BALANCE
    return VOID


# ---------------------------------------------------------------------------
# 2. Recursion / awakening (A5.1, A1.5 purge)
# ---------------------------------------------------------------------------

def iterate(f: Callable[[float], float], x0: float, n: int = 10000,
            tol: float = 1e-12, detect_cycle: bool = False) -> Tuple[float, int, bool, int]:
    """Iterate x_{k+1}=f(x_k) until fixed point, cycle, or max steps.

    Returns (x, steps, converged, cycle_length). cycle_length=0 if none detected.
    Backward-compatible: callers using 3-tuple unpacking must update to 4-tuple.
    """
    x = x0
    seen = {}
    for i in range(1, n + 1):
        xn = f(x)
        if not math.isfinite(xn):
            return x, i, False, 0
        if detect_cycle and x in seen:
            return x, i, False, i - seen[x]
        seen[x] = i
        if abs(xn - x) < tol:
            return xn, i, True, 0
        x = xn
    return x, n, False, 0


def purge_if_flat(ys: List[float], eps: float = 1e-9) -> bool:
    """Automated purge (A1.5): True if the last change is ~0 (y'=0).

    Heuristic: compares only the last two samples; not a full derivative.
    """
    if len(ys) < 2:
        return False
    return abs(ys[-1] - ys[-2]) < eps


# ---------------------------------------------------------------------------
# 2c. Derivative-based purge + canvas energy (enhancements)
# ---------------------------------------------------------------------------

def purge_derivative(ys: List[float], eps: float = 1e-9) -> bool:
    """Purge if the mean absolute successive difference is below eps."""
    if len(ys) < 2:
        return False
    diffs = [abs(ys[i] - ys[i-1]) for i in range(1, len(ys))]
    return (sum(diffs) / len(diffs)) < eps


def canvas_energy(scale_factor: float) -> float:
    """Energy density of the canvas at a given scale (E ~ 1/scale)."""
    if scale_factor <= 0:
        raise ValueError("scale_factor must be > 0")
    return 1.0 / scale_factor


# ---------------------------------------------------------------------------
# 2b. Erosion (A7.4)
# ---------------------------------------------------------------------------

def erosion_step(states: List[int], pairs: int = 1) -> List[int]:
    """Erode `pairs` of (+1,-1) into (0,0), preserving net-zero.

    Returns a new list. If fewer than `pairs` opposing pairs exist, erodes
    as many as possible.
    """
    out = list(states)
    pos = [i for i, v in enumerate(out) if v == 1]
    neg = [i for i, v in enumerate(out) if v == -1]
    k = min(pairs, len(pos), len(neg))
    for a, b in zip(pos[:k], neg[:k]):
        out[a] = 0
        out[b] = 0
    return out


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

    Present (z=0) is zero. Near-present derivative is positive for the
    DESI-anchored quintom-B case (density increasing backward from today);
    the integrated value at z~1 is sample-dependent (see GROUNDING.md §2.4).
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
# 4b. Rolling-fold duality (A2.5): photon <-> dark energy
# ---------------------------------------------------------------------------

def roll_orientation(angle_deg: float) -> str:
    """Orientation of the canvas-fold at a given roll angle.

    0 deg (mod 180) -> 'photon' (crease, folded)
    90 deg (mod 180) -> 'dark_energy' (unfolded tension)
    """
    a = angle_deg % 180.0
    if a < 45.0 or a >= 135.0:
        return "photon"
    return "dark_energy"


def roll_convert(crease_density: float, total: float = 1.0) -> tuple:
    """Convert a crease density into (photon_fraction, dark_energy_fraction).

    Conservation: photon + dark_energy = total.
    """
    p = max(0.0, min(total, crease_density))
    return (p, total - p)


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


# ---------------------------------------------------------------------------
# 6. Timeline / 26-year milestone (A6.1, A6.3)
# ---------------------------------------------------------------------------

from datetime import date

ANCHOR_DATE = date(2000, 10, 26)
MILESTONE_YEARS = 26


def milestone_date() -> date:
    return ANCHOR_DATE.replace(year=ANCHOR_DATE.year + MILESTONE_YEARS)


def years_since_anchor(now: date = None) -> float:
    if now is None:
        now = date.today()
    delta = now - ANCHOR_DATE
    return delta.days / 365.25


def milestone_reached(now: date = None) -> bool:
    if now is None:
        now = date.today()
    return now >= milestone_date()


def logistic(r: float):
    """Return f(x)=r*x*(1-x) for use with iterate()."""
    def f(x: float) -> float:
        return r * x * (1.0 - x)
    return f


# ---------------------------------------------------------------------------
# 8. Universal impedance & mass gap (L.O.R.E. proof sectors)
# ---------------------------------------------------------------------------

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
    return Lambda / math.sinh(2.0 * math.pi / (g_eff ** 2 * (N - 1.0)))


def grokking_delay(g_eff: float, V_mem: float, V_post: float) -> float:
    """Grokking delay T = (1/g_eff)*ln(V_mem/V_post)."""
    return (1.0 / g_eff) * math.log(V_mem / V_post)


# ---------------------------------------------------------------------------
# 9. Geometry: particles as stretched points (A3.6)
# ---------------------------------------------------------------------------

def stretched_distance(d0: float, scale_factor: float) -> float:
    """Apparent separation of two points under canvas stretching (A3.6)."""
    return d0 * scale_factor


def apparent_separation(points: List, scale_factor: float) -> list:
    """Pairwise distances among points scaled by the canvas stretch factor."""
    out = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d0 = abs(points[j] - points[i])
            out.append((i, j, d0 * scale_factor))
    return out


# ---------------------------------------------------------------------------
# 10. Stroboscopic sampling (A4.6)
# ---------------------------------------------------------------------------

def strobe(signal: List, rate: int) -> List:
    """Downsample a fine signal by `rate`, producing the frozen alias (blade)."""
    if rate < 1:
        raise ValueError("rate must be >= 1")
    return list(signal[::rate])


# ---------------------------------------------------------------------------
# 11. Search utility (meta-audit / exploration)
# ---------------------------------------------------------------------------

import re as _re
from pathlib import Path as _Path

def search_text(root, pattern, include="*.md", regex=False):
    """Search files under root for pattern. Returns list of (path, lineno, line)."""
    root = _Path(root)
    results = []
    for p in root.rglob(include):
        if not p.is_file():
            continue
        try:
            for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                if (pattern in line) if not regex else _re.search(pattern, line):
                    results.append((str(p), i, line.strip()))
        except (UnicodeDecodeError, OSError):
            continue
    return results


# ---------------------------------------------------------------------------
# 12. Prized-problem numerical sectors (evidence only, not proofs)
# ---------------------------------------------------------------------------

def collatz_spine_sum(k: int) -> int:
    """spineSum(k) = (4^(k+1) - 1) / 3."""
    return (4 ** (k + 1) - 1) // 3


def collatz_spine_check(k: int) -> bool:
    """Verify 4^(k+1) == 3*spineSum(k) + 1."""
    return 4 ** (k + 1) == 3 * collatz_spine_sum(k) + 1


def goldbach_check(n: int) -> bool:
    """Check Goldbach for even n >= 4: n = p + q with primes p,q."""
    if n < 4 or n % 2 != 0:
        return False
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    primes = [i for i in range(2, n) if sieve[i]]
    pset = set(primes)
    for p in primes:
        if (n - p) in pset:
            return True
    return False


def zeta_partial(s: float, N: int) -> float:
    """Partial sum sum_{n=1}^N 1/n^s (real s)."""
    return sum(1.0 / (n ** s) for n in range(1, N + 1))


def delta_norm_uncertainty(w0, wa, sigma_w0, sigma_wa, h=1e-5):
    """Approximate 1-sigma uncertainty on delta_norm at z=1 via finite differences."""
    base = delta_norm(1.0, w0, wa)
    dw0 = (delta_norm(1.0, w0 + h, wa) - delta_norm(1.0, w0 - h, wa)) / (2 * h)
    dwa = (delta_norm(1.0, w0, wa + h) - delta_norm(1.0, w0, wa - h)) / (2 * h)
    var = (dw0 * sigma_w0) ** 2 + (dwa * sigma_wa) ** 2
    return abs(base), math.sqrt(var)


# ---------------------------------------------------------------------------
# 13. Recursion families (R4): Mandelbrot / Kené-style complex iteration
# ---------------------------------------------------------------------------

def kene_step(z, c):
    """One step of the Kené/Mandelbrot-style recursion: z -> z^2 + c."""
    return z * z + c


def mandelbrot_escape(c, max_iter=100, radius=2.0):
    """Iterate z_{n+1}=z_n^2+c from z0=0; return (escaped, n)."""
    z = 0 + 0j
    for n in range(1, max_iter + 1):
        z = z * z + c
        if abs(z) > radius:
            return True, n
    return False, max_iter


# ---------------------------------------------------------------------------
# 14. Optional visualization (matplotlib)
# ---------------------------------------------------------------------------

def plot_delta(w0=-0.75, wa=-0.87, zmax=2.0, n=100):
    """Plot delta_norm(z) for a CPL model. Requires matplotlib."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise RuntimeError("matplotlib not installed")
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


# ---------------------------------------------------------------------------
# 15. Consciousness / attention (phenomenological, A3.2, A4.6, A5.3)
# ---------------------------------------------------------------------------

def attention_trace(stimuli, threshold=0.5):
    """Map a stimulus stream to ternary attention states.

    active (+1) if stimulus > threshold, balance (-1) if < -threshold, else void (0).
    """
    out = []
    for s in stimuli:
        if s > threshold:
            out.append(1)
        elif s < -threshold:
            out.append(-1)
        else:
            out.append(0)
    return out


def conscious_moment(stream, sample_rate=1):
    """A conscious 'now' is a stroboscopic alias of the stimulus stream (A4.6)."""
    return strobe(list(stream), sample_rate)


def closure_check(exterior, interior, tol=1e-9):
    """Awakening criterion: exterior and interior states coincide (A5.3, E≡I)."""
    if len(exterior) != len(interior):
        return False
    return all(abs(e - i) < tol for e, i in zip(exterior, interior))


# ---------------------------------------------------------------------------
# 16. Multi-agent consciousness simulation (phenomenological)
# ---------------------------------------------------------------------------

def multi_agent_step(agents, stimuli, threshold=0.5, erosion_pairs=1):
    """Advance each agent's attention trace and erode noise.

    agents: list of lists (ternary states per agent).
    Returns updated agents.
    """
    out = []
    for a in agents:
        # shift: drop oldest, append new attention state from stimulus
        trace = list(a)
        if trace:
            trace = trace[1:]
        # use the last stimulus value for the new slot
        new_val = stimuli[-1] if stimuli else 0.0
        new_state = 1 if new_val > threshold else (-1 if new_val < -threshold else 0)
        trace.append(new_state)
        trace = erosion_step(trace, pairs=erosion_pairs)
        out.append(trace)
    return out


def network_closure(agents):
    """Fraction of agents whose state is net-zero (balanced awareness)."""
    if not agents:
        return 0.0
    balanced = sum(1 for a in agents if net_zero(a))
    return balanced / len(agents)


if __name__ == "__main__":
    # small demo
    import math
    print("ternary net_zero([1,-1,0]):", net_zero([1, -1, 0]))
    print("cusp roots a=1,b=0:", cusp_roots(1.0, 0.0))
    print("bifurcation a=1,b=0:", bifurcation_value(1.0, 0.0))
    print("w(0.5) CPL:", w_cpl(0.5, -0.75, -0.87))
    print("rho ratio z=1:", rho_lambda_ratio(1.0, -0.75, -0.87))
    x, steps, conv, _ = iterate(lambda x: math.cos(x), 1.0)
    print("fixed point cos:", x, steps, conv)
    print("logistic r=2.5 fixed point:", iterate(logistic(2.5), 0.5)[0])
    print("anchor:", ANCHOR_DATE, "milestone:", milestone_date(),
          "reached:", milestone_reached(), "years:", round(years_since_anchor(), 3))
