#!/usr/bin/env python3
"""
deepread.py — run the deep-read audit on any clo-author paper, via Codex.

Segments the paper with paper_coherence.py, fans readers out across segments as
parallel `codex exec` calls, batch-verifies each segment's comments, then merges
and writes the report. Every model call goes to Codex, so a full run costs no
Claude tokens.

Project-agnostic: point it at any paper directory.

    python3 scripts/deepread.py --root . --paper paper
    python3 scripts/deepread.py --segment seg03 --skeptic
    python3 scripts/deepread.py --dry-run            # projection only, no calls

Reader roles and their instructions live in .claude/agents/paper-reader-*.md.
Standard library only. Python 3.9+.
"""

from __future__ import annotations

import argparse
import concurrent.futures as futures
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
AGENTS = REPO / ".claude" / "agents"
COHERENCE = HERE / "paper_coherence.py"

CAP = 3  # max comments per reader — see the Hard limit section in each role file
BUDGET_TOKENS = 2_500_000
DEBUG_DIR: Optional[Path] = None  # set by --debug


# --------------------------------------------------------------------------
# Codex bridge
# --------------------------------------------------------------------------


def codex(prompt: str, cwd: Path, timeout: int = 900) -> Tuple[str, int]:
    """One headless Codex call. Read-only sandbox — this pipeline never edits."""
    try:
        proc = subprocess.run(
            [
                "codex", "exec",
                "--sandbox", "read-only",
                "--skip-git-repo-check",
                prompt,
            ],
            cwd=str(cwd),
            input="",
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        raise SystemExit("error: codex CLI not found on PATH (brew install codex)")
    except subprocess.TimeoutExpired:
        return "", 0
    # Codex writes the transcript to stdout and its usage footer to stderr.
    out = (proc.stdout or "") + "\n" + (proc.stderr or "")
    m = re.search(r"tokens used\s*\n?\s*([\d,]+)", out)
    tokens = int(m.group(1).replace(",", "")) if m else 0
    if DEBUG_DIR is not None:
        DEBUG_DIR.mkdir(parents=True, exist_ok=True)
        n = len(list(DEBUG_DIR.glob("*.txt")))
        (DEBUG_DIR / ("%03d.txt" % n)).write_text(
            "=== PROMPT ===\n" + prompt + "\n\n=== OUTPUT ===\n" + out, encoding="utf-8")
    return out, tokens


def clean_prose(text: str) -> str:
    """Strip Codex's framing and stderr footer from a markdown answer."""
    for marker in ("\nhook: Stop", "\ntokens used", "\nReading additional input"):
        i = text.find(marker)
        if i > 0:
            text = text[:i]
    # Codex echoes a banner and the prompt before the answer; the answer starts
    # at the last standalone "codex" line.
    i = text.rfind("\ncodex\n")
    if i != -1:
        text = text[i + len("\ncodex\n"):]
    lines = [ln for ln in text.splitlines()
             if not ln.startswith(("OpenAI Codex v", "----", "workdir:", "model:",
                                   "provider:", "approval:", "sandbox:", "reasoning",
                                   "[20", "ERROR ", "--------"))]
    out = "\n".join(lines).strip()
    # our own section header is added by the report writer
    for h in ("## Overall assessment", "# Overall assessment"):
        if out.startswith(h):
            out = out[len(h):].lstrip()
    return out


def extract_json(text: str) -> Optional[object]:
    """Recover the JSON value a Codex run ended with.

    Codex emits reasoning, then the answer, then a usage footer on stderr. A
    greedy regex spans all three and never parses, so scan backwards from the
    last closing bracket and return the first slice that loads.
    """
    # Drop the trailing footer so the last bracket belongs to the answer.
    # NB: "\ncodex\n" precedes the final answer — trimming there would cut it.
    for marker in ("\nhook: Stop", "\ntokens used"):
        i = text.rfind(marker)
        if i > 0:
            text = text[:i]
    for close, open_ in (("]", "["), ("}", "{")):
        end = text.rfind(close)
        while end != -1:
            start = text.rfind(open_, 0, end)
            while start != -1:
                try:
                    return json.loads(text[start : end + 1])
                except Exception:
                    start = text.rfind(open_, 0, start)
            end = text.rfind(close, 0, end)
    return None


# --------------------------------------------------------------------------
# Prompts
# --------------------------------------------------------------------------


def role_file(role: str) -> Path:
    return AGENTS / ("paper-reader-%s.md" % role)


def reader_prompt(role: str, seg_path: Path, seg_dir: Path, context: str) -> str:
    return f"""You are the "{role}" deep-read commenter for an economics paper.

FIRST read your role definition in full and follow it exactly:
  {role_file(role)}

THEN read the segment you are assigned:
  {seg_path}

It contains the section's prose ("text"), the tables it cites with captions,
notes and parsed rows ("tables"), figures, equations, and theorem blocks.

Document context: {seg_dir}/manifest.json is the paper's structure.
{context}

Comment on THIS segment only. Every comment must quote exact text from it.
Return AT MOST {CAP} comments, ranked — this limit is not negotiable.
If the segment is sound, return an empty array. That is a valid result.

Output ONLY a JSON array, no prose around it, each element:
{{"quote","title","problem","why_it_matters","fix",
  "severity":"critical|major|minor","confidence":"high|medium|low"}}"""


def verify_prompt(seg_id: str, seg_path: Path, comments: List[dict]) -> str:
    return f"""You are the adversarial verifier for one section of an economics paper.
Your job is to REFUTE comments, not collect them.

Read your role definition and follow it exactly:
  {AGENTS / "coherence-skeptic.md"}

The section under review:
  {seg_path}
You may open the paper's .tex files for surrounding context.

All {len(comments)} comments raised on this section:

{json.dumps(comments, indent=2)}

For each: does the quoted text actually say what the comment claims? Is there a
nearby sentence, footnote, or table note that already answers it? Is it taste
rather than a defect? Default to refuted when uncertain — passing a weak comment
costs far more than dropping a real one.

Seeing them together, also collapse comments that are the same underlying defect.

Return ONLY the survivors as a JSON array, same element shape as the input plus
"survived_because". Expect to keep a small minority. An empty array is valid."""


def merge_prompt(survivors: List[dict], coherence_findings: List[dict]) -> str:
    return f"""You are the consolidator for a deep read of an economics paper.

Read your role definition and follow it exactly:
  {AGENTS / "coherence-consolidator.md"}

Comments that survived adversarial verification, across all sections:

{json.dumps(survivors, indent=2)}

A deterministic engine already reported these mechanical findings. DROP any
comment that merely restates one of them — they are already covered and they
block on their own:

{json.dumps(coherence_findings[:40], indent=2)}

Deduplicate by "same underlying edit", merge clusters (taking the LOWEST
confidence in each), and rank by what changes the paper's conclusions.

Return markdown: comments grouped by section, ranked within each, every one
carrying its exact quote, the problem, why it matters, and the specific fix."""


def overall_prompt(merged: str, seg_dir: Path) -> str:
    return f"""You write the overall assessment for a deep read of an economics paper.

Read your role definition and follow it exactly:
  {AGENTS / "paper-overall.md"}

Paper structure: {seg_dir}/manifest.json
Abstract and introduction: {seg_dir}/seg01.json, {seg_dir}/seg02.json

The merged comments:

{merged}

Write the assessment per your role file: the argument in your own words, what
has to hold for it to stand, the two or three things that most threaten it
(ranked, each citing evidence and what would settle it), and what the paper
already handles. One page. No score, no accept/reject verdict. Markdown only."""


# --------------------------------------------------------------------------
# Pipeline
# --------------------------------------------------------------------------


def plan_readers(manifest: List[dict], skeptic: bool) -> List[Tuple[str, str]]:
    jobs: List[Tuple[str, str]] = []
    for m in manifest:
        jobs.append((m["id"], "general"))
        if skeptic:
            jobs.append((m["id"], "skeptic"))
        if m["tables"]:
            jobs.append((m["id"], "evidence"))
        if m["equations"] or m["theory_blocks"]:
            jobs.append((m["id"], "rigor"))
    return jobs


def project(manifest: List[dict], jobs: List[Tuple[str, str]]) -> Dict[str, object]:
    readers, verifiers = len(jobs), len(manifest)
    est = readers * 37_000 + verifiers * 106_000 + 2 * 56_000
    return {
        "segments": len(manifest),
        "readers": readers,
        "verifiers": verifiers,
        "agents": readers + verifiers + 2,
        "max_comments": readers * CAP,
        "projected_tokens": est,
        "over_budget": est > BUDGET_TOKENS,
    }


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Deep-read audit via Codex.")
    ap.add_argument("--root", default=".", help="Project root")
    ap.add_argument("--paper", default="paper", help="Manuscript directory")
    ap.add_argument("--segment", default=None, help="Run one segment only (e.g. seg03)")
    ap.add_argument("--skeptic", action="store_true", help="Add the adversarial twin reader")
    ap.add_argument("--min-segment-words", type=int, default=300)
    ap.add_argument("--jobs", type=int, default=6, help="Parallel Codex calls (default 6)")
    ap.add_argument("--dry-run", action="store_true", help="Project cost, make no calls")
    ap.add_argument("--out", default=None, help="Report path")
    ap.add_argument("--debug", default=None, help="Directory to dump raw Codex transcripts")
    args = ap.parse_args(argv)

    global DEBUG_DIR
    if args.debug:
        DEBUG_DIR = Path(args.debug).resolve()
    root = Path(args.root).resolve()
    seg_dir = root / "quality_reports" / "deepread" / "segments"

    if not args.dry_run and not shutil.which("codex"):
        sys.stderr.write(
            "error: codex CLI not found on PATH.\n"
            "  install:  brew install codex\n"
            "  then:     codex login\n"
            "  (use --dry-run to see the cost projection without Codex)\n"
        )
        return 2
    if not COHERENCE.is_file():
        sys.stderr.write("error: %s not found — deepread needs it to segment\n" % COHERENCE)
        return 2
    if not AGENTS.is_dir():
        sys.stderr.write("error: reader roles not found at %s\n" % AGENTS)
        return 2

    # 1. Segment (deterministic, free)
    rc = subprocess.run(
        [
            sys.executable, str(COHERENCE),
            "--root", str(root), "--paper", args.paper, "--quiet",
            "--segments", str(seg_dir),
            "--min-segment-words", str(args.min_segment_words),
            "--json", str(root / "quality_reports" / "coherence" / "index.json"),
        ],
        capture_output=True, text=True,
    )
    if not (seg_dir / "manifest.json").is_file():
        sys.stderr.write("error: segmentation produced nothing\n%s\n" % rc.stderr[:400])
        return 2

    manifest = json.loads((seg_dir / "manifest.json").read_text())
    if args.segment:
        manifest = [m for m in manifest if m["id"] == args.segment]
        if not manifest:
            sys.stderr.write("error: no such segment: %s\n" % args.segment)
            return 2

    jobs = plan_readers(manifest, args.skeptic)
    proj = project(manifest, jobs)

    print("Segments      %d" % proj["segments"])
    print("Readers       %d (skeptic %s)" % (proj["readers"], "on" if args.skeptic else "off"))
    print("Verifiers     %d" % proj["verifiers"])
    print("Total agents  %d" % proj["agents"])
    print("Max comments  %d (cap %d/reader)" % (proj["max_comments"], CAP))
    print("Projected     %.1fM tokens  [Codex]" % (proj["projected_tokens"] / 1e6))
    if proj["over_budget"]:
        print("WARNING: over the %.1fM budget — raise --min-segment-words or drop --skeptic"
              % (BUDGET_TOKENS / 1e6))
    if args.dry_run:
        return 0

    segs = {m["id"]: seg_dir / ("%s.json" % m["id"]) for m in manifest}
    context = "The paper is in %s." % (root / args.paper)
    spent = 0
    t0 = time.time()

    # 2. Read — parallel Codex calls
    print("\nReading...")
    by_seg: Dict[str, List[dict]] = {m["id"]: [] for m in manifest}
    with futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futs = {
            pool.submit(codex, reader_prompt(role, segs[sid], seg_dir, context), root): (sid, role)
            for sid, role in jobs
        }
        for fut in futures.as_completed(futs):
            sid, role = futs[fut]
            out, tok = fut.result()
            spent += tok
            parsed = extract_json(out)
            got = parsed if isinstance(parsed, list) else []
            for c in got[:CAP]:
                if isinstance(c, dict):
                    c["role"], c["seg"] = role, sid
                    by_seg[sid].append(c)
            print("  %-7s %-9s %2d comments  (%s tok)" % (sid, role, len(got[:CAP]), f"{tok:,}"))

    raised = sum(len(v) for v in by_seg.values())
    print("  -> %d comments raised, %s tokens" % (raised, f"{spent:,}"))

    # 3. Verify — one batched call per segment
    print("\nVerifying...")
    survivors: List[dict] = []
    todo = [(sid, cs) for sid, cs in by_seg.items() if cs]
    with futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futs = {
            pool.submit(codex, verify_prompt(sid, segs[sid], cs), root): sid
            for sid, cs in todo
        }
        for fut in futures.as_completed(futs):
            sid = futs[fut]
            out, tok = fut.result()
            spent += tok
            parsed = extract_json(out)
            kept = parsed if isinstance(parsed, list) else []
            for c in kept:
                if isinstance(c, dict):
                    c["seg"] = sid
                    survivors.append(c)
            print("  %-7s %2d -> %2d survived  (%s tok)"
                  % (sid, len(by_seg[sid]), len(kept), f"{tok:,}"))

    print("  -> %d survived of %d" % (len(survivors), raised))

    # 4. Merge + 5. Overall
    findings = []
    idx_path = root / "quality_reports" / "coherence" / "index.json"
    if idx_path.is_file():
        try:
            findings = json.loads(idx_path.read_text()).get("findings", [])
        except Exception:
            findings = []

    merged, overall = "", ""
    if survivors:
        print("\nMerging...")
        merged_raw, tok = codex(merge_prompt(survivors, findings), root)
        merged = clean_prose(merged_raw)
        spent += tok
        print("  consolidated  (%s tok)" % f"{tok:,}")
        print("Assessing...")
        overall_raw, tok = codex(overall_prompt(merged, seg_dir), root)
        overall = clean_prose(overall_raw)
        spent += tok
        print("  overall  (%s tok)" % f"{tok:,}")

    # 6. Report
    date = datetime.date.today().isoformat()
    out_path = Path(args.out) if args.out else (
        root / "quality_reports" / "deepread" / ("%s_report.md" % date)
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Deep Read", "",
        "**Date:** %s  " % date,
        "**Paper:** `%s`  " % (Path(args.paper) / "main.tex"),
        "**Engine:** Codex (`codex exec`), %d agents" % proj["agents"], "",
        "## Funnel", "",
        "| | |", "|---|---:|",
        "| Segments | %d |" % proj["segments"],
        "| Readers | %d |" % proj["readers"],
        "| Comments raised | %d |" % raised,
        "| Survived verification | %d |" % len(survivors),
        "| Tokens (Codex) | %s |" % f"{spent:,}",
        "| Projected | %s |" % f"{proj['projected_tokens']:,}",
        "| Wall clock | %.1f min |" % ((time.time() - t0) / 60),
        "",
    ]
    if overall.strip():
        lines += ["## Overall assessment", "", overall.strip(), ""]
    if merged.strip():
        lines += ["## Comments", "", merged.strip(), ""]
    if not survivors:
        lines += ["## Comments", "", "No comments survived verification.", ""]
    out_path.write_text("\n".join(lines), encoding="utf-8")

    print("\n%s" % out_path)
    print("Actual %s tokens vs %s projected (%.0f%%)"
          % (f"{spent:,}", f"{proj['projected_tokens']:,}",
             100.0 * spent / max(1, proj["projected_tokens"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
