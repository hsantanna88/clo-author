# Reasoning Checks (Layer 2)

What parsing cannot reach. Each check reads `quality_reports/coherence/index.json`
— never the raw paper — so the model only ever sees pre-filtered candidate spans.
That is what keeps this layer cheap and what keeps it from wandering into
judgment.

**The rule for every check below:** a finding must be resolvable by pointing at
two places in the paper that cannot both be right. If resolving it requires an
opinion about whether the research is good, it is not a coherence finding — it
belongs to `/review`.

---

## R1 — Estimand drift

**Candidates.** Paragraphs whose `refs` include an `eq:` label, plus the
`\begin{equation}` body carrying that label.

**Ask.** Does the prose describe the same estimand the equation defines? Compare
the treatment variable, the unit of observation, the fixed-effect structure, the
comparison group, and the time window.

**Finds.** Text says "the effect of treatment on the treated" while the equation
is a pooled OLS interaction with no ATT weighting. Text says "controlling for
county-by-year fixed effects" while the equation has `\alpha_c + \gamma_t`.

**Not a finding.** The equation is correct but the design is questionable. That
is `/review --methods`.

---

## R2 — Claim strength vs evidence

**Candidates.** Paragraphs containing a strength word — large, substantial,
sizeable, strong, dramatic, striking, negligible, precise, robust — within the
same sentence as a number of kind `estimate`.

**Ask.** Does the estimate support the adjective, given the outcome's own scale
in the table (mean dependent variable, SD, or baseline row)?

**Finds.** "A substantial increase" attached to 0.02 SD. "Precisely estimated"
attached to a coefficient smaller than its standard error. "Robust across
specifications" where the cited columns flip sign.

**Not a finding.** A large effect the author calls large. Disagreement about
whether the magnitude is economically interesting — that is a referee's call.

**This is the one check most likely to overreach.** Require the contradiction to
be arithmetic (estimate vs its own SE, or vs the baseline in the same table),
not rhetorical.

---

## R3 — Cross-section contradiction

**Candidates.** Pair every paragraph in Data / Empirical Strategy that states a
sample restriction, a definition, or an assumption, against every paragraph in
Results / Robustness / Conclusion that restates it.

**Ask.** Do the two statements agree on the sample, the period, the treatment
definition, or the assumption?

**Finds.** Data section says the sample runs 2005–2012; conclusion says
"over the 2005–2015 period". Strategy says treatment is "share above 0.5";
robustness describes the baseline as "any activation".

**Not a finding.** A deliberate restriction stated once and varied on purpose in
a robustness check — the paper says it is varying it.

---

## R4 — Notation semantics (INV-7)

**Candidates.** Symbols appearing in more than one section's math, taken from
the index's equation bodies. The deterministic layer already catches macros
defined twice; this catches the same symbol *used* two ways.

**Ask.** Does each symbol carry one meaning throughout?

**Finds.** `\beta` is the treatment effect in Section 4 and a nuisance
coefficient in Section 6. `i` indexes individuals in the main equation and
municipalities in the event study. `\ell` is relative time in one place and a
lag order in another.

**Not a finding.** Conventional reuse the paper defines locally and explicitly
("in this subsection, $j$ indexes...").

---

## R5 — Unstated assumption

**Candidates.** Theory papers only. Every `proof` / `theorem` / `proposition` /
`lemma` environment body, paired with the assumptions block.

**Ask.** Does the proof invoke a property never stated in the theorem's
hypotheses or the paper's assumption list — continuity, monotonicity,
independence, an interior solution, a finite moment?

**Finds.** A proof differentiates a function never assumed differentiable. A
result relies on single-crossing that appears nowhere in the assumptions.

**Not a finding.** A standard step the field would not state. Flag only where
the missing assumption is load-bearing.

---

## R6 — Direction language

**Candidates.** Sentences containing a direction verb — increases, decreases,
raises, reduces, lowers, improves, worsens — with a number of kind `estimate`
that the deterministic layer already matched to a table cell.

**Ask.** Does the verb match the sign of the matched cell?

**Finds.** "SC reduces food insecurity by 4.9 percentage points" where the cell
is `+0.0489`. Sign flips of this kind survive proofreading because both halves
read fluently.

**Not a finding.** A reduction in a bad outcome described as an improvement, or
any case where the outcome's polarity makes the verb correct.

---

## Output

Return findings as JSON matching the deterministic layer's schema, with two
additions:

```json
{
  "check": "R2-claim-strength",
  "severity": "minor",
  "file": "paper/sections/results.tex",
  "line": 13,
  "message": "...",
  "evidence": "...",
  "suggestion": "...",
  "layer": "reasoning",
  "confidence": "high | medium | low"
}
```

Rules:

- **Two anchors or it is not a finding.** Cite the two locations that cannot
  both be right. A finding with one anchor is an opinion.
- `severity` never exceeds `minor`. Reasoning findings do not block.
- Emit nothing rather than something weak. An empty reasoning pass on a coherent
  paper is the correct output and should be reported as such.
- Do not restate deterministic findings. If the number already mismatched in
  Layer 1, R6 has nothing to add.
- Never edit the paper. This agent produces findings only.
