# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-10-31

### Added

- `model/__main__.py`: `python -m model` now works.
- `model/phenomena.py`: phenomenon → canvas-operation map, exported publicly.
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
