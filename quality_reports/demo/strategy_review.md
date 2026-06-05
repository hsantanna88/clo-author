# Strategy Review: LLM Adoption and Labor Market Outcomes

**Date:** 2026-04-10 **Reviewer:** strategist-critic

## Phase 1: Claim Identification

- **Paper type:** Reduced-form
- **Design:** DiD + shift-share exposure measure
- **Estimand:** ATT of LLM exposure on occupation-level employment growth
- **Treatment:** Occupational exposure to GPT capabilities (continuous, interacted with post-ChatGPT indicator)
- **Control:** Low-exposure occupations (bottom two quintiles of Felten et al. 2023 index)
- **Outcomes:** Employment share, hourly wages, task composition (routine cognitive share)

## Phase 2: Core Design Validity

### Design Check: Shift-Share DiD

**Assessment:** CONCERNS

#### Issues Found: 3

##### Issue 2.1: Exposure index conflates displacement and augmentation channels

- **Location:** paper/sections/empirical_strategy.tex:38-52
- **Severity:** CRITICAL
- **Problem:** The Felten et al. (2023) AIOE index measures which tasks *can be* performed by AI, not whether AI *substitutes for* or *complements* human workers on those tasks. A coder with high exposure could be displaced (firm replaces coder with Copilot) or augmented (coder becomes 2x productive, firm hires more). The paper treats all exposure as displacement without justification. The estimand is therefore ambiguous — the coefficient captures a net effect that cannot be signed ex ante.
- **Suggested fix:** Decompose exposure into substitution score (tasks where AI output directly replaces human output — e.g., translation, data entry) and complementarity score (tasks where AI assists humans — e.g., coding, analysis, writing). Eloundou et al. (2023) Table 1 provides task-level labels that enable this decomposition. Estimate separate effects for each component. The headline result should be: "displacement concentrates in high-substitution occupations" — not "high-exposure occupations lose employment."

##### Issue 2.2: Pre-trends starting 2019 undermine parallel trends

- **Location:** paper/figures/event_study_employment.pdf; paper/sections/results.tex:67-74
- **Severity:** CRITICAL
- **Problem:** Event study coefficients for Q5 (highest exposure) vs. Q1 (lowest exposure) show a negative trajectory beginning 2019Q3 — more than 3 years before ChatGPT's launch (November 2022). The paper attributes this to COVID disproportionately affecting office/admin workers but provides no formal test. If high-exposure occupations were already declining due to pre-LLM automation (RPA, cloud-based tools), the DiD estimate captures a secular trend, not a ChatGPT effect.
- **Suggested fix:** (a) Rambachan & Roth (2023) sensitivity analysis with `HonestDiD` — report the breakdown value (how steep a linear pre-trend violation zeroes out the effect). (b) Control for pre-period automation exposure (robot/RPA penetration from Acemoglu & Restrepo 2020) interacted with time. (c) Test for a level shift: does the coefficient on exposure *accelerate* after 2022Q4 relative to the pre-existing trend? A trend break is far more convincing than a level in the presence of pre-trends.

##### Issue 2.3: Result driven by narrow set of occupations

- **Location:** scripts/02_estimate_main.R:89-112
- **Severity:** MAJOR
- **Problem:** The top-quintile exposure group is dominated by three 2-digit SOC groups: Office & Administrative Support (SOC 43), Legal Support (SOC 23), and Translation/Interpretation (SOC 27-3091). Together these account for 61% of the employment decline. Dropping any single group reduces significance below 5%. The paper is not estimating "the effect of LLMs on exposed occupations" — it is estimating "the effect on office admin, paralegals, and translators," which is a much narrower claim.
- **Suggested fix:** (a) Report Goldsmith-Pinkham et al. (2020) Rotemberg weights explicitly — which occupations have the largest influence? (b) Report leave-one-out estimates dropping each of the top-5 weight occupations. (c) Reframe the finding honestly: if the effect is driven by three occupation groups, say so and explain why these groups are first-order for the LLM displacement question. A narrow but honest result beats a broad but fragile one.

### Sanity Check

- **Sign:** Ambiguous. Paper finds negative employment, but Brynjolfsson et al. (2025) and Noy & Zhang (2023) find augmentation in high-exposure roles. Sign depends on whether substitution or complementarity dominates — which is exactly what the paper doesn't decompose.
- **Magnitude:** Questionable. 3.2pp employment decline in 18 months across all top-quintile occupations. For context, the PC revolution took roughly a decade to produce comparable displacement in clerical occupations (Autor, Levy & Murnane 2003). Either LLMs are dramatically faster-acting or the estimate includes confounds.
- **Dynamics:** Concerning. Effects appear immediately at 2022Q4 with no buildup. But firm-level AI adoption was gradual (Zolas et al. 2024 show enterprise adoption took 6-12 months after ChatGPT). Immediate occupation-level effects with gradual firm-level adoption is inconsistent.
- **Consistency:** Fragile. The employment result does not survive: (a) controlling for remote work feasibility (Dingel & Neiman 2020), (b) state-by-quarter fixed effects, or (c) dropping office/admin workers. Wage effects are uniformly zero. This pattern — fragile employment effect with zero wage effect — is more consistent with measurement noise than displacement.

## Phase 3: Inference

### Issues Found: 2

##### Issue 3.1: Shift-share standard errors need correction

- **Location:** paper/sections/empirical_strategy.tex:58; scripts/02_estimate_main.R:95
- **Severity:** MAJOR
- **Problem:** Standard errors are clustered at the occupation level (N=460 6-digit SOC codes). In a shift-share design where the shocks (GPT release timing) are common across occupations, cross-occupation residual correlation is mechanically induced. Adao, Kolesar & Morales (2019) show that conventional cluster-robust SEs are biased downward in this setting.
- **Suggested fix:** Implement Adao et al. (2019) exposure-robust SEs. The `ShiftShareSE` R package computes these directly. If significance disappears under corrected SEs, this is informative.

##### Issue 3.2: Multiple testing across outcome variables

- **Location:** paper/tables/table2_main_results.tex
- **Severity:** MINOR
- **Problem:** Three primary outcomes (employment, wages, task composition) tested without multiple testing adjustment. Employment is significant, wages are not, task composition is marginal. With 3 tests, the employment result's effective p-value is higher than reported.
- **Suggested fix:** Report Romano-Wolf adjusted p-values across the three outcomes. Or pre-specify employment as the primary outcome with wages and task composition as secondary.

## Phase 4: Polish & Completeness

### Issues Found: 2

##### Issue 4.1: Missing placebo test with pre-LLM AI exposure

- **Location:** paper/sections/robustness.tex
- **Severity:** MINOR
- **Problem:** A powerful placebo: assign the 2023 GPT exposure scores to the 2012-2018 period and estimate the same model. If the exposure index predicts employment changes before LLMs existed, the index is capturing something about these occupations other than LLM exposure (e.g., susceptibility to any form of automation).
- **Suggested fix:** Add this placebo. If null, it strengthens identification. If significant, it reveals that the exposure index captures general automation vulnerability, which fundamentally changes the paper's interpretation.

##### Issue 4.2: No discussion of measurement error in exposure index

- **Location:** paper/sections/data.tex:43
- **Severity:** MINOR
- **Problem:** The GPT-4 self-assessment of its own capabilities (used to construct the exposure index) is subject to systematic bias. GPT-4 likely overestimates its ability on tasks it performs poorly (Dunning-Kruger for LLMs) and underestimates capabilities it wasn't prompted to demonstrate. Webb (2020) provides an alternative patent-based measure. No discussion of this.
- **Suggested fix:** Report results using Webb (2020) patent-based automation exposure as an alternative measure. Discuss the direction of bias from self-assessment. If results are robust to the alternative measure, this concern is mitigated.

## Summary

- **Overall assessment:** MAJOR ISSUES
- **Critical issues (must fix):** 2 (exposure decomposition, pre-trends)
- **Major issues (should fix):** 2 (narrow occupation drivers, shift-share SEs)
- **Minor issues (consider):** 3 (multiple testing, placebo test, measurement error)

## Priority Recommendations

1.  **\[CRITICAL\]** Decompose exposure into substitution vs. complementarity. This single change reframes the paper from "LLMs reduce employment" (uninterpretable) to "LLM *substitution* reduces employment in X occupations while LLM *complementarity* increases productivity in Y occupations" (interpretable, novel, policy-relevant). Highest-value revision.
2.  **\[CRITICAL\]** Address pre-trends with Rambachan & Roth (2023) and test for an acceleration post-ChatGPT. If the effect is just a continuation of the 2019 trend, the paper's causal claim does not hold.
3.  **\[MAJOR\]** Report shift-share diagnostics (Rotemberg weights, leave-one-out, Adao et al. SEs). Be transparent about which occupations drive the result.

## Positive Findings

- The data construction is a genuine contribution. Linking O\*NET task descriptions → GPT capability scores → CPS employment outcomes at the occupation-by-quarter level creates a panel dataset that will be used by others regardless of this paper's specific results.
- The choice to study occupation-level outcomes (rather than firm- or individual-level) is a deliberate scale choice that complements the firm-level studies (Brynjolfsson et al. 2025). The paper should frame this as a feature: occupation-level analysis captures equilibrium reallocation that firm-level studies miss.
- The event study figures are well-constructed — clear, properly labeled, with confidence bands. The pre-trend is visually obvious, which is honest presentation even though it creates an identification problem.