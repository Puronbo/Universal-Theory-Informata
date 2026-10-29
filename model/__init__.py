"""Model engine package.

A rigorous alternative architecture of reality: axioms, engine, Lean 4 core.

Modules:
- ternary: three-state grammar and net-zero invariant (A0.2, A0.3).
- recursion: fixed-point iteration (awakening) and purge (A1.5).
- cusp: cusp catastrophe roots, bifurcation set, crease density proxy.
- dark_energy: CPL w(a), rho_Lambda(z), DESI-anchored predictions (A2.2).
- rolling_fold: photon <-> dark energy duality (A2.5).
- playhead: Planck-time discrete frame reading (A4.1, A4.3, A4.4).
- timeline: 26-year milestone (A6.1, A6.3).
- impedance: Universal impedance & mass gap (L.O.R.E. proof sectors).
- geometry: Particles as stretched points (A3.6).
- stroboscopic: Stroboscopic sampling (A4.6).
- search: Meta-audit / exploration utilities.
- prized_problems: Collatz, Goldbach, Zeta evidence (not proofs).
- recursion_families: Mandelbrot / Kené-style complex iteration (R4).
- consciousness: Attention, closure (phenomenological, A3.2, A4.6, A5.3).
- multi_agent: Multi-agent consciousness simulation (phenomenological).
- self_looping: Cosmological coupling & UV/IR inversion (A8).
- equator: Equator of Scale (A9.1-A9.4).
- clock: Clock, broken mirror, entropy brake (A10).
- plotting: Optional matplotlib visualization.

Constants:
- VOID, ACTIVE, BALANCE: Ternary state values
- VALID_STATES: Tuple of valid states
- ANCHOR_DATE: date(2000, 10, 26)
- MILESTONE_YEARS: 26
- PLANCK_TIME: 5.391247e-44
- DESI_REFERENCE: DESI DR2 reference values
"""

from model.clock import (
    PLANCK_TIME,
    cp_violation_tilt,
    entropy_brake,
    planck_refresh_rate,
)
from model.consciousness import (
    attention_trace,
    closure_check,
    conscious_moment,
)
from model.cusp import (
    bifurcation_value,
    crease_density,
    crease_density_proxy,
    cusp_roots,
    fold_spectrum,
    on_cusp,
)
from model.dark_energy import (
    DESI_REFERENCE,
    check_predictions,
    delta_derivative_present,
    delta_norm,
    delta_norm_uncertainty,
    rho_lambda_ratio,
    w_cpl,
)
from model.dimensions import (
    dimension_bleed,
    dimension_circle,
)
from model.equator import (
    gauge_node,
    imaginary_rotate,
    scale_midpoint,
)
from model.geometry import (
    apparent_separation,
    stretched_distance,
)
from model.hyperbolic import (
    c0_center,
    novelty_score,
    poincare_distance,
)
from model.impedance import (
    grokking_delay,
    impedance_series,
    resonance_w0,
    schwinger_mass_gap,
    thirring_gn_mass_gap,
)
from model.mp_operator import (
    mp_discriminant,
    mp_regime,
    mp_roots,
)
from model.multi_agent import (
    multi_agent_step,
    network_closure,
)
from model.neural_phase import (
    simulate_neural_phase_locking,
    coherence,
    noise_filtering,
)
from model.rubber_ball import (
    hertz_contact_radius,
    hertz_indentation,
    mie_efficiency,
    thermal_speed,
)
from model.eeg_stream import (
    bandpass_filter,
    fft_magnitude,
    channel_coherence,
    process_eeg_stream,
)
from model.millennium import (
    poincare_closed,
    navier_stokes_phase_bleed,
)
from model.playhead import (
    Playhead,
)
from model.plotting import (
    plot_cosmic_web,
    plot_delta,
)
from model.prized_problems import (
    collatz_spine_check,
    collatz_spine_sum,
    goldbach_check,
    zeta_partial,
)
from model.recursion import (
    canvas_energy,
    erosion_step,
    iterate,
    purge_derivative,
    purge_if_flat,
)
from model.recursion_families import (
    alias_shift_prediction,
    fractal_dimension,
    julia_escape,
    julia_fractal_dimension,
    kene_recursive,
    kene_step,
    mandelbrot_escape,
    rg_beta,
    rg_fixed_point,
    rg_fixed_point_prediction,
    rg_flow_trajectory,
    rg_flow_with_beta,
    scale_invariance_check,
    stroboscopic_shift,
    zeno_freeze,
)
from model.rolling_fold import (
    roll_convert,
    roll_orientation,
)
from model.search import (
    search_text,
)
from model.self_looping import (
    cosmological_coupling,
    portal_journey,
    uv_ir_inversion,
)
from model.stroboscopic import (
    strobe,
)
from model.ternary import (
    ACTIVE,
    BALANCE,
    VALID_STATES,
    VOID,
    is_valid_state,
    net_zero,
    ternarize,
    ternary_compose,
)
from model.timeline import (
    ANCHOR_DATE,
    MILESTONE_YEARS,
    logistic,
    milestone_date,
    milestone_reached,
    years_since_anchor,
)

__all__ = [
    # Constants
    "VOID",
    "ACTIVE",
    "BALANCE",
    "VALID_STATES",
    "ANCHOR_DATE",
    "MILESTONE_YEARS",
    "PLANCK_TIME",
    "DESI_REFERENCE",
    # Ternary
    "is_valid_state",
    "net_zero",
    "ternary_compose",
    "ternarize",
    # Recursion
    "iterate",
    "purge_if_flat",
    "purge_derivative",
    "canvas_energy",
    "erosion_step",
    # Cusp
    "cusp_roots",
    "bifurcation_value",
    "on_cusp",
    "crease_density",
    "crease_density_proxy",
    "fold_spectrum",
    # Dark Energy
    "w_cpl",
    "rho_lambda_ratio",
    "delta_norm",
    "delta_derivative_present",
    "delta_norm_uncertainty",
    "check_predictions",
    # Dimensions
    "dimension_circle",
    "dimension_bleed",
    # Rolling Fold
    "roll_orientation",
    "roll_convert",
    # Playhead
    "Playhead",
    # Timeline
    "milestone_date",
    "years_since_anchor",
    "milestone_reached",
    "logistic",
    # Impedance
    "resonance_w0",
    "impedance_series",
    "schwinger_mass_gap",
    "thirring_gn_mass_gap",
    "grokking_delay",
    # MP-Operator
    "mp_discriminant",
    "mp_regime",
    "mp_roots",
    # Geometry
    "stretched_distance",
    "apparent_separation",
    # Hyperbolic
    "c0_center",
    "novelty_score",
    "poincare_distance",
    # Stroboscopic
    "strobe",
    # Search
    "search_text",
    # Prized Problems
    "collatz_spine_sum",
    "collatz_spine_check",
    "goldbach_check",
    "zeta_partial",
    # Recursion Families
    "alias_shift_prediction",
    "fractal_dimension",
    "julia_escape",
    "julia_fractal_dimension",
    "kene_recursive",
    "kene_step",
    "mandelbrot_escape",
    "rg_beta",
    "rg_fixed_point",
    "rg_fixed_point_prediction",
    "rg_flow_trajectory",
    "rg_flow_with_beta",
    "scale_invariance_check",
    "stroboscopic_shift",
    "zeno_freeze",
    # Consciousness
    "attention_trace",
    "conscious_moment",
    "closure_check",
    # Multi-Agent
    "multi_agent_step",
    "network_closure",
    # Rubber Ball
    "hertz_contact_radius",
    "hertz_indentation",
    "mie_efficiency",
    "thermal_speed",
    # Neural Phase
    "simulate_neural_phase_locking",
    "coherence",
    "noise_filtering",
    # EEG Stream
    "bandpass_filter",
    "fft_magnitude",
    "channel_coherence",
    "process_eeg_stream",
    # Millennium
    "poincare_closed",
    "navier_stokes_phase_bleed",
    # Self-Looping
    "cosmological_coupling",
    "uv_ir_inversion",
    "portal_journey",
    # Equator
    "scale_midpoint",
    "imaginary_rotate",
    "gauge_node",
    # Clock
    "planck_refresh_rate",
    "cp_violation_tilt",
    "entropy_brake",
    # Plotting
    "plot_cosmic_web",
    "plot_delta",
]

__version__ = "0.1.0"
