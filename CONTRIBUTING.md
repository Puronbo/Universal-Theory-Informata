# Contributing

Thanks for helping improve the model. This project mixes executable code with
explicitly labelled speculative material, so changes must stay honest about
what is implemented, what is conjectural, and what is merely a demo.

## Setup

```bash
python -m pip install -e ".[dev,docs]"
pre-commit install              # optional, runs ruff/black/mypy on commit
```

Python 3.10+ is required. Lean 4 is only needed for `lean/` changes.

## Checks (must pass before a PR)

| Command | What it enforces |
|---|---|
| `python -m pytest tests -q --cov-fail-under=90` | tests + 90% coverage gate |
| `ruff check .` | lint and import order |
| `black --check model cli.py validate_claims.py tests` | formatting |
| `mypy model cli.py` | strict typing |
| `python -m bandit -c pyproject.toml -r model cli.py validate_claims.py` | security scan |
| `python validate_claims.py` | overclaim and cross-reference audit |
| `cd lean && lake build` | Lean formalization |

CI runs the same commands on Python 3.10–3.13, plus a pdoc build and example
smoke tests.

## Adding code

- Keep modules focused; put new physics in a new `model/<topic>.py` and export
  the public surface from `model/__init__.py`.
- Every public function needs a docstring, full type hints, and a test.
- Return types should be concrete (`tuple`, `TypedDict`, dataclass) rather than
  bare `dict` when practical.
- Validate domains explicitly (`ValueError` for out-of-range or non-finite
  input). Silent garbage is worse than a loud failure.
- Name magic numbers as module constants and say whether they are derived,
  calibrated, or heuristic.
- Mark speculative code in the docstring: `grounded`, `candidate`, or
  `phenomenological`. See `docs/ARCHITECTURE.md` for the current map.

## Tests

- Put tests in `tests/test_<module>.py`; prefer exact values or tight tolerances.
- Cover error paths and boundary conditions, not just the happy path.
- Do not use `assert False`; use `pytest.raises`.
- Add a regression test with every bug fix.
- Numerical regressions should record the failing input and the old/new error.

## Documentation

- `README.md` is the entry point; keep counts and commands current.
- `docs/ARCHITECTURE.md` explains the module map and validation status.
- `CHANGELOG.md` gets an entry for user-visible changes.
- API docs are generated, never hand-edited:

  ```bash
  python -m pdoc model -o docs/api
  ```

## Lean

- No `sorry` is allowed in `lean/Model`.
- Prefer small, checkable lemmas that mirror Python functions by name.
- Run `lake build` from `lean/` before opening a PR.

## Epistemic rules

- Do not upgrade a conjecture to a claim in prose or docstrings.
- Numerical evidence is not a proof; label it as evidence.
- The meta-audit (`validate_claims.py`) rejects a small list of overclaim
  phrases; extend it when you find new ones.

## Commits and PRs

- One logical change per commit; explain *why* in the body.
- Update `CHANGELOG.md` and version metadata for releases.
- PRs should state: what changed, how it was verified, and which claims (if
  any) changed status.
