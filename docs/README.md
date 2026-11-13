# Documentation

| File | Purpose |
|---|---|
| `ARCHITECTURE.md` | Module map, data flow, epistemic status, testing strategy |
| `../ANTITHESIS.md` | Dual pairs, the pole-string lattice, and the Open Dissipative Exterior counter-model |
| `../IMAGINARY_UNIVERSE.md` | Audit of the attached analysis and the integrated phase/Liouvillian tooling |
| `../BECOMING_ONE.md` | Audit of the "becoming one" passage: commutator residue, double-well instability, and resolvent poles |
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
