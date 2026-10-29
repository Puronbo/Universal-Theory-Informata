# Universal Theory Informata

> A rigorous, self-consistent Theory of Everything: the Self-Looping Informational Cosmos.

## Overview

This repository contains a complete, testable, machine-verified framework that redefines
reality as a **self-generating, self-correcting fluid information processor**. Instead of
searching for a single master particle, the model closes the loop: a pixelated field grid
at the bottom renders a fractal tree of matter in the middle, and macroscopic
gravitational drains pump dark energy back out from the top to sustain the network
eternally.

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

### Millennium integration

All seven Clay Millennium Prize Problems are mapped onto the architecture as a
finite, self-looping computational matrix. See `MILLENNIUM_INTEGRATION.md` and
`PRIZED_PROBLEMS.md` (honest audit: no problem is declared settled except
Poincaré, solved by Perelman).

## Repository layout

| Path | Purpose |
|---|---|
| `model/` | Pure-Python engine (24 modules) |
| `tests/` | 98 tests (all pass) |
| `lean/` | Lean 4 machine-checked math core (mathlib integrated) |
| `docs/` | API reference (pydoc) |
| `examples/` | Demo scripts |
| `*.md` | Axioms, grounding, connections, guides, research memos |

## Quick start

```bash
pip install -e .
python -m pytest tests/ -q          # 98/98 pass
cd lean && lake build               # clean (18,108 jobs)
python validate_claims.py           # meta-audit: clean
python run_all.py                   # run everything
python cli.py timeline              # milestone status
python simulate.py                  # end-to-end demo
```

## Verification

- **Python:** 98/98 tests pass.
- **Lean 4:** clean build (18,108 jobs, mathlib4 integrated).
- **Meta-audit:** no overclaim phrases; all engine references valid.

## Epistemic status

Empirical claims (dark energy, spin topology) are quarantined from metaphysical
ones (sync point, vessel identity, awakening). See `GROUNDING.md` and
`THEORY_OF_EVERYTHING.md` §5.

## License

MIT

## Author

Michael Grafiel S Puno (conceptual framework) and contributors.
