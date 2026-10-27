"""Meta-audit: grep for overclaim phrases (L.O.R.E.-style honest audit)."""
import re, pathlib

ROOT = pathlib.Path(__file__).parent
FORBIDDEN = [
    "is entirely governed",
    "physics is entirely",
    "we have proven",
    "the model proves",
    "True Observer downloaded",
]
# Files to scan (docs + code)
TARGETS = ["AXIOMS.md", "GROUNDING.md", "CONNECTIONS.md", "GUIDE.md",
           "FOLDING_CALIBRATION.md", "HORIZON_FINDINGS.md", "LORE_CALIBRATION.md"]

def main():
    hits = []
    for name in TARGETS:
        p = ROOT / name
        if not p.exists():
            continue
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            low = line.lower()
            if any(w in low for w in ("never", "not ", "caution", "aspir", "label")):
                continue
            for phrase in FORBIDDEN:
                if phrase.lower() in low:
                    hits.append((name, i, phrase, line.strip()[:120]))
    if hits:
        print("OVERCLAIM HITS:")
        for h in hits:
            print(f"  {h[0]}:{h[1]} [{h[2]}] {h[3]}")
        return 1
    print("Meta-audit: no overclaim phrases found.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
