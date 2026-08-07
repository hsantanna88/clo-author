---
name: explain
description: Build understanding of analysis code an agent wrote — delta-explainer, 5-question quiz with separate answer key, optional interactive micro-world. Dispatches the explainer agent. Run it before you take a result to a coauthor, a seminar, or a referee.
argument-hint: "[script path or 'all'] Options: --quiz | --grade | --microworld | --status"
allowed-tools: Read,Grep,Glob,Write,Edit,Bash,Task
---

# Explain

Correctness is what `/review` checks. **Comprehension is what this checks.** Agents produce analysis faster than you can read it; the binding constraint on a paper is no longer whether the code runs, it is whether the author can reconstruct why the estimation sample looks the way it does.

`/explain` produces three artifacts and one gate.

**Input:** `$ARGUMENTS` — a script path (`scripts/R/03_main_estimation.R`), `all`, or a flag.

---

## Modes

| Invocation | What happens |
|-----------|--------------|
| `/explain scripts/R/03_main.R` | Explainer + quiz (questions and key), then offers to run the quiz |
| `/explain all` | Every script flagged missing or stale by `--status` |
| `/explain <script> --quiz` | Ask the five questions, wait for answers, grade, log |
| `/explain <script> --grade` | Grade answers already in the conversation |
| `/explain <script> --microworld` | Also build the interactive HTML micro-world |
| `/explain --status` | Coverage table: which scripts have current / stale / missing explainers |

---

## Workflow

### Step 1: Coverage check
```bash
python3 scripts/explainer_status.py
```
Prints one row per script under `scripts/`: `CURRENT`, `STALE` (script changed since the explainer was written), or `MISSING`. With no target argument, present this table and ask which script to explain.

### Step 2: Dispatch the explainer
Dispatch the **explainer** agent with the script, the strategy memo, `results_summary.md`, and any prior explainer for the same script.

The agent writes:

```
quality_reports/explainers/{script}_explainer.md    # delta-explainer, with fingerprint
quality_reports/explainers/{script}_quiz.md         # 5 questions, no answers
quality_reports/explainers/{script}_quiz_key.md     # answers + traces
```

### Step 3: Instrument the ledger if it is missing
If the sample construction ledger comes back `NOT INSTRUMENTED`, the script is not printing drop counts. **This is the most common outcome on the first run and it is worth fixing at the source.**

Offer to dispatch **coder** to add counting to the restriction block:

```r
n0 <- nrow(dt)
dt <- dt[age %between% c(18, 64)]
message(sprintf("  age 18-64: %s -> %s (dropped %s)",
                format(n0, big.mark = ","), format(nrow(dt), big.mark = ","),
                format(n0 - nrow(dt), big.mark = ",")))
```

Then re-run the script and re-dispatch the explainer. Never let the explainer fill the gap with a guess.

### Step 4: Read it, then take the quiz
Present the explainer. Then ask the five questions — **one message, all five, no answers in view.** Wait for the author. Do not hint, do not narrow the options, do not reveal an answer because they are close.

### Step 5: Grade and log
Grade strictly against the key (rules in `.claude/agents/explainer.md`). Pass = 4/5 with Q1 correct.

Report per question: verdict, the correct answer, and the trace (script line or results file). For each miss, name the explainer section to re-read.

Append the attempt to `quality_reports/explainers/understanding_log.md` and add a research journal entry per `.claude/rules/logging.md`.

### Step 6: Micro-world (only if asked)
Build the single-file HTML per `.claude/agents/explainer.md`, using `.claude/skills/explain/templates/microworld.html` as the skeleton. Label precomputed vs. illustrative in the page header. Open it for the user.

---

## The understanding gate

Per `.claude/rules/understanding.md` (INV-26):

| Point in the pipeline | Enforcement |
|----------------------|-------------|
| After `/analyze` passes code review | Explainer + quiz generated automatically |
| `/write results` | **Warn** if the script behind the tables has no passing quiz attempt |
| `/submit` | **Block** — every script producing a paper exhibit needs a current explainer and a passing attempt at the current fingerprint |

Stale ≠ missing. If the script changed after the last passing attempt, the fingerprint no longer matches and the gate reopens. That is the point: understanding decays when the code moves.

The gate is a gate, not a score. It never enters the weighted quality aggregate — a quiz result is a fact about the author, not about the artifact.

---

## Bundled Resources

### Templates
| File | Purpose |
|------|---------|
| `explain/templates/explainer-doc.md` | Delta-explainer structure with the sample ledger |
| `explain/templates/quiz.md` | Question and answer-key format, with worked examples |
| `explain/templates/microworld.html` | Self-contained interactive skeleton (slider → estimate) |

### Scripts
| File | Purpose |
|------|---------|
| `scripts/explainer_status.py` | Fingerprints scripts, reports CURRENT / STALE / MISSING, reads the log |

---

## Principles

- **Delta, not tutorial.** Explain what departs from the strategy memo. Everything else is noise.
- **The ledger is not optional.** Every sample restriction, with counts, in application order, reconciling to the N in the main table.
- **Answers live in a separate file.** A visible key measures nothing.
- **Fail is information.** A missed question points at a section to re-read, never at code to rewrite.
- **Never guess a number.** `NOT INSTRUMENTED` is honest; a plausible count is a fabrication that will end up in a footnote.
- **Label simulated micro-worlds loudly.** An illustrative toy mistaken for an estimate is a retraction.
