# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-10-31

### Added

- `model/__main__.py`: `python -m model` now works.
- `model/phenomena.py`: phenomenon → canvas-operation map, exported publicly.
- `model/roots.py`: integer roots, including the `-1`-th root / `-1`-th power
  duality (`x^(1/e^(iπ)) = 1/x`).
- `model/mobius.py`: Möbius matrix representation, composition, powers, order,
  and fixed-point solving; `Mobius.inversion()` is `z -> 1/z`.
- `model/duality.py`: explicit dual pairs (UV/IR, exterior/interior,
  compression/expansion, photon/dark energy, entropy/structure, time,
  substrate, information), `dual_of`, `dual_pair`, and `all_poles`.
- `model/antithesis.py`: contractive, translating, and nilpotent counter-models;
  entropy `-log(x)`; invariants (`lyapunov_exponent`, `information_loss`);
  cycle detection (`orbit_period`, `is_cyclic`); and side-by-side
  involution/contraction/translation orbits (`compare_regimes`).
- `model/mobius.py`: `translation()` and `contraction()` constructors and
  `classify()` for periodic, hyperbolic, parabolic, elliptic, and loxodromic
  maps.
- CLI: `python -m model duality` (list, `--pair`, or `--pole`) and
  `python -m model antithesis` (three regimes plus entropy, information loss,
  and Lyapunov exponent; `--nilpotent` adds the `N² = 0` collapse).
- `model/fold.py`: the inversion quotient `q(x) = x + 1/x`, preimage solver,
  fundamental-domain representative, and `compare_fold`. Unlike the
  contraction, `q` is genuinely non-invertible: `q(1/x) = q(x)`.
- `model/antithesis.py`: log-coordinate conjugacy (`log_coordinate`,
  `exp_coordinate`, `log_orbit`, `compare_log_conjugacy`); under `t = log x`
  the contraction becomes translation by `log(rate)`.
- CLI: `python -m model fold --x 2`, and `python -m model antithesis --log`
  for the conjugacy.
- `model/lattice.py`: the Boolean lattice of pole strings over the eight dual
  pairs (256 strings, 128 complement orbits), with join/meet, order,
  complement, atoms, coatoms, canonical representatives, binomial rank
  enumeration (`strings_of_rank`, `rank_counts`), and the folded rank profile
  (`orbit_rank_counts`).
- CLI: `python -m model lattice` (summary) and `--bits 10101010` (one string,
  its dual, canonical representative, join, and meet).
- `lean/Model/Lattice.lean`: Boolean-lattice laws for pole strings, including
  commutativity, associativity, absorption, distributivity, complement, and
  order.
- `model/phase.py`: complex phase, observable intensity, wavelength/wavenumber,
  quarter-turn rotation, and the real/imaginary split.
- `model/superoperator.py`: finite-dimensional commutator/Liouvillian,
  Hilbert–Schmidt self-adjointness, transition frequencies, commutant zero
  modes, trace, the diagonal resolvent with pole validation, the Liouvillian
  resolvent, and truncated oscillator operators that expose the boundary defect
  in the canonical commutator.
- `model/symmetry_breaking.py`: classical double-well potential, stable minima,
  curvature, and a toy vacuum expectation value.
- `model/spacebar.py`: candidate parameters of the press — Compton period,
  action/phase, tick count, unitary press, thermal companion, mass-shell
  residual, and a catalog of every candidate with its status.
- `model/pressing.py`: toy checks for the mutual-press essay — a Page–Wootters
  history state and conditional slices, GPS gravitational/velocity drift and
  factory detune, the de Sitter conformal strip and proper-time divergence, the
  Connes two-point spectral distance, and the qubit modular flow plus Unruh
  temperature.
- `model/fold.py`: `fold_from_log(t) = 2*cosh(t)`, the fold/contraction law,
  and `fold_power(x, n) = fold(x**n)` via Chebyshev fast doubling.
- `IMAGINARY_UNIVERSE.md`: claim-by-claim audit of the attached analysis, with
  the rigorous parts integrated, the derived identities listed, and the
  metaphors quarantined.
- `BECOMING_ONE.md`: audit of the "force of becoming one" passage, correcting
  the finite-dimensional CCR claim and the Higgs-vev overclaim while keeping
  the commutator residue, the double-well instability, the resolvent-pole
  picture, and the truncated-oscillator boundary defect.
- `SPACEBAR.md`: enumeration of the press's candidate parameters, the
  real-phase/unitarity link, the Compton tick count as the scale-free real
  coordinate of the phase, the measured baryon asymmetry, and the rejection of a
  free knob as the finger.
- `PRESSING.md`: thesis-by-thesis audit of the mutual-press essay, keeping the
  Page–Wootters illustration, GPS drift, de Sitter conformal strip, Connes
  distance, and modular/Unruh core, correcting the "bounded commutator" and
  "total phase" readings, and dropping the unverified Rovelli attribution.
- `lean/Model/Antithesis.lean`: formal mirror of the contrast —
  `involution_involutive` (`f² = id`), `contractOrbit_eq` (`gⁿx = rⁿx`),
  `translation_no_fixed`, `nilpotent_sq_zero` (`N² = 0`), `entropy_gain_pos`,
  plus `fold_invariant`, `fold_ge_two`, `fold_not_injective`,
  `log_contraction`, `exp_log_coordinate`, `fold_exp`, `fold_product`,
  `fold_sq`, and `fold_discriminant`.
- `ANTITHESIS.md`: axis table, the Open Dissipative Exterior, the
  group-versus-semigroup contrast, the periodic/hyperbolic/parabolic
  trichotomy, the nilpotent limit, and information loss.
- Property tests for `uv_ir_inversion`: involution, multiplicativity, order
  reversal, self-dual point, and agreement with `nth_root(scale, -1)`.
- Architecture note: UV/IR inversion is an order-2 automorphism, not a flow.
- Tests for phenomena, plotting error paths, neural fallback, EEG bandpass,
  cusp precision, CLI entry points, exports, and the meta-audit itself.
- Governance: `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`,
  issue/PR templates, Dependabot, `.editorconfig`, pre-commit hooks.
- Documentation: `docs/ARCHITECTURE.md`, `docs/README.md`,
  `examples/README.md`.
- Packaging: `py.typed`, classifiers, `docs` extra, bandit/coverage config.
- CI: Python 3.10–3.13 matrix, lint/type/security/docs jobs, coverage gate,
  CLI and example smoke tests.

### Changed

- `portal_journey` now validates its domain and honours the `T` duration;
  `uv_ir_inversion` rejects non-finite input.
- `cusp_roots` uses a cancellation-free Cardano branch; worst-case residual
  dropped from ~1e-7 to ~1e-16.
- `goldbach_check` uses a memoized sieve; `collatz_spine_sum` and
  `zeta_partial` validate their inputs.
- `bandpass_filter` is a real difference-of-moving-averages bandpass and uses
  both `low` and `high`.
- `search_text` compiles regexes once.
- README, module counts, commands, and validation status refreshed.
- Corrected the antithesis wording: the contraction `g(x) = r x` is invertible
  (inverse `x / r`); the genuinely non-invertible opposites are the quotient
  fold and the nilpotent.
- Version bumped to 0.2.0 (Python package and Lean library).

### Fixed

- CI installed neither the package nor its test dependencies.
- `cli validate` depended on the current working directory.
- Duplicate `plot_cosmic_web` definitions (4 copies) and dead `main()` in
  `validate_claims.py`.
- Unreachable cusp and crease-density branches; unimported `pytest` reference;
  `assert False` test anti-patterns.
- Plotting tests opened an interactive backend; `tests/conftest.py` now forces
  Matplotlib's non-interactive Agg backend.
- `examples/erosion_demo.py` now puts the repository root on `sys.path` like
  the other examples.
- Corrupted UTF-16 tail in `.gitignore`; stale `engine` import in the notebook.
- Strict mypy and ruff violations across the package.

### Removed

- Stale generated `docs/engine.html` (it documented the retired `engine.py`).

## [0.1.0]

Initial public snapshot: axioms, Python engine, 66-test suite, Lean 4 core,
calibration memos, and the book text.
