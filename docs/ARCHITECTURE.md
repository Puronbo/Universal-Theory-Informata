# Architecture

This document is the map of the `model` package: what each module does, how the
pieces depend on each other, and how much confidence to place in each part.

## Design rules

1. **One topic per module.** Public names are re-exported from
   `model/__init__.py`; everything else is private.
2. **No hidden I/O at import time.** Plotting, NumPy, and Matplotlib are
   optional; importing `model` never requires them.
3. **Fail loudly.** Domain errors raise `ValueError`; no silent clamping.
4. **Label the epistemic status.** Every module is `grounded`, `candidate`, or
   `phenomenological` (table below). The label governs how prose may describe it.
5. **The audit is executable.** `validate_claims.py` and `tests/test_audit.py`
   enforce link integrity and forbid a list of overclaim phrases.

## Data flow

```text
ternary ──► recursion/erosion ──► playhead ──► timeline
   │                │                 │
   │                └──► cusp ◄───────┘
   │                        │
   └──► geometry/hyperbolic │
            │               ▼
            └──────────► dark_energy ◄── rolling_fold
                                │
                                ▼
                         self_looping ◄── equator / clock
                                │
                                ▼
                         phenomena (map)
```

`model/__init__.py` is a flat public facade. Modules do not import each other in
cycles; the only optional third-party imports are NumPy in `neural_phase` and
Matplotlib in `plotting` (lazy, inside functions).

## Module map and status

| Module | Responsibility | Status |
|---|---|---|
| `ternary.py` | Three-state grammar, net-zero invariant, threshold mapping | **grounded** (pure algebra) |
| `recursion.py` | Fixed-point iteration, purge, erosion, canvas energy | **candidate** (math is tested; interpretation is not) |
| `cusp.py` | Cusp-catastrophe roots, bifurcation curve, crease density | **candidate** |
| `geometry.py` | Stretched-point distances | **candidate** |
| `hyperbolic.py` | Poincaré disk distance and novelty | **grounded** (standard geometry) |
| `dimensions.py` | Circle-of-dimensions phases and bleed | **candidate** |
| `impedance.py` | Resonance / mass-gap sector (L.O.R.E.) | **candidate** |
| `mp_operator.py` | αD + βV fold/unfold operator | **candidate** |
| `millennium.py` | Millennium-problem integration helpers | **conceptual** (only Poincaré is settled, by Perelman) |
| `dark_energy.py` | CPL `w(a)`, ρ ratio, DESI-anchored deltas | **calibrated** (not a proof) |
| `rolling_fold.py` | Photon ↔ dark-energy fold duality | **candidate** |
| `playhead.py` | Planck-time frame sampling | **phenomenological** |
| `stroboscopic.py` | Aliased sampling | **phenomenological** |
| `timeline.py` | 26-year milestone, logistic map | **phenomenological** |
| `self_looping.py` | Cosmological coupling, UV/IR inversion, portal trajectory | **candidate** |
| `roots.py` | Integer roots, negative roots, root/power duality | **grounded** (pure algebra) |
| `mobius.py` | Möbius matrices, composition, powers, fixed points | **grounded** (standard geometry) |
| `equator.py` | Equator of scale | **candidate** |
| `clock.py` | Planck refresh, CP tilt, entropy brake | **phenomenological** |
| `consciousness.py` | Attention / closure analogues | **phenomenological** |
| `multi_agent.py` | Multi-agent closure simulation | **phenomenological** |
| `neural_phase.py` | Kuramoto phase locking (NumPy optional) | **phenomenological** |
| `eeg_stream.py` | Bandpass, DFT, channel coherence | **schematic** (consumer-EEG toy, not clinical) |
| `rubber_ball.py` | Hertz contact, thermal speed, Mie placeholder | **calibrated** (Hertz; Mie is a placeholder) |
| `recursion_families.py` | Mandelbrot/Julia/Kené toys, RG flow toys | **toy** |
| `prized_problems.py` | Collatz/Goldbach/ζ numerical evidence | **evidence only** (never proofs) |
| `phenomena.py` | Phenomenon → canvas-operation table | **taxonomy** (no physical claim) |
| `search.py` | Repository text search | **tooling** |
| `plotting.py` | Optional Matplotlib plots | **tooling** |

## Public API

`model.__all__` is the contract. `tests/test_exports.py` checks that every name
is unique and resolves. Add new public functions to both the import block and
`__all__` in `model/__init__.py`.

Stable entry points:

- CLI: `python -m model {darkenergy,recurse,timeline,validate}`
- Library: `from model import iterate, cusp_roots, w_cpl, portal_journey, ...`
- Audit: `python validate_claims.py [--generate-crossref]`

## UV/IR inversion as an order-2 automorphism

`uv_ir_inversion(scale)` is the reciprocal map \(f(s)=1/s\) on positive
scales. It is the \(-1\)-th root, because \(1/e^{i\pi}=-1\):

\[
f(s)=s^{1/e^{i\pi}}=s^{-1}.
\]

Mathematically it is:

- an involution: \(f(f(s))=s\);
- a multiplicative automorphism: \(f(st)=f(s)f(t)\);
- order-reversing on positives: \(s<t \Rightarrow f(s)>f(t)\);
- represented on the Riemann sphere by the Möbius matrix
  \(\begin{pmatrix}0&1\\1&0\end{pmatrix}\), with fixed points \(s=\pm1\)
  (the positive self-dual scale is \(s=1\)).

`tests/test_self_looping.py` enforces the first three invariants;
`model.mobius` exposes the matrix form, composition, powers, and fixed-point
solver; `model.roots` shows that the \(-1\)-th root is simultaneously the
\(-1\)-th power.

Because \(f^2=\mathrm{id}\) and \(f\) reverses order on \(\mathbb{R}_{>0}\),
the UV/IR flip is a **discrete order-2 symmetry**, not the time-1 map of a
continuous flow. The model should not be read as claiming a continuous UV/IR
evolution. This is an algebraic property of the map, not evidence for the
physical T-duality interpretation.

## Dependencies

- Runtime: Python ≥ 3.10 standard library only.
- Optional: NumPy (faster Kuramoto path), Matplotlib (plotting).
- Development: pytest, pytest-cov, ruff, black, mypy, bandit, pre-commit.
- Docs: pdoc.
- Formalization: Lean 4 + mathlib (independent build under `lean/`).

## Testing strategy

`tests/` mirrors the module layout. Four layers:

1. **Unit/contract tests** for every public function, including error paths.
2. **Regression tests** for audit findings (cusp cancellation, portal domain,
   CLI working-directory independence, duplicate plots).
3. **Invariant tests** (net-zero preservation, zero-coherence constant signals,
   export resolution, axiom links).
4. **Meta-audit tests** that run `validate_claims.py` in-process so docs cannot
   drift silently.

Coverage is branch-aware and gated at 90% in CI (currently ~96%). Numerical
claims in tests use explicit tolerances; see `tests/test_cusp.py` for the
near-double-root case.

## Formalization boundary

The Lean tree (`lean/Model`) mirrors selected algebraic facts: ternary net-zero,
the cusp bifurcation value, CPL relations, playhead indexing, and rolling-fold
identities. It contains no `sorry`, but it does **not** formalize the physical
interpretation. `lake build` is part of CI.

## Known limitations

- The physics modules are models, not measurements; only `dark_energy.py` and
  the Hertz part of `rubber_ball.py` are calibrated to external data.
- `eeg_stream.py` is a schematic, not a validated signal-processing pipeline.
- `neural_phase.py` is a toy Kuramoto simulation with a pure-Python fallback.
- `recursion_families.py` is explicitly toy mathematics.
- The meta-audit catches listed phrases, not every possible overclaim; prose
  review is still required.

## Adding a module

1. Create `model/<topic>.py` with a module docstring and a status label.
2. Add full type hints and input validation.
3. Export the public names from `model/__init__.py` and its `__all__`.
4. Add `tests/test_<topic>.py` covering success and failure paths.
5. Add a row to the table above and an entry to `CHANGELOG.md`.
6. Run the checks listed in `CONTRIBUTING.md`.
