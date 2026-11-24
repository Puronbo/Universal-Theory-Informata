"""Model engine package.

A rigorous alternative architecture of reality: axioms, engine, Lean 4 core.

Modules:
- antithesis: Contractive, translating, and nilpotent counter-models; entropy; log conjugacy.
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
- roots: Integer roots and the root/power duality.
- mobius: Möbius transformations, composition, fixed points.
- duality: Binary poles and the involution that swaps them.
- fold: Quotient fold x+1/x and fundamental-domain representative.
- fold_corpus: Executable core of the Fold corpus: homothety, fold, cap/puncture ledger, closure, solid angle.
- grid_topology: Puncture versus hole on a finite lattice: Euler characteristic, bounded components, hole depth.
- unit_group: The multiplicative group, unit residues, and the projective reciprocal.
- step_expansion: One-step division by n/n^n, hyperfactorial product, and additive enclosure.
- lattice: Boolean lattice of pole strings over the dual pairs.
- phase: Complex phase, observable intensity, and wavelength/wavenumber.
- superoperator: Liouvillian commutator and commutant zero modes.
- symmetry_breaking: Double-well potential and a nonzero vacuum value (toy model).
- spacebar: Candidate parameters for the first-deviation press (proper time, phase, ticks).
- pressing: Toy checks for Page-Wootters time, GPS drift, de Sitter conformal time, Connes distance, and modular flow.
- vacuum_info: Bekenstein/holographic/de Sitter bounds, Landauer erasure, two-mode squeezing, and no-signaling.
- equator: Equator of Scale (A9.1-A9.4).
- clock: Clock, broken mirror, entropy brake (A10).
- phenomena: Phenomenon → canvas-operation map.
- plotting: Optional matplotlib visualization.
- cache_topology: Reuse-distance persistence, LRU simulation, and working-set estimates.
- latent_topology: Exact Rips persistence in dimensions 0 and 1, Betti numbers, hole scale.

Constants:
- VOID, ACTIVE, BALANCE: Ternary state values
- VALID_STATES: Tuple of valid states
- ANCHOR_DATE: date(2000, 10, 26)
- MILESTONE_YEARS: 26
- PLANCK_TIME: 5.391247e-44
- DESI_REFERENCE: DESI DR2 reference values
"""

from model.antithesis import (
    LogConjugacy,
    OrbitComparison,
    RegimeComparison,
    compare_log_conjugacy,
    compare_orbits,
    compare_regimes,
    contract,
    contract_orbit,
    entropy,
    exp_coordinate,
    information_loss,
    inversion_orbit,
    is_cyclic,
    log_coordinate,
    log_orbit,
    lyapunov_exponent,
    nilpotent_apply,
    nilpotent_orbit,
    orbit_period,
    translation,
    translation_orbit,
)
from model.cache_topology import (
    CacheStats,
    hit_rate_curve,
    merge_gaps,
    reuse_distances,
    saturation_capacity,
    simulate_lru,
    working_set_candidates,
    working_set_estimate,
    working_set_keys,
    working_set_splits,
)
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
from model.duality import (
    DUAL_PAIRS,
    DualPair,
    all_poles,
    dual_of,
    dual_pair,
    dual_pairs,
)
from model.eeg_stream import (
    bandpass_filter,
    channel_coherence,
    fft_magnitude,
    process_eeg_stream,
)
from model.equator import (
    gauge_node,
    imaginary_rotate,
    scale_midpoint,
)
from model.fold import (
    FoldComparison,
    compare_fold,
    fold,
    fold_from_log,
    fold_power,
    fold_preimages,
    representative,
)
from model.fold_corpus import (
    SurfaceLedger,
    compose_reflections,
    division_collapse_scale,
    division_point,
    doubling_agrees_with_negation,
    doubling_is_bijective,
    fold_orbit,
    horizon_ratio,
    midpoint_map,
    midpoint_scale,
    observer_split,
    projection_onto_crease,
    reflect_point,
    reflection_matrix,
    rotation_matrix,
    scale_determinant,
    scale_point,
    schwarzschild_radius,
    solid_angle_fraction,
    two_fold_rotation_angle,
    wheel_turn,
    wheel_turns,
)
from model.geometry import (
    apparent_separation,
    stretched_distance,
)
from model.grid_topology import (
    Cell,
    bounded_background_components,
    disk_cells,
    grid_hole_depth,
    grid_hole_scale,
    hole_is_resolved,
    lattice_euler_characteristic,
    lattice_step,
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
from model.latent_topology import (
    Point,
    betti_at,
    distance_matrix,
    dominant_bar,
    euclidean,
    hole_scale,
    persistence_diagram,
    rips_persistence,
)
from model.lattice import (
    WIDTH,
    PoleString,
    all_strings,
    atoms,
    bottom,
    canonical,
    coatoms,
    complement,
    from_bits,
    from_poles,
    join,
    leq,
    meet,
    orbit_count,
    orbit_rank_counts,
    rank_counts,
    same_orbit,
    strings_of_rank,
    top,
)
from model.millennium import (
    navier_stokes_phase_bleed,
    poincare_closed,
)
from model.mobius import (
    Mobius,
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
    coherence,
    noise_filtering,
    simulate_neural_phase_locking,
)
from model.phase import (
    WaveSample,
    conjugate,
    imaginary_height,
    intensity,
    phase_angle,
    phase_factor,
    real_width,
    rotate_quarter_turn,
    wave_sample,
    wavelength_from_wavenumber,
    wavenumber_from_wavelength,
)
from model.phenomena import (
    PHENOMENA,
    phenomena_list,
    phenomenon_type,
)
from model.playhead import (
    Playhead,
)
from model.plotting import (
    plot_cosmic_web,
    plot_delta,
)
from model.pressing import (
    BOLTZMANN,
    EARTH_GM,
    EARTH_RADIUS,
    GPS_CLOCK_FREQUENCY,
    GPS_ORBIT_RADIUS,
    SECONDS_PER_DAY,
    commutator_norm_two_point,
    conditional_state,
    connes_distance_two_point,
    desitter_closed_scale_factor,
    desitter_conformal_time_range,
    desitter_proper_time,
    gps_factory_detune,
    gps_gravitational_drift_us_per_day,
    gps_net_drift_us_per_day,
    gps_velocity_drift_us_per_day,
    modular_flow_bloch,
    modular_frequency,
    modular_hamiltonian,
    page_wootters_state,
    unruh_temperature,
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
from model.roots import (
    nth_root,
)
from model.rubber_ball import (
    hertz_contact_radius,
    hertz_indentation,
    mie_efficiency,
    thermal_speed,
)
from model.search import (
    search_text,
)
from model.self_looping import (
    cosmological_coupling,
    portal_journey,
    uv_ir_inversion,
)
from model.spacebar import (
    BARYON_TO_PHOTON_RATIO,
    REDUCED_PLANCK,
    SPEED_OF_LIGHT,
    ParameterCandidate,
    action_from_proper_time,
    candidate_parameters,
    compton_frequency,
    compton_period,
    is_on_mass_shell,
    mass_shell_residual,
    phase_from_action,
    phase_from_proper_time,
    spacebar_from_proper_time,
    spacebar_from_ticks,
    thermal_weight,
    ticks_from_proper_time,
    wrap_ticks,
)
from model.step_expansion import (
    additive_expansion,
    additive_interval,
    divide_by_step,
    expansion_term,
    hyperfactorial,
    log_expansion,
    multiplicative_collapse,
    multiplicative_expansion,
    step,
    tail_bound,
)
from model.stroboscopic import (
    strobe,
)
from model.superoperator import (
    commutant_dimension,
    commutator,
    commutes,
    dagger,
    diagonal,
    hilbert_schmidt,
    identity,
    is_self_adjoint,
    is_zero_matrix,
    liouvillian,
    liouvillian_eigenvalues,
    liouvillian_resolvent,
    matadd,
    matmul,
    matscale,
    matsub,
    resolvent_diagonal,
    resolvent_norm,
    trace,
    truncated_annihilation,
    truncated_creation,
    zero_matrix,
    zero_mode_pairs,
)
from model.symmetry_breaking import (
    double_well_curvature,
    double_well_minima,
    double_well_potential,
    is_symmetric_zero_unstable,
    vev_magnitude,
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
from model.unit_group import (
    divides,
    is_field_mod,
    projective_reciprocal,
    reciprocal,
    reciprocal_fixed_points,
    unit_inverse,
    units_mod,
)
from model.vacuum_info import (
    BITS_PER_NAT,
    PLANCK_LENGTH,
    apply_local_unitary,
    bekenstein_bits,
    desitter_bits,
    desitter_horizon_radius,
    holographic_bits,
    landauer_energy,
    marginal_probabilities,
    two_mode_mutual_information,
    two_mode_squeezing_photon_number,
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
    # Möbius
    "Mobius",
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
    # Antithesis
    "LogConjugacy",
    "OrbitComparison",
    "RegimeComparison",
    "compare_log_conjugacy",
    "compare_orbits",
    "compare_regimes",
    "contract",
    "contract_orbit",
    "entropy",
    "exp_coordinate",
    "information_loss",
    "inversion_orbit",
    "is_cyclic",
    "log_coordinate",
    "log_orbit",
    "lyapunov_exponent",
    "nilpotent_apply",
    "nilpotent_orbit",
    "orbit_period",
    "translation",
    "translation_orbit",
    # Fold
    "FoldComparison",
    "compare_fold",
    "fold",
    "fold_from_log",
    "fold_power",
    "fold_preimages",
    "representative",
    # Fold corpus
    "SurfaceLedger",
    "compose_reflections",
    "division_collapse_scale",
    "division_point",
    "doubling_agrees_with_negation",
    "doubling_is_bijective",
    "fold_orbit",
    "horizon_ratio",
    "midpoint_map",
    "midpoint_scale",
    "observer_split",
    "projection_onto_crease",
    "reflect_point",
    "reflection_matrix",
    "rotation_matrix",
    "scale_determinant",
    "scale_point",
    "schwarzschild_radius",
    "solid_angle_fraction",
    "two_fold_rotation_angle",
    "wheel_turn",
    "wheel_turns",
    # Lattice
    "WIDTH",
    "PoleString",
    "all_strings",
    "atoms",
    "bottom",
    "canonical",
    "coatoms",
    "complement",
    "from_bits",
    "from_poles",
    "join",
    "leq",
    "meet",
    "orbit_count",
    "orbit_rank_counts",
    "rank_counts",
    "same_orbit",
    "strings_of_rank",
    "top",
    # Phase
    "WaveSample",
    "conjugate",
    "imaginary_height",
    "intensity",
    "phase_angle",
    "phase_factor",
    "real_width",
    "rotate_quarter_turn",
    "wave_sample",
    "wavelength_from_wavenumber",
    "wavenumber_from_wavelength",
    # Superoperator
    "commutant_dimension",
    "commutes",
    "commutator",
    "dagger",
    "diagonal",
    "hilbert_schmidt",
    "identity",
    "is_self_adjoint",
    "is_zero_matrix",
    "liouvillian",
    "liouvillian_eigenvalues",
    "liouvillian_resolvent",
    "matadd",
    "matmul",
    "matscale",
    "matsub",
    "resolvent_diagonal",
    "resolvent_norm",
    "trace",
    "truncated_annihilation",
    "truncated_creation",
    "zero_matrix",
    "zero_mode_pairs",
    # Symmetry breaking
    "double_well_curvature",
    "double_well_minima",
    "double_well_potential",
    "is_symmetric_zero_unstable",
    "vev_magnitude",
    # Spacebar parameter
    "BARYON_TO_PHOTON_RATIO",
    "REDUCED_PLANCK",
    "SPEED_OF_LIGHT",
    "ParameterCandidate",
    "action_from_proper_time",
    "candidate_parameters",
    "compton_frequency",
    "compton_period",
    "is_on_mass_shell",
    "mass_shell_residual",
    "phase_from_action",
    "phase_from_proper_time",
    "spacebar_from_proper_time",
    "spacebar_from_ticks",
    "thermal_weight",
    "ticks_from_proper_time",
    "wrap_ticks",
    # Pressing
    "BOLTZMANN",
    "EARTH_GM",
    "EARTH_RADIUS",
    "GPS_CLOCK_FREQUENCY",
    "GPS_ORBIT_RADIUS",
    "SECONDS_PER_DAY",
    "commutator_norm_two_point",
    "conditional_state",
    "connes_distance_two_point",
    "desitter_closed_scale_factor",
    "desitter_conformal_time_range",
    "desitter_proper_time",
    "gps_factory_detune",
    "gps_gravitational_drift_us_per_day",
    "gps_net_drift_us_per_day",
    "gps_velocity_drift_us_per_day",
    "modular_flow_bloch",
    "modular_frequency",
    "modular_hamiltonian",
    "page_wootters_state",
    "unruh_temperature",
    # Vacuum information
    "BITS_PER_NAT",
    "PLANCK_LENGTH",
    "apply_local_unitary",
    "bekenstein_bits",
    "desitter_bits",
    "desitter_horizon_radius",
    "holographic_bits",
    "landauer_energy",
    "marginal_probabilities",
    "two_mode_mutual_information",
    "two_mode_squeezing_photon_number",
    # Cache topology
    "CacheStats",
    "hit_rate_curve",
    "merge_gaps",
    "reuse_distances",
    "saturation_capacity",
    "simulate_lru",
    "working_set_candidates",
    "working_set_estimate",
    "working_set_keys",
    "working_set_splits",
    # Latent topology
    "Point",
    "betti_at",
    "distance_matrix",
    "dominant_bar",
    "euclidean",
    "hole_scale",
    "persistence_diagram",
    "rips_persistence",
    # Grid topology
    "Cell",
    "bounded_background_components",
    "disk_cells",
    "grid_hole_depth",
    "grid_hole_scale",
    "hole_is_resolved",
    "lattice_euler_characteristic",
    "lattice_step",
    # Unit group
    "divides",
    "is_field_mod",
    "projective_reciprocal",
    "reciprocal",
    "reciprocal_fixed_points",
    "unit_inverse",
    "units_mod",
    # Step expansion
    "additive_expansion",
    "additive_interval",
    "divide_by_step",
    "expansion_term",
    "hyperfactorial",
    "log_expansion",
    "multiplicative_collapse",
    "multiplicative_expansion",
    "step",
    "tail_bound",
    # Duality
    "DUAL_PAIRS",
    "DualPair",
    "all_poles",
    "dual_of",
    "dual_pair",
    "dual_pairs",
    # Roots
    "nth_root",
    # Equator
    "scale_midpoint",
    "imaginary_rotate",
    "gauge_node",
    # Clock
    "planck_refresh_rate",
    "cp_violation_tilt",
    "entropy_brake",
    # Phenomena
    "PHENOMENA",
    "phenomena_list",
    "phenomenon_type",
    # Plotting
    "plot_cosmic_web",
    "plot_delta",
]

__version__ = "0.2.0"
