# Quiz format

Two files, always. The questions file never contains an answer, a hint, or a range.

---

## File 1 — `{script}_quiz.md`

```markdown
---
script: scripts/R/NN_name.R
fingerprint: a3f21c9b4e07
generated: YYYY-MM-DD
---

# Quiz: [script name]

Five questions. Pass is 4 of 5, and Q1 must be correct.
Answer from understanding — checking the script first defeats the purpose,
though checking it *after* is the whole point.

**Q1 (sample construction — blocking).**
[Question]

**Q2.**
[Question]

**Q3.**
[Question]

**Q4 (counterfactual).**
[Question]

**Q5.**
[Question]
```

## File 2 — `{script}_quiz_key.md`

```markdown
---
script: scripts/R/NN_name.R
fingerprint: a3f21c9b4e07
---

# Answer key — do not read before attempting

**Q1.** [Answer]
- **Trace:** `scripts/R/NN_name.R:112–128`
- **Credit:** CORRECT requires naming the restriction and the approximate share lost.
  PARTIAL if the restriction is right but the magnitude is off by more than 2×.
- **On a miss:** re-read explainer §1 (sample ledger).

[... one block per question ...]
```

---

## Writing good questions

**Q1 is always sample construction and always blocking.** Not "how many observations are there" —
that is lookup. Ask what the sample *is*, and what it cost:

> Which sample restriction drops the most observations, roughly what share does it drop, and is
> it in the strategy memo?

**Include at least one counterfactual.** Direction plus rough magnitude:

> If the balanced-panel requirement were dropped, does the main coefficient grow or shrink, and
> by roughly how much?

**Include at least one question the explainer does not directly answer.** It should require
joining two facts — a construction choice against a result, a drop count against a claim in the
draft:

> The paper says the effect is concentrated in small establishments. Given how `emp_size_bin` is
> built, what is the one timing problem with that claim?

**Calibrate to medium.** Answerable by someone who read the explainer and thought about it for
thirty seconds. Not a trick, not a recall test.

---

## Questions that are not allowed

| Bad question | Why |
|-------------|-----|
| "Which package estimates the main specification?" | Trivia. No decision hangs on it. |
| "How many lines is the cleaning section?" | Lookup. |
| "Did the merge drop about 11% of observations?" | Yes/no, and the answer is in the question. |
| "What does `feols` do?" | Not a delta. The author knows. |
| "What is the coefficient in column 3?" | Recall, not understanding — unless the question asks what it *implies*. |

---

## Grading

| Verdict | Standard |
|---------|----------|
| CORRECT | Right substance. Wording free, rounding free, "about a fifth" for 18% is fine. |
| PARTIAL | Right direction, wrong magnitude, or missing the mechanism. |
| INCORRECT | Wrong, or "I don't know." |

**Pass = 4 of 5 CORRECT or PARTIAL, with Q1 CORRECT.**

Grade strictly. A quiz everyone passes carries no information. Report the verdict, the correct
answer, and the trace for every question — including the ones they got right, since a right answer
for the wrong reason is worth catching.

A fail means: re-read the named explainer section, then try again. It never means the code is
wrong, and it never triggers a rewrite.
