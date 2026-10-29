"""Dynamic dark energy (A2.2, GROUNDING.md).

CPL equation of state, rho_Lambda(z), DESI-anchored predictions.
"""

from __future__ import annotations

import math

# DESI DR2 anchored reference values (GROUNDING.md)
DESI_REFERENCE: dict[str, object] = {
    "w0_range": (-0.85, -0.66),
    "wa_range": (-1.11, -0.61),
    "sig_DESI_CMB": 3.1,
    "sig_with_SNe": (2.8, 4.2),
}


def w_cpl(a: float, w0: float, wa: float) -> float:
    """CPL equation of state w(a) = w0 + wa*(1 - a)."""
    return w0 + wa * (1.0 - a)


def rho_lambda_ratio(z: float, w0: float, wa: float) -> float:
    """rho_DE(z)/rho_DE(0) for CPL. a = 1/(1+z).

    rho ~ (1+z)^{3(1+w0+wa)} * exp(-3*wa*z/(1+z))
    """
    # a = 1.0 / (1.0 + z)  # not used directly in computation
    exponent: float = 3.0 * (1.0 + w0 + wa)
    exp_arg: float = -3.0 * wa * z / (1.0 + z)
    result: float = (1.0 + z) ** exponent * math.exp(exp_arg)
    return result


def delta_norm(z: float, w0: float, wa: float) -> float:
    """Normalized delta(t) of A2.2: delta/rho0 = rho_DE(z)/rho_DE(0) - 1.

    Present (z=0) is zero. Near-present derivative is positive for the
    DESI-anchored quintom-B case (density increasing backward from today);
    the integrated value at z~1 is sample-dependent (see GROUNDING.md §2.4).
    """
    return rho_lambda_ratio(z, w0, wa) - 1.0


def delta_derivative_present(w0: float, wa: float, h: float = 1e-5) -> float:
    """Numerical derivative d(delta_norm)/dz at z=0 (present).

    For the grounded (decaying) case this should be > 0.
    """
    return (delta_norm(h, w0, wa) - delta_norm(0.0, w0, wa)) / h


def delta_norm_uncertainty(
    w0: float,
    wa: float,
    sigma_w0: float,
    sigma_wa: float,
    h: float = 1e-5,
) -> tuple[float, float]:
    """Approximate 1-sigma uncertainty on delta_norm at z=1 via finite differences.

    Returns (base_value, uncertainty).
    """
    base = delta_norm(1.0, w0, wa)
    dw0 = (delta_norm(1.0, w0 + h, wa) - delta_norm(1.0, w0 - h, wa)) / (2 * h)
    dwa = (delta_norm(1.0, w0, wa + h) - delta_norm(1.0, w0, wa - h)) / (2 * h)
    var = (dw0 * sigma_w0) ** 2 + (dwa * sigma_wa) ** 2
    return abs(base), math.sqrt(var)


def check_predictions(
    w0: float,
    wa: float,
    sigma_w0: float,
    sigma_wa: float,
) -> dict[str, bool]:
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
