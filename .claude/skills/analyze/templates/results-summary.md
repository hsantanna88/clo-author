# Results Summary

**Project:** [project name]
**Date:** [YYYY-MM-DD]
**Scripts:** [list scripts that produced these results]

---

## Paper-to-Code Naming Map

| Paper Symbol | Code Name | Description |
|-------------|-----------|-------------|
| $Y_{it}$ | [name] | [outcome] |
| $D_{it}$ | [name] | [treatment] |
| $\hat{\beta}$ | [name] | [main coefficient] |

---

## Key Findings

| Result | Estimate | SE | 95% CI | p-value | N | Table/Figure |
|--------|----------|-----|--------|---------|---|-------------|
| Main effect | | | | | | Table X |
| [Heterogeneity 1] | | | | | | Table Y |
| [Heterogeneity 2] | | | | | | Table Y |

### Interpretation
- [One sentence: magnitude and direction of main effect]
- [One sentence: economic significance — what does the coefficient mean in real terms?]
- [One sentence: comparison to prior literature if available]

---

## Robustness

| Check | Result | Consistent with main? | Table/Figure |
|-------|--------|-----------------------|-------------|
| [Alternative controls] | | Yes / No / Partially | Table R1 |
| [Alternative sample] | | Yes / No / Partially | Table R1 |
| [Placebo test] | | Pass / Fail | Table R2 |
| [Alternative estimator] | | Yes / No / Partially | Table R3 |

### Robustness Assessment
- [One sentence: overall robustness pattern]
- [Flag any specification where results change materially]

---

## Descriptive Statistics

| Variable | N | Mean | SD | Min | Max |
|----------|---|------|----|-----|-----|
| [Outcome] | | | | | |
| [Treatment] | | | | | |
| [Key control 1] | | | | | |

---

## Data Notes

- **Sample size:** [N observations, N units, T periods]
- **Period:** [start year -- end year]
- **Key exclusions:** [list sample restrictions and how many observations each drops]
- **Missing data:** [how handled — dropped / imputed / indicator]
- **Merge rates:** [if applicable — N matched / N total]

---

## Flags and Anomalies

- [Any unexpected patterns, data quality issues, convergence problems]
- [Any results that the writer should caveat or investigate further]
- [Any deviations from the strategy memo and why]

---

## Output Files

### Tables
| File | Description | Paper location |
|------|-------------|---------------|
| `paper/tables/[name].tex` | [what it shows] | Table [N] |

### Figures
| File | Description | Paper location |
|------|-------------|---------------|
| `paper/figures/[name].pdf` | [what it shows] | Figure [N] |

### Intermediate Objects
| File | Description |
|------|-------------|
| `scripts/python/results/[nombre].npz` | [what it contains] |
