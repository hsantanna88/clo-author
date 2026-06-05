# Plan: Enforcement Layer — Lessons from Escafoldiamento

**Status:** COMPLETED **Date:** 2026-04-09 **Origin:** Comparative analysis of cattvs (Escafoldiamento) architecture **Scope:** 5 improvements to clo-author's enforcement mechanisms, borrowing patterns from cattvs's contract-driven, grep-verified, hook-enforced approach

------------------------------------------------------------------------

## Context

The cattvs scaffold uses a defensive engineering pattern: contracts as source of truth, grep-based verification skills, pre/post hooks that enforce quality automatically, numbered architectural invariants, and structured decision records. Clo-author's creative orchestration (worker-critic pairs, scoring rubrics, multi-agent pipeline) is stronger, but its enforcement layer is softer — relying on agent judgment where mechanical verification would be more reliable.

These 5 changes add hard enforcement without compromising the creative architecture.

------------------------------------------------------------------------

## Item 1: Grep-Based Verification Checks for R/Python/Julia Scripts

**What:** Add a verification skill or extend `/review --code` with mechanically verifiable checks that run grep/pattern matching before the coder-critic's judgment rubric.

**Why:** The coder-critic's 16 check categories are judgment-based. Mechanical checks catch the obvious stuff instantly and let the critic focus on harder questions (strategy alignment, numerical discipline edge cases).

**Files to modify:** - `.claude/skills/review/SKILL.md` — add a `--lint` mode or integrate into existing `--code` flow - Alternatively: create `.claude/skills/tools/SKILL.md` new subcommand `/tools lint`

**Checks to implement (R):**

``` bash
# set.seed() present exactly once, near top of script
grep -c 'set\.seed(' script.R

# All library() calls in first 30 lines
grep -n 'library(' script.R | awk -F: '$1 > 30 {print "FAIL: library() at line " $1}'

# No absolute paths
grep -n '/Users/\|/home/\|C:\\' script.R

# No growing vectors in loops (append pattern)
grep -n 'c(.*,.*)\s*$' script.R  # heuristic — flag for manual review

# No == on floats
grep -n '==.*\.' script.R | grep -v 'character\|string\|integer\|TRUE\|FALSE'

# No print() in final scripts (use message() or logging)
grep -n '^[^#]*print(' script.R

# Packages loaded at top, not mid-script
# (check that no library() call appears after first non-comment, non-library line)
```

**Checks to implement (Python):**

``` bash
# No absolute paths
grep -n '/Users/\|/home/\|C:\\' script.py

# random seed set
grep -c 'random\.seed\|np\.random\.seed\|torch\.manual_seed' script.py

# imports at top
grep -n '^import \|^from ' script.py | awk -F: '$1 > 30 {print "FAIL: import at line " $1}'
```

**Effort:** Small. 1-2 hours. Mostly writing grep patterns and adding them to a skill.

------------------------------------------------------------------------

## Item 2: Pre-Flight Loading in /analyze

**What:** Make Step 1 of `/analyze` explicitly output what it read from the strategy memo and domain profile before any code is written. The coder must state: "I read the strategy memo. The identification strategy is X. The key variables are Y. The naming map I'll follow is Z." Only then proceed to write code.

**Why:** The cattvs `/pre-code` skill forces contract loading before implementation. Currently, the coder agent is *instructed* to read the strategy memo, but there's no verification it actually did, and no explicit mapping from strategy concepts to code variable names.

**Files to modify:** - `.claude/skills/analyze/SKILL.md` — restructure Step 1 to require explicit output - `.claude/agents/coder.md` — add a "Pre-Code Report" section as mandatory first output

**Pre-Code Report format:**

``` markdown
## Pre-Code Report
**Strategy memo:** [path or "not found"]
**Paper type:** [reduced-form / structural / theory+empirics / descriptive]
**Identification strategy:** [one sentence]
**Key variables:**
- Outcome: [paper name] → [code name]
- Treatment: [paper name] → [code name]
- Controls: [list]
- Fixed effects: [list]
**Data source:** [path]
**Naming map confirms:** [yes/no — do code names match paper notation?]

Proceeding to implementation.
```

**Effort:** Small. 30 minutes. Edit two files.

------------------------------------------------------------------------

## Item 3: Numbered Content Invariants

**What:** Create `.claude/rules/content-invariants.md` with 10-15 numbered, non-negotiable rules for paper and code output. These are the "laws" — the writer-critic, coder-critic, and verifier check against them.

**Why:** These rules currently exist scattered across `content-standards.md`, `working-paper-format.md`, agent prompts, and journal profiles. A single numbered list makes enforcement unambiguous and gives critics a canonical reference to cite in deductions.

**File to create:** - `.claude/rules/content-invariants.md`

**Draft invariants:**

``` markdown
# Content Invariants

These are non-negotiable. Every agent checks against them. Violations are deductions, not suggestions.

## Paper

1. Every table uses `threeparttable` with notes explaining key variables, sample, and data source.
2. Every figure has a note below it (via `\caption` or figure notes) explaining what is shown.
3. No `\hline` — use `\toprule`, `\midrule`, `\bottomrule` (booktabs).
4. Significance stars follow journal profile. AEA journals: no stars. Default: stars with note defining thresholds.
5. Abstract is 150 words or fewer.
6. JEL codes and keywords present after abstract.
7. Notation is consistent across all sections — same symbol means same thing everywhere.
8. Every causal claim has a corresponding identification section. No causal language in descriptive papers.
9. `biblatex` + `biber`, not `natbib` + `bibtex`.
10. `hyperref` loaded last in preamble.

## Code

11. `set.seed()` called exactly once, at the top of the main script, if any stochastic element exists.
12. All packages loaded at the top of the script, before any data or computation.
13. No absolute paths. All paths relative to project root.
14. No growing vectors in loops — pre-allocate or use vectorized operations.
15. Output files go to the path specified by the Output Organization setting in CLAUDE.md.

## Talk

16. Notation in talk matches paper exactly — same symbols, same subscripts.
17. Every claim on a slide is traceable to the paper. No orphan results.
```

**Effort:** Small. 1 hour. Consolidate existing scattered rules, number them, write the file. Update agent prompts to reference it.

**Files to also update (add "Check content-invariants.md" to review criteria):** - `.claude/agents/writer-critic.md` - `.claude/agents/coder-critic.md` - `.claude/agents/storyteller-critic.md` - `.claude/agents/verifier.md`

------------------------------------------------------------------------

## Item 4: Strategy Decision Records

**What:** When the strategist proposes an identification strategy and the user approves it, save a structured decision record alongside the strategy memo.

**Why:** Strategy memos are prose. The coder reads them to understand *what* to implement, but not *why* this approach was chosen over alternatives. When a referee later asks "why not use IV instead of DiD?", the response letter writer needs to know what was considered and rejected. ADR-style records capture this.

**File to modify:** - `.claude/skills/strategize/SKILL.md` — add Step 4: save strategy decision record

**Template:**

``` markdown
# Strategy Decision Record — [Date]

## Research Question
[One sentence]

## Chosen Strategy
[Method, data, variation]

## Alternatives Considered

| Alternative | Why rejected |
|-------------|-------------|
| [IV with X] | [No valid instrument for Z] |
| [RDD at threshold Y] | [Insufficient density near cutoff] |
| [Structural model] | [Reduced-form sufficient for policy question] |

## Key Assumptions
1. [Parallel trends hold because...]
2. [No anticipation because...]

## What Would Invalidate This
- [If pre-trends fail...]
- [If the instrument is weak...]

## Approved By
[User, date]
```

**Save to:** `quality_reports/strategy_decision_[date].md`

**Effort:** Small. 30 minutes. Edit the skill, add template.

------------------------------------------------------------------------

## Item 5: PostToolUse Hook for R Script Linting

**What:** Add a PostToolUse hook that runs lightweight checks on R/Python scripts after any Edit or Write operation.

**Why:** Cattvs runs cppcheck after every edit automatically. A lightweight lint on R scripts would catch absolute paths, missing `set.seed()`, misplaced `library()` calls, and other mechanical issues before the coder-critic is even dispatched.

**Files to modify:** - `.claude/settings.json` — add PostToolUse hook - `.claude/hooks/lint-scripts.sh` — new hook script

**Hook logic (lint-scripts.sh):**

``` bash
#!/bin/bash
# Only run on R/Python files
FILE="$CLAUDE_TOOL_ARG_FILE_PATH"
[[ "$FILE" != *.R && "$FILE" != *.py ]] && exit 0

ERRORS=""

# Check for absolute paths
if grep -qn '/Users/\|/home/\|C:\\' "$FILE" 2>/dev/null; then
  ERRORS+="WARNING: Absolute path detected. Use relative paths.\n"
fi

# R-specific
if [[ "$FILE" == *.R ]]; then
  # Check library() after line 30
  LATE_LIBS=$(grep -n 'library(' "$FILE" | awk -F: '$1 > 30 {print $0}')
  if [[ -n "$LATE_LIBS" ]]; then
    ERRORS+="WARNING: library() calls should be at top of script:\n$LATE_LIBS\n"
  fi
fi

if [[ -n "$ERRORS" ]]; then
  echo -e "$ERRORS"
fi

exit 0  # Advisory, not blocking
```

**Settings.json addition:**

``` json
{
  "matcher": "Edit|Write",
  "hooks": [{
    "type": "command",
    "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/lint-scripts.sh",
    "timeout": 5
  }]
}
```

**Decision: advisory or blocking?** Start advisory (exit 0). Promote to blocking after testing across projects.

**Effort:** Small-medium. 1 hour. Write the hook, test it, add to settings.

------------------------------------------------------------------------

## Implementation Order

| Order | Item | Effort | Dependencies |
|----------------|----------------|----------------|-------------------------|
| 1 | Item 3: Content invariants | 1 hour | None — standalone file + agent refs |
| 2 | Item 2: Pre-flight in /analyze | 30 min | None |
| 3 | Item 1: Grep-based verification | 1-2 hours | Item 3 (references invariants) |
| 4 | Item 4: Strategy decision records | 30 min | None |
| 5 | Item 5: PostToolUse lint hook | 1 hour | Test across a real project first |

Total: \~4-5 hours. Could be a single session or spread across two.

------------------------------------------------------------------------

## What This Does NOT Change

- Agent architecture (worker-critic pairs) — untouched
- Quality scoring model (weighted rubrics) — untouched
- Skill structure (10 commands) — untouched
- Orchestration flow (dependency graph) — untouched

This adds an **enforcement layer underneath** the existing creative orchestration. The agents still do judgment work. The new layer catches mechanical violations before judgment is even needed.

------------------------------------------------------------------------

## Version

This would be **v4.1.0** — "Enforcement Layer" or "Hard Gates."