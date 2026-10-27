"""CLI entry point: python -m model ..."""
import argparse
import json
from engine import (
    w_cpl, rho_lambda_ratio, delta_norm, check_predictions,
    iterate, logistic, milestone_reached, milestone_date, net_zero,
)

def main():
    p = argparse.ArgumentParser(prog="model", description="Model engine CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    de = sub.add_parser("darkenergy", help="CPL dark energy calc")
    de.add_argument("--w0", type=float, default=-0.75)
    de.add_argument("--wa", type=float, default=-0.87)
    de.add_argument("--z", type=float, default=1.0)

    rec = sub.add_parser("recurse", help="Iterate a map")
    rec.add_argument("--map", choices=["cos", "logistic"], default="cos")
    rec.add_argument("--r", type=float, default=2.5)
    rec.add_argument("--x0", type=float, default=0.5)

    tl = sub.add_parser("timeline", help="Milestone status")

    args = p.parse_args()
    if args.cmd == "darkenergy":
        print(json.dumps({
            "rho_ratio": rho_lambda_ratio(args.z, args.w0, args.wa),
            "delta_norm": delta_norm(args.z, args.w0, args.wa),
            "predictions": check_predictions(args.w0, args.wa, 0.06, 0.25),
        }, indent=2))
    elif args.cmd == "recurse":
        import math
        f = (lambda x: math.cos(x)) if args.map == "cos" else logistic(args.r)
        x, steps, conv = iterate(f, args.x0)
        print(json.dumps({"fixed_point": x, "steps": steps, "converged": conv}, indent=2))
    elif args.cmd == "timeline":
        print(json.dumps({"milestone_date": str(milestone_date()),
                          "reached": milestone_reached()}, indent=2))

if __name__ == "__main__":
    main()
