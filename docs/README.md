# Documentation

| File | Purpose |
|---|---|
| `ARCHITECTURE.md` | Module map, data flow, epistemic status, testing strategy |
| `../ANTITHESIS.md` | Dual pairs, the pole-string lattice, and the Open Dissipative Exterior counter-model |
| `../IMAGINARY_UNIVERSE.md` | Audit of the attached analysis and the integrated phase/Liouvillian tooling |
| `../BECOMING_ONE.md` | Audit of the "becoming one" passage: commutator residue, double-well instability, and resolvent poles |
| `../SPACEBAR.md` | Candidate parameters of the press: proper time, phase, ticks, mass shell, and the rejected free knob |
| `../PRESSING.md` | Five-thesis mutual-press audit: Page–Wootters, GPS, de Sitter, Connes, and thermal time |
| `../VACUUM_INFO.md` | What “nothing” can hold: information bounds, erasure cost, squeezed-vacuum entanglement, and no-signaling |
| `../ZERO_AND_HOLES.md` | Zero as reference, \(0/0\) as underdetermination, conditioned values, the inward/outward duality, and the topology of holes |
| `../TOPOLOGY_EXPERIMENTS.md` | Two measured experiments: cache reuse-distance persistence versus LRU capacity, and latent-hole persistence as an OOD diagnostic |
| `../PUNCTURE_RESOLUTION.md` | The cap/puncture ledger on a finite lattice: Euler characteristic, hole depth, and the resolution limit |
| `../STEP_EXPANSION.md` | One-step division by \(n/n^n\), the hyperfactorial product, a rigorous additive enclosure, the OEIS decomposition, and the exact/reformulation boundary |
| `../PI_INTERSECTION.md` | Archimedes' nested rational intervals, rigorous square-root bounds, and \(\pi\) as the intersection \(\{\pi\}\) |
| `../FOLD_CORPUS.md` | The exact core of the Fold corpus, the independent numerical audit, and the exact/reformulation/rhyme boundary |
| `the_book_of_puno.md` | Long-form conceptual text |
| `api/` | Generated API reference (not committed) |

## Build API docs

```bash
python -m pip install -e ".[docs]"
python -m pdoc model -o docs/api
```

Open `docs/api/model.html` in a browser. CI builds the docs on every push to
catch broken docstrings/imports.

The old `engine.html` was removed: it documented `engine.py`, which no longer
exists after the package split.
