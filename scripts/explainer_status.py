#!/usr/bin/env python3
"""
explainer_status.py — understanding coverage for clo-author.

Answers one question: for every analysis script in this project, does a current explainer
exist, and has the author passed its quiz at the *current* version of the script?

Understanding decays when code moves. An explainer written against a script that has since
changed is worse than no explainer, because it reads as current. This tool makes that
mechanical: each explainer carries a 12-char sha256 fingerprint of the script it describes,
and anything that no longer matches is STALE.

Usage
-----
  python3 scripts/explainer_status.py                    # coverage table
  python3 scripts/explainer_status.py --hash <script>    # fingerprint one script
  python3 scripts/explainer_status.py --json             # machine-readable
  python3 scripts/explainer_status.py --gate             # exit 1 if anything is not PASSED

Statuses
--------
  PASSED   explainer current AND a passing quiz attempt logged at this fingerprint
  UNTESTED explainer current, no passing attempt at this fingerprint
  STALE    explainer exists but the script changed since it was written
  MISSING  no explainer

Stdlib only. No dependencies.
"""

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

SCRIPT_SUFFIXES = {".R", ".r", ".py", ".jl", ".do"}
SKIP_DIRS = {"output", "outputs", "logs", "__pycache__", ".ipynb_checkpoints", "renv"}
# Infrastructure scripts live in scripts/ too; they are not analysis and need no explainer.
SKIP_NAMES = {"explainer_status.py", "generate_dashboard.py", "generate_html_report.py",
              "paper_coherence.py", "deepread.py"}

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "scripts"
EXPLAINER_DIR = ROOT / "quality_reports" / "explainers"
LOG_PATH = EXPLAINER_DIR / "understanding_log.md"

STATUS_ORDER = {"MISSING": 0, "STALE": 1, "UNTESTED": 2, "PASSED": 3}


def fingerprint(path: Path) -> str:
    """First 12 hex chars of the file's sha256. Newline-insensitive is deliberate: a
    whitespace-only edit does not invalidate understanding, but any real edit does."""
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()[:12]


def find_scripts() -> list[Path]:
    if not SCRIPTS_DIR.is_dir():
        return []
    out = []
    for p in sorted(SCRIPTS_DIR.rglob("*")):
        if not p.is_file() or p.suffix not in SCRIPT_SUFFIXES:
            continue
        if p.name in SKIP_NAMES or set(p.relative_to(SCRIPTS_DIR).parts) & SKIP_DIRS:
            continue
        out.append(p)
    return out


def explainer_path(script: Path) -> Path:
    return EXPLAINER_DIR / f"{script.stem}_explainer.md"


def read_front_matter(path: Path) -> dict:
    """Minimal YAML front-matter reader: flat `key: value` pairs only."""
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.split("#")[0].strip().strip("'\"")
    return fm


def passing_fingerprints() -> set[str]:
    """Fingerprints with at least one PASS in the understanding log.

    Parsed from the log's per-attempt blocks:
        ### YYYY-MM-DD — scripts/R/03_main.R
        **Fingerprint:** a3f21c9b4e07
        **Score:** 4/5 (Q1 correct)
        **Verdict:** PASS
    """
    if not LOG_PATH.is_file():
        return set()
    text = LOG_PATH.read_text(encoding="utf-8", errors="replace")
    passed, current = set(), None
    for line in text.splitlines():
        if line.startswith("###"):
            current = None
        fm = re.match(r"\*\*Fingerprint:\*\*\s*([0-9a-f]{6,})", line.strip())
        if fm:
            current = fm.group(1)[:12]
        if current and re.match(r"\*\*Verdict:\*\*\s*PASS\b", line.strip()):
            passed.add(current)
    return passed


def classify(script: Path, passed: set[str]) -> dict:
    exp = explainer_path(script)
    current = fingerprint(script)
    row = {
        "script": str(script.relative_to(ROOT)),
        "fingerprint": current,
        "explainer": str(exp.relative_to(ROOT)) if exp.is_file() else None,
    }
    if not exp.is_file():
        row["status"] = "MISSING"
        return row
    recorded = read_front_matter(exp).get("fingerprint", "")
    if recorded != current:
        row["status"] = "STALE"
        row["explainer_fingerprint"] = recorded or "(none)"
        return row
    row["status"] = "PASSED" if current in passed else "UNTESTED"
    return row


def render_table(rows: list[dict]) -> str:
    if not rows:
        return ("No analysis scripts found under scripts/.\n"
                "Nothing to explain yet — run /analyze first.")
    width = max(len(r["script"]) for r in rows)
    lines = [f"{'SCRIPT'.ljust(width)}  STATUS    FINGERPRINT",
             f"{'-' * width}  --------  -----------"]
    for r in sorted(rows, key=lambda r: (STATUS_ORDER[r["status"]], r["script"])):
        lines.append(f"{r['script'].ljust(width)}  {r['status'].ljust(8)}  {r['fingerprint']}")

    counts = {s: sum(1 for r in rows if r["status"] == s) for s in STATUS_ORDER}
    lines.append("")
    lines.append("  ".join(f"{s}: {counts[s]}" for s in
                          ["PASSED", "UNTESTED", "STALE", "MISSING"]))
    todo = [r for r in rows if r["status"] in ("MISSING", "STALE")]
    if todo:
        lines.append("")
        lines.append("Next: /explain " + todo[0]["script"])
    elif any(r["status"] == "UNTESTED" for r in rows):
        first = next(r for r in rows if r["status"] == "UNTESTED")
        lines.append("")
        lines.append(f"Next: /explain {first['script']} --quiz")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Understanding coverage for analysis scripts")
    ap.add_argument("--hash", metavar="SCRIPT",
                    help="print the 12-char fingerprint of one script and exit")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--gate", action="store_true",
                    help="exit 1 unless every script is PASSED (used by /submit)")
    args = ap.parse_args()

    if args.hash:
        p = Path(args.hash)
        if not p.is_absolute():
            p = ROOT / p
        if not p.is_file():
            print(f"No such file: {args.hash}", file=sys.stderr)
            return 2
        print(fingerprint(p))
        return 0

    passed = passing_fingerprints()
    rows = [classify(s, passed) for s in find_scripts()]

    if args.json:
        print(json.dumps({"scripts": rows}, indent=2))
    else:
        print(render_table(rows))

    if args.gate:
        blocking = [r for r in rows if r["status"] != "PASSED"]
        if blocking:
            if not args.json:
                print(f"\nGATE FAILED — {len(blocking)} script(s) without a passing quiz "
                      f"at the current fingerprint.", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
