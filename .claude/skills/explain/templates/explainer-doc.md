---
script: scripts/R/NN_name.R
fingerprint: [12-char sha256 prefix — python3 scripts/explainer_status.py --hash <script>]
generated: YYYY-MM-DD
strategy_memo: quality_reports/strategy/{project}/strategy_memo.md
---

# Explainer: [script name]

> Written as a delta against the strategy memo. If you have not read the memo, read it first —
> this document assumes it and explains only where the code departed from it, refined it, or
> decided something it left open.

## Headline

[Two or three sentences. What this script produces, and the one thing about it you do not
already know. If something here would surprise the author, it goes in this paragraph and
nowhere else.]

Example:
> Produces Table 2 (main DiD) and Figure 3 (event study) for the 2014 cohort. The thing to know:
> the balanced-panel requirement in §3 of the memo drops 18% of treated workers, and they are not
> a random 18% — they are disproportionately in establishments with fewer than 10 employees.

---

## 1. Sample construction ledger

| Step | Restriction | N before | N after | Dropped | Why |
|------|-------------|---------:|--------:|--------:|-----|
| 0 | Raw load, 2010–2019 | — | 41,203,884 | — | Source file as delivered |
| 1 | Age 18–64 | 41,203,884 | 38,110,442 | 3,093,442 | Memo §2.1 |
| 2 | Formal employment spell > 30 days | 38,110,442 | 35,884,109 | 2,226,333 | Memo §2.1 |
| 3 | Merge to municipality panel | 35,884,109 | 35,442,880 | 441,229 | 98.8% match; unmatched are pre-2012 codes |
| 4 | Balanced panel, 2012–2018 | 35,442,880 | 29,004,551 | 6,438,329 | **Not in the memo — see §3** |
| — | **Estimation sample** | | **29,004,551** | | Matches Table 2 N |

Rules for this table:

- One row per restriction, **in the order the code applies them**. Order changes the counts.
- Each row's `N after` is the next row's `N before`. No gaps.
- The final `N after` equals the N in the main results table. If it does not, that mismatch is
  the finding — state it in the Headline and stop.
- Counts come from the script's actual printed output. If the script does not print them, write
  `NOT INSTRUMENTED` in the count columns and flag it. Never estimate.
- Bold any restriction that is not in the strategy memo.

---

## 2. Variable construction

Only variables whose definition involved a choice. Skip anything mechanical.

| Paper notation | Code name | Construction |
|---------------|-----------|--------------|
| $w_{it}$ | `log_hourly_wage` | Monthly earnings ÷ contracted hours, deflated to **2014** BRL by IPCA, then logged. Zeros dropped (not winsorized) — 1,203 obs. |
| $D_{it}$ | `treated_post` | 1 from the calendar year of UPP installation onward, using the **installation** date, not the announcement date. |
| — | `emp_size_bin` | Establishment headcount in December, binned 1–9 / 10–49 / 50+. December, not annual mean — the annual mean straddles the treatment date. |

---

## 3. Judgment calls

Where the memo was silent and the code decided anyway.

**[Call 1 — one line title]**
- **Decided:** [what the code does]
- **Alternative not taken:** [the other reasonable choice]
- **Does it matter:** [checked / unchecked; if checked, the magnitude]

Example:
> **Balanced panel over 2012–2018**
> - **Decided:** kept only workers observed in every year of the window.
> - **Alternative not taken:** unbalanced panel with worker FE, which the memo's §3 language
>   arguably implies.
> - **Does it matter:** yes. Unbalanced moves the main coefficient from −0.043 to −0.031 — 28%
>   smaller in magnitude. State magnitude changes this way, not as a signed percentage: "−28%" is
>   ambiguous when the coefficient itself is negative.
>   Run as robustness column (4), but the main specification is the balanced one and the paper
>   does not currently say why.

---

## 4. What would change the answer

Two to four levers, each with a direction and — where known — a magnitude.

| Lever | Direction | Magnitude | Status |
|-------|-----------|-----------|--------|
| Unbalanced panel | Attenuates | −0.043 → −0.031 | Run, column (4) |
| Cluster at state not municipality | Widens SE | SE 0.011 → 0.019 | Run |
| Include 2019 (post-reform) | Unknown | — | **Not run** |

Never speculate about a magnitude for an unrun sensitivity. `Not run` is the entry.

---

## 5. Open questions

[What you are not confident about. An empty section here is almost always a lie.]

- [Question or uncertainty, and what would resolve it]

---

*Quiz: `quality_reports/explainers/{script}_quiz.md` — take it before this result leaves your desk.*
