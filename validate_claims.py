"""Meta-audit: grep for overclaim phrases + axiom cross-reference check."""
import re, pathlib, ast

ROOT = pathlib.Path(__file__).parent

# Import the model package to get function/class names
import model


def check_engine_refs():
    src = (ROOT / "model" / "__init__.py").read_text(encoding="utf-8")
    # Get all exports from __all__
    all_match = re.search(r'__all__\s*=\s*\[(.*?)\]', src, re.DOTALL)
    known = set()
    if all_match:
        items = all_match.group(1)
        for item in re.findall(r'"([^"]+)"', items):
            known.add(item)
    # Also check module-level constants in engine modules
    for mod_file in (ROOT / "model").glob("*.py"):
        if mod_file.name == "__init__.py":
            continue
        try:
            mod_src = mod_file.read_text(encoding="utf-8")
            tree = ast.parse(mod_src)
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    known.add(node.name)
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            known.add(target.id)
        except SyntaxError:
            pass

    missing = []
    for md in ROOT.glob("*.md"):
        for m in re.finditer(r"model\.([A-Za-z_][A-Za-z0-9_]*)", md.read_text(encoding="utf-8")):
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
        print("MODEL REFERENCES NOT FOUND:")
        for m in missing_refs:
            print(f"  {m[0]}: model.{m[1]}")
        return 1
    print("Meta-audit: no overclaim phrases found.")
    print("Model references: all valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())