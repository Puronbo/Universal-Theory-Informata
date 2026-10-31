"""Run all checks: tests, meta-audit, lean build."""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
LEAN = os.path.join(ROOT, "lean")


def run(label, cmd, cwd=None):
    print(f"\n=== {label} ===")
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    print(r.stdout.strip() or "(no stdout)")
    if r.stderr.strip():
        print(r.stderr.strip()[:500])
    return r.returncode


rc = 0
rc |= run("Python tests", [sys.executable, "-m", "pytest", "tests/", "-q"], cwd=ROOT)
rc |= run("Meta-audit", [sys.executable, "validate_claims.py"], cwd=ROOT)
rc |= run("Lean build", ["lake", "build"], cwd=LEAN)
print(f"\n=== RESULT: {'PASS' if rc == 0 else 'FAIL'} (rc={rc}) ===")
raise SystemExit(rc)
