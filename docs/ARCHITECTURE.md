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
| `duality.py` | Binary poles and the involution that swaps them | **taxonomy** (no physical claim) |
| `lattice.py` | Boolean lattice of pole strings over the dual pairs | **taxonomy** (no physical claim) |
| `fold.py` | Inversion quotient `x + 1/x`, preimages, representative | **toy** (conceptual quotient) |
| `fold_corpus.py` | Homothety, fold/crease, cap–puncture ledger, closure, solid angle | **grounded** (standard geometry and arithmetic; readings quarantined) |
| `antithesis.py` | Contraction, translation, nilpotent, entropy, log conjugacy | **toy** (conceptual counter-model) |
| `phase.py` | Complex phase, observable intensity, wavelength/wavenumber | **grounded** (standard complex arithmetic) |
| `superoperator.py` | Liouvillian, commutant zero modes, resolvent, truncated oscillator | **grounded** (standard linear algebra) |
| `symmetry_breaking.py` | Double-well potential, minima, curvature, toy vev | **toy** (classical mechanism) |
| `spacebar.py` | Candidate parameters of the press: proper time, phase, ticks, mass shell | **grounded** (standard kinematics) |
| `pressing.py` | Page–Wootters toy, GPS drift, de Sitter strip, Connes distance, modular flow | **grounded** (standard definitions) |
| `vacuum_info.py` | Bekenstein/holographic/de Sitter bounds, Landauer cost, squeezing, no-signaling | **grounded** (standard bounds; relational reading is interpretation) |
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

- CLI: `python -m model {darkenergy,recurse,timeline,validate,duality,fold,antithesis,lattice}`
- Library: `from model import iterate, cusp_roots, w_cpl, portal_journey, wave_sample, liouvillian, ...`
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

## Dual pairs and the antithesis

`model.duality` registers the framework's binary poles and provides a single
swap: UV/IR, exterior/interior, compression/expansion, photon/dark energy,
entropy/structure, becoming/block, discrete/continuous, and
reprocessed/erased. By construction `dual_of(dual_of(pole)) == pole`.

`model.antithesis` implements the limit cases in which the return loop is
removed: a dissipative contraction `g(x) = rate * x` (invertible, with the
expansion inverse `x / rate`), a parabolic translation `x + shift`, and the
nilpotent `N(x, y) = (0, x)`. It adds monotone entropy `-log(x)`,
`lyapunov_exponent`, `information_loss`, cycle detection via
`orbit_period`/`is_cyclic`, and `compare_regimes`, which places a periodic
involution, a hyperbolic contraction, and a parabolic translation side by side.
`log_coordinate`/`log_orbit`/`compare_log_conjugacy` show that contraction is
translation in log coordinates.

`model.fold` is the genuinely non-invertible opposite of the involution: the
quotient `q(x) = x + 1/x`, invariant under `x -> 1/x`, two-to-one on positive
scales, with `fold_preimages` and `representative`.
`Mobius.classify()` reports the corresponding Möbius dynamical type. In the
log coordinate the fold is `2*cosh(t)` (`fold_from_log`), and powers become
Chebyshev composition (`fold_power`). The conceptual rationale, axis table,
and limits are in `ANTITHESIS.md`.

`model.lattice` turns the eight dual pairs into a Boolean coordinate: a pole
string chooses one pole from every pair, so there are `2**8 = 256` strings.
Join and meet are bitwise OR and AND; complement is the duality involution; the
fold identifies each string with its complement, giving 128 orbits. The rank
counts are binomial (`1, 8, 28, 56, 70, 56, 28, 8, 1`), the folded rank
profile is `(1, 8, 28, 56, 35)`, and `strings_of_rank`/`rank_counts`/
`orbit_rank_counts` expose them. This is a taxonomy of the registered pairs,
not a physical claim.

`model.phase` makes the hidden/visible contrast explicit with standard complex
arithmetic: a complex amplitude has an intensity `|psi|**2`, a phase angle, and
real/imaginary coordinates. `model.superoperator` implements the finite-
dimensional Liouvillian `L_H(A) = [H, A]`; its zero modes are the commutant of
`H`, and its eigenvalues are the transition frequencies. The resolvent
`(zI-H)**-1` has poles exactly at the eigenvalues, and
`liouvillian_resolvent` applies the same statement to transition frequencies.
The truncated oscillator shows the finite-dimensional near-miss:
`[a, a^dagger] = I - N|N-1><N-1|`. Both are tooling, not physical claims. The
source audit, the derived identities, and the list of rejected metaphors are in
`IMAGINARY_UNIVERSE.md`.

`model.symmetry_breaking` is a classical double-well toy model: the symmetric
point is unstable and the minima give a nonzero order parameter. It does not
derive the Higgs value. The passage audit, including the trace obstruction
against finite-dimensional canonical commutation, is in `BECOMING_ONE.md`.

`model.spacebar` makes the argument of the "press" explicit. A real phase is
unitary; the Compton period is one full press; the dimensionless tick count
`tau/T_C` is the scale-free coordinate of the phase. A dimensionful proper
time needs a mass to fix the phase, and the affine parameter is pure gauge.
The candidate catalog and the rejection of a free knob are in `SPACEBAR.md`.

`model.pressing` encodes the checkable residue of the five-thesis essay: a
Page–Wootters history state and its conditional slices, the GPS gravitational
and velocity clock drifts with the factory detune, the finite conformal strip
of closed-slicing de Sitter, the Connes two-point spectral distance with the
`‖[D,f]‖ <= 1` constraint, and the modular flow of a qubit Gibbs state with
the Unruh temperature. It does not establish the essay's metaphysics. The
thesis-by-thesis grades, including the finite-conformal-time analogy and the
dropped Rovelli attribution, are in `PRESSING.md`.

`model.vacuum_info` makes the information content of "nothing" explicit. A
literal void has one state and zero bits; a vacuum, horizon, code, or constraint
has correlations. The module implements the Bekenstein bit bound, the
holographic area bound, the de Sitter radius and capacity, the Landauer erasure
cost, the mean photon number and mutual information of a two-mode squeezed
vacuum, and a bipartite no-signaling toy (`apply_local_unitary`,
`marginal_probabilities`). The bounds describe capacity and protection, not the
creation of information or an origin story. The six jobs and the caveats are in
`VACUUM_INFO.md`.

`ZERO_AND_HOLES.md` is a documentation-only audit with no engine module. It
separates the standard mathematics (zero as identity and reference, \(0/0\) as
an underdetermined ratio resolved by limits, blow-up, conditioning, or wheel
algebra, numbers as conditioned values via currying, the duality of a category
with its opposite, Alexander duality, Betti numbers, persistent homology, and
the homotopy classification of defects) from the interpretative readings (zero
as coordinate rather than ground, the inward road ending at the empty set as a
base case rather than an author, redemption as making a cycle bound). It states
no physical prediction and is not an axiom set.

`model.cache_topology` tests the first architectural proposal from that audit.
It computes LRU stack distances, the 0-dimensional persistence of the distance
profile, two working-set estimates plus the tied-gap splits, an LRU
simulation, and the capacity at which the hit rate saturates. The measurement result is negative: the widest
gap in the distance profile does not predict the 90% capacity accurately
(errors reach \(3.5\times\)), and on the line 0-dimensional persistence is only
the sorted gap list. The numbers are in `TOPOLOGY_EXPERIMENTS.md`.

`model.latent_topology` tests the second proposal. It computes exact
\(\mathbb{Z}_2\) Rips persistence in dimensions 0 and 1 by reducing the boundary
matrix of the truncated complex, with Betti numbers, a dominant-bar selector,
and a hole scale. On synthetic clouds a ring and a disk separate by dominant
\(H_1\) persistence, and a nearest-neighbour rule misses points inside the
hole in this thin-ring test. The implementation enumerates a complex whose
triangle count grows cubically, so it is limited to small clouds. The measured
tables and the truncation caveat are in `TOPOLOGY_EXPERIMENTS.md`.

`model.grid_topology` tests whether the Fold corpus's cap/puncture ledger
survives discretization. On a square lattice, a one-cell puncture and a thin
annulus have the same Euler characteristic (zero) and one bounded background
component each. The difference is metric: a punctured disk has a hole of depth
one, so its physical scale is the lattice step and vanishes under refinement,
while a fixed annulus keeps its scale. At coarse resolution the two masks can
be the same cell set, so the puncture is the refinement limit of a small hole,
not a lattice object. The tables and the exact/rhyme boundary are in
`PUNCTURE_RESOLUTION.md`.

`model.unit_group` builds the exact algebra behind the "one is everything"
reading. In the integers one divides every integer while only ±1 divide one; in
a field every nonzero element is a unit. The unit group of
\(\mathbb{Z}/n\mathbb{Z}\) is every nonzero residue exactly when \(n\) is prime.
The projective reciprocal extends \(x\mapsto1/x\) by \(0\leftrightarrow\infty\)
and has fixed points ±1, so \(1/0\) is a choice of compactification rather than
a value in a field. See `ZERO_AND_HOLES.md` for the exact/rhyme boundary.

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

Coverage is branch-aware and gated at 90% in CI (currently ~98%). Numerical
claims in tests use explicit tolerances; see `tests/test_cusp.py` for the
near-double-root case.

## Formalization boundary

The Lean tree (`lean/Model`) mirrors selected algebraic facts: ternary net-zero,
the cusp bifurcation value, CPL relations, playhead indexing, rolling-fold
identities, and the antithesis contrast (`involution_involutive`,
`contractOrbit_eq`, `translation_no_fixed`, `nilpotent_sq_zero`,
`entropy_gain_pos`, `fold_invariant`, `fold_ge_two`, `fold_not_injective`,
`log_contraction`, `exp_log_coordinate`, plus the Boolean-lattice laws in
`Model.Lattice`). It contains no `sorry`, but it does **not** formalize the
physical interpretation. `lake build` is part of CI.

## Known limitations

- The physics modules are models, not measurements; only `dark_energy.py` and
  the Hertz part of `rubber_ball.py` are calibrated to external data.
- `eeg_stream.py` is a schematic, not a validated signal-processing pipeline.
- `neural_phase.py` is a toy Kuramoto simulation with a pure-Python fallback.
- `recursion_families.py` is explicitly toy mathematics.
- `antithesis.py`/`ANTITHESIS.md` are a conceptual counter-model, not a physical
  alternative or a refutation.
- `phase.py` and `superoperator.py` are standard complex/linear algebra used as
  tooling; they do not turn the source document into a physical theory.
- `symmetry_breaking.py` is a classical toy double well; it does not derive the
  Higgs vev.
- `spacebar.py` is formal bookkeeping for the operator's argument; the
  baryon-asymmetry ratio is measured, not derived.
- `pressing.py` checks arithmetic and definitions from the mutual-press essay;
  Page–Wootters conditional evolution, GPS drift, the de Sitter conformal strip,
  the Connes distance, and modular flow do not establish "no key," "all
  pressing is mutual," or a bounded "total phase."
- `vacuum_info.py` states standard capacity bounds; it does not show that the
  vacuum stores a message, that horizon entropy is readable, or that the bounds
  explain the origin.
- `cache_topology.py` shows that a persistence threshold on reuse distances is
  a coarse scale, not a cache-sizing rule; it does not compare against ARC or
  production traces.
- `latent_topology.py` is exact but enumerates a cubically growing complex; the
  OOD threshold is fitted to the reported samples and is not a calibrated score.
- `grid_topology.py` treats a depth-one hole as unresolved; a two-by-two hole is
  real but has depth one, so the criterion is a small-hole detector, not an
  exact classifier.
- `IMAGINARY_UNIVERSE.md`, `BECOMING_ONE.md`, `SPACEBAR.md`, `PRESSING.md`,
  `VACUUM_INFO.md`, `ZERO_AND_HOLES.md`, and `TOPOLOGY_EXPERIMENTS.md` record
  which source claims are rejected or left as metaphor; they are not axiom sets.
- The meta-audit catches listed phrases, not every possible overclaim; prose
  review is still required.

## Adding a module

1. Create `model/<topic>.py` with a module docstring and a status label.
2. Add full type hints and input validation.
3. Export the public names from `model/__init__.py` and its `__all__`.
4. Add `tests/test_<topic>.py` covering success and failure paths.
5. Add a row to the table above and an entry to `CHANGELOG.md`.
6. Run the checks listed in `CONTRIBUTING.md`.
