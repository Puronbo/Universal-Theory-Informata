# Security Policy

## Supported versions

| Version | Supported |
|---|---|
| 0.2.x | yes |
| < 0.2 | no |

## Reporting a vulnerability

Please **do not open a public issue** for security problems. Use GitHub's
private vulnerability reporting: repository → **Security** → **Report a
vulnerability**.

Include:

- affected version/commit,
- a minimal reproduction,
- impact (for example: arbitrary code execution, path traversal, CI secret
  exposure, dependency compromise),
- any suggested fix.

You should receive an acknowledgement within seven days. Once a fix is ready,
we will coordinate disclosure and credit you unless you prefer to stay
anonymous.

## Scope

In scope:

- the Python package (`model/`, `cli.py`),
- the CLI and validation scripts,
- CI workflows and packaging metadata.

Out of scope:

- the physical/metaphysical truth of the model's claims (see
  `GROUNDING.md` for the project's epistemic policy),
- numerical disagreement with the model's predictions,
- vulnerabilities in optional local tooling that is not part of the package.

## Practices

- Dependencies are updated by Dependabot; CI installs from `pyproject.toml`.
- The package performs no network, filesystem-write, or credential access at
  import time.
- `cli validate` executes the repository's own `validate_claims.py` with the
  current interpreter; it never executes user-supplied paths.
- Static analysis runs in CI (`bandit`); findings must be fixed or explicitly
  skipped with a documented reason in `pyproject.toml`.
