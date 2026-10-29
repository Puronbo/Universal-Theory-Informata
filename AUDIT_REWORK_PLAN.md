# Comprehensive Audit & Rework Plan

## Project Overview
This is a "rigorous alternative architecture of reality" model with:
- **engine.py**: Core computational engine (689 lines, monolithic)
- **game_engine.py**: Simple simulation built on engine
- **cli.py**: CLI entry point
- **simulate.py**: End-to-end demo
- **tests.py**: 66 tests (all passing)
- **validate_claims.py**: Meta-audit script
- **lean/**: Lean 4 formalization skeletons (unchecked)
- **docs/**: Markdown documentation

---

## Critical Issues (Must Fix)

### 1. Monolithic engine.py (689 lines, 20 sections)
**Problem**: Single file mixes ternary logic, recursion, cusp catastrophe, dark energy, playhead, timeline, impedance, geometry, stroboscopic, search, prized problems, recursion families, plotting, consciousness, multi-agent, self-looping matrix, equator of scale, clock/mirror/entropy.

**Fix**: Split into a proper package structure:
```
model/
├── __init__.py          # Public API exports
├── ternary.py           # Ternary logic (A0.2, A0.3)
├── recursion.py         # Fixed-point iteration, purge (A5.1, A1.5)
├── cusp.py              # Cusp catastrophe (candidate formalization)
├── dark_energy.py       # CPL, DESI anchoring (A2.2)
├── rolling_fold.py      # Rolling-fold duality (A2.5)
├── playhead.py          # Playhead sampling (A4.1, A4.3, A4.4)
├── timeline.py          # 26-year milestone (A6.1, A6.3)
├── impedance.py         # Universal impedance & mass gap (L.O.R.E.)
├── geometry.py          # Stretched points (A3.6)
├── stroboscopic.py      # Stroboscopic sampling (A4.6)
├── search.py            # Search utility (meta-audit)
├── prized_problems.py   # Collatz, Goldbach, Zeta (evidence only)
├── recursion_families.py # Mandelbrot/Kené (R4)
├── consciousness.py     # Attention, closure (phenomenological)
├── multi_agent.py       # Multi-agent simulation (phenomenological)
├── self_looping.py      # Cosmological coupling, UV/IR (A8)
├── equator.py           # Equator of Scale (A9)
├── clock.py             # Clock, broken mirror, entropy brake (A10)
└── plotting.py          # Optional matplotlib visualization
```

### 2. No Proper Package Configuration
**Problem**: pyproject.toml uses `py-modules` (flat) instead of package structure. No `[tool.setuptools.packages.find]`.

### 3. No Linting/Formatting/Type Checking
**Problem**: No ruff, black, mypy configuration. Inconsistent style.

### 4. Test Organization
**Problem**: All 66 tests in single `tests.py`. Should be split into test modules matching the package structure, run with pytest.

---

## High Priority Issues

### 5. Type Safety Gaps
- Many functions lack type hints
- `iterate` returns 4-tuple but documented as backward-compatible with 3-tuple (breaking change)
- `cusp_roots` returns `List[complex]` but could be `Tuple[complex, complex, complex]`
- `search_text` uses `_re` and `_Path` - unconventional aliasing

### 6. Potential Bugs / Edge Cases

| Function | Issue | Severity |
|----------|-------|----------|
| `cusp_roots` | Division by zero when `p=0` in casus irreducibilis | Medium |
| `portal_journey` | Returns `float("inf")` for scale at inversion | Medium |
| `uv_ir_inversion` | No handling of extreme values (1e-35, 1e26) | Low |
| `goldbach_check` | O(n log log n) sieve per call; no caching | Low |
| `ternary_compose` | Empty list returns 0.0, but `sum([])/len([])` would be division by zero (handled) | - |

### 7. Inconsistent Return Types
- `iterate`: Returns `(x, steps, converged, cycle_length)` - 4 values
- `mandelbrot_escape`: Returns `(escaped, n)` - 2 values
- `check_predictions`: Returns `dict` with string keys
- `portal_journey`: Returns `dict` with mixed types

### 8. Magic Numbers
Many functions have hardcoded thresholds:
- `ternarize`: ±1/3 thresholds (heuristic, not derived)
- `crease_density_proxy`: eps=0.05 default
- `purge_if_flat` / `purge_derivative`: eps=1e-9 default
- `attention_trace`: threshold=0.5 default
- `strobe`: rate validation but no max

---

## Medium Priority Issues

### 9. Documentation
- Many functions have minimal docstrings
- No API documentation generation (sphinx/pdoc)
- Module-level docstrings missing in some areas

### 10. Performance Optimizations
- `collatz_spine_sum`, `zeta_partial` could use `@lru_cache`
- `goldbach_check` recomputes sieve every call
- `search_text` reads entire files - could use `mmap` for large files

### 11. Separation of Concerns
- "Grounded/validated" code mixed with "toy/speculative" code
- No clear marking of validation status in code
- Consciousness/multi-agent code is explicitly "phenomenological" but mixed with physics

### 12. CLI Improvements
- Only 3 subcommands (darkenergy, recurse, timeline)
- No `--help` examples
- No output formatting options (json, yaml, table)

---

## Low Priority / Nice to Have

### 13. Lean 4 Formalization
- All Lean files are skeletons with `sorry` or minimal proofs
- Should be fleshed out to match engine.py functionality

### 14. Examples
- `demo.ipynb` exists but minimal
- Could add Jupyter notebooks for each major module

### 15. CI/CD
- No GitHub Actions for testing, linting, type checking

---

## Recommended Implementation Order

### Phase 1: Foundation (Week 1)
1. Restructure into package with proper `pyproject.toml`
2. Add ruff, black, mypy configuration
3. Split `engine.py` into modules
4. Update imports in all files

### Phase 2: Testing & Quality (Week 1-2)
1. Split `tests.py` into `tests/` directory matching package structure
2. Add pytest configuration with coverage
3. Fix type hints across codebase
4. Add pre-commit hooks

### Phase 3: Bug Fixes & Polish (Week 2)
1. Fix edge cases in `cusp_roots`, `portal_journey`
2. Standardize return types (use NamedTuple or dataclasses)
3. Replace magic numbers with named constants
4. Improve docstrings

### Phase 4: Documentation & Lean (Week 2-3)
1. Add sphinx/pdoc configuration
2. Flesh out Lean 4 formalizations
3. Add example notebooks

### Phase 5: CI/CD (Week 3)
1. GitHub Actions for test, lint, typecheck
2. Automated release workflow

---

## Risk Assessment

| Change | Risk | Mitigation |
|--------|------|------------|
| Package restructure | High - breaks all imports | Do in single commit, run full test suite |
| Module split | Medium - internal refactor | Keep public API in `__init__.py` |
| Type hints | Low - additive | Use `typing.TYPE_CHECKING` for circular deps |
| Test restructure | Low - additive | Keep old tests.py until new ones pass |

---

## Validation Criteria

After rework:
- [ ] All 66 tests still pass
- [ ] `python -m model` CLI works
- [ ] `python simulate.py` works
- [ ] `python validate_claims.py` works
- [ ] `python game_engine.py` works
- [ ] `mypy model/` passes (strict mode)
- [ ] `ruff check model/` passes
- [ ] `black --check model/` passes
- [ ] Test coverage ≥ 90%
- [ ] Lean 4 files at least parse (`lake build`)