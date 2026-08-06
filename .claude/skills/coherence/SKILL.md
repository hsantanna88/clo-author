---
name: coherence
description: >
  Catch internal inconsistencies in a paper and propose concrete fixes. Checks
  cross-references, citation keys, claim numbers against the tables they cite,
  derived arithmetic, and notation. Two layers — a deterministic parser that
  produces verifiable findings, and an optional reasoning pass for what parsing
  cannot reach. This is the verifier, not the referee: it answers "is the paper
  internally sound", never "is the paper any good". Use before every commit, and
  always before submission.
argument-hint: "[file path] Options: --deep, --fix, --strict, --json"
allowed-tools: Read,Grep,Glob,Bash,Task,Write
---

# Coherence

Internal-consistency audit. Every finding is checkable: a reference either
resolves or it does not, a number either appears in the cited table or it does
not. Judgment calls belong to `/review`, not here.

**Input:** `$ARGUMENTS` — optional file path to scope the audit, plus flags.

---

## Why this is separate from `/review`

A referee report mixes two kinds of finding, and blending them makes both worse:

| | Coherence (this skill) | `/review --peer` |
|---|---|---|
| Question | Is the paper internally sound? | Would this be published? |
| Verdict | Checkable — right or wrong | Contestable — referees disagree |
| Severity | Blocking when major | Scored, advisory |
| Cost | Free, seconds | Minutes, judgment-heavy |
| Cadence | Every commit | Once, pre-submission |

Run this first. It clears the factual layer so the referees spend their comments
on identification and contribution instead of stale numbers.

---

## Layer 1 — Deterministic (always runs)

```bash
python3 scripts/paper_coherence.py \
  --root . --paper paper \
  --json quality_reports/coherence/index.json \
  --markdown quality_reports/coherence/$(date +%F)_report.md
```

Standard library only, no dependencies, exits 1 when a blocking finding exists.

| Check | Severity | What it proves |
|---|---|---|
| `undefined-ref` | major | A `\ref`/`\cref` target has no `\label` |
| `duplicate-label` | major | The same label is defined twice |
| `undefined-cite` | major | A citation key is absent from the `.bib` |
| `missing-input` | major | An `\input{}` target does not exist |
| `missing-graphic` | major | An `\includegraphics{}` target does not exist |
| `number-mismatch` | major | A claim number in prose matches no cell in any table |
| `abstract-number-unsourced` | major | An abstract number appears in no table |
| `number-wrong-table` | minor | The number exists, but in a table other than the one cited |
| `derived-arithmetic` | minor | "X% relative to a baseline of Y" does not follow from the stated effect |
| `significance-mismatch` | minor | Reported p-value disagrees with the cell's stars |
| `orphan-float` | minor | A table or figure is never referenced in the text |
| `table-file-wrapped` | minor | A table body carries its own float/caption (INV-13) |
| `float-in-section` | minor | A float is declared in a section file (INV-23) |
| `duplicate-macro` | minor | A macro is defined twice — silent notation drift (INV-7) |

Enforces **INV-7, INV-11, INV-13, INV-23**.

### How number matching works

A claim number is matched rounding-tolerantly against every cell of the tables
its paragraph cites, allowing a percentage-point rescale and sign loss. Prose
"4.9 percentage points" matches a cell of `0.0489`; "standard error 0.016"
matches `(0.0162)`; "$-0.017$" matches `-0.0170`.

Table context carries forward from a `\cref` until the next section heading,
because papers cite a table once and then discuss it for several paragraphs.

**Deliberately not treated as claims** — these were each a measured source of
false positives, not hypotheticals:

- bare integers (indices, counts, `$\ell = -3$`)
- rate denominators (`per 100,000`)
- p-values, F-statistics, and confidence-interval bounds
- figures the author marks "not shown" / "available on request"
- hedged figures (`roughly 5.7`) — reported as minor, never blocking
- years and year ranges, citation years, layout lengths (`0.5em`)

When no table body can be parsed at all, the number checks stay silent rather
than inventing findings about tables they could not read.

---

## Layer 2 — Reasoning fan-out (`--deep`)

Five specialists in parallel, adversarial verification per finding, then a merge
stage. Same shape as `/review --peer` (editor → parallel referees → decision),
and the same shape Refine uses (commenters → skeptic → dedup → consolidate).

```
paper_coherence.py --slices           ← pre-filter: each agent gets its own slice
        │
   ┌────┼────┬────────┬─────────┬────────┐
   ▼    ▼    ▼        ▼         ▼        │  PARALLEL
 spec  claims continuity notation theory │
  R1    R2+R6    R3        R4      R5    │
   └────┴────┴────────┴─────────┴────────┘
        │  union of candidate findings
        ▼
   coherence-skeptic  × one per finding, in parallel — tries to REFUTE
        │  survivors
        ▼
   coherence-consolidator  ← dedup across checks, merge clusters, rank
        │
        ▼
   ## Reasoning layer  (appended to the report)
```

### Why each stage exists

**Slicing.** `--slices` writes one candidate file per check. The specification
auditor gets equation bodies and the paragraphs citing them; the notation auditor
gets symbols used in more than one file. Nobody reads the whole paper — that is
what makes five agents affordable. Typical counts on a 40-page applied paper:
specification 3, claims 15, continuity 48, notation 1, theory 0.

**Separate agents, not one agent with six checks.** Each check is a different
kind of reading, and one context holding all six attends to the later ones
worse. Independent agents also do not anchor on each other: an agent that just
found an estimand drift is primed to find more.

**The skeptic.** Fan-out multiplies the false-positive surface — five agents
each licensed to report, none able to see the others. One skeptic per finding,
prompted to refute and defaulting to refuted when uncertain, is what keeps the
precision the deterministic layer earned.

**The consolidator.** Overlapping slices produce the same defect from different
angles: a sign flip surfaces as both R6 and R1. Without a merge stage the fan-out
yields a longer report, not a better one. This is the stage Refine had to build
two of (`COMMENT_DEDUPLICATOR`, `COMMENT_CONSOLIDATOR`), and skipping it is the
standard way fan-out goes wrong.

### Dispatch

1. Run Layer 1 with `--slices quality_reports/coherence/slices`
2. Dispatch the five specialists in parallel, one Task each, passing only its
   slice path. **Skip any agent whose slice is empty** — an applied paper with no
   theorem environments must not spawn a theory auditor.
3. Union the returned findings. Dispatch one `coherence-skeptic` per finding, in
   parallel. Drop everything refuted; substitute any `corrected_finding`.
4. Dispatch `coherence-consolidator` once over the survivors plus the Layer 1
   findings.
5. Append its `## Reasoning layer` section to the report.

Agent count: 5 finders (fewer when slices are empty) + one skeptic per candidate
+ 1 consolidator. On a clean applied paper that is typically 4 + 2 + 1.

Checks are specified in `checks/reasoning-checks.md`. Reasoning findings are
**advisory and never block**, and are kept visually separate in the report — they
are the layer that can be wrong.

---

## Modes

| Invocation | Behavior |
|---|---|
| `/coherence` | Layer 1 over the whole paper |
| `/coherence sections/results.tex` | Layer 1 scoped to one file |
| `/coherence --deep` | Layer 1 + Layer 2 |
| `/coherence --fix` | Layer 1, then apply only unambiguous mechanical fixes |
| `/coherence --strict` | Promote minor findings to blocking (pre-submission) |
| `/coherence --json` | Emit the index only, no markdown |

### What `--fix` will and will not touch

Applies:
- `undefined-ref` where exactly one defined label is within edit distance 2 (a typo)
- `missing-graphic` where exactly one file in `figures/` matches the stem (a wrong extension)

Never applies:
- **Any claim number.** When prose and table disagree, the tool cannot know
  which is right — the table may be stale, or the prose may be. Report the
  nearest cell and let the author decide. Auto-editing a result is the one
  failure mode that would make this tool dangerous.
- Structural findings (`float-in-section`, `table-file-wrapped`) — those need a
  human to decide placement.

After `--fix`, re-run the audit and re-compile.

---

## Reporting

Save to `quality_reports/coherence/YYYY-MM-DD_report.md`; the index goes to
`quality_reports/coherence/index.json`. Refresh the dashboard afterwards:

```bash
python3 scripts/generate_dashboard.py
```

Present to the user in this order: verdict, blocking findings with the nearest
table cell for each, then non-blocking, then the coverage table. Always state
the coverage numbers — "87 claim numbers checked against 393 table cells" is
what makes a clean result meaningful. A PASS with 0 cells indexed means the
tables could not be parsed, not that the paper is sound; say so plainly.

---

## Gate

| Context | Rule |
|---|---|
| Commit | Blocking findings must be zero |
| PR | Blocking zero; minor reported |
| `/submit final` | Run with `--strict`; blocking and minor both zero |
| Talks | Advisory (INV-21 traceability still applies) |

Deterministic findings are blocking because they are facts. Reasoning findings
never block on their own.

---

## Principles

- **Every finding is checkable.** If it cannot be verified without trusting a
  model, it belongs in Layer 2 and is labelled advisory.
- **Silence is a valid result.** A clean paper produces an empty report. Do not
  manufacture findings to look useful.
- **Never auto-edit a result.** Report the discrepancy and the nearest cell.
- **False positives are the failure mode.** One bad finding costs more trust
  than ten real ones earn. Any new check ships with a false-positive audit
  across real papers before it is enabled.
- **Precision over recall on numbers.** Missing a stale number is recoverable;
  crying wolf on a correct one trains the author to ignore the tool.
