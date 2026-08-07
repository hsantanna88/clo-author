---
name: analyze
description: End-to-end data analysis dispatching Coder and Data-engineer for implementation, coder-critic for review. Supports R, Python, Julia. Replaces /data-analysis.
argument-hint: "[dataset path or goal] Options: --dual [lang1,lang2]"
allowed-tools: Read,Grep,Glob,Write,Edit,Bash,Task
---

# Analyze

Run end-to-end data analysis by dispatching the **Coder** (analysis), **Data-engineer** (cleaning + figures), and **coder-critic** (code review).

**Input:** `$ARGUMENTS` — dataset path or description of analysis goal.

---

## Workflow

### Step 1: Pre-Code Report (mandatory)
Before writing any code, the Coder must output a structured report proving it read the strategy inputs:

```markdown
## Pre-Code Report
**Strategy memo:** [path or "not found"]
**Domain profile:** [loaded / not found]
**Language:** [R / Python / Julia — from CLAUDE.md]
**Paper type:** [reduced-form / structural / theory+empirics / descriptive]

**Identification strategy:** [one sentence from memo]
**Key variables:**
- Outcome: [paper name] → [code name]
- Treatment: [paper name] → [code name]
- Controls: [list]
- Fixed effects: [list]
- Clustering: [level]
**Data source:** [path or description]
**Estimator:** [from strategy memo]
**Robustness checks required:** [list from memo]
**Naming map confirms:** [yes / no — do planned code names match paper notation?]

Proceeding to implementation.
```

If the strategy memo is missing, the Coder proceeds with the user's description — but flags that no memo was found and strategic alignment checks (coder-critic categories 1-3) cannot be verified.

### Step 2: Data Preparation (if needed)
If raw data provided, dispatch **Data-engineer** first:
- Clean and wrangle raw data
- Handle missing values, construct variables per strategy memo
- Generate summary statistics table
- Create publication-quality descriptive figures
- Save cleaned data, codebook, and figures

### Step 3: Main Analysis
Dispatch **Coder** agent:
- Stage 0: Data loading (from cleaned data or raw)
- Stage 1: Main specification (from strategy memo or user description)
- Stage 2: Robustness checks
- Stage 3: Publication-ready output (tables to `paper/tables/`, figures to `paper/figures/`)
- Produce `results_summary.md` with all estimates, SEs, and key statistics (MANDATORY)
- Save scripts to `scripts/R/` (or appropriate language directory)

The Coder follows these principles:
- **Script structure:** Use the Script Structure Template below
- **Packages:** `fixest` for panel data, `modelsummary` for tables, `ggplot2` for figures
- **Standard errors:** Cluster at appropriate level (match treatment assignment)
- **Output:** `.tex` tables for LaTeX, `.pdf`/`.png` figures, `.rds` for intermediate objects
- **No hardcoded paths.** All paths relative to repository root.
- **saveRDS everything.** Every computed object (estimates, model fits, data frames, summary statistics) gets serialized to `.rds` for downstream use by the writer and other agents.

### Step 4: Code Review
Dispatch **coder-critic** agent — run the full 12-category checklist:

**Strategic (categories 1-3):**
1. **Code-strategy alignment** — Does the code implement the strategy memo faithfully? Correct dependent variable, treatment, controls, fixed effects, sample restrictions?
2. **Sanity checks** — Are summary statistics printed before regressions? Do coefficient signs match economic intuition? Are sample sizes reasonable?
3. **Robustness sufficiency** — Are required robustness checks present? Alternative specifications, placebo tests, sensitivity analysis per strategy memo?

**Code Quality (categories 4-12):**
4. **Structure** — Does the script follow the standard template? Clear section headers, logical flow from setup to export?
5. **Console hygiene** — No spurious `print()` statements polluting output. Intentional output only.
6. **Reproducibility** — `set.seed()` at top if any stochastic elements. No absolute paths. All packages loaded at top. Directory creation with `showWarnings = FALSE`.
7. **Functions** — Repeated logic extracted into functions. No copy-paste code blocks with minor variations.
8. **Figure quality** — Publication-ready: proper axis labels, titles, legends, font sizes. Consistent theme across all figures.
9. **RDS pattern** — Every computed object (models, data frames, summary stats) saved via `saveRDS()` for downstream use. Not just final outputs — intermediate objects too.
10. **Comments** — Section headers present. Non-obvious code commented. No commented-out dead code left behind.
11. **Error handling** — Graceful handling of missing files, empty data subsets, convergence failures. Informative error messages.
12. **Polish** — Consistent naming conventions. No magic numbers. Clean whitespace. Professional quality ready for replication package.

If strategy memo exists, cross-reference code against stated design.
Save report to `quality_reports/[script]_code_review.md`.

Generate HTML version and refresh dashboard:
```bash
python3 scripts/generate_html_report.py code-audit quality_reports/[script]_code_review.md
python3 scripts/generate_dashboard.py
```

### Step 5: Fix Issues
If coder-critic finds Critical or Major issues:
1. Re-dispatch Coder with specific fixes (max 3 rounds)
2. Re-run coder-critic to verify fixes

### Step 6: Explainer and Quiz (mandatory once code review passes)

Code review answers "is this correct?" It does not answer "does the author understand it?" Those
are different questions and only the first one scales — nobody reads a 2,000-line cleaning
pipeline line by line, and the sample restrictions buried in it are what a referee will ask about.

Once coder-critic scores >= 80, dispatch the **explainer** agent (see `.claude/agents/explainer.md`):

```
quality_reports/explainers/{script}_explainer.md    # delta against the strategy memo
quality_reports/explainers/{script}_quiz.md         # 5 questions
quality_reports/explainers/{script}_quiz_key.md     # answers + traces, separate file
```

**If the sample construction ledger comes back `NOT INSTRUMENTED`**, the script is not printing
drop counts. Re-dispatch the Coder to add them to the restriction block, re-run, then re-dispatch
the explainer. Never let the explainer estimate a count it could not read.

Then present the explainer and offer the quiz. Taking it is the author's call — the gate does not
block here. It blocks at `/submit`, warns at `/write results`, and `python3
scripts/explainer_status.py` reports coverage at any time. See `.claude/rules/understanding.md`.

Full protocol, grading, and micro-worlds: `/explain`.

### Step 7: Present Results
1. **Results summary** — key estimates with SEs and interpretation (from `results_summary.md`)
2. **Scripts created** — paths and descriptions
3. **Output files** — tables in `paper/tables/`, figures in `paper/figures/`
4. **Code review score** — from coder-critic
5. **Sample ledger headline** — the restriction that dropped the most observations, with counts
6. **Quiz** — offered, and its result if taken
7. **TODO items** — missing data, additional specifications needed

---

## Script Structure Template

```r
# ============================================================
# [Descriptive Title]
# Author: [from project context]
# Purpose: [What this script does]
# Inputs: [Data files]
# Outputs: [Figures, tables, RDS files]
# ============================================================

# 0. Setup ----
library(tidyverse)
library(fixest)
library(modelsummary)

set.seed(42)

dir.create("paper/tables", recursive = TRUE, showWarnings = FALSE)
dir.create("paper/figures", recursive = TRUE, showWarnings = FALSE)

# 1. Data Loading ----

# 2. Exploratory Analysis ----

# 3. Main Analysis ----

# 4. Tables and Figures ----

# 5. Export ----
# saveRDS(model_fit, "scripts/R/output/model_fit.rds")
# saveRDS(main_results, "scripts/R/output/main_results.rds")
```

---

## Results Summary (Mandatory Artifact)

Every analysis run MUST produce `results_summary.md` containing:
- All point estimates with standard errors and significance levels
- Sample sizes for each specification
- Key summary statistics (means, medians, standard deviations of main variables)
- Robustness check results (brief table or comparison)
- Any flags or anomalies discovered during analysis

This file is the primary handoff artifact to the writer agent. Without it, the writer cannot draft the results section.

---

## Dual-Language Mode (`--dual r,python`)

When `--dual [lang1,lang2]` is provided (e.g., `--dual r,python`, `--dual r,julia`):

1. **Data-engineer** runs once — language-agnostic cleaning, saves to `data/cleaned/`
2. **Two Coder agents** dispatched in parallel — same strategy memo, different languages
3. **coder-critic** reviews each implementation independently (max 3 rounds each)
4. **Comparison step** — verify numerical alignment per `.claude/references/domain-profile.md` tolerances:
   - Point estimates must match within declared tolerance
   - Standard errors must match within declared tolerance
   - Flag any divergences with exact values from both languages
5. Save comparison report to `quality_reports/cross_language_comparison.md`

### Replication Tolerance Approach

Inspired by Scott Cunningham's replication methodology: **if two independent implementations agree, neither has a bug.** This is the core rationale for dual-language mode.

**Tolerance thresholds:**
- **Floating-point differences are normal.** Minor numerical differences (e.g., 1e-10) between R and Python arise from different linear algebra backends, optimizer defaults, and floating-point arithmetic. These are expected, not bugs.
- **Point estimates:** Must agree within 1e-6 (relative) or as declared in `domain-profile.md`
- **Standard errors:** Must agree within 1e-4 (relative) — SE computation varies more across implementations due to degrees-of-freedom corrections and clustering algorithms
- **P-values:** Must agree on significance at conventional levels (0.01, 0.05, 0.10). If one language says p=0.049 and the other says p=0.051, flag for manual review but do not treat as a bug.
- **Sample sizes:** Must match exactly. Any discrepancy indicates a data handling difference that must be resolved.

**When results diverge beyond tolerance:**
1. Both Coder agents are re-dispatched to investigate
2. Check: different default options (e.g., na.rm handling, convergence criteria)
3. Check: different variable coding or factor ordering
4. The comparison report includes a side-by-side table of all estimates
5. If divergence persists after investigation, escalate to user with exact values from both languages

---

## Bundled Resources

### Templates
| File | Purpose |
|------|---------|
| `analyze/templates/pre-code-report.md` | Mandatory pre-check report format before writing code |
| `analyze/templates/paper-to-code-map.md` | Naming map protocol: paper notation to code variables |
| `analyze/templates/r-script-structure.R` | Boilerplate R script scaffold following INV-14..19 |
| `analyze/templates/python-script-structure.py` | Boilerplate Python script scaffold |
| `analyze/templates/results-summary.md` | Mandatory results summary output for writer handoff |

### References
| File | Purpose |
|------|---------|
| `analyze/references/table-standards.md` | Full table formatting standards: booktabs, coefficient display, panel structure, R packages, file naming |
| `analyze/references/figure-standards.md` | Full figure formatting standards: themes, colors, axis labels, export settings, common plot types |

### Config
| File | Purpose |
|------|---------|
| `analyze/config/replication-tolerances.json` | Tolerances for dual-language replication comparison (point estimates, SEs, p-values) |

### Gotchas
| File | Purpose |
|------|---------|
| `analyze/gotchas.md` | Known failure points: R package quirks, numerical issues, output traps, cross-language divergence sources |

---

## Principles
- **Reproduce, don't guess.** If the user specifies a regression, run exactly that.
- **Show your work.** Print summary statistics before jumping to regressions.
- **Strategy alignment.** If strategy memo exists, code MUST implement it faithfully.
- **Worker-critic pairing.** Coder creates, coder-critic critiques. Never skip review.
- **Correct is not the same as understood.** Every passing script gets an explainer and a quiz. If you cannot say which restriction cost you the most observations, you do not yet own the result.
- **saveRDS everything.** Every computed object gets saved via `saveRDS()` for downstream use -- model fits, cleaned data frames, summary statistics, not just final tables.
- **Publication-ready output.** Tables and figures directly includable in the paper.
- **Cross-language convergence.** When `--dual` is used, divergence is a bug until proven otherwise.
