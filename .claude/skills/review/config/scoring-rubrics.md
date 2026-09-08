# Scoring Rubrics -- All Critics

Consolidated deduction tables from all critic agents. Each critic starts at 100 and deducts for issues found. Floor at 0.

---

## Writer-Critic (Manuscript Review)

### Critical (blocking)

| Issue | Deduction |
|-------|-----------|
| Paper doesn't compile | -20 |
| Causal language without identification (INV-8) | -20 |
| No claim-source map (INV-27) | -15 |
| Numbers in text don't match tables (INV-11) | -10 per, max -30 |
| Strategy section misrepresents the actual design | -15 |
| Missing table notes on any table (INV-1) | -5 per, max -15 |
| Missing figure notes on any figure (INV-2) | -5 per, max -15 |

### Major (quality)

| Issue | Deduction |
|-------|-----------|
| Voice tone mismatch (when style guide exists) | -10 |
| AI vocabulary (3+ instances) | -2 per, max -10 |
| Missing JEL codes or keywords (INV-6) | -5 |
| Claim-source map entries missing | -5 per, max -20 |
| Broken links in claim-source map | -10 per |
| Sentence length median off by >5 words | -5 |
| Wrong document class or formatting | -5 |
| Uniform sentence length (no variation) | -5 |

### Minor (polish)

| Issue | Deduction |
|-------|-----------|
| Filler phrases | -2 per, max -6 |
| Announcements | -2 per, max -6 |
| Em dash overuse | -3 |
| Rule of three | -3 |
| Paragraph openings don't match style guide | -3 per, max -9 |
| Unresolved references | -3 per |
| Overfull hbox warnings | -1 per, max -5 |

---

## Coder-Critic (Code Review)

### Critical (strategic)

| Issue | Deduction |
|-------|-----------|
| Domain-specific bugs (clustering, estimand) | -30 |
| Code doesn't match strategy memo | -25 |
| Scripts don't run | -25 |
| Sign of main result implausible | -20 |
| Hardcoded absolute paths | -20 |
| Missing robustness checks from memo | -15 |
| Wrong clustering level | -15 |
| Optimizer didn't converge (structural) | -15 |
| No paper-to-code naming map | -10 |

### Major (code quality)

| Issue | Deduction |
|-------|-----------|
| No `set.seed()` / not reproducible | -10 |
| Missing RDS saves | -10 |
| Float comparison with `==` | -10 |
| No CDF clamping (when computing CDFs) | -10 |
| No inverse link guards | -10 |
| Magnitude implausible (10x literature) | -10 |
| Missing outputs (tables/figures) | -10 |
| Growing lists in loops (no pre-allocation) | -5 |
| Missing function preconditions (`stopifnot`) | -5 |

### Minor (polish)

| Issue | Deduction |
|-------|-----------|
| Missing figure/table generation | -5 |
| Non-reproducible output | -5 |
| Stale outputs | -5 |
| No documentation headers | -5 |
| No project layout (no numbered scripts) | -5 |
| Console output pollution | -3 |
| Poor comment quality | -3 |
| Inconsistent style | -2 |
| Prohibited patterns (LOW severity) | -1 per |

---

## Strategist-Critic (Causal Audit)

The strategist-critic does not use a point-deduction rubric. Instead, it classifies issues by severity:

| Severity | Definition |
|----------|-----------|
| **CRITICAL** | Identification is wrong or unsupported. Fatal design flaw. |
| **MAJOR** | Missing important check or wrong inference. Should fix before publication. |
| **MINOR** | Could strengthen but paper works without it. Nice to have. |

**Overall assessment scale:**
- **SOUND** -- Design is valid, implementation is correct
- **MINOR ISSUES** -- Fixable concerns, none threatening core results
- **MAJOR ISSUES** -- Significant concerns that could change conclusions
- **CRITICAL ERRORS** -- Fundamental design flaw or incorrect implementation

**Proportional criticism principle:** A working paper missing Oster bounds is MINOR. A paper with violated parallel trends is CRITICAL.

---

## Theorist-Critic (Theory Review)

| Category | Issue | Deduction |
|----------|-------|-----------|
| **Proof validity** | Step does not follow / gap in logic | -20 per gap |
| | Circular argument | -25 |
| | Unjustified limit/expectation interchange | -10 per instance |
| | Uniform convergence claim without Donsker / VC / bracketing argument | -10 |
| | Taylor remainder not shown to be $o_p/O_p$ at claimed rate | -10 per instance |
| | Rate arithmetic wrong | -15 |
| **Identification** | Substitution from counterfactual to observable is unjustified | -20 |
| | Design invariant invoked without being stated (parallel trends / exclusion / monotonicity / continuity) | -15 |
| **Statements** | Over-claim (conclusion exceeds what proof supports) | -15 |
| | Under-claim (proof supports strictly more) | -3 |
| | Pointwise vs. uniform conflation | -10 |
| **Assumptions** | Assumption never used in the proof | -5 per assumption |
| | Assumption not interpreted (no plain-language gloss) | -3 per assumption |
| | High-level condition with no primitive counterpart and no justification | -5 |
| | Non-minimal (strictly stronger than needed, with no rationale) | -5 |
| **Notation (INV-7)** | Symbol used with two meanings | -5 per symbol |
| | Symbol used before definition | -3 per instance |
| | Inconsistency with paper's empirical sections or domain-profile notation | -5 |
| **Citations** | Cited result doesn't apply (wrong version, wrong assumptions) | -10 per instance |
| | Wrong journal/year for a named result | -3 per instance |
| | Missing citation for a named result that was invoked | -5 per instance |
| **Linkage** | Orphan theorem (not used elsewhere) | -3 |
| | Orphan claim (stated in paper, not supported by any theorem) | -10 |
| **Exposition** | Proof strategy missing | -3 |
| | Appendix reference broken | -2 |
| | Theorem environment doesn't match preamble | -2 |

---

## Storyteller-Critic (Talk Review)

**Advisory -- non-blocking.** Talk scores do not gate commits or PRs.

| Issue | Deduction |
|-------|-----------|
| Slides don't compile | -20 |
| Numbers don't match paper | -20 |
| Wrong narrative arc for paper type | -15 |
| No hook in first 2 slides | -15 |
| Talk wrong length for format | -15 |
| Structural talk missing counterfactual slide | -10 |
| Theory talk missing distinguishing prediction | -10 |
| Text overflow | -10 per slide (max -30) |
| Missing backup slides | -5 |
| Inconsistent notation with paper | -5 |
| Font too small for projection | -3 per slide |
| Slide tries to do two things | -2 per slide |

---

## Librarian-Critic (Literature Review)

| Issue | Deduction |
|-------|-----------|
| Missing seminal paper in the field | -20 |
| No coverage of methods literature | -15 |
| Over-reliance on working papers (>50%) | -10 |
| Missing recent papers (last 2 years) | -10 |
| Scope too narrow | -10 |
| No frontier map / gap identification | -10 |
| Proximity scores inconsistent | -5 |
| Missing BibTeX entries | -5 per paper |

---

## Explorer-Critic (Data Assessment Review)

| Issue | Deduction |
|-------|-----------|
| Proposed variable doesn't measure the concept | -25 |
| Major sample selection issue unaddressed | -20 |
| Better dataset exists and was missed | -15 |
| No discussion of measurement error | -10 |
| Access timeline unrealistic | -10 |
| Missing identification compatibility check | -10 |
| No discussion of external validity | -5 |

---

## Quality Gates

| Gate | Overall Score | Per-Component Minimum |
|------|--------------|----------------------|
| Commit | >= 80 | None enforced |
| PR | >= 90 | None enforced |
| Submission | >= 95 | >= 80 per component |
| Below 80 | < 80 | Blocked |

Talk scores are advisory and do not block pipeline progression.
