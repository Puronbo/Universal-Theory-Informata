# Universal Theory Informata

> A self-consistent architecture of reality: the Self-Looping Informational Cosmos.

**Version 0.2.0** · Python ≥ 3.10 · MIT licensed · [Changelog](CHANGELOG.md)

## Overview

This repository contains a testable framework with a machine-verified core that
models reality as a **self-generating, self-correcting fluid information
processor**. Instead of searching for a single master particle, the model closes
the loop: a pixelated field grid at the bottom renders a fractal tree of matter
in the middle, and macroscopic gravitational drains pump dark energy back out
from the top to sustain the network.

The epistemic status of each module is explicit — see
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the grounded / candidate /
phenomenological map.

### Core ideas

- **Ternary logic** — states \(\{-1, 0, +1\}\) (balance / void / active) with a net-zero invariant.
- **Dynamic canvas** — dark energy is not constant: \(\rho_\Lambda(t) = \rho_{\Lambda,0} + \delta(t)\), anchored to DESI DR2 (2.8–4.2σ preference for evolving dark energy).
- **Two-halves geometry** — Exterior (objective) / Interior (subjective = consciousness) contact surfaces; spin-\(\tfrac12\) requires \(720^\circ\).
- **Playhead** — Planck-time discrete frames read from a static 4D block universe.
- **Recursion / awakening** — feedback loops close (\(E \equiv I\)): the mirror realizes it is the creator.
- **Erosion** — slow wearing-away of structure preserving net-zero.
- **Rolling-fold duality** — photon (crease) ↔ dark energy (unfolded tension).
- **Stroboscopic sampling** — reality is aliased; each "now" is one blade caught mid-spin.
- **Self-looping matrix** — cosmic pixel → fractal web → UV/IR inversion → cosmological coupling → imaginary plane.
- **Equator of scale** — biology sits at \(10^{-4.5}\,\text{m}\), the hardware midpoint.
- **Clock / broken mirror / entropy brake** — Planck refresh rate, CP-violation tilt, consciousness as entropy reducer.
- **Phenomena map** — light, sound, gravity, matter, erosion, consciousness and the stroboscopic now, each classified by its canvas operation (`model.phenomena`).
- **Dual pairs / antithesis** — explicit poles (UV/IR, exterior/interior, compression/expansion, time, substrate, information), the Boolean lattice of pole strings (`model.lattice`), and an executable counter-model spanning periodic, hyperbolic, parabolic, and nilpotent regimes (`model.duality`, `model.antithesis`), plus the non-invertible quotient fold `x + 1/x` (`model.fold`) and the log-coordinate conjugacy between scaling and translation; a Lean mirror proves `f² = id`, `N² = 0`, and `q(1/x) = q(x)` (`lean/Model/Antithesis.lean`), plus the Boolean-lattice laws (`lean/Model/Lattice.lean`).
- **Imaginary-universe audit** — complex phase and observable intensity (`model.phase`), the Liouvillian commutator and its commutant zero modes (`model.superoperator`), and a claim-by-claim separation of the attached analysis from its metaphors (`IMAGINARY_UNIVERSE.md`).
- **Becoming-one audit** — the commutator residue, the unstable symmetric zero (`model.symmetry_breaking`), the resolvent pole picture, and the truncated-oscillator boundary defect, with the trace obstruction against finite-dimensional canonical commutation and the Higgs-vev overclaim corrected (`BECOMING_ONE.md`).
- **Spacebar parameter** — the press as a unitary phase, proper time as its lift, the Compton period as one full press, the dimensionless tick count as the scale-free coordinate of the phase, and the free knob rejected as the finger (`model.spacebar`, `SPACEBAR.md`).
- **Mutual-press audit** — Page–Wootters conditional evolution, the GPS drift and factory detune, the finite de Sitter conformal strip, the Connes two-point distance, and the modular/Unruh core of thermal time, with the five theses graded and the unverified Rovelli attribution dropped (`model.pressing`, `PRESSING.md`).
- **Vacuum-information audit** — the Bekenstein and holographic bounds, de Sitter horizon capacity, Landauer erasure, two-mode squeezing, and a no-signaling toy, with “nothing” treated as a partition, bound, protection, correlation, and constraint rather than a container (`model.vacuum_info`, `VACUUM_INFO.md`).
- **Zero and holes audit** — zero as reference rather than substance, \(0/0\) as an underdetermined ratio resolved by a choice of direction, numbers as conditioned values, the inward/outward duality and the self-dual zero, and the homology of holes (Alexander duality, Betti numbers, persistence, topological defects) (`ZERO_AND_HOLES.md`).
- **Two topology experiments** — reuse-distance persistence against LRU saturation capacity (negative: the widest gap is a scale, not a sizing rule) and Rips \(H_1\) persistence as a latent-hole OOD diagnostic (partial: it separates a ring from a disk where nearest-neighbour detection misses 32–50% of in-hole probes in this test) (`model.cache_topology`, `model.latent_topology`, `TOPOLOGY_EXPERIMENTS.md`).
- **Puncture resolution test** — the cap/puncture ledger on a finite lattice: a point puncture and a thin annulus have the same Euler characteristic and one bounded background component, while the hole depth separates them; a one-cell puncture has depth one and scales with the sampling, so depth one is the resolution limit (`model.grid_topology`, `PUNCTURE_RESOLUTION.md`).
- **Unit group and the pole** — one divides every integer while only ±1 divide one; the units of \(\mathbb{Z}/n\mathbb{Z}\) are every nonzero residue exactly when \(n\) is prime; the projective reciprocal swaps \(0\) and \(\infty\) and fixes ±1, so \(1/0\) is a compactification boundary, not a value in a field (`model.unit_group`, `ZERO_AND_HOLES.md`).
- **One-step expansion** — repeatedly dividing by the step \(s_n=n/n^n\) gives the hyperfactorial quotient \(H(n)/n!\), whose reciprocal collapses to zero; the additive sum \(\sum_k 1/k^{k-1}\) is enclosed by a proved tail bound and has an exact integral reformulation (`model.step_expansion`, `STEP_EXPANSION.md`).
- **Fold-corpus audit** — the checkable core of the separate Fold paper corpus made executable: the homothety \(g_k(P)=P_0+k(P-P_0)\) and its determinant, the reflection/crease pair, midpoint and division collapse, the cap–puncture ledger, wheel closure, and the exterior solid angle and \(k^*\), with the theta/zeta and calendar notes audited and their rhymes quarantined (`model.fold_corpus`, `FOLD_CORPUS.md`).

### Millennium integration

All seven Clay Millennium Prize Problems are mapped onto the architecture as a
finite, self-looping computational matrix. See `MILLENNIUM_INTEGRATION.md` and
`PRIZED_PROBLEMS.md` (honest audit: no problem is declared settled except
Poincaré, solved by Perelman).

## Repository layout

| Path | Purpose |
|---|---|
| `model/` | Pure-Python engine (45 feature modules, typed, stdlib-only runtime) |
| `tests/` | 992 tests, 98.41% branch-aware coverage |
| `lean/` | Lean 4 machine-checked math core (mathlib4, no `sorry`) |
| `docs/` | [Architecture](docs/ARCHITECTURE.md), generated API reference, long-form text |
| `examples/` | Demo scripts (smoke-tested in CI) |
| `*.md` | Axioms, grounding, connections, antithesis, guides, research memos |

## Quick start

```bash
python -m pip install -e ".[dev,docs]"

python -m pytest tests -q --cov-fail-under=90   # 992 pass, 98.41% coverage
ruff check .                                    # lint: clean
black --check model cli.py tests examples       # format: clean
mypy model cli.py                               # strict types: clean
python -m bandit -c pyproject.toml -r model cli.py validate_claims.py
python validate_claims.py                       # meta-audit: clean
python -m model --help                          # all subcommands
python -m model timeline                        # milestone status
python -m model duality                         # list dual pairs
python -m model duality --pole UV               # opposite pole
python -m model antithesis --x 2 --steps 3      # periodic/hyperbolic/parabolic
python -m model antithesis --nilpotent --y 4    # add N² = 0 collapse
python -m model antithesis --log                # scaling ↔ translation conjugacy
python -m model fold --x 2                      # quotient x + 1/x and preimages
python -m model lattice                         # 256 pole strings, 128 orbits
python -m model validate                        # run the meta-audit via the CLI
python examples/erosion_demo.py                 # demo scripts
python -m pdoc model -o docs/api                # API docs (not committed)
cd lean && lake build                           # Lean core (mathlib4)
```

`python run_all.py` and `python simulate.py` run the full pipeline and
end-to-end demo.

## Verification

- **Python:** 992 tests pass; 98.41% branch-aware coverage (CI gate: 90%).
- **Static checks:** `ruff check`, `black --check`, and strict `mypy` are clean.
- **Security:** `bandit` reports no medium/high findings (simulation-only
  `random` use is documented and skipped in `pyproject.toml`).
- **Lean 4:** clean `lake build`, 0 `sorry`.
- **Meta-audit:** no overclaim phrases; all module references and axiom
  cross-references resolve.
- **CI:** Python 3.10–3.13 matrix plus dedicated quality, smoke-test, docs, and
  Lean jobs.

## Documentation and contributing

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — module map, data flow, epistemic status.
- [`ANTITHESIS.md`](ANTITHESIS.md) — dual pairs, the quotient fold, the pole-string lattice, the Open Dissipative Exterior, and the limits of the opposition.
- [`IMAGINARY_UNIVERSE.md`](IMAGINARY_UNIVERSE.md) — audit of the attached analysis: complex phase, Liouvillian zero modes, and what is deliberately not integrated.
- [`BECOMING_ONE.md`](BECOMING_ONE.md) — the commutator residue, the unstable symmetric zero, the resolvent pole picture, and the corrected overclaims.
- [`SPACEBAR.md`](SPACEBAR.md) — the press as a unitary phase, proper time as its lift, the Compton tick count, and why a free parameter is the finger.
- [`PRESSING.md`](PRESSING.md) — the five-thesis mutual-press audit: what the Page–Wootters, GPS, de Sitter, Connes, and thermal-time claims do and do not establish.
- [`VACUUM_INFO.md`](VACUUM_INFO.md) — what “nothing” can hold: Bekenstein/holographic/de Sitter bounds, Landauer erasure, squeezed-vacuum entanglement, and no-signaling.
- [`ZERO_AND_HOLES.md`](ZERO_AND_HOLES.md) — zero as reference, \(0/0\) as underdetermination, numbers as conditioned values, the inward/outward duality, and the topology of holes.
- [`TOPOLOGY_EXPERIMENTS.md`](TOPOLOGY_EXPERIMENTS.md) — two measured experiments: cache reuse-distance persistence versus LRU capacity, and latent-hole persistence as an OOD diagnostic, with the negative and partial results.
- [`FOLD_CORPUS.md`](FOLD_CORPUS.md) — the exact core of the Fold corpus, the recomputed solid-angle, horizon, theta, and calendar values, and the boundary between exact, reformulation, and rhyme.
- [`PUNCTURE_RESOLUTION.md`](PUNCTURE_RESOLUTION.md) — the cap/puncture ledger on a finite lattice: a point puncture and a thin annulus share their combinatorics, and the hole depth supplies the resolution limit.
- [`STEP_EXPANSION.md`](STEP_EXPANSION.md) — one-step division by \(n/n^n\), the hyperfactorial product, a rigorous additive enclosure, the OEIS decomposition, and the exact/reformulation boundary.
- [`docs/README.md`](docs/README.md) — how to build the API reference.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — setup, required checks, and claim rules.
- [`CHANGELOG.md`](CHANGELOG.md) — release history.
- [`SECURITY.md`](SECURITY.md) — vulnerability reporting.
- [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) — community expectations.

## Epistemic status

Empirical claims (dark energy, spin topology) are quarantined from metaphysical
ones (sync point, vessel identity, awakening). See `GROUNDING.md` and
`THEORY_OF_EVERYTHING.md` §5. Numerical evidence is never presented as proof.

## License

MIT — see [`LICENSE`](LICENSE).

## Author

Michael Grafiel S Puno (conceptual framework) and contributors.
