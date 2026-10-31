"""Meta-audit: grep for overclaim phrases + axiom cross-reference check."""

from __future__ import annotations

import argparse
import ast
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent

FORBIDDEN = [
    "is entirely governed",
    "physics is entirely",
    "we have proven",
    "the model proves",
    "True Observer downloaded",
]

OVERCLAIM_TARGETS = [
    "AXIOMS.md",
    "GROUNDING.md",
    "CONNECTIONS.md",
    "GUIDE.md",
    "FOLDING_CALIBRATION.md",
    "HORIZON_FINDINGS.md",
    "LORE_CALIBRATION.md",
    "STROBOSCOPIC.md",
    "PRIZED_PROBLEMS.md",
]


def generate_crossref_table() -> str:
    """Render a table of axioms and whether CONNECTIONS.md mentions each."""
    axioms = sorted(
        {
            a.replace("**", "")
            for a in re.findall(r"\*\*A\d+\.\d+", (ROOT / "AXIOMS.md").read_text(encoding="utf-8"))
        }
    )
    conn = (ROOT / "CONNECTIONS.md").read_text(encoding="utf-8")
    lines = ["| Axiom | In CONNECTIONS.md |", "|---|---|"]
    for axiom in axioms:
        status = "yes" if axiom in conn else "no"
        lines.append(f"| {axiom} | {status} |")
    return "\n".join(lines)


def check_engine_refs() -> list[tuple[str, str]]:
    """Return (file, name) pairs for `model.<name>` references that do not exist."""
    src = (ROOT / "model" / "__init__.py").read_text(encoding="utf-8")
    all_match = re.search(r"__all__\s*=\s*\[(.*?)\]", src, re.DOTALL)
    known: set[str] = set()
    if all_match:
        known.update(re.findall(r'"([^"]+)"', all_match.group(1)))

    for mod_file in (ROOT / "model").glob("*.py"):
        if mod_file.name == "__init__.py":
            continue
        known.add(mod_file.stem)  # module names are valid `model.<name>` targets
        try:
            tree = ast.parse(mod_file.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                known.add(node.name)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        known.add(target.id)

    missing: list[tuple[str, str]] = []
    for md in ROOT.glob("*.md"):
        for match in re.finditer(
            r"model\.([A-Za-z_][A-Za-z0-9_]*)", md.read_text(encoding="utf-8")
        ):
            name = match.group(1)
            if name != "py" and name not in known:
                missing.append((md.name, name))
    return missing


def check_overclaims() -> list[tuple[str, int, str, str]]:
    """Return (file, line, phrase, text) for forbidden claim phrases."""
    hits: list[tuple[str, int, str, str]] = []
    for name in OVERCLAIM_TARGETS:
        path = ROOT / name
        if not path.exists():
            continue
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            low = line.lower()
            if any(
                word in low for word in ("never", "not ", "caution", "aspir", "label", "candidate")
            ):
                continue
            for phrase in FORBIDDEN:
                if phrase.lower() in low:
                    hits.append((name, line_no, phrase, line.strip()[:120]))
    return hits


def check_cross_refs() -> list[str]:
    """Return axiom labels present in AXIOMS.md but absent from CONNECTIONS.md."""
    axioms = {
        a.replace("**", "")
        for a in re.findall(r"\*\*A\d+\.\d+", (ROOT / "AXIOMS.md").read_text(encoding="utf-8"))
    }
    conn = (ROOT / "CONNECTIONS.md").read_text(encoding="utf-8")
    return [axiom for axiom in sorted(axioms) if axiom not in conn]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate-crossref", action="store_true")
    args = parser.parse_args()
    if args.generate_crossref:
        print(generate_crossref_table())
        return 0

    hits = check_overclaims()
    if hits:
        print("OVERCLAIM HITS:")
        for file, line_no, phrase, text in hits:
            print(f"  {file}:{line_no} [{phrase}] {text}")
        return 1

    missing_refs = check_engine_refs()
    if missing_refs:
        print("MODEL REFERENCES NOT FOUND:")
        for file, name in missing_refs:
            print(f"  {file}: model.{name}")
        return 1

    missing_axioms = check_cross_refs()
    if missing_axioms:
        print("AXIOMS MISSING FROM CONNECTIONS.md:")
        for axiom in missing_axioms:
            print(f"  {axiom}")
        return 1

    print("Meta-audit: no overclaim phrases found.")
    print("Model references: all valid.")
    print("Axioms: all present in CONNECTIONS.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
