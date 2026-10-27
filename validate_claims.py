"""Meta-audit: grep for overclaim phrases + axiom cross-reference check."""
import re, pathlib, ast

ROOT = pathlib.Path(__file__).parent

def check_engine_refs():
    src = (ROOT / "engine.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    funcs = {n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
    # also module-level constants
    consts = {t.targets[0].id for t in tree.body if isinstance(t, ast.Assign) and isinstance(t.targets[0], ast.Name)}
    known = funcs | consts
    missing = []
    for md in ROOT.glob("*.md"):
        for m in re.finditer(r"engine\.([A-Za-z_][A-Za-z0-9_]*)", md.read_text(encoding="utf-8")):
            name = m.group(1)
            if name == "py":
                continue
            if name not in known:
                missing.append((md.name, name))
    return missing
FORBIDDEN = [
    "is entirely governed",
    "physics is entirely",
    "we have proven",
    "the model proves",
    "True Observer downloaded",
]

def check_overclaims():
    hits = []
    targets = ["AXIOMS.md", "GROUNDING.md", "CONNECTIONS.md", "GUIDE.md",
               "FOLDING_CALIBRATION.md", "HORIZON_FINDINGS.md", "LORE_CALIBRATION.md",
               "STROBOSCOPIC.md", "PRIZED_PROBLEMS.md"]
    for name in targets:
        p = ROOT / name
        if not p.exists():
            continue
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            low = line.lower()
            if any(w in low for w in ("never", "not ", "caution", "aspir", "label", "candidate")):
                continue
            for phrase in FORBIDDEN:
                if phrase.lower() in low:
                    hits.append((name, i, phrase, line.strip()[:120]))
    return hits

def check_cross_refs():
    # Every axiom label A#.# in AXIOMS.md should appear in CONNECTIONS.md
    axioms = set(re.findall(r"\*\*A\d+\.\d+", (ROOT / "AXIOMS.md").read_text(encoding="utf-8")))
    axioms = {a.replace("**", "") for a in axioms}
    conn = (ROOT / "CONNECTIONS.md").read_text(encoding="utf-8")
    missing = [a for a in sorted(axioms) if a not in conn]
    return missing

def main():
    hits = check_overclaims()
    if hits:
        print("OVERCLAIM HITS:")
        for h in hits:
            print(f"  {h[0]}:{h[1]} [{h[2]}] {h[3]}")
        return 1
    missing_refs = check_engine_refs()
    if missing_refs:
        print("ENGINE REFERENCES NOT FOUND:")
        for m in missing_refs:
            print(f"  {m[0]}: engine.{m[1]}")
        return 1
    print("Meta-audit: no overclaim phrases found.")
    print("Engine references: all valid.")
    return 0
    print("Meta-audit: no overclaim phrases found.")
    if missing:
        print(f"  ({len(missing)} axioms not yet in CONNECTIONS.md)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
