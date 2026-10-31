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

### Millennium integration

All seven Clay Millennium Prize Problems are mapped onto the architecture as a
finite, self-looping computational matrix. See `MILLENNIUM_INTEGRATION.md` and
`PRIZED_PROBLEMS.md` (honest audit: no problem is declared settled except
Poincaré, solved by Perelman).

## Repository layout

| Path | Purpose |
|---|---|
| `model/` | Pure-Python engine (29 feature modules, typed, stdlib-only runtime) |
| `tests/` | 227 tests, 96% branch-aware coverage |
| `lean/` | Lean 4 machine-checked math core (mathlib4, no `sorry`) |
| `docs/` | [Architecture](docs/ARCHITECTURE.md), generated API reference, long-form text |
| `examples/` | Demo scripts (smoke-tested in CI) |
| `*.md` | Axioms, grounding, connections, guides, research memos |

## Quick start

```bash
python -m pip install -e ".[dev,docs]"

python -m pytest tests -q --cov-fail-under=90   # 227 pass, 96% coverage
ruff check .                                    # lint: clean
black --check model cli.py tests examples       # format: clean
mypy model cli.py                               # strict types: clean
python -m bandit -c pyproject.toml -r model cli.py validate_claims.py
python validate_claims.py                       # meta-audit: clean
python -m model --help                          # all subcommands
python -m model timeline                        # milestone status
python -m model validate                        # run the meta-audit via the CLI
python examples/erosion_demo.py                 # demo scripts
python -m pdoc model -o docs/api                # API docs (not committed)
cd lean && lake build                           # Lean core (mathlib4)
```

`python run_all.py` and `python simulate.py` run the full pipeline and
end-to-end demo.

## Verification

- **Python:** 227 tests pass; 96% branch-aware coverage (CI gate: 90%).
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
