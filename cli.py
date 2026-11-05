"""CLI entry point: python -m model ..."""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

from model import (
    DUAL_PAIRS,
    check_predictions,
    compare_regimes,
    delta_norm,
    dual_of,
    dual_pair,
    entropy,
    information_loss,
    iterate,
    logistic,
    lyapunov_exponent,
    milestone_date,
    milestone_reached,
    orbit_period,
    rho_lambda_ratio,
)


def _fail(message: str) -> NoReturn:
    """Print a CLI error to stderr and exit with status 2."""
    print(message, file=sys.stderr)
    raise SystemExit(2)


def _duality_command(pole: str | None, pair_name: str | None) -> None:
    """Report dual pairs, one named pair, or the opposite of one pole."""
    if pole is not None:
        try:
            opposite = dual_of(pole)
        except ValueError as exc:
            _fail(str(exc))
        print(json.dumps({"pole": pole, "dual": opposite}, indent=2))
    elif pair_name is not None:
        try:
            pair = dual_pair(pair_name)
        except ValueError as exc:
            _fail(str(exc))
        print(
            json.dumps(
                {"name": pair.name, "left": pair.left, "right": pair.right},
                indent=2,
            )
        )
    else:
        print(
            json.dumps(
                {
                    "count": len(DUAL_PAIRS),
                    "pairs": [
                        {"name": pair.name, "left": pair.left, "right": pair.right}
                        for pair in DUAL_PAIRS
                    ],
                },
                indent=2,
            )
        )


def _antithesis_command(x: float, steps: int, rate: float, shift: float) -> None:
    """Report the periodic, hyperbolic, and parabolic orbits from ``x``."""
    if not math.isfinite(x) or x <= 0.0:
        _fail("x must be finite and > 0")
    try:
        regimes = compare_regimes(x, steps, rate, shift)
        payload = {
            "initial": regimes.initial,
            "steps": steps,
            "involution": list(regimes.involution),
            "contraction": list(regimes.contraction),
            "translation": list(regimes.translation),
            "periods": {
                "involution": orbit_period(regimes.involution),
                "contraction": orbit_period(regimes.contraction),
                "translation": orbit_period(regimes.translation),
            },
            "entropy": entropy(x),
            "information_loss": information_loss(x, steps, rate),
            "lyapunov_exponent": lyapunov_exponent(rate),
        }
    except ValueError as exc:
        _fail(str(exc))
    print(json.dumps(payload, indent=2))


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

    dual = sub.add_parser("duality", help="Dual pairs and opposite poles")
    dual_group = dual.add_mutually_exclusive_group()
    dual_group.add_argument("--pole", help="pole to flip, e.g. UV")
    dual_group.add_argument("--pair", dest="pair_name", help="pair name, e.g. scale")

    anti = sub.add_parser("antithesis", help="Periodic, hyperbolic, and parabolic orbits")
    anti.add_argument("--x", type=float, default=2.0)
    anti.add_argument("--steps", type=int, default=3)
    anti.add_argument("--rate", type=float, default=0.5)
    anti.add_argument("--shift", type=float, default=1.0)

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
    elif args.cmd == "duality":
        _duality_command(args.pole, args.pair_name)
    elif args.cmd == "antithesis":
        _antithesis_command(args.x, args.steps, args.rate, args.shift)


if __name__ == "__main__":
    main()
