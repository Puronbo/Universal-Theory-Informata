"""CLI entry point: python -m model ..."""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

from model import (
    check_predictions,
    delta_norm,
    iterate,
    logistic,
    milestone_date,
    milestone_reached,
    rho_lambda_ratio,
)


def _run_meta_audit() -> None:
    """Run validate_claims.py from the repository checkout."""
    script = Path(__file__).resolve().with_name("validate_claims.py")
    if not script.exists():
        raise SystemExit(f"validate_claims.py not found next to {__file__}")
    result = subprocess.run(
        [sys.executable, str(script)], capture_output=True, text=True, check=False
    )
    print(result.stdout.strip())
    if result.returncode != 0:
        print(result.stderr.strip())
        raise SystemExit(result.returncode)


def main() -> None:
    parser = argparse.ArgumentParser(prog="model", description="Model engine CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    de = sub.add_parser("darkenergy", help="CPL dark energy calc")
    de.add_argument("--w0", type=float, default=-0.75)
    de.add_argument("--wa", type=float, default=-0.87)
    de.add_argument("--z", type=float, default=1.0)

    rec = sub.add_parser("recurse", help="Iterate a map")
    rec.add_argument("--map", choices=["cos", "logistic"], default="cos")
    rec.add_argument("--r", type=float, default=2.5)
    rec.add_argument("--x0", type=float, default=0.5)

    sub.add_parser("timeline", help="Milestone status")
    sub.add_parser("validate", help="Run meta-audit")

    args = parser.parse_args()
    if args.cmd == "darkenergy":
        print(
            json.dumps(
                {
                    "rho_ratio": rho_lambda_ratio(args.z, args.w0, args.wa),
                    "delta_norm": delta_norm(args.z, args.w0, args.wa),
                    "predictions": check_predictions(args.w0, args.wa, 0.06, 0.25),
                },
                indent=2,
            )
        )
    elif args.cmd == "recurse":
        f = math.cos if args.map == "cos" else logistic(args.r)
        x, steps, converged, _ = iterate(f, args.x0)
        print(json.dumps({"fixed_point": x, "steps": steps, "converged": converged}, indent=2))
    elif args.cmd == "timeline":
        print(
            json.dumps(
                {
                    "milestone_date": str(milestone_date()),
                    "reached": milestone_reached(),
                },
                indent=2,
            )
        )
    elif args.cmd == "validate":
        _run_meta_audit()


if __name__ == "__main__":
    main()
