# Understanding: The Comprehension Gate

Agents write analysis faster than the author can read it. `/review` and the critics check whether
the code is *correct*. This rule covers the other failure — code that is correct and that the
author cannot explain.

That failure has a cost the quality score does not capture. A referee asks why the estimation
sample has 549,598 workers; a seminar attendee asks what happens without the balanced-panel
requirement; a coauthor asks which deflator base year was used. "Let me check the script" is an
acceptable answer once. It is not an acceptable posture toward your own paper.

---

## The rule

**INV-26.** Every script that produces a paper exhibit (a file in `paper/tables/` or
`paper/figures/`) has a current explainer in `quality_reports/explainers/` and a passing quiz
attempt logged at the script's current fingerprint.

Current means the fingerprint in the explainer's front matter matches
`python3 scripts/explainer_status.py --hash <script>`. When the script changes, the explainer goes
STALE and the gate reopens — deliberately. Understanding decays when the code moves.

---

## Enforcement points

| Where | Enforcement | Rationale |
|-------|-------------|-----------|
| `/analyze`, after coder-critic >= 80 | **Generate** explainer + quiz automatically | The moment the code is trustworthy is the moment to understand it |
| `/write results` | **Warn** if the scripts behind the tables have no passing attempt | You can draft against numbers you have not internalized; you should know that you are |
| `/submit` | **Block** — `python3 scripts/explainer_status.py --gate` must exit 0 | Nothing leaves under your name that you cannot defend |
| `/dashboard refresh` | **Report** the coverage table | Makes decay visible before it becomes a deadline problem |

Between those points the gate is silent. This is not a checkpoint to clear on every edit.

---

## Not a score

The understanding gate never enters the weighted quality aggregate in `quality.md`. It is a gate,
like `/coherence` — pass/fail, no partial credit, no deduction.

The reason is structural: **a quiz result is a fact about the author, not about the artifact.** A
score measures the work; folding a comprehension result into it would let good code compensate for
an author who does not understand it, which is exactly the trade this rule exists to prevent. It
would also create pressure to write easy quizzes.

For the same reason: the explainer agent never rewrites code in response to a failed quiz. A miss
means re-read a section, not refactor a script.

---

## What makes an explainer honest

Full protocol in `.claude/agents/explainer.md`. The three that matter most:

1. **The sample construction ledger reconciles.** Every restriction, in application order, with
   counts, ending at exactly the N in the main table. A ledger that does not reconcile is itself
   the finding.
2. **Counts are read, never estimated.** If the script does not print drop counts, the explainer
   says `NOT INSTRUMENTED` and the fix is to instrument the script — not to infer a plausible
   number. A fabricated count is the one failure mode of this system that is worse than no system.
3. **Answer keys live in a separate file.** A quiz with visible answers measures nothing.

---

## Commands

```bash
python3 scripts/explainer_status.py              # coverage: PASSED / UNTESTED / STALE / MISSING
python3 scripts/explainer_status.py --hash <f>   # fingerprint one script
python3 scripts/explainer_status.py --gate       # exit 1 unless all PASSED (submission gate)
```

```
/explain <script>              # explainer + quiz
/explain <script> --quiz       # take it, get graded, logged
/explain <script> --microworld # interactive knobs over the choices that mattered
/explain --status              # coverage table
```
