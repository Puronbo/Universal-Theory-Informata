# INDEX — Complete File Inventory

## Documentation
- `AXIOMS.md` — numbered axiom set (A0–A14) + dependency map + open questions
- `GROUNDING.md` — empirical anchors (DESI/Euclid dark energy)
- `FOLDING_CALIBRATION.md` — Folding Calculus "dark side" lessons
- `LORE_CALIBRATION.md` — L.O.R.E. 0/0 singularity calibration
- `PUNO_BOOK_CALIBRATION.md` — Book of Puno fold philosophy
- `CONNECTIONS.md` — model ↔ governing laws of nature
- `HORIZON_FINDINGS.md` — cosmic horizons + acceleration controversy
- `STROBOSCOPIC.md` — stroboscopic principle across domains
- `PRIZED_PROBLEMS.md` — honest audit of Millennium problems
- `MILLENNIUM_INTEGRATION.md` — seven prized problems as finite loop
- `RESEARCH_ROADMAP.md` — 12 prioritized research items
- `SELF_LOOPING_MATRIX.md` — cosmic pixel → imaginary realm
- `ASYMPTOTIC_SAFETY.md` — asymptotic-safety candidate
- `KENÉ_RECURSION.md` — Kené recursion candidate
- `CONSCIOUSNESS_ALIAS.md` — consciousness as stroboscopic alias
- `COMPLETED_COSMOS.md` — self-generating fluid machine
- `THEORY_OF_EVERYTHING.md` — definitive ToE statement
- `GUIDE.md` — complete guide
- `GLOSSARY.md` — formal definitions
- `CROSSREF.md` — axiom cross-reference index
- `README.md` — project overview

## Code
- `model/` — 24 Python modules (engine)
- `tests/` — 24 test files (103 tests)
- `lean/` — Lean 4 math core (14 modules, mathlib)
- `cli.py` — CLI entry point
- `simulate.py` — end-to-end demo
- `game_engine.py` — game-engine-style simulation
- `run_all.py` — one-command verification
- `validate_claims.py` — honest-audit meta-check
- `examples/` — demo scripts
- `docs/` — API reference (pydoc)

## Verification
- `python -m pytest tests/ -q` → 103/103 pass
- `cd lean && lake build` → clean (18,110 jobs)
- `python validate_claims.py` → clean
- `python run_all.py` → PASS
