# Manuscript Review: 8 Check Categories

Extracted from `writer-critic.md`. Used by the writer-critic agent for manuscript review.

---

## Prerequisite Checks

**Before running categories:**

- Read `.claude/rules/content-invariants.md` -- enforce INV-1 through INV-13 and INV-27. Cite invariant numbers (e.g., "violates INV-3") in report alongside deductions.
- Read `.claude/rules/thesis-format.md` -- enforce all Required items listed in the deduction table.
- Identify the paper type (reduced-form, structural, theory+empirics, descriptive) from the strategy memo or the manuscript itself. This determines which checks apply.

---

## 1. Structure and Flow

- Does the paper follow the standard section order for its paper type?
- Does each paragraph have a single identifiable argument move (motivation, result statement, mechanism, qualification, etc.)?
- Are transitions between sections coherent?
- Does the introduction contribution statement appear in the first 2 pages?
- Is there a roadmap? (Optional but if present, is it one sentence?)
- Does the conclusion restate the main finding with effect size?

**Paper-type-specific:**

**Reduced-form:** Introduction follows: motivation -> question -> stakes -> identification preview -> result -> literature positioning?

**Structural:** Introduction includes model preview -> estimation/counterfactual preview -> key counterfactual result -> literature?

**Theory + empirics:** Introduction includes theory preview -> empirical preview -> literature positioning?

**Descriptive:** Introduction includes data/measurement innovation -> key fact -> why it matters -> literature?

---

## 2. Claims and Evidence

- Every empirical claim is supported by a table, figure, or citation
- No orphan claims (assertions without evidence)
- Numbers in text match the tables and figures exactly (INV-11)
- Effect sizes stated with units ("4.2 percentage points", not "the coefficient is significant")
- Comparisons to prior literature include specific magnitudes from cited papers
- No stale numbers (values that don't match current output files)

**Claim-source map verification (INV-27):**
- Does `quality_reports/claim_source_map_{project}.md` exist? If not: -15
- Every numerical claim in the manuscript has a map entry? -5 per missing
- Map entries point to files that exist? -10 per broken link
- Numbers in the map match the manuscript? -5 per mismatch

---

## 3. Identification Fidelity

- Does the empirical strategy section accurately describe the strategy memo's design?
- No overclaiming: causal language only in papers with causal designs (INV-8)
- Assumptions named and stated formally (parallel trends, exclusion restriction, continuity, etc.)
- Threats acknowledged -- no "our results are robust to all concerns"
- Estimand clearly stated (ATT, ATE, LATE, or equivalent)

**Paper-type-specific:**

**Reduced-form:** Design-specific elements present (pre-trends for DiD, first stage for IV, bandwidth for RDD, event definition for ES)?

**Structural:** Identification argument maps data moments to parameters? Estimation method justified?

**Theory + empirics:** Testable predictions numbered and linked to evidence?

**Descriptive:** No causal language. Patterns described as correlations or associations.

---

## 4. Writing Quality

Run the 24-pattern AI detection check from the Writer's cleanup pass:

**Content patterns:**
- Significance inflation ("pivotal moment", "transformative impact", "groundbreaking") -- -3 per, max -9
- Promotional language -- -3 per, max -9
- Superficial -ing analyses ("highlighting...", "underscoring...") -- -2 per, max -6
- Vague attributions ("experts argue", "scholars have noted") -- -3 per, max -9

**Language patterns:**
- AI vocabulary (additionally, delve, foster, garner, interplay, tapestry, underscore, landscape) -- -2 per, max -10
- Copula avoidance ("serves as" instead of "is") -- -1 per, max -5
- Negative parallelisms ("not X but Y" overuse) -- -2 per, max -6
- Excessive hedging beyond field norms -- -3

**Style patterns:**
- Em dash overuse (>2 per page) -- -3
- Rule of three everywhere -- -3
- Uniform sentence length (no variation) -- -5

**Communication patterns:**
- Filler phrases ("It's important to note that...", "It is worth mentioning...") -- -2 per, max -6
- Announcements ("In the next section, we will discuss...") -- -2 per, max -6

---

## 5. LaTeX and Format

Enforce all Required items from `.claude/rules/thesis-format.md`:

| Issue | Deduction |
|-------|-----------|
| Wrong document class or font size (not 12pt article) | -5 |
| Missing `\doublespacing` in body | -5 |
| Using `natbib` instead of `biblatex` (INV-9) | -3 |
| Using `bibtex` instead of `biber` (INV-9) | -3 |
| Missing `fancyhdr` page number setup | -2 |
| `\textbf{}` wrapping `\title{}` | -3 |
| `\and` between authors instead of `\quad` | -3 |
| Repeated affiliation text outside `\thanks{}` | -3 |
| Missing JEL codes or keywords (INV-6) | -5 |
| `\hline` instead of booktabs rules (INV-3) | -3 |
| Missing table notes (INV-1) | -5 per table, max -15 |
| Missing figure notes (INV-2) | -5 per figure, max -15 |
| `hyperref` not loaded second-to-last (INV-10) | -2 |
| Missing `cleveref` after `hyperref` (INV-10) | -2 |
| Manual `Figure~\ref{}` instead of `\cref{}` | -1 per, max -5 |
| Missing `microtype` | -2 |
| Missing abstract `\noindent` and `\singlespacing` | -2 |
| Abstract exceeds 150 words (INV-5) | -3 |
| No titles inside figures -- titles in `\caption{}` only (INV-12) | -3 per, max -9 |
| R/Python/Julia output includes `\begin{table}` wrapper (INV-13) | -3 per, max -9 |

---

## 6. Compilation

Verifier-lite checks:

- Does the paper compile with `latexmk` without errors? If not: -20
- All `\ref{}` and `\cref{}` references resolved (no "??" in output)? -3 per unresolved
- All `\cite{}` keys exist in the bibliography file? -3 per missing
- All cited tables/figures exist in `paper/tables/` and `paper/figures/`? -5 per missing
- No overfull/underfull hbox warnings exceeding 10pt? -1 per, max -5

---

## 7. Voice Fidelity

**Only scored when `.claude/references/personal-style-guide.md` contains real content (not the template).**

Compare the draft against the style guide:

| Issue | Deduction |
|-------|-----------|
| Uses 3+ words from "author avoids" list | -5 per word, max -15 |
| Sentence length median off by >5 words from guide | -5 |
| Paragraph openings don't match documented patterns | -3 per, max -9 |
| Tone mismatch (e.g., bombastic when author is dry) | -10 |
| Hedging frequency doesn't match documented pattern | -3 |
| Em dash rate deviates significantly from guide | -2 |

If the style guide is still a template, report: "Voice fidelity not scored -- style guide not yet extracted. Run `/write style-guide [paper-dir]` to enable."

---

## 8. Notation Consistency

- Same symbol means the same thing everywhere (INV-7)
- Every symbol defined at first use
- Notation matches the strategy memo
- Subscript conventions consistent ($i$ for individual, $t$ for time, $g$ for group -- or whatever the paper uses, but consistent)
- Notation in tables matches notation in text

---

## Standalone Mode

When invoked via `/review [file.tex]` or `/review --proofread`, run categories **4, 5, 6, 8 only** (writing quality + LaTeX + compilation + notation). No strategy alignment -- just prose and format quality.

When invoked via `/review --all` or `/review --peer`, run all 8 categories.

---

## Report Format

```markdown
# Manuscript Review -- [Project Name]
**Date:** [YYYY-MM-DD]
**Reviewer:** writer-critic
**Paper type:** [Reduced-form / Structural / Theory+Empirics / Descriptive]
**Score:** [XX/100]
**Mode:** [Full / Standalone (prose quality only)]

## Structure and Flow: [COHERENT/ISSUES/MAJOR ISSUES]
## Claims and Evidence: [SUPPORTED/GAPS/UNSUPPORTED]
## Identification Fidelity: [FAITHFUL/OVERCLAIMED/MISREPRESENTED]
## Writing Quality: [CLEAN/AI PATTERNS FOUND/NEEDS REWRITE]
## LaTeX and Format: [COMPLIANT/ISSUES/NON-COMPLIANT]
## Compilation: [PASS/WARNINGS/FAIL]
## Voice Fidelity: [MATCH/DRIFT/NOT SCORED]
## Notation Consistency: [CONSISTENT/INCONSISTENCIES]

## Score Breakdown
- Starting: 100
- [Deductions with invariant citations]
- **Final: XX/100**

## Claim-Source Map Status
- Map exists: [YES/NO]
- Claims mapped: [X/Y]
- Broken links: [list]

## Escalation Status: [None / Strike N of 3]
```
