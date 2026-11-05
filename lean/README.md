# Lean 4 Formalization (verified)

Lean 4.35.0 is installed via elan. This project builds cleanly with `lake build`.

## Build

```bash
cd lean
lake build
```

## Files
- `Model/Ternary.lean` — ternary states, net-zero, theorems.
- `Model/Cusp.lean` — cusp bifurcation value, theorem.
- `Model/DarkEnergy.lean` — CPL w, rho ratio, delta; theorem.
- `Model/Playhead.lean` — index function.
- `Model/Erosion.lean` — erosion placeholder.
- `Model/Antithesis.lean` — involution vs contraction and nilpotent (`N² = 0`).
- `Model.lean` — library root imports.
- `Main.lean` — executable entry point.
