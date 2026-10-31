## What changed

<!-- One or two sentences. Link issues if relevant. -->

## Verification

- [ ] `python -m pytest tests -q --cov-fail-under=90`
- [ ] `ruff check .`
- [ ] `black --check model cli.py validate_claims.py tests`
- [ ] `mypy model cli.py`
- [ ] `python validate_claims.py`
- [ ] `cd lean && lake build` (if Lean changed)

## Claim status

<!-- Did this change upgrade, downgrade, or leave untouched any epistemic
     claim? grounded / candidate / phenomenological. -->

## Notes for reviewers

<!-- Anything tricky, follow-ups, or intentional trade-offs. -->
